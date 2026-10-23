# Detailed Terms

[Terminology index](../../terminology.md) · [Anti-patterns](anti-patterns.md) · [References](references.md)

## subagent

**Meaning and status:** An agent that a lead agent spawns to handle a delegated task and whose result returns to the lead. Developer usage across harnesses: Claude Code ("Subagents are specialized AI assistants"), the Claude Agent SDK, Codex ("A delegated agent that Codex starts to handle a specific task"), and Cursor. Anthropic's multi-agent engineering post uses "subagents" for the same thing and "worker" informally.

**Use and distinctions:** The running instance, as opposed to its configuration (see subagent definition). "Worker" is an acceptable informal synonym in prose about a lead and its workers; "teammate" is Claude Code's word for a peer in an agent team, not a subagent.

**Reference:** [R001](references.md#r001), [R002](references.md#r002), [R003](references.md#r003), [R005](references.md#r005), [R013](references.md#r013).

## subagent definition

**Meaning and status:** The record that configures a subagent before it runs: model, effort, tools, permissions, and instructions. The Agent SDK names the type `AgentDefinition`; Claude Code and Cursor describe it as a Markdown file with YAML frontmatter; Codex calls it a custom agent file, role, or agent type.

**Use and distinctions:** Say "subagent definition" in harness-neutral prose, "agent file" when the sentence points at a path, "role" in Codex-specific text, and `agent_type` when naming a supported spawn argument that selects it. The routing skills ship definitions such as `opus-builder`, `astra-builder`, `sol-scout`, and `sol-clerk`. Their configured model and effort determine the assignment; the name alone does not verify the running model.

**Reference:** [R002](references.md#r002), [R004](references.md#r004), [R005](references.md#r005).

## task

**Meaning and status:** The unit of work a lead delegates to a subagent. Every harness document checked uses it: Claude Code ("a delegation message that summarizes the task"), Codex ("handle a specific task"), Cursor, Hermes ("Per-task model override"), Anthropic's research post ("research tasks").

**Use and distinctions:** Prefer "delegated task" on first use when the lead's own task is also in view. In Claude Code the historical tool name was `Task`; the tool is now `Agent`, so the noun no longer collides with a tool name.

**Reference:** [R001](references.md#r001), [R003](references.md#r003), [R005](references.md#r005), [R007](references.md#r007), [R013](references.md#r013).

## dispatch

**Meaning and status:** The act of handing a task to a subagent. Developer usage in the peer routing package AqueGen/model-routing ("Route every dispatch"); the routing skills use it for the one-line statement made before each spawn.

**Use and distinctions:** A dispatch statement identifies the delegated task, role when used, model, effort, configuration source, and observed runtime status. Its format follows the current routing skill. Do not use "dispatch" for the configured record or for the standing policy.

**Reference:** [R010](references.md#r010), [R011](references.md#r011).

## route

**Meaning and status:** A standing assignment of a class of work to a model at an effort. Research usage in the LLM routing literature (RouteLLM, Hybrid LLM), where a router assigns queries to models.

**Use and distinctions:** "The reviewer route runs Fable at `high`" describes policy; "this spawn's assignment" describes one decision. A proxy's "route string" (for example an opencodex `ocx-route`) is that product's identifier for a pinned model and effort, so name it "route string" when both senses are near.

**Reference:** [R008](references.md#r008), [R009](references.md#r009).

## tier

**Meaning and status:** A task-difficulty class used by a routing policy. The earlier pack policy used four classes: mechanical collection, bounded execution, judgment-adjacent support, and judgment core. Current GPT routing distinguishes ordinary research from complex judgment rather than treating all semantic work as one class. A fixed scope does not make implementation, diagnosis, or summarization mechanical. Developer usage in AqueGen/model-routing uses the same general noun ("Think in tiers, not model names").

**Use and distinctions:** Reserved for difficulty. Do not use "tier" for a model class or a service tier; say "model class" and "service tier" in full.

**Reference:** [R010](references.md#r010), [R011](references.md#r011), [R017](references.md#r017).

## install set

**Meaning and status:** One of this pack's two package directories. `skills/minimal/` holds the skills installed by default; `skills/additional/` holds the skills installed on request. A local name chosen by the maintainer on 2026-10-12.

**Use and distinctions:** Describes availability only. Whether and when a skill runs is still decided by its description and invocation settings, so a skill in the minimal set may still open only on an explicit request. Do not call a set a "tier"; that word is reserved for routing difficulty.

**Reference:** [R016](references.md#r016).

## role

**Meaning and status:** Codex's noun for a named subagent configuration: a `[agents.<name>]` table with a `config_file`, or a standalone role file under `agents/` that carries `name`, `description`, `developer_instructions`, and any `config.toml` key such as `model` and `model_reasoning_effort`. Source-specific to Codex.

**Use and distinctions:** Use in Codex-specific sections and asset names. Outside Codex, "subagent definition" is the neutral noun. CrewAI's `role` is a persona field and unrelated.

**Reference:** [R004](references.md#r004).

## effort floor

**Meaning and status:** Historical name for the pack's 2026-09-20 rule that every below-frontier model ran at `xhigh` by default. It is not a universal current requirement. Current routing respects explicit session settings and uses the defaults in the relevant model-routing skill without automatically lowering a frontier worker's effort.

**Use and distinctions:** A local policy name, not an industry term. Retain it when explaining the earlier policy; do not use it to override a current routing decision.

**Reference:** [R011](references.md#r011), [R015](references.md#r015).
