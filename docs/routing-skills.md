# Model routing skill composition

GPT-6.1 Sol handles most ordinary research, source selection, collection, organization, and summaries. GPT-6 Astra handles consequential judgment, synthesis for decisions, complex work, and final review. Independent research can run on Sol while Astra handles the decision it informs.

| Skill | Responsibility |
| --- | --- |
| `model-routing` | GPT and Fable model and effort policies, worker roles, and nested delegation |
| `orchestrate-subagents` | Decomposition, ownership, coordination, and synthesis |
| `small-model-handoff` | Fixed execution contracts for a deliberately selected mechanical or weaker executor |
| `codex-delegate` | External Codex mission launch, authority, runtime, and evidence |

GPT routing applies inside delegated missions and under non-GPT leads whenever the worker is a GPT model. The external `codex-delegate` mission still defaults to an Astra lead. Fable routing keeps its Anthropic choices separate. The [terminology index](../terminology.md) records shared orchestration vocabulary.

## Research And Decisions

| Packet | GPT route |
| --- | --- |
| Download specified URLs and return file hashes | Script or Sol 6.1 |
| Select sources and summarize a paper's methods and limitations | Sol 6.1 |
| Organize cited evidence and compare documented options | Sol 6.1 |
| Decide whether conflicting evidence justifies a direction | Astra |
| Diagnose a difficult failure, design or implement a system, conduct final review | Astra |
| Research followed by a consequential recommendation | Sol research plus Astra decision synthesis |

Sol may refine queries, select sources, interpret and organize evidence, and pursue routine follow-ups within the assigned question. It returns citations, limitations, contradictions, and missing coverage. Astra resolves consequential conflicts and verifies the evidence that drives a decision. A mixed packet stays with Astra when its difficult decisions cannot be separated usefully.

The mechanical-only contract remains available through `sol-clerk`. Its restrictions do not apply to `sol-scout` or every Sol worker, and ordinary research does not need `small-model-handoff`.

## Effort And Authority

Preserve an explicit user choice and the effective session effort where supported. The Codex assets default unnamed workers to Sol 6.1 at `xhigh`; Astra roles remain at `xhigh` and must be selected for complex work and consequential decisions. Fable assets preserve selected session effort; Sonnet and Opus retain their separate defaults.

Actual user budgets, concurrency limits, and scope remain binding at every delegation depth. Each dispatch states task, role, model, effort, configuration source, and whether runtime settings were observed. Selecting a role or accepting a request does not prove which settings ran. The routing change is an operating choice, not a measured cost or quality improvement.

## Adoption

Editing or installing a routing skill does not activate its role assets. Apply configuration changes only under the user's configuration grant and preserve unrelated settings. Current harness schemas control role fields, override support, and fork modes.

Add the current Sol 6.1 `sol-scout`, retain `astra-scout` for difficult investigation and decision synthesis, and preserve the Astra builder and judge roles. Replace any legacy GPT-6 Sol `sol-scout` with the new asset. The mechanical `sol-clerk` stays available. Update obsolete `sol-builder` references to `astra-builder`; retire obsolete files only within the installation grant. The repository assets and an installed runtime are separate verification targets.
