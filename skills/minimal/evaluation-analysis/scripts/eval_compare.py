#!/usr/bin/env python3
"""Analyze a per-sample LLM eval result table: grain, outcomes, rates, and paired comparisons.

Usage:
    python3 scripts/eval_compare.py results.jsonl --item prompt_id --sample sample_idx \
        --score refused --cluster behavior_id --category category \
        --status judge_status --ok-status ok [--pair model_a model_b] [--json out.json]

Input is JSONL, CSV, or TSV with one row per (model, item, sample). The report
prints, in order:

1. Grain: rows, distinct keys, duplicate keys (exact or conflicting), the
   expected models x items x K row count, missing (model, item) pairs, pairs
   with fewer than K samples, and items whose cluster or category disagrees.
2. Outcome classes per model: status values, missing scores, graded rows, and
   for binary scores the count of 1 and 0. Non-ok status and missing scores are
   excluded from every denominator and counted here.
3. Per-model rate: the mean of item means, with a clustered standard error and a
   t(C-1) interval, beside the item-level and row-pooled standard errors that
   ignore clustering or sampling.
4. For each pair, candidate minus baseline on shared items: the paired clustered
   difference with t(C-1) interval and p-value, a seeded cluster bootstrap
   interval, the unclustered and unpaired standard errors for contrast, the
   correlation of item means, the prediction and data noise split, and a
   per-category table with Holm and Benjamini-Hochberg over the declared family.

Scores in [0, 1] are shown in percentage points; other scores in their own unit.
Without --cluster each item is its own cluster. Without --pair, two models are
compared in sorted order and three or more in every sorted pair.

Exit status: 0 on success; 2 when the input cannot be analyzed as given (a
missing column, a blank key or grouping value, a non-numeric score, a duplicate
key under the default --on-duplicate error, an item with two clusters or
categories, a declared category with no rows, or an unknown model), with the
reason on stderr. The grain report is printed before a grain error.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

# `python3 -I` leaves the script's directory off sys.path; the sibling modules live there.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_analysis import (
    CategoryRow,
    Interval,
    ModelRate,
    NoiseSplit,
    PairComparison,
    check_family,
    compare_pair,
    model_rates,
)
from eval_table import (
    MAX_LISTED,
    Columns,
    GrainReport,
    InputError,
    ItemTable,
    OutcomeCounts,
    Row,
    count_outcomes,
    inspect_grain,
    keep_first_of_each_key,
    parse_rows,
    read_records,
    reduce_to_items,
)

EXIT_INPUT_ERROR: int = 2


def main(argv: list[str] | None = None) -> int:
    args: argparse.Namespace = _parse_args(argv)
    columns: Columns = Columns(
        model=args.model,
        item=args.item,
        score=args.score,
        sample=args.sample,
        cluster=args.cluster,
        category=args.category,
        status=args.status,
        ok_status=args.ok_status,
    )
    family: list[str] | None = [name.strip() for name in args.family.split(",") if name.strip()] if args.family else None
    try:
        rows: list[Row] = parse_rows(read_records(args.input, args.format), columns)
        print(_header(args, columns, len(rows)))
        grain: GrainReport = inspect_grain(rows, args.samples)
        print(_render_grain(grain, args.on_duplicate))
        _raise_on_grain_errors(grain, args.on_duplicate)
        if grain.duplicate_keys:
            rows = keep_first_of_each_key(rows)
        outcomes: list[OutcomeCounts] = count_outcomes(rows, columns)
        print(_render_outcomes(outcomes, columns))
        table: ItemTable = reduce_to_items(rows, columns)
        check_family(table, family)
        rates: list[ModelRate] = model_rates(table, args.level)
        print(_render_rates(rates, table, args.level))
        pairs: list[PairComparison] = [
            compare_pair(table, a, b, level=args.level, family=family, bootstrap=args.bootstrap, seed=args.seed)
            for a, b in _pairs(args.pair, sorted(table.scores))
        ]
        for pair in pairs:
            print(_render_pair(pair, table, args))
    except InputError as err:
        sys.stdout.flush()  # keep the grain report ahead of the error when both streams share a terminal
        print(f"error: {err}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    if args.json is not None:
        report: dict[str, object] = {
            "input": str(args.input),
            "columns": asdict(columns),
            "unit_scale": table.unit_scale,
            "level": args.level,
            "grain": asdict(grain),
            "outcomes": [asdict(outcome) for outcome in outcomes],
            "rates": [asdict(rate) for rate in rates],
            "pairs": [asdict(pair) for pair in pairs],
        }
        args.json.write_text(json.dumps(_finite(report), indent=2) + "\n", encoding="utf-8")
    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Grain check and clustered, paired comparison of a per-sample eval result table.")
    parser.add_argument("input", type=Path, help="JSONL, CSV, or TSV with one row per (model, item, sample)")
    parser.add_argument("--format", choices=("jsonl", "csv", "tsv"), help="override the format inferred from the suffix")
    parser.add_argument("--model", default="model", help="model column (default: model)")
    parser.add_argument("--item", default="item_id", help="item or prompt id column (default: item_id)")
    parser.add_argument("--sample", help="sample index or seed column; omit when each item has one sample per model")
    parser.add_argument("--score", default="score", help="numeric or boolean score column (default: score)")
    parser.add_argument("--cluster", help="item group column such as template, behavior, or passage")
    parser.add_argument("--category", help="category column for the per-category table")
    parser.add_argument("--status", help="grader or run status column; rows not equal to --ok-status are excluded")
    parser.add_argument("--ok-status", default="ok", help="status value of a validly graded row (default: ok)")
    parser.add_argument("--samples", type=int, help="expected samples per (model, item); default: the largest observed")
    parser.add_argument("--pair", nargs=2, action="append", metavar=("BASELINE", "CANDIDATE"), help="report CANDIDATE minus BASELINE; repeatable")
    parser.add_argument("--family", help="comma-separated categories that form the multiplicity family; others are exploratory")
    parser.add_argument("--on-duplicate", choices=("error", "keep-first"), default="error", help="duplicate key handling (default: error)")
    parser.add_argument("--level", type=float, default=0.95, help="interval level (default: 0.95)")
    parser.add_argument("--bootstrap", type=int, default=5000, help="cluster bootstrap replicates; 0 skips it (default: 5000)")
    parser.add_argument("--seed", type=int, default=0, help="bootstrap seed (default: 0)")
    parser.add_argument("--json", type=Path, help="also write the full report as JSON to this path")
    args: argparse.Namespace = parser.parse_args(argv)
    if not 0.0 < args.level < 1.0:
        parser.error("--level must be between 0 and 1")
    if args.samples is not None and args.samples < 1:
        parser.error("--samples must be at least 1")
    return args


def _raise_on_grain_errors(grain: GrainReport, on_duplicate: str) -> None:
    if grain.inconsistent_items:
        raise InputError(f"{len(grain.inconsistent_items)} item(s) have more than one cluster or category; fix the join that produced them")
    if grain.duplicate_keys and on_duplicate == "error":
        conflicting: int = sum(1 for d in grain.duplicate_keys if d.conflicting)
        raise InputError(
            f"the key is not unique: {len(grain.duplicate_keys)} key(s) repeat across {grain.duplicate_rows} rows, "
            f"{conflicting} with conflicting scores or status; find their origin, or pass --on-duplicate keep-first "
            "after confirming the copies are reruns appended twice"
        )


def _pairs(requested: list[list[str]] | None, models: list[str]) -> list[tuple[str, str]]:
    if requested:
        return [(baseline, candidate) for baseline, candidate in requested]
    return list(itertools.combinations(models, 2))


def _header(args: argparse.Namespace, columns: Columns, rows: int) -> str:
    key: str = ", ".join(name for name in (columns.model, columns.item, columns.sample) if name)
    lines: list[str] = [
        f"Eval comparison report: {args.input} ({rows} rows)",
        f"key ({key}); score {columns.score}; cluster {columns.cluster or '(none: each item is its own cluster)'}; "
        f"category {columns.category or '(none)'}; status {columns.status or '(none)'}" + (f" with ok = {columns.ok_status!r}" if columns.status else ""),
    ]
    return "\n".join(lines)


def _render_grain(grain: GrainReport, on_duplicate: str) -> str:
    lines: list[str] = ["", "== Grain"]
    lines.append(f"rows {grain.rows}; distinct keys {grain.distinct_keys}; duplicate-key rows {grain.duplicate_rows}")
    if grain.duplicate_keys:
        exact: int = sum(1 for d in grain.duplicate_keys if not d.conflicting)
        lines.append(f"  repeated keys: {len(grain.duplicate_keys)} (exact copies {exact}, conflicting score or status {len(grain.duplicate_keys) - exact})")
        by_model: dict[str, int] = {}
        for duplicate in grain.duplicate_keys:
            by_model[duplicate.model] = by_model.get(duplicate.model, 0) + len(duplicate.lines)
        lines.append("  duplicate-key rows by model: " + ", ".join(f"{m} {n}" for m, n in sorted(by_model.items())))
        for duplicate in grain.duplicate_keys[:MAX_LISTED]:
            tag: str = "conflicting" if duplicate.conflicting else "exact"
            lines.append(f"  {duplicate.model} / {duplicate.item} / {duplicate.sample or '-'}: lines {duplicate.lines} ({tag})")
        action: str = (
            "stop" if on_duplicate == "error" else f"keep the first row of each key, drop {grain.duplicate_rows - len(grain.duplicate_keys)} later copies"
        )
        lines.append(f"  duplicate policy: {on_duplicate} ({action})")
    source: str = "declared" if grain.samples_declared else "largest observed"
    lines.append(
        f"expected rows: {len(grain.models)} models x {grain.items} items x {grain.expected_samples} samples ({source}) = "
        f"{grain.expected_rows}; distinct keys {grain.distinct_keys} ({grain.distinct_keys - grain.expected_rows:+d})"
    )
    lines.append(f"missing (model, item) pairs: {len(grain.missing_pairs)}")
    lines.extend(f"  {model} / {item}" for model, item in grain.missing_pairs[:MAX_LISTED])
    lines.append(f"(model, item) pairs with fewer than {grain.expected_samples} samples: {len(grain.short_pairs)}")
    lines.extend(f"  {model} / {item}: {n}" for model, item, n in grain.short_pairs[:MAX_LISTED])
    lines.append(f"items with more than one cluster or category: {len(grain.inconsistent_items)}")
    lines.extend(f"  {item} {label}: {', '.join(values)}" for item, label, values in grain.inconsistent_items[:MAX_LISTED])
    return "\n".join(lines)


def _render_outcomes(outcomes: list[OutcomeCounts], columns: Columns) -> str:
    statuses: list[str] = sorted({status for o in outcomes for status in o.status_counts})
    headers: list[str] = ["model", "rows"] + [f"{columns.status}={s}" for s in statuses] + ["missing score", "graded"]
    binary: bool = all(o.score_one is not None for o in outcomes)
    if binary:
        headers += ["score 1", "score 0"]
    body: list[list[str]] = []
    for o in outcomes:
        cells: list[str] = [o.model, str(o.rows)] + [str(o.status_counts.get(s, 0)) for s in statuses] + [str(o.missing_score), str(o.graded)]
        if binary:
            cells += [str(o.score_one), str(o.score_zero)]
        body.append(cells)
    note: str = "denominators are graded rows: rows with " + (f"{columns.status} = {columns.ok_status!r} and a score" if columns.status else "a score")
    return "\n".join(["", "== Outcome classes per model", *_table(headers, body), note])


def _render_rates(rates: list[ModelRate], table: ItemTable, level: float) -> str:
    unit: str = _unit(table)
    pct: str = f"{level * 100:g}%"
    headers: list[str] = ["model", "items", "clusters", f"rate ({unit})", "SE clustered", f"{pct} CI t(C-1)", "SE items indep.", "SE rows pooled"]
    body: list[list[str]] = [
        [
            r.model,
            str(r.items),
            str(r.clusters),
            _num(r.rate.estimate, table),
            _num(r.rate.se, table),
            _ci(r.rate.low, r.rate.high, table),
            _num(r.se_items_independent, table),
            _num(r.se_rows_pooled, table),
        ]
        for r in rates
    ]
    note: str = "rate = mean of item means; the last two SEs ignore clustering or treat samples as independent and are shown for contrast"
    return "\n".join(["", "== Per-model rate", *_table(headers, body), note])


def _render_pair(pair: PairComparison, table: ItemTable, args: argparse.Namespace) -> str:
    unit: str = _unit(table)
    pct: str = f"{args.level * 100:g}%"
    d: Interval = pair.difference
    lines: list[str] = ["", f"== Paired comparison: {pair.candidate} - {pair.baseline}"]
    lines.append(
        f"paired items {pair.items} (unpaired: {pair.only_baseline} only in {pair.baseline}, "
        f"{pair.only_candidate} only in {pair.candidate}); clusters {pair.clusters}"
    )
    lines.append(f"difference {_num(d.estimate, table, signed=True)} {unit}")
    lines.append(f"  paired, clustered: SE {_num(d.se, table)}; {pct} CI t({d.df}) {_ci(d.low, d.high, table)}; p = {_p(d.p_value)}")
    if pair.bootstrap_low is not None and pair.bootstrap_high is not None:
        lines.append(
            f"  cluster bootstrap ({args.bootstrap} replicates, seed {args.seed}): percentile {pct} CI {_ci(pair.bootstrap_low, pair.bootstrap_high, table)}"
        )
    lines.append(
        f"  for contrast: SE paired with items independent {_num(pair.se_paired_items_independent, table)}; "
        f"SE unpaired {_num(pair.se_unpaired, table)}; correlation of item means {pair.correlation:.3f}"
    )
    lines.extend(_render_noise(pair))
    lines.extend(_render_categories(pair, table, args.level))
    return "\n".join(lines)


def _render_noise(pair: PairComparison) -> list[str]:
    if pair.noise is None:
        return ["noise split: not estimable (needs items with at least 2 graded samples from both models)"]
    n: NoiseSplit = pair.noise
    lines: list[str] = [
        f"noise split of the per-item difference ({n.items_used} items with >= 2 samples per model):",
        f"  total variance {n.total_variance:.4f} = prediction {n.prediction_variance:.4f} + data {n.data_variance:.4f}; "
        f"prediction share {n.prediction_share:.0%}",
    ]
    if n.data_variance <= 0:
        lines.append("  data variance estimate is not above zero: prediction noise accounts for all observed spread between items")
    return lines


def _render_categories(pair: PairComparison, table: ItemTable, level: float) -> list[str]:
    if not pair.categories:
        return []
    pct: str = f"{level * 100:g}%"
    headers: list[str] = [
        "category",
        "items",
        "clusters",
        "diff",
        "SE indep.",
        "SE clust.",
        f"{pct} CI t(C-1)",
        "p indep. (z)",
        "p clust.",
        "p Holm",
        "p BH",
        "note",
    ]
    body: list[list[str]] = [_category_cells(row, table) for row in pair.categories]
    family_note: str = f"family: {len(pair.family)} categories ({', '.join(pair.family)}); Holm and BH use the clustered p over the family"
    return ["", f"per category, {pair.candidate} - {pair.baseline} ({_unit(table)}):", *_table(headers, body), family_note]


def _category_cells(row: CategoryRow, table: ItemTable) -> list[str]:
    return [
        row.category,
        str(row.items),
        str(row.clusters),
        _num(row.difference, table, signed=True),
        _num(row.se_items_independent, table),
        _num(row.se_clustered, table),
        _ci(row.low, row.high, table),
        _p(row.p_items_independent),
        _p(row.p_clustered),
        _p(row.p_holm),
        _p(row.p_bh),
        row.note,
    ]


def _unit(table: ItemTable) -> str:
    return "pt" if table.unit_scale == 100.0 else "score units"


def _num(value: float, table: ItemTable, *, signed: bool = False) -> str:
    if math.isnan(value):
        return "n/a"
    scaled: float = value * table.unit_scale
    return f"{scaled:+.2f}" if signed else f"{scaled:.2f}"


def _ci(low: float, high: float, table: ItemTable) -> str:
    if math.isnan(low) or math.isnan(high):
        return "n/a"
    return f"[{_num(low, table, signed=True)}, {_num(high, table, signed=True)}]"


def _p(value: float | None) -> str:
    if value is None or math.isnan(value):
        return "n/a"
    return f"{value:.4f}" if value >= 0.0001 else f"{value:.1e}"


def _table(headers: list[str], body: list[list[str]]) -> list[str]:
    widths: list[int] = [max(len(cells[i]) for cells in [headers, *body]) for i in range(len(headers))]
    return ["  ".join(cell.ljust(width) for cell, width in zip(cells, widths, strict=True)).rstrip() for cells in [headers, *body]]


def _finite(value: object) -> object:
    """Replace NaN with None so the JSON report is valid JSON."""
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, dict):
        return {key: _finite(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_finite(item) for item in value]
    return value


if __name__ == "__main__":
    sys.exit(main())
