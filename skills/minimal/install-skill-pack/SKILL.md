---
name: install-skill-pack
description: >
  Install or refresh skills globally from a Git repository or revision with
  the Skills CLI for Claude Code, Codex, Cursor, and other Skills CLI agents,
  then verify revision, installed content, symlinks, and discovery per agent.
  Resolves name collisions with a recorded prefix rename that later refreshes
  reapply. Use for "install this skill pack", "refresh my skills", "스킬 설치해줘".
---

# Install Skill Pack

Install skills from a user-selected Git repository. Install globally unless the user explicitly asks for a project-local install. Let the CLI manage the canonical package under `~/.agents/skills` and the agent-facing links.

## Targets

Choose target agents in this order and report which rule applied: the agents the user names for this install; otherwise a default agent list recorded in the user's instruction files; otherwise the harnesses the CLI detects on this host, proposed once for the user to confirm. Pass each target as an explicit `--agent`. Never use `--all` and never omit `--agent`: without it the CLI picks targets itself, and when it detects no harness it installs to every agent it knows. [Skills CLI usage](references/skills-cli-usage.md) covers detection, agent IDs, and per-agent topology.

## Prerequisites and CLI

Node with npm and npx at the version the resolved Skills CLI release declares in `engines.node`, `git`, `python3` for the rename script, and network access to the repository host and the npm registry. If a tool is missing or too old, stop and report it rather than installing it.

Resolve npm's stable `skills@latest` once per operation and reuse that exact version for every command; check its `--version` and live `--help` as in the CLI-usage reference, and stop rather than adapting an unknown interface from memory. An npm `min-release-age` policy can refuse a young release with an `ETARGET / No matching version found` error that reads like a missing version; step down to the newest release the policy allows instead of bypassing it. Running the CLI executes the npm publisher's code; reviewing skill packages does not cover that.

## Revision

Pick one mode and prepare a disposable review checkout as in [revision selection](references/revision-selection.md):

- **Default:** no revision input. Keep the CLI source bare (`owner/repo`) so it follows the remote's default branch without assuming `main`.
- **Branch:** append `#<branch>` to the CLI source. Never `@<branch>`; the CLI reads `@` as a skill filter.
- **Commit:** require a full commit ID, fetch it into a detached checkout, and install from that local path; remote `#ref` does not reliably accept a raw commit ID.

Record the checked-out commit as `reviewed_sha`. Immediately before installing from a default or named branch, confirm the remote still points to `reviewed_sha`; if it moved, review the new snapshot.

## Review

Locate each requested skill by its frontmatter name and require exactly one matching package per name. If a name is absent, stop rather than switching revisions, repositories, or local checkouts. Use `--skill '*'` only for an explicitly requested complete pack. A repository may group packages into install-set directories such as `skills/minimal/`; for a set, list the package names there and pass each as `--skill`, keeping the repository as the source.

Scale the review to the source. For the owner's own repositories (`gigio1023/*`), check what changed since the installed revision (the lock's `skillFolderHash` is the Git tree hash, so `git rev-parse <rev>:<skill-path>` shows which packages changed) and look closer at new or changed scripts, hooks, and network or credential access. For third-party sources, read each selected package in full and apply [source review](references/source-review.md); record a `pass` or `block` per skill. Third-party scanner results are optional and neither pass nor block on their own.

## Renames

Compare the selected names with installed global skills from other sources and with the target harnesses' built-in commands. When `~/.agents/skill-pack-renames.json` has an entry for this source, or a collision needs one, follow [renames](references/renames.md): the user decides which side takes a prefix, and `scripts/rename_skills.py` writes the renamed and rewritten packages for review.

## Install and Verify

```bash
npx --yes "skills@$skills_cli_version" add \
  "$install_source" \
  --global \
  --agent <agent-id> \
  --agent <agent-id> \
  --skill <skill-name> \
  --yes
```

Omit `--copy`; the normal path is one canonical copy plus agent symlinks, and the CLI switches to copy mode on its own when every target shares one skills directory. With renamed packages, run the command twice: once from `install_source` for the `unchanged` packages and once from the script's output directory for the `written` ones, by their new names.

For each target, run `skills list --global --agent <id> --json` and check the name, the canonical path, the agent's display name in `agents` for a detected harness, canonical content against the reviewed revision, and the link topology, as the CLI-usage reference describes. An absent universal harness can be canonical-ready without appearing in `agents`; report that instead of creating its config directory. If an install result is uncertain, inspect canonical content and links before rerunning. Remove the review checkout and renamed output only after verification passes.

## Updates

Bare sources and named branches follow their remote and need review again after a commit change. Exact-commit and renamed installs come from a temporary local path, so `skills update` skips them; refresh them by running this skill on the source again. Only an explicit request to update every tracked global skill authorizes `npx --yes "skills@$skills_cli_version" update --global --yes`, which can fetch unreviewed sources; say so beforehand.

## Gotchas

- Do not pass CLI flags through a shell variable. Zsh does not word-split an unquoted variable, so a flags string arrives as one argument; the CLI ignored it, installed project-locally, and still printed `Installed`. Write flags literally and confirm the mode with the per-agent listing.
- An installed canonical package may have been edited in place by another session or harness. Before overwriting one, compare it against the reviewed revision and surface material diffs instead of silently discarding them.
- Global installation does not authorize deleting unrelated or stale skills; remove those only when the user names them.

Report the CLI version, source and revision, the target-selection rule, installed skills per agent with their verification status, any renames, and anything blocked with the finding behind it.
