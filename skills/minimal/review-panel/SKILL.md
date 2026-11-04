---
name: review-panel
description: >
  Review an artifact with reviewers whose contexts are separate from the authoring session, by default two from different model families such as Claude Fable and GPT-6 Astra, then judge every finding against the artifact by its evidence, never by how many reviewers agree, apply the valid ones, and re-check. Covers code and diffs, research and system designs, design documents, evaluations and results, documents and PR bodies, plans, skills, and operating processes. Also checks review comments from people before acting on them. Use for "review this with Fable and Codex", "get a second opinion on this design", "cross-check this PR", "리뷰해줘", "교차 검토", or "Fable이랑 Astra로 리뷰". NOT for posting inline comments on a GitHub PR (pr-review-comment, when installed), a launch verdict on a built evaluation or result (evaluation-audit, which this skill can use as criteria), attacking one idea (idea-critique), or a quick self-check that needs no separate reviewer.
---

# Review Panel

Have an artifact reviewed by reviewers who did not write it and do not share the authoring session's context, then decide what each finding is worth by checking it in the artifact. The result is a judgment table that marks every material finding valid, partially valid, or rejected with the evidence checked, the valid fixes applied within the granted scope, the relevant checks re-run, and the questions that need the user.

Findings are judged by evidence in the artifact, never by how many reviewers raised them. Reviewers who agree may share one premise: the same packet, the same stale document, the same misleading comment, or similar training. A single reviewer's finding whose evidence holds outranks two that agree without it, and agreement neither raises a finding's rank nor replaces checking it.

## Scope

The skill covers code and diffs, research and system designs, design documents, evaluations and results, documents such as PR bodies and Notion pages, plans and work against intent, skills and skill packs, and operating processes or systems. Route nearby requests elsewhere:

- Posting validated findings as inline comments on a GitHub PR belongs to `pr-review-comment` when installed; it can take this skill's valid findings as its candidates.
- A launch, hold, or report verdict on a built evaluation, benchmark, judge, or result belongs to `evaluation-audit`. This skill can borrow its checks as review criteria; the verdict stays there.
- Attacking one stated idea or hunch belongs to `idea-critique`.
- A quick self-check that needs no separate reviewer needs no skill: check the work directly.

When a large artifact is split across many reviewers, `orchestrate-subagents` supplies dispatch and liveness mechanics. This skill owns the packet, the criteria, and the adjudication. Reviewers supply findings; the lead judges them.

## Choose the Reviewers

An explicit user choice of reviewers, models, or count governs. Without one:

- Use two reviewers from different model families when both are reachable, typically Claude Fable and GPT-6 Astra, so their blind spots are less likely to coincide.
- Run GPT-6 Astra through Codex with `codex-delegate` when it is installed and the user named Codex or asked for a cross-family review, in its read-only sandbox.
- Fill any other seat with a separate subagent of any trusted model. The session's own model is acceptable when the reviewer's context is clean: it receives the packet and the artifact, not the conversation.
- Choose each reviewer's model and effort with `model-routing` when installed, else with the user's routing policy or the harness defaults, and state the resolved settings.

If a requested family cannot be reached from this harness, say so and name the coverage lost; do not substitute another model silently. Independence is what the panel buys. A reviewer that saw the authoring conversation is not independent, and neither is a review the session performs itself. When no separate context can be started, say so, offer the review the session can give, and label it as not independent.

Every reviewer is read-only: no edits, no commits, no posting to a forge or tracker, no runs that change state or spend budget, and no network unless the user granted it for this review. A reviewer writes only the report path its packet names, if any. The packet and every file a reviewer reads go to that model's provider, so for an external provider include only what the user's data policy allows that provider to receive.

## Choose Criteria and Axes

Pick criteria by artifact type and borrow them from the skill that owns the artifact when it is installed: `coding-standards` for code, `design-doc` and `idea-critique` for designs, `evaluation-audit` for evaluations and results, `copydesk` and the publishing skill for documents, `work-plan` review mode for work against a plan, and `skill-builder` for skills. When the owning skill is absent, write the criteria into the packet directly. Quote or summarize the criteria that matter rather than only naming a skill, since a reviewer in another harness may not have it installed. Read [criteria by artifact](references/criteria-by-artifact.md) when writing the criteria section of a packet; it holds the per-artifact table, fallback criteria, and criteria for operating processes.

