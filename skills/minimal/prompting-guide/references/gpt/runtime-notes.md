# GPT-6 Runtime Notes

The model, effort, and tool-calling distinctions below were checked against official OpenAI documentation on 2026-10-06. The later runtime-feature sections retain their 2026-09-23 review date; recheck them before changing an integration. Codex and the public API have separate catalogs and controls.

## Models And Effort

| Model | Exact ID | API effort | Tool calling |
| --- | --- | --- | --- |
| GPT-6 Astra | `gpt-6-astra` | `low`, `medium`, `high`, `xhigh`, `max` | Responses |
| GPT-6.1 Sol | `gpt-6.1-sol` | `low`, `medium` (default), `high`, `xhigh`, `max` | Responses |
| Legacy GPT-6 Sol | `gpt-6-sol` | Includes `none`; default `medium` | Responses, or Chat Completions at `none` |

The [Sol 6.1 model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol) explicitly excludes `none` and `minimal`. Do not transfer the legacy Sol tool-calling exception to Sol 6.1. The [GPT-6 migration guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.1-sol) distinguishes these models and Astra.

Codex reads its own catalog. The local CLI 0.159.3 bundled catalog inspected on 2026-10-06 listed Astra and Sol 6.1 with `low` through `ultra`, both with default `low`. A bundled catalog does not prove served availability or account access. Check the active surface before assigning a model, and treat `ultra` as a harness mode rather than an API effort.

## Migration Compatibility

The [migration quickstart](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.1-sol#migration-quickstart) establishes these settings:

- Preserve the effective effort where supported. Astra and Sol 6.1 have no `none`; start at `low` for a previous `none` or `minimal` baseline and verify the target workload.
- Use Responses for tools. Astra and Sol 6.1 support Chat Completions without tools. The Chat Completions function-calling exception at `none` belongs to legacy Sol and Luna only.
- When effort is not `none`, remove `temperature`, `top_p`, and `top_logprobs`; also remove Chat Completions `logprobs` or Responses `message.output_text.logprobs` include entries.
- Verify processing-tier and data-residency compatibility separately when relevant to the deployment.
- When migrating older integrations, review the current caching contract before replacing legacy cache fields.

Keep runtime compatibility changes separate from prompt edits and routing policy. Whether Sol 6.1 fits a workload is a routing decision governed by the current GPT policy in `model-routing`, when installed.

## Moving From GPT-5.6

The `model-routing` skill, when installed, owns current GPT task assignments. OpenAI documented GPT-5.6's prompt tendencies, such as preferring shorter prompts and compressing output under generic brevity instructions, for GPT-5.6 only; do not carry them to a newer model unmeasured. Start from this package's patterns and verify changes against the target workload.

[Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md) keeps the API capabilities GPT-5.6 had, including Programmatic Tool Calling, multi-agent orchestration, persisted reasoning, compaction, pro mode, and prompt caching. They stay runtime settings:

- `reasoning.mode: "pro"` selects pro execution for difficult tasks that tolerate latency; it is independent of `reasoning.effort` and is not a prompt instruction ([reasoning guide](https://developers.openai.com/api/docs/guides/reasoning#reasoning-mode)).
- `reasoning.context` selects whether earlier turns' reasoning is rendered into the next sample on supported models. Carry reasoning only while the objective and assumptions still hold; stale reasoning can anchor the model to an obsolete path.
- Programmatic Tool Calling fits bounded, deterministic reduction of large structured results. Keep direct calls for approvals, citations, semantic judgment, and steps where each result changes the next move.

## Changing Effort During A Conversation

The [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) supports `configuration_update` for the GPT-6 family in standard, single-agent mode. Insert the item before the next user message while retaining the original request-level `reasoning.effort` to preserve the cacheable prompt prefix. The updated effort persists until another update, and two updates may not sit next to each other. This changes effort only; check the current compatibility section before combining it with other modes.

The [prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering#message-roles-and-instruction-following) also notes that `instructions` from a previous response are not inherited merely by passing `previous_response_id`. The integration must supply applicable instructions on the next request.

## Async Tools

With [async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling), set `async: true` on a function or custom tool definition. The application executes the tool and returns its eventual output with the original `call_id`. The model can work on independent steps in the meantime. This feature does not host the job or replace application state management.

Before adopting it, identify the result consumer, failure path, and completion condition. Keep dependent actions behind the actual result. Do not equate an async call with a completed action or with background response generation.

## Mid-Turn Steering

[Steering](https://developers.openai.com/api/docs/guides/steering) is available for the GPT-6 family over a Responses WebSocket connection. Send `response.steer` after `response.created`, identifying the original response with `previous_response_id`. Acceptance queues the input; it does not establish that the change has taken effect.

Steering does not retract emitted output, undo earlier actions, or cancel started tools. Track continuation and failure events, and return outstanding tool results or approvals required by the API. A prompt cannot supply this transport behavior on its own.
