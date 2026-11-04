# Execute Mode

Advance the objective using the plan's current understanding and next decision. Execute, inspect the result, and choose the next bounded action within established scope. A plan guides the work; it does not make a contradicted assumption true.

## Re-enter from actual state

Scope the run from the request: a named task narrows the run to that task and its genuine prerequisites, a plan path covers the plan's current work, and "continue the plan" without a path resumes the most recent plan under `.plans/` with unfinished current work, asking which one when several fit.

Read the goal, existing grants, current work, sources, and project context. Inspect relevant actual state before acting: results, data and model versions, changed files, or active jobs.

Older plans may use `stage`, `needs`, `owns`, `avoid`, `acceptance`, `check`, `Planned against`, `Reconsider when`, Results, and Run log, and a header that names `gigio-execute-plan`. Read their meaning and preserve completed records: honor an `avoid` or ownership line as a write boundary, re-check a `Planned against` anchor that the current action depends on, read `acceptance` and `check` as the plan's assessment and completion threshold, and read `Reconsider when` as the stop-and-ask condition. Use known dependencies for current execution; do not insist on rewriting a usable old plan or treating speculative later stages as settled research decisions.

Resolve discrepancies that can be checked. Preserve unrelated work. An unavailable checker remains unverified, and a missing input blocks the work that needs it. Do not substitute another dataset, model, or environment and present it as the named one. Before retrying a remote or long-running action, establish whether the original is still active.

## Execute and interpret

Perform the next analysis, experiment, review, or implementation. Use the relevant specialist's method: research, evaluation, and experiment skills for research questions, data, runs, and measurement (`evaluation-operations` owns the run state of a multi-run evaluation campaign), and development skills for implementation and harness tools (`coding-standards` for writing, structuring, and verifying code). Load only the capability needed now. Do not prohibit a worker from reading relevant skills or sources.

Check the actual result rather than accepting a worker's completion claim. Record the finding and what it changes. A negative result, an excluded explanation, or a supported statement that available data cannot distinguish alternatives can complete an investigation. An input-format check does not establish that a model evaluation ran, and an inconclusive comparison does not establish equivalence.

Within the same question and permitted resources, perform quick diagnostics or follow-up work without asking for every small choice. Update the current plan and project understanding so the next session inherits the revised state. Keep earlier results and the reason for a changed action.

## Keep implementation notes

During implementation, keep implementation notes in the plan or in a file beside it that the plan links, with a Deviations list. When an edge case forces leaving the plan, such as an input the plan did not anticipate, an interface that differs from what the plan assumed, or a check that cannot run as written, choose the conservative option and continue: the one easiest to reverse, touching least outside the task, and staying inside existing grants. Record each deviation with what the plan said, what was done instead, and why, so the next session and a later review see it without reconstructing it from the diff.

A deviation that changes direction, meaning the goal, question, success criterion, or consequential scope, is not a note: raise it with the user as the next section describes and pause the work that depends on it.

## Raise direction problems promptly

Bring a proposed change of research question, project goal, success criterion, or consequential scope to the user when the finding appears, before acting on it. Present the observation, why the old approach is doubtful, the proposed next work, and the expected cost or duration. Pause the work that depends on the doubtful premise; continue independent authorized work if useful. Do not defer a known direction problem to a final review while consuming resources on its invalid premise, and do not edit the user's stated goal or limits yourself.

Ask before a long new activity, such as two to three days or more, unless the user already authorized that activity and its bounds. Also respect narrower project limits and material cost, shared-resource, or external-effect constraints. A fast action is not automatically authorized if it changes those boundaries.

## Coordinate workers

An explicit user choice about delegation governs, including whether to delegate, how many workers, and the budget. Without one, the lead decides. Once the direction is settled and the questions that would change the work are answered, dispatch the ready independent tasks through `orchestrate-subagents`, which carries the dispatch defaults and their limits. Keep work sequential where each step depends on the previous result. Give workers the objective, sources, task boundaries, relevant skills, expected result, existing grants, and the decisions already made, so they finish without routing routine questions back. Name project and plan paths without copying whole records. Delegation adds no authority beyond the existing grants.

Partition shared writes and live-job ownership before parallel work. Read-only workers can examine the same sources. Do not duplicate a running experiment because its original session lost a handle. The lead integrates findings and owns project digest and plan updates unless another owner is established.

Use `git-worktree-setup` for requested implementation isolation and `small-model-handoff`, when installed, to bound a weaker executor; otherwise use the selected harness's real runtime mechanisms. Their absence is not a reason to invent a framework, and a supported direct route is fine when sufficient.

## Verify progress and continue

Match verification to the claim. Use a run of the real entry point on fixed input, plus the tests the project keeps, for implemented behavior, actual logs and outputs for run completion, source inspection for a review finding, and justified comparison for an interpretation. A read-only review needs no changed source file. A command exit code is not a substitute for interpreting its output.

Keep execution failures distinct from unwelcome research results. Retry only after a concrete correction or new information makes it useful, within remaining limits. Repeated identical failure calls for diagnosis or stopping, not spending the budget unchanged. Do not change the question merely to obtain a passing result.

Update existing records proportionally: what happened, what was learned, the sources needed to check it, and the next decision. Keep raw attempts and operational state in their established records rather than duplicating them in the plan.

Continue in-scope work until the plan's `Done when` threshold is shown by its evidence, or until a decision point, limit, or real blocker is reached. When the plan's `Stop and ask when` condition occurs, stop the work that depends on it and bring the observation to the user. A round whose plan states only an activity, such as "keep investigating", has no end the executor can recognize: propose a threshold to the user before spending beyond a quick check. When requested, use review mode for review and the appropriate publication skill, such as `commit-and-push` or `draft-pr`, for delivery. Do not commit, publish, install, or start another workstream simply because a round finished.

Finish with the result, its support, any material unresolved question, the deviations recorded this round, and the next useful action. The whole project is not complete merely because the current round is complete.

## Source note

Keeping implementation notes that record deviations from the plan while the work runs is adapted from Thariq Shihipar, ["A field guide to Claude Fable 5: Finding your unknowns"](https://claude.com/resources/articles/a-field-guide-to-claude-fable-finding-your-unknowns) (Anthropic, 2026-07-06). The practice is rewritten here, not copied.
