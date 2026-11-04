# Data and Comparison

Use when selecting measures, transforming data, or choosing a display. Work from supplied files, queries, or a documented API. Establish the comparison before styling it.

## Define the measured quantity

Inspect the unit of observation, population, period, time zone, versions, and aggregation. State the conditions that change interpretation where readers encounter the result. Keep the source query and transformations in the project; expose authorized source links and definitions when they help the reader interpret, reproduce, or act on the result.

Name the actual metric boundary. Completion rate counts completed work over attempted work; latency may describe only successful requests. A cost per attempt and a cost per completed task answer different questions. When a filter changes the population, recompute the appropriate denominator with it.

Use code or a spreadsheet for totals, rates, differences, and rankings. Preserve raw numeric values for calculations and sorting; round for presentation. Compute combined rates from the combined compatible numerators and denominators. Retain subgroup results when their differences change the decision.

### Synthetic arithmetic example

The teaching examples use these independently invented inputs:

- Baseline: 92 completed out of 100 attempted; successful-request median latency 240 ms.
- Candidate: 96 completed out of 100 attempted; successful-request median latency 180 ms.
- Other requests timed out.

The completion-rate difference is **4 percentage points**. The relative increase is approximately **4.35%**. The successful-request median latency reduction is **25%**, computed as `(240 - 180) / 240`. Keep these quantities separately named.

For a weighting example, combine groups with 9/10 and 10/100 completions as **19/110**, approximately **17.27%**. The unweighted average of their rates answers a different question from overall request completion. Use that average only when the equal-group estimand is actually intended.

A zero denominator produces an undefined rate, not a measured 0%. Keep failed, timed-out, missing, stale, and zero observations distinct in both calculations and labels. Interpolation can help a time view when its method and affected interval are visible; it remains an estimated value rather than a new observation.

## Preserve what makes the comparison fair

Use compatible definitions, units, populations, and relevant resource budgets. If conditions differ, show the difference and qualify the comparison. Put an important cost alongside the apparent benefit: latency with completions, utilization with capacity, a rate with its sample count, a mean with the subgroup or tail that matters.

Choose aggregation according to the quantity. An arithmetic mean, weighted rate, median, and geometric mean describe different properties. A benchmark site's geometric mean is a useful example of summary-plus-detail, not a default for unrelated metrics. Where uncertainty affects ranking, use justified intervals or observed variation and name the method. An untested difference is neither statistically significant nor proven equivalent.

Attach an event annotation to its actual time and population. Describe temporal coincidence as an observation; use causal wording when the design and evidence support it. A link next to a hypothesis does not establish that cause.

## Choose the encoding by the question

| Reader question | Starting display | Preserve |
| --- | --- | --- |
| Which category is higher? | Sorted bars or dots | Comparable quantities and a common scale; a meaningful zero for bars |
| What changed over time? | Lines with relevant event annotations | Actual intervals, gaps, period, time zone, and consistent definitions |
| Where is variation or a tail? | Distribution, histogram, quantiles, or box plot | Sample count, binning or summary method, and important subgroups |
| Which trade-off should I choose? | Scatterplot, aligned small multiples, or comparison table | Decision-relevant dimensions and each option's costs |
| Which exact record needs attention? | Prioritized searchable table | Units, stable row identity, status, and reason for priority |
| How is a total composed? | Stacked bars or a concise composition view | A valid part-whole relationship and comparable segments |
| Are two quantities moving similarly? | Aligned panels or an indexed comparison | Original units where needed and the index baseline |
| Does location explain the question? | Map with an accessible list or table | Coverage, spatial unit, source, and the selected measure |

For a difficult chart choice, compare candidate encodings on the same data. Dual axes can make relationships appear or disappear as scales change. Prefer aligned panels when each quantity's movement matters independently; use indexing when relative movement from a meaningful baseline is the question. Use dual axes only with clearly identified quantities, defensible scales, and a reader task that benefits from them. [Datawrapper's comparison](https://datawrapper.de/blog/why-i-changed-my-mind-on-dual-axis-charts) demonstrates evaluating alternatives rather than treating one chart type as universally correct.

## Make the evidence readable

Give the decisive comparison adequate space. Put units in headings and axes, align numeric columns, and use consistent precision. Prefer direct labels when they reduce lookup effort. Keep color meanings stable and add a text or shape cue for status. Put a material exclusion or definition beside the affected result; put longer reproducibility detail behind a useful link or in methods.

Use an exact table when the reader needs to inspect values, and a chart when pattern recognition is the task. Add an accessible summary or data representation where needed. Select details by what changes the reader's judgment, not by a fixed card or chart count.

Write a stated finding in three parts. The conclusion comes first. At most four reasons follow, each tied to a value or view on the page. The scope closes it: the population, period, version, and selection under which the finding holds. More than four reasons usually means several findings or reasons that restate one another, so split or rank them. An important contrary result is one of the reasons or a limit in the scope, beside the conclusion rather than in a footnote. With the synthetic inputs above: *Candidate completes more requests at a lower median latency.* Reasons: 96 versus 92 of 100 completed; successful-request median 180 versus 240 ms. Scope: one 100-request replay, with timeouts excluded from latency.

## Check the result

Independently compute representative values, including the combined population and a subgroup. Compare them with the displayed rows, cards, chart, finding, and export. Test zero denominator, missing records, duplicates, changed period, and an important contrary subgroup where those risks apply. Inspect the result at the delivered size.

Foundations: [IBM Carbon dashboards](https://carbondesignsystem.com/data-visualization/dashboards), [Datawrapper on chart text](https://datawrapper.de/blog/text-in-data-visualizations), and [Wilke on making a point](https://clauswilke.com/dataviz/telling-a-story.html). See [pattern examples](pattern-examples.md) for operational and analysis applications.
