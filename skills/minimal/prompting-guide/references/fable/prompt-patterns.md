# Claude Fable Prompt Patterns

Patterns for Claude Fable 5 and Claude Fable 5.1. Clauses marked *5.1* address behaviors that changed in Fable 5.1; they are harmless on Fable 5.

Blocks followed by a "Quoted verbatim from Anthropic" line reproduce Anthropic's published wording exactly so it can be pasted unchanged. That quoted text remains Anthropic's and is not covered by this repository's MIT license. The other blocks are this pack's own templates.

## Contents

- Prompt contract
- Intent and action
- Scope and authority
- Progress and long runs
- Tool-call batching and append-only history
- Tools and subagents
- Memory, compaction, and context
- Output and readability
- Search, edits, and long outputs
- Runtime controls
- Migration and evaluation
- Failure diagnosis

## Prompt Contract

Start with:

```text
Purpose: [larger task, audience, and why this work matters]
Goal: [user-visible outcome]
Done: [observable completion conditions]
Context: [relevant evidence and inputs]
Authority: [allowed work, excluded work, pause conditions]
Tools and state: [non-obvious routing, delegation, memory]
Output: [artifact or answer shape]
Validation and stop: [checks, fallbacks, finish condition]
```

Keep each section at the right altitude. Fable generally needs the governing decision rule, not every behavioral variant the rule implies.

## Intent and Action

Give the reason:

```text
This work supports [larger objective] for [audience]. They need [what the output enables]. With that in mind, [request].
```

Prevent overplanning:

```text
When you have enough information to act, act. Do not re-derive established facts, reopen settled decisions, or narrate options you will not pursue. When a choice is needed, make a recommendation and state what evidence would change it.
```

Autonomous completion clause. Anthropic's Fable 5.1 wording; the first paragraph carries most of the effect if length must be limited:

```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not.

Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.

Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide.

Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Use the autonomous clause only for workflows where the user will not be present to answer mid-run. It can make the model less likely to ask about genuinely ambiguous requests, so check that trade-off. If the product needs specific confirmations, list them in a sentence after the opening. Interactive sessions can use a lighter pause rule.

## Scope and Authority

Assessment boundary:

```text
When the user asks a question, describes a problem, or requests diagnosis, the deliverable is the assessment. Report findings and stop. Implement a change only when the request authorizes it.
```

Scope boundary for high effort:

```text
Do not add features, refactor, or introduce abstractions beyond the task. Choose the simplest complete change for current requirements. Validate at user input, external APIs, and other real system boundaries; do not add defensive machinery for impossible internal states.
```

Deliverable scope, paired with the autonomous clause for unattended runs:

```text
The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it. Read ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. If you see a real problem with the task as specified, say so in a sentence or two and keep building under stated assumptions; if the user hears the concern and reaffirms, that is their decision, so deliver the full request.

If a question comes up partway, first do everything that doesn't depend on the answer; then state the assumption you made, or — when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a turn that also delivers that progress. If one part turns out to be blocked, complete every other part in full and say exactly what you left out and why — the whole task is the deliverable, and scaling it down is the user's call, not yours. A step you have decided on is something to run, not to announce: describing the next step and ending the turn leaves it undone until the user replies.

Keep changes to what the request needs. Something else you notice worth doing — cleanup or documentation the task didn't call for, a change to a file the task didn't require — is a suggestion to make at the end, not a change to make; actions clearly beyond what the ask implies, and risky or destructive ones, still need the user's go-ahead.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Changes and tests (*5.1*). Cuts unrequested additions and committed test files with no measured change in task success:

```text
If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well. Verify your work however you like; scratch scripts and quick checks need not be kept. Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files. This is about extras only: implement every behavior the task asks for, completely.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Pause rule:

```text
Pause when an action lacks required authorization, scope materially changes, or a needed decision belongs to the user. Preserve an existing grant for the same action and target; continue independent authorized work while awaiting missing input.
```

## Progress and Long Runs

Evidence rule:

```text
Before reporting progress, audit each claim against a tool result or named artifact from this run. State failed, skipped, and unverified checks plainly. Report verified completion without hedging.
```

Progress updates (*5.1*). Fable 5.1 narrates less during long tool-calling turns, and its between-call notes arrive as progress-update `thinking` blocks that are empty under the default `display: "omitted"`. Do these in order: set `thinking.display` to `"updates"` (beta) or `"summarized"` and render non-empty thinking blocks as status lines; delete prompt lines such as "hold all findings for the final response"; then, only if the product still needs more, add:

```text
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

If the UI collapses or hides tool output, tell the model each turn (turn-scoped system message), or it may run commands to "show" output the user never sees:

