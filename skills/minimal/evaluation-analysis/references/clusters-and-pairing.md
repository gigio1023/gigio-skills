# Clusters, Pairing, and Noise

Read this when choosing the unit of analysis or the cluster level, when clusters or items are few, when comparing two or more models, and when splitting noise to plan the next run.

## Item scores from K samples

The variance of an item's mean score over K samples is Var(x) + E[sigma^2]/K, where Var(x) is the spread of true item means and E[sigma^2] the average sample-to-sample variance within an item (Miller 2024, section 3). Average each item's samples first and take the standard error over items. A standard error over all K x N rows treats samples of one item as independent draws and is inconsistent; in the synthetic trial its 95 percent intervals covered 70 percent of the time. Once E[sigma^2]/K is well below Var(x), more samples barely narrow the interval.

lm-evaluation-harness's `mean_stderr` treats every document as independent, and Inspect reduces epochs to one score per sample with the mean reducer before computing metrics by default. Check which a reported standard error did.

Lowering the sampling temperature to reduce noise changes the system under test and can move variance into the item means instead of removing it (Miller 2024, section 3.3); compare at the temperature the decision concerns.

## Choosing the cluster level

- Items cluster when they share construction: prompts written from one seed behavior, variants of one template, attack strategies applied to one goal, questions about one passage or source document, turns of one conversation, or cases from one generator run. The test: if one item were replaced by a fresh draw, which other items would change with it?
- With nested groupings, cluster at the highest level that was sampled. Prompts inside behaviors cluster by behavior. Clustering too high costs width; clustering too low under-covers.
- A category fixed by design (bio, cyber, fraud) is a stratum reported separately, not a cluster, unless the categories were themselves sampled from a larger set.
- Report the cluster count beside the item count: "300 prompts in 60 behaviors".
- The clustered standard error of a mean of n item scores x_i in C clusters is sqrt(sum over clusters of (sum of x_i - mean within the cluster)^2 x C/(C-1)) / n (Miller 2024, equation 4, with the C/(C-1) factor Inspect's `stderr(cluster=...)` applies). With every item in its own cluster it equals the ordinary standard error. The clustered standard error was about three times the naive one on one public reading-comprehension benchmark in Miller's Table 4.

## Few clusters and small item counts

- Use the t critical value with C-1 degrees of freedom; with 10 clusters it is 2.26 rather than 1.96. Inspect's `ci()` does the same for clustered intervals.
- A cluster bootstrap resamples whole clusters with replacement and takes percentiles. It helps with skewed differences, but in Bowyer et al.'s clustered simulations neither the clustered CLT nor the cluster bootstrap reached nominal coverage at small sizes; only a Bayesian model of the clusters did (Bowyer et al. 2025, section 3 and Figure 3). Treat t(C-1) and the bootstrap as approximate and say how many clusters they rest on.
- For independent binary items with one sample each and fewer than a few hundred items, the CLT interval under-covers; use the Wilson score interval or a Beta posterior instead (Bowyer et al. 2025, section 3.1). Inspect provides `ci_wilson`.
- With fewer than about five clusters no interval for the mean is trustworthy; report per-cluster results.

## Paired comparison

- When two models answered the same items, Var(paired difference) = Var(unpaired difference) - 2 Cov(A, B)/n, so pairing is free precision whenever item scores correlate (Miller 2024, section 4). Take the per-item difference of item means, then its clustered standard error at the same cluster level. Report the correlation of item means.
- An unpaired analysis is correct only when the models ran on different items.
- Never decide by interval overlap. Two 95 percent intervals can overlap while the paired interval excludes zero, and the overlap rule has no fixed error rate. Inspect's `ci()` documentation mentions overlap as a use; the paired interval replaces it for a comparison.
- McNemar's test on (item, sample) pairs treats the K samples of an item as independent pairs; in the synthetic trial its 95 percent interval covered 86 percent of the time.
- With more than two models, declare the comparisons first: each candidate against one baseline, or all pairs as in Wang's all-pairs comparison. The pairs claimed together form a multiplicity family; see [categories and multiplicity](categories-and-multiplicity.md).

## Noise split

- By the law of total variance, the variance of the per-item difference is data variance (item to item) plus prediction variance (sample to sample within an item). Estimate prediction variance as the mean over items of var_A/k_A + var_B/k_B from each item's sample variances; data variance is the remainder (Wang 2025).
- Wang reports that paired prediction noise usually exceeds paired data noise, so averaging more samples per item often buys more precision than expected. A high prediction share argues for more samples per item; a high data share argues for more items, the only remedy for data noise.
- A data variance estimate at or below zero means prediction noise accounts for all observed spread at this K.
- As a rough check, Wang finds that SE(A - B) is close to sqrt(p(1-p)/N) for many evals, with p the accuracy of A and N items. A measured paired clustered value far from it deserves a look at the grain.

## The 1/sqrt(nR) rule

The planning rule that the paired-difference half-width is about 1/sqrt(nR) for n cases and R repetitions counts all nR samples as independent. It ignores item clusters and the correlation of samples within an item, so it is an optimistic lower bound. On the synthetic trial with 300 prompts and 3 samples it gave 3.3 points, while the paired, behavior-clustered half-width was 4.8 points. Use it before rows exist, then replace it with the measured interval; Miller's sample-size formula with measured variances, or its clustered version, is the next step and belongs to evaluation-design.
