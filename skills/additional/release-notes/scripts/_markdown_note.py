"""Render the same release note as GitHub-flavored Markdown for a release body.

A GitHub release body cannot carry the note's inline SVG, so each chart
becomes the table of values it draws, a card pair becomes a field table, and
a text change becomes a ``diff`` block. The release title is entered
separately on GitHub, so the body starts with the summary. Section order and
every number match the HTML output, because both read ``NoteContent``.
"""

from __future__ import annotations

from _diff_data import DiffData
from _inline import escape_markdown, render_markdown
from _note_content import DiffPiece, FieldEntry, NoteContent, word_diff
from _note_source import ChangeView, Figure, FigureType, FullList, Highlight, Item


def render_markdown_note(content: NoteContent) -> str:
    note, s, diff = content.note, content.s, content.diff
    doc = diff.document

    def r(text: str) -> str:
        return render_markdown(text, diff)

    out: list[str] = []
    if note.subtitle:
        out.append(f"*{r(note.subtitle)}*")
    if note.overview is not None:
        # A release body cannot carry inline SVG: the overview's alt text stands in for it.
        out.append(f"*{r(note.overview.alt)}*")
    out.append(_bullets(note.summary, diff))
    meta_heads: list[str] = [s["as_is"], s["to_be"]] + ([s["released"]] if doc.get("date") else [])
    meta_cells: list[str] = [
        " ".join(v for v in (doc["old"]["label"], doc["old"].get("ref")) if v),
        " ".join(v for v in (doc["new"]["label"], doc["new"].get("ref")) if v),
    ] + ([doc["date"]] if doc.get("date") else [])
    out.append(_table(meta_heads, [meta_cells]))
    out.append(f"## {escape_markdown(s['h_actions'])}")
    if note.actions:
        out.append("\n".join(f"- **{r(a.who)}:** {r(a.what)}" + ("\n" + _bullets(a.items, diff, 1) if a.items else "")
                             for a in note.actions))
    else:
        out.append(escape_markdown(s["no_actions"]))
    out.append(f"## {escape_markdown(s['h_glance'])}")
    out.append("\n".join(f"- {escape_markdown(sentence)}" for sentence in content.reconcile_sentences()))
    out.extend(_figure(content, figure) for figure in note.figures)
    if note.changes:
        out.append(f"## {escape_markdown(s['h_changes'])}")
        out.extend(_highlight(content, change) for change in note.changes)
    if note.field_list is not None:
        entries = content.field_list(note.field_list)
        if entries:
            heading: str = s["h_field_list"].format(field=content.field_label(note.field_list))
            out.append(f"## {escape_markdown(heading)}")
            out.extend(_field_entry(content, entry) for entry in entries)
    mapping = content.mapping_rows()
    if mapping:
        out.append(f"## {escape_markdown(s['h_mapping'])}")
        out.append(_table([s["col_id"], s["as_is"], s["to_be"], s["col_change"]], [list(row) for row in mapping]))
    for section in note.sections:
        out.append(f"## {r(section.heading)}")
        out.append(_bullets(section.items, diff))
    if note.open_questions:
        out.append(f"## {escape_markdown(s['h_questions'])}")
        out.append(_bullets(note.open_questions, diff))
    if note.full_list is FullList.APPENDIX:
        out.append(_appendix(content))
    out.append(f"## {escape_markdown(s['h_source'])}")
    out.append(_source(content))
    return "\n\n".join(out) + "\n"


def _appendix(content: NoteContent) -> str:
    s, diff = content.s, content.diff

    def r(text: str) -> str:
        return render_markdown(text, diff)

    index_heads: list[str] = [s["col_id"], s["col_name"], s["col_change"]] + ([s["col_why"]] if content.shows_reasons() else [])
    index_rows: list[list[str]] = [[r(v) if i == 3 else escape_markdown(v) for i, v in enumerate(row)] for row in content.index_rows()]
    index_table: str = _table([escape_markdown(h) for h in index_heads], index_rows, escape=False)
    return f"## {escape_markdown(s['h_index'])}\n\n<details><summary>{escape_markdown(s['h_index'])}</summary>\n\n{index_table}\n\n</details>"


def _bullets(items: list[Item], diff: DiffData, depth: int = 0) -> str:
    lines: list[str] = []
    for item in items:
        lines.append(f"{'  ' * depth}- {render_markdown(item.text, diff)}")
        if item.items:
            lines.append(_bullets(item.items, diff, depth + 1))
    return "\n".join(lines)


def _points(label: str, items: list[Item], diff: DiffData) -> str:
    head: str = f"**{escape_markdown(label)}:**"
    if len(items) == 1 and not items[0].items:
        return f"{head} {render_markdown(items[0].text, diff)}"
    return f"{head}\n\n{_bullets(items, diff)}"


def _figure(content: NoteContent, figure: Figure) -> str:
    s, diff = content.s, content.diff
    old_label, new_label = diff.old_label, diff.new_label
    title: str = f"**{render_markdown(figure.title, diff)}**"
    caption: str = render_markdown(figure.caption, diff)
    if figure.type is FigureType.CHANGE_KINDS:
        table: str = _table([s["col_change"], s["stat_records"]], [[b.label, f"{b.value:,}"] for b in content.kind_bars()], numeric=True)
        caption += " " + escape_markdown(s["kinds_overlap"])
    elif figure.type in (FigureType.GROUP_DUMBBELL, FigureType.FIELD_DUMBBELL):
        if figure.type is FigureType.GROUP_DUMBBELL:
            rows = content.group_rows()
            first: str = content.field_label(diff.document["roles"]["group"])
        else:
            rows = content.field_rows(figure.field or "")
            first = s["col_name"]
        table = _table([first, f"{s['as_is']} {old_label}", f"{s['to_be']} {new_label}"],
                       [[row.label, content.value(row.before), content.value(row.after)] for row in rows], numeric=True)
    else:
        table = render_markdown(figure.alt or "", diff)
    return f"{title}\n\n{table}\n\n{caption}"


