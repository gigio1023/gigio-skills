# Opus 5.5 Runtime And Migration

The runtime facts a prompt author needs to put each fix in the right layer. Recheck the linked pages before changing an integration.

## Model Facts

- The API ID is `claude-opus-5-5`, a fixed ID with no date suffix. Amazon Bedrock uses `anthropic.claude-opus-5-5`; Google Cloud, Microsoft Foundry, and Claude Platform on AWS use `claude-opus-5-5`.
- It has a 1M-token context window and 128k max output tokens, the same as Opus 5.
- Prices per million tokens are $4 input and $20 output, below Opus 5's $5 and $25. Cache reads cost $0.20 (0.05x the input price), 5-minute cache writes $5, and 1-hour cache writes $8. Batch processing is half price. The minimum cacheable prompt is 512 tokens.
- Anthropic's [models overview](https://platform.claude.com/docs/en/models/overview) recommends starting with Opus 5.5 for most workloads and using Fable 5.1 for demanding reasoning and long-horizon agentic work, or when evals on Opus 5.5 at higher effort still fall short.

## Effort

Source: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5-5).

- Opus 5.5 supports `low`, `medium`, `high`, `xhigh`, and `max`. The default is `medium`; Opus 5 and earlier Opus models default to `high`, so a request that omits `effort` now runs one level lower than it did on Opus 5.
- Adaptive thinking is always on, so effort is the primary control for reasoning depth, latency, and cost.
- In Anthropic's testing, 5.5 at `medium` matches or exceeds Opus 5 at `high` on coding and knowledge-work evaluations, and `low` comes close on several coding evaluations at much lower cost. At a given level, 5.5 tends to think more per turn than Opus 5, most of all at `xhigh` and `max`.
- `max_tokens` is a hard limit on thinking plus response text, including thinking that is not returned. Size it for the chosen level.
- Changing the top-level `effort` between requests invalidates the prompt cache. Per-message effort (beta) changes individual turns and keeps it.
- Fast mode (research preview) is available for Opus 5.5 on the Claude API only, with `speed: "fast"`.

## Breaking Changes From Opus 5

