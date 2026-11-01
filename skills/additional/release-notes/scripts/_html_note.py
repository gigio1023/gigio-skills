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
from _note_content import DiffPiece, NoteContent
from _note_source import ChangeView, Figure, FigureType, Highlight
from _svg_charts import Palette, change_kind_bars, embedded_svg, pair_dumbbell

ASSETS: Path = Path(__file__).resolve().parent.parent / "assets"


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
        f'  @bottom-right {{ content: counter(page) " / " counter(pages); font: {margin_font}; color: {palette.ink_2}; }} }}'
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
    out.append(f'<p class="reconcile">{html.escape(content.reconcile_sentence())}</p>')
    out.append(f"<h2>{html.escape(s['h_actions'])}</h2>")
    if note.actions:
        items: str = "".join(f"<li><strong>{r(a.who)}</strong> {r(a.what)}</li>" for a in note.actions)
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
        heading: str = s["h_field_list"].format(field=content.field_label(note.field_list).lower())
        items: str = "".join(f"<dt>{escape_text(name, diff)}</dt><dd>{escape_text(value, diff)}</dd>"
                             for name, value in content.field_list(note.field_list))
        out.append(f'<h2>{html.escape(heading)}</h2><dl class="field-list">{items}</dl>')
    mapping: list[tuple[str, str, str, str]] = content.mapping_rows()
    if mapping:
        out.append(f"<h2>{html.escape(s['h_mapping'])}</h2>")
        headers: list[str] = [s["col_id"], s["as_is"], s["to_be"], s["col_change"]]
        cells: list[list[str]] = [[escape_text(v, diff) for v in row] for row in mapping]
        if note.reasons:
            headers.append(s["col_why"])
            for row, cell in zip(mapping, cells, strict=True):
                reason: str | None = note.reasons.get(row[0])
                cell.append(r(reason) if reason else html.escape(s["not_recorded"]))
        out.append(_table(headers, cells))
    for section in note.sections:
        out.append(f"<h2>{r(section.heading)}</h2>" + "".join(f"<p>{r(p)}</p>" for p in section.paragraphs))
    if note.open_questions:
        out.append(f"<h2>{html.escape(s['h_questions'])}</h2>")
        out.append("<ul>" + "".join(f"<li>{r(q)}</li>" for q in note.open_questions) + "</ul>")
    out.append(f"<h2>{html.escape(s['h_index'])}</h2>")
    index: list[list[str]] = [[escape_text(v, diff) for v in row] for row in content.index_rows()]
    out.append(_table([s["col_id"], s["col_name"], s["col_change"]], index))
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
    s, c = content.s, content.diff.counts
    tiles: list[tuple[str, str, str]] = [
        ("", s["stat_records"], f"{bound_number('counts.before', c['before'])} \u2192 {bound_number('counts.after', c['after'])}"),
        ("added", s["stat_added"], bound_number("counts.added", c["added"])),
        ("removed", s["stat_removed"], bound_number("counts.removed", c["removed"])),
        ("", s["stat_changed"], bound_number("counts.changed", c["changed"])),
    ]
    inner: str = "".join(
        f'<div class="stat {cls}"><b>{value}</b><span>{html.escape(label)}</span></div>' for cls, label, value in tiles
    )
    return f'<section class="stats">{inner}</section>'


def _figure(content: NoteContent, figure: Figure, palette: Palette) -> str:
    s, diff = content.s, content.diff
    title_html: str = render_html(figure.title, diff)
    title_text: str = html.unescape(_strip_tags(title_html))
    caption: str = render_html(figure.caption, diff)
    if figure.type is FigureType.CHANGE_KINDS:
        svg: str = change_kind_bars(content.kind_bars(), content.bars_aria(title_text), palette)
        caption += " " + html.escape(s["kinds_overlap"])
    elif figure.type is FigureType.GROUP_DUMBBELL:
        rows = content.group_rows()
        svg = pair_dumbbell(rows, _key(content, "old"), _key(content, "new"), content.pairs_aria(title_text, rows), palette)
    elif figure.type is FigureType.FIELD_DUMBBELL:
        rows = content.field_rows(figure.field or "")
        svg = pair_dumbbell(rows, _key(content, "old"), _key(content, "new"), content.pairs_aria(title_text, rows), palette)
    elif figure.src is not None and figure.alt is not None:
        svg = embedded_svg(figure.src, html.unescape(_strip_tags(render_html(figure.alt, diff))))
    else:
        raise NoteSourceError(f"figure {title_text!r}: an svg figure needs src and alt")
    return f'<figure><p class="fig-title">{title_html}</p>{svg}<figcaption>{caption}</figcaption></figure>'


