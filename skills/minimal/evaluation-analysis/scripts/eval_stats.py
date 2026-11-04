"""Standard-library statistics for eval_compare.py.

Everything here is a pure function over plain lists so the skill runs on any
Python 3.10+ without installing packages. The Student t distribution is computed
from the regularized incomplete beta function (continued fraction, modified
Lentz), which agrees with scipy.stats.t to about 1e-10 for the degrees of
freedom an eval analysis uses.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from statistics import NormalDist

_CF_MAX_ITER = 500
_CF_EPS = 1e-15
_CF_TINY = 1e-300


def mean(values: Sequence[float]) -> float:
    """Arithmetic mean; raises ValueError on an empty sequence."""
    if not values:
        raise ValueError("mean of an empty sequence")
    return math.fsum(values) / len(values)


def sample_variance(values: Sequence[float]) -> float:
    """Variance with ddof=1; NaN when fewer than two values."""
    n: int = len(values)
    if n < 2:
        return math.nan
    m: float = mean(values)
    return math.fsum((v - m) ** 2 for v in values) / (n - 1)


def standard_error(values: Sequence[float]) -> float:
    """Standard error of the mean treating every value as independent."""
    return math.sqrt(sample_variance(values) / len(values))


def clustered_standard_error(values: Sequence[float], clusters: Sequence[str]) -> float:
    """Cluster-robust standard error of the mean (Miller 2024, eq. 4).

    Sums the deviations from the overall mean within each cluster, squares the
    cluster sums, and applies the small-sample factor C/(C-1) that Inspect AI's
    ``stderr(cluster=...)`` also uses. With every value in its own cluster it
    equals ``standard_error``. NaN when there are fewer than two clusters.
    """
    m: float = mean(values)
    sums: dict[str, float] = {}
    for value, cluster in zip(values, clusters, strict=True):
        sums[cluster] = sums.get(cluster, 0.0) + (value - m)
    c: int = len(sums)
    if c < 2:
        return math.nan
    return math.sqrt(math.fsum(s * s for s in sums.values()) * c / (c - 1)) / len(values)


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    """Pearson correlation; NaN when either side has zero variance."""
    mx: float = mean(x)
    my: float = mean(y)
    sxy: float = math.fsum((a - mx) * (b - my) for a, b in zip(x, y, strict=True))
    sxx: float = math.fsum((a - mx) ** 2 for a in x)
    syy: float = math.fsum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return math.nan
    return sxy / math.sqrt(sxx * syy)


def _beta_continued_fraction(a: float, b: float, x: float) -> float:
    qab: float = a + b
    qap: float = a + 1.0
    qam: float = a - 1.0
    c: float = 1.0
    d: float = 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > _CF_TINY else _CF_TINY)
    h: float = d
    for m in range(1, _CF_MAX_ITER + 1):
        m2: int = 2 * m
        for aa in (
            m * (b - m) * x / ((qam + m2) * (a + m2)),
            -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2)),
        ):
            d = 1.0 + aa * d
            d = 1.0 / (d if abs(d) > _CF_TINY else _CF_TINY)
            c = 1.0 + aa / c
            c = c if abs(c) > _CF_TINY else _CF_TINY
            h *= d * c
        if abs(d * c - 1.0) < _CF_EPS:
            return h
    raise ArithmeticError(f"incomplete beta did not converge for a={a}, b={b}, x={x}")


def regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    """I_x(a, b) for a, b > 0 and 0 <= x <= 1."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    log_front: float = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x)
    front: float = math.exp(log_front)
    # The continued fraction converges fast only below this point; use symmetry above it.
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _beta_continued_fraction(a, b, x) / a
    return 1.0 - front * _beta_continued_fraction(b, a, 1.0 - x) / b


def t_two_sided_p(t_value: float, df: float) -> float:
    """Two-sided p-value P(|T| >= |t|) for Student t with df degrees of freedom."""
    if math.isnan(t_value):
        return math.nan
    if math.isinf(t_value):
        return 0.0
    return regularized_incomplete_beta(df / 2.0, 0.5, df / (df + t_value * t_value))


