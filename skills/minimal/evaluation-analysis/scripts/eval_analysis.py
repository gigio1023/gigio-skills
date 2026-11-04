"""Estimates for eval_compare.py: per-model rates, paired differences, noise, and categories.

Every estimate starts from item scores (the mean of an item's K samples), never
from pooled sample rows, and every standard error is clustered by the item group
column when one is given. Intervals use t with C-1 degrees of freedom, where C is
the number of clusters, because a cluster-robust standard error from a few dozen
clusters is itself noisy. The row-pooled and unclustered numbers are computed
only to show how much they understate the uncertainty.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import eval_stats as stats
from eval_table import InputError, ItemScore, ItemTable


@dataclass
class Interval:
    estimate: float
    se: float
    df: int  # clusters - 1
    low: float
    high: float
    p_value: float  # two-sided, against zero, t(df)


@dataclass
class ModelRate:
    model: str
    items: int
    clusters: int
    graded_rows: int
    rate: Interval
    se_items_independent: float
    se_rows_pooled: float


@dataclass
class NoiseSplit:
    """Law of total variance for the per-item difference (Wang 2025)."""

    items_used: int
    total_variance: float
    prediction_variance: float  # mean over items of var_A/k_A + var_B/k_B
    data_variance: float  # total minus prediction; can come out negative from noise
    prediction_share: float


@dataclass
class CategoryRow:
    category: str
    items: int
    clusters: int
    difference: float
    se_items_independent: float
    se_clustered: float
    low: float
    high: float
    p_items_independent: float
    p_clustered: float
    p_holm: float | None
    p_bh: float | None
    in_family: bool
    note: str


@dataclass
class PairComparison:
    baseline: str
    candidate: str
    items: int
    only_baseline: int
    only_candidate: int
    clusters: int
    difference: Interval
    bootstrap_low: float | None
    bootstrap_high: float | None
    se_paired_items_independent: float
    se_unpaired: float
    correlation: float
    noise: NoiseSplit | None
    family: list[str]
    categories: list[CategoryRow]


def interval(values: list[float], clusters: list[str], level: float) -> Interval:
    """Clustered mean with a t(C-1) interval; NaN fields when fewer than two clusters."""
    estimate: float = stats.mean(values)
    cluster_count: int = len(set(clusters))
    if cluster_count < 2:
        return Interval(estimate, math.nan, 0, math.nan, math.nan, math.nan)
    se: float = stats.clustered_standard_error(values, clusters)
    df: int = cluster_count - 1
    critical: float = stats.t_quantile(0.5 + level / 2.0, df)
    p_value: float = stats.t_two_sided_p(estimate / se, df) if se > 0 else math.nan
    return Interval(estimate, se, df, estimate - critical * se, estimate + critical * se, p_value)


def model_rates(table: ItemTable, level: float) -> list[ModelRate]:
    """Each model's mean item score with clustered, item-level, and row-pooled standard errors."""
    rates: list[ModelRate] = []
    for model in sorted(table.scores):
        items: list[str] = sorted(table.scores[model])
        values: list[float] = [table.scores[model][item].mean for item in items]
        clusters: list[str] = [table.cluster_of[item] for item in items]
        rows: list[float] = table.graded_rows[model]
        rates.append(
            ModelRate(
                model=model,
                items=len(items),
                clusters=len(set(clusters)),
                graded_rows=len(rows),
                rate=interval(values, clusters, level),
                se_items_independent=stats.standard_error(values) if len(values) > 1 else math.nan,
                se_rows_pooled=stats.standard_error(rows) if len(rows) > 1 else math.nan,
            )
        )
    return rates


def compare_pair(
    table: ItemTable,
    baseline: str,
    candidate: str,
    *,
    level: float,
    family: list[str] | None,
    bootstrap: int,
    seed: int,
) -> PairComparison:
    """Candidate minus baseline on items both models scored, paired and clustered."""
    for model in (baseline, candidate):
        if model not in table.scores:
            raise InputError(f"model {model!r} has no graded rows; models with graded rows: {', '.join(sorted(table.scores))}")
    a_scores: dict[str, ItemScore] = table.scores[baseline]
    b_scores: dict[str, ItemScore] = table.scores[candidate]
    shared: list[str] = sorted(set(a_scores) & set(b_scores))
    if len(shared) < 2:
        raise InputError(f"{candidate} and {baseline} share {len(shared)} scored item(s); a paired comparison needs at least 2")
    a_values: list[float] = [a_scores[item].mean for item in shared]
    b_values: list[float] = [b_scores[item].mean for item in shared]
    differences: list[float] = [b - a for a, b in zip(a_values, b_values, strict=True)]
    clusters: list[str] = [table.cluster_of[item] for item in shared]
    difference: Interval = interval(differences, clusters, level)
    low: float | None = None
    high: float | None = None
    if bootstrap > 0 and len(set(clusters)) >= 2:
        low, high = stats.cluster_bootstrap_interval(differences, clusters, level=level, replicates=bootstrap, seed=seed)
    n: int = len(shared)
    return PairComparison(
        baseline=baseline,
        candidate=candidate,
        items=n,
        only_baseline=len(set(a_scores) - set(b_scores)),
        only_candidate=len(set(b_scores) - set(a_scores)),
        clusters=len(set(clusters)),
        difference=difference,
        bootstrap_low=low,
        bootstrap_high=high,
        se_paired_items_independent=stats.standard_error(differences),
        se_unpaired=math.sqrt(stats.sample_variance(a_values) / n + stats.sample_variance(b_values) / n),
        correlation=stats.pearson(a_values, b_values),
        noise=_noise_split(table, baseline, candidate, shared, differences),
        family=_family(table, family),
        categories=_categories(table, shared, differences, family, level),
    )