def _highlight(content: NoteContent, change: Highlight) -> str:
    s, diff = content.s, content.diff
    head: str = f"### {escape_markdown(change.id)} {render_markdown(change.title, diff)}"
    if change.view is ChangeView.TEXT_DIFF:
        before, after = content.text_diff(change.id, change.field or "")
        body: str = f"{escape_markdown(content.field_label(change.field or ''))}\n\n{_diff_fence(before, after)}"
    elif change.excerpt is not None:
        before, after = word_diff(*change.excerpt)
        label: str = s["excerpt_of"].format(field=content.field_label(change.field or ""))
        body = f"{escape_markdown(label)}\n\n{_diff_fence(before, after)}"
    else:
        fields, section, entry = content.card_fields(change.id, change.fields)
        old_head: str = f"{s['as_is']} {diff.old_label}"
        new_head: str = f"{s['to_be']} {diff.new_label}"
        if section == "added":
            status: str = escape_markdown(s["not_in"].format(label=diff.old_label))
            table = _table([s["col_field"], new_head], [[f.label, _bold(f.new or "", True)] for f in fields], escape=False)
            body = f"{status}\n\n{table}"
        elif section == "removed" and entry["successors"]:
            # A merged or replaced record: its fields beside each successor's, as in the HTML cards.
            successors = content.successor_fields(change.id, change.fields)
            heads: list[str] = [s["col_field"], old_head] + [f"{new_head} {title}" for title, _ in successors]
            rows = [[f.label, _bold(f.old or "", any(items[i].changed for _, items in successors))]
                    + [_bold(items[i].new or "", items[i].changed) for _, items in successors]
                    for i, f in enumerate(fields)]
            body = f"{escape_markdown(content.change_labels(change.id)[0])}\n\n{_table(heads, rows, escape=False)}"
        elif section == "removed":
            table = _table([s["col_field"], old_head], [[f.label, _bold(f.old or "", True)] for f in fields], escape=False)
            body = f"{escape_markdown(s['not_in'].format(label=diff.new_label))}\n\n{table}"
        else:
            rows = [[f.label, _bold(f.old or "", f.changed), _bold(f.new or "", f.changed)] for f in fields]
            body = _table([s["col_field"], old_head, new_head], rows, escape=False)
    why: str = _points(s["why"], change.why, diff)
    impact: str = _points(s["impact"], change.impact, diff)
    figure: str = f"\n\n{_figure(content, change.figure)}" if change.figure is not None else ""
    return f"{head}\n\n{body}\n\n{why}\n\n{impact}{figure}"


def _source(content: NoteContent) -> str:
    s, doc = content.s, content.diff.document
    lines: list[str] = [
        f"- {escape_markdown(s['src_data'])}: `{content.diff.path.name}`",
        f"- {escape_markdown(s['as_is'])}: {escape_markdown(' '.join(v for v in (doc['old']['source'], doc['old'].get('ref')) if v))}",
        f"- {escape_markdown(s['to_be'])}: {escape_markdown(' '.join(v for v in (doc['new']['source'], doc['new'].get('ref')) if v))}",
        f"- {escape_markdown(s['src_tool'])}: `version_diff.py`",
        f"- {escape_markdown(s['src_minor'])}: {escape_markdown(s['minor_rule'])}",
    ]
    if content.note.full_list is FullList.OMIT:
        lines.append(f"- {escape_markdown(s['src_full_list'])}: {escape_markdown(s['full_list_omitted'])}")
    lines.extend(f"- {render_markdown(link.label, content.diff)}: <{link.url}>" for link in content.note.links)
    return "\n".join(lines)


def _field_entry(content: NoteContent, entry: FieldEntry) -> str:
    title: str = f"**{escape_markdown(entry.title)}**"
    if entry.section == "added":
        absent: str = escape_markdown(content.s["not_in"].format(label=content.diff.old_label))
        return f"{title}\n\n{absent}\n\n```diff\n+ {entry.new}\n```"
    before, after = content.text_diff(entry.record_id, content.note.field_list or "")
    return f"{title}\n\n{_diff_fence(before, after)}"


def _diff_fence(before: list[DiffPiece], after: list[DiffPiece]) -> str:
    old_text: str = "".join(p.text for p in before)
    new_text: str = "".join(p.text for p in after)
    return f"```diff\n- {old_text}\n+ {new_text}\n```"



def _bold(text: str, on: bool) -> str:
    escaped: str = escape_markdown(text)
    return f"**{escaped}**" if on and escaped else escaped


def _table(headers: list[str], rows: list[list[str]], *, numeric: bool = False, escape: bool = True) -> str:
    def cell(value: str) -> str:
        return escape_markdown(value) if escape else value

    align: list[str] = ["---"] + [("---:" if numeric else "---") for _ in headers[1:]]
    lines: list[str] = ["| " + " | ".join(cell(h) for h in headers) + " |", "| " + " | ".join(align) + " |"]
    lines.extend("| " + " | ".join(cell(v) for v in row) + " |" for row in rows)
    return "\n".join(lines)
