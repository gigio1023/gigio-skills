"""Parse note.json, the hand-written part of a release note, into typed records.

note.json holds the words: title, the overview figure, the opening bullets,
actions, figure choices, the material changes with their reasons, extra
sections, and open questions. Prose is bullets: an item is a string or an
object with ``text`` and nested ``items``, up to three levels.
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
from _overview_svg import check_overview

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
    EXCERPT = "excerpt"


MAX_DEPTH: int = 3


class FullList(StrEnum):
    APPENDIX = "appendix"
    OMIT = "omit"


@dataclass(frozen=True)
class Item:
    """One bullet: its text and the bullets nested under it."""

    text: str
    items: list[Item]


@dataclass(frozen=True)
class Overview:
    """The page-one figure of the whole change, drawn by the note author."""

    src: Path
    alt: str
    caption: str | None


@dataclass(frozen=True)
class Action:
    who: str
    what: str
    items: list[Item]


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
    why: list[Item]
    impact: list[Item]
    figure: Figure | None
    fields: list[str] | None  # cards view: show only these fields
    excerpt: tuple[str, str] | None  # excerpt view: (as-is excerpt, to-be excerpt) of one field


@dataclass(frozen=True)
class Section:
    heading: str
    items: list[Item]


@dataclass(frozen=True)
class Link:
    label: str
    url: str


@dataclass(frozen=True)
class Note:
    lang: str
    title: str
    subtitle: str | None
    overview: Overview | None
    summary: list[Item]
    actions: list[Action]
    figures: list[Figure]
    changes: list[Highlight]
    sections: list[Section]
    open_questions: list[Item]
    links: list[Link]
    field_labels: dict[str, str]
    reasons: dict[str, str]
    field_list: str | None
    full_list: FullList

    def prose(self) -> Iterator[tuple[str, str]]:
        """Yield (location, text) for every string that may carry inline markup."""
        yield "title", self.title
        if self.subtitle:
            yield "subtitle", self.subtitle
        if self.overview is not None:
            yield "overview.alt", self.overview.alt
            if self.overview.caption:
                yield "overview.caption", self.overview.caption
        yield from _item_texts(self.summary, "summary")
        for i, action in enumerate(self.actions):
            yield f"actions[{i}].who", action.who
            yield f"actions[{i}].what", action.what
            yield from _item_texts(action.items, f"actions[{i}].items")
        for i, figure in enumerate(self.figures):
            yield f"figures[{i}].title", figure.title
            yield f"figures[{i}].caption", figure.caption
        for i, change in enumerate(self.changes):
            yield f"changes[{i}].title", change.title
            yield from _item_texts(change.why, f"changes[{i}].why")
            yield from _item_texts(change.impact, f"changes[{i}].impact")
            if change.figure is not None:
                yield f"changes[{i}].figure.title", change.figure.title
                yield f"changes[{i}].figure.caption", change.figure.caption
        for i, section in enumerate(self.sections):
            yield f"sections[{i}].heading", section.heading
            yield from _item_texts(section.items, f"sections[{i}].items")
        yield from _item_texts(self.open_questions, "open_questions")
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
        "subtitle", "overview", "actions", "figures", "changes", "sections", "open_questions", "links", "field_labels",
        "reasons", "field_list", "full_list"})
    if top["schema"] != SCHEMA:
        raise NoteSourceError(f"{path}: schema must be {SCHEMA!r}")
    if top["lang"] not in LANGUAGES:
        raise NoteSourceError(f"{path}: lang must be one of {sorted(LANGUAGES)}; add strings to assets/strings.json for another")
    note = Note(
        lang=top["lang"],
        title=_text(top["title"], "title"),
        subtitle=_text(top["subtitle"], "subtitle") if "subtitle" in top else None,
        overview=_overview(top["overview"], path.parent) if "overview" in top else None,
        summary=_items(top["summary"], "summary"),
        actions=[_action(a, f"actions[{i}]") for i, a in enumerate(_list(top.get("actions", []), "actions"))],
        figures=[_figure(f, f"figures[{i}]", path.parent) for i, f in enumerate(_list(top.get("figures", []), "figures"))],
        changes=[_highlight(c, f"changes[{i}]", path.parent) for i, c in enumerate(_list(top.get("changes", []), "changes"))],
        sections=[_section(s, f"sections[{i}]") for i, s in enumerate(_list(top.get("sections", []), "sections"))],
        open_questions=_items(top.get("open_questions", []), "open_questions"),
        links=[_link(k, f"links[{i}]") for i, k in enumerate(_list(top.get("links", []), "links"))],
        field_labels=_labels(top.get("field_labels", {}), "field_labels"),
        reasons=_labels(top.get("reasons", {}), "reasons"),
        field_list=_text(top["field_list"], "field_list") if "field_list" in top else None,
        full_list=_full_list(top.get("full_list", FullList.APPENDIX.value)),
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


def _items(value: Any, where: str, depth: int = 1) -> list[Item]:
    """Bullets: a list whose entries are strings or {"text", "items"} objects, at most MAX_DEPTH levels deep."""
    if depth > MAX_DEPTH:
        raise NoteSourceError(f"{where}: bullets nest at most {MAX_DEPTH} levels; move the detail to a later section")
    found: list[Item] = []
    for i, entry in enumerate(_list(value, where)):
        if isinstance(entry, str):
            found.append(Item(_text(entry, f"{where}[{i}]"), []))
            continue
        item: dict[str, Any] = _object(entry, f"{where}[{i}]", required={"text"}, optional={"items"})
        found.append(Item(_text(item["text"], f"{where}[{i}].text"), _items(item.get("items", []), f"{where}[{i}].items", depth + 1)))
    return found


def _points(value: Any, where: str) -> list[Item]:
    """A why or impact: one string, shown inline after its label, or a list of bullets."""
    return [Item(_text(value, where), [])] if isinstance(value, str) else _items(value, where)


def _item_texts(items: list[Item], where: str) -> Iterator[tuple[str, str]]:
    for i, item in enumerate(items):
        yield f"{where}[{i}]", item.text
        yield from _item_texts(item.items, f"{where}[{i}].items")


def _overview(value: Any, base: Path) -> Overview:
    item: dict[str, Any] = _object(value, "overview", required={"src", "alt"}, optional={"caption"})
    src: Path = (base / _text(item["src"], "overview.src")).resolve()
    if not src.is_file():
        raise NoteSourceError(f"overview.src: {src} does not exist")
    check_overview(src)
    caption: str | None = _text(item["caption"], "overview.caption") if "caption" in item else None
    return Overview(src, _text(item["alt"], "overview.alt"), caption)


def _full_list(value: Any) -> FullList:
    try:
        return FullList(value)
    except ValueError as err:
        raise NoteSourceError(f"full_list: one of {[f.value for f in FullList]}") from err


def _labels(value: Any, where: str) -> dict[str, str]:
    if not isinstance(value, dict):
        raise NoteSourceError(f"{where}: expected an object of name to text")
    return {str(k): _text(v, f"{where}.{k}") for k, v in value.items()}


def _action(value: Any, where: str) -> Action:
    item: dict[str, Any] = _object(value, where, required={"who", "what"}, optional={"items"})
    return Action(who=_text(item["who"], f"{where}.who"), what=_text(item["what"], f"{where}.what"),
                  items=_items(item.get("items", []), f"{where}.items", 2))


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
    item: dict[str, Any] = _object(value, where, required={"id", "title", "why", "impact"},
                                   optional={"view", "field", "figure", "fields", "as_is", "to_be"})
    try:
        view: ChangeView = ChangeView(item.get("view", ChangeView.CARDS.value))
    except ValueError as err:
        raise NoteSourceError(f"{where}.view: one of {[v.value for v in ChangeView]}") from err
    if view in (ChangeView.TEXT_DIFF, ChangeView.EXCERPT) and "field" not in item:
        raise NoteSourceError(f"{where}: a {view.value} view names the text field in 'field'")
    excerpt: tuple[str, str] | None = None
    if view is ChangeView.EXCERPT:
        if "as_is" not in item or "to_be" not in item:
            raise NoteSourceError(f"{where}: an excerpt view gives 'as_is' and 'to_be', each copied verbatim from the field")
        excerpt = (_text(item["as_is"], f"{where}.as_is"), _text(item["to_be"], f"{where}.to_be"))
    elif "as_is" in item or "to_be" in item:
        raise NoteSourceError(f"{where}: 'as_is' and 'to_be' belong to the excerpt view")
    fields: list[str] | None = None
    if "fields" in item:
        if view is not ChangeView.CARDS:
            raise NoteSourceError(f"{where}: 'fields' limits the cards view only")
        fields = [_text(f, f"{where}.fields[{i}]") for i, f in enumerate(_list(item["fields"], f"{where}.fields"))]
    figure: Figure | None = _figure(item["figure"], f"{where}.figure", base) if "figure" in item else None
    return Highlight(id=str(item["id"]), title=_text(item["title"], f"{where}.title"), view=view, field=item.get("field"),
                     why=_points(item["why"], f"{where}.why"), impact=_points(item["impact"], f"{where}.impact"), figure=figure,
                     fields=fields, excerpt=excerpt)


def _section(value: Any, where: str) -> Section:
    item: dict[str, Any] = _object(value, where, required={"heading", "items"}, optional=set())
    return Section(_text(item["heading"], f"{where}.heading"), _items(item["items"], f"{where}.items"))


def _link(value: Any, where: str) -> Link:
    item: dict[str, Any] = _object(value, where, required={"label", "url"}, optional=set())
    return Link(_text(item["label"], f"{where}.label"), _text(item["url"], f"{where}.url"))


def field_text(raw: Any) -> str:
    """A field value as the text a reader sees: lists joined with commas, objects as JSON."""
    if isinstance(raw, list):
        return ", ".join(str(item) for item in raw)
    if isinstance(raw, dict):
        return json.dumps(raw, ensure_ascii=False)
    return "" if raw is None else str(raw)


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
        if change.fields is not None and not set(change.fields) <= set(compared):
            raise NoteSourceError(f"changes[{i}].fields: {sorted(set(change.fields) - set(compared))} are not compared fields ({compared})")
        if change.excerpt is not None:
            if entry["section"] != "changed" or change.field not in entry["major_fields"]:
                raise NoteSourceError(f"changes[{i}]: {change.id} has no changed field {change.field!r} to excerpt")
            for side, part in (("old", change.excerpt[0]), ("new", change.excerpt[1])):
                whole: str = field_text(entry[side].get(change.field))
                if part not in whole:
                    key: str = "as_is" if side == "old" else "to_be"
                    raise NoteSourceError(f"changes[{i}].{key}: the excerpt does not appear verbatim in {change.id} "
                                          f"{change.field} ({diff.old_label if side == 'old' else diff.new_label}) in {diff.path.name}")
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
    # One reason per record: a change section carries its own why, and the index points to it.
    both: list[str] = sorted(set(note.reasons) & {change.id for change in note.changes})
    if both:
        raise NoteSourceError(f"reasons: {', '.join(both)} also have a change section; keep the reason in changes[].why only")
    if note.field_list is not None and note.field_list not in compared:
        raise NoteSourceError(f"field_list: {note.field_list!r} is not a compared field ({compared})")
