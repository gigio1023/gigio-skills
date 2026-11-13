# Goal Mode Prompts

Read this with the target family's guide when the user wants a Codex Goal mode or Claude Code `/goal` prompt explained, drafted, reviewed, translated, set, or handed to the other harness. It is not for ordinary objectives, acceptance criteria, task prompts, implementation plans, or autonomous work without explicit Goal mode intent.

Turn intent into a goal prompt that the named harness can pursue and judge honestly. Support advice, drafting, review, cross-harness translation, and explicit activation without forcing one workflow on every request.

## Quick Path

1. Identify the requested mode: explain, draft, review, translate, or activate. Do not turn a request for guidance or copy into a running goal.
2. Identify the target harness. Read [codex-goals.md](codex-goals.md) for Codex and [claude-goals.md](claude-goals.md) for Claude Code. When translating, read both.
3. Inspect safely available context before asking for facts: repository instructions, plans, tests, scripts, issues, logs, or the supplied draft. Ask one concise question only when the missing answer changes the outcome or completion evidence materially. Continue drafting the settled parts while that answer is pending; do not invent a verification command or activate an unresolved goal to avoid asking.
4. Decide whether goal mode fits. Use it for substantial work with a closed, verifiable end state. Recommend a normal prompt, plan, automation, or human review gate when that is the better control surface.
5. Write the smallest contract that preserves the outcome, evidence, material boundaries, and real stop conditions. Keep a direct goal payload below the target's documented limit. For domain-specific proof or a file-backed contract, read [goal-patterns.md](goal-patterns.md).
6. Audit the draft for false completion, unverified assumptions, impossible checks, hidden side effects, and target-specific evaluator blind spots.
7. Return the requested artifact. Activate it only when the user explicitly asked to set or start the goal and the current session exposes an agent-callable goal-state capability.

## Goal Fit

A goal fits substantial multi-turn work with a closed, observable finish line: a bounded migration, failing-to-passing bug fix, benchmark target, finite review queue, or decision-ready research artifact.

Use another surface when:

- one direct turn or a small edit is enough;
- the route must be approved before changes begin, which calls for a plan;
- work repeats on a schedule or reacts indefinitely, which calls for an automation or hook;
- no rubric, reference, or human gate can make subjective completion honest;
- unrelated backlog items have no single terminal outcome.

Goal mode governs continuation. It does not expand permissions, authorize external or destructive actions, replace project instructions, or turn missing access into permission.

## Shared Goal Contract

Use only the parts that change the run. Do not force these into fixed headings when one compact paragraph is clearer.

- **Outcome:** one concrete state, artifact, behavior, or decision that will be true at completion.
- **Context:** the files, sources, reproduction, plan, issue, or environment that materially changes the work or should be inspected first.
- **Verification:** the check and expected signal that prove completion. Name exact commands only after confirming they exist or deriving them from the project. Require the agent to report the evidence it actually observed.
- **Constraints:** compatibility, preservation, safety, authority, quality, and side-effect limits that prevent a plausible wrong result.
- **Scope:** include or exclude paths, systems, records, or deliverables only when ambiguity would widen the task.
- **Stop or escalation:** name missing access, failed prerequisites, conflicts, unsafe operations, or user decisions that should stop continuation. Add a time, turn, or cost bound only when the user wants one or runaway risk makes a proposed bound worth confirming.

## Modes

### Explain

Answer the user's question and make the target-specific behavior explicit. If both harnesses matter, compare only differences that change how the goal should be written or operated.

### Draft

Return a ready-to-use goal payload for the named target plus assumptions or a short rationale only when useful. A user asking for copy has not asked to start the goal.

### Review

Lead with the highest-impact defects, then provide a revised payload or minimal patch. Preserve working constraints and user intent. Check target syntax, payload length, evidence visibility, scope, authority, and completion honesty.

### Translate

Preserve the outcome and evidence while adapting evaluator semantics:

- Codex to Claude Code: make every completion claim demonstrable in the conversation because Claude Code's goal evaluator does not inspect tools or files itself. Add an optional run bound only when wanted.
- Claude Code to Codex: retain transcript-friendly evidence, then express the objective as outcome, constraints, and verification. Keep runtime budget controls separate unless the user explicitly requested them.

Translation is not literal rewriting. Remove source-harness commands, status verbs, metadata, or assumptions that the target does not share.

### Activate

Activation changes the current session's goal state and may immediately start work. Do it only on an explicit set, start, create, or run request and only through an agent-callable goal-state capability in that same session. Claude Code's `/goal` is user-entered session input, so return a ready-to-submit command and say that the user must submit it. Do not start another CLI process or remote session to simulate activation.

1. Inspect the current goal state when the harness supports it.
2. Continue a matching active goal instead of creating a duplicate.
3. If an unfinished goal conflicts, explain the conflict and request a choice rather than replacing it silently.
4. Set the refined objective through the target's native capability. Include a token budget only when the user explicitly supplied one.
5. Follow the runtime's own rules for completion, blocking, pause, resume, and clearing. Never claim completion without the evidence named in the goal.

If the current session cannot expose an agent-callable goal capability, return the copy-paste payload and a minimal handoff instruction.

## Output Contract

Match the response to the request:

- explanation: recommendation, target-specific reason, and a small example when it clarifies the rule;
- draft: one copy-paste payload, then material assumptions or caveats;
- review: findings first, followed by the corrected payload;
- translation: target payload plus the semantic changes that mattered;
- direct activation: the goal state changed, the objective used, and any immediate caveat or next action;
- activation handoff: the ready-to-submit command and the fact that the user must submit it in the target session.

When returning direct command text, count characters if it is near the target's limit. Do not say a goal was activated when only text was produced.

## Gotchas

- A referenced file is not automatically visible to a separate evaluator.
- "Work autonomously and never ask" can suppress necessary approval or blocker handling. Define the decisions the agent may make and the conditions that require escalation.
- Mandatory budgets, universal test bans, fixed check counts, and exhaustive templates create fake rigor when the task does not need them.
- Do not invent project commands, available tools, deployment targets, audience stakes, or production access to make a prompt look complete.
- The family guide owns general prompting for the target model; this reference owns goal-mode contracts and handoffs.