```text
Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

The harness should provide long timeouts, streaming, asynchronous monitoring, and resumability. Do not solve runtime timeouts with more prompt text.

If exact user-facing content must arrive without ending the turn, define a dedicated tool with a single message field. Pair it with:

```text
Use the send-to-user tool for partial deliverables, direct replies, or progress facts the user must receive verbatim. Do not use it for narration or reasoning.
```

## Tool-Call Batching and Append-Only History

Batching nudge (*5.1*). In coding and computer-use loops where the next independent calls are implied rather than named, Fable 5.1 may issue one tool call per turn. Append this after each batch of tool results:

```text
First privately list what you need next; then request every item that doesn't depend on another's result in this one response.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Deliver it as a turn-scoped system message (`role: "system"`, `clear_at: "next_user_message"`, beta) so the model reads only the newest copy; without the beta, put it in a text block after the `tool_result` blocks in the same user message. Append a fresh copy each turn and leave earlier copies untouched.

Append-only history is a harness rule, not a prompt clause. Send each assistant turn back exactly as returned, thinking blocks included. Do not inject and later remove reminders, summarize older turns in place, or rewrite `system` or `tools` mid-session: those edits restart the prompt cache and, on Fable 5.1, invalidate every later thinking block (a 400 `bound to a different conversation` for accounts created on or after 2026-08-31, or dropped blocks with `prefix_mismatch_behavior: "drop_block"`). Use mid-conversation system messages for instruction and tool changes and server-side compaction or context editing for trimming. To find edits a harness already makes, run a session with `drop_block` and log `input_transformations`.

## Tools and Subagents

Tool descriptions should make triggers and boundaries clear without aggressive "always use" language. Include decisive return fields and error behavior. Fable 5.1 does not support forced `tool_choice` (`any` or a named tool); say in the prompt when a tool applies and rely on `strict: true` or structured outputs for schema-valid arguments.

Delegation clause:

```text
Delegate independent subtasks and continue non-overlapping work while they run. Give each subagent a bounded question, evidence requirement, and stop condition. Intervene when a subagent lacks context or leaves scope. Synthesize results before acting; do not concatenate reports.
```

Non-blocking subagents (*5.1*). Have the tool that starts a subagent return immediately, deliver each result to the lead in a later user message, and give the lead a separate wait tool. The model still often chooses to wait; the savings come from the runs where it carries on. Use a fresh-context verifier for consequential long runs or subjective quality gates. Do not require a committee for routine bounded work.

## Memory, Compaction, and Context

Memory clause:

```text
Store one durable lesson or decision per record with a one-line summary. Record confirmed approaches and corrections with why they mattered. Do not copy facts already available in the repository or conversation. Update duplicates and delete records that become wrong.
```

Choose the context mechanism by purpose:

| Mechanism | Use for |
| --- | --- |
| Active context | Current task instructions and high-signal evidence |
| Compaction | In-session continuity after history grows |
| Tool-result clearing | Old results that can be fetched again |
| Memory or state artifact | Decisions and progress that must survive sessions |
| Subagent context | Isolated independent work or fresh verification |

Client-side compaction summary (*5.1*). Server-side compaction already does this. If you summarize on the client, replace the whole history with one summary message plus the new user turn, replay nothing else, and use this instruction. The last sentence matters when the summarization request still carries the conversation's tools:

```text
Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary such that this conversation will be continued by a new context window without needing to redo work or be reprovided with relevant constraints or context. Be sure to preserve: (1) any difficulties or problems that came up, and how they were handled or resolved; (2) any possibilities, options, or approaches that were raised, tried, or set aside, and why; (3) anything that was asked for, decided, agreed, ruled out, or established as a preference, constraint, or boundary — stated exactly; (4) exactly where things stand now — what has been covered, settled, or completed so far; (5) anything still open, unresolved, promised, or expected to happen next; (6) specific details that would be hard to reconstruct — names, numbers, dates, exact wording, links or references — kept exactly. Be complete on these even at the cost of length; keep everything else concise. Weight the two voices differently: keep what the user said, asked for, shared, or established carefully and close to their own words; your own explanations and reasoning can be condensed much further, to what they concluded or produced — as long as nothing in the six items above is dropped. Do not call any tools while writing this summary; respond with text only.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Cache reads on Fable 5.1 cost a quarter of the Fable 5 rate, so compacting early to save cost may no longer be the right trade; experiment with later compaction points.

For long documents, place source material before the query. Wrap multiple documents and metadata in clear XML tags such as `<documents>`, `<document>`, `<source>`, and `<document_content>`. Ask the model to cite or quote the relevant passages before synthesizing when traceability matters.

Use three to five diverse examples only when format, tone, or edge behavior needs demonstration. Wrap examples in `<examples>` and `<example>` tags.

## Output and Readability

Outcome-first final response:

```text
Open with what happened or what you found. Then provide the evidence that matters, the main caveat, and any action the user must take. Drop tool-loop shorthand and write for a reader who did not watch the work.
```

Keep complete sentences. Avoid dense arrow chains, unexplained internal labels, and references to analysis the user never saw. Choose clarity over compressed fragments.

Writing density (*5.1*). Where prose runs long and dense, define the anti-pattern in a user message (preferred) or the system prompt; the short form "Please remove all mannered prose." also tends to work:

```text
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Formatting in chat (*5.1*). Fable 5.1 uses bold, headers, and lists less than earlier models. Replace anti-formatting rules with a rule that says when structure is appropriate:

