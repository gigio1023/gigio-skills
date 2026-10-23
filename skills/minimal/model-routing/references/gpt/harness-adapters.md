# Harness Adapters

Apply the GPT routing policy through the active harness's supported controls. Use its current tool schema and model catalog; implementation behavior that contradicts the exposed contract is not permission to bypass it.

## Capability Check

Before a spawn in an unfamiliar surface, establish:

1. Whether model and effort are set per call, per role, or globally.
2. Which model IDs and effort levels the surface accepts.
3. Which fork modes, role pins, and override rules apply.
4. Whether the result exposes the child's applied settings.

Record the selected settings and their source in the dispatch. Record runtime confirmation separately. If only one delegation model is available, send it only packets eligible for that model under the GPT policy. Keep other work with an eligible lead or report the limitation; do not silently turn the available model into a substitute for the selected route.

## Codex

The [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) documents `agents.default_subagent_model` and `agents.default_subagent_reasoning_effort`. Explicit spawn values take precedence over those defaults. The [subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) documents custom TOML agents with `name`, `description`, and `developer_instructions`, plus supported configuration fields such as `model` and `model_reasoning_effort`.

Read the active spawn tool before dispatch. A role that locks settings must be used with those settings; select another role or a supported explicit override when the task needs different settings. Do not assume `agent_type` exists on every Codex surface.

When the current tool says a full-history fork inherits settings and rejects overrides, follow that contract. For an override, use `fork_turns: "none"` or a supported positive integer string and supply the context the worker needs. For a full-history fork, omit overrides and use it only when the inherited model and effort fit the task. Historical handler behavior does not change this rule.

### Explicit Spawn

For a surface exposing the native `spawn_agent` fields below:

```json
{"task_name":"implement_parser","message":"Implement the assigned parser change within the supplied scope and return the diff and verification evidence.","model":"gpt-6-astra","reasoning_effort":"xhigh","fork_turns":"none"}
```

For ordinary research, set `model: "gpt-6.1-sol"` with an explicit supported effort. Supply the question, scope, sources or discovery context, evidence expectations, output, and escalation conditions. Sol may refine queries, select sources, organize findings, and summarize evidence within that scope. Use the narrower fixed execution contract only for `sol-clerk`.

### Optional Role Installation

1. Confirm the target CLI and account expose both `gpt-6-astra` and `gpt-6.1-sol` for the combined policy. Inspect the current catalog; a bundled entry does not establish account access.
2. Under the user's installation grant, merge `assets/gpt/codex/config.snippet.toml` into the chosen user or project configuration. Unnamed workers default to Sol 6.1 at `xhigh`; select Astra explicitly for complex work, decision synthesis, and final review.
3. Copy the role files from `assets/gpt/codex/agents/` into the supported agent directory, conventionally `~/.codex/agents/` or the project's `.codex/agents/`. Inspect existing files before replacing any.
4. Add the current `sol-scout` for ordinary research and retain `astra-scout` for difficult investigation and decision synthesis. Replace any legacy GPT-6 Sol version of `sol-scout` with the current Sol 6.1 definition. Keep `astra-builder`, `astra-judge`, and the mechanical `sol-clerk`. Update old `sol-builder` references to `astra-builder`; retire obsolete files only within the installation grant and preserve unrelated custom roles.
5. Validate configuration and role discovery through the target harness. A live model call runs only when the task requests or requires it; report untested runtime application otherwise.

Set model and effort together in explicit defaults. The assets use `xhigh`; preserve an explicitly selected effort by choosing a compatible role or supported explicit spawn instead of silently using a conflicting pin. Do not change service tier, concurrency, or the lead model as a side effect of installing worker roles.

### Delegated Missions

`codex-delegate` owns the external mission's launch, model, effort, grant, and evidence. This routing policy applies to GPT children inside that mission whenever the packet and harness allow internal subagents. It applies again to permitted descendants. The mission's scope and budget remain binding.

## Hermes Agent

The Hermes v0.21.3 source inspected on 2026-09-23 uses `delegation.model`, `delegation.provider`, and `delegation.reasoning_effort` as shared child settings. An empty child effort inherits the parent's resolved effort; `agent.reasoning_overrides` does not set the child effort in that version. These are dated findings. Recheck the current version before configuring it.

With a single child model, select the shared setting for the delegated workload. Sol 6.1 can handle ordinary research and collection while an eligible lead keeps complex judgment and decision synthesis. If workers must perform Astra work, use Astra or a supported separate configuration. Do not change a shared setting while active workers depend on it; recheck the current runtime before applying configuration.

## OpenCode

The agent documentation inspected on 2026-09-20 used per-agent `model` and `mode: subagent`, with provider-specific effort fields. Recheck the installed provider and [agent documentation](https://opencode.ai/docs/agents/) before installation. Express Sol 6.1 as the ordinary research route and Astra as the complex work and decision route; keep a separate mechanical role if useful. Do not infer API support from a display name.

## Claude Code And Cursor

Use the current native or proxy adapter for GPT access. The Fable family's adapter reference, `references/fable/harness-adapters.md`, describes the separately maintained Claude and Cursor mechanics. Confirm the exact GPT model ID, effort, tool support, and override behavior before dispatch. A proxy alias is not proof that it resolves to Astra or Sol 6.1.

## API Boundary

GPT-6.1 Sol is `gpt-6.1-sol`, distinct from legacy `gpt-6-sol`. Its public API accepts `low`, `medium`, `high`, `xhigh`, and `max`; `none` and `minimal` are unsupported. Tool calling requires Responses. Codex's catalog and modes are separate from this API contract. For migration details, discover the companion `prompting-guide` skill (formerly `gpt6-prompting-guide`) and read its GPT runtime notes.
