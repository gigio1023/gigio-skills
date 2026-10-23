# References

[Terminology index](../../terminology.md)

<a id="r001"></a>
## R001 — Claude Code, "Create custom subagents"

- Anthropic; official product documentation.
- https://code.claude.com/docs/en/sub-agents
- Checked 2026-09-20 against Claude Code 2.1.278.
- Supporting passages: the definition of subagents, "Subagent files use YAML frontmatter for configuration", "Claude composes a delegation message that summarizes the task", the frontmatter table (`model`, `effort`), and the model resolution order.
- Used by: subagent, subagent definition, task; the "lane" anti-pattern (absence of the word, page text searched).
- Inspection status: full page fetched and searched.

<a id="r002"></a>
## R002 — Claude Agent SDK, "Subagents"

- Anthropic; official SDK documentation.
- https://code.claude.com/docs/en/agent-sdk/subagents
- Checked 2026-09-20.
- Supporting passages: the `AgentDefinition` type with `model` and `effort`, "Programmatic definition" and "Filesystem-based definition" headings, "spawn to handle focused subtasks".
- Used by: subagent, subagent definition.
- Inspection status: full page fetched and searched.

<a id="r003"></a>
## R003 — OpenAI Codex, "Subagents"

- OpenAI; official product documentation.
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- Checked 2026-09-20.
- Supporting passages: "A delegated agent that Codex starts to handle a specific task", custom agent files, the role-to-model guidance for GPT-5.6 Terra and Luna, the caution about parallel write-heavy workflows.
- Used by: subagent, task; the "lane" anti-pattern (absence).
- Inspection status: full page fetched and searched.

<a id="r004"></a>
## R004 — OpenAI Codex, "Config reference"

- OpenAI; official product documentation, cross-checked against the `codex-rs/core/config.schema.json` file at tag `rust-v0.154.0` in github.com/openai/codex.
- https://learn.chatgpt.com/docs/config-file/config-reference
- Checked 2026-09-20 against Codex CLI 0.154.0.
- Supporting passages: the `[agents]` table, `[agents.<name>]` custom role declarations with `config_file`, `default_subagent_model`, `default_subagent_reasoning_effort`; the schema's `AgentRoleToml` definition.
- Used by: role, subagent definition.
- Inspection status: page fetched; schema and source files read in a local checkout of the tag.

<a id="r005"></a>
## R005 — Cursor, "Subagents"

- Cursor; official product documentation.
- https://cursor.com/docs/agent/subagents
- Checked 2026-09-20.
- Supporting passages: "Each subagent is a markdown file with YAML frontmatter", the `model` string with bracketed options, "Agent proactively delegates tasks".
- Used by: subagent, subagent definition, task.
- Inspection status: page fetched and searched; the definition directory was not stated on the page.

<a id="r006"></a>
## R006 — OpenCode, "Agents"

- OpenCode maintainers; official documentation.
- https://opencode.ai/docs/agents/
- Checked 2026-09-20.
- Supporting passages: `agent.<name>` configuration, `mode: primary` and `mode: subagent`, provider passthrough keys such as `reasoningEffort`, `permission.task`.
- Used by: subagent definition; the "lane" anti-pattern (absence).
- Inspection status: page fetched and searched.

<a id="r007"></a>
## R007 — Hermes Agent, "Delegation" and "Kanban worker lanes"

- Nous Research; official documentation.
- https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation and https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes
- Checked 2026-09-20 for vocabulary; configuration keys (`delegation.model`, `delegation.provider`, `agent.reasoning_overrides`) observed in a local configuration the same day and not checked key by key against these pages.
- Supporting passages: "profile" for the configured agent, "Per-task model override", and the Kanban definition of a worker lane as "A class of process that the kanban dispatcher can route tasks to".
- Used by: task; the "lane" anti-pattern (the one harness usage, and its narrower meaning).
- Inspection status: pages fetched and searched for the nouns above; the configuration reference was not compared with the local keys.

<a id="r008"></a>
## R008 — RouteLLM

- Isaac Ong, Amjad Almahairi, and others (LMSYS); research paper, 2024.
- https://arxiv.org/abs/2406.18665
- Checked 2026-09-20.
- Supporting passages: router models that dynamically select between a stronger and a weaker model at inference time; the nouns "router", "route", and "model".
- Used by: route; the "lane" anti-pattern (literature nouns).
- Inspection status: abstract and framing sections read.

<a id="r009"></a>
## R009 — Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing

- Dujian Ding and others; research paper, ICLR 2024.
- https://arxiv.org/abs/2404.14618
- Checked 2026-09-20.
- Supporting passages: "a router that assigns queries" to a small or large model based on predicted quality gap; the nouns "router" and "routing".
- Used by: route.
- Inspection status: abstract and method sections read.

<a id="r010"></a>
## R010 — AqueGen/model-routing (community package)

