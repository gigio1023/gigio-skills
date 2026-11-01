"""Render a release note as one self-contained HTML file: inline CSS and inline SVG.

The same file is the HTML deliverable and the source the PDF renderer prints.
Section order: identity, summary, counts that reconcile, required actions,
figures, material changes as as-is and to-be pairs, the ID mapping, extra
sections, open questions, the full change index, and the source of the
numbers. Every piece of text from note.json or diff.json is escaped.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from _errors import NoteSourceError
from _inline import bound_number, escape_text, render_html
from _note_content import CardField, DiffPiece, FieldEntry, NoteContent
from _note_source import ChangeView, Figure, FigureType, Highlight
from _svg_charts import (
    DumbbellKey,
    Palette,
    change_kind_bars,
    embedded_svg,
    mark_svg,
    pair_dumbbell,
)

ASSETS: Path = Path(__file__).resolve().parent.parent / "assets"
KEEP_ROWS: int = 12  # about a third of a page at 9 pt; longer tables break between rows


def render_document(content: NoteContent) -> str:
    template: str = (ASSETS / "note.html").read_text(encoding="utf-8")
    css: str = (ASSETS / "note.css").read_text(encoding="utf-8")
    palette: Palette = Palette.from_css(css)
    title: str = _plain_title(content)
    replacements: dict[str, str] = {
        "@@LANG@@": content.note.lang,
        "@@TITLE@@": html.escape(title),
        "@@CSS@@": css,
        "@@PAGE_CSS@@": _page_css(title, palette),
        "@@BODY@@": _body(content, palette),
    }
    for slot, value in replacements.items():
        template = template.replace(slot, value)
    return template


def _plain_title(content: NoteContent) -> str:
    # The <title> and running header take plain text, so inline markup is rendered and tags dropped.
    return html.unescape(_strip_tags(render_html(content.note.title, content.diff)))


def _page_css(title: str, palette: Palette) -> str:
    # Margin boxes get literal values: custom properties from :root do not reach the page context.
    quoted: str = title.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    margin_font: str = f"8pt {palette.font}"
    return (
        "@page { size: A4; margin: 18mm 16mm 20mm 16mm;\n"
        f'  @top-left {{ content: "{quoted}"; font: {margin_font}; color: {palette.ink_2}; }}\n'
        f'  @bottom-right {{ content: counter(page) " / " counter(pages); font: {margin_font}; color: {palette.ink_2}; }} }}\n'
        "@page :first { @top-left { content: none; } }"
    )


def _body(content: NoteContent, palette: Palette) -> str:
    note, s, diff = content.note, content.s, content.diff

    def r(text: str) -> str:
        return render_html(text, diff)

    out: list[str] = ["<header>", f'<p class="kicker">{html.escape(s["kicker"])}</p>', f"<h1>{r(note.title)}</h1>"]
    if note.subtitle:
        out.append(f'<p class="subtitle">{r(note.subtitle)}</p>')
    out.append(_meta(content))
    out.append("</header>")
    out.append('<section class="summary">' + "".join(f"<p>{r(p)}</p>" for p in note.summary) + "</section>")
    out.append(_stats(content))
    out.append(f'<p class="reconcile">{html.escape(" ".join(content.reconcile_sentences()))}</p>')
    out.append(f"<h2>{html.escape(s['h_actions'])}</h2>")
    if note.actions:
        # The colon keeps role and action apart in extracted text and Markdown, where bold is lost.
        items: str = "".join(f"<li><strong>{r(a.who)}:</strong> {r(a.what)}</li>" for a in note.actions)
        out.append(f'<ul class="actions">{items}</ul>')
    else:
        out.append(f"<p>{html.escape(s['no_actions'])}</p>")
    if note.figures:
        out.append(f"<h2>{html.escape(s['h_glance'])}</h2>")
        out.extend(_figure(content, figure, palette) for figure in note.figures)
    if note.changes:
        out.append(f"<h2>{html.escape(s['h_changes'])}</h2>")
        out.extend(_highlight(content, change, palette) for change in note.changes)
    if note.field_list is not None:
        entries = content.field_list(note.field_list)
        if entries:
            heading: str = s["h_field_list"].format(field=content.field_label(note.field_list))
            out.append(f"<h2>{html.escape(heading)}</h2>" + "".join(_field_entry(content, e, note.field_list, palette) for e in entries))
    mapping: list[tuple[str, str, str, str]] = content.mapping_rows()
    if mapping:
        out.append(f"<h2>{html.escape(s['h_mapping'])}</h2>")
        out.append(_table([s["col_id"], s["as_is"], s["to_be"], s["col_change"]], [[escape_text(v, diff) for v in row] for row in mapping]))
    for section in note.sections:
        out.append(f"<h2>{r(section.heading)}</h2>" + "".join(f"<p>{r(p)}</p>" for p in section.paragraphs))
    if note.open_questions:
        out.append(f"<h2>{html.escape(s['h_questions'])}</h2>")
        out.append("<ul>" + "".join(f"<li>{r(q)}</li>" for q in note.open_questions) + "</ul>")
    out.append(f"<h2>{html.escape(s['h_index'])}</h2>")
    headers: list[str] = [s["col_id"], s["col_name"], s["col_change"]] + ([s["col_why"]] if content.shows_reasons() else [])
    index: list[list[str]] = [[r(v) if i == 3 else escape_text(v, diff) for i, v in enumerate(row)] for row in content.index_rows()]
    out.append(_table(headers, index))
    out.append(_source(content))
    return "\n".join(out)


def _meta(content: NoteContent) -> str:
    s, doc = content.s, content.diff.document
    cells: list[tuple[str, str]] = [
        (s["as_is"], " ".join(v for v in (doc["old"]["label"], doc["old"].get("ref")) if v)),
        (s["to_be"], " ".join(v for v in (doc["new"]["label"], doc["new"].get("ref")) if v)),
    ]
    if doc.get("date"):
        cells.append((s["released"], doc["date"]))
    inner: str = "".join(f"<div><span>{html.escape(k)}</span>{html.escape(v)}</div>" for k, v in cells)
    return f'<div class="meta">{inner}</div>'


def _stats(content: NoteContent) -> str:
    """Count tiles; each removal kind gets its own tile so no count mixes merges with removals."""
    tiles: list[str] = []
    for tile in content.tiles():
        value: str = " \u2192 ".join(bound_number(path, content.diff.resolve(path)) for path in tile.paths)
        label_path: str = html.escape(tile.paths[-1], quote=True)
        tiles.append(f'<div class="stat {tile.tone}"><b>{value}</b>'
                     f'<span data-label="{label_path}">{html.escape(tile.label)}</span></div>')
    return f'<section class="stats n{len(tiles)}">{"".join(tiles)}</section>'


def _figure(content: NoteContent, figure: Figure, palette: Palette) -> str:
    s, diff = content.s, content.diff
    title_html: str = render_html(figure.title, diff)
    title_text: str = html.unescape(_strip_tags(title_html))
    caption: str = render_html(figure.caption, diff)
    key = DumbbellKey(s["as_is"], s["to_be"], s["key_same"], diff.old_label, diff.new_label)
    if figure.type is FigureType.CHANGE_KINDS:
        svg: str = change_kind_bars(content.kind_bars(), content.bars_aria(title_text), palette)
        caption += " " + html.escape(s["kinds_overlap"])
    elif figure.type is FigureType.GROUP_DUMBBELL:
        rows = content.group_rows()
        svg = pair_dumbbell(rows, key, content.pairs_aria(title_text, rows), palette)
    elif figure.type is FigureType.FIELD_DUMBBELL:
        rows = content.field_rows(figure.field or "")
        svg = pair_dumbbell(rows, key, content.pairs_aria(title_text, rows), palette)
    elif figure.src is not None and figure.alt is not None:
        svg = embedded_svg(figure.src, html.unescape(_strip_tags(render_html(figure.alt, diff))))
    else:
        raise NoteSourceError(f"figure {title_text!r}: an svg figure needs src and alt")
    return f'<figure><p class="fig-title">{title_html}</p>{svg}<figcaption>{caption}</figcaption></figure>'


def _head(content: NoteContent, side: str, palette: Palette, extra: str = "") -> str:
    """A card head: the chart's hollow or filled mark, the side and version, so the pair reads in grayscale."""
    word: str = content.s["as_is"] if side == "old" else content.s["to_be"]
    label: str = content.diff.old_label if side == "old" else content.diff.new_label
    tail: str = f"<br>{extra}" if extra else ""
    return f'<p class="card-head">{mark_svg(palette, side)}{html.escape(word + " " + label)}{tail}</p>'


