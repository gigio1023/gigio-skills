---
name: model-routing
description: >
  Choose each subagent's model and reasoning effort and state the resolved settings before spawning, whenever a Claude Fable lead delegates in a harness with subagents or a GPT-6 lead spawns subagents or a GPT worker is assigned, including inside codex-delegate missions. Also installs or maintains the shipped subagent definitions, GPT worker defaults, and Codex role files, and brings Fable in as a judge under another lead when asked. Use for "which model for this subagent", "set the workers' effort", "subagent model 정해줘", "worker 모델 골라줘". NOT for deciding whether to delegate (orchestrate-subagents) or launching an external mission (codex-delegate).
---

# Model Routing

This skill ships two routing policies, one per model family. They share orchestration principles but not model tables, default routes, or effort rules, so load only the policy that applies and keep each family's rules on that family's models.

## Select the Policy

Read the lead's identity from what the harness states, such as the system prompt or the model setting. The harness alone does not settle it: Claude Code can reach GPT models through a proxy, and a proxied Fable lead can run inside Codex.

| Lead | Load |
|------|------|
| Claude Fable 5 or 5.1; Mythos 5 and 5.1 count as Fable | `references/fable/policy.md` |
| GPT-6 Astra, GPT-6.1 Sol, or legacy GPT-6 Sol, including a lead inside a `codex-delegate` mission | `references/gpt/policy.md` |
| Any other model, or a lead that cannot be established | No shipped policy for that lead: say so and use the harness defaults, apart from the cross-family cases below. Treat an unestablished lead as non-Fable. |

Two cases open a policy other than the lead's. A worker from another family follows its own family's policy, for that worker only. Installing or maintaining shipped files follows the policy of the family whose files change, whoever edits them: a GPT lead updating Fable agent definitions reads the Fable policy and its harness adapters. GPT workers follow `references/gpt/policy.md` under any lead, including a Fable lead or a lead with no shipped policy. Under a non-Fable lead, the Fable policy applies only on request, when the user names it (formerly `fable5-model-routing`) or asks to put Fable on the judgment; its "Another model leads" rule in `references/fable/policy.md` governs that case. Without such a request, Anthropic workers under a non-Fable lead have no shipped policy and use the harness defaults.

Never carry one family's tier table, default routes, effort defaults, or role files to the other family's models. For example, Fable workers inherit the selected session effort even though the GPT roles ship at `xhigh`, and the GPT division between ordinary Sol research and Astra judgment does not govern Sonnet or Haiku routes.

## Boundaries

This skill selects model and effort for a delegation that the user or the lead has already decided on. An explicit user instruction about delegation, model, effort, or budget governs; otherwise `orchestrate-subagents` and the lead's judgment decide whether to delegate. Install or update subagent definitions, worker defaults, or role files only under the user's configuration grant. Each policy states these boundaries in full for its family.

## Family Files

Open a family's policy first; it says when to read the rest.

| Family | Policy | Harness mechanics | Maintenance notes | Installable assets |
|--------|--------|-------------------|-------------------|--------------------|
| Fable | `references/fable/policy.md` | `references/fable/harness-adapters.md` | `references/fable/source-notes.md` | `assets/fable/agents/claude-code/` |
| GPT | `references/gpt/policy.md` | `references/gpt/harness-adapters.md` | `references/gpt/source-notes.md` | `assets/gpt/codex/` |

When maintaining this skill, edit only the family whose facts or policy changed. The policies are not mirrored, so a change to one does not imply the same change to the other.
