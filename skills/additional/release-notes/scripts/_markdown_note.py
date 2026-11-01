"""Render the same release note as GitHub-flavored Markdown for a release body.

A GitHub release body cannot carry the note's inline SVG, so each chart
becomes the table of values it draws, a card pair becomes a field table, and
a text change becomes a ``diff`` block. The release title is entered
separately on GitHub, so the body starts with the summary. Section order and
every number match the HTML output, because both read ``NoteContent``.
"""

from __future__ import annotations

from _inline import escape_markdown, render_markdown
from _note_content import NoteContent
from _note_source import ChangeView, Figure, FigureType, Highlight


def render_markdown_note(content: NoteContent) -> str:
    note, s, diff = content.note, content.s, content.diff
    doc = diff.document
    c: dict[str, int] = diff.counts

    def r(text: str) -> str:
        return render_markdown(text, diff)

    out: list[str] = []
    if note.subtitle:
        out.append(f"*{r(note.subtitle)}*")
    out.extend(r(p) for p in note.summary)
    meta_heads: list[str] = [s["as_is"], s["to_be"]] + ([s["released"]] if doc.get("date") else [])
    meta_cells: list[str] = [
        " ".join(v for v in (doc["old"]["label"], doc["old"].get("ref")) if v),
        " ".join(v for v in (doc["new"]["label"], doc["new"].get("ref")) if v),
    ] + ([doc["date"]] if doc.get("date") else [])
    out.append(_table(meta_heads, [meta_cells]))
    out.append(_table(
        [s["stat_records"], s["stat_added"], s["stat_removed"], s["stat_changed"]],
        [[f"{c['before']:,} → {c['after']:,}", f"{c['added']:,}", f"{c['removed']:,}", f"{c['changed']:,}"]],
        numeric=True,
    ))
    out.append(escape_markdown(content.reconcile_sentence()))
    out.append(f"## {escape_markdown(s['h_actions'])}")
    if note.actions:
        out.append("\n".join(f"- **{r(a.who)}** {r(a.what)}" for a in note.actions))
    else:
        out.append(escape_markdown(s["no_actions"]))
    if note.figures:
        out.append(f"## {escape_markdown(s['h_glance'])}")
        out.extend(_figure(content, figure) for figure in note.figures)
    if note.changes:
        out.append(f"## {escape_markdown(s['h_changes'])}")
        out.extend(_highlight(content, change) for change in note.changes)
    if note.field_list is not None:
        heading: str = s["h_field_list"].format(field=content.field_label(note.field_list).lower())
        out.append(f"## {escape_markdown(heading)}")
        out.append("\n".join(f"- **{escape_markdown(name)}**: {escape_markdown(value)}"
                             for name, value in content.field_list(note.field_list)))
    mapping = content.mapping_rows()
    if mapping:
        out.append(f"## {escape_markdown(s['h_mapping'])}")
        headers: list[str] = [s["col_id"], s["as_is"], s["to_be"], s["col_change"]]
        rows: list[list[str]] = [[escape_markdown(v) for v in row] for row in mapping]
        if note.reasons:
            headers.append(s["col_why"])
            for source_row, row in zip(mapping, rows, strict=True):
                reason: str | None = note.reasons.get(source_row[0])
                row.append(r(reason) if reason else escape_markdown(s["not_recorded"]))
        out.append(_table(headers, rows, escape=False))
    for section in note.sections:
        out.append(f"## {r(section.heading)}")
        out.extend(r(p) for p in section.paragraphs)
    if note.open_questions:
        out.append(f"## {escape_markdown(s['h_questions'])}")
        out.append("\n".join(f"- {r(q)}" for q in note.open_questions))
    out.append(f"## {escape_markdown(s['h_index'])}")
    index_table: str = _table([s["col_id"], s["col_name"], s["col_change"]], [list(row) for row in content.index_rows()])
    out.append(f"<details><summary>{escape_markdown(s['h_index'])}</summary>\n\n{index_table}\n\n</details>")
    out.append(f"## {escape_markdown(s['h_source'])}")
    out.append(_source(content))
    return "\n\n".join(out) + "\n"


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
        old_text: str = "".join(p.text for p in before)
        new_text: str = "".join(p.text for p in after)
        body: str = f"{escape_markdown(content.field_label(change.field or ''))}\n\n```diff\n- {old_text}\n+ {new_text}\n```"
    else:
        fields, section, entry = content.card_fields(change.id)
        old_head: str = f"{s['as_is']} {diff.old_label}"
        new_head: str = f"{s['to_be']} {diff.new_label}"
        if section == "added":
            status: str = escape_markdown(s["not_in"].format(label=diff.old_label))
            table = _table([s["col_field"], new_head], [[f.label, _bold(f.new or "", True)] for f in fields], escape=False)
            body = f"{status}\n\n{table}"
        elif section == "removed":
            gone: str = content.change_labels(change.id)[0] if entry.get("successors") else s["not_in"].format(label=diff.new_label)
            table = _table([s["col_field"], old_head], [[f.label, _bold(f.old or "", True)] for f in fields], escape=False)
            body = f"{escape_markdown(gone)}\n\n{table}"
        else:
            rows = [[f.label, _bold(f.old or "", f.changed), _bold(f.new or "", f.changed)] for f in fields]
            body = _table([s["col_field"], old_head, new_head], rows, escape=False)
    why: str = f"**{escape_markdown(s['why'])}** {render_markdown(change.why, diff)}"
    impact: str = f"**{escape_markdown(s['impact'])}** {render_markdown(change.impact, diff)}"
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
    lines.extend(f"- [{render_markdown(link.label, content.diff)}]({link.url})" for link in content.note.links)
    return "\n".join(lines)


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
