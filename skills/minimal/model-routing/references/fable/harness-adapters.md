# Harness Adapters

The routing policy in `references/fable/policy.md` is harness-neutral. This reference says how each harness actually sets a subagent's model and effort, what it cannot set, where the subagent definitions go, and how to report what was resolved. Facts carry the date and version they were checked against; recheck them when the harness changes.

## Contents

- Generic procedure for any harness
- Claude Code
- Cursor
- Hermes Agent
- OpenCode
- Proxy-routed subagents
- Codex under a Fable lead
- Reporting and measurement

## Generic Procedure for Any Harness

Before the first spawn in an unfamiliar harness, establish four things and record them in the task artifact with the date and version.

1. **Where a delegated agent's model is set.** Three places are common: an argument on the spawn call, a field in a per-agent definition file, or one global delegation setting. A harness may offer more than one, with a precedence order.
2. **Where its reasoning effort is set.** Check the same three places. Many harnesses set effort only per definition or only globally.
3. **Which routes that allows.** Per-spawn control means the tier table can be applied directly and stated in the dispatch line. Per-definition control means install one definition per route, then choose the definition. Global-only control means one route; decide whether it is acceptable for the tier and state the inherited settings.
4. **Whether the runtime exposes the applied settings.** Look for a dispatch log, a hook, or a status view. If nothing exposes them, every dispatch line ends with `runtime unverified`.

If a subagent cannot be given a different model or effort, the skill still governs the decision: say the inherited values, and do not send judgment-adjacent work to a below-frontier model.

## Claude Code

Checked against Claude Code 2.1.278 and its documentation on 2026-09-20; alias, effort-resolution, and cost facts rechecked against Claude Code 2.1.280 and Anthropic's Opus 5.5 pages on 2026-09-23 (`code.claude.com/docs/en/sub-agents`, `code.claude.com/docs/en/model-config`, `code.claude.com/docs/en/agent-sdk/subagents`). Sonnet 5.5, Ultracode, the Agent tool's `effort` argument, fan-out defaults, and prices rechecked on 2026-10-07 against Claude Code 2.1.292, its changelog, and the same pages.

**Choosing the definition.** The Agent tool's `subagent_type` selects a subagent definition; that is the primary control. Its `model` argument accepts the aliases `sonnet`, `opus`, `haiku`, and `fable`, and applies only to definitions that do not pin a model. Since 2.1.292 the tool also takes an optional `effort` argument; its tool description tells the lead to set it only when the user, CLAUDE.md, or a skill asks for a specific level. When a route needs a level that no installed definition carries, pass it there and say so in the dispatch line. How it ranks against a definition's `effort` was not documented when checked on 2026-10-07.

**Definition fields.** A definition in `~/.claude/agents/<name>.md` (user) or `.claude/agents/<name>.md` (project) carries `model` (`sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit`) and `effort` (`low`, `medium`, `high`, `xhigh`, `max`; default inherits the session). Other fields such as `tools`, `disallowedTools`, `permissionMode`, and `maxTurns` bound the subagent further. The Agent SDK's `AgentDefinition.effort` also accepts a number.

**Model resolution.** Per-invocation `model` → the definition's `model` (`inherit` means the main conversation's model) → `CLAUDE_CODE_SUBAGENT_MODEL` → the main conversation's model. `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` applies one model to every subagent, teammate, and workflow agent; set alone, it pins them to the main model. The env var alone does not move the built-in Explore and Plan agents. A family alias such as `opus` or `fable`, in the per-invocation `model` or in a definition, resolves to the main conversation's exact model when that model belongs to the same family, including any `[1m]` suffix; under a Fable 5 lead, `fable-reviewer` and `fable-builder` therefore run Fable 5, not Fable 5.1. An alias in `CLAUDE_CODE_SUBAGENT_MODEL` always resolves to the version the alias points to.

