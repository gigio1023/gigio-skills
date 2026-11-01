"""Rows, labels, and sentences that both the HTML and the Markdown renderer print.

Every number here is read from diff.json, and every label from the language's
entry in ``assets/strings.json`` or from note.json ``field_labels``, so the
two outputs cannot disagree about a count or the name of a change kind.
"""

from __future__ import annotations

import difflib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from _diff_data import DiffData
from _errors import NoteSourceError
from _note_source import Note
from _svg_charts import BarRow, PairRow

STRINGS_PATH: Path = Path(__file__).resolve().parent.parent / "assets" / "strings.json"
REMOVAL_KINDS: tuple[str, ...] = ("merged", "split", "replaced", "removed")

# The one label each counted path carries wherever a number is printed under a label.
# check_numbers.py reads the same table, so a correct number under another kind's label fails.
LABEL_KEYS: dict[str, str] = {
    "counts.after": "stat_records",
    "counts.added": "stat_added",
    "counts.changed": "stat_changed",
    "counts.minor_only": "kind_minor",
    "removal_kinds.merged": "label_merged",
    "removal_kinds.split": "label_split",
    "removal_kinds.replaced": "label_replaced",
    "removal_kinds.removed": "stat_removed",
}


def expected_label(path: str, strings: dict[str, str], roles: dict[str, str | None]) -> str | None:
    """The label a counted path must carry, or None when the label depends on note.json field labels."""
    if path in LABEL_KEYS:
        return strings[LABEL_KEYS[path]]
    if path == f"field_changes.{roles['name']}.major":
        return strings["kind_renamed"]
    if path == f"field_changes.{roles['parent']}.major":
        return strings["kind_moved"]
    return None


def load_strings(lang: str) -> dict[str, str]:
    return _strings(lang)


@dataclass(frozen=True)
class CardField:
    label: str
    old: str | None
    new: str | None
    changed: bool


@dataclass(frozen=True)
class FieldEntry:
    """One record in the field list: its ID, its ID and name, its list section, and the field's two values."""

    record_id: str
    title: str
    section: str
    old: str | None
    new: str | None


@dataclass(frozen=True)
class DiffPiece:
    text: str
    op: str  # "same", "removed", or "added"


