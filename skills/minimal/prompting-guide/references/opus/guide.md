# Claude Opus 5.5 Prompting Guide

Produce a usable prompt or instruction change for Claude Opus 5.5. Prompts written for Opus 5 carry over and remain the baseline; this package adds what changed in 5.5 and removes what 5.5 no longer needs. It applies Anthropic's [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) together with [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5), which the 5.5 page names as its starting point. Loading it does not select a model, set effort, or change any runtime.

## Put Each Fix In Its Layer

Much of the Opus 5.5 guidance changes a setting, the agent loop, or a tool rather than prompt text. Decide the layer before writing a clause:

- **Prompt text:** scope, completion, stop policy, communication cadence, exploration, and the instructions to remove.
- **Request settings:** `effort`, `max_tokens`, `thinking.display`, per-message effort, and refusal fallback. Prose cannot stand in for them; a line asking for less thinking works less reliably than lowering effort.
- **Agent loop:** what counts as the end of a task, continuation messages, silence reminders, time signals, and how instructions or tools change without editing earlier turns.
- **Tools:** a send-to-user tool for exact mid-turn content, cropping or a container for dense images, and strict tool use for schema-valid calls.

Then identify who owns each layer in the target host. An API integration owns all four. Instruction files loaded by Claude Code or the Agent SDK own the text and a few settings; the harness already runs the loop, keeps history append-only, and marks pasted text, so restating those in CLAUDE.md or a skill adds context without changing behavior. A chat product owns its system prompt and request settings. Read [host notes](host-notes.md) before editing instructions that Claude Code or another agent harness will load.

## Remove Before Adding

Most Opus 5.5 guidance deletes. Before adding a clause, look for these in the existing stack and remove or re-test them:

- Requests to think carefully or step by step, especially in chat system prompts. Effort governs thinking, and removing the line makes replies start sooner.
- Requests to write reasoning into the response. They can draw a `reasoning_extraction` refusal; read summarized thinking instead.
- Rules telling the model not to think, and the thinking-disabled mitigation written for Opus 5. Thinking is always on in 5.5.
- Explicit verification steps, re-check reminders, and subagents assigned to verify the lead's own work. Opus 5 verifies its work unprompted and these instructions add cost without quality; the 5.5 pages do not reverse that.
- Review prompts that ask only for high-severity or conservative findings. The model reports less; ask for every finding and filter in a separate pass.
- Visual-input workarounds built for earlier models, which 5.5 may no longer need, and general style bans such as "avoid a generic look", which should name the specific patterns instead.
- Reliance on forced `tool_choice`, which 5.5 rejects. State in the prompt when a tool applies.

Keep domain knowledge, exact syntax, permission boundaries, and required output structures.

## Choose The Relevant Material

| Task | Read |
| --- | --- |
| Fix an observed behavior | The matching section of [symptom patterns](symptom-patterns.md) |
| Write a new prompt | The [prompt template](../../assets/opus/prompt.template.md), then only the patterns the workload needs |
| Migrate from Opus 5 or an earlier model | [Runtime and migration](runtime-and-migration.md), then the removal list above |
| Edit CLAUDE.md, a skill, or a subagent definition that runs on Opus | [Host notes](host-notes.md) |

## Make The Change

Establish the target model, its effort, the host, and whether a person is present while it runs; the unattended stop policy and the chat follow-up clause both depend on that last fact. Read available traces or failing outputs, and separate the observed behavior from the suspected prompt cause.

Add a clause only for an observed symptom or a behavior the workload will certainly hit, such as an unattended multi-part run. Each pattern names its costs and placement; honor both. A clause that must be present from the session's first request, such as the stop policy or a send-to-user tool, cannot be patched in mid-conversation without invalidating earlier thinking blocks.

Treat effort as a setting to measure, not a prompt problem. The 5.5 default is `medium` where Opus 5's is `high`; level names do not transfer between models, and 5.5 thinks more per turn than Opus 5 at the same level, most of all at `xhigh` and `max`.

## Deliver

- **New prompt:** the prompt, the settings and tools it assumes, and the symptom each model-specific clause addresses.
- **Review:** the most consequential issue first, with a minimal revision.
- **Migration:** removed legacy instructions, added 5.5 clauses, and request or loop changes as three separate lists.

State what was checked statically and which behavior is untested. Model trials and eval suites run only on request. When requested, run the same cases at the intended effort, include a long unattended case if the prompt governs one, grade the final artifact rather than the transcript, and record tool calls and tokens for clauses known to add them.
