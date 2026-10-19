# Package ownership and source migration

Since 2026-10-12 this repository is the single pack: Gigio Pack and Research Credo were imported, their skills merged here, and both repositories archived (see [the 2026-10-12 mapping](#merges-renames-and-new-skills-on-2026-10-12)). The sections below record earlier moves between the three repositories in date order, and their ownership statements describe the arrangement at that time.

## Incoming from Gigio Pack

The following names and their helper resources move from Gigio's `skills/<name>/` into this repository's `skills/development/<name>/`:

- `orchestrate-subagents`
- `small-model-handoff`
- `fable5-model-routing`
- `git-worktree-setup`
- `commit-and-push`
- `draft-pr`
- `python-coding-standards`

The migration starts from Gigio main at `ada2fa6`. Earlier package history remains in Gigio. Orchestration and bounded handoff wording is adjusted to support the current decision round without requiring a fully fixed project plan.

## Outgoing to Research Credo

| Current source | Destination source |
| --- | --- |
| `skills/development/evaluation-operations/` | research-credo `skills/evaluation-operations/` |
| `skills/productivity/internal-source-research/` | research-credo `skills/internal-source-research/` |

The names and resources are preserved, including the reader-record refinements from the writer branch. No duplicate discoverable compatibility packages remain here. Research methods are independent of whether their result changes code.

## Renamed and removed on 2026-09-23

The owner stopped using GPT-5.6 models, and OpenAI publishes one prompting guide for the GPT-6 family.

| Before | After |
| --- | --- |
| `skills/development/gpt6-astra-prompting-guide/` | `skills/development/gpt6-prompting-guide/`, covering GPT-6 Astra and Sol |
| `skills/development/gpt56-sol-prompting-guide/` | Removed; GPT-6 Sol prompts use `gpt6-prompting-guide` |
| `gpt6-astra-model-routing` Codex roles `terra-scout`, `luna-clerk` | `sol-scout`, `sol-clerk`, both on `gpt-6-sol` |

The Skills CLI tracks installed skills by path, so an update does not rename them. After this change merges, install `gpt6-prompting-guide`, confirm it is discovered, and remove the old global names only when the owner asks: `npx --yes skills remove --global gpt6-astra-prompting-guide gpt56-sol-prompting-guide --yes`. Codex role files already copied to `~/.codex/agents/` keep their old names until they are replaced.

## Merged on 2026-09-29

`python-docstrings` was merged into `python-coding-standards`. Docstring and comment work reads the same repository conventions, carries the same review-versus-change authority boundary, and runs the same checks as any other Python change, and the coding-standards skill already owned "explain what the code cannot show". The merged description carries the docstring triggers ("docstring 추가", "주석 보강", "문서화해줘" on Python source).

| Before | After |
| --- | --- |
| `skills/development/python-docstrings/SKILL.md`, `references/contract-patterns.md`, `references/review-checklist.md` | `skills/development/python-coding-standards/references/docstrings-and-comments.md` |
| `skills/development/python-docstrings/scripts/verify_doc_only_diff.py`, `scripts/smoke_test.sh` | `skills/development/python-coding-standards/scripts/` (the guard now parses without type comments, normalizes `...` and `pass` bodies, and finds directives anywhere in a comment) |

After this change merges, update `python-coding-standards` and remove the old global name only when the owner asks: `npx --yes skills remove --global python-docstrings --yes`.

## Astra defaults and writing integration

GPT work now defaults to Astra. GPT-6.1 Sol is reserved for fixed mechanical collection or execution with no semantic decisions. Source selection, summaries, diagnosis, implementation, writing, and review stay with Astra even when their scope is bounded. `codex-delegate` uses the same default and applies the routing policy to any authorized internal subagents.

| Previous asset or behavior | Replacement |
| --- | --- |
| `sol-scout`, `sol-builder` Codex roles | `astra-scout`, `astra-builder` |
| `sol-clerk` on GPT-6 Sol | `sol-clerk` on GPT-6.1 Sol, mechanical work only |
| Unnamed Codex workers on Sol | Astra workers |
| `fable-lean-builder` with reduced effort | `fable-builder` with session effort |
| One fixed writing revision rule | New writing, local correction, or broad revision from the request |
| STE sentence and connective limits in the writing profile | Meaning-preserving clarity with language-appropriate sentences |

Changing these files does not change an active session. During an explicitly requested installation, reconcile previously copied role files with the selected role set, preserve unrelated custom definitions, and verify the actual model and effort at dispatch. A legacy role that remains installed can still pin an old model. Existing delegated runs retain their recorded model and lifecycle evidence when resumed; choose a new mission when a different lead model is needed.

Copydesk incorporates useful STE-inspired English clarity principles. The external `asd-ste100` skill is neither modified nor required. Update the installed copydesk package before refreshing any user-scope writing-profile copy with `sync_profile.py`. The source profile and repository instruction template change together; publication alone does not replace the live user files.

## Publication and installation

Merge the Research Credo destination first, then this change, then the Gigio source removals. The merged writer was installed and verified before the slop-aware-writing repository was archived on 2026-09-24. Review destination contents before removing source packages.

Publishing PRs does not install them. During a separately requested refresh, use `install-skill-pack` to select the available destination revision, add the moved names, and verify tracked repository/path metadata and the intended harness destinations. A same-name installed directory alone does not prove migration; old source metadata cannot follow a moved path automatically. Preserve customizations, avoid duplicate names, and never uninstall first or hand-edit installer locks.

The writer is `copydesk`, renamed from `technical-report-writing` on 2026-09-24 (reinstall under the new name and remove the old package); `share-internal-doc` was merged into it on 2026-09-24 as `references/sharing-and-delivery.md` and retired from Gigio Pack. `slop-aware-writing` and `korean-clarity` are merged into the writer; their repository was archived on 2026-09-24 and remains the MIT license source. See [writing composition](writing-skills.md).

## Install sets on 2026-10-12

Bundled packages moved from `skills/development/` and `skills/productivity/` into two install sets. `skills/minimal/` holds the default install and `skills/additional/` the on-request install. The packages imported from Gigio Pack (`3b206a1`) and Research Credo (`6217cd0`) on the same day were placed directly into these sets. `gigio-project-setup` was not imported as a package; its duty moved into `work-plan` in the merge below.

The Skills CLI tracks each installed package by repository and path, so `skills update` does not follow the move. During a separately requested refresh, use `install-skill-pack` with an explicit mapping from each installed name and tracked source to its new path, install the new paths by name, verify tracked metadata and harness destinations, and only then remove packages still attributed to retired sources.

## Merges, renames, and new skills on 2026-10-12

| Former names | Current name | Set | Change |
| --- | --- | --- | --- |
| `gigio-write-plan`, `gigio-execute-plan`, `gigio-review-results`, `gigio-project-setup` | `work-plan` | minimal | Write, execute, review, and project-context modes, each opened only on request; old plan files keep working |
| `deep-interview` | `interview` | minimal | Independent questions asked together in rounds; measurement questions become investigation items |
| `use-terminology`, `curate-terminology` | `terminology` | minimal | Read-only lookup first, curation only for gaps, disputes, or requests |
| `fable5-model-routing`, `gpt6-astra-model-routing` | `model-routing` | minimal | Dispatcher over two unchanged family policies; agent and role files keep their models and effort |
| `fable5-prompting-guide`, `opus5-prompting-guide`, `gpt6-prompting-guide` | `prompting-guide` | minimal | Dispatcher over three unchanged family guides |
| `cross-harness-skills` | `skill-builder` | minimal | Absorbed as conditional references |

New in the minimal set: `design-exploration`, `idea-critique`, `design-doc`, and `bug-diagnosis`. `literature-research` gains a mechanism-map mode, and `find-unknowns` is realigned to scan broadly for what neither side has noticed, lead with its own view, and ask the consequential questions together. The writing profile's "First screen" heading is now "Opening". Concepts adapted from mattpocock/skills (`49dd158`, MIT License, Copyright (c) 2026 Matt Pocock) are rewritten and credited in each skill's source notes.

The repository was renamed from `gigio1023/agent-skills` to `gigio1023/gigio-skills` on the same day. GitHub redirects the old URL, but packages installed from it keep the old source in the Skills CLI lock until they are reinstalled from the new name.

Descriptions named their former names until 2026-10-12; since then former names live only in this document, and a request that uses one is routed by the tables here. Installed copies under the former names are not updated by `skills update`; during a requested refresh, install the current names, verify them, then remove the former names. Codex role files and agent definitions already installed from the routing skills keep working, but their text names the former routing skill until they are reinstalled.

## Coding standards, review, and load testing on 2026-10-12

| Former name or set | Current name or set | Change |
| --- | --- | --- |
| `python-coding-standards` | `coding-standards` | Language-agnostic code and test principles; Python moves to `references/python/` |
| `insight-dashboard`, `frontend-design` in additional | minimal | Report and dashboard front ends are recurring work |
| None | `review-panel` | Separate reviewers, usually from different model families, with findings judged by evidence |
| None | `load-testing` | Load and capacity tests of services and model endpoints |

`interview` now applies the unknowns lens inside an interview (the user's current understanding, a first-round blind-spot scan, tacit criteria shown as options), while `find-unknowns` stays the quick standalone pass. During a requested refresh, install the current names, verify them, then remove `python-coding-standards`.

## Listing budget and goal prompts on 2026-10-12

| Former name or text | Current | Change |
| --- | --- | --- |
| `goal-prompting` in additional | `prompting-guide/references/goal-mode/` | Goal mode guidance is a reference the prompting guide loads on request; the package is removed |
| "Formerly …" clauses in descriptions | This document | Former names left the descriptions |
| Ten descriptions over 1,000 characters or carrying former names | Shortened under the description rule in `AGENTS.md` | What the skill does, the phrases that call it, and a NOT clause |

Claude Code lists skills within about 1% of the model's context window and Codex within 2%. When the listing overflows, Claude Code drops the descriptions of the least-used skills and Codex shortens descriptions and then omits skills. The pack's descriptions totaled 31,483 characters across 48 skills before this change. During a requested refresh, reinstall the changed skills, verify them, then remove `goal-prompting`.

## Vulnerability reporting on 2026-10-14

| Former name or set | Current name or set | Change |
| --- | --- | --- |
| None | `vuln-report` in additional | Vulnerability reports, advisories, and their evidence packages, with rules sourced from a survey of published reports, maintainer policies, and record formats |

`copydesk` keeps general writing; `vuln-report` owns report structure, evidence, severity and range decisions, and disclosure for security findings. It sits in the additional set because the minimal-set test in `AGENTS.md` asks whether a kind of the maintainer's work recurs without an owner, and that has not been asserted for security reporting. Install it by name when needed.

## Zcode CLI on 2026-10-14

`zcode-cli` joins the additional install set. It owns official Zcode CLI discovery, authorized API-key setup, model and reasoning selection, task execution, and session continuation. API-key setup distinguishes Coding Plan from the standard API, includes a private provider profile, and checks the resolved session selection separately from a successful response. `read-agent-sessions` continues to own reading stored conversations for another agent. The package supports any model in the runtime catalog and defaults to GLM-5.3 at max effort when the user names no model. Publication does not install the skill or change Zcode authentication.

## Spot GPU evaluation on 2026-10-19

| Former name or set | Current name or set | Change |
| --- | --- | --- |
| None | `spot-gpu-evaluation` in additional | Operating LLM and agent evaluations on preemptible or spot GPU instances: placement, restart path, restarter and holds, guest lifecycle units, durable publication, preemption-aware scoring, monitoring, and cost |

`evaluation-operations` keeps campaign state across runs, `ml-experiment` keeps training and serving-configuration comparisons, and `load-testing` keeps capacity under load; the new skill owns the node-level operation of an evaluation on capacity the provider can reclaim. It sits in the additional set because it needs a cloud account with spot GPU capacity, which an installer may lack. Install it by name when needed.
