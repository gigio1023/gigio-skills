# Python Project Environment

Read this when setting up Python, changing dependencies, writing a single-file script, running fixes or formatting, adding security checks, or arranging local and CI commands. Prefer uv project management; this is not a pip-based installation recipe.

## Project files and scope

For new Python projects, start on CPython's current bugfix release line, or one line older when a required dependency lags. 3.12 receives security fixes only; it remains the syntax floor for `type` aliases and type parameters, not a new-project baseline. Initialize only inside the intended project, and keep `project.requires-python`, the selected development interpreter, and CI consistent. `uv init` creates a packaged `src/<name>/` layout; `uv init --no-package` gives a flat layout for a tool that is never installed as a distribution. Choose by whether anything will import the project, not by habit. In an existing project, inspect its metadata, lockfile, workspace, and automation before changing them; an incidental code fix does not authorize replacing its package manager or dropping older Python support. Identify a conflicting requirement explicitly.

Use `uv python pin <version>` when the project should persist its development interpreter in `.python-version`. The supported range in `requires-python` and the selected development version serve different purposes; `--python` on one command does not itself pin later commands. Do not assume the newest local interpreter matches the project's intended test runtime.

Use `pyproject.toml` for declared dependencies and configuration, and generate `uv.lock` through uv. Keep the lockfile in version control for the managed project; do not commit `.venv/`. Do not hand-edit resolved packages in the lockfile. Add or remove dependencies through `uv add` and `uv remove`, and keep their constraints deliberate rather than upgrading unrelated packages.

## Dependency groups

Put runtime requirements in `project.dependencies` under `[project]`. Use `[dependency-groups]` for tools used to develop and check the project, such as `test` and `lint`, adding separate groups only when they serve distinct commands or environments. Do not put development-only tools into runtime requirements or publish them as optional features by accident. `[project.optional-dependencies]` is for extras that consumers select, not the default home for test and lint tools.

For a project that uses pytest and Ruff, the relevant operations are:

```bash
uv add pydantic
uv add --group test pytest
uv add --group lint ruff
uv sync --group test --group lint
uv run --locked --group test pytest
uv run --locked --group lint ruff check .
```

These are examples, not a requirement to add those tools to an existing project. Reuse its chosen test and lint tools. A `dev` group may include `test` and `lint` with `{ include-group = "test" }` and `{ include-group = "lint" }`. Decide whether groups are selected explicitly or through `tool.uv.default-groups`; keep local and CI commands consistent. Review resolution across groups instead of bypassing incompatibilities with an environment-only install.

## Reproduce the environment

Run project commands through `uv run` and synchronize with `uv sync`. These can update the environment and lockfile; they are not read-only diagnostics. Once dependency changes are intentional and resolved, use `uv lock --check` and locked runs in CI to fail on stale metadata instead of silently relocking. `--frozen` skips the freshness check and is not equivalent to `--locked`.

Use only the groups needed by the environment. When a deployment should exclude every development group, account for configured defaults rather than assuming `--no-dev` disables all of them. Do not let a test-only dependency become an undeclared runtime dependency because it happens to exist locally.

## Single-file scripts

A script that is one file and that nothing imports declares its Python range and dependencies inline, in a PEP 723 `# /// script` block at the top of the file, instead of in a `pyproject.toml`. This is the script layout [Python architecture](architecture.md) shows; once the script gains a second module, an importer, or a second entry point, move it into a project.

```bash
uv init --script fetch_report.py --python 3.14   # writes the inline block
uv add --script fetch_report.py httpx           # adds to the block's dependencies
uv lock --script fetch_report.py                # optional: writes fetch_report.py.lock
uv run --script fetch_report.py
```

The inline block is the script's declaration, so a missing dependency goes into it, never into a `uv run --with` flag. A shebang of `#!/usr/bin/env -S uv run --script` lets the file run on its own. A script with inline metadata gets its own environment even inside a project directory, and uv ignores the project's dependencies for it; a script that needs the project's code belongs in the project as an entry point or a module. When the script's runs must reproduce, commit its `.lock` file beside it and run with `uv run --locked --script`, which fails on a stale lock instead of relocking.

## Fix and format only what you edited

Run `ruff check --fix` and `ruff format` on the files you edited, not the whole tree, unless the project already keeps every file clean. Check first with `ruff format --check .` and `ruff check .`: if they report only the files you touched, or nothing, a project-wide run changes nothing else and is fine. If they report files nobody touched, a project-wide run would bury the change in unrelated edits and blame noise, so pass the edited paths instead, for example the Python files from `git diff --name-only --diff-filter=d <base> -- '*.py'` to `uv run --locked --group lint ruff format` and to `ruff check --fix`. When the project configures no formatter, do not add one as a side effect. When an edited file was never formatted, formatting it rewrites lines you did not change; format only the changed region with `ruff format --range <first>-<next> <file>`, where `<next>` is the line after the last changed line because a bare line number means that line's first column, or leave the file unformatted and say so. A repository-wide formatting or fix pass is its own change, made on request. Unsafe fixes stay manual, as [errors and checks](errors-and-checks.md) says.

