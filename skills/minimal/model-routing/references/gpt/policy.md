# GPT Routing Policy

Use GPT-6.1 Sol for most ordinary research, collection, organization, and summaries. Use GPT-6 Astra for consequential judgment, synthesis that supports decisions, complex design or implementation, difficult diagnosis, and final review. Split independent research from the decision it informs so Sol can gather and organize evidence while Astra works on the difficult part.

This is this pack's operating policy, not a measured quality or cost comparison. A user's explicit model choice or routing policy overrides it. It applies to GPT workers under any lead, at every permitted delegation depth, and inside missions launched through `codex-delegate`. Anthropic choices remain with the [Fable routing policy](../fable/policy.md).

## Routing Decision

Choose by the decisions the packet requires, not merely by whether it involves interpretation. Sol may choose sources, refine queries, summarize meaning, classify findings, compare reported facts, identify gaps, and pursue routine follow-ups within the assigned question. Those ordinary research decisions do not by themselves require Astra.

| Work | Route |
| --- | --- |
| Search for sources, collect evidence, summarize papers or repository behavior | Sol 6.1 |
| Extract limitations, organize findings, build cited comparisons, draft a factual brief | Sol 6.1 |
| Fetch specified URLs, deduplicate by a supplied key, run fixed status commands | Script or Sol 6.1 |
| Resolve consequential conflicting evidence, test hidden premises, recommend a direction | Astra |
| Synthesize evidence around decision criteria, trade-offs, and what would change the decision | Astra |
| Design or implement a system, diagnose a difficult failure, conduct final review | Astra |
| Mixed research and decision work | Sol 6.1 for separable research; Astra for integration and judgment |

The distinction is the purpose and difficulty of the work. Summarizing each paper's methods and limitations belongs with Sol; deciding whether conflicting results justify a research direction belongs with Astra. Comparing documented options belongs with Sol; choosing the option under uncertain requirements belongs with Astra. A packet whose consequential decisions cannot be separated stays on Astra without a required Sol trial.

Give Sol the question, scope, available context, source and coverage expectations, output, and escalation conditions. Do not require a fixed query list, mechanical-only acceptance, or a stop on every unexpected result. Sol resolves routine obstacles within scope and returns evidence when a material contradiction, missing premise, difficult diagnosis, or change of direction needs Astra. Continue independent parts when that does not depend on the unresolved decision.

Prefer a direct script or tool call when it already performs a mechanical operation. The `sol-clerk` role remains available for fixed execution; its restrictions apply to that role, not all Sol workers. When a fixed executor contract is useful and `small-model-handoff` is installed, it may write that packet. Ordinary research packets do not need that workflow.

## Delegation And Effort

An explicit user instruction about delegation, model, effort, or budget governs. Within that grant and the current harness contract, the lead or `orchestrate-subagents` decides whether delegation helps. This policy selects model and effort for an already justified GPT delegation; it does not require spawning or changing installed configuration.

Workers finish their assigned scope and return evidence. The lead owns integration, conflict resolution, and the final user response. When a worker may delegate further, its packet carries this GPT routing rule and the same authority and resource limits. An Astra worker should use Sol for separable ordinary research rather than duplicate its own model for every child.

Preserve the user's selected effort or the effective session effort when supported and appropriate to the task. Do not lower effort merely because the model is a worker. When no effort has been chosen, the shipped roles use `xhigh` for both Astra and Sol 6.1. Name model and effort together; a model-only override may use a catalog default. Runtime-specific modes such as `ultra` need their own compatibility and delegation checks.

Keep the user's actual cost, time, concurrency, and token limits. Do not invent a frontier consultation cap or require a cheap-model trial before Astra. After a failure, inspect the evidence and choose the next action within the grant; retry count alone does not identify the cause.

## Worker Roles

| Role | Responsibility | Shipped model and effort |
| --- | --- | --- |
| `sol-scout` | Ordinary research, source selection, collection, organization, cited summaries | `gpt-6.1-sol`, `xhigh` |
| `astra-scout` | Difficult investigation, conflicting evidence, synthesis for decisions | `gpt-6-astra`, `xhigh` |
| `astra-builder` | Design, implementation, difficult debugging, decision-sensitive writing | `gpt-6-astra`, `xhigh` |
| `astra-judge` | Independent final review of a specification, evidence, or artifact | `gpt-6-astra`, `xhigh` |
| `sol-clerk` | Fixed collection, transformation, or command execution | `gpt-6.1-sol`, `xhigh` |
| Unnamed worker | Ordinary research and execution; explicitly select Astra for the work above | `gpt-6.1-sol`, `xhigh` |

The role defines the task; it does not expand authority. A review packet returns findings, while a packet that authorizes fixes may include them. Astra is not restricted to advisory consultations. Sol's default does not make it the fallback for a packet that requires Astra.

Read [harness adapters](harness-adapters.md) before the first spawn in an unfamiliar harness. Use only fields, models, and effort levels the active surface supports. If the selected model is unavailable, keep the work with an eligible lead or report the limitation. Do not silently substitute Sol for required Astra judgment, or Astra for a requested Sol budget.

Before a spawn, state the task, role, selected model and effort, configuration source, and confirmation state. For example:

```text
Literature collection and summaries | sol-scout | gpt-6.1-sol | xhigh | spawn arguments | runtime unverified
Decision synthesis | astra-scout | gpt-6-astra | xhigh | spawn arguments | runtime unverified
```

Requested settings and observed runtime settings are separate evidence. A role file or accepted request establishes configuration, not proof of what the child ran.

## Worker Evidence

Research workers return an answer to their assigned question, source URLs or file locations, relevant facts and limitations, distinctions between observation and inference, unresolved conflicts, and missing coverage. Sol may organize and interpret evidence within scope; flag conclusions that depend on an unresolved premise for Astra. Astra verifies the evidence that drives its decision rather than repeating every collection step.

Implementation and review workers return changed files or actionable findings, relevant checks, unresolved issues, and material limits. A `sol-clerk` returns raw or mechanically transformed output, source locations, command exit statuses, requested counts or hashes, and failed or missing items.

## Installation

The [Codex assets](../../assets/gpt/codex/config.snippet.toml) provide worker defaults and role files. Install or update them only when the user requests configuration changes. Reuse that authorization without another confirmation. Merge with existing configuration, preserve unrelated settings, and verify installed paths and model availability. Editing or installing the skill alone does not activate its roles.

Record runtime checks in the task's artifact or installation report. Change packaged [source notes](source-notes.md) only when maintaining this policy, not during ordinary use.

## Verification

Check that ordinary research and summaries can resolve to Sol without mechanical-only restrictions, while consequential decisions and complex work explicitly resolve to Astra. Inspect mixed packets for a useful split, role references, selected effort, and the actual harness contract. Report material substitutions and unobserved runtime settings. Package checks establish consistency; they do not demonstrate a quality or cost gain.
