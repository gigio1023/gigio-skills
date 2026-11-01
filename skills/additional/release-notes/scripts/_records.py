"""Read one version of an artifact as records keyed by a stable ID.

Accepted sources:

- a directory: every ``*.json`` file below it, sorted by path; each file holds
  one record (an object) or a list of records
- a ``.json`` file: a list of records, or an object whose list of records sits
  at ``records_path`` (a dotted key path such as ``items`` or ``data.entries``)
- a ``.jsonl`` file: one record per non-blank line
- a ``.csv`` file: one record per row, every value a string

A record must be a JSON object holding the key field with a string or integer
value. Duplicate keys within one version are an error, because a release note
cannot say which of two records with the same ID is the released one.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from _errors import InputDataError

Record = dict[str, Any]


def load_version(source: Path, key_field: str, records_path: str | None) -> dict[str, Record]:
    """Return the records of one version keyed by ``str(record[key_field])``."""
    if not source.exists():
        raise InputDataError(f"{source}: no such file or directory")
    located: list[tuple[str, Record]] = list(_read_records(source, records_path))
    by_id: dict[str, Record] = {}
    duplicates: list[str] = []
    for where, record in located:
        key: str = _record_key(record, key_field, where)
        if key in by_id:
            duplicates.append(key)
            continue
        by_id[key] = record
    if duplicates:
        shown: str = ", ".join(sorted(set(duplicates))[:10])
        raise InputDataError(f"{source}: duplicate {key_field!r} values: {shown}")
    if not by_id:
        raise InputDataError(f"{source}: no records found")
    return by_id


def _read_records(source: Path, records_path: str | None) -> list[tuple[str, Record]]:
    if source.is_dir():
        files: list[Path] = sorted(source.rglob("*.json"))
        if not files:
            raise InputDataError(f"{source}: directory holds no *.json files")
        located: list[tuple[str, Record]] = []
        for path in files:
            located.extend(_records_from_value(_read_json(path), str(path)))
        return located
    suffix: str = source.suffix.lower()
    if suffix == ".json":
        value: Any = _read_json(source)
        if records_path is not None:
            value = _follow_path(value, records_path, source)
        elif isinstance(value, dict):
            list_keys: list[str] = [k for k, v in value.items() if isinstance(v, list)]
            raise InputDataError(
                f"{source}: top level is an object; pass --records-path naming the list of records"
                f" (keys holding lists: {', '.join(list_keys) or 'none'})"
            )
        return _records_from_value(value, str(source))
    if suffix == ".jsonl":
        return _read_jsonl(source)
    if suffix == ".csv":
        with source.open(newline="", encoding="utf-8") as handle:
            return [(f"{source}:{row_no}", dict(row)) for row_no, row in enumerate(csv.DictReader(handle), start=2)]
    raise InputDataError(f"{source}: unsupported format {suffix!r}; use a directory of JSON files, .json, .jsonl, or .csv")


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise InputDataError(f"{path}: invalid JSON at line {err.lineno}: {err.msg}") from err


def _read_jsonl(path: Path) -> list[tuple[str, Record]]:
    located: list[tuple[str, Record]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value: Any = json.loads(line)
        except json.JSONDecodeError as err:
            raise InputDataError(f"{path}:{line_no}: invalid JSON: {err.msg}") from err
        located.extend(_records_from_value(value, f"{path}:{line_no}"))
    return located


def _follow_path(value: Any, records_path: str, source: Path) -> Any:
    for part in records_path.split("."):
        if not isinstance(value, dict) or part not in value:
            raise InputDataError(f"{source}: --records-path {records_path!r} does not exist (missing {part!r})")
        value = value[part]
    return value


def _records_from_value(value: Any, where: str) -> list[tuple[str, Record]]:
    if isinstance(value, dict):
        return [(where, value)]
    if isinstance(value, list):
        located: list[tuple[str, Record]] = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                raise InputDataError(f"{where}[{index}]: record is {type(item).__name__}, expected an object")
            located.append((f"{where}[{index}]", item))
        return located
    raise InputDataError(f"{where}: expected an object or a list of objects, found {type(value).__name__}")


def _record_key(record: Record, key_field: str, where: str) -> str:
    if key_field not in record:
        raise InputDataError(f"{where}: record has no {key_field!r} field; pass --key with the ID field name")
    key: Any = record[key_field]
    if isinstance(key, bool) or not isinstance(key, (str, int)) or str(key).strip() == "":
        raise InputDataError(f"{where}: {key_field!r} must be a non-empty string or integer, found {key!r}")
    return str(key)
