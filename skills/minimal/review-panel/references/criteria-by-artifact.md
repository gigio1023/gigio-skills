# Criteria by Artifact

Read this when writing the criteria section of a review packet. Each row names the skill that owns the artifact. When that skill is installed, take its criteria and quote or summarize the ones that matter in the packet, because a reviewer in another harness may not have the skill. When it is absent, use the fallback criteria below and state them in the packet directly. A project's own instructions, style guides, and lint configuration come before any skill's defaults.

| Artifact | Owning skill, when installed | Fidelity against | Standards |
| --- | --- | --- | --- |
| Code or diff | `coding-standards` | Request, issue, or design document | Project conventions, then the skill |
| Research or system design | `design-doc`, `idea-critique` | Chosen concept and goals | Design sections, boundary, bets |
| Evaluation or result | `evaluation-audit` | The decision it informs | Readiness checks |
| Document, PR body, Notion page | `copydesk` and the publishing skill | Purpose and reader | Prose and structure |
| Plan or work against intent | `work-plan` review mode | User goal and plan | Requested, done, learned |
| Skill or skill pack | `skill-builder` | The task the skill serves | Contract, discovery, validation |
| Operating process or system | none | Stated goal | Failure modes, ownership, invariants |

A mixed artifact, such as a PR that changes code and its documentation, takes each part's criteria; the axes still get one packet each.

## Code and diffs

- **Fidelity:** the change does what the request, issue, or design document at the named revision asks, no more and no less. Callers and contracts it touches still hold. Unrequested expansion is a finding.
- **Standards:** the repository's instructions and lint configuration first, then `coding-standards` when installed and covering the language. Without it: names that state a responsibility, data flow and side effects visible from the caller, errors handled at trust and I/O boundaries, no dead or speculative code, types at public interfaces, and each new dependency justified.
- **Security-sensitive handling:** secrets kept out of code and logs, input validated where it crosses a trust boundary, and permission checks where state changes.
- **Weakened bar:** a change that lowers a check instead of meeting it is a finding by itself, reported with its location and no further proof of harm. Look in the diff against its base for a new lint or type suppression (`# noqa`, `# type: ignore`, `@ts-ignore`, `eslint-disable`, `# pragma: no cover`, a new ignore rule in the linter, type checker, or secret-scan baseline); a test skipped, marked expected to fail, or deleted; an assertion removed or loosened, such as an exact value replaced by a range, an equality by a non-null check, or a specific exception by a broad one; a threshold lowered, such as coverage, a score floor, a tolerance, a timeout, or a severity level; and a check made non-blocking or dropped from CI. A stated reason that holds makes it partially valid rather than rejected, since the user still decides whether the bar moves. Under this pack's test policy, removing or changing an existing test needs the user's approval, so a deleted test stays a finding even when the test was weak. A tightened bar needs no finding.
- **Tests:** judged against the project's policy. Under this pack's default, the absence of new tests is not a finding by itself; a reviewer's request for tests becomes a question for the user.
- **Code smells:** an optional heuristic. A smell named by `coding-standards` or the project's style guide prompts a closer look at that spot; it is not a checklist whose entries are findings without evidence of harm.

## Research and system designs

- **Fidelity:** the design serves the chosen concept and stated goals, and each goal has a completion condition a reviewer can check.
- **Design sections, from `design-doc`:** every learned or judging component sits behind a fixed interface with its adapters listed; the verification split puts each component on the tested or the evaluated side; each decision has a status, an evidence kind, and a reversal condition; unmeasured bets sit in an experiment queue; undecided items are phrased as open questions.
- **Threat model or operating boundary:** what an adversary or untrusted input controls, what identity and state stay fixed, which objective categories are in scope, and the assumptions the protection depends on, written in methodology terms with no attack procedures.
- **Load-bearing bets, in the manner of `idea-critique`:** the strongest case for each bet, the strongest attack on it, and the measurement whose outcome would decide between them. A bet the design rests on with no deciding measurement is a finding.

## Evaluations and results

- Use the checks of `evaluation-audit`: oracle and null passes, the identity of the served model, data and labels, grader errors, sampled trajectories, and denominators. Reviewers report findings; the launch, hold, or report verdict stays with that skill.
- Without it, state those checks directly, and add whether compared conditions had the same budget and whether uncertainty is reported at the independent unit.

## Documents, PR bodies, and Notion pages

- **Fidelity:** the text serves its reader and purpose, and each claim matches its source.
- **Standards:** `copydesk` for prose, and the publishing skill for structure: `draft-pr` for PR bodies, `write-notion` for Notion pages, `write-issue` for issues. Without them: the opening carries the finding or decision, numbers keep their conditions, status words agree across headings, body, and figures, terms stay consistent, and padding is cut.

## Plans and work against intent

- Use the review mode of `work-plan`: compare what was requested, done, and learned; flag unsupported claims, unrequested expansion, and unconfirmed proposals presented as decisions; send direction findings to the user.

## Skills and skill packs

- Use `skill-builder`: the description leads with concrete tasks and natural phrases, NOT clauses name real neighbors, decision rules replace fixed procedures where order is not fragile, references load on a named condition, prerequisites have a fallback, the validator passes, and a public package carries no private or work-derived material.
- For a pack, also check overlaps and conflicts between skills, and that each shared rule has one home.

## Operating processes and systems

No pack skill owns these, so state the criteria in the packet:

- **Stated goal:** each step serves it, and something observable shows whether it is met.
- **Failure modes:** for each dependency, what happens when it is slow, unavailable, or wrong; how the failure is noticed; and how the process recovers.
- **Ownership:** each step, alert, and handoff has an owner role.
- **What must not break:** invariants, data that must not be lost, and limits on cost and access, and whether the change preserves them.
- **Drift:** how the process notices that it no longer matches the system it operates.
