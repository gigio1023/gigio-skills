# Codex

Checked 2026-11-21 against the Codex docs under `learn.chatgpt.com/docs` and, where the docs are silent, the `openai/codex` main source. Checked on a local `codex-cli 0.171.0`: the `exec` flags named below, `codex exec resume`, and the feature list. Nothing here was exercised in a delegated run. The subagent tools change between builds, so trust the live tool list over this file.

## Roles and Models

Model IDs have changed across versions: the models page on this date names GPT-6.2 Astra (`gpt-6.2-astra`), GPT-6.2 Sol (`gpt-6.2-sol`), and GPT-6 Luna (`gpt-6-luna`), and still lists older IDs such as `gpt-6-astra` and `gpt-6-sol` that local configs carry. Take the ID from what the installed CLI offers and record the one that ran.

| Role | Model family | Note |
| --- | --- | --- |
| Lead | Astra | Or a lead in another harness |
| Child session | Astra | Sol when the task is research, collection, or cited summary |
| Subagent executing a fixed plan | Sol or Luna | Luna for narrow, repeatable work |

## A Codex Run as the Child Session

When the lead runs in another harness, the child is one durable non-interactive run.

- `codex exec` takes the brief as its prompt, `-m` for the model, `-o` to capture the final message, `--json` for events, and `--output-schema` to force the report fields. `codex exec resume <SESSION_ID>` continues the same thread with a follow-up.
- The lead learns of completion from process exit and the captured message. There is no mid-run steering: a rejection is a resumed turn that carries the gap.
- The run may use its own subagents within the brief's limit.
- The brief and every file the run reads go to the provider behind the Codex account. Include only what the user's data policy allows that provider to see.
- If the host has a launcher for detached Codex runs, use it for launch, watch, resume, and cancel instead of composing the commands by hand.

## A Lead Inside Codex

- No in-model tool starts a top-level session. A child session the user can open is a separate `codex exec` run. Whether that run shows in `codex agents` is unchecked: `codex exec` runs on an embedded app server unless given `--remote`, and `codex agents` browses sessions on a shared one. The lead waits on process exit; nothing pushes completion to it.
- A subagent suits a piece whose result the lead needs in the same turn. In the CLI the user inspects and switches to its thread with `/subagents`.
- Set model and reasoning effort on every `spawn_agent`. A spawn that sets a model without an effort runs at that model's default effort. Whether the fields are offered depends on the build: the V2 `spawn_agent` drops `model` and `reasoning_effort` from its schema unless model overrides are exposed, V1 drops them when a hide option is set, and a model whose catalog entry lacks multi-agent support is refused. `agents.default_subagent_model` and `agents.default_subagent_reasoning_effort` in the config are the fallback; an explicit spawn value takes precedence over them.
- A child's completion notice goes to the parent's mailbox without starting a parent turn (`trigger_turn` is false in the source), so it does not wake an idle parent. Call `wait_agent` with a timeout matched to the expected duration.
- Children inherit the parent turn's sandbox and approval settings. A custom agent file under `~/.codex/agents/`, or `.codex/agents/` in a project, can set model, effort, and instructions and turn some tools off, but cannot replace the sandbox, approvals, provider, or MCP servers. The scope in a brief is therefore an instruction only. Keep parallel writers in separate worktrees.
- Feature flags decide which subagent tools exist. On the checked machine `multi_agent` was on and marked deprecated, and `multi_agent_v2` was off though marked stable; reports of hidden model fields concern the V2 tools, and a model's catalog entry can select V2 regardless of the flag ([openai/codex#31097](https://github.com/openai/codex/issues/31097)). The config reference still lists `features.multi_agent` as stable and omits `multi_agent_v2`, so trust `codex features list` for the current state.
