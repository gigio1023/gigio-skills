# Subagent fan-out budget

The main conversation may run up to 10 subagents at once. A subagent spawns at most 2 at once, at any depth, and prefers 1; extra work it does itself or runs in a second wave.

# Skill installs

When `install-skill-pack` installs or refreshes skills and the request names no agents, target these: claude-code, hermes-agent, opencode, cursor, codex, github-copilot, zcode, openclaw, grok.

# Code and writing

By default verify code with real runs and evaluation instead of new tests. The `coding-standards` and `copydesk` skills are there for substantial code or document work. The writing profile below applies to text a colleague will read.

@~/.agents/skills/copydesk/references/writing-profile.md
