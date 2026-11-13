# Global instruction files

The author's user-scope instruction files for Claude Code and Codex, kept here so they have history and travel between machines. They hold only neutral operating rules: a subagent fan-out budget (Claude Code), a rule on scope and questions to the user (Codex), the default agent targets for skill installs, a default of verifying code with real runs, and the writing profile of `copydesk`. Anyone adopting the pack can copy them as a starting point and replace the parts that are personal taste.

| File | Loaded by | Profile delivery |
|---|---|---|
| [CLAUDE.md](CLAUDE.md) | Claude Code, as `~/.claude/CLAUDE.md` | `@~/.agents/skills/copydesk/references/writing-profile.md` import; the installed skill's file is read at session start |
| [AGENTS.md](AGENTS.md) | Codex, as `~/.codex/AGENTS.md` | A copy of the profile between `<!-- writing-profile:start -->` and `<!-- writing-profile:end -->`, refreshed by `sync_profile.py` |

## Setup on a machine

```bash
ln -sf "$(pwd)/docs/global-instructions/CLAUDE.md" ~/.claude/CLAUDE.md
ln -sf "$(pwd)/docs/global-instructions/AGENTS.md" ~/.codex/AGENTS.md
```

Run from the repository root of a clone that stays in place. As observed on 2026-09-24, Cowork sessions skip a symlinked `~/.claude/CLAUDE.md`; on a machine that uses Cowork, copy the file instead of linking it.

## When the writing profile changes

The profile's single source is `skills/minimal/copydesk/references/writing-profile.md`. After it changes and the skill is reinstalled, refresh the Codex copy and commit:

```bash
python3 ~/.agents/skills/copydesk/scripts/sync_profile.py docs/global-instructions/AGENTS.md
```

`--check` reports drift without writing. The Claude Code file needs no refresh because it imports the installed file.
