# Source Notes

## Policy And Evidence

On 2026-10-24 this pack changed its operating policy: Sol 6.1 handles most ordinary research, source selection, collection, organization, and summaries; Astra handles consequential judgment, decision synthesis, complex work, and final review. This supersedes the mechanical-only Sol policy from 2026-10-06. The split is a maintainer preference intended to reduce routine Astra use, not a measured cost or quality result. Explicit user routing choices still govern.

This policy owns GPT model selection. The Fable policy in `references/fable/` owns Anthropic choices. They share delegation concepts, but their policies are not mirrored text. Orchestration owns decomposition and synthesis, and each harness adapter owns the supported control mechanism.

## Sources Checked On 2026-10-06

| Source | Checked claim |
| --- | --- |
| [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Exact ID, supported efforts, default `medium`, Responses tool requirement |
| [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.1-sol) | Sol 6.1 differs from legacy Sol; preserve supported effort during migration |
| [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Custom TOML agent schema and discovery locations |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Worker model and effort default keys, explicit spawn precedence |

The local Codex CLI was `0.159.3`. Its `codex debug models --bundled` catalog listed Astra and Sol 6.1 with `low`, `medium`, `high`, `xhigh`, `max`, and `ultra`; both bundled defaults were `low`. These catalog values differ from the API default and do not establish served catalog values or account access.

The authoring session's native spawn tool exposed both model IDs and `xhigh`. Its contract allowed model and effort overrides only with `fork_turns: "none"` or a positive integer string. Full-history forks inherited settings. No child was launched to test these assets.

## Dated Adapter Evidence

- Codex source at `rust-v0.154.0`, inspected 2026-09-20, described role pins and model-only catalog fallback. Current documentation and the active tool contract now control the normal path. In particular, this package no longer recommends exploiting historical full-fork implementation behavior.
- Hermes Agent v0.21.3, inspected 2026-09-23: `tools/delegate_tool_config.py` lines 494-507 and `hermes_cli/config_defaults.py` established shared delegation model and effort settings.
- [OpenCode agents](https://opencode.ai/docs/agents/), inspected 2026-09-20: per-agent model, subagent mode, and provider-specific effort configuration. Recheck before configuring a newer version.

## Policy History

- 2026-10-24: added `sol-scout` on Sol 6.1 and made Sol 6.1 the unnamed worker default. Narrowed `astra-scout` to difficult investigation and decision synthesis, retained Astra builder and judge roles, and kept `sol-clerk` as an optional mechanical executor. Source selection and interpretation alone no longer require Astra. Effort defaults remain `xhigh`; no new model capability or runtime claim is introduced.

- 2026-10-12: packaged with the Fable policy in the `model-routing` skill, formerly `gpt6-astra-model-routing` and `fable5-model-routing`. This policy moved to `references/gpt/policy.md` and its Codex assets to `assets/gpt/codex/`; role models, efforts, and instructions are unchanged. `small-model-handoff` became optional for Sol packets, with a self-contained packet fallback.
- 2026-10-06: Astra became the default for named and unnamed GPT workers at every allowed delegation depth. `sol-scout` and `sol-builder` became Astra roles. `sol-clerk` moved to Sol 6.1 with a mechanical-only packet. Removed automatic frontier effort reduction, cheap-first trials, arbitrary consultation caps, and the mirrored Fable core. Preserved actual user budgets and authorization boundaries.
- 2026-09-23: earlier policy used legacy GPT-6 Sol for general workers. That policy and its runtime assumptions are superseded.
- 2026-09-20: initial GPT-family routing package.

## Verification Boundary

Package, reference, and TOML checks establish authored consistency. They do not establish installed configuration, a successful model spawn, cost savings, or quality improvement. Normal skill use records mutable runtime facts in task artifacts; maintaining this file requires a skill-edit request.