class NoteContent:
    """Derived content for one note: the note source, its data file, and its language strings."""

    def __init__(self, note: Note, diff: DiffData) -> None:
        self.note: Note = note
        self.diff: DiffData = diff
        self.s: dict[str, str] = _strings(note.lang)
        roles: dict[str, str | None] = diff.document["roles"]
        self.name_field: str | None = roles["name"]
        self.parent_field: str | None = roles["parent"]
        self.entries: dict[str, tuple[str, dict[str, Any]]] = {
            entry["id"]: (section, entry)
            for section in ("added", "removed", "changed", "minor_only")
            for entry in diff.document[section]
        }

    def field_label(self, field: str) -> str:
        return self.note.field_labels.get(field, field.replace("_", " ").capitalize())

    def removal_parts(self) -> list[tuple[str, int]]:
        """Nonzero removal kinds in a fixed order: merged, split, replaced, removed."""
        kinds: dict[str, int] = self.diff.document["removal_kinds"]
        return [(kind, kinds[kind]) for kind in REMOVAL_KINDS if kinds[kind]]

    def reconcile_sentences(self) -> list[str]:
        """The identity, how the records that left divide by kind, and how shared records divide."""
        values: dict[str, str] = {k: f"{v:,}" for k, v in self.diff.counts.items()}
        values["gone"] = values["removed"]
        sentences: list[str] = [self.s["reconcile_identity"].format(**values)]
        parts: list[str] = [self.s[f"part_{kind}"].format(n=f"{n:,}") for kind, n in self.removal_parts()]
        if parts:
            joined: str = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + self.s["and"] + parts[-1]
            sentences.append(self.s["reconcile_gone"].format(gone=values["gone"], gone_parts=joined))
        sentences.append(self.s["reconcile_shared"].format(**values))
        return sentences

    def reason_for(self, record_id: str) -> str:
        """The record's one reason: from note.json reasons, a pointer to its change section, or the no-reason text."""
        if record_id in self.note.reasons:
            return self.note.reasons[record_id]
        if any(change.id == record_id for change in self.note.changes):
            return self.s["see_change"].format(id=record_id)
        if self.entries[record_id][0] == "minor_only":
            return self.s["minor_reason"]
        return self.s["not_recorded"]

    def shows_reasons(self) -> bool:
        return bool(self.note.reasons or self.note.changes)

    def name_of(self, record_id: str) -> str:
        section, entry = self.entries[record_id]
        record: dict[str, Any] = entry["new"] if section in ("changed", "minor_only") else entry["record"]
        return str(record.get(self.name_field, "")) if self.name_field else ""

    def change_labels(self, record_id: str) -> list[str]:
        """Change kinds of one listed record, in the closed vocabulary of diff.json."""
        section, entry = self.entries[record_id]
        if section == "added":
            return [self.s["kind_added"]]
        if section == "removed":
            return [self._removal_label(entry)]
        if section == "minor_only":
            return [self.s["kind_minor"]]
        return [self.kind_label(field) for field in entry["major_fields"]]

    def kind_label(self, field: str) -> str:
        if field == self.name_field:
            return self.s["kind_renamed"]
        if field == self.parent_field:
            return self.s["kind_moved"]
        return self.s["kind_field"].format(field=self.field_label(field))

    def kind_bars(self) -> list[BarRow]:
        counts: dict[str, int] = self.diff.counts
        rows: list[BarRow] = [BarRow(self.s["kind_added"], counts["added"], "added", "counts.added")]  # filtered below
        rows += [BarRow(self.s[LABEL_KEYS[f"removal_kinds.{kind}"]], n, "removed", f"removal_kinds.{kind}")
                 for kind, n in self.removal_parts()]
        for field, tally in self.diff.document["field_changes"].items():
            if tally["major"]:
                rows.append(BarRow(self.kind_label(field), tally["major"], "neutral", f"field_changes.{field}.major"))
        if counts["minor_only"]:
            rows.append(BarRow(self.s["kind_minor"], counts["minor_only"], "neutral", "counts.minor_only"))
        # Zero rows are dropped and the rest sorted by count, so the largest kind of change reads first.
        return sorted((row for row in rows if row.value), key=lambda row: -row.value)

    def group_rows(self) -> list[PairRow]:
        groups: dict[str, dict[str, int]] = self.diff.document["groups"]
        rows: list[PairRow] = [PairRow(name, g["before"], g["after"]) for name, g in groups.items()]
        return sorted(rows, key=lambda r: (-(r.after - r.before), r.label))

    def field_rows(self, field: str) -> list[PairRow]:
        rows: list[PairRow] = []
        for entry in self.diff.document["changed"]:
            if field not in entry["major_fields"]:
                continue
            old, new = entry["old"].get(field), entry["new"].get(field)
            if isinstance(old, bool) or isinstance(new, bool) or not isinstance(old, (int, float)) or not isinstance(new, (int, float)):
                raise NoteSourceError(f"field-dumbbell: {entry['id']} {field} is not numeric in both versions ({old!r}, {new!r})")
            rows.append(PairRow(f"{entry['id']} {self.name_of(entry['id'])}".strip(), old, new))
        if not rows:
            raise NoteSourceError(f"field-dumbbell: no record has a major change in {field!r}")
        return sorted(rows, key=lambda r: (r.after - r.before, r.label))

    def bars_aria(self, title: str) -> str:
        return f"{title}: " + ", ".join(f"{r.label} {r.value:,}" for r in self.kind_bars())

    def pairs_aria(self, title: str, rows: list[PairRow]) -> str:
        return f"{title}: " + ", ".join(f"{r.label} {_plain(r.before)} → {_plain(r.after)}" for r in rows)

    def mapping_rows(self) -> list[tuple[str, str, str, str]]:
        """Rows of ID, as-is, to-be, change for renamed, moved, and removed records."""
        rows: list[tuple[str, str, str, str]] = []
        for field, label in ((self.name_field, self.s["kind_renamed"]), (self.parent_field, self.s["kind_moved"])):
            if field is None:
                continue
            for entry in self.diff.document["changed"]:
                if field in entry["major_fields"]:
                    rows.append((entry["id"], self.value(entry["old"].get(field)), self.value(entry["new"].get(field)), label))
        for entry in self.diff.document["removed"]:
            old_name: str = self.name_of(entry["id"]) or entry["id"]
            successors: str = ", ".join(self._id_and_name(r) for r in entry["successor_records"])
            to_be: str = successors or self.s["not_in"].format(label=self.diff.new_label)
            rows.append((entry["id"], old_name, to_be, self._removal_label(entry)))
        return rows

    def index_rows(self) -> list[tuple[str, ...]]:
        """ID, name, change kinds, and, when the note gives reasons, each record's one reason."""
        rows: list[tuple[str, ...]] = []
        for rid in sorted(self.entries):
            labels: list[str] = self.change_labels(rid)
            if self.note.lang == "en":
                # A list reads as one sentence in English: only its first kind starts with a capital.
                labels = labels[:1] + [label[:1].lower() + label[1:] for label in labels[1:]]
            row: tuple[str, ...] = (rid, self.name_of(rid), ", ".join(labels))
            rows.append(row + (self.reason_for(rid),) if self.shows_reasons() else row)
        return rows

    def successor_fields(self, record_id: str, only: list[str] | None = None) -> list[tuple[str, list[CardField]]]:
        """For a removed record with successors: each successor's ID and name and its fields beside the removed record's."""
        _, entry = self.entries[record_id]
        found: list[tuple[str, list[CardField]]] = []
        for successor in entry["successor_records"]:
            fields: list[CardField] = []
            for field in self.diff.document["compared_fields"]:
                if only is not None and field not in only:
                    continue
                old: str = self.value(entry["record"].get(field))
                new: str = self.value(successor.get(field))
                fields.append(CardField(self.field_label(field), old, new, old != new))
            found.append((self._id_and_name(successor), fields))
        return found

    def text_diff(self, record_id: str, field: str) -> tuple[list[DiffPiece], list[DiffPiece]]:
        """Word-level difference of one text field of a changed record; see word_diff."""
        _, entry = self.entries[record_id]
        return word_diff(str(entry["old"].get(field, "")), str(entry["new"].get(field, "")))

    def card_fields(self, record_id: str, only: list[str] | None = None) -> tuple[list[CardField], str, dict[str, Any]]:
        """Fields for the as-is and to-be cards of one record, plus its list section and entry; ``only`` limits the fields."""
        section, entry = self.entries[record_id]
        fields: list[CardField] = []
        changed: set[str] = set(entry.get("major_fields", [])) | set(entry.get("minor_fields", []))
        if section in ("added", "removed"):
            changed = set(self.diff.document["compared_fields"])
        for field in self.diff.document["compared_fields"]:
            if only is not None and field not in only:
                continue
            old: str | None = None if section == "added" else self.value((entry.get("old") or entry["record"]).get(field))
            new: str | None = None if section == "removed" else self.value((entry.get("new") or entry["record"]).get(field))
            fields.append(CardField(self.field_label(field), old, new, field in changed))
        return fields, section, entry

    def field_list(self, field: str) -> list[FieldEntry]:
        """Every added record and every record whose field changed, except those with their own change section.

        A changed record carries both values, so the reader sees what the field said before.
        Records shown in a change section already show both versions there.
        """
        shown: set[str] = {change.id for change in self.note.changes}
        entries: list[FieldEntry] = []
        for record_id in sorted(self.entries):
            section, entry = self.entries[record_id]
            if record_id in shown:
                continue
            title: str = f"{record_id} {self.name_of(record_id)}".strip()
            if section == "added":
                entries.append(FieldEntry(record_id, title, section, None, self.value(entry["record"].get(field))))
            elif section == "changed" and field in entry["major_fields"]:
                entries.append(FieldEntry(record_id, title, section, self.value(entry["old"].get(field)), self.value(entry["new"].get(field))))
        return entries

    def _id_and_name(self, record: dict[str, Any]) -> str:
        key: str = self.diff.document["roles"]["key"]
        name: str = str(record.get(self.name_field, "")) if self.name_field else ""
        return f"{record[key]} {name}".strip()

    def value(self, raw: Any) -> str:
        if raw is None or raw == "":
            return self.s["empty"]
        if isinstance(raw, list):
            return ", ".join(str(item) for item in raw)
        if isinstance(raw, dict):
            return json.dumps(raw, ensure_ascii=False)
        return _plain(raw) if isinstance(raw, (int, float)) and not isinstance(raw, bool) else str(raw)

    def _removal_label(self, entry: dict[str, Any]) -> str:
        ids: str = ", ".join(entry["successors"])
        return self.s[f"kind_{entry['kind']}"].format(ids=ids)


