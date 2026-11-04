# Categories and Multiplicity

Read this before reporting per-category results, comparing several models at once, or looking at a campaign's results before it finishes.

## Declare the family

- The family is the set of tests whose results the reader will act on together: usually every category of one comparison, and every pair when several models are claimed in one report. Write it down before testing.
- A cut chosen after seeing the data, such as long prompts, one language, or the category that looked interesting, is exploratory. Report it as such, without an adjusted p-value, and do not add it to the family afterwards.
- The family size counts every declared test, including a category that could not be estimated; the script enters such a category as p = 1 so the correction does not shrink.

## Test each category

- Use the paired item-level difference within the category, clustered at the same level as the overall comparison, with t(C-1) where C counts the clusters inside the category.
- Prompt-level p-values that ignore clustering overstate significance. In the synthetic trial, four of six categories had prompt-level p below 0.05, two had clustered p below 0.05, and one survived Holm on the clustered p-values. Per-category clustered t(9) intervals covered 95 percent of the time; prompt-level z intervals covered 88 percent.

## Choose the correction

- Holm controls the family-wise error rate: the chance of any false claim in the family. Use it when each category's result is stated on its own, as in a customer report that names which categories regressed.
- Benjamini-Hochberg controls the false discovery rate: the expected share of false claims among those declared. Use it to screen which categories deserve a closer look.
- Name the correction beside the table. Unadjusted p-values can stay in the table for reference; the claim uses the adjusted ones.

## Small categories

- A small category keeps its own interval, however wide; the width is the result. Do not merge categories after seeing results to reach significance.
- A category with fewer than two clusters cannot support a clustered interval. Report its counts and its difference without a test.
- An aggregate difference can come from one category; in the synthetic trial most of model B's gain came from fraud. Show the per-category table beside the aggregate, as evaluation-audit's release mode requires.

## Peeking and stopping

Looking at interim results of a running campaign and stopping when a difference becomes significant inflates false positives. Fix the stopping point in advance; an analysis of a partial campaign is labelled interim and exploratory. Which runs have finished is evaluation-operations' record.

## Inconclusive is not equivalence

An interval that includes zero does not show that two models are equal. To claim no regression, compare the interval with an equivalence margin, normally the smallest decision-relevant difference evaluation-design recorded, and say whether the whole interval lies inside it.