def _highlight(content: NoteContent, change: Highlight, palette: Palette) -> str:
    s, diff = content.s, content.diff
    head: str = f'<h3><span class="id">{html.escape(change.id)}</span> {render_html(change.title, diff)}</h3>'
    if change.view is ChangeView.TEXT_DIFF:
        before, after = content.text_diff(change.id, change.field or "")
        body: str = _diff_block(content, before, after, content.field_label(change.field or ""), palette)
    else:
        body = _cards(content, change.id, palette)
    why: str = f'<p class="why"><strong>{html.escape(s["why"])}:</strong> {render_html(change.why, diff)}</p>'
    impact: str = f'<p class="impact"><strong>{html.escape(s["impact"])}:</strong> {render_html(change.impact, diff)}</p>'
    figure: str = _figure(content, change.figure, palette) if change.figure is not None else ""
    return f'<section class="change">{head}{body}{why}{impact}{figure}</section>'


def _cards(content: NoteContent, record_id: str, palette: Palette) -> str:
    """As-is and to-be cards; a merged or replaced record shows each successor's fields on the to-be side."""
    s, diff = content.s, content.diff
    fields, section, _ = content.card_fields(record_id)

    def rows(items: list[CardField], side: str) -> str:
        return "".join(
            f'<dt>{html.escape(f.label)}</dt><dd class="{"diff" if f.changed else "same"}">'
            f'{escape_text((f.old if side == "old" else f.new) or "", diff)}</dd>' for f in items)

    successors: list[tuple[str, list[CardField]]] = content.successor_fields(record_id) if section == "removed" else []
    if successors:
        # The as-is card marks the fields that differ from any successor shown beside it.
        fields = [CardField(f.label, f.old, f.new, any(items[i].changed for _, items in successors))
                  for i, f in enumerate(fields)]
    if section == "added":
        old_card: str = f'<div class="card">{_head(content, "old", palette)}<p class="absent">{html.escape(s["not_in"].format(label=diff.old_label))}</p></div>'
    else:
        old_card = f'<div class="card">{_head(content, "old", palette)}<dl>{rows(fields, "old")}</dl></div>'
    if successors:
        status: str = escape_text(content.change_labels(record_id)[0], diff)
        blocks: str = "".join(f'<p class="successor">{escape_text(title, diff)}</p><dl>{rows(items, "new")}</dl>'
                              for title, items in successors)
        new_card: str = f'<div class="card to-be">{_head(content, "new", palette, status)}{blocks}</div>'
    elif section == "removed":
        new_card = f'<div class="card to-be">{_head(content, "new", palette)}<p class="absent">{html.escape(s["not_in"].format(label=diff.new_label))}</p></div>'
    else:
        new_card = f'<div class="card to-be">{_head(content, "new", palette)}<dl>{rows(fields, "new")}</dl></div>'
    return f'<div class="pair">{old_card}{new_card}</div>'