def t_cdf(t_value: float, df: float) -> float:
    """Student t cumulative distribution function."""
    t_squared: float = t_value * t_value
    if t_squared < df:
        # Near zero the tail form loses digits; P(|T| < t) = I_{t^2/(df+t^2)}(1/2, df/2) keeps them.
        central: float = regularized_incomplete_beta(0.5, df / 2.0, t_squared / (df + t_squared))
        return 0.5 + 0.5 * central if t_value > 0 else 0.5 - 0.5 * central
    tail: float = 0.5 * t_two_sided_p(t_value, df)
    return 1.0 - tail if t_value > 0 else tail


def t_quantile(p: float, df: float) -> float:
    """Inverse Student t CDF by bisection; p in (0, 1), df >= 1."""
    if not 0.0 < p < 1.0:
        raise ValueError(f"t quantile needs 0 < p < 1, got {p}")
    if p == 0.5:
        return 0.0
    if p < 0.5:
        return -t_quantile(1.0 - p, df)
    hi: float = 1.0
    while t_cdf(hi, df) < p:
        hi *= 2.0
    lo: float = 0.0
    for _ in range(200):
        mid: float = (lo + hi) / 2.0
        if t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-13:
            break
    return (lo + hi) / 2.0


def normal_two_sided_p(z_value: float) -> float:
    """Two-sided p-value under the standard normal."""
    return 2.0 * (1.0 - NormalDist().cdf(abs(z_value)))


def cluster_bootstrap_interval(
    values: Sequence[float],
    clusters: Sequence[str],
    *,
    level: float,
    replicates: int,
    seed: int,
) -> tuple[float, float]:
    """Percentile interval for the mean, resampling whole clusters with replacement.

    Each replicate draws C clusters and takes the mean of all values in the drawn
    clusters, so a cluster's weight follows its size as in the point estimate.
    """
    sums: dict[str, float] = {}
    counts: dict[str, int] = {}
    for value, cluster in zip(values, clusters, strict=True):
        sums[cluster] = sums.get(cluster, 0.0) + value
        counts[cluster] = counts.get(cluster, 0) + 1
    names: list[str] = sorted(sums)
    cluster_sums: list[float] = [sums[n] for n in names]
    cluster_counts: list[int] = [counts[n] for n in names]
    rng: random.Random = random.Random(seed)
    c: int = len(names)
    estimates: list[float] = []
    for _ in range(replicates):
        picks: list[int] = [rng.randrange(c) for _ in range(c)]
        total: float = math.fsum(cluster_sums[i] for i in picks)
        n: int = sum(cluster_counts[i] for i in picks)
        estimates.append(total / n)
    estimates.sort()
    tail: float = (1.0 - level) / 2.0
    return _percentile(estimates, tail), _percentile(estimates, 1.0 - tail)


def _percentile(sorted_values: Sequence[float], q: float) -> float:
    """Linear-interpolation percentile, the numpy default."""
    position: float = q * (len(sorted_values) - 1)
    low: int = math.floor(position)
    high: int = min(low + 1, len(sorted_values) - 1)
    weight: float = position - low
    return sorted_values[low] * (1.0 - weight) + sorted_values[high] * weight


def holm_adjust(p_values: Sequence[float]) -> list[float]:
    """Holm step-down adjusted p-values (family-wise error control)."""
    m: int = len(p_values)
    order: list[int] = sorted(range(m), key=lambda i: p_values[i])
    adjusted: list[float] = [0.0] * m
    running: float = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p_values[index]))
        adjusted[index] = running
    return adjusted


def benjamini_hochberg_adjust(p_values: Sequence[float]) -> list[float]:
    """Benjamini-Hochberg step-up adjusted p-values (false discovery rate control)."""
    m: int = len(p_values)
    order: list[int] = sorted(range(m), key=lambda i: p_values[i], reverse=True)
    adjusted: list[float] = [0.0] * m
    running: float = 1.0
    for position, index in enumerate(order):
        rank: int = m - position
        running = min(running, min(1.0, p_values[index] * m / rank))
        adjusted[index] = running
    return adjusted
