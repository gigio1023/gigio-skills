---
name: evaluation-operations
description: >
  Operate, resume, monitor, or reconstruct the evidence-backed state of a
  multi-run campaign, whether its runs are evaluations or training and
  ablation runs: durable attempts, resume and rerun decisions, ownership,
  priorities, and results. Use when approved work spans runs or sessions and
  its live progress or results must stay accurate, as in "where is the
  campaign", "resume the sweep", "which ablation runs finished",
  "캠페인 상태 확인해줘", or "ablation 이어서 돌려줘". NOT for designing what an
  evaluation measures or its cases (evaluation-design), designing a training
  comparison or readying and recovering a single run (ml-experiment), a
  verdict on a built eval or its result (evaluation-audit), statistical
  analysis of result rows (evaluation-analysis), load or capacity
  tests (load-testing), generic code review, or a one-off evaluation run.
---

# Evaluation Operations

Maintain factual operational control of a multi-run campaign, whether its runs are evaluations or training and ablation runs: preserve what happened, keep already approved work moving when requested, and report only what current evidence establishes. Designing the comparison a sweep runs (its factors, baselines, and seeds) and deciding whether one run is ready or recoverable from its saved state belong to ml-experiment; designing what an evaluation measures belongs to evaluation-design; the statistical analysis of finished result rows, with grain checks and clustered, paired intervals, belongs to evaluation-analysis. This skill supplies the working method. The project supplies its runner, scheduler, manifests, registries, and deterministic checks; do not replace them with a new campaign framework, controller, daemon, schema, or parallel spreadsheet.

## Select the authority mode

Use the mode the request actually grants, and keep it throughout the work unless the user changes it.

- **Status or diagnosis** is read-only. Inspect sources and report the state; do not rewrite source records, launch work, restart work, rescore, or rerun.
- **Resume or execute** permits only work already approved for its models or targets, data, configuration, budget, resource limits, and other stated bounds. It can use the project's canonical durable records as the operation requires.
- **Monitoring** is observational unless the request also grants execution or a specific change. Waiting for completion does not authorize dispatch, retries, rescoring, cancellation, or record repair. Define the terminal condition and use a supported sustained-observation route as described below.

Reuse an existing session grant; do not ask for it again. An authorized runtime model or API call needed by the approved campaign is part of that execution and does not need repeat approval. A status request, idle capacity, a prepared configuration, a source location, or a queued-looking record does not authorize execution. Keep external publication, a new costly experiment, a model or API call outside the approved campaign or its limits, scheduler installation, destructive cleanup, and access to an unapproved host in separate scope.

Keep private inputs, results, and source maps outside this package and within the approved sharing scope. Logs, errors, and commands can contain prompts, responses, personal identifiers, local paths, and signed URLs; share only the necessary redacted diagnostics and retain raw evidence in approved storage under its retention policy. Credentials stay in the configured secret mechanism, never in reports or worker packets. Use only approved destinations and providers; do not transmit material to a new provider merely to obtain cheaper routing.

## Bind the campaign to its actual records

Before drawing a conclusion or taking an action, find the available project-defined records or explicit coordination that establish campaign scope, priorities, durable attempts and results, raw outputs, live runtime state, and applicable budget, resource, ownership, and validation rules. A project may use a manifest or queue, but a simple approved campaign may instead use a verified single owner and a small task record. Read [project binding](references/project-binding.md) when those sources are not already clear, disagree, or must be reconstructed.

Do not invent a universal record shape or make a second registry. If an authorized operation needs its first durable task or attempt record, create the smallest record supported by the project's normal location and practice, not a new framework or parallel spreadsheet. A file location, configuration, launch request, or local synthetic fixture is evidence of preparation or possible provenance, not proof that inference or training ran or a result was validated. If the project has no source or coordination for a fact needed to act, identify the smallest missing source or authority rather than filling it in from an assumption.

## Reconcile facts, not optimistic labels

Reconcile current live handles, jobs, processes, and logs with durable attempts and raw outputs. Preserve disagreements and name the evidence for each side. Treat an agent or worker report as a lead to reconcile, not proof of completed inference or a validated result. A lost handle or stale process identifier is not proof that work stopped; check an available scheduler, runtime, log, or project-defined recovery record before retrying. Never launch a duplicate merely because a handle is unavailable.

Keep these facts distinct even if a local project displays them under one status field:

- infrastructure or input readiness;
- inference completion;
- scoring completion;
- validation and comparability.

A training or ablation run has the same separation: a launched job, a finished training process, a saved checkpoint that loads, an evaluated checkpoint, and a comparable result are different facts. They can overlap or pipeline and do not require a new shared enum. A launch being accepted, queued, or prepared is not completed inference. A completed inference is not necessarily scored. A score is not necessarily validated or comparable. Treat a null, missing, or unreadable value as unknown unless the project's own contract says otherwise; it is never zero by default.

Use the project's deterministic checks where available, and describe precisely which fact each check establishes. Do not call a static source inspection, a hypothetical command, or a fixture-backed local check a real execution result.

For a campaign whose cases try to elicit unwanted behavior, read [adversarial runs](references/adversarial-runs.md) for its denominators, outcome classes, baseline pass, and replay records.

## Preserve identity, attempts, and result lineage

