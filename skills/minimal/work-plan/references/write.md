# Write Mode

Create a plan a later session can use to make the next useful advance. Keep the overall direction visible; detail the next analysis, experiment, review, or implementation whose result changes the next decision. Do not manufacture a complete sequence when later steps depend on findings.

## Establish the basis

Read the intent the work answers to: whatever the user or project already maintains, such as instruction files, a design or research document, a brief, a parent plan, or a project record. Read current user instructions and relevant results. Identify the next decision or desired result and why it matters.

Recover facts before asking questions. Settle the questions whose answers would change the plan before detailing work, including consequential unknowns nobody has noticed yet, and ask them together rather than one at a time. Use `find-unknowns` when the search for what neither side has noticed needs its own pass, and `interview` only when the user wants sustained questioning. Open empirical questions can be the work itself.

Preserve accepted goals and limits in recognizable user wording. Label a planner's new proposal only where it could change intent or authority, and keep the label until the user accepts or changes it. An unanswered question is not approval, but sufficient existing direction does not need another confirmation.

When the work spans repositories or sessions and no maintained document carries the project's lasting context, read [project-context.md](project-context.md) before writing the plan.

## Detail the next work

Use [the plan template](../assets/plan-template.md) under the user's chosen root, defaulting to `.plans/<topic>.md`. The root can be a research workspace, a vault, or several repositories. Follow its established storage and visibility policy; do not silently add a Git exclusion or a competing tracking system.

Bound the current round by the next decision. State the question, relevant known facts, important assumptions, selected action, expected information, how to assess the result, when the round is done, and when to stop and ask. Later possibilities can remain short alternatives or open questions rather than scheduled tasks.

A result can justify proceeding, reject an explanation, reveal insufficient information, or require a change in direction. Make that distinction visible before execution, so a negative or inconclusive result is recognizable as an outcome rather than a defect. Do not demand a predicted finding, code output, or pass/fail command when the work calls for judgment.

Write the completion threshold as a condition someone other than the executor can check, together with the evidence that shows it: a named command and its pass condition, a metric with its threshold, measurement method, and number of runs, a stated set of cases or sources examined, or an artifact the user approves. For research and judgment work, the threshold is the decision the round must enable and the evidence standard that settles it, which a negative or inconclusive result can meet; it never names the finding in advance. Reject activity goals such as "keep investigating", "make progress on X", or "improve the pipeline", because no observation ends them. Rewrite one into the outcome it serves when the plan's context makes the rewrite safe, and ask when the rewrite could change what the user wants.

Also write the condition that makes the executor stop and ask instead of continuing: a result that contradicts a premise of the round, a check that cannot run as written, a limit that will be exceeded, the same failure repeating after correction, or a choice that would change scope or authority. Name the concrete case for this round rather than repeating the general rules every mode keeps.

For implementation, dependencies and checks may be known in advance. For research, record dependencies that are real now. Use task IDs when actions need separate ownership, and preserve existing IDs. Stage numbers are optional scheduling aids.

For delivery work, the default ordering is unchanged: first the work whose result informs the next decision. When integration risk dominates, because the open question is whether the parts connect at all rather than how well any one performs, one option is to run early the simplest path that crosses every seam end to end, sometimes called a walking skeleton, with stand-ins where real parts are not ready: a rule in place of a model, for example, so that the request, the module call, the verdict, the response, and the metric each run once. Later rounds replace the stand-ins one at a time and rerun the same path. Offer it beside other orderings, such as building the riskiest component first or measuring a candidate model before wiring it in; it is never a required first round.

Before simultaneous execution, partition shared writes: name the paths, output locations, or shared resources each parallel action writes, and which live jobs it owns. Do this for the work about to run in parallel, not for every future finding. A read-only comparison can name its sources and result location; it needs no artificial edit. A run names its inputs, resource limits, and existing output records. Do not copy code bodies, raw logs, or an entire literature collection into a plan.

## Carry authority and continuity

Record existing grants for targets, data, compute, budget, publication, and consequential actions. Fast follow-up checks within the same question and permitted resources may be chosen during execution. Ask before a direction change or a long new activity, such as work expected to take two to three days or more, unless that exact activity was already authorized. Short duration alone does not authorize paid services, private-data transfer, or a new external write. Apply tighter project limits when present, and consider cost and disruption as well as elapsed time.

Link the source records and versions whose change would invalidate this round: a commit, a dataset revision, a model checkpoint, a document version, or observed live state may be appropriate. Do not require hashes or rerunning every historical check when they cannot affect the current action.

Use existing experiment and research records. The plan coordinates work and decisions; it is not the only permissible place for state.

## Deliver

Provide the saved path, the first useful action, and any material proposed intent awaiting a decision. A planning-only request ends at the plan. If execution was requested too, continue in execute mode under the same grant.

When revising a plan, preserve earlier results and the reason for a changed action while updating upcoming work. The next session should see the current plan immediately without reconstructing it from an append-only history.

## Source note

The measurable completion threshold with its evidence, the stop-and-ask condition, and the rejection of activity goals are adapted from the `define-goal` skill in [openai/skills at 49f948f](https://github.com/openai/skills/tree/49f948f/skills/.curated/define-goal) (Apache License 2.0), rewritten here for plan files and for research rounds whose result is not known in advance.