Source: [What's new](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5#breaking-changes) and the [migration guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide#migrating-from-claude-opus-5).

1. **Thinking cannot be disabled.** `thinking: {"type": "disabled"}` and `thinking: {"type": "enabled", "budget_tokens": N}` return a 400 `invalid_request_error`. Omit `thinking` or send `{"type": "adaptive"}`, and use a lower effort level where thinking used to be disabled.
2. **Forced tool use is not supported.** `tool_choice` of type `any` or `tool` returns a 400, including on the token counting endpoint; `auto` and `none` work. For schema-valid calls, keep `auto` and set `strict: true`, or move the schema to structured outputs. To make the model call a tool, say in the prompt when it applies.
3. **Thinking blocks are tied to the model and the conversation.** See [append-only history](#append-only-history).
4. **`computer_20251124` is rejected on the Claude API and Google Cloud.** Declare `computer_toolset_20260801` with no beta header and no `name` or display size, then update the loop for member `tool_use` blocks (the action is the block's `name`), several per turn, and echo `toolset_name` on every result. Amazon Bedrock still accepts the older tool.

A shape change that fails no request: text the model writes between tool calls arrives as progress-update `thinking` blocks, at most one before each tool call, with empty text at the default `display: "omitted"`. `display: "updates"` (beta) returns the updates while reasoning stays hidden; `display: "summarized"` returns both, mixed. Select content blocks by `type` and pass `thinking` blocks back unmodified with tool results.

## Append-Only History

Source: [Preserved thinking](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking) and [mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages).

- Every thinking block records the model that produced it. Opus 5.5 reads blocks from Opus 5 and earlier Opus, Sonnet, and Haiku models, but not from Fable or Mythos. On the Claude API, Fable 5.1 and Mythos 5.1 read Opus 5.5 blocks; no other model does. A block the target model cannot read is dropped before the model sees it, without an error or a charge; with the binding-controls beta header the drop is reported in a top-level `input_transformations` array. A router or fallback that moves a conversation off 5.5 therefore loses its reasoning, except onto Fable 5.1 or Mythos 5.1 on the API.
- The API also checks whether anything before a 5.5 thinking block, meaning the `system` prompt, the `tools`, or an earlier message, changed after the block was produced. For accounts created on or after 2026-08-31 00:00 UTC, replaying a block after such a change returns a 400 by default. Setting `thinking.block_binding.prefix_mismatch_behavior` to `"drop_block"` with the binding-controls header drops the affected blocks instead.
- Consequences for prompt authors: include the stop policy and any send-to-user tool from the first request; deliver later instruction or tool changes as mid-conversation system messages; send per-turn reminders as turn-scoped system messages (`clear_at: "next_user_message"`) and leave them in place. A `tool_addition` block in a mid-conversation system message can carry a full tool definition (beta), and on-demand compaction (beta) can keep later thinking blocks valid under the conditions its page states.

## Refusals

Source: [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback).

A decline returns HTTP 200 with `stop_reason: "refusal"` and a `stop_details` object whose `category` names the policy area; expect `bio` and `reasoning_extraction` on 5.5 in addition to `cyber`. Configure server-side fallback (`fallbacks: "default"`, beta), the SDK middleware, or your own retry. Server-side fallback does not retry `reasoning_extraction` declines; it returns them.

## Agent Loop Summary

The loop rules from [symptom patterns](symptom-patterns.md) in one place: treat a text-only end of turn as a report; continue with a message naming open items, at most two or three times per task; wait for running background work before calling a task done; count silent tool-calling steps and send at most two or three turn-scoped reminders; append elapsed time against a budget for agent teams and keep a hard timeout. [Task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets) (beta) give an advisory token budget for the whole loop and are supported on Opus 5.5.

## Beta Headers

The authoritative list for this guide. Each feature's page states current availability.

| Feature | Beta header |
| --- | --- |
| `thinking.display: "updates"` | `thinking-display-updates-2026-08-18` |
| Turn-scoped system messages (`clear_at`) | `mid-conversation-system-clear-at-2026-08-21` |
| Per-message effort | `mid-conversation-output-config-2026-07-01` |
| Thinking-binding controls and `input_transformations` | `thinking-binding-controls-2026-08-01` |
| Server-side fallback | `server-side-fallback-2026-07-01` |
| Tool definitions in a message | `inline-tools-2026-09-15` |
| Compaction on demand | `compact-2026-09-04` |
| Task budgets | `task-budgets-2026-03-13` |
| Fast mode | `fast-mode-2026-02-01` |
| 300k output on the Batches API | `output-300k-2026-03-24` |

## From Older Models

- **Claude Managed Agents:** only the model name changes.
- **Opus 4.8:** apply the Opus 4.8 to Opus 5 migration first, then Opus 5 to 5.5. Disabling thinking is not an option at any effort.
- **Opus 4.7 and earlier Opus models:** work through the matching section of the [Opus 5 migration guide](https://platform.claude.com/docs/en/models/opus-5/migration-guide) (sampling parameters rejected, manual extended thinking rejected, prefill removed, newer tokenizer) targeting `claude-opus-5-5`, then Opus 5 to 5.5. Where that guide says thinking can be disabled or `computer_20251124` keeps working, neither holds on 5.5 on the Claude API or Google Cloud.
- **Sonnet 5:** apply the Opus 5 guide's section on moving up from Sonnet 5, then Opus 5 to 5.5.

## Migration Checklist

- Update the model ID.
- Remove `thinking` disabled or manual-budget settings and choose an effort level; set `effort` explicitly.
- Replace forced `tool_choice` with `auto` plus strict tool use or structured outputs, and move the tool trigger into the prompt.
- Move computer use on the Claude API or Google Cloud to `computer_toolset_20260801`.
- Read content blocks by `type`; pass `thinking` blocks back unmodified; if the interface shows text between tool calls, set `display: "updates"` or `"summarized"` and render non-empty thinking blocks.
- Stop editing earlier turns, the `system` prompt, or `tools` mid-conversation; expect lost reasoning if a router moves conversations off 5.5.
- Handle `stop_reason: "refusal"` and configure fallback.
- Remove prompt instructions tuned for Opus 5 or for thinking disabled (see the removal list in `guide.md`), then re-baseline cost and latency at the chosen effort.
