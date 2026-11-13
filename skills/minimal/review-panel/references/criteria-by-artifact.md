# Criteria by Artifact

Criteria to quote or summarize into a review packet; a reviewer in another harness may not have the same skills installed. A project's own instructions, style guides, and lint configuration come first. A mixed artifact, such as a PR that changes code and its documentation, takes each part's criteria.

## Code and diffs

- **Fidelity:** the change does what the request, issue, or design document at the named revision asks, no more and no less. Callers and contracts it touches still hold. Unrequested expansion is a finding.
- **Standards:** the repository's instructions and lint configuration first. Otherwise: names that state a responsibility, data flow and side effects visible from the caller, errors handled at trust and I/O boundaries, no dead or speculative code, types at public interfaces, and each new dependency justified.
- **Security-sensitive handling:** secrets kept out of code and logs, input validated where it crosses a trust boundary, and permission checks where state changes.
- **Weakened bar:** a change that lowers a check instead of meeting it is a finding by itself. Look in the diff for a new lint or type suppression (`# noqa`, `# type: ignore`, `@ts-ignore`, `eslint-disable`, `# pragma: no cover`, a new ignore rule or secret-scan baseline entry); a test skipped, marked expected to fail, or deleted; an assertion loosened, such as an exact value replaced by a range or a specific exception by a broad one; a lowered threshold (coverage, score floor, tolerance, timeout, severity); and a check made non-blocking or dropped from CI. A stated reason that holds makes it partially valid, since the user still decides whether the bar moves.
- **Tests:** judged against the project's own test policy; a reviewer's request for new tests where the policy does not call for them is a question for the user.
- **Code smells:** a smell prompts a closer look at that spot; it is not a finding without evidence of harm.

## Research and system designs

- **Fidelity:** the design serves the chosen concept and stated goals, and each goal has a completion condition a reviewer can check.
- **Structure:** learned or judging components sit behind fixed interfaces; it is clear which parts are tested and which are evaluated; decisions carry their evidence and a reversal condition; unmeasured bets and open questions are named as such.
- **Threat model or operating boundary:** what an adversary or untrusted input controls, what stays fixed, and the assumptions the protection depends on.
- **Load-bearing bets:** the strongest case for each bet, the strongest attack, and the measurement that would decide between them. A bet with no deciding measurement is a finding.

## Evaluations and results

- Oracle and null passes, the identity of the served model, data and labels, grader errors, sampled trajectories, and denominators. Whether compared conditions had the same budget, and whether uncertainty is reported at the independent unit.

## Documents, PR bodies, and Notion pages

- **Fidelity:** the text serves its reader and purpose, and each claim matches its source.
- **Standards:** the opening carries the finding or decision, numbers keep their conditions, status words agree across headings, body, and figures, terms stay consistent, and padding is cut.

## Plans and work against intent

- Compare what was requested, done, and learned; flag unsupported claims, unrequested expansion, and proposals presented as decisions; send direction findings to the user.

## Skills and skill packs

- The description says what the skill does and when, with natural trigger phrases; decision rules replace fixed procedures where order is not fragile; references load on a named condition; the validator passes; a public package carries no private or work-derived material.
- For a pack, also check overlaps and conflicts between skills, and that each shared rule has one home.

## Operating processes and systems

- **Stated goal:** each step serves it, and something observable shows whether it is met.
- **Failure modes:** for each dependency, what happens when it is slow, unavailable, or wrong; how the failure is noticed; and how the process recovers.
- **Ownership:** each step, alert, and handoff has an owner role.
- **What must not break:** invariants, data that must not be lost, and limits on cost and access.
- **Drift:** how the process notices that it no longer matches the system it operates.
