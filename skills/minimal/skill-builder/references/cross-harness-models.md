# Model Differences For Portable Skills

Use this when one package must serve GPT-6 (Astra and Sol 6.1), Claude Fable, and Claude Opus, and its instructions need writing or simplifying. It is a dated maintenance reference, not a reason to put model names into every domain skill. For instructions aimed at one model family, apply the `prompting-guide` skill when installed. For a model change in a single-model package, [frontier audit](frontier-model-audit.md) owns the procedure.

## Contents

- Sources
- Shared behavior
- Differences to preserve
- Portable prompt pattern
- Tools and parallel work
- Long runs and communication
- Requested comparisons

## Sources

Fable snapshot reviewed 2026-07-10 and extended to Fable 5.1 on 2026-09-23. GPT-6 reviewed 2026-09-05 for Astra and on 2026-09-23 for Sol, when this pack stopped using GPT-5.6. Opus 5.5 addition reviewed 2026-09-23. Sol 6.1 runtime identity, effort, and tool requirements were checked on 2026-10-06; the older prompting observations remain Astra-derived.

- OpenAI, [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md). Its prompting observations come from Astra and are offered as a starting point for the whole family, including Sol; its limitations and migration sections give the Sol runtime differences.
- OpenAI, [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) and [current GPT-6 migration guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.1-sol): Sol 6.1 rejects `none` and `minimal`, defaults to `medium` in the API, and requires Responses for tool calling. Legacy `gpt-6-sol` is a separate model contract.
- Anthropic, [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) and [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).
- Anthropic, [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5), which builds on [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5).
- Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Skill format and harness sources (OpenAI Build skills, Anthropic skill authoring guidance, Claude Code skills) are recorded in the [source guide](skill-docs.md). Refresh these sources before relying on current model, effort, API, metadata, or harness availability details.

## Shared Behavior

Both model families reward a smaller, clearer contract:

- Start from the smallest prompt that preserves the task and passes applicable checks. State the result and completion bar instead of narrating ordinary reasoning or implementation steps.
- Keep important constraints, authority, evidence, output, and stop conditions. Delete repeated rules, generic competence reminders, obsolete weaker-model compensation, irrelevant tools, routine process narration, and examples that do not change behavior.
- Match degrees of freedom to risk: contextual heuristics for open work, parameterized patterns for preferred approaches, and deterministic scripts or exact gates for fragile work. A bare `MUST` without a mechanism is rarely useful.
- Define the difference between assessment and mutation once. Both families can take useful initiative, but can also over-act when boundaries are implicit.
- Ground progress and completion claims in current tool results or named artifacts, and report failures faithfully. Visible updates belong at real phase changes, not after routine calls.
- Request evidence, assumptions, decisions, and concise rationale. Never request hidden reasoning, chain-of-thought, scratchpads, or reflection transcripts.

The portable writing rule is:

> Lead with the outcome. Keep required facts, decisions, artifacts, evidence, caveats, and next actions. Remove introductions, repetition, generic reassurance, and options not pursued first.

This counters GPT-6's tendency toward detailed, formatted responses and Fable's tendency at high effort to elaborate or survey unused alternatives, without cutting required substance.

## Differences To Preserve