def word_diff(old_text: str, new_text: str) -> tuple[list[DiffPiece], list[DiffPiece]]:
    """Word-level difference of two texts: pieces for the as-is text and for the to-be text.

    Words are compared without the spaces between them, so a changed run of words is one piece.
    A single shared word between two changes joins the change on both sides: difflib matches
    short words such as "as" or "the" that belong to different phrases, and a reader sees one
    rewritten phrase more clearly than two fragments around a coincidental match.
    """
    old_words: list[str] = old_text.split()
    new_words: list[str] = new_text.split()
    matcher = difflib.SequenceMatcher(None, old_words, new_words, autojunk=False)
    segments: list[list[Any]] = [[op == "equal", old_words[i1:i2], new_words[j1:j2]]
                                 for op, i1, i2, j1, j2 in matcher.get_opcodes()]
    merged: list[list[Any]] = []
    for index, segment in enumerate(segments):
        between_changes: bool = 0 < index < len(segments) - 1 and not segments[index + 1][0] and bool(merged) and not merged[-1][0]
        if segment[0] and len(segment[1]) == 1 and between_changes:
            segment = [False, segment[1], segment[2]]
        if merged and not merged[-1][0] and not segment[0]:
            merged[-1][1] += segment[1]
            merged[-1][2] += segment[2]
        else:
            merged.append([segment[0], list(segment[1]), list(segment[2])])
    before: list[DiffPiece] = []
    after: list[DiffPiece] = []
    for same, old_part, new_part in merged:
        if old_part:
            before.append(DiffPiece(" ".join(old_part), "same" if same else "removed"))
        if new_part:
            after.append(DiffPiece(" ".join(new_part), "same" if same else "added"))
    return _spaced(before), _spaced(after)


def _strings(lang: str) -> dict[str, str]:
    table: dict[str, dict[str, str]] = json.loads(STRINGS_PATH.read_text(encoding="utf-8"))
    if lang not in table:
        raise NoteSourceError(f"no strings for lang {lang!r} in {STRINGS_PATH}")
    return table[lang]


def _spaced(pieces: list[DiffPiece]) -> list[DiffPiece]:
    """Put back the single space between consecutive pieces, outside the highlighted runs."""
    spaced: list[DiffPiece] = []
    for index, piece in enumerate(pieces):
        if index:
            spaced.append(DiffPiece(" ", "same"))
        spaced.append(piece)
    return spaced


def _plain(value: float) -> str:
    return f"{int(value):,}" if float(value).is_integer() else f"{value:,}"
