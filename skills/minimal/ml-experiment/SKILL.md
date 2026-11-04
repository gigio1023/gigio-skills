---
name: ml-experiment
description: >
  Design, run, or interpret an ML experiment: a training, fine-tuning, or
  weight-adaptation comparison, an inference or serving configuration
  comparison at pinned revisions, a reproduction, or the training data it
  needs. NOT for what an eval measures or its cases (evaluation-design),
  analyzing per-item eval results (evaluation-analysis), a verdict on a
  built eval (evaluation-audit), operating a multi-run
  campaign's state (evaluation-operations), latency, throughput, or capacity
  under load (load-testing), or literature (literature-research).
---

# ML Experiment

Turn an empirical question into evidence that supports a decision: a comparison that can answer it, training data fit for its intended use, and a serving configuration whose results you can attribute. A trained checkpoint, a working runner, or a higher number is not by itself that evidence; a negative finding or a bounded unresolved question can finish the work.

Use only the parts the task needs. A training comparison, a serving comparison, and a reproduction each stand alone, and one question often needs two. What an evaluation measures, and whether a built evaluation can be trusted, belong to the evaluation skills below.

## Start from the question

Recover the question, the decision the answer could change, existing results, the model, data, and serving setup in use, and the constraints before asking. Name the unit being compared (a run, record, response, or task completion) and keep counts in that unit; records, source groups, and independent observations are not interchangeable.

A design or review request returns findings. Building, training, adapting, or executing needs the corresponding request. Fast checks within the same question and always-on resources (those already running at no added cost) may proceed. Present the observation, the proposed change, and one sentence predicting the result before changing direction, before any run that spends beyond the always-on tier or the project's stated budget, and before long new work, unless that activity is already authorized. Spend is the gate, not duration: a short run on paid accelerators needs the same presentation as a multi-day one. When the project has a praxis profile (the profile `praxis-direction` sets up, when installed), its compute ladder and approval threshold define the tiers; without a profile, the always-on tier is the resources the user already approved for this work. Data access, shared hardware, external annotation, and provider limits still apply to short runs, and public availability does not establish permission or consent.

Use the project's runner, records, identifiers, schemas, and plan. Do not create a new tracking framework, registry, or harness.

## Experiment

State which alternatives the next observation could distinguish and how the answer would change the work. For performance improvement, identify the intended benefit and a credible current baseline; for reproduction, the original claim and its conditions. Choose the smallest comparison that can answer this round: the changed factor, the baseline, comparison conditions, meaningful outputs, and why it is informative. Tune nuisance settings fairly when they interact with the factor under study; identical settings are not always a fair comparison. Separate exploratory selection from a confirmatory comparison.

With little compute, iterate at the smallest model and data scale at which the phenomenon still appears, and say when a result may not transfer to full scale. With little data, spend it on evaluation before training: a few hundred labelled examples usually buy a credible measurement and rarely a credible fine-tune.

For requested execution, inspect the actual runner, checkpoint, preprocessing, split, objective, optimizer, schedule, compute allocation, and result records the experiment depends on, following the framework's version-specific documentation. Before an expensive run, use an authorized small check that data reach the intended computation, losses and gradients behave plausibly, checkpoints save and load, and the measurements can be recovered; a smoke test establishes readiness only. Keep enough identity to tie results to their inputs and configurations, preserve unsuccessful attempts, and inspect live state before restarting. When the runs form a sweep or ablation campaign that spans runs or sessions, evaluation-operations keeps its attempts, ownership, priorities, and resume or rerun decisions; this skill designs the comparison and decides whether a single run is ready or recoverable.

Read [design and interpretation](references/design-and-interpretation.md) for baselines, interactions, variance, or inconclusive outcomes, and [training and recovery](references/training-and-recovery.md) for execution decisions.

## Training data

Recover the target task, intended population, unit of observation, source material, permitted handling, and the data decision the recipe needs: what to train on, which known problem to revise, or whether the data supports the intended behavior change. Inspect real records before prescribing categories.