## Optional security checks

A project that publishes packages, runs CI on pull requests, or handles credentials can add the checks below. They are options to offer, not defaults for every project: add one when the user asks or the project's policy calls for it, keep the tools the project already runs, and put each in a dependency group, a pre-commit hook, or a CI job, never in runtime dependencies.

| Check | What it finds | Where it runs |
| --- | --- | --- |
| `pip-audit` | Known vulnerabilities in the locked dependencies | CI, on demand |
| `zizmor` | GitHub Actions risks: template injection, dangerous triggers, broad permissions, unpinned actions | CI, pre-commit |
| Dependabot or Renovate | Outdated and vulnerable dependencies, as update pull requests | Scheduled |
| `detect-secrets` | Credentials committed to the repository | Pre-commit, CI |

```bash
uv export --format requirements.txt --no-emit-project --locked -o requirements-audit.txt
uvx pip-audit -r requirements-audit.txt --disable-pip
uvx zizmor .github/workflows/
uvx detect-secrets scan > .secrets.baseline   # then the pre-commit hook checks against it
```

Dependabot reads `.github/dependabot.yml`; the `uv` ecosystem updates `uv.lock`, and the `github-actions` ecosystem updates pinned actions. `uv audit` covers the same ground as pip-audit but was still experimental in uv 0.12.9 on 2026-11-04. Pin these tools' versions in CI as the project pins its other tools. Fix a finding or record why it does not apply; an ignore entry in the audit configuration, a zizmor suppression, or a new baseline entry with no reason beside it lowers the bar the check exists to hold.

## Exceptional environments

Do not use `pip install` or `uv pip install` for ordinary setup, dependency changes, or failed-resolution recovery. Missing uv, a resolver error, and convenience alone do not justify either command. Check whether a compatible uv project workflow is available; if setup authority or a prerequisite is missing, report it rather than silently installing a global tool.

A narrowly scoped external environment that cannot consume the project workflow can justify an exception. State the concrete restriction and keep a reproducible dependency source, preferably derived from the project metadata and lockfile, instead of making ad hoc installs the source of truth. Do not use transient `uv run --with` dependencies to conceal missing declarations for normal project commands.

## Sources

Checked 2026-09-29 against uv 0.12:

- [uv projects](https://docs.astral.sh/uv/guides/projects/): project files, interpreter selection, and command execution.
- [uv dependency management](https://docs.astral.sh/uv/concepts/projects/dependencies/): project requirements, extras, groups, includes, and default groups.
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/): environment updates and locked versus frozen behavior.
- [Python release cycle](https://devguide.python.org/versions/): which lines receive bugfix and security releases.

Checked 2026-11-04 against uv 0.12.9 and Ruff 0.16.5, with each command above run on a fixed sample project and script:

- [PEP 723](https://peps.python.org/pep-0723/) and [uv scripts](https://docs.astral.sh/uv/guides/scripts/): inline script metadata, script locks, and project isolation.
- [Ruff formatter](https://docs.astral.sh/ruff/formatter/): `--check`, `--diff`, and `--range`.
- [pip-audit](https://github.com/pypa/pip-audit) 2.10.1, [zizmor](https://docs.zizmor.sh/) 1.32.0, [detect-secrets](https://github.com/Yelp/detect-secrets) 1.5.0, and the [Dependabot options reference](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference) for the `uv` and `github-actions` ecosystem values.
- The script and security-tool selection follows the `modern-python` plugin in [trailofbits/skills at 711af09](https://github.com/trailofbits/skills/tree/711af09/plugins/modern-python) (CC-BY-SA-4.0); its ideas are rewritten here, not its text. Scoping fixes and formatting to edited files follows the `ruff` skill in [astral-sh/claude-code-plugins at f3ce88a](https://github.com/astral-sh/claude-code-plugins/tree/f3ce88a/plugins/astral/skills/ruff) (MIT or Apache-2.0).

Astral publishes its own `uv`, `ruff`, and `ty` skills in [astral-sh/claude-code-plugins](https://github.com/astral-sh/claude-code-plugins); they cover commands and migration, and the `uv` skill permits `uv pip install` for legacy workflows where this pack does not. The current-line Python baseline, uv-first setup, explicit group selection, and the restricted pip exception are this pack's defaults, adjustable by the user's own instructions, not universal Python requirements.
