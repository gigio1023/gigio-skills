# Measurements

Use when a document presents data, equations, or comparison tables. Check the underlying evidence and calculations before optimizing the presentation. A restrained style can still make a false comparison appear credible.

## Specify the measured quantity

Identify the unit of observation: request, user, run, machine, task, or dataset example. Keep counts distinct from independent trials. State the relevant population, period, version, hardware, workload, concurrency, warm-up, caching, budget, and success criteria where they affect interpretation. Avoid repeating the full setup beside every number; expose the decisive conditions locally and link a useful methods section.

Define nonstandard metric boundaries. Does latency start before queueing? Does it include retries? Is throughput completed work or attempted work? Does a success rate include timeouts? Is cost per attempt, per successful task, or per token? Do not let familiar metric names hide different calculations.

Compute arithmetic with code or a spreadsheet. Show numerator and denominator when a rate would otherwise be ambiguous. Keep absolute differences, relative changes, ratios, and percentage-point changes distinct. Do not average subgroup percentages with incompatible denominators or silently pool dependent trials. Display precision supported by the measurement rather than every decimal available from a tool.

## Preserve uncertainty and the comparison

Use the same measure, unit, population, and relevant budget across compared systems. If a difference is unavoidable, make it visible and qualify the conclusion. Separate measurement at a historical revision from current product behavior. A source's self-reported benchmark remains an attributed result until independently reproduced.

Keep missing, not measured, failed, timed out, and zero distinct. State how censored or failed observations enter the summary. A lower successful-request latency can coexist with more failures; show both when the decision depends on reliability. Report variability and uncertainty when they affect ranking or a proposed threshold. Label intervals with their type and construction.

A repeated run, an ablation, a paired comparison, and a causal intervention answer different questions. Describe the actual procedure. If a confidence interval or significance test was not computed, do not invent one; report the observed variation and the limitation it creates. “Not statistically significant” is not proof of equivalence.

## Tables

A short table can still be dense when its cells mix methods, results, interpretation, and source history.

Make column headings carry repeated context: units, metric names, direction when unclear, and relevant settings. Align numeric values for comparison, keep precision consistent, and order rows for the reader's question. Use restrained emphasis on the meaningful comparison, not a badge in every cell. A status column can be useful; a “verified” decoration usually does not add evidence.

Keep conditions that change a row's interpretation beside that row. Use a short note for a shared exclusion or measurement rule. Cells should hold values, identifiers, or short phrases; put extended explanations beside the table. When comparing qualitative attributes, use consistent short descriptions and explain the deciding trade-off outside the grid. A one-row table of unrelated facts is often clearer as a sentence or list. Do not fill missing cells with invented zeroes.

For alternatives, compare the same decision dimensions and explain the chosen trade-off in prose. Avoid a composite score unless its meaning and weights are justified for this decision.

## Equations, code, and reproduction

Define each symbol's meaning, unit, and domain before or beside its first useful use. Explain what the equation computes and why it is the right quantity; do not use notation to make ordinary arithmetic look scientific. Keep the displayed formula, implementation, and reported value consistent. Refer to equations by number only when that helps navigation.

A code example should demonstrate the behavior under discussion with the smallest meaningful context. Mark pseudocode as such, preserve assumptions affecting order or state, and keep executable examples aligned with the documented version. A historical RFC's provisional syntax is evidence of its design argument, not a modern copy-paste example.

Keep input references, transformation code, configurations, and actual results in the authorized project. Use stable links and versions rather than personal paths in a shared report. Distinguish reproduction instructions from a reproduction already performed. Never manufacture plausible output because a run or download failed.

## Output checks

Verify calculations independently of formatting. Check that tables and text use the same population and definition.
