# Fable 5 and Fable 5.1 Prompting Guide

Build prompts that give Claude Fable a clear reason, outcome, boundary, and evidence bar while leaving room for strong long-horizon judgment. Remove legacy micromanagement before adding model-specific scaffolding. Fable 5 prompts carry over to Fable 5.1 unchanged; the shifts section below covers the behaviors that moved.

## Approach

Name the exact model (Fable 5 or 5.1) and the runtime. Define the observable outcome, why it matters, the authority boundary, and the evidence of completion. For an existing prompt, separate an observed failure in traces from a suspected prompt cause. Remove repeated rules, exhaustive behavior lists, stale thinking-budget instructions, aggressive tool triggers, anti-formatting and hold-your-findings rules written for chattier models, and scaffolding for behavior Fable already performs. Then add brief clauses only for real gaps, from [prompt patterns](prompt-patterns.md) or [the prompt template](../../assets/fable/prompt.template.md). Put effort, thinking display, timeouts, fallback, compaction, history handling, and tool setup in the API or harness, not the prompt. Ask for evidence and decisions, never a transcript of private reasoning.

## Core Prompt Shape

For complex work, keep these sections short and omit empty ones:

1. Role and larger purpose.
2. Goal and definition of done.
3. Context, inputs, and accepted evidence.
4. Scope, authority, and pause conditions.
5. Tools, delegation, memory, and progress behavior.
6. Output and user communication.
7. Validation, fallback, and stop rules.

Give the reason behind important instructions. Fable uses intent to resolve ambiguity and connect work across long-running streams.

## Model-Specific Rules

### Use Strong Instruction Following

Prefer one clear instruction over a taxonomy of prohibited variants. If a prompt lists every way to be verbose, pause, or overbuild, replace it with the desired behavior and completion bar. Remove contradictions before adding emphasis.

When enough information exists, instruct the model to act. Ask for a recommendation when judgment is needed, not an exhaustive survey of options that will not be pursued.

Contract steps, not cognition steps. Use numbered steps only when order or completeness is part of the task's correctness: prerequisite retrieval, approval boundaries, required artifact stages, validation, or an externally auditable pipeline. Otherwise state the outcome, invariants, and stopping condition and let the model choose the path. Fable follows short instructions strongly — a misdesigned procedure is followed just as faithfully, so every step must earn its place.

### Bound Scope at High Effort

Fable can explore and improve beyond the request, especially at higher effort. State what the task authorizes and what it does not. Distinguish assessment from implementation and reversible in-scope work from destructive, irreversible, or scope-expanding action.

Do not require permission for every routine step. Pause only for real user input, material scope changes, or consequential actions that need confirmation.

### Ground Progress and Completion

For long autonomous work, require every progress claim to point to a current tool result or named artifact. Failed, skipped, and unverified checks must remain visible. A plan, a changed file, or the model's confidence is not completion evidence.

### Design Long Runs as a Harness Problem

Hard tasks may take minutes or hours. Configure timeouts, streaming, asynchronous status, and resumability in the harness. Give the prompt sparse checkpoint rules instead of forcing narration after every tool call. Keep the conversation history append-only: per-turn reminders and mid-run instruction or tool changes go in turn-scoped or mid-conversation system messages, never in edits to earlier turns.

When the user must receive exact content mid-run, provide a dedicated send-to-user tool and tell the model when to call it. Do not route narration or reasoning through that tool.

### Delegate Independent Work

Fable can manage sustained subagent collaboration. Delegate when work is independent, context isolation helps, a specialist tool matters, or a fresh verifier reduces anchoring. Prefer asynchronous coordination: a spawning tool that returns immediately, results delivered in a later user message, and a separate wait tool, so the lead keeps working.

Do not turn every task into a committee. Keep dependent judgment with the lead and synthesize results before acting.

### Use Durable Memory Selectively

Give long-running agents a place to store corrections, confirmed approaches, decisions, and state that must survive sessions. Keep one lesson per record with a short summary. Do not duplicate the repository or chat history, and update or delete stale memory.

Use compaction for in-session continuity and memory or state artifacts for facts that must survive summarization or a fresh session. If the harness compacts on the client, tell the model what the summary must preserve.

### Keep Final Communication Reader-Facing

After a long run, write the final response as a re-grounding for someone who did not see the tool loop. Lead with the outcome, reintroduce necessary vocabulary, use complete sentences, and explain the one or two user actions that remain.

### Keep Thinking Controls in the Runtime