def _key(content: NoteContent, side: str) -> str:
    word: str = content.s["as_is"] if side == "old" else content.s["to_be"]
    return f"{content.diff.document[side]['label']} {word}"


def _highlight(content: NoteContent, change: Highlight, palette: Palette) -> str:
    s, diff = content.s, content.diff
    head: str = f'<h3><span class="id">{html.escape(change.id)}</span> {render_html(change.title, diff)}</h3>'
    if change.view is ChangeView.TEXT_DIFF:
        body: str = _text_diff(content, change)
    else:
        body = _cards(content, change.id)
    why: str = f'<p class="why"><strong>{html.escape(s["why"])}</strong> {render_html(change.why, diff)}</p>'
    impact: str = f'<p class="impact"><strong>{html.escape(s["impact"])}</strong> {render_html(change.impact, diff)}</p>'
    figure: str = _figure(content, change.figure, palette) if change.figure is not None else ""
    return f'<section class="change">{head}{body}{why}{impact}{figure}</section>'


def _cards(content: NoteContent, record_id: str) -> str:
    s, doc = content.s, content.diff.document
    fields, section, entry = content.card_fields(record_id)

    def card(side: str) -> str:
        label: str = doc["old"]["label"] if side == "old" else doc["new"]["label"]
        head: str = f'<p class="card-head">{html.escape((s["as_is"] if side == "old" else s["to_be"]) + " " + label)}</p>'
        absent: bool = (side == "old" and section == "added") or (side == "new" and section == "removed")
        if absent:
            note: str = s["not_in"].format(label=label)
            if side == "new" and entry.get("successors"):
                note = content.change_labels(record_id)[0]
            absent_text: str = escape_text(note, content.diff)
            return f'<div class="card {"to-be" if side == "new" else ""}">{head}<p class="absent">{absent_text}</p></div>'
        rows: str = "".join(
            f'<dt>{html.escape(f.label)}</dt><dd class="{"diff" if f.changed else "same"}">'
            f'{escape_text((f.old if side == "old" else f.new) or "", content.diff)}</dd>'
            for f in fields
        )
        return f'<div class="card {"to-be" if side == "new" else ""}">{head}<dl>{rows}</dl></div>'

    return f'<div class="pair">{card("old")}{card("new")}</div>'


def _text_diff(content: NoteContent, change: Highlight) -> str:
    s, doc = content.s, content.diff.document
    before, after = content.text_diff(change.id, change.field or "")
    tag: dict[str, str] = {"same": "", "removed": "del", "added": "ins"}

    def pieces(items: list[DiffPiece]) -> str:
        return "".join(f"<{tag[p.op]}>{escape_text(p.text, content.diff)}</{tag[p.op]}>" if tag[p.op]
                       else escape_text(p.text, content.diff) for p in items)

    label: str = html.escape(content.field_label(change.field or ""))
    return (
        f'<div class="textdiff">'
        f'<p class="card-head">{html.escape(s["as_is"])} {html.escape(doc["old"]["label"])}<br>{label}</p><p>{pieces(before)}</p>'
        f'<p class="card-head">{html.escape(s["to_be"])} {html.escape(doc["new"]["label"])}<br>{label}</p><p>{pieces(after)}</p>'
        f"</div>"
    )


def _table(headers: list[str], rows: list[list[str]]) -> str:
    """A borderless table; cells arrive as HTML, already escaped, and the first column holds IDs."""
    head: str = "".join(f'<th scope="col">{html.escape(h)}</th>' for h in headers)
    body: str = "".join(
        "<tr>" + "".join(f'<td class="id">{c}</td>' if i == 0 else f"<td>{c}</td>" for i, c in enumerate(row)) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _source(content: NoteContent) -> str:
    s, doc = content.s, content.diff.document

    def version(side: str) -> str:
        parts: list[str] = [doc[side]["source"], doc[side].get("ref") or ""]
        return " ".join(p for p in parts if p)

    rows: list[tuple[str, str]] = [
        (s["src_data"], content.diff.path.name),
        (s["as_is"], version("old")),
        (s["to_be"], version("new")),
        (s["src_tool"], "version_diff.py"),
        (s["src_minor"], s["minor_rule"]),
    ]
    items: str = "".join(f"<dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd>" for k, v in rows)
    links: str = ""
    if content.note.links:
        links = "<ul>" + "".join(
            f'<li><a href="{html.escape(link.url, quote=True)}">{render_html(link.label, content.diff)}</a></li>'
            for link in content.note.links
        ) + "</ul>"
    return f'<section class="source"><h2>{html.escape(s["h_source"])}</h2><dl>{items}</dl>{links}</section>'


def _strip_tags(markup: str) -> str:
    return re.sub(r"<[^>]+>", "", markup)
