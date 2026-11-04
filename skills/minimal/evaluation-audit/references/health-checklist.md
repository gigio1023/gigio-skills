# Health Checklist

Item-level checks per audit area, paraphrased from Anthropic's eval health checklist (Anthropic), Inspect Evals' validity and trajectory skills (Inspect), Hamel Husain and Shreya Shankar's eval-audit skill (Hamel), promptfoo, and PyRIT; revisions are in [sources](sources.md). Numbers are source defaults, not gates. Each item names evidence that must exist; producing it is evaluation-design work.

## Task design

- A claimed data source has a loading path and samples match its format. The name matches what the cases test; asking about a behavior measures statements unless the system can act (Inspect).
- Large sets get programmatic checks over every case (duplicates, balance, lengths, schema, malformed rows), then a stratified close read of about 20 to 50 cases (Anthropic). A model auditor over every case is a costlier probe.
- Success and failure are both possible with the tools, files, and services given; for agents, each step of the critical path is possible (Inspect).
- A case that asks for a disclosure or a prohibited action has a real target, so compliance is verifiable rather than apparent (Inspect).
- A reference answer passes the grader. A case nobody passes is more often broken than hard (Anthropic).
- About ten labels re-derived independently; the origin of ground truth recorded. A compared model's outputs are never gold (Anthropic).
- No surface pattern lets a trivial baseline score well; no answer leaks through the prompt, examples, tool descriptions, or readable files; tool-use cases are not answerable from memory (Anthropic).
- Coverage in both directions: should act and should not, should refuse and should not (Anthropic).
- Headroom exists, live facts in gold answers carry a check date, and generated cases are fixed at the generator (Anthropic).

## Harness (Anthropic)

- An attempt with no scorable output goes to an error record with a failure class, never a zero. Truncation carries its own status, refusal is its own outcome, and no answer differs from a negative answer.
- Each trial starts from clean state in a complete environment; seeds are pinned, order-sensitive iteration is sorted, and sampling matches production.
- Scaffold limits (a missing tool, a tight step budget, dropped context) are separated from model limits where practical, and the longest prompt and answer fit the context and output limits.
- Retries back off and are recorded per row; a pass only on retry counts as a fail by default; each case has a wall-clock ceiling.
- The model named in each response is the model requested, and system prompt, tools, version, sampling, and scaffold match production through the real entry point.
- Full trajectories per case, with grader inputs and outputs, are saved; repetitions report variance; case set, grader, and dependencies are versioned together.
- An oracle passes and a null output (empty, constant, majority class) fails through the whole pipeline, judged on the eval as a whole: a criterion that only prohibits something may pass a null, but a null that scores well overall points to a one-sided case set or metric.

## Metrics hygiene (Anthropic)

- Tokens come from the response's usage record, cost from those tokens at the served model's rates, and judge cost is recorded apart.
- Cache share is comparable across variants; latency covers the final successful request; agents get a per-call breakdown.
- Latency and throughput recorded in an eval run are unloaded and are not reported as serving performance or capacity; those claims need a load test (load-testing).

## Grader (Anthropic, Inspect)

- It rewards what the prompt asks for and grades outcomes, not a required path. For agents acting on an environment it scores the persisted end state, not the narration.
- Direct measurement over proxies. Substring matching for natural-language properties is a weak proxy unless the string is itself the ground truth (Inspect).
- Not too rigid (format, units, wrappers normalized); not too lenient (a wrong but plausible answer fails); cheat-resistant (hard-coded outputs, a readable key, degenerate policies, instructions injected into the judge's input).
- Ground truth is structurally unreachable from the system under test.
- A handful of graded failures were read; above about one in ten grader errors, fix the grader before a full pass (Anthropic).
- The same output graded twice gets the same score, or variance is reported. Separate checks over one blended score; worst-case aggregation for rare high-stakes behavior; doing nothing is never optimal; a grader crash is an error.

## Judge evidence (Anthropic, Hamel, PyRIT)

- Agreement with independent human labels, per class (true positive and true negative rates), not raw accuracy. Defaults: about 90 percent on clear cases (Anthropic); each rate above 90 percent as the target and 80 percent as the floor (Hamel).
- Few-shot examples come from a training split; the reported rates come from a held-out test split used once (Hamel).
- Empty output, "I don't know", and a confident answer to another question get the verdict the rubric requires (probes from Anthropic). All three fail a criterion that rewards a correct or complete answer. Under a criterion that only prohibits something, such as disclosing personal data or producing harmful output, the expected verdict follows the rubric and an empty output passes. When both completion and a prohibition matter, they are scored as separate criteria rather than one verdict.
- Position, verbosity, self-preference, and label-deference controls are in place (Anthropic).
- Agreement is bound to one identity (model snapshot, prompt, rubric, sampling). A change to any of them, or a shift in the scored population, triggers re-validation (PyRIT).
- Equivalent answers in different formats get the same verdict.
- Labelers had domain expertise and saw full traces (Hamel).

## Detectability (Anthropic)

- For a pass rate, the paired-difference half-width is roughly 1/sqrt(n R) at n cases and R repetitions (25 cases, 2 repetitions: about 14 points). This is a lower bound: it treats every outcome as independent and ignores item clusters and the correlation of repetitions of one case, so a measured interval is wider (1.4 times on a synthetic table of 300 prompts from 60 behaviors). When result rows exist, check the interval computed from them at the item and cluster level (evaluation-analysis) instead of the rule. Compare it with headroom and the smallest decision-relevant difference. Cheapest levers first: repetitions, cases, a paired or continuous metric.
- Splits are drawn at random, never by baseline score.
- Disabling the mechanism under study drops the score, and trajectories show it engaging.
- The headline recomputes from per-case rows; `evaluation-analysis/scripts/eval_compare.py` recomputes rates and paired differences after a key and grain check.

## Sampled trajectories (Inspect)

Read a sample, or scan with a model once the cost is approved (Inspect suggests at least 100 samples). Decide what each flag invalidates:

- external failure (rate limit, network, missing dependency): the failure;
- formatting failure with a correct answer: the failure, under the intended measure;
- shortcut or reward hacking: the success;
- refusal: its own outcome, never a capability failure.

## Execution budget and elicitation campaigns

- Turns, tokens, and wall time are stated per system and equal or declared across compared systems; budget exhaustion is its own outcome.
- Success rate is over validly graded results only, with errors counted apart; zero graded results is inconclusive (promptfoo).
- A baseline pass without the technique exists, so its added effect is measurable (PyRIT).
- For tool-using targets, success is judged on persisted state; a final refusal does not undo a write (promptfoo).
