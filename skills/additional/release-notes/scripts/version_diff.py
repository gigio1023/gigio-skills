#!/usr/bin/env python3
"""Compare two released versions of an artifact keyed by ID and write the data file.

The data file (diff.json) is the only source of the numbers a release note
prints. It holds both version identities, the counts, the identities the counts
satisfy, per-field and per-group tallies, and the full added, removed, changed,
and minor-only record lists. ``build_note.py`` reads numbers from it and
``check_numbers.py`` compares the rendered note against it.

Change classes, defined once:

- added: the ID exists only in the new version
- removed: the ID exists only in the old version; a successor file can mark it
  merged (into an ID that also existed before, or together with other IDs),
  split (into several IDs), or replaced (by one new ID)
- changed: a shared ID with at least one major field change; the name field
  counts as renamed and the parent field as moved
- minor only: every field change is minor, meaning the two strings differ only
  in letter case, punctuation, or whitespace (the rule MITRE's CWE diff reports
  use); minor changes are counted and not narrated
- unchanged: a shared ID with identical compared fields

The counts satisfy ``before - removed + added = after`` and
``shared = changed + minor_only + unchanged``; the script checks both, and the
per-group balance, before writing. Python 3.11+ and the standard library only.
Exit status 0 on success, 2 on an input or usage error.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Any

from _errors import InputDataError, ReleaseNoteError
from _records import Record, load_version

SCHEMA: str = "release-notes/diff@1"
MINOR_RULE: str = "strings that differ only in letter case, punctuation, or whitespace"

# Records are dataclasses because the bundled scripts run with the standard
# library alone; there is no project environment to install Pydantic into.


class Severity(StrEnum):
    MAJOR = "major"
    MINOR = "minor"


class RemovalKind(StrEnum):
    MERGED = "merged"
    SPLIT = "split"
    REPLACED = "replaced"
    REMOVED = "removed"


@dataclass(frozen=True)
class Roles:
    """Which record fields carry the ID, the display name, the parent, and the group."""

    key: str
    name: str | None
    parent: str | None
    group: str | None


@dataclass(frozen=True)
class FieldChange:
    field: str
    old: Any
    new: Any
    severity: Severity


@dataclass
class GroupTally:
    before: int = 0
    after: int = 0
    added: int = 0
    removed: int = 0
    moved_in: int = 0
    moved_out: int = 0


@dataclass(frozen=True)
class VersionInfo:
    label: str
    ref: str | None
    source: str
    records: int


@dataclass
class DiffResult:
    """Everything diff.json holds, before serialization."""

    old: VersionInfo
    new: VersionInfo
    release_date: str | None
    roles: Roles
    compared_fields: list[str]
    added: list[dict[str, Any]] = field(default_factory=list)
    removed: list[dict[str, Any]] = field(default_factory=list)
    changed: list[dict[str, Any]] = field(default_factory=list)
    minor_only: list[dict[str, Any]] = field(default_factory=list)
    unchanged: int = 0
    groups: dict[str, GroupTally] = field(default_factory=dict)
    facts: dict[str, dict[str, Any]] = field(default_factory=dict)
    old_ids: list[str] = field(default_factory=list)
    new_ids: list[str] = field(default_factory=list)


def main(argv: list[str]) -> int:
    args: argparse.Namespace = _parse_args(argv)
    try:
        old: dict[str, Record] = load_version(Path(args.old), args.key, args.records_path)
        new: dict[str, Record] = load_version(Path(args.new), args.key, args.records_path)
        roles: Roles = _resolve_roles(args, old, new)
        fields: list[str] = _compared_fields(args.fields, roles, old, new)
        successors: dict[str, list[str]] = _read_successors(Path(args.successors), old, new) if args.successors else {}
        result: DiffResult = DiffResult(
            old=VersionInfo(args.old_label, args.old_ref, Path(args.old).name, len(old)),
            new=VersionInfo(args.new_label, args.new_ref, Path(args.new).name, len(new)),
            release_date=_check_date(args.date),
            roles=roles,
            compared_fields=fields,
            facts=_read_facts(Path(args.facts)) if args.facts else {},
            old_ids=list(old),
            new_ids=list(new),
        )
        _classify(result, old, new, successors)
        if roles.group is not None:
            result.groups = _group_tallies(roles.group, result, old, new)
        document: dict[str, Any] = _to_document(result)
    except ReleaseNoteError as err:
        print(f"version_diff: {err}", file=sys.stderr)
        return 2
    out: Path = Path(args.out)
    out.write_text(json.dumps(document, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    _print_summary(document, out)
    return 0


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--old", required=True, help="old version: directory of JSON files, .json, .jsonl, or .csv")
    parser.add_argument("--new", required=True, help="new version, same format as --old")
    parser.add_argument("--old-label", required=True, help="version identifier printed in the note, such as 2.0")
    parser.add_argument("--new-label", required=True)
    parser.add_argument("--old-ref", help="tag, commit, or release URL of the old version")
    parser.add_argument("--new-ref")
    parser.add_argument("--date", help="release date of the new version, YYYY-MM-DD")
    parser.add_argument("--key", default="id", help="ID field (default: id)")
    parser.add_argument("--name-field", help="display-name field; a change counts as renamed (default: name, when present)")
    parser.add_argument("--parent-field", help="parent or category field; a change counts as moved")
    parser.add_argument("--group-field", help="field whose values get before and after counts, often the parent")
    parser.add_argument("--fields", help="comma-separated fields to compare (default: every field except the key)")
    parser.add_argument("--records-path", help="dotted path to the record list inside a .json object")
    parser.add_argument("--successors", help="CSV with columns old_id,new_id for removed IDs that have a successor")
    parser.add_argument("--facts", help="JSON object of extra numbers: {name: {value, source}}")
    parser.add_argument("--out", required=True, help="path of the data file to write, such as diff.json")
    return parser.parse_args(argv)


def _resolve_roles(args: argparse.Namespace, old: dict[str, Record], new: dict[str, Record]) -> Roles:
    present: set[str] = {name for record in [*old.values(), *new.values()] for name in record}
    name: str | None = args.name_field or ("name" if "name" in present else None)
    for flag, value in (("--name-field", name), ("--parent-field", args.parent_field), ("--group-field", args.group_field)):
        if value is not None and value not in present:
            raise InputDataError(f"{flag} {value!r} appears in no record of either version")
    return Roles(key=args.key, name=name, parent=args.parent_field, group=args.group_field)


def _compared_fields(requested: str | None, roles: Roles, old: dict[str, Record], new: dict[str, Record]) -> list[str]:
    if requested:
        fields: list[str] = [f.strip() for f in requested.split(",") if f.strip()]
    else:
        fields = []
        for record in [*old.values(), *new.values()]:
            fields.extend(f for f in record if f not in fields)
    fields = [f for f in fields if f != roles.key]
    leading: list[str] = [f for f in (roles.name, roles.parent) if f is not None and f in fields]
    return leading + [f for f in fields if f not in leading]


def _check_date(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as err:
        raise InputDataError(f"--date {value!r} is not YYYY-MM-DD") from err


def _read_successors(path: Path, old: dict[str, Record], new: dict[str, Record]) -> dict[str, list[str]]:
    successors: dict[str, list[str]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not {"old_id", "new_id"} <= set(reader.fieldnames):
            raise InputDataError(f"{path}: needs the header old_id,new_id")
        for row_no, row in enumerate(reader, start=2):
            old_id, new_id = row["old_id"].strip(), row["new_id"].strip()
            if old_id not in old or old_id in new:
                raise InputDataError(f"{path}:{row_no}: {old_id} must exist in the old version and not in the new one")
            if new_id not in new:
                raise InputDataError(f"{path}:{row_no}: successor {new_id} does not exist in the new version")
            successors.setdefault(old_id, []).append(new_id)
    return successors


def _read_facts(path: Path) -> dict[str, dict[str, Any]]:
    facts: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(facts, dict):
        raise InputDataError(f"{path}: expected an object of {{name: {{value, source}}}}")
    for name, fact in facts.items():
        valid: bool = isinstance(fact, dict) and isinstance(fact.get("source"), str) and fact["source"].strip() != ""
        number: Any = fact.get("value") if isinstance(fact, dict) else None
        if not valid or isinstance(number, bool) or not isinstance(number, (int, float)):
            raise InputDataError(f"{path}: fact {name!r} needs a numeric 'value' and a non-empty 'source'")
    return facts


def _classify(result: DiffResult, old: dict[str, Record], new: dict[str, Record], successors: dict[str, list[str]]) -> None:
    targets: dict[str, int] = {}
    for new_ids in successors.values():
        for new_id in new_ids:
            targets[new_id] = targets.get(new_id, 0) + 1
    for key in new:
        if key not in old:
            result.added.append({"id": key, "record": new[key]})
    for key in old:
        if key not in new:
            next_ids: list[str] = successors.get(key, [])
            kind: RemovalKind = _removal_kind(next_ids, old, targets)
            result.removed.append({"id": key, "kind": kind.value, "successors": next_ids, "record": old[key],
                                   "successor_records": [new[n] for n in next_ids]})
            continue
        changes: list[FieldChange] = [c for f in result.compared_fields if (c := _compare(f, old[key], new[key])) is not None]
        entry: dict[str, Any] = {
            "id": key,
            "major_fields": [c.field for c in changes if c.severity is Severity.MAJOR],
            "minor_fields": [c.field for c in changes if c.severity is Severity.MINOR],
            "changes": [{"field": c.field, "old": c.old, "new": c.new, "severity": c.severity.value} for c in changes],
            "old": old[key],
            "new": new[key],
        }
        if entry["major_fields"]:
            result.changed.append(entry)
        elif changes:
            result.minor_only.append(entry)
        else:
            result.unchanged += 1


def _removal_kind(next_ids: list[str], old: dict[str, Record], targets: dict[str, int]) -> RemovalKind:
    if not next_ids:
        return RemovalKind.REMOVED
    if len(next_ids) > 1:
        return RemovalKind.SPLIT
    only: str = next_ids[0]
    return RemovalKind.MERGED if only in old or targets[only] > 1 else RemovalKind.REPLACED


def _compare(name: str, old: Record, new: Record) -> FieldChange | None:
    before: Any = old.get(name)
    after: Any = new.get(name)
    if before == after:
        return None
    if isinstance(before, str) and isinstance(after, str) and _normalize(before) == _normalize(after):
        return FieldChange(name, before, after, Severity.MINOR)
    return FieldChange(name, before, after, Severity.MAJOR)


def _normalize(text: str) -> str:
    kept: str = "".join(ch for ch in text if not unicodedata.category(ch).startswith("P"))
    return re.sub(r"\s+", " ", kept).strip().casefold()


def _to_document(result: DiffResult) -> dict[str, Any]:
    counts: dict[str, int] = {
        "before": result.old.records,
        "after": result.new.records,
        "added": len(result.added),
        "removed": len(result.removed),
        "shared": result.old.records - len(result.removed),
        "changed": len(result.changed),
        "minor_only": len(result.minor_only),
        "unchanged": result.unchanged,
        "net": result.new.records - result.old.records,
    }
    removal: dict[str, int] = {kind.value: sum(1 for r in result.removed if r["kind"] == kind.value) for kind in RemovalKind}
    _check_identities(counts)
    return {
        "schema": SCHEMA,
        "old": vars(result.old),
        "new": vars(result.new),
        "date": result.release_date,
        "roles": vars(result.roles),
        "compared_fields": result.compared_fields,
        "minor_rule": MINOR_RULE,
        "counts": counts,
        "removal_kinds": removal,
        "field_changes": _field_tallies(result),
        "groups": {name: vars(tally) for name, tally in result.groups.items()},
        "identities": [
            f"{counts['before']} - {counts['removed']} + {counts['added']} = {counts['after']}",
            f"{counts['shared']} = {counts['changed']} + {counts['minor_only']} + {counts['unchanged']}",
        ],
        "added": result.added,
        "removed": result.removed,
        "changed": result.changed,
        "minor_only": result.minor_only,
        "facts": result.facts,
        "ids": {"old": result.old_ids, "new": result.new_ids},
    }


def _check_identities(counts: dict[str, int]) -> None:
    if counts["before"] - counts["removed"] + counts["added"] != counts["after"]:
        raise ReleaseNoteError(f"counts do not reconcile: {counts}")
    if counts["shared"] != counts["changed"] + counts["minor_only"] + counts["unchanged"]:
        raise ReleaseNoteError(f"shared records do not reconcile: {counts}")


def _field_tallies(result: DiffResult) -> dict[str, dict[str, int]]:
    tallies: dict[str, dict[str, int]] = {f: {"major": 0, "minor": 0} for f in result.compared_fields}
    for entry in [*result.changed, *result.minor_only]:
        for change in entry["changes"]:
            tallies[change["field"]][change["severity"]] += 1
    return tallies


def _group_tallies(group_field: str, result: DiffResult, old: dict[str, Record], new: dict[str, Record]) -> dict[str, GroupTally]:
    """Count records per group in both versions and the flows that explain the difference.

    Groups appear in first-seen order across the old and then the new version.
    Each group satisfies after = before - removed - moved_out + added + moved_in.
    """
    tallies: dict[str, GroupTally] = {}

    def tally(value: Any) -> GroupTally:
        return tallies.setdefault(str(value), GroupTally())

    for record in old.values():
        tally(record.get(group_field)).before += 1
    for record in new.values():
        tally(record.get(group_field)).after += 1
    for entry in result.removed:
        tally(entry["record"].get(group_field)).removed += 1
    for entry in result.added:
        tally(entry["record"].get(group_field)).added += 1
    for entry in [*result.changed, *result.minor_only]:
        before, after = entry["old"].get(group_field), entry["new"].get(group_field)
        if before != after:
            tally(before).moved_out += 1
            tally(after).moved_in += 1
    for name, t in tallies.items():
        if t.before - t.removed - t.moved_out + t.added + t.moved_in != t.after:
            raise ReleaseNoteError(f"group {name!r} does not reconcile: {vars(t)}")
    return tallies


def _print_summary(document: dict[str, Any], out: Path) -> None:
    counts: dict[str, int] = document["counts"]
    print(f"wrote {out}")
    print(f"{document['old']['label']} -> {document['new']['label']}: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    for identity in document["identities"]:
        print(f"identity: {identity}")
    majors: str = ", ".join(f"{k} {v['major']}" for k, v in document["field_changes"].items() if v["major"])
    print(f"major field changes (an ID can count in several): {majors or 'none'}")
    for name in ("added", "removed", "changed", "minor_only"):
        ids: list[str] = [entry["id"] for entry in document[name]]
        print(f"{name}: {' '.join(ids) if ids else '-'}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