def _diff_block(content: NoteContent, before: list[DiffPiece], after: list[DiffPiece], field_label: str, palette: Palette) -> str:
    tag: dict[str, str] = {"same": "", "removed": "del", "added": "ins"}

    def pieces(items: list[DiffPiece]) -> str:
        return "".join(f"<{tag[p.op]}>{escape_text(p.text, content.diff)}</{tag[p.op]}>" if tag[p.op]
                       else escape_text(p.text, content.diff) for p in items)

    label: str = html.escape(field_label)
    return (f'<div class="textdiff">{_head(content, "old", palette, label)}<p>{pieces(before)}</p>'
            f'{_head(content, "new", palette, label)}<p>{pieces(after)}</p></div>')


def _field_entry(content: NoteContent, entry: FieldEntry, field: str, palette: Palette) -> str:
    """One record of the field list: both values with the word-level change, or the new value of an added record."""
    title: str = f'<p class="entry-title">{escape_text(entry.title, content.diff)}</p>'
    if entry.section == "added":
        absent: str = html.escape(content.s["not_in"].format(label=content.diff.old_label))
        block: str = (f'<div class="textdiff">{_head(content, "old", palette)}<p>{absent}</p>'
                      f'{_head(content, "new", palette)}<p>{escape_text(entry.new or "", content.diff)}</p></div>')
    else:
        before, after = content.text_diff(entry.record_id, field)
        block = _diff_block(content, before, after, "", palette)
    return f'<section class="field-entry">{title}{block}</section>'


def _table(headers: list[str], rows: list[list[str]]) -> str:
    """A borderless table; cells arrive as HTML, already escaped, and the first column holds IDs."""
    head: str = "".join(f'<th scope="col">{html.escape(h)}</th>' for h in headers)
    body: str = "".join(
        "<tr>" + "".join(f'<td class="id">{c}</td>' if i == 0 else f"<td>{c}</td>" for i, c in enumerate(row)) + "</tr>"
        for row in rows
    )
    # A short table stays on one page, so a heading never sits above a lone first row.
    keep: str = ' class="keep"' if len(rows) <= KEEP_ROWS else ""
    return f"<table{keep}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _source(content: NoteContent) -> str:
    s, doc = content.s, content.diff.document

    def version(side: str) -> str:
        parts: list[str] = [doc[side]["source"], doc[side].get("ref") or ""]
        return " ".join(p for p in parts if p)

    rows: list[tuple[str, str]] = [
        (html.escape(s["src_data"]), html.escape(content.diff.path.name)),
        (html.escape(s["as_is"]), html.escape(version("old"))),
        (html.escape(s["to_be"]), html.escape(version("new"))),
        (html.escape(s["src_tool"]), "version_diff.py"),
        (html.escape(s["src_minor"]), html.escape(s["minor_rule"])),
    ]
    # Links print as rows with the address visible, so a printed copy still shows where they lead.
    rows += [(render_html(link.label, content.diff), f'<a href="{html.escape(link.url, quote=True)}">{html.escape(link.url)}</a>')
             for link in content.note.links]
    items: str = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    return f'<section class="source"><h2>{html.escape(s["h_source"])}</h2><dl>{items}</dl></section>'


def _strip_tags(markup: str) -> str:
    return re.sub(r"<[^>]+>", "", markup)
