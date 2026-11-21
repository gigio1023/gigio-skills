# Codex

Read from the Codex docs on 2026-11-21. Checked on a local `codex-cli 0.171.0`: the `exec` flags named below, `codex exec resume`, and the feature list. Nothing here was exercised in a delegated run. The subagent tools change between builds, so trust the live tool list over this file.

## Roles and Models

Model IDs have changed across versions: the docs on this date name GPT-6.2 Astra, GPT-6.2 Sol, and GPT-6 Luna, while local configs still carry IDs such as `gpt-6-astra` and `gpt-6-sol`. Take the ID from what the installed CLI offers and record the one that ran.

| Role | Model family | Note |
| --- | --- | --- |
| Lead | Astra | Or a lead in another harness |
| Child session | Astra | Sol when the task is research, collection, or cited summary |
| Subagent executing a fixed plan | Sol or Luna | Luna is a leaf: as a subagent it has no subagent tools |

## A Codex Run as the Child Session

When the lead runs in another harness, the child is one durable non-interactive run.

- `codex exec` takes the brief as its prompt, `-m` for the model, `-o` to capture the final message, `--json` for events, and `--output-schema` to force the report fields. `codex exec resume <SESSION_ID>` continues the same thread with a follow-up.
- The lead learns of completion from process exit and the captured message. There is no mid-run steering: a rejection is a resumed turn that carries the gap.
- The run may use its own subagents within the brief's limit.
- The brief and every file the run reads go to the provider behind the Codex account. Include only what the user's data policy allows that provider to see.
- If the host has a launcher for detached Codex runs, use it for launch, watch, resume, and cancel instead of composing the commands by hand.

## A Lead Inside Codex

- No in-model tool starts a top-level session. A child session the user can open is a separate `codex exec` run, which then appears in `codex agents`. The lead waits on process exit; nothing pushes completion to it.
- A subagent suits a piece whose result the lead needs in the same turn. The user can only switch to it with `/subagents`.
- Set model and reasoning effort on every `spawn_agent`. Setting only the model resets effort to that model's default. Some builds hide these fields from the tool schema or reject models outside an allowlist; `agents.default_subagent_model` and `agents.default_subagent_reasoning_effort` in the config are the fallback.
- Completion mail does not wake an idle parent. Call `wait_agent` with a timeout matched to the expected duration.
- Children inherit the parent's sandbox and approval policy, and an agent role file in `~/.codex/agents/` can set model and instructions but cannot narrow permissions. The scope in a brief is therefore an instruction only. Keep parallel writers in separate worktrees.
- Feature flags decide which subagent tools exist. On the checked machine `multi_agent` was on and marked deprecated, and `multi_agent_v2` was off; reports of hidden model fields concern the V2 tools. `codex features list` shows the current state.