def _noise_split(table: ItemTable, baseline: str, candidate: str, shared: list[str], differences: list[float]) -> NoiseSplit | None:
    """Split the per-item difference variance into prediction noise and data noise.

    Prediction variance is estimated only from items where both models have at
    least two graded samples; without such items the split is not estimable.
    """
    within: list[float] = []
    for item in shared:
        a: ItemScore = table.scores[baseline][item]
        b: ItemScore = table.scores[candidate][item]
        if a.samples >= 2 and b.samples >= 2:
            within.append(a.variance / a.samples + b.variance / b.samples)
    if not within:
        return None
    total: float = stats.sample_variance(differences)
    prediction: float = stats.mean(within)
    return NoiseSplit(
        items_used=len(within),
        total_variance=total,
        prediction_variance=prediction,
        data_variance=total - prediction,
        prediction_share=prediction / total if total > 0 else math.nan,
    )


def _family(table: ItemTable, declared: list[str] | None) -> list[str]:
    observed: list[str] = sorted(set(table.category_of.values()) - {""})
    return list(declared) if declared is not None else observed


def check_family(table: ItemTable, declared: list[str] | None) -> None:
    """A declared category with no graded item is an input error, not a silent gap."""
    if declared is None:
        return
    observed: set[str] = set(table.category_of.values())
    empty: list[str] = [category for category in declared if category not in observed]
    if empty:
        raise InputError(f"declared category {', '.join(empty)} has no rows; categories in the input: {', '.join(sorted(observed))}")


def _categories(
    table: ItemTable,
    shared: list[str],
    differences: list[float],
    declared: list[str] | None,
    level: float,
) -> list[CategoryRow]:
    """Per-category paired differences; Holm and BH run over the declared family only."""
    family: list[str] = _family(table, declared)
    if not family:
        return []
    names: list[str] = family + sorted(set(table.category_of[item] for item in shared) - set(family) - {""})
    rows: list[CategoryRow] = [_category_row(table, shared, differences, name, level, name in family) for name in names]
    in_family: list[CategoryRow] = [row for row in rows if row.in_family]
    # A family member that cannot be tested still counts toward the family size, entered as p = 1.
    family_p: list[float] = [1.0 if math.isnan(row.p_clustered) else row.p_clustered for row in in_family]
    for row, holm, bh in zip(in_family, stats.holm_adjust(family_p), stats.benjamini_hochberg_adjust(family_p), strict=True):
        row.p_holm = holm
        row.p_bh = bh
    return rows


def _category_row(
    table: ItemTable,
    shared: list[str],
    differences: list[float],
    category: str,
    level: float,
    in_family: bool,
) -> CategoryRow:
    picked: list[int] = [index for index, item in enumerate(shared) if table.category_of[item] == category]
    values: list[float] = [differences[index] for index in picked]
    clusters: list[str] = [table.cluster_of[shared[index]] for index in picked]
    note: str = "" if in_family else "exploratory, outside the declared family"
    if len(set(clusters)) < 2:
        reason: str = "no paired items" if not values else "fewer than 2 clusters, not estimable"
        return CategoryRow(
            category=category,
            items=len(values),
            clusters=len(set(clusters)),
            difference=stats.mean(values) if values else math.nan,
            se_items_independent=math.nan,
            se_clustered=math.nan,
            low=math.nan,
            high=math.nan,
            p_items_independent=math.nan,
            p_clustered=math.nan,
            p_holm=None,
            p_bh=None,
            in_family=in_family,
            note=f"{note}; {reason}" if note else reason,
        )
    clustered: Interval = interval(values, clusters, level)
    se_items: float = stats.standard_error(values)
    p_items: float = stats.normal_two_sided_p(clustered.estimate / se_items) if se_items > 0 else math.nan
    return CategoryRow(
        category=category,
        items=len(values),
        clusters=len(set(clusters)),
        difference=clustered.estimate,
        se_items_independent=se_items,
        se_clustered=clustered.se,
        low=clustered.low,
        high=clustered.high,
        p_items_independent=p_items,
        p_clustered=clustered.p_value,
        p_holm=None,
        p_bh=None,
        in_family=in_family,
        note=note,
    )
