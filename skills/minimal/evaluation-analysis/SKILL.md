---
name: evaluation-analysis
description: >
  Analyze per-sample LLM evaluation results in JSONL or CSV and produce a
  grain check, outcome counts, and rates and model differences with
  clustered, paired intervals and per-category multiplicity control from a
  rerunnable script. Use for "analyze these eval
  results", "compare these two models on this eval", "is this difference
  real", "eval 결과 분석해줘", "두 모델 비교해줘", "카테고리별 차이 봐줘". NOT for
  designing or sizing an eval (evaluation-design), a launch, hold, or report
  verdict (evaluation-audit), campaign run state (evaluation-operations),
  designing a training or serving comparison (ml-experiment), or a
  dashboard's views (insight-dashboard).
---

# Evaluation Analysis

Produce an analysis of per-sample eval results that a colleague can rerun: the grain and outcome counts that say what the numbers are computed over, each model's rate, and each requested difference in percentage points with an interval at the right unit, together with the command that regenerates them. An item is one case of the eval (a case in evaluation-design, a sample in Inspect, a doc in lm-evaluation-harness); a sample is one graded answer to an item (a repetition, an Inspect epoch). The analysis informs a decision and does not make it: a launch, hold, or report verdict belongs to evaluation-audit, and sizing an eval or changing what it measures belongs to evaluation-design.

The analysis is read-only on result records. Write derived tables, scripts, and reports to a location the user names or to a scratch directory, never over raw results. Rerunning the eval or the grader is outside this skill; when an input is missing, say which one and what would supply it.

## Declare before looking at differences

Before computing any difference, write down the models and pairs with the baseline of each, the metric and its denominator, the key that identifies a row, the cluster column, the category family, and the interval level. A choice made after seeing which version looks significant is exploratory and labelled so. Choose the method from the design (paired items, clustered items, K samples per item), not from a diagnostic test's p-value, and report the planned result even when another method would look better.

## Grain and outcomes first

- Assert that the key (model, item, sample) is unique and compare the row count with models x items x K. Rows appended twice, missing (model, item) pairs, and items with fewer samples change every later number; find where they came from before dropping anything.
- Count outcome classes per model: graded success and failure, refusal where it is its own class, no answer, grader error, infrastructure error. Grader and infrastructure errors leave the denominator and are reported beside the rate; outcomes the system is responsible for stay in it, as evaluation-design's measurement rules say. Check that a harness default did not already turn no answer into 0.
- Compare row counts before and after any join with item metadata; a join that adds rows has a repeated key on one side.
- Compute a rate from item scores and combined counts. An average of category averages is a different estimand (the macro mean) and is used only when stated.

Read [grain and outcomes](references/grain-and-outcomes.md) for the checks, the missingness questions, and the harness defaults that hide each problem.

## Unit, clusters, and pairing

- Average each item's K samples into one item score before any standard error. Pooling K x N rows treats samples of one item as independent and understates the standard error.
- When items come in groups that share construction (a template, a seed behavior, a passage, a source document, a conversation), use the clustered standard error at the highest such level, report the cluster count C beside the item count, and take the interval from t(C-1) or a cluster bootstrap.
- Compare two models on the same items through the paired item-level difference, clustered the same way, and report the correlation of their item scores. Never decide by whether two per-model intervals overlap: overlapping intervals can hide a clear paired difference.

Read [clusters and pairing](references/clusters-and-pairing.md) when choosing the cluster level, when clusters or items are few, when comparing more than two models, and for the noise split.

## Categories and multiplicity

Declare the category family before testing. Test each category with its paired, cluster-aware p-value, then apply Holm when any single false claim is costly, as in a report naming which categories regressed, or Benjamini-Hochberg when screening which categories to investigate. Label every cut outside the family exploratory. A small category keeps its own interval with its own cluster count, and a category with fewer than two clusters supports counts, not a clustered interval. Read [categories and multiplicity](references/categories-and-multiplicity.md) before reporting per-category results.

## Effects in natural units

Report a rate difference in percentage points with its interval, item count, and cluster count. Cohen's d, odds ratios, and log-odds are added on request and placed beside the points, because a reader acts on "9 points more refusals". An interval that includes zero is inconclusive, not evidence of no difference; state which differences it rules out, and compare it with the smallest decision-relevant difference when evaluation-design recorded one.

## Noise and planning

Split the variance of the per-item difference into prediction noise (sample to sample within an item) and data noise (item to item). When prediction noise dominates, more samples per item narrow the interval; when data noise dominates, only more items do. Hand sizing of the next run to evaluation-design with the measured variances. The `1/sqrt(nR)` half-width that evaluation-design and evaluation-audit use for planning is an optimistic lower bound that ignores item clusters and the correlation of samples within an item; once rows exist, the measured interval replaces it.

## Script

`scripts/eval_compare.py` runs on Python 3.10 or newer with the standard library only. Resolve the directory that holds this `SKILL.md`, then run:

```bash
python3 <skill-dir>/scripts/eval_compare.py results.jsonl \
  --item prompt_id --sample sample_idx --score refused \
  --cluster behavior_id --category category \
  --status judge_status --ok-status ok \
  --pair model_a model_b --family bio,cyber,fraud --json analysis.json
```

It prints the grain report, outcome classes per model, and per-model rates, then for each pair the paired clustered difference with t(C-1) and cluster bootstrap intervals, the unclustered and unpaired standard errors for contrast, the noise split, and the per-category table with Holm and Benjamini-Hochberg. It exits with status 2 and a reason on a missing column, a blank key or grouping value, a non-numeric score, a repeated key, an item with two clusters or categories, or a declared category with no rows. Pass `--on-duplicate keep-first` only after confirming the copies are reruns appended twice. `--seed` fixes the bootstrap; `--help` lists every option.

An analysis the script does not cover, such as another estimand, a regression on item features, or judge agreement, is written as a seeded script beside the data with its package versions recorded. Headline numbers are recomputed from raw rows, not copied from a summary table, which is the evidence evaluation-audit's "headline recomputes" check reads.

## Synthetic example

A synthetic red-team table: 3 models, 300 prompts drawn from 60 seed behaviors in 6 categories, 3 samples per prompt, judge errors, and 8 rows appended twice. Coverage of nominal 95 percent intervals over 400 regenerated item sets:

| Interval | Coverage | Mean width |
| --- | --- | --- |
| Model A rate, all rows pooled | 0.70 | 6.4 pt |
| Model A rate, clustered by behavior, t(59) | 0.975 | 14.2 pt |
| B - A, (prompt, sample) pairs, McNemar | 0.86 | 7.6 pt |
| B - A, paired by prompt | 0.89 | 8.5 pt |
| B - A, paired and clustered by behavior, t(59) | 0.965 | 10.9 pt |
| Per category, paired prompt-level z | 0.88 | 20.2 pt |
| Per category, clustered t(9) | 0.95 | 28.2 pt |

On one draw, four of six categories had prompt-level p below 0.05; with clustering and Holm, one did. The key check found the 16 rows of the 8 repeated keys at once.

## Report

The analysis note states, at the length the decision needs:

- the declared pairs, metric, denominator, cluster level, category family, and interval level;
- the grain findings and what was done about each;
- outcome counts per model and the resulting denominator;
- each rate and difference in points with its interval, item count, and cluster count;
- the per-category table with the correction named, and which results are exploratory;
- the noise split when items have more than one sample;
- the command, input file and revision, and script version that regenerate the numbers.

A table or dashboard built from these numbers keeps their intervals and denominators; insight-dashboard decides how it presents them.

Read [sources](references/sources.md) when maintaining this package.