Fable always uses adaptive thinking. Do not set manual extended-thinking budgets or ask the prompt to reveal its reasoning. Use the effort parameter for depth and the thinking display setting for summaries or progress updates.

Request concise rationale, assumptions, evidence, and decisions. Instructions to echo or transcribe reasoning trigger the reasoning-extraction refusal category.

### Handle Refusals as API State

The application must handle `stop_reason: "refusal"`, including fallback and user-facing behavior; server-side default fallback retries on the model Anthropic recommends for the category. Do not prompt around safeguards. Three habits reduce false positives on benign coding work: ask whether a program has bugs rather than whether it compiles, give context for lesser-known languages, and keep base64-encoded tool output out of context.

## Fable 5.1 Shifts

Each shift has a clause in [prompt patterns](prompt-patterns.md). Delete conflicting legacy rules before adding one.

- **Fewer progress updates during tool runs.** First make the runtime request them (`thinking.display: "updates"`), then remove hold-your-findings lines, then ask for an opening line, brief updates, and a standalone recap.
- **One tool call per turn** in loops where the next reads are implied. Send the one-sentence batching nudge fresh each turn as a turn-scoped system message.
- **Thinking blocks bound to the conversation.** Editing earlier turns now invalidates them as well as the cache; the append-only rule above is mandatory.
- **Less formatting, denser prose.** Replace anti-formatting rules with a rule that says when structure helps; define mannered prose rather than asking for brevity.
- **Unrequested fixes and extra tests** on open-ended implementation. Say what to leave out: pre-existing bugs are follow-ups, tests match what the task and repository call for.
- **Unmarked quotations** in summaries. Add one complete example with a rationale.
- **Fewer searches at `low` effort.** Raise effort for those turns or add the name-verification clause.
- **Whole-file rewrites** for small edits. Add the targeted-edit clause.
- **Long thinking before long deliverables at `xhigh` and `max`.** Prefer `high`; otherwise size `max_tokens` and add the long-output note.
- **Forced tool use rejected.** Say in the prompt when a tool applies; use strict tool use or structured outputs for schema-valid JSON.

## Effort and Evaluation

Create evaluation fixtures or run additional model sessions only on request. A static review may deliver revised wording with an untested-behavior caveat; it does not need a new benchmark to finish.

Start at `high`, the default. Step up to `xhigh` or `max` only for capability-sensitive long-horizon work, and down to `medium` or `low` for routine or interactive work once evals show quality holds. Effort names do not mean the same thinking across models, so re-run the sweep when moving from Fable 5 to Fable 5.1. Fable 5.1 at `medium` roughly matches Fable 5 at lower cost. Compare its cost per task against the current Opus model before relying on a cross-family claim. Fable 5.1 also accepts per-message effort changes that keep the prompt cache, so a loop can run hard steps higher and routine steps lower.

Use two to five positive cases and one or two near misses. Include at least one long-run case when the prompt governs tools, state, or subagents. Grade the final environment or artifact, not only the transcript.

## Output Contract

For a new prompt, return the final prompt plus the runtime settings and tools it assumes. For a review, lead with the most consequential issue and provide a minimal revision. For a migration, separate removed legacy scaffolding, added Fable-specific clauses, and API or harness changes; for Fable 5 to Fable 5.1, also list the forced-tool-use, thinking-block binding, and history-editing checks. State when live evals were unavailable.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| [prompt-patterns.md](prompt-patterns.md) | Writing or revising a non-trivial Fable prompt | Prompt clauses, long-run scaffolding, Fable 5.1 shifts, runtime controls, migration, and failure patterns |
| [prompt.template.md](../../assets/fable/prompt.template.md) | Starting a new complex prompt | Compact fill-in prompt skeleton |

## Gotchas

- Do not preserve old scaffolding merely because it once improved a weaker model, including anti-formatting and hold-your-findings rules written for chattier models.
- Do not expose token countdowns unless the harness requires them; they can encourage premature wrap-up in very long sessions.
- Do not ask Fable to reproduce hidden reasoning or summarized thinking.
- Do not use manual `budget_tokens` or forced `tool_choice`, and do not copy an effort level across models unmeasured.
- Do not inject and delete per-turn text in earlier turns; use turn-scoped system messages.
- Do not treat a text-only promise to act as completed work.
- Do not overdelegate tightly coupled work or block on each subagent immediately.
- Do not use memory as a second copy of the repository or conversation.
- Do not hide a refusal or fallback that changes confidence or reproducibility.
