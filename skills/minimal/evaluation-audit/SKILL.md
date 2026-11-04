---
name: evaluation-audit
description: >
  Give a launch, hold, or report verdict on a built eval, benchmark, judge,
  harness, or scoring change, or on a result before it informs a decision
  or reaches a customer. Checks each readiness claim against artifacts at
  current revisions: oracle and null passes, the served model, data and labels,
  grader errors, sampled trajectories, denominators. NOT for designing an eval
  (evaluation-design), analyzing result rows (evaluation-analysis), operating
  a multi-run campaign (evaluation-operations),
  load or capacity test results (load-testing), or finding code bugs
  (bug-diagnosis).
---

# Evaluation Audit

Return one verdict for the audited artifact and the decision it serves. Launch and hold apply to an instrument before it is used: an eval, benchmark, harness, judge, or scoring change. Report and hold apply to a result before it informs a decision or reaches a reader.

- **Launch**: the instrument can carry the named decision at the named scope. Launch is a verdict, not authorization; the campaign or merge proceeds under its own approval.
- **Report**: the result can inform the decision or reach its reader at the stated strength, with the listed caveats.
- **Hold**: at least one claim fails, or is unverified in a way that could change the decision, and the table names what clears it.

State the decision and its scope first (a pilot, a full campaign, a merge, an internal decision, a customer report), because the same eval can be fit for one and not another. Give the verdict as a table with one row per readiness claim.

Synthetic example. Verdict: hold, for a full campaign.

| Claim | Evidence | Verdict | Condition to clear |
| --- | --- | --- | --- |
| Reference answers pass the grader | Oracle probe, 5 cases, runner at `a1b2c3d`: 5 of 5 pass | Holds | None |
| Timeouts are excluded, not scored | `runner/score.py:88` maps a timeout to score 0 | Fails | Owner routes timeouts to the error record; rerun the null probe |
| Judge agrees with human reference labels | No validation results for the current judge prompt | Unverified | Validation on independent labels (evaluation-design) |

Row verdicts are holds, fails, or unverified. Unverified is not failed: keep a defect apart from evidence that was unavailable.

## Authority

The audit is read-only on project records. Design documents, configs, case sets, labels, result files, and campaign records stay as they are.

- Cheap probes inside the always-on tier (resources already running at no added cost) may proceed without asking: a handful of cases end to end, an oracle run and a null run on a few cases, a served-model check on a smoke case. Keep their outputs out of the project's result records and note the revision they ran on.
- A costlier probe (a full pass, a model auditor over every case, paid accelerators, a fresh judge validation round) becomes a condition to clear, listed with one sentence predicting what it would show. Run it only on request. When the project has a praxis profile (the profile `praxis-direction` sets up, when installed), its compute ladder defines the tiers; without a profile, the always-on tier is the resources the user already approved for this work.
- Never repair the eval while auditing it. A fix goes back to evaluation-design or to the artifact's owner as the condition to clear, stated as the smallest change that would clear it. An auditor that certifies its own patch grades its own work, the failure a separate audit exists to prevent.

## Read the artifacts, not the claims

Audit what exists at its current revision (runner and grader code, case set and labels, judge prompt and model, environment, raw result rows) and record each revision read. A design document, PR body, README, or worker summary that says ready, validated, or verified end to end supplies claims to check, not evidence. Collect every verifiable claim first (data provenance, mechanism, coverage, reported numbers) and give each its own row.

Before any other check, run the eval end to end on a handful of cases, or find a results file produced at the current revision. Code that does not run at its current revision is the first finding, and the verdict is hold.

## The checks

Cover the areas the audited artifact touches; a scoring change needs no case-set review. Read [the health checklist](references/health-checklist.md) for item-level checks per area and their sources.

- **Task design**: each case can be both passed and failed with the affordances given, labels and their origin are correct, nothing leaks the answer, and coverage runs in both directions.
- **Harness**: infrastructure errors and model failures land in separate records; truncation is visible; trials are isolated and deterministic; the served model is the one requested; configuration matches production; trajectories are saved.
- **Metrics hygiene**: tokens and cost come from recorded usage, latency from the right boundaries, and judge cost is kept apart. Latency or throughput from an unloaded eval run is not presented as performance or capacity under load, which needs a load test (load-testing).
- **Grader**: rewards outcomes over paths and, for agents, the end state; is neither too rigid nor too lenient; resists cheating; uses ground truth the system cannot reach; has its failures spot-checked; is deterministic or has measured variance.
- **Judge evidence**: validation results against independent reference labels exist for this judge identity (model snapshot, prompt, rubric, sampling), format sensitivity was tested, and re-validation triggers are stated. Producing new labels or agreement measurements is evaluation-design work.
- **Detectability**: the noise floor is below the smallest decision-relevant difference, the mechanism under study is actually wired, and the headline recomputes from raw rows. When a result's interval is missing or ignores clustering or repeated samples, the condition to clear is an evaluation-analysis run on the raw rows.
- **Sampled trajectories**: a sample was read for external failure, formatting failure, shortcut or reward hacking, and refusal, since each can invalidate a success or a failure.
- **Execution budget**: turns, tokens, and wall time are a comparison condition, equal or declared across compared systems, and budget exhaustion is counted as its own outcome.

For a campaign whose cases try to elicit unwanted behavior, the checklist adds verifiable compliance, a baseline pass without the technique, and denominators over validly graded results.

## Scoring-change gate

A change to a scorer, metric, answer extraction, verdict parsing, or code that consumes a grader's output moves reported numbers. Establish three things: the bug exists (it reproduces at the base revision through the shipped wiring, not a stub), the fix removes it (same inputs, changed revision), and what else moves (which numbers change, in which direction, how often over real outputs, and whether the change declares it). If the first two cannot be run, the verdict is hold with those rows unverified. Read [scoring change](references/scoring-change.md) for reachability, exclusion values, swallowed errors, and whether tests pin both sides.

## Release mode

Use release mode when a result will reach a customer or another external reader; credo-release, when installed, is its paper counterpart. On top of the checks above, a report verdict requires:

- a comparability tag on each number: harness or tool version, judge identity, case set version, and denominator, since numbers compare only under the same tag;
- the caveats that could mislead, stated before the result;
- the provenance and license of the eval items, and whether this reader may receive them;
- neutral framing: the measured behavior under the stated conditions, no ranking or generalization the measurement does not support, and per-category results that a single aggregate does not replace;
- a hand-off of the writing: the audit supplies the verdict, tags, and caveats, and the requested writing skill or method writes the prose.

## Report

Order findings by severity. Lead with anything that makes a number actively misleading: infrastructure errors scored as model failures, no answer conflated with a negative answer, ground truth the system can reach, gold labels taken from a model under comparison, a split selected by score, a noise floor larger than the difference sought, a nondeterministic judge. Then list what adds noise or limits generality without flipping the conclusion.

Frame each finding as an observation with its evidence location (file and line, case id, trajectory step, revision), why it could matter, and the condition that clears it; the owner often has context the audit lacks. Report what matters for the decision, not every deviation from an ideal. An audit that finds nothing wrong is a valid result; say so, with what was checked.

Read [sources](references/sources.md) when maintaining this package.
