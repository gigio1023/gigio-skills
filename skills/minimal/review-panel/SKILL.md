---
name: review-panel
description: >
  Have an artifact reviewed by reviewers whose context is separate from the
  authoring session, then judge every finding against the artifact by its
  evidence rather than by how many reviewers agree, apply the valid ones, and
  re-check. Also checks review comments from people. Use for "cross-check
  this PR with another model", "get a second opinion on this design", or
  "교차 검토".
disable-model-invocation: true
---

# Review Panel

Have an artifact reviewed by reviewers who did not write it and do not share the authoring session's context, then decide what each finding is worth by checking it in the artifact.

Findings are judged by evidence in the artifact, never by how many reviewers raised them. Reviewers who agree may share one premise: the same packet, the same stale document, the same misleading comment, or similar training. A single reviewer's finding whose evidence holds outranks two that agree without it.

## Reviewers

An explicit user choice of reviewers, models, or count governs. Otherwise the lead picks the reviewers and their number from what is reachable and what a missed defect would cost. Reviewers from different model families are less likely to share blind spots; a separate subagent on the session's own model is also acceptable when it receives only the packet and the artifact, not the conversation. Say which reviewers ran.

Independence is what the panel buys. A reviewer that saw the authoring conversation is not independent, and neither is a review the session performs itself; if no separate context can be started, say so and label the review as not independent. If a requested model cannot be reached, say so rather than substituting silently.

Reviewers are read-only: no edits, commits, posts to a forge or tracker, state-changing or budget-spending runs, or network unless granted for this review. A reviewer writes only the report path its packet names. The packet and the files a reviewer reads go to that model's provider, so for an external provider include only what the user's data policy allows.

## Sizing and Axes

Size the review by asking whether a wrong version of this change would fail loudly where it is made or silently somewhere else. A crash, type error, or failing check at the changed line shows itself on the next run, so light coverage usually suffices. A silent defect passes every check at the change site and surfaces later: a guard that still passes but no longer guards, an auth, money, or data boundary, a public interface or serialized format other code depends on, a reported number, or retry, timeout, ordering, and concurrency behavior. Give silent or uncertain changes more coverage, and have the packet name where the failure would surface (callers, consumers of a format, the metric pipeline) so reviewers read those too. Designs and evaluations are mostly silent until results arrive.

For code and designs it often helps to review two axes in separate contexts: fidelity (does it do what the request, issue, or design asked) and standards (does it meet the applicable rules). Kept apart, a reviewer who finds the code clean does not take that as evidence it is correct. Fidelity needs an intent source at a named revision; if none exists, state the intent as the lead understands it and mark it as a hypothesis to test. [Criteria by artifact](references/criteria-by-artifact.md) has criteria to quote into a packet.

## Packet

Send the same packet to every reviewer on an axis, so differences come from the reviewers. [The packet template](assets/review-packet.template.md) is a starting point. A packet says what to review (paths, revision or diff range, out of scope), why the artifact exists and for whom, the criteria, current rules that override older records (so compliance with a newer decision is not flagged), the limits, and the response wanted: findings ranked by impact with `path:line` evidence and a concrete fix, parts checked and found sound, a short list of what the reviewer declined to judge and why, and a verdict for the stated purpose.

Keep the lead's conclusions out of the packet; a suspicion goes in only as a hypothesis to test. Do not pass one reviewer's findings to another in the first round.

## Adjudication

Verify each material finding in the artifact: open the cited location, read the governing rule or intent source, and run the cheap check that would show the problem. A reviewer's citation is a lead, not proof.

- **Valid:** the problem exists as described. Apply the proposed fix or a better one.
- **Partially valid:** the problem is real but its cause, scope, or fix is wrong. Record what holds and apply the corrected fix.
- **Rejected:** the problem does not exist at this revision, the cited location says otherwise, or it conflicts with a newer user decision. Record the reason and evidence.

A finding that needs a measurement or access the review lacked stays open with the check that would settle it. A finding arguing that a current rule is wrong goes to the user as a question.

Read each reviewer's declined list as a coverage map: an item one reviewer declined and no other judged is a part nobody reviewed. Cover it with a check of your own, another reviewer, or an open item, and never read silence as approval.

Merge duplicates into one finding listing every reviewer who raised it; its judgment comes from the check alone. Rank by impact on the artifact's purpose, not by agreement. Keep rejected findings with their reasons so a later round does not reopen them without new evidence. A judgment table (finding, raised by, evidence checked, judgment, action) works well; [the worked example](references/example.md) shows its depth and the line between partially valid and rejected.

## Apply and Re-check

Show the judgment before applying when the user asked to see it or a fix is consequential: it changes behavior beyond the reviewed change, an interface, a design decision, or published text, or is hard to reverse. Otherwise apply valid fixes within the scope already granted and re-run the checks that cover them. A review-only request, or a review of someone else's artifact, returns the judgment and proposed fixes without editing. A second round is worth it when fixes changed structure or behavior broadly.

## Review Comments From People

Comments from a human reviewer follow the same rule: verify each against the artifact before implementing it. Ask about unclear comments before implementing related ones. When a comment is wrong for this artifact, answer with the evidence. A comment that conflicts with an earlier user decision goes to the user. Reply with the fix or the evidence, without performative agreement. Posting replies or resolving threads on a forge or tracker needs the user's approval.

## Report

Lead with what the review means for the artifact's next step, then the judgments, the changes applied, the checks re-run, open items and questions for the user, and the panel as run, including declined items no reviewer judged and any loss of independence.

Adapted sources and licenses are listed in [sources](references/sources.md).