For code and designs, review two axes in separate contexts: fidelity, whether it does what was asked or designed, and standards, whether it meets the standards that apply. Kept apart, a reviewer who finds the code clean does not take that as evidence it is correct, and one who finds a gap against the request does not grade the style more harshly for it. Fidelity needs an intent source at a named revision: the request, issue, design document, or plan. Look for one before asking; if none exists, state the intent as the lead understands it and mark it in the packet as a hypothesis for the reviewers to test.

Axes and reviewers multiply. Four contexts, each family on each axis, give the strongest coverage; two contexts with one axis per family cost half and lose the cross-family check on each axis. Choose by the cost of a defect that slips through, and name the coverage chosen in the report. Other artifact types usually need one context per reviewer, unless they also have an intent source and a separate standard worth keeping apart.

Judge the cost of a slipped defect by asking whether a wrong version of this change would fail loudly where it is made or silently somewhere else. A loud, local defect, such as a crash, a type error, or a failing check at the changed line, shows itself on the next run, so the cheaper coverage is usually enough. A silent defect passes every check at the change site and surfaces later: a guard that still passes but no longer guards, an auth, money, or data boundary, a public interface or serialized format other code depends on, a reported number, or retry, timeout, ordering, and concurrency behavior that degrades without an error. Silent or unsure gets the full coverage, and the packet names the distant places where the failure would surface, such as the callers, the consumers of the format, or the metric pipeline, so reviewers read them as well as the diff. The same question sizes the review of a design or an evaluation, where most defects are silent until results arrive.

## Write the Packet

Write one packet per axis and send the same packet to each reviewer on that axis, so differences in findings come from the reviewers, not the packets. Start from [the packet template](assets/review-packet.template.md) when writing one. The packet states:

- What to review: paths, revision or commit, diff range, and what is out of scope.
- Why the artifact exists: its purpose, the owner's goals, and its reader or user.
- The axis and its criteria.
- Current rules that override older records, such as a newer user decision that supersedes a section of the design document, so reviewers do not flag compliance with the newer rule as a defect.
- Limits: read-only access, network, and time.
- The required response: findings ranked by impact, each with `path:line` evidence, why it matters, and a concrete fix; the parts checked and found sound; a short list of what the reviewer declined to judge, one line each with the reason, such as outside its criteria, needing access or a run it lacked, or outside what it can assess; and a verdict for the stated purpose.

Keep the lead's conclusions out of the packet. A suspicion the lead wants checked goes in only as a hypothesis to test, marked as one. Do not pass one reviewer's findings to another in the first round.

## Adjudicate

Verify each material finding in the artifact itself: open the cited location, read the governing rule or intent source, and run the cheap check that would show the problem, such as an entry point on fixed input. A reviewer's citation is a lead, not proof. Then mark the finding:

- **Valid:** the problem exists as described. Apply the proposed fix or a better one.
- **Partially valid:** the problem is real, but its cause, scope, or fix is wrong. Record what holds and what does not, and apply the corrected fix.
- **Rejected:** the problem does not exist at this revision, the cited location says otherwise, or the finding conflicts with a newer user decision or current rule, which wins. Record the reason and the evidence.

When settling a finding needs a measurement or access the review was not granted, neither apply nor reject it: list it as an open investigation item with the check that would settle it. A finding arguing that a current rule is itself wrong goes to the user as a question instead of being applied or dropped.

Read each reviewer's declined list as a coverage map: an item one reviewer declined and no other reviewer judged is a part of the artifact nobody reviewed. Cover it with a check of your own, another reviewer, or an open investigation item, and never read silence on it as approval.

Merge duplicates into one finding that lists every reviewer who raised it; its judgment comes from the check alone. Never group, rank, or weight findings by agreement; rank them by impact on the artifact's purpose. Keep rejected findings in the table with their reasons, so a later round does not reopen them without new evidence. Non-material items such as wording preferences may be applied when plainly right and in scope, or dropped with a one-line reason.

