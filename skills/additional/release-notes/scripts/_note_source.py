"""Parse note.json, the hand-written part of a release note, into typed records.

note.json holds the words: title, summary, actions, figure choices, the
material changes with their reasons, extra sections, and open questions.
Numbers come from diff.json through ``{{...}}`` tokens. The parser rejects
unknown keys so a misspelled field fails loudly instead of disappearing from
the rendered note, and it checks every ID and field the note cites against
the data file.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from _diff_data import DiffData
from _errors import NoteSourceError

SCHEMA: str = "release-notes/note@1"
LANGUAGES: frozenset[str] = frozenset({"en", "ko"})


class FigureType(StrEnum):
    CHANGE_KINDS = "change-kinds"
    GROUP_DUMBBELL = "group-dumbbell"
    FIELD_DUMBBELL = "field-dumbbell"
    SVG = "svg"


class ChangeView(StrEnum):
    CARDS = "cards"
    TEXT_DIFF = "text-diff"


@dataclass(frozen=True)
class Action:
    who: str
    what: str


@dataclass(frozen=True)
class Figure:
    type: FigureType
    title: str
    caption: str
    field: str | None
    src: Path | None
    alt: str | None


@dataclass(frozen=True)
class Highlight:
    """One material change shown as an as-is and to-be pair, with its reason and reader impact."""

    id: str
    title: str
    view: ChangeView
    field: str | None
    why: str
    impact: str
    figure: Figure | None


@dataclass(frozen=True)
class Section:
    heading: str
    paragraphs: list[str]


@dataclass(frozen=True)
class Link:
    label: str
    url: str


@dataclass(frozen=True)
class Note:
    lang: str
    title: str
    subtitle: str | None
    summary: list[str]
    actions: list[Action]
    figures: list[Figure]
    changes: list[Highlight]
    sections: list[Section]
    open_questions: list[str]
    links: list[Link]
    field_labels: dict[str, str]
    reasons: dict[str, str]
    field_list: str | None

    def prose(self) -> Iterator[tuple[str, str]]:
        """Yield (location, text) for every string that may carry inline markup."""
        yield "title", self.title
        if self.subtitle:
            yield "subtitle", self.subtitle
        for i, text in enumerate(self.summary):
            yield f"summary[{i}]", text
        for i, action in enumerate(self.actions):
            yield f"actions[{i}].who", action.who
            yield f"actions[{i}].what", action.what
        for i, figure in enumerate(self.figures):
            yield f"figures[{i}].title", figure.title
            yield f"figures[{i}].caption", figure.caption
        for i, change in enumerate(self.changes):
            yield f"changes[{i}].title", change.title
            yield f"changes[{i}].why", change.why
            yield f"changes[{i}].impact", change.impact
            if change.figure is not None:
                yield f"changes[{i}].figure.title", change.figure.title
                yield f"changes[{i}].figure.caption", change.figure.caption
        for i, section in enumerate(self.sections):
            yield f"sections[{i}].heading", section.heading
            for j, text in enumerate(section.paragraphs):
                yield f"sections[{i}].paragraphs[{j}]", text
        for i, text in enumerate(self.open_questions):
            yield f"open_questions[{i}]", text
        for i, link in enumerate(self.links):
            yield f"links[{i}].label", link.label
        for record_id, reason in self.reasons.items():
            yield f"reasons.{record_id}", reason


def load_note(path: Path, diff: DiffData) -> Note:
    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        raise NoteSourceError(f"{path}: cannot read the note source: {err}") from err
    top: dict[str, Any] = _object(raw, "note.json", required={"schema", "lang", "title", "summary"}, optional={
        "subtitle", "actions", "figures", "changes", "sections", "open_questions", "links", "field_labels", "reasons",
        "field_list"})
    if top["schema"] != SCHEMA:
        raise NoteSourceError(f"{path}: schema must be {SCHEMA!r}")
    if top["lang"] not in LANGUAGES:
        raise NoteSourceError(f"{path}: lang must be one of {sorted(LANGUAGES)}; add strings to assets/strings.json for another")
    note = Note(
        lang=top["lang"],
        title=_text(top["title"], "title"),
        subtitle=_text(top["subtitle"], "subtitle") if "subtitle" in top else None,
        summary=_texts(top["summary"], "summary"),
        actions=[_action(a, f"actions[{i}]") for i, a in enumerate(_list(top.get("actions", []), "actions"))],
        figures=[_figure(f, f"figures[{i}]", path.parent) for i, f in enumerate(_list(top.get("figures", []), "figures"))],
        changes=[_highlight(c, f"changes[{i}]", path.parent) for i, c in enumerate(_list(top.get("changes", []), "changes"))],
        sections=[_section(s, f"sections[{i}]") for i, s in enumerate(_list(top.get("sections", []), "sections"))],
        open_questions=_texts(top.get("open_questions", []), "open_questions"),
        links=[_link(k, f"links[{i}]") for i, k in enumerate(_list(top.get("links", []), "links"))],
        field_labels=_labels(top.get("field_labels", {}), "field_labels"),
        reasons=_labels(top.get("reasons", {}), "reasons"),
        field_list=_text(top["field_list"], "field_list") if "field_list" in top else None,
    )
    _check_against_diff(note, diff)
    return note


def _object(value: Any, where: str, *, required: set[str], optional: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise NoteSourceError(f"{where}: expected an object")
    missing: set[str] = required - value.keys()
    unknown: set[str] = value.keys() - required - optional
    if missing:
        raise NoteSourceError(f"{where}: missing {sorted(missing)}")
    if unknown:
        raise NoteSourceError(f"{where}: unknown keys {sorted(unknown)}; allowed: {sorted(required | optional)}")
    return value


def _list(value: Any, where: str) -> list[Any]:
    if not isinstance(value, list):
        raise NoteSourceError(f"{where}: expected a list")
    return value


def _text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NoteSourceError(f"{where}: expected a non-empty string")
    return value


def _texts(value: Any, where: str) -> list[str]:
    return [_text(item, f"{where}[{i}]") for i, item in enumerate(_list(value, where))]


def _labels(value: Any, where: str) -> dict[str, str]:
    if not isinstance(value, dict):
        raise NoteSourceError(f"{where}: expected an object of name to text")
    return {str(k): _text(v, f"{where}.{k}") for k, v in value.items()}


def _action(value: Any, where: str) -> Action:
    item: dict[str, Any] = _object(value, where, required={"who", "what"}, optional=set())
    return Action(who=_text(item["who"], f"{where}.who"), what=_text(item["what"], f"{where}.what"))


def _figure(value: Any, where: str, base: Path) -> Figure:
    item: dict[str, Any] = _object(value, where, required={"type", "title", "caption"}, optional={"field", "src", "alt"})
    try:
        kind: FigureType = FigureType(item["type"])
    except ValueError as err:
        raise NoteSourceError(f"{where}.type: one of {[t.value for t in FigureType]}") from err
    if kind is FigureType.FIELD_DUMBBELL and "field" not in item:
        raise NoteSourceError(f"{where}: a field-dumbbell names the numeric field to compare in 'field'")
    src: Path | None = None
    if kind is FigureType.SVG:
        if "src" not in item or "alt" not in item:
            raise NoteSourceError(f"{where}: an svg figure needs 'src' (path relative to note.json) and 'alt' (its values as text)")
        src = (base / item["src"]).resolve()
        if not src.is_file():
            raise NoteSourceError(f"{where}.src: {src} does not exist")
    return Figure(kind, _text(item["title"], f"{where}.title"), _text(item["caption"], f"{where}.caption"),
                  item.get("field"), src, item.get("alt"))


def _highlight(value: Any, where: str, base: Path) -> Highlight:
    item: dict[str, Any] = _object(value, where, required={"id", "title", "why", "impact"}, optional={"view", "field", "figure"})
    try:
        view: ChangeView = ChangeView(item.get("view", ChangeView.CARDS.value))
    except ValueError as err:
        raise NoteSourceError(f"{where}.view: one of {[v.value for v in ChangeView]}") from err
    if view is ChangeView.TEXT_DIFF and "field" not in item:
        raise NoteSourceError(f"{where}: a text-diff view names the text field in 'field'")
    figure: Figure | None = _figure(item["figure"], f"{where}.figure", base) if "figure" in item else None
    return Highlight(id=str(item["id"]), title=_text(item["title"], f"{where}.title"), view=view, field=item.get("field"),
                     why=_text(item["why"], f"{where}.why"), impact=_text(item["impact"], f"{where}.impact"), figure=figure)


def _section(value: Any, where: str) -> Section:
    item: dict[str, Any] = _object(value, where, required={"heading", "paragraphs"}, optional=set())
    return Section(_text(item["heading"], f"{where}.heading"), _texts(item["paragraphs"], f"{where}.paragraphs"))


def _link(value: Any, where: str) -> Link:
    item: dict[str, Any] = _object(value, where, required={"label", "url"}, optional=set())
    return Link(_text(item["label"], f"{where}.label"), _text(item["url"], f"{where}.url"))


def _check_against_diff(note: Note, diff: DiffData) -> None:
    listed: dict[str, dict[str, Any]] = {}
    for section in ("added", "removed", "changed", "minor_only"):
        for entry in diff.document[section]:
            listed[entry["id"]] = {"section": section, **entry}
    compared: list[str] = diff.document["compared_fields"]
    for i, change in enumerate(note.changes):
        entry: dict[str, Any] | None = listed.get(change.id)
        if entry is None:
            raise NoteSourceError(f"changes[{i}].id: {change.id} is not added, removed, or changed in {diff.path.name}")
        if change.view is ChangeView.TEXT_DIFF:
            fields: list[str] = [c["field"] for c in entry.get("changes", []) if isinstance(c["new"], str) and isinstance(c["old"], str)]
            if change.field not in fields:
                raise NoteSourceError(f"changes[{i}].field: {change.id} has no changed text field {change.field!r}; "
                                      f"changed text fields: {fields or 'none'}")
    figures: list[tuple[str, Figure]] = [(f"figures[{i}]", f) for i, f in enumerate(note.figures)]
    figures += [(f"changes[{i}].figure", c.figure) for i, c in enumerate(note.changes) if c.figure is not None]
    for where, figure in figures:
        if figure.type is FigureType.FIELD_DUMBBELL and figure.field not in compared:
            raise NoteSourceError(f"{where}.field: {figure.field!r} is not a compared field ({compared})")
        if figure.type is FigureType.GROUP_DUMBBELL and not diff.document["groups"]:
            raise NoteSourceError(f"{where}: group-dumbbell needs version_diff.py --group-field")
    for name in note.field_labels:
        if name not in compared:
            raise NoteSourceError(f"field_labels: {name!r} is not a compared field ({compared})")
    for record_id in note.reasons:
        if record_id not in listed:
            raise NoteSourceError(f"reasons: {record_id} is not added, removed, or changed in {diff.path.name}")
    if note.field_list is not None and note.field_list not in compared:
        raise NoteSourceError(f"field_list: {note.field_list!r} is not a compared field ({compared})")