For each observed attempt, retain enough project-defined provenance to distinguish the actual provider or target, model identity and revision, runtime, prompt or configuration, data and evaluation unit, case and repeat, and scorer. For a training run this also covers the base checkpoint and its revision, the code revision, the training configuration and seed, the data version, and the checkpoints the run produced. Record values actually observed. Mark an unpinned alias as mutable, distinguish it from an exact revision, and leave an unavailable revision unknown rather than fabricating one.

Keep historical attempts, including incomplete, failed, and excluded work, with their reasons, raw-output lineage, denominators, and conditions under the project's retention and access rules. Preservation is not indefinite permission to retain private raw content. Do not overwrite an earlier score when rescoring. Create or request the project's linked derived result so the new scorer version and input lineage point back to the original raw attempt while permitted earlier records remain inspectable. Mark expired or unavailable evidence and its effect on verification honestly; do not silently delete records or recreate missing evidence. Read [attempts, results, and rescoring](references/attempts-and-result-lineage.md) when reconstructing provenance, judging sufficiency, or choosing among resume, rescore, and rerun.

Do not infer that gold labels were inaccessible or leakage-free from a record's appearance. Check the project's stated separation and access boundaries before making a comparability claim.

## Move only authorized ready work

When execution is requested, first re-anchor to the latest approved priorities, including any user change made while work was already running. Before claiming or dispatching a ready item, check its current prerequisites, configured target and resource limits, budget, and project-defined ownership mechanism. Use an existing claim, lease, reservation, or verified owner to prevent duplicate workers. For simple serial work, a verified single current owner is sufficient; do not require a bespoke lease system. If a small durable task record is needed and the operation authorizes it, create it through the project's normal practice rather than making a parallel registry.

An unrelated failure should not stall independent approved work. Preserve the failed attempt, isolate its cause, route its blocker to the responsible source, and continue other ready items only within the authorization and limits above. Bound non-idempotent actions. After a repeated deterministic failure, stop retrying and report the smallest missing input, correction, or authority that would change the outcome.

Use the following decision rules rather than treating every unfinished item alike:

- **Resume** an existing attempt only when current evidence supports that it remains the correct owned execution and its inputs, configuration, and limits still match the approved campaign.
- **Rescore** only when sufficient raw output and required input lineage exist, the intended data and label boundary are correct, and the requested scorer is authorized. Preserve the earlier result as described above.
- **Rerun** only when the raw output is absent or unusable under the project's rules, or the approved campaign explicitly requires a new execution. First rule out an existing live attempt and confirm the new work remains inside the approved scope.

For training and ablation runs the same rules apply to their own objects. Resuming continues an owned run from a checkpoint only when its saved state supports continuation; what a checkpoint supports (optimizer, scheduler, RNG, and data-progress state) is a single-run question answered with ml-experiment's training and recovery guidance. Re-evaluating a saved checkpoint under an authorized evaluation is the rescore case: it creates a linked derived result and leaves the training attempt as it was. Retraining is the rerun case, justified only when no usable checkpoint exists or the approved sweep calls for a fresh run, such as an added seed.

Read [operational modes](references/operational-modes.md) before taking an action when authority, recovery, queue ownership, or monitoring behavior is ambiguous.

## Monitor through a real runtime mechanism

For an approved monitoring request, state what counts as a meaningful update and the user-facing terminal condition. If the request is to continue until completion, use the current harness's supported native wait with fresh project-state reads, or an existing project scheduler or runtime observation route, until that condition is reached. A project-specific scheduler is not required when the harness can sustain observation. Use a bounded period only when the request, runtime, or authority gives a real bound; do not silently shorten a sustain request. Do not infer progress from idle compute alone.

If no supported sustained-observation mechanism exists, state the real runtime or authority blocker, make any safe immediate observation that remains in scope, and say that no background monitor continues after the current work ends. Do not promise that monitoring persists unless the runtime actually provides it. When execution is also authorized, re-check priorities before new dispatch; cancel or stop only specifically authorized, identified jobs.

## Report a decision-ready operational picture

Use the project's native report or record format when it has one; otherwise write concise prose rather than imposing a fixed table. Include:

- what actually finished, remains active or pending, failed, is blocked, or was excluded, with reasons and evidence;
- which comparisons are validated and comparable, their denominator and conditions, and what prevents that claim for the rest;
- the authoritative sources consulted, unresolved contradictions, and active job handles or equivalent live references that the intended audience may receive;
- the next approved action, or the smallest missing input or authority that blocks it.

Label the evidence boundary when it matters: a hypothetical plan, source location, or synthetic local fixture is not real execution; real execution is not automatically a validated result. Preserve uncertainty instead of smoothing it into progress language.

Keep operational preservation separate from document selection. Retain required provenance in the campaign's records; include it in a reader-facing report when it affects interpretation, reproduction, audit, or action. Active handles, failures, denominators, and unresolved state remain visible when the operator needs them. Routine report-build receipts need not accompany the result.

## Compose and finish

Read [synthetic maintainer review cases](references/synthetic-maintainer-review-cases.md) only when maintaining or auditing this skill. They are illustrative review material, not exercised behavior.

Use a separate orchestration, handoff, or shared-document capability only when the task calls for it. This skill remains useful with one worker and does not make delegation, a particular harness, or a new scheduler a prerequisite.

Finish a status or diagnosis request when the evidence-backed state and remaining uncertainty are clear. Finish an authorized execution or monitoring request at its stated terminal condition, with durable project records and a truthful handoff for anything still active or blocked.
