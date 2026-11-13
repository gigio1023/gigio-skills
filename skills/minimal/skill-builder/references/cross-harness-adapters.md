# Harness Adapters

Use this before adding syntax or behavior that may belong only to Claude Code or Codex. The portable package uses the documented shared format. Optional adapters add native behavior without becoming required for the task's meaning or authority boundary. The [validator contract](validation.md) owns name, description, and metadata format rules; this file covers what differs between harnesses.

## Loading And Discovery

Both harnesses disclose progressively: metadata is visible for discovery, the full SKILL.md loads when selected, and supporting references and scripts are used as needed. The retrieval rules in SKILL.md therefore apply to both.

Both harnesses can shorten discovery text. Codex budgets its initial skill listing and can shorten descriptions when many skills are installed; Claude Code also truncates discovery text. Put the most discriminative trigger in the first sentence and do not spend the opening on a workflow summary.

Claude Code accepts optional frontmatter such as invocation control, tools, arguments, path filters, forked context, and hooks. Codex supports optional `agents/openai.yaml` policy, dependency, and interface metadata. These native features belong in the target adapter. Do not reject supported standard metadata merely because it is optional.

## Locations And Invocation

| Concern | Codex | Claude Code |
| --- | --- | --- |
| Repo skill | `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| User skill | `$HOME/.agents/skills/<name>/SKILL.md` | `$HOME/.claude/skills/<name>/SKILL.md` |
| Explicit invocation | `$name` or the current skill picker | `/name` or the current skill picker |
| Implicit invocation | Matches `description` | Matches `description` and optional Claude-only discovery metadata |

Keep canonical source in the repository's documented package location. Use an installer or a verified symlink or copy to expose it to both harnesses. Installation documentation may name these locations; the portable SKILL.md should not.

Do not tell an executing skill to invoke itself with `/name` or `$name`. Those forms are for user and harness entry, not the task workflow.

## Resources And Script Paths

The rules in SKILL.md for package-relative paths and prerequisites apply. The harness-specific part: do not require `${CLAUDE_SKILL_DIR}`, dynamic `!` command injection, a fixed Codex installation path, or the current project working directory in the portable path. Document commands from the skill root, or tell the agent to resolve the directory containing the active SKILL.md before running them.

Claude Code adapters may use `${CLAUDE_SKILL_DIR}` or dynamic injection. Codex adapters may declare dependencies in `agents/openai.yaml`. These can improve the native experience but must not be the only runnable path.

## Tools, Permissions, And Side Effects

Tool names and approval systems differ. Portable prose names the capability: read a file, search a repository, inspect a rendered artifact, query the configured source, or run a non-destructive test. Name an exact CLI or API only when it is part of the domain contract.

For MCP servers or connectors, describe the required service and capability. Put the exact namespace or dependency mapping in a harness adapter unless the package controls a stable, fully qualified tool contract.

Claude Code hooks, `allowed-tools`, and invocation-control metadata can enforce or narrow a workflow. Codex policies, approvals, config, and plugin metadata can do similar work. A prompt instruction is not mechanical enforcement. If an invariant must be guaranteed, ship a deterministic validator or hook adapter where supported and keep the portable authority rule as defense in depth.

External writes, destructive changes, purchases, secret exposure, and material scope expansion require explicit authority regardless of adapter availability.

## Subagents And Long-Running Work

Both harnesses can provide isolated workers, but availability, inheritance, permissions, nesting, and communication differ. A portable skill states:

- which work is independent;
- the evidence packet each worker returns;
- ownership boundaries for shared files;
- a sequential fallback;
- that delegation does not broaden authority.

Do not hard-code a built-in subagent type. Claude Code subagents can start with fresh context and preloaded skills; Codex subagents and threads follow the current surface's configuration. Put native orchestration details in a dedicated orchestration skill or harness reference.

For long work, specify sparse evidence-backed progress and a real completion condition. Harness-specific user-message or progress channels are adapters for that contract, not portable tool calls.

## Adapter Placement

- `SKILL.md`: shared domain workflow and safety and evidence contract.
- `references/`: domain detail and dated model or harness maintenance material.
- `.claude/` docs or plugin metadata: Claude Code installation and native extras.
- `.codex/` docs or `agents/openai.yaml`: Codex installation and native extras.
- Hooks or deterministic scripts: mechanical enforcement and repeatable checks.
- Dedicated routing or orchestration skills: model, effort, cost, and agent topology.