```text
Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Quoting retrieved sources (*5.1*). When summarizing documents, Fable 5.1 more often reproduces source passages without marking them as quotations. Add one complete `<example>` to the system prompt: the user's request, a response that conveys each source in the assistant's own indirect speech with at most one short marked quotation, and a `<rationale>` sentence explaining why it is correct. Write tool calls in the example as templated output such as `[web_search: ...]`, using your tool's name.

## Search, Edits, and Long Outputs

Search at low effort (*5.1*). At `low`, Fable 5.1 calls search and retrieval tools less often. Raise effort for the affected turns, per message where the API supports it, or add:

```text
When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. This holds even when you have some background on it — partial background is exactly what makes an out-of-date answer sound authoritative, so familiarity is not a reason to skip the search.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Targeted edits (*5.1*). Fable 5.1 rewrites whole files for small changes more often than Fable 5. Append to the system prompt or first user message:

```text
The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Long outputs at `xhigh` and `max` (*5.1*). Prefer `high` for long deliverables. If you run higher, set `max_tokens` for thinking plus reply and append this to the user message with the real value:

```text
Everything produced in one reply, including any reasoning or drafting done before the reply, counts toward a single limit of about [max_tokens] tokens. If that limit is reached before the reply is finished, the person receives a cut-off response and has to start over. Composing an entire output or deliverable in full as reasoning and then again as a reply would double the length of the turn without improving the result, so don't do that.

