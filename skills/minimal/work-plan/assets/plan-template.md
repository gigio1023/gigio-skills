# <project work>

> To execute or continue, use work-plan in execute mode on this file; to revise it, use work-plan in write mode. If the skill is unavailable, follow the objective, current understanding, authority, and next action below.

## Goal and basis

State the user's goal and relevant constraints in recognizable wording. Link the maintained intent records this work answers to. Identify any material agent proposal that has not been accepted.

## Current understanding

What sources or results establish, what remains uncertain, and which interpretations would change the next action. Link existing records instead of duplicating them.

## Next decision or result

What this round should let us decide, understand, produce, or rule out. Explain how an inconclusive or negative result would affect the next step.

## Current work

- Action: <the next bounded analysis, experiment, review, or implementation>
- Inputs: <sources, data, model, environment, and versions that matter>
- Assessment: <observation, comparison, judgment, or command that establishes the result>
- Done when: <checkable threshold that ends this round and the evidence that shows it; never an activity such as "keep investigating">
- Limits: <time, cost, targets, data access, and other existing grants>
- Ownership: <writes, output locations, shared resources, or live jobs, only when parallel work or shared resources make it matter>
- Stop and ask when: <result, contradiction, failed check, repeated failure, or limit that pauses the work for the user's decision>

Add stable task IDs and actual dependencies when several actions are independently useful. Parallel actions must not make conflicting writes or duplicate live jobs. Do not fill future stages with speculative tasks.

## Authority and pause points

Carry actions already authorized. Identify direction changes and resource expansion needing a user decision; a finding that challenges direction goes to the user when it appears. Fast checks within the current question and limits can proceed; long new work such as a two-to-three-day run needs confirmation unless already authorized.

## Sources and continuation

Name canonical results, research index, run registry, and active jobs needed for this work. Identify source state whose change would invalidate the current action.

First action for a fresh session: <one concrete action>.

## Results and next decision

Fill during execution: what was actually done, what the result supports, what it does not settle when relevant, and the next selected action or proposal. Link underlying output or inspected sources. Code changes and successful commands are not required for a valid finding.

## Implementation notes

For implementation work; omit otherwise. Deviations: each departure an edge case forced, with what the plan said, what was done instead, and why it was the conservative choice. A departure that changes direction goes to the user instead of this list. A separate notes file beside the plan works too when this section links it.

## Changes to the plan

Keep a concise history of consequential changes: previous action or assumption, observed reason, new action, and any user decision. Keep upcoming work current; preserve earlier results.
