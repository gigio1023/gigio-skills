"""Read a per-sample eval result table and check its grain for eval_compare.py.

The table has one row per (model, item, sample). This module parses JSONL, CSV,
or TSV into typed rows, rejects missing columns and blank key values, reports
duplicate keys, missing (model, item) pairs, short sample counts, and items whose
cluster or category disagrees across rows, and reduces the K samples of each
(model, item) to one item score. Records are dataclasses rather than Pydantic
models because the skill's scripts must run on a bare Python install.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import eval_stats as stats

MISSING_SCORE_TOKENS: frozenset[str] = frozenset({"", "na", "nan", "null", "none"})
TRUE_TOKENS: frozenset[str] = frozenset({"true", "yes"})
FALSE_TOKENS: frozenset[str] = frozenset({"false", "no"})
MAX_LISTED: int = 10  # examples printed per finding


class InputError(Exception):
    """The input cannot be analyzed as given; the message says what to fix."""


@dataclass(frozen=True)
class Columns:
    """Column names that define the key, the score, and the item groupings."""

    model: str
    item: str
    score: str
    sample: str | None
    cluster: str | None
    category: str | None
    status: str | None
    ok_status: str


@dataclass(frozen=True)
class Row:
    """One graded sample; ``line`` is its 1-based line number in the input file."""

    line: int
    model: str
    item: str
    sample: str
    score: float | None
    cluster: str
    category: str
    status: str | None


@dataclass
class DuplicateKey:
    model: str
    item: str
    sample: str
    lines: list[int]
    conflicting: bool  # rows disagree on score or status


@dataclass
class GrainReport:
    """What the table holds against what a complete models x items x K table would hold."""

    rows: int
    distinct_keys: int
    duplicate_keys: list[DuplicateKey]
    duplicate_rows: int  # every row that shares its key with another row
    models: list[str]
    items: int
    expected_samples: int
    samples_declared: bool
    expected_rows: int
    missing_pairs: list[tuple[str, str]]
    short_pairs: list[tuple[str, str, int]]
    inconsistent_items: list[tuple[str, str, list[str]]]  # item, column, distinct values


@dataclass
class OutcomeCounts:
    """Row counts per outcome class for one model, after duplicate handling."""

    model: str
    rows: int
    status_counts: dict[str, int]
    excluded_status: int
    missing_score: int
    graded: int
    score_one: int | None  # None when scores are not binary
    score_zero: int | None


@dataclass
class ItemScore:
    """A (model, item) reduced over its graded samples."""

    mean: float
    variance: float  # over samples, ddof=1; NaN with one sample
    samples: int


@dataclass
class ItemTable:
    """Item-level scores plus the grouping each item belongs to."""

    scores: dict[str, dict[str, ItemScore]]  # model -> item -> score
    graded_rows: dict[str, list[float]]  # model -> every graded sample score
    cluster_of: dict[str, str]
    category_of: dict[str, str]
    binary: bool
    unit_scale: float  # 100 when every score lies in [0, 1], else 1
    clusters_are_items: bool = field(default=False)


def read_records(path: Path, file_format: str | None) -> list[tuple[int, dict[str, object]]]:
    """Return (data line number, record) pairs from a JSONL, CSV, or TSV file."""
    chosen: str = file_format or _format_from_suffix(path)
    if not path.is_file():
        raise InputError(f"input file not found: {path}")
    if chosen == "jsonl":
        return _read_jsonl(path)
    delimiter: str = "\t" if chosen == "tsv" else ","
    with path.open(newline="", encoding="utf-8") as handle:
        reader: csv.DictReader[str] = csv.DictReader(handle, delimiter=delimiter)
        if reader.fieldnames is None:
            raise InputError(f"{path} has no header row")
        return [(index, dict(record)) for index, record in enumerate(reader, start=2)]


def _format_from_suffix(path: Path) -> str:
    suffix: str = path.suffix.lower()
    formats: dict[str, str] = {".jsonl": "jsonl", ".ndjson": "jsonl", ".csv": "csv", ".tsv": "tsv"}
    if suffix not in formats:
        raise InputError(f"cannot tell the format of {path.name}; pass --format jsonl, csv, or tsv")
    return formats[suffix]


def _read_jsonl(path: Path) -> list[tuple[int, dict[str, object]]]:
    records: list[tuple[int, dict[str, object]]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, text in enumerate(handle, start=1):
            if not text.strip():
                continue
            try:
                value: object = json.loads(text)
            except json.JSONDecodeError as err:
                raise InputError(f"{path.name} line {line_number} is not valid JSON: {err.msg}") from err
            if not isinstance(value, dict):
                raise InputError(f"{path.name} line {line_number} is not a JSON object")
            records.append((line_number, value))
    return records


def parse_rows(records: list[tuple[int, dict[str, object]]], columns: Columns) -> list[Row]:
    """Validate column presence and values, then convert records to typed rows."""
    if not records:
        raise InputError("the input has no data rows")
    present: set[str] = set().union(*(record.keys() for _, record in records))
    wanted: list[str] = [
        name for name in (columns.model, columns.item, columns.score, columns.sample, columns.cluster, columns.category, columns.status) if name is not None
    ]
    absent: list[str] = [name for name in wanted if name not in present]
    if absent:
        raise InputError(f"missing column(s) {', '.join(absent)}; the input has {', '.join(sorted(present))}")
    blank: dict[str, list[int]] = defaultdict(list)
    rows: list[Row] = []
    for line, record in records:
        values: dict[str, str] = {}
        for name in (columns.model, columns.item, columns.sample, columns.cluster, columns.category):
            if name is None:
                continue
            text: str = _text(record.get(name))
            if not text:
                blank[name].append(line)
            values[name] = text
        status: str | None = None
        if columns.status is not None:
            status = _text(record.get(columns.status)) or "(blank)"
        rows.append(
            Row(
                line=line,
                model=values[columns.model],
                item=values[columns.item],
                sample=values[columns.sample] if columns.sample else "",
                score=_score(record.get(columns.score), columns.score, line),
                cluster=values[columns.cluster] if columns.cluster else values[columns.item],
                category=values[columns.category] if columns.category else "",
                status=status,
            )
        )
    if blank:
        details: str = "; ".join(f"{name} on lines {_first(lines)}" for name, lines in blank.items())
        raise InputError(f"empty values in key or grouping columns: {details}")
    return rows


def _text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value).strip()


def _score(value: object, column: str, line: int) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return None if math.isnan(float(value)) else float(value)
    text: str = str(value).strip().lower()
    if text in MISSING_SCORE_TOKENS:
        return None
    if text in TRUE_TOKENS:
        return 1.0
    if text in FALSE_TOKENS:
        return 0.0
    try:
        number: float = float(text)
    except ValueError as err:
        raise InputError(f"score column {column} must be numeric or boolean; line {line} has {value!r}") from err
    return None if math.isnan(number) else number


def _first(lines: list[int]) -> str:
    shown: str = ", ".join(str(line) for line in lines[:MAX_LISTED])
    return shown + (f" and {len(lines) - MAX_LISTED} more" if len(lines) > MAX_LISTED else "")


def inspect_grain(rows: list[Row], expected_samples: int | None) -> GrainReport:
    """Compare the table with a complete models x items x K grid and find key collisions."""
    by_key: dict[tuple[str, str, str], list[Row]] = defaultdict(list)
    for row in rows:
        by_key[(row.model, row.item, row.sample)].append(row)
    duplicates: list[DuplicateKey] = [
        DuplicateKey(
            model=key[0],
            item=key[1],
            sample=key[2],
            lines=[row.line for row in group],
            conflicting=len({(row.score, row.status) for row in group}) > 1,
        )
        for key, group in by_key.items()
        if len(group) > 1
    ]
    models: list[str] = sorted({row.model for row in rows})
    items: list[str] = sorted({row.item for row in rows})
    samples_per_pair: Counter[tuple[str, str]] = Counter((model, item) for model, item, _ in by_key)
    k: int = expected_samples if expected_samples is not None else max(samples_per_pair.values())
    missing: list[tuple[str, str]] = [(m, i) for m in models for i in items if (m, i) not in samples_per_pair]
    short: list[tuple[str, str, int]] = [(m, i, n) for (m, i), n in sorted(samples_per_pair.items()) if n < k]
    return GrainReport(
        rows=len(rows),
        distinct_keys=len(by_key),
        duplicate_keys=duplicates,
        duplicate_rows=sum(len(d.lines) for d in duplicates),
        models=models,
        items=len(items),
        expected_samples=k,
        samples_declared=expected_samples is not None,
        expected_rows=len(models) * len(items) * k,
        missing_pairs=missing,
        short_pairs=short,
        inconsistent_items=_inconsistent_items(rows),
    )


def _inconsistent_items(rows: list[Row]) -> list[tuple[str, str, list[str]]]:
    """Items whose cluster or category differs across rows, the usual mark of a bad join."""
    clusters: dict[str, set[str]] = defaultdict(set)
    categories: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        clusters[row.item].add(row.cluster)
        categories[row.item].add(row.category)
    found: list[tuple[str, str, list[str]]] = []
    for label, mapping in (("cluster", clusters), ("category", categories)):
        found.extend((item, label, sorted(values)) for item, values in sorted(mapping.items()) if len(values) > 1)
    return found


def keep_first_of_each_key(rows: list[Row]) -> list[Row]:
    """Drop every row whose key already appeared earlier in the file."""
    seen: set[tuple[str, str, str]] = set()
    kept: list[Row] = []
    for row in rows:
        key: tuple[str, str, str] = (row.model, row.item, row.sample)
        if key not in seen:
            seen.add(key)
            kept.append(row)
    return kept


def count_outcomes(rows: list[Row], columns: Columns) -> list[OutcomeCounts]:
    """Count outcome classes per model; non-ok status and missing scores leave the denominator."""
    by_model: dict[str, list[Row]] = defaultdict(list)
    for row in rows:
        by_model[row.model].append(row)
    binary: bool = all(row.score in (0.0, 1.0) for row in rows if _is_graded(row, columns))
    counts: list[OutcomeCounts] = []
    for model in sorted(by_model):
        group: list[Row] = by_model[model]
        graded: list[float] = [row.score for row in group if _is_graded(row, columns) and row.score is not None]
        statuses: Counter[str] = Counter(row.status for row in group if row.status is not None)
        excluded: int = sum(n for status, n in statuses.items() if status != columns.ok_status)
        counts.append(
            OutcomeCounts(
                model=model,
                rows=len(group),
                status_counts=dict(sorted(statuses.items())),
                excluded_status=excluded,
                missing_score=sum(1 for row in group if _status_ok(row, columns) and row.score is None),
                graded=len(graded),
                score_one=sum(1 for s in graded if s == 1.0) if binary else None,
                score_zero=sum(1 for s in graded if s == 0.0) if binary else None,
            )
        )
    return counts


def _status_ok(row: Row, columns: Columns) -> bool:
    return columns.status is None or row.status == columns.ok_status


def _is_graded(row: Row, columns: Columns) -> bool:
    return _status_ok(row, columns) and row.score is not None


def reduce_to_items(rows: list[Row], columns: Columns) -> ItemTable:
    """Average each (model, item)'s graded samples into one item score."""
    samples: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    graded_rows: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if _is_graded(row, columns) and row.score is not None:
            samples[row.model][row.item].append(row.score)
            graded_rows[row.model].append(row.score)
    if not graded_rows:
        raise InputError("no graded rows remain after excluding non-ok status and missing scores")
    every_score: list[float] = [s for scores in graded_rows.values() for s in scores]
    scores: dict[str, dict[str, ItemScore]] = {
        model: {item: ItemScore(mean=stats.mean(values), variance=stats.sample_variance(values), samples=len(values)) for item, values in per_item.items()}
        for model, per_item in samples.items()
    }
    return ItemTable(
        scores=scores,
        graded_rows=dict(graded_rows),
        cluster_of={row.item: row.cluster for row in rows},
        category_of={row.item: row.category for row in rows},
        binary=all(s in (0.0, 1.0) for s in every_score),
        unit_scale=100.0 if all(0.0 <= s <= 1.0 for s in every_score) else 1.0,
        clusters_are_items=columns.cluster is None,
    )