| Topic | GPT-6 (Astra-derived guidance; verify on Sol 6.1) | Claude Fable | Portable treatment |
| --- | --- | --- | --- |
| Prompt size | Follows longer instructions, but conflicting guidance in skills or `AGENTS.md` can stop work early | Brief steering can replace enumerated behavior; older prescriptive skills can degrade output | Start small, resolve conflicts at their source, retain only evaluated task deltas |
| Long work | Stays coherent on long tasks but asks for clarification more often | Designed for long-horizon autonomy; can run longer and occasionally stop early or overplan; 5.1 sends fewer progress updates during tool runs | Define done state, authorized actions, grounded phase updates, and genuine blockers; configure runtime outside the domain skill |
| Brevity | Tends toward detailed, formatted responses with recurring phrases | Outcome-first selective brevity works; 5.1 writes denser prose with less formatting | State what must remain, the prose style, and what to trim |
| Tools | Async tool calling, Programmatic Tool Calling, and mid-turn steering are runtime features | Strong direct tool use and asynchronous subagent coordination | Route by task shape; do not require a provider-specific mechanism |
| Parallelism | May delegate less often than the workflow wants | Fable dispatches and sustains subagents readily | Make independence the rule, say when to delegate, and keep a sequential fallback |
| Verification | Tests thoroughly, sometimes more broadly than a small change needs | 5.1 can add unrequested fixes and extra tests on open-ended implementation | Tie checks to the changed behavior and required repository checks |
| Effort | Preserve supported effort; the minimum for Astra and Sol 6.1 is `low`; legacy Sol also accepts `none` | Effort is a major latency/cost control and high can over-explore routine work | Record effort in evaluations; do not hard-code it in portable domain skills |
| Prompt structure | Short, task-first skill descriptions and conditional reading | XML tags help complex mixed-content API prompts | Use plain Markdown for normal skills; reserve XML for adapter templates with a measured need |
| Memory | Persisted reasoning and harness memory require freshness discipline | Explicit lesson memory can improve long-running agents | Store durable state outside upgradeable skill folders and only when the workflow needs it |

Claude Opus 5.5 shares Fable 5.1's API behavior (thinking always on, forced tool use rejected, append-only history) but differs in ways a portable skill should not paper over. Its default effort is `medium`, and at a given level it thinks more per turn than Opus 5. On long unattended runs it can end a turn with a progress update, so the done state must be checkable rather than inferred from a text-only turn. It delegates readily and verifies its own work unprompted, so delegation and verification instructions should state criteria rather than encourage more. The Opus guide in the `prompting-guide` skill, when installed, covers Opus-targeted prompts.

Do not average away these differences. The shared core states intent and contract; a model or harness adapter selects runtime controls. The `model-routing` skill, when installed, owns the current GPT task assignments. That routing policy does not change the Anthropic model choices or prove a model capability limit.

## Portable Prompt Pattern

Use only the fields that change behavior:

```text
Outcome: <user-visible artifact or decision>

Context: <why this matters and source material that changes the work>

Success: <required facts, files, states, evidence, or validation>

Authority: <assessment-only vs local change; actions still requiring approval>

Constraints: <invariants, preservation rules, exclusions, safety boundaries>

Routing: <capability decision rules, prerequisites, parallel/sequential rule>

Output: <reader-facing shape and facts that must remain>

Stop/fallback: <done condition, bounded retries, real blocker>
```

For a simple task, collapse this to a paragraph and a short checklist. A fixed template that adds empty headings is legacy scaffolding, not portability.

Personality belongs here only when tone is part of the product or artifact. Otherwise let the harness's global style own it. Explain intent when it affects judgment, especially for long work, but do not add a generic role paragraph to every skill.

## Tools And Parallel Work

Tool descriptions or skill instructions should communicate:

- the capability and prerequisite;
- when the route is appropriate;
- important return fields and error states;
- allowed side effects;
- retry and stop behavior when non-obvious.

Prefer direct calls when one result is small, approval-sensitive, citation-bearing, native-artifact producing, or semantically changes the next action. Prefer a deterministic script or programmatic reduction for large structured filtering, joining, ranking, aggregation, or repeated validation. Prefer parallel workers for independent work, isolated context, specialized access, or fresh review.

Parallel calls alone do not justify a programmatic layer. Parallel workers alone do not justify coordination overhead. The core workflow must still work in one context when the harness lacks either mechanism.

## Long Runs And Communication

For multi-step tasks, allow a short user-visible preamble and sparse updates at major phase changes. Each progress claim must point to a current result or named artifact. Do not request narration of every tool call.

The final response re-grounds the reader: outcome first, decisive evidence, material caveat, and any action needed from them. Avoid private shorthand or terms invented during the work unless they are reintroduced.

Provider-specific send-to-user tools and Codex progress surfaces are harness features. A portable skill specifies the communication outcome, not either mechanism.

## Requested Comparisons

A cross-model comparison runs only on request. Its sequence and matrix are in the [review gate](cross-harness-review.md#evaluation-matrix). Without a request, deliver the static patch and report the untested model behavior.