Judge a finding that asks for new tests against the project's test policy. This pack's default is no new tests: fixes are verified by running real entry points on fixed input, and learned or judged behavior through evaluation. When the team's documented policy or the reviewer calls for tests, or existing tests would be removed or changed, ask the user.

The judgment table has the columns ID, finding, raised by, evidence checked, judgment, and action, with longer reasoning in notes beside it. Read [the worked example](references/example.md) when the depth of the table or the line between partially valid and rejected is unclear.

## Apply and Re-check

Show the judgment table to the user before applying anything when the user asked to see it or when a fix is consequential: it changes behavior beyond the reviewed change, an interface, a design decision, or published text, or it would be hard to reverse. Otherwise apply the valid and partially valid fixes within the scope the user already granted for this artifact and re-run the checks that cover them, such as the entry points, validators, renders, or evaluation slices the findings touched. Ask the user's questions together and early, with the table: rules a finding disputes, test requests, and consequential fixes. A review-only request, or a review of someone else's artifact, returns the table and the proposed fixes without editing.

A second round earns its cost when the fixes changed structure or behavior broadly. Send a fresh context the original packet and the changed parts, or ask each original reviewer to check its own findings against the fix.

## Review Comments From People

Comments from a human reviewer on a PR, document, or design follow the same rule. Verify each one against the artifact before implementing it. When some comments are unclear, ask about them before implementing the related ones, since a partial reading can produce the wrong change. When a comment is wrong for this artifact, answer with the evidence: the location, the run output, or the rule it conflicts with. A comment that conflicts with an earlier decision of the user goes to the user. Reply by stating the fix or the evidence, without performative agreement. Posting replies or resolving threads on a forge or tracker is an external write and needs the user's approval.

## Report

Lead with what the review means for the artifact's next step. Then give the judgment table, the changes applied with their paths, the checks re-run with their results, the rejected findings with reasons, the open investigation items and questions for the user, and the panel as run: reviewers, models and effort, axes, the coverage chosen and why, access granted, declined items no reviewer judged and how they were covered, and any loss of independence or coverage.

## Sources

Running the fidelity axis and the standards axis as separate subagents is adapted from the `code-review` skill in [mattpocock/skills at 49dd158](https://github.com/mattpocock/skills/tree/49dd158/skills/engineering/code-review) (MIT License, Copyright (c) 2026 Matt Pocock), rewritten here and extended from code to designs and other artifacts. That skill's baseline of code smells appears here only as an optional heuristic through `coding-standards`. Verifying review feedback against the codebase before implementing it, clarifying unclear items before implementing related ones, and pushing back with technical evidence instead of performative agreement are adapted from the `receiving-code-review` skill in [obra/superpowers](https://github.com/obra/superpowers) version 6.3.0 (MIT License, Copyright (c) 2025 Jesse Vincent), rewritten here and applied to panel findings as well as comments from people. Asking each reviewer for what it declined to judge is adapted from the code reviewer prompt of the `requesting-code-review` skill in [obra/superpowers at 22f0b46](https://github.com/obra/superpowers/tree/22f0b46/skills/requesting-code-review) (MIT License, Copyright (c) 2025 Jesse Vincent). Sizing a review by whether a defect would fail loudly at the change site or silently elsewhere is adapted from the review depth gate of the `ce-code-review` skill in [EveryInc/compound-engineering-plugin at a3bcedf](https://github.com/EveryInc/compound-engineering-plugin/tree/a3bcedf/skills/ce-code-review) (MIT License, Copyright (c) 2025 Every). Treating a weakened bar in the diff as a finding is adapted from the `constraint-driven-development` skill in [addyosmani/agent-skills at 301b02b](https://github.com/addyosmani/agent-skills/tree/301b02b/skills/constraint-driven-development) (MIT License, Copyright (c) 2025 Addy Osmani). All three are rewritten here.

## References

| File | Read it when |
| --- | --- |
| [references/criteria-by-artifact.md](references/criteria-by-artifact.md) | Writing the criteria section of a packet |
| [assets/review-packet.template.md](assets/review-packet.template.md) | Writing a review packet |
| [references/example.md](references/example.md) | The judgment table's depth or the line between partially valid and rejected is unclear |
