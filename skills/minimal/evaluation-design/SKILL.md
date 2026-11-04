---
name: evaluation-design
description: >
  Design or build an evaluation of an LLM system or model, or change what one
  measures: failure modes, cases and labels, code checks and validated judges,
  comparison conditions with execution budgets, and the smallest difference
  the decision needs. NOT for a verdict on a built eval (evaluation-audit),
  analyzing result rows (evaluation-analysis), operating a multi-run campaign
  (evaluation-operations), training data or a
  training comparison (ml-experiment), latency or capacity under load
  (load-testing), benchmark surveys (literature-research), choosing eval
  tooling, or harness code that leaves the measurement unchanged.
---

# Evaluation Design

Produce a measurement contract: a proposal stating which decision an eval informs, which behaviors and failures it reveals, on which cases, scored by which checks, under which conditions, and at what resolution. When building is requested, also produce the instrument in the project's runner. A large case set, a working runner, or a judge that agrees with itself is not by itself a sound measurement, and the designer does not certify its own work: a launch, hold, or trust verdict belongs to evaluation-audit, which reads the artifacts rather than this skill's summary.

A design request returns a proposal. Writing cases, labels, judges, or runner code needs the request. Fast checks within the always-on tier may proceed. Present spend beyond the always-on tier or the project's stated budget first, with one sentence predicting the result; a praxis profile's compute ladder defines the tiers when present; without a profile, the always-on tier is the resources and API quota the user already approved for this work. Use the project's runner, records, and schemas; do not create a new harness or tracking framework. If the request turns out to be a runner fix, a status question, or a verdict on an existing eval, say so and hand it to its owner.

## The decision

Name who acts on the result and what they decide: launch a campaign, adopt a model or configuration, change a prompt, report to a customer, or support a research claim. Then name the smallest difference that would change that decision, in the eval's own unit, such as the margin a candidate must beat the incumbent by before a switch. The rest of the design is sized against it. If nobody can name the decision or the difference, record the eval as exploratory: its numbers can describe behavior but cannot gate a choice.

Name the unit being scored (case, trial, episode, conversation, task completion) and keep counts in it. Report task success, policy compliance, quality, cost, and latency apart when one score would hide a trade-off.

## Real outputs before failure categories

Read real outputs of the system under test before fixing failure categories. A deployed system has production traces; a new capability has pilot trajectories, and a few pilot runs on draft cases are enough to start. Note what went wrong in each output, then group the notes into failure modes. Categories from a taxonomy, a prior benchmark, or a generic quality list are hypotheses until outputs show them, so record which modes were observed and which are only proposed. Sample at random as well as by outliers or clusters. A failure that exists because the prompt never asked for the behavior is a specification fix before it is an evaluator.

## Case set and eval labels

- Cover intended behaviors and their boundaries in both directions: cases where the system should act and cases where it should not. A safety eval measures over-refusal on benign requests that resemble disallowed ones; a tool-use eval includes cases where calling the tool is wrong. A one-sided set lets a degenerate policy score perfectly.
- Give each case an observable success condition and a reference solution that passes the scorer.
- Split eval data by the unit of generalization (source, entity, conversation, task family, time), and keep cases used to tune the system or its judge apart from cases that report the result.
- Treat model-generated labels and cases as candidates until the review the decision requires establishes them, and record who or what produced each label.
- Preserve disagreement: an ambiguous item stays marked with its competing labels instead of being forced into a clean label.

Read [cases and labels](references/cases-and-labels.md) when building or revising a case set, writing a label definition, or choosing a split. Training data for a model under adaptation belongs to ml-experiment; a corpus that serves both evaluation and training keeps the split rules of both.

## Code checks before model judges

Check each failure mode with code when a rule can decide it from the output or the end state: parsing, schema, string or value match, execution, or a state query. Use a model judge only for the interpretive remainder. The default is one binary judge per failure mode, with explicit pass and fail definitions, and severity expressed through several binary judges. A validated ordinal scale is defensible when severity itself is the quantity, as in harm severity. A holistic "is this good" judge yields verdicts nobody can act on. For an agent that acts on an environment, score what it left behind rather than its narration, and grade the outcome rather than one prescribed path.

Validating a judge is part of building it, because new reference labels and agreement measurements are new evidence. Read [judge validation](references/judge-validation.md) when writing a judge, measuring it against reference labels, or re-validating after a change. Read [measurement and scoring](references/measurement-and-scoring.md) for denominators, outcome classes, aggregation, and uncertainty. Analyzing the result rows of a run, with grain checks, clustered and paired intervals, and per-category multiplicity, belongs to evaluation-analysis.

## Comparison conditions

Fix and record everything that affects the claim:

- the requested model revision and the model that actually served each request, read from the response;
- system and user prompts, tools and scaffold, decoding settings, and the information available to the system;
- the execution budget in turns, tokens, and wall time, since budget exhaustion is an outcome and a different budget is a different comparison;
- cost and latency as measured conditions: tokens from the provider's usage records, judge cost apart from target cost, latency from the final successful request. An eval run is unloaded, so its latency compares conditions within the eval and is not evidence of latency or throughput under concurrent load, which load-testing measures.

When the decision concerns a deployed system, call its real entry point with its production configuration; a reimplemented call measures something else. Put the noise floor next to the smallest decision-relevant difference before the full pass, and budget repetitions and cases together when sizing the set. If the noise floor exceeds the difference, say so with the numbers and offer more repetitions, more cases, a paired design, or a more sensitive metric.

## Building on request

Implement the agreed cases, checks, judges, and aggregation in the project's runner. While building, run an oracle (reference answers or a known-good variant, which should pass) and a null (empty output, a constant answer, or the majority class, which should fail the eval as a whole, though a criterion that only prohibits something may pass it) through the full pipeline, plus hand-worked boundary, invalid, and missing outputs through the actual scoring path. Keep each probe's raw output where evaluation-audit can read it and state what each established; a mock response validates scorer logic, not target performance. Return a built instrument with its probe results, never a readiness verdict.

## Adversarial evaluations

When the eval asks whether a system can be driven past its policy or trust boundaries, read [adversarial evaluation design](references/red-team-design.md). Run accounting for such campaigns belongs to evaluation-operations.

## Measurement contract

Mark the contract "Proposal: not checked by evaluation-audit" until that audit has run. It states, at the length the decision needs:

- the decision, who makes it, and the smallest decision-relevant difference;
- the unit, population, case set version, both-direction coverage, and label provenance;
- failure modes marked observed or proposed, the check for each, and each judge's identity and validation status;
- metrics with numerators, denominators, and outcome classes;
- comparison conditions including the execution budget, and the noise floor at the planned repetitions and cases;
- when built: what was implemented, which probes ran, and where their outputs live;
- open conditions the audit or the user must settle.

Read [sources](references/sources.md) when maintaining this package.