**Effort resolution.** The session level comes from an explicit choice (`CLAUDE_CODE_EFFORT_LEVEL`, `--effort`, `/effort`), else settings (a level saved per model under `modelSettings.<model>.effortLevel`, or a top-level `effortLevel`), else the model default (`high`, except Opus 5.5 and Sonnet 5.5 at `medium` and Opus 4.7 at `xhigh`). A top-level `effortLevel` in the user settings file no longer applies to Opus 5.5 or later models; only a per-model entry does. A definition's `effort` overrides the session level but not the env var. `maxEffortLevel` caps every path; across settings files the lowest value wins, and `modelSettings.<model>.maxEffortLevel` replaces it per model. A definition without `effort` inherits the session level, which on a machine that saves `xhigh` for the lead model means `xhigh` for the subagent.

**Aliases.** `fable` resolves to Fable 5.1 unless `ANTHROPIC_DEFAULT_FABLE_MODEL` overrides it; in Claude apps gateway sessions `fable` and `best` resolve to Fable 5. `opus` resolves to Opus 5.5 from v2.1.280 on the Anthropic API, Claude Platform on AWS, Amazon Bedrock, and Google Cloud's Agent Platform, and to Opus 4.6 on Microsoft Foundry, so a definition with `model: opus` changed models when the alias moved; pin `claude-opus-5-5` when the version matters. `sonnet` resolves to Sonnet 5.5 on the Anthropic API from v2.1.284, to Sonnet 4.6 on Claude Platform on AWS, and to Sonnet 4.5 on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, so `sonnet-collector` and `sonnet-researcher` moved from Sonnet 5 to Sonnet 5.5 with the alias; pin `claude-sonnet-5` or `claude-sonnet-5-5` when the version matters.

**Caps and related settings.** `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (default 20) and `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (default 3) bound fan-out; the SDK adds `maxBudgetUsd`. `ultracode` is a setting, not an effort level: it lets Claude orchestrate dynamic workflows at whatever effort the session runs. Since 2.1.285 it is its own toggle in `/effort` and no longer forces `xhigh`; only `--effort ultracode` and the Agent SDK's `effortLevel: "ultracode"` also set `xhigh`. Sessions with ultracode on are exempt from the concurrent-subagent limit. Since 2.1.277 a subagent's result reaches the lead under a header marking it as subagent output.

**Cost note.** Cached input is the largest term in an agent loop. Fable 5.1 cache reads ($0.25 per million) cost half of Opus 5's ($0.50), which made `fable` at `low` a cheaper escalation than `opus` while `opus` meant Opus 5. Opus 5.5's cache reads are $0.20 and its base prices are $4 and $20 against Fable 5.1's $10 and $50, so that argument now runs the other way. Sonnet 5.5 costs the same as Sonnet 5: $2 and $10, with cache reads at $0.20 (pricing page, 2026-10-07). Whether Fable at `low` is cheaper per completed task than Opus 5.5 at the floor is unmeasured.

**Installing the definitions.** Copy the files from `assets/fable/agents/claude-code/` into `~/.claude/agents/` or the project's `.claude/agents/` after the user approves, then spawn with `subagent_type` set to the definition's name. Preserve the selected session effort for Fable roles; their assets omit `effort`. Use an explicit compatible definition when the user selects another level. If an earlier version of this pack installed `fable-lean-builder`, update references to it and retire that old installed role only within the installation grant.

**Measuring what ran.** Nothing in the Agent tool's result reports the applied effort to the lead. The user can run `/tasks`, which names each subagent's model and adds its effort level when the definition, or the skill it forked from, sets `effort`. A `PostToolUse` hook matched on the `Agent` tool receives the call's full input and result as JSON on stdin. A filter such as `jq -c '{subagent_type: .tool_input.subagent_type, model: .tool_input.model}' >> ~/.claude/dispatch-log.jsonl` records each dispatch's requested `subagent_type` and `model`, which is what was asked for, not what ran. Keep the filter: a bare `cat >>` would also persist every subagent prompt and result in plain text. Propose the hook; do not install it unasked. Without a confirmation the lead can read, dispatch lines end with `runtime unverified`.

