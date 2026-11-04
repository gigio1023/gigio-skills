# Grain and Outcomes

Read this before computing any rate: when checking the key and row counts, joining item metadata, deciding what enters a denominator, handling missing rows, or choosing how to average.

## Key and expected rows

- The key is (model, item, sample). When item ids repeat across subsets, the item part of the key includes the subset. The sample part is the sample index or seed; without one, the key is (model, item) and K is 1.
- The expected row count is models x items x K. Fewer distinct keys than that means missing rows; more rows than distinct keys means repeated keys. Report both numbers, not only a clean-looking total.
- An exact copy (same key, same score and status) usually comes from a rerun appended twice or a log concatenated twice. Keep one copy only after confirming that origin.
- A conflicting copy (same key, different score or status) is a rerun with another outcome or a regrade. Dropping either copy picks a result; ask which attempt is authoritative. The record of attempts belongs to evaluation-operations.
- A missing (model, item) pair is a crash, a timeout, or a filter. A paired comparison drops the item, so report how many items each model lost and whether the losses concentrate in one category or on hard items: a model that times out on hard items scores higher on the rest.
- A (model, item) with fewer than K samples still yields an item mean, with more prediction noise. Each item keeps equal weight.
- Each item belongs to one cluster and one category. An item with two values usually comes from a join on the wrong key.

## Joins

Before merging item metadata such as category, cluster, or difficulty, assert that the metadata key is unique, compare row counts before and after, and count unmatched rows on both sides. A many-to-many join multiplies rows without an error; an inner join drops items that lack metadata without a warning.

## Outcome classes and denominators

- Count per model: graded rows by score, refusal when it is its own class, no answer or empty output, truncation or budget exhaustion, grader error, and infrastructure error.
- Attribute before excluding. Grader and infrastructure errors leave the denominator and are reported beside the rate. Outcomes the system is responsible for stay in it, each counted as its own class. A refusal is the measured outcome in a refusal eval and a separate class in a capability eval; name which.
- Error rates that differ across models are a finding. If one model has 5 percent grader errors and another 1 percent, and the errors fall on hard items, the first model's rate is computed on an easier subset. Compare error rates per category before comparing rates.
- Harness defaults can hide a class before the rows reach the analysis. Inspect's `value_to_float` maps NOANSWER to 0 and PARTIAL to 0.5 by default, so no answer becomes a failure unless the scorer says otherwise. Many lm-evaluation-harness task configs apply the `take_first` filter to repeated generations, so K samples can arrive as one.

## Missing values

Understand missingness before dropping rows: which models, categories, and items it touches, and whether it plausibly depends on difficulty or on the outcome. When excluding the affected items could change the conclusion, report the result with and without them.

## Averaging

- The micro mean pools items; the macro mean averages category means. They answer different questions and are equal only with equal category sizes. State which one a number is.
- Never average averages computed over different denominators unless the macro estimand is intended.
- With unequal K, average within each item first so every item carries equal weight; pooling rows would weight items by how many samples survived.

## Recompute from rows

Every headline number is recomputed by a script from the raw rows, not copied from a summary table, a dashboard export, or a harness log line. A headline that does not recompute is a finding for evaluation-audit.