- AqueGen; open-source Claude Code plugin; developer usage, authorship not independently verified.
- https://github.com/AqueGen/model-routing/blob/main/skills/model-routing/SKILL.md
- Checked 2026-09-20.
- Supporting passages: "Route every dispatch", "Think in tiers, not model names", the dispatch-logging hook; the word "lane" is absent from the package and "tier" is used throughout.
- Used by: dispatch, tier; the "lane" anti-pattern (peer usage).
- Inspection status: SKILL.md, agent files, hooks, and commands read; word counts taken over the repository.

<a id="r011"></a>
## R011 — Maintainer decision, 2026-09-20: retire "lane" and adopt the routing vocabulary

- Repository maintainer; dated local editorial decision made while reviewing the routing skills.
- Location: this record; applied in the routing skills, `docs/routing-skills.md`, and the terminology documents introduced in the same change.
- Decision: use subagent, subagent definition, task, dispatch, route, and tier as recorded in the index; do not use "lane" for those senses in this pack's prose; exceptions for quoted text, product syntax, and fields that own the word. Also confirms the "effort floor" policy name and meaning.
- Used by: dispatch, tier, effort floor; the "lane" anti-pattern.
- Inspection status: decision recorded from the maintainer's instruction; no external source.

<a id="r012"></a>
## R012 — matteoscurati/delegation-kit (community package, rejected as vocabulary authority)

- matteoscurati; open-source package for Claude Code and Codex.
- https://github.com/matteoscurati/delegation-kit
- Checked 2026-09-20.
- Status: rejected as an authority for wording. It uses "lane" heavily for configured subagents, but a large share of its recent commit history carries model-authorship trailers, and the source policy excludes model-written prose from terminology authority. Its role names (`astra-judge`, `terra-builder`, `luna-clerk`) were still useful as examples of the `<model>-<role>` naming shape.
- Used by: the "lane" anti-pattern (community usage with authorship judgment).
- Inspection status: agent files, Codex role files, and commit history read.

<a id="r013"></a>
## R013 — Anthropic, "How we built our multi-agent research system"

- Anthropic; engineering blog post, published 2025-06-13.
- https://www.anthropic.com/engineering/multi-agent-research-system
- Checked 2026-09-20.
- Supporting passages: an orchestrator that spawns "specialized subagents" with "specific research tasks"; scaling the number of subagents with task complexity.
- Used by: subagent, task; the "lane" anti-pattern (absence, page text searched).
- Inspection status: full page fetched and searched.

<a id="r014"></a>
## R014 — OpenAI Agents SDK, "Handoffs"

- OpenAI; official SDK documentation.
- https://openai.github.io/openai-agents-python/handoffs/
- Checked 2026-09-20.
- Supporting passages: handoffs "allow an agent to delegate tasks to another agent" and are represented "as tools to the LLM"; the configured unit is an `Agent`.
- Used by: the "lane" anti-pattern (absence, and "handoff" as the SDK's noun for transfer of control).
- Inspection status: page fetched and searched.

<a id="r015"></a>
## R015: Maintainer routing revision, 2026-10-06

- Repository maintainer; revision of the pack's model assignments.
- Location: [GPT routing](../../skills/minimal/model-routing/references/gpt/policy.md) and [routing overview](../routing-skills.md).
- Decision: GPT work defaults to Astra. Sol 6.1 handles only fixed mechanical work without semantic judgment. Bounded implementation, summaries, and diagnosis still require Astra. Explicit model and effort choices take precedence over package defaults; no automatic frontier-worker effort reduction.
- Used by: dispatch, tier, and the historical effort-floor entry. Existing field names remain unchanged.
- Inspection status: historical maintainer decision. [R017](#r017) superseded its GPT task assignments on 2026-10-24; explicit effort choices and the rule against automatic frontier-worker effort reduction remain compatible. This record makes no new claim about industry terminology or model benchmark performance.

<a id="r016"></a>
## R016: Maintainer layout decision, 2026-10-12

- Repository maintainer; decision to group bundled packages by install set instead of by source category.
- Location: [repository structure](../repo-structure.md) and the `skills/minimal/` and `skills/additional/` directories.
- Decision: the default install is the minimal set; the additional set is installed on request. The set names describe availability, not invocation. "Tier" stays reserved for routing difficulty.
- Used by: install set.
- Inspection status: maintainer decision; this record makes no claim about industry terminology.

<a id="r017"></a>
## R017: Maintainer routing revision, 2026-10-24

- Repository maintainer; revision of the pack's GPT task assignments, superseding [R015](#r015).
- Location: [GPT routing](../../skills/minimal/model-routing/references/gpt/policy.md) and [routing overview](../routing-skills.md).
- Decision: Sol 6.1 handles ordinary research, source selection, query refinement, collection, organization, cited summaries, and factual comparisons. Astra handles complex design, implementation, difficult diagnosis, consequential judgments, decision-oriented synthesis, and final review. Mechanical restrictions belong to the selected execution contract, not to every Sol assignment. Explicit model and effort choices take precedence over package defaults.
- Used by: dispatch and tier. Existing field names remain unchanged.
- Inspection status: maintainer decision applied to the current package; no quality or cost comparison is claimed.
