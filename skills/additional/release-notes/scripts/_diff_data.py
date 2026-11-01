"""Read diff.json and answer the questions the builder and the checks ask of it.

The builder resolves ``{{dotted.path}}`` tokens against it; the number check
asks which numbers and IDs the note may print and which strings are version
identifiers rather than numbers.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from _errors import NoteSourceError

SCHEMA: str = "release-notes/diff@1"
NUMBER_PATTERN: re.Pattern[str] = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")


@dataclass(frozen=True)
class DiffData:
    """A loaded diff.json; ``document`` is the parsed JSON, kept whole for token lookup."""

    path: Path
    document: dict[str, Any]

    @property
    def old_label(self) -> str:
        return str(self.document["old"]["label"])

    @property
    def new_label(self) -> str:
        return str(self.document["new"]["label"])

    @property
    def counts(self) -> dict[str, int]:
        return self.document["counts"]

    def resolve(self, dotted: str) -> Any:
        """Return the value at a dotted path such as ``counts.added`` or ``groups.Billing.after``.

        A fact resolves to its value, so ``facts.<name>`` prints the number.
        """
        value: Any = self.document
        for part in dotted.split("."):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                raise NoteSourceError(f"token {{{{{dotted}}}}} names no value in {self.path.name} (missing {part!r})")
        if isinstance(value, dict) and "value" in value and "source" in value:
            value = value["value"]
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise NoteSourceError(f"token {{{{{dotted}}}}} is a {type(value).__name__}; point it at a number or a label")
        return value

    def known_ids(self) -> set[str]:
        return set(self.document["ids"]["old"]) | set(self.document["ids"]["new"])

    def identifier_strings(self) -> list[str]:
        """Strings that contain digits without being counts: version labels, refs, sources, the date."""
        found: list[str] = []
        for side in ("old", "new"):
            for key in ("label", "ref", "source"):
                value: Any = self.document[side].get(key)
                if value:
                    found.append(str(value))
        if self.document.get("date"):
            found.append(str(self.document["date"]))
        return sorted(set(found), key=len, reverse=True)

    def allowed_numbers(self) -> set[str]:
        """The numbers a note may print, as canonical strings.

        These are the counts and tallies, fact values, and numbers inside the
        field values of added, removed, and changed records. Digits inside IDs,
        version labels, and the date are excluded, so a mistyped count that
        happens to equal part of an ID still fails the check.
        """
        numbers: set[str] = set()
        for section in ("counts", "removal_kinds", "field_changes", "groups"):
            _collect_numbers(self.document[section], numbers, None)
        for fact in self.document["facts"].values():
            _collect_numbers(fact["value"], numbers, None)
        key: str = self.document["roles"]["key"]
        shape: re.Pattern[str] | None = self.id_shape()
        for section in ("added", "removed", "changed", "minor_only"):
            for entry in self.document[section]:
                records: list[dict[str, Any]] = [entry[k] for k in ("record", "old", "new") if k in entry]
                for record in records + entry.get("successor_records", []):
                    _collect_numbers({k: v for k, v in record.items() if k != key}, numbers, shape)
        return numbers

    def id_shape(self) -> re.Pattern[str] | None:
        """A pattern matching tokens shaped like this artifact's IDs, for finding unknown IDs.

        Letters stay literal and digit runs generalize, so ``FB-001`` gives ``FB-\\d{3}``.
        IDs without letters give no pattern, since any number would match. An ID that ends
        in a digit may be followed directly by a letter, because PDF text extraction can
        join a table's ID cell to the next cell (``FB-004Card``).
        """
        shapes: set[str] = set()
        for key in self.known_ids():
            if not re.search(r"[^\W\d_]", key):
                continue
            body: str = "".join(r"\d" if ch.isdigit() else re.escape(ch) for ch in key)
            shapes.add(body + (r"(?![0-9_-])" if key[-1].isdigit() else r"(?![A-Za-z0-9_-])"))
        if not shapes:
            return None
        alternatives: str = "|".join(sorted(shapes, key=len, reverse=True))
        return re.compile(rf"(?<![A-Za-z0-9_-])(?:{alternatives})")


def load_diff(path: Path) -> DiffData:
    try:
        document: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        raise NoteSourceError(f"{path}: cannot read the data file: {err}") from err
    if not isinstance(document, dict) or document.get("schema") != SCHEMA:
        raise NoteSourceError(f"{path}: not a {SCHEMA} data file; produce it with version_diff.py")
    return DiffData(path=path, document=document)


def canonical_number(text: str) -> str:
    """Normalize ``1,234``, ``+4``, ``−2``, and ``3.50`` to ``1234``, ``4``, ``2``, ``3.5``."""
    cleaned: str = text.replace(",", "").lstrip("+-−")
    try:
        value: Decimal = Decimal(cleaned)
    except InvalidOperation:
        return cleaned
    return format(value.normalize(), "f")


def _collect_numbers(value: Any, into: set[str], id_shape: re.Pattern[str] | None) -> None:
    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)):
        into.add(canonical_number(str(abs(value))))
    elif isinstance(value, str):
        text: str = id_shape.sub(" ", value) if id_shape is not None else value
        into.update(canonical_number(match) for match in NUMBER_PATTERN.findall(text))
    elif isinstance(value, dict):
        for item in value.values():
            _collect_numbers(item, into, id_shape)
    elif isinstance(value, list):
        for item in value:
            _collect_numbers(item, into, id_shape)