Instead, when the person has asked for a long or effort-intensive deliverable such as a multi-section document, a large table or dataset, or a complete code file, spend extra effort on understanding the request, checking the inputs the answer depends on, settling the structure and other difficult decisions, and otherwise using the reasoning space to reason and the output space to write an output. Usually it is not needed to draft an output multiple times.
```

Quoted verbatim from Anthropic's [Prompting Claude Fable 5.1][fable-5-1].

Safeguard false positives. Ask "Are there any bugs in this program?" rather than "Does this program compile without errors?"; give context or documentation for lesser-known languages; remove tools that return base64-encoded data into the model's context. Finding vulnerabilities in source code is permitted. A blocked request still returns `stop_reason: "refusal"`, so keep the fallback in place.

Vision. On dense charts and images, run the model as an agent with a container holding the raw files and basic image libraries, or at least a crop-and-zoom tool that returns an enlarged region.

## Runtime Controls

Keep these outside the prompt:

- Fable uses adaptive thinking at all times; `thinking: {"type": "disabled"}` and `budget_tokens` return 400.
- Effort levels are `low`, `medium`, `high` (default), `xhigh`, and `max`, set at `output_config.effort`. Level names do not map to the same thinking across models; re-run the sweep per model.
- Per-message effort (beta header `mid-conversation-output-config-2026-07-01`): an effort-only `role: "system"` message with empty content changes the level from the next user turn and keeps the prompt cache. Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, and Sonnet 5.5 (adaptive thinking only; with `thinking: {"type": "between_tools"}` a changed level returns 400); Fable 5 returns 400.
- `thinking.display`: `"omitted"` (default), `"summarized"`, or `"updates"` (beta header `thinking-display-updates-2026-08-18`) for progress notes without reasoning. Raw reasoning is never returned.
- Mid-conversation system messages add instructions or tool changes without editing `system` or `tools`; turn-scoped ones (`clear_at: "next_user_message"`, beta header `mid-conversation-system-clear-at-2026-08-21`) apply for one turn and cost no input tokens once cleared.
- Fable 5.1 binds thinking blocks to the conversation that produced them, and only Fable 5.1 and Mythos 5.1 read them; every other model, including the newer Opus 5.5, drops them, so a router or fallback from Fable 5.1 to Opus 5.5 loses that reasoning for the turn. Fable 5.1 does read earlier models' blocks and, on the Claude API, Opus 5.5's. Controls: beta header `thinking-binding-controls-2026-08-01`, `thinking.block_binding.prefix_mismatch_behavior`.
- Forced `tool_choice` (`any`, `tool`) returns 400 on Fable 5.1; `auto` and `none` are unchanged.
- Refusals arrive as `stop_reason: "refusal"` with `stop_details.category` (`cyber`, `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms`, or null). Server-side `fallbacks: "default"` (beta header `server-side-fallback-2026-07-01`) retries on the recommended model. Read the permitted targets from the model's `allowed_fallback_models` entry in the Models API (with the beta header) rather than hard-coding them; on 2026-10-07 the Fable 5.1 page still named Opus 4.8 and Opus 5, and Claude Code re-runs Fable 5.1, Fable 5, and Opus 5.5 refusals on the same two models (Opus 4.8 for cybersecurity, Opus 5 for biology). SDK middleware covers other platforms.
- Long tasks need appropriate client timeouts, streaming, and asynchronous UX. Compaction, context editing, memory, task budgets, and fallback are API or harness capabilities.
- In Claude Code, the `fable` alias selects Fable 5.1 from v2.1.257; session effort comes from `/effort`, `--effort`, or `CLAUDE_CODE_EFFORT_LEVEL`, and a skill or subagent's frontmatter `effort` overrides the session level.

Do not prompt the model to expose or reproduce reasoning. Ask for concise rationale, evidence, assumptions, and decision criteria.

## Migration and Evaluation

Run comparisons only when requested. For static prompt work, inspect the existing stack and available traces, deliver the patch, and state the behavior not exercised. Do not create a benchmark or invoke another model merely because the runtime is available.

Migration sequence from an older Claude model:

1. Run the current prompt and tools on representative cases.
2. Remove old response-length taxonomies, aggressive tool triggers, manual thinking budgets, repeated rules, and unnecessary orchestration.
3. Add only measured Fable-specific controls for scope, progress evidence, long-run communication, memory, or early stopping.
4. Set the intended effort and harness controls outside the prompt.
5. Rerun the same cases and compare outcomes, evidence, scope, latency, tokens, and cost.

Fable 5 to Fable 5.1, in addition to the model ID:

1. Remove forced `tool_choice`; move schema enforcement to strict tool use or structured outputs.
2. Keep the history append-only; move per-turn reminders to turn-scoped system messages and run the history-editing check.
3. Re-tune effort from `high`; consider per-message effort instead of one level all session.
4. Watch agent loops for one tool call per turn and add the batching nudge.
5. Delete anti-narration and anti-formatting lines before adding the progress-update and formatting clauses; re-run evals.

Include a difficult case near the top of the workload range. Simple tests alone can hide the model behaviors the prompt is meant to govern. Grade the environment or artifact when possible. A polished transcript is not proof that a code change, external action, or generated file is correct.

## Failure Diagnosis

| Symptom | Likely cause | First intervention |
| --- | --- | --- |
| Overplanning | Ambiguous goal or legacy exhaustive process | Add reason, outcome, and action threshold |
| Unrequested cleanup, extra tests | High effort without scope boundary | Add the scope clause and the changes-and-tests clause |
| False progress | No evidence contract | Require claims to cite current tool results |
| Text-only promise to act, permission asked for requested work | Long-run early stopping | Add the autonomous clause and deliverable scope |
| Silent minutes during tool runs (*5.1*) | `display: "omitted"` or anti-narration lines | Request progress updates in the runtime, delete suppressing lines, then add the update clause |
| One tool call per turn in a loop (*5.1*) | Implied rather than named reads | Add the batching nudge as a turn-scoped system message |
| 400 `bound to a different conversation` (*5.1*) | Harness edits earlier turns | Make history append-only; use turn-scoped and mid-conversation system messages |
| Dense prose, missing structure (*5.1*) | Anti-formatting rules; default density | Add the formatting rule and the mannered-prose definition |
| Unmarked quotations in summaries (*5.1*) | Default summarization style | Add one complete example with rationale |
| Answers from memory at `low` (*5.1*) | Low effort lowers search triggering | Raise effort for those turns or add the verification clause |
| Whole-file rewrites (*5.1*) | Default edit style | Add the targeted-edit clause |
| Long wait or `max_tokens` at `xhigh`/`max` (*5.1*) | Deliverable drafted in thinking | Run at `high`, or size `max_tokens` and add the long-output note |
| Premature handoff | Exposed context countdown or anxiety | Hide countdown and use durable state |
| Excessive subagents, idle lead | Blanket delegation or blocking spawn tool | Delegate only independent bounded work; make spawn non-blocking |
| Dense final summary | Tool-loop language leaked to user output | Add reader re-grounding clause |
| Refusal after reasoning request | Reasoning-extraction instruction | Remove transcript request; use evidence and summaries |
| Refusal on benign coding work | Compile-check phrasing, unknown language, base64 tool output | Rephrase, add language context, remove base64 tools; keep fallback |
| Slow routine task | Effort too high or prompt too heavy | Lower effort and remove stale scaffolding |
| Cross-session drift | No durable state artifact | Pair compaction with maintained memory or handoff state |

[fable-5-1]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