- Match the target formatting to the recipe. Prompt and target templates, masking, and special tokens are part of the training setup, not cosmetic, and a formatting mismatch is a common silent failure.
- Check for contamination with evaluation material. Training data that overlaps the evaluation set, by exact records or by near-duplicates, inflates every later number and cannot be undone after the run.
- Relate sampling weights and coverage to the target population. Convenience sources, oversampling, and synthetic examples change the distribution the model learns; distinguish construction counts from deployment prevalence.
- Treat label noise as a measured quantity, not an assumption. A model-generated label is a candidate until the required review establishes it, and preserving disagreement is better than forcing uncertain items into a clean label.

Pair structural checks with content review sampled across relevant groups and failure modes; a reviewed sample is not proof that every record is correct. Read [construction and review](references/construction-and-review.md) for sampling, annotation, splitting, generated data, or lineage decisions. Evaluation case sets and the review of evaluation labels are designed in evaluation-design, not here; a corpus that serves both evaluation and training keeps the split rules of both.

## Serving and inference comparisons

A number is only attributable to the configuration and mode that produced it. Before freezing a serving setup for a full campaign, establish what you are actually comparing. These comparisons choose a configuration by what it produces: outcome class, quality, and the effect of a mode. Latency, throughput, and error rate under concurrent load are a load test's measurement (load-testing); timings from an unloaded comparison run are not capacity or performance evidence.

- Pin revisions. The model, tokenizer, serving engine, and quantization each have a version; a mutable alias can resolve to a different checkpoint between runs, so record the resolved revision, not the alias.
- Treat a mode switch as a first-class variable. Reasoning on or off, a thinking budget, a tool-use mode, or a decoding preset can move the result as much as the model choice, so vary it deliberately and report which mode each number came from.
- Bind published model-card numbers to the serving configuration and mode they were measured under. A card figure measured with reasoning off, on a specific engine and sampler, does not predict a reasoning-on deployment on a different stack; carry the conditions with the number or do not reuse it.
- Run a small comparison before freezing a configuration for a full run. A short comparison at pinned revisions can show that a mode, a sampler, or an engine changes the outcome class, for a fraction of the cost of discovering it after a full campaign.

## Interpret and report

Inspect actual outputs, comparison conditions, and errors. Separate measured observations from explanations and untested expectations. Before attributing an apparent improvement to the intended change, generate rival explanations from genuinely different classes and name a check that would separate them:

- measurement or processing artifact: a changed scorer, a truncation setting, or a parsing difference raised the number without the capability changing.
- confound: data, compute budget, or a serving mode changed alongside the factor under study, so the comparison does not isolate it.
- selection: the result was chosen on validation outcomes, or the cases favour the candidate.
- reverse causation: the outcome shaped the training or selection, rather than the change producing the outcome.

This rival-class framing is adapted from K-Dense hypothesis-generation (see [sources](references/sources.md)). Prefer a check where the rival and the intended explanation predict meaningfully different outcomes. Repetition and uncertainty estimates should answer a real decision question at the actual independent unit, not satisfy a fixed seed-count ritual. An inconclusive difference is not equivalence.

Report the result at its supported strength with the conditions that matter to the reader, and keep full configuration and provenance in the project records. Do not hide a consequential failure to make a conclusion more favourable. Record what changed in the project's understanding, where the decisive result lives, and the next action or proposed test. Broader direction changes remain the user's decision.

For a weight-adaptation or capability-preserving comparison, read [model adaptation](references/model-adaptation.md); it applies whenever the task changes one behavior while trying to preserve the rest.

## Pointers

- evaluation-design decides what an evaluation measures: its failure modes, case set, code checks, judges and their validation, and comparison conditions.
- evaluation-analysis analyzes per-item eval result rows: grain and outcome checks, clustered and paired intervals for rates and model differences, and per-category multiplicity.
- evaluation-audit gives a launch, hold, or report verdict on a built evaluation, benchmark, judge, harness, scoring change, or result.
- evaluation-operations keeps the evidence-backed state of an approved multi-run campaign, evaluation runs or training and ablation runs alike: attempts, ownership, priorities, resume and rerun decisions, and results.
- load-testing measures latency, throughput, errors, and capacity of a serving endpoint under load.

Read [sources](references/sources.md) when maintaining this package.
