"""Read one version of an artifact as records keyed by a stable ID.

Accepted sources:

- a directory: every file below it that matches ``include`` (default
  ``**/*.json``), sorted by path; each file holds one record (an object) or a
  list of records, and ``path_pattern`` can add fields taken from the file's
  path, such as a category that exists only as a directory name
- a ``.json`` file: a list of records, or an object whose list of records sits
  at ``records_path`` (a dotted key path such as ``items`` or ``data.entries``)
- a ``.jsonl`` file: one record per non-blank line
- a ``.csv`` file: one record per row, every value a string

A record must be a JSON object holding the key field with a string or integer
value. Duplicate keys within one version are an error, because a release note
cannot say which of two records with the same ID is the released one.

A role such as the display name can sit inside an object field, so roles are
dotted paths (``label.en``); ``value_at`` reads one and ``field_of`` names the
top-level field that holds it.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from _errors import InputDataError

Record = dict[str, Any]
DEFAULT_INCLUDE: str = "**/*.json"


@dataclass(frozen=True)
class SourceLayout:
    """Where records sit in one export.

    ``records_path`` names the record list inside a ``.json`` object. ``include`` selects the files of a
    directory source, as a glob relative to it. ``path_pattern`` is searched in each selected file's path
    relative to the directory, in POSIX form; every named group becomes a field of each record in that file.
    """

    records_path: str | None = None
    include: str | None = None
    path_pattern: re.Pattern[str] | None = None


def value_at(record: Record, path: str) -> Any:
    """The value at a dotted path such as ``label.en``, or None when a step is missing."""
    return _walk(record, path)[1]


def has_path(record: Record, path: str) -> bool:
    """Whether every step of a dotted path exists in the record, even when the value is null."""
    return _walk(record, path)[0]


def _walk(record: Record, path: str) -> tuple[bool, Any]:
    value: Any = record
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return False, None
        value = value[part]
    return True, value


def field_of(path: str) -> str:
    """The top-level field that holds a dotted path: ``label`` for ``label.en``."""
    return path.split(".", 1)[0]


def load_version(source: Path, key_field: str, layout: SourceLayout) -> dict[str, Record]:
    """Return the records of one version keyed by ``str(record[key_field])``."""
    if not source.exists():
        raise InputDataError(f"{source}: no such file or directory")
    if not source.is_dir() and (layout.include is not None or layout.path_pattern is not None):
        raise InputDataError(f"{source}: --include and --path-pattern select files of a directory source; this is a file")
    located: list[tuple[str, Record]] = list(_read_records(source, layout))
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


def _read_records(source: Path, layout: SourceLayout) -> list[tuple[str, Record]]:
    if source.is_dir():
        return _read_directory(source, layout)
    suffix: str = source.suffix.lower()
    records_path: str | None = layout.records_path
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


def _read_directory(source: Path, layout: SourceLayout) -> list[tuple[str, Record]]:
    include: str = layout.include or DEFAULT_INCLUDE
    files: list[Path] = sorted(path for path in source.glob(include) if path.is_file())
    if not files:
        raise InputDataError(f"{source}: no file matches {include!r}")
    located: list[tuple[str, Record]] = []
    for path in files:
        records: list[tuple[str, Record]] = _records_from_value(_read_json(path), str(path))
        if layout.path_pattern is not None:
            from_path: dict[str, str] = _path_fields(path.relative_to(source).as_posix(), layout.path_pattern, path)
            records = [(where, _with_path_fields(record, from_path, where)) for where, record in records]
        located.extend(records)
    return located


def _path_fields(relative: str, pattern: re.Pattern[str], path: Path) -> dict[str, str]:
    """The named groups of ``pattern`` in a file's relative path; every file must match and every group capture."""
    match: re.Match[str] | None = pattern.search(relative)
    if match is None:
        raise InputDataError(f"{path}: --path-pattern {pattern.pattern!r} does not match {relative!r}; "
                             "narrow --include to the record files or widen the pattern")
    missing: list[str] = [name for name, value in match.groupdict().items() if value is None]
    if missing:
        raise InputDataError(f"{path}: --path-pattern captured nothing for {missing} in {relative!r}")
    return match.groupdict()


def _with_path_fields(record: Record, from_path: dict[str, str], where: str) -> Record:
    clash: list[str] = sorted(set(from_path) & set(record))
    if clash:
        raise InputDataError(f"{where}: the record already has {clash}; name the --path-pattern groups differently")
    return {**record, **from_path}


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