## Cursor

Checked against `cursor.com/docs/subagents` (formerly `cursor.com/docs/agent/subagents`) on 2026-09-20; definition locations rechecked on 2026-09-23.

A subagent file carries `name`, `description`, `model` (default `inherit`), `readonly`, and `is_background`. Model and effort travel together in the model string: `model: "claude-opus-5[effort=high]"`, with further options such as `context=300k` and `fast=false` combinable as `[effort=high,context=300k]`. An empty bracket pair such as `composer-2.5[]` selects the standard variant instead of the fast one, which is a cost difference. Options depend on the model and use the SDK's parameter names; the page does not enumerate which models accept `effort`, so confirm a Fable model string against a live `agent models` listing before relying on it. There is no per-invocation choice: the route is which definition runs. Definitions live in `.cursor/agents/` for a project and `~/.cursor/agents/` for the user; project definitions win on a name conflict, and `.cursor/` wins over `.claude/` or `.codex/` copies of the same name.

## Hermes Agent

Checked against the Hermes Agent v0.21.3 source (`tools/delegate_tool_config.py`, `hermes_cli/config_defaults.py`) on 2026-09-23; key names were first observed in a local configuration on 2026-09-20.

`delegation.model` and `delegation.provider` set one model for every delegated agent, so Hermes offers one delegated-agent model per configuration. `delegation.reasoning_effort` sets every delegated agent's effort; when it is empty, a child takes the parent's already-resolved effort. `agent.reasoning_effort` and `agent.reasoning_overrides` resolve only the lead's effort, so a per-model effort override does not reach a child. Express the effort floor as `delegation.reasoning_effort: xhigh` beside the delegation model; one value then applies to every child. With this shape, the routing decision is whether the configured delegation model and effort fit the tier of the work being delegated; when they do not, keep the work with the lead or ask the user to change the delegation settings for the session, and state the inherited settings in the dispatch line.

## OpenCode

Checked against `opencode.ai/docs/agents/` on 2026-09-20.

Agents are defined in `opencode.json` under `agent.<name>` or as Markdown agent files, with `mode: subagent` for delegated agents. Each agent carries its own `model`, and unrecognized keys pass through to the provider, so `reasoningEffort` sets the subagent's effort where the provider supports it. `permission.task` controls which agents may be spawned. Routes are therefore per definition, as in Claude Code.

## Proxy-Routed Subagents

A proxy can expose GPT models as Claude Code agent definitions. Inspect its actual route list, exact model ID, effort, and tool support before selecting a route. Do not infer these from an alias or assume a spawn override changes a pinned proxy definition.

GPT workers follow the GPT routing policy in `references/gpt/policy.md` even under a Fable lead. Use Sol 6.1 for ordinary research, source selection, collection, organization, and summaries; use Astra for complex work, consequential judgment, decision synthesis, and final review. The mechanical-only contract applies to `sol-clerk`, not every Sol worker. A proxy exposing only legacy GPT-6 Sol does not satisfy an exact Sol 6.1 route.

## Codex Under a Fable Lead

A Fable lead inside Codex is possible only through a proxy. If it occurs, the mechanics are Codex's: spawn arguments, `[agents]` defaults, and role files, described in the GPT adapter reference, `references/gpt/harness-adapters.md`. Follow the active tool contract, including fork restrictions. Anthropic workers follow the Fable policy; GPT workers follow the GPT routing policy.

## Reporting and Measurement

State one line per task before spawning: tier, `agent_type`, resolved model, resolved effort, where the value was read, and `runtime confirmed` or `runtime unverified`. "Where the value was read" is a file path, a settings key, a proxy route string, or the word `inherited` followed by the inherited value. Never describe the intended configuration as the one that ran.
