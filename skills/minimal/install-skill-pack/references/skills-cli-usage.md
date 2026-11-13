# Skills CLI Usage

Target selection and the live CLI checks that keep installation behavior aligned with the npm release used for an operation.

## Resolve The Stable CLI

Treat npm's `latest` dist-tag as the highest stable release. Resolve it once and reuse the exact version for review, installation, listing, and removal commands:

```bash
skills_cli_version="$(npm view skills@latest version)"
case "$skills_cli_version" in
  ''|*[!0-9.]*|.*|*.) exit 1 ;;
esac
test "$(npx --yes "skills@$skills_cli_version" --version)" = "$skills_cli_version"
npx --yes "skills@$skills_cli_version" --help
```

The CLI runs under Node, and each release declares its minimum in `engines.node`; read it with `npm view "skills@$skills_cli_version" engines`. Stop and report an older Node rather than upgrading it.

Require live help to expose `add`, `--global`, repeatable `--agent`, repeatable `--skill`, `--yes`, `--copy`, and JSON listing. Stop rather than adapting an unknown interface from memory. Do not opt into a snapshot or prerelease unless the user explicitly requests that separate trust boundary.

An npm policy can refuse the newest release before this resolve step even runs. `min-release-age` in `~/.npmrc` rejects versions published within its window, and npm reports the refusal as `ETARGET / No matching version found ... with a date before <cutoff>`, which reads like the version does not exist. Read it as a policy block: resolve `latest`, then step down to the newest release older than the cutoff. Do not bypass the policy by pinning a snapshot, a tag, or a mirror.

## Select Target Agents

Choose the targets in this order and report which rule applied:

1. The agents the user names for this install.
2. A default agent list the user has recorded in their instruction files, such as a global `CLAUDE.md` or `AGENTS.md`. Apply its exclusions and additions as written.
3. The harnesses the CLI detects on this host. Each registry entry in the resolved release's `dist/cli.mjs` (in the npx cache) has a `detectInstalled` check, usually whether the harness's home directory exists, for example `CLAUDE_CONFIG_DIR` or `~/.claude` for Claude Code, `CODEX_HOME` or `~/.codex` for Codex, and `~/.cursor` for Cursor. Evaluate those checks read-only, propose the detected list once, and install after the user confirms or edits it. When nothing is detected, ask the user for targets instead of falling back to every agent.

Pass the chosen IDs as explicit `--agent` arguments. Never use `--all`, and never omit `--agent`: with `--yes` and no `--agent`, Skills CLI 1.7.1 installs to the detected agents plus every universal agent, and to every registered agent when it detects none. Validate IDs through the resolved CLI's registry when exposed; otherwise the explicit `add` command is the compatibility gate and must fail closed on an unknown ID. IDs can differ from display names: Hermes uses `hermes-agent`, not `hermes`.

### Example Target List

A user who installs to many harnesses might record a list like this nine-agent set as their default. The third column shows each target's global topology in symlink mode:

| Agent | CLI ID | Global topology in symlink mode |
| --- | --- | --- |
| Claude Code | `claude-code` | Agent-facing link below `CLAUDE_CONFIG_DIR/skills`, defaulting to `~/.claude/skills` |
| Hermes Agent | `hermes-agent` | Agent-facing link below `HERMES_HOME/skills`, defaulting to `~/.hermes/skills` |
| OpenCode | `opencode` | Universal canonical package under `~/.agents/skills` |
| Cursor | `cursor` | Universal canonical package under `~/.agents/skills` |
| Codex | `codex` | Universal canonical package under `~/.agents/skills` |
| GitHub Copilot | `github-copilot` | Universal canonical package under `~/.agents/skills`; its own CLI reads that directory as a personal source |
| ZCode | `zcode` | Agent-facing link below `~/.zcode/skills` |
| OpenClaw | `openclaw` | Agent-facing link below `~/.openclaw/skills`, falling back to `~/.clawdbot` or `~/.moltbot` homes |
| Grok (`Grok Build` in CLI output) | `grok` | Agent-facing link below `$GROK_HOME/skills`, defaulting to `~/.grok/skills` |

The CLI decides an agent is universal when its registry `skillsDir` is the canonical `.agents/skills`; when a target's topology matters for verification, read the registry from `dist/cli.mjs` in the npx cache instead of assuming this table.

## Preserve Symlink Mode

The normal non-interactive command omits `--copy`. When the selected targets span more than one registry `skillsDir`, the CLI keeps its default symlink mode: it copies the reviewed package once to the canonical `~/.agents/skills/<name>` directory, lets universal agents read that location directly, and links non-universal agent directories to it. When every selected target shares one `skillsDir` (only universal agents, or a single non-universal agent), Skills CLI 1.7.1 switches to copy mode even without `--copy`: the package lands directly in that directory, which is the canonical directory for universal agents and the agent's own skills directory otherwise, and no symlink is expected. For a single non-universal agent, read "canonical package" in the checks below as that agent's skills directory.

Read the installation summary. In symlink mode, require each selected universal agent under `universal:` and each other selected agent under `symlink →`; in single-directory copy mode, require every selected agent under `copy →`. A reported symlink fallback or a copy-only summary for targets that span more than one directory fails verification.

An agent may link its entire `skills` directory to the canonical directory instead of linking each skill. Accept either layout only when the agent-facing skill resolves to the same canonical package and at least the skill entry or its parent `skills` directory is a symbolic link.

## Verify Every Agent

For each selected ID, run the resolved version independently:

```bash
npx --yes "skills@$skills_cli_version" list \
  --global --agent <agent-id> --json
```

For every requested skill, require all of the following:

- the JSON entry's `name` matches and resolves to the canonical package;
- when the target harness is detected on the host, its display name appears in the entry's `agents` array; display names come from the registry's `displayName`, so Skills CLI 1.7.0 reports Grok as `Grok Build`;
- the canonical package contains exactly the reviewed files with matching contents and executable bits;
- in symlink mode, non-universal targets, such as Claude Code or Grok in the example table, resolve to that canonical package through a verified skill-level or parent-directory symlink;
- universal targets, such as Codex or Cursor, resolve through the universal canonical directory, so no separate per-agent symlink is expected.

Universal targets share one canonical directory. When such a harness is not installed or its configured home is absent, the CLI may accept the target and prepare the canonical package while omitting its display name from `agents`. Require that target in the successful installation summary, leave its config directory untouched, and report `canonical-ready; runtime discovery unavailable`. If the harness is present but omitted, treat that as failed discovery.

Do not infer runtime discovery from a directory that merely exists. The JSON `name` and canonical path prove package readiness; the `agents` member proves discovery only for a harness the CLI can detect.

## Check Lock Freshness

The lock file's `skillFolderHash` is the git tree hash of the skill folder, not a content digest of a tarball. `git rev-parse <rev>:<skill-path>` in the source repository therefore says whether an installed skill is current without diffing files: equal hashes mean the canonical package matches that revision exactly. Use it to decide whether a reinstall is needed and to confirm one afterwards; a mismatch with matching content means only the lock's source metadata is stale.
