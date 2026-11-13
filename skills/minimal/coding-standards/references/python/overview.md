# Python

Read this before writing, structuring, typing, documenting, or reviewing Python, or before setting up a Python project or changing its dependencies. It gives the Python form of the skill's language-agnostic rules and says when to read each deeper Python reference. The repository's written rules still come first.

## Contents

- Repository constraints
- Project and environment
- Structure and modules
- Types and annotations
- Domain models and enums
- Docstrings and comments
- Errors and checks
- Reference files
- Gotchas

## Repository constraints

Read the project's Python support range, `pyproject.toml`, lockfile, and configured formatter, linter, type checker, and test runner before choosing syntax or tools. In a repository the user does not own, a convention the touched module follows consistently counts as a repository constraint for style-only rules such as annotating every local; mixed style there is still not an exemption. Report a conflict with an older Python or incompatible tooling instead of breaking support.

## Project and environment

Use uv's project workflow for setup and dependency changes: `pyproject.toml`, `uv.lock`, `uv add`, `uv sync`, `uv run`. `pip install` and `uv pip install` are not routine setup, a shortcut, or a retry after failed resolution; an exceptional environment needs a concrete reason and a reproducible dependency record. A new project starts on CPython's current bugfix line, or one line older when a dependency lags; 3.12 is the syntax floor for `type` aliases and type parameters, not a baseline. Keep runtime dependencies and development groups distinct. Read [project environment](project-environment.md) when setting up Python, changing dependencies, arranging groups, writing a single-file script, or adding security checks.

## Structure and modules

Directories are packages split by domain and then by responsibility, as the skill's structure rule says; [Python architecture](architecture.md) shows the layouts. New modules start private (`_name.py`), and `__init__.py` re-exports the public surface through `__all__` or `from ._x import Name as Name`; a public module keeps the names callers import while its machinery lives in a private module beside it. Exceptions, constants, and small shared types live in leaf modules that import nothing from the package. Read [Python functions and modules](functions-and-modules.md) before moving code or changing public imports, and for the Ruff gates a new project adopts.

## Types and annotations

Annotate functions, returns, model fields, attributes, module-level values, and local variables, even when the value makes the type inferable, unless the repository constraints above say otherwise. The local annotation is for the reader, not the checker: in a diff, a review, or a long function passing external-library values around, the declared type says what a name holds without a language server, and the need grows with every library involved. Use `dict[str, int]`, `list[Item]`, and `Item | None`, never `typing.Dict` or `typing.List`; import an SDK's real client, request, response, and stream types instead of `Any`; add no cast or suppression merely to make an annotation present. Past a handful of parameters, the rest are keyword-only. Read [types and enums](types-and-enums.md) for binding syntax, SDK types, and narrow exceptions.

## Domain models and enums

Pydantic `BaseModel` is the default for application-owned structured data: internal models, configuration, inputs, results, values passed between phases, domain entities and value objects. That default is for applications, services, tools, pipelines, and agents that already depend on Pydantic. Two cases differ and say so beside the record: a library or SDK whose users must not inherit a Pydantic dependency, and a measured hot path where construction or validation cost dominates; there, records are dataclasses, `NamedTuple`, or plain classes, which is why fastapi and attrs keep Pydantic at their boundary. Otherwise `TypedDict`, dataclasses, and dictionaries are not competing record representations: one model per meaning, no parallel layers. Services and resource owners stay ordinary classes. A closed string vocabulary that is persisted or transmitted is an `enum.StrEnum` with explicit values; provider-extensible strings stay open. Read [Pydantic integration](pydantic-integration.md) for this pack's choices on unknown fields, enum values, domain models, and compatibility.

## Docstrings and comments

A public name without a docstring is a defect; a private helper whose name and signature say everything needs none. Follow the repository's docstring convention (Google, NumPy, or Sphinx) and preserve tool directives such as `# noqa`, `# type: ignore`, `# ty: ignore`, and `# pragma: no cover` unless that tool's behavior is in scope. After a doc-only edit in a Git repository, run the guard from inside that repository, resolving the skill directory that holds `SKILL.md`: `python3 <skill-dir>/scripts/verify_doc_only_diff.py --base HEAD -- path/to/file.py`. It fails on any executable AST change or changed tool directive. Read [docstrings and comments](docstrings-and-comments.md) for the contract map, Python-specific contracts, patterns, the review checklist, and the guard's limits.

## Errors and checks

A package has one exception root, translated at one seam, chained with `raise ... from ...`. Run the repository's checks relevant to the changed behavior through `uv run` in uv-managed projects. Read [Python errors and checks](errors-and-checks.md) when changing exceptions, cleanup, or `asyncio` code, or when choosing check commands.

## Reference files

| File | Read or run when | Content |
| --- | --- | --- |
| [project environment](project-environment.md) | Setting up Python, changing dependencies, arranging groups, writing a single-file script, running fixes or formatting, adding security checks | uv workflow, version baseline, groups, locked runs, PEP 723 scripts, edited-file fix and format scope, optional security checks, exceptions |
| [Python architecture](architecture.md) | Creating a project or package, adding a port, wiring adapters, building an agent loop | Layouts, Protocol ports, composition root, Pydantic domain models, agent-loop sample, import-linter contracts |
| [Python functions and modules](functions-and-modules.md) | Writing a multi-phase function, moving code, choosing lint gates | Worked skeleton, private modules and re-exports, size evidence, Ruff block |
| [types and enums](types-and-enums.md) | Defining types, integrating a typed SDK, changing enum values | Annotation forms, representation table, stable enum values |
| [Pydantic integration](pydantic-integration.md) | Changing models, validation, or serialization | Unknown-field policy, enum values, domain models, the library exception |
| [docstrings and comments](docstrings-and-comments.md) | Adding, correcting, or reviewing docstrings and comments | Modes, contract map, Python-specific contracts, patterns, checklist, guard limits |
| [Python errors and checks](errors-and-checks.md) | Changing exceptions, cleanup, async code, or check commands | Exception root, chaining, cancellation, uv-run checks |
| [reference repositories](reference-repositories.md) | A rule needs its evidence, or a large unit needs a precedent | Nine measured packages, numbers, quoted explanations, what not to imitate |
| `scripts/verify_doc_only_diff.py` | After a doc-only edit with a Git base | AST and tool-directive comparison; `scripts/smoke_test.sh` exercises it |

## Gotchas

- Annotating every local is a readability rule, not a type-checking rule. Every measured library annotates 0% to 17% of locals, and the rule holds anyway.
- Pydantic-first is an application default. A library that must not impose the dependency, or a measured hot path, uses dataclasses or plain classes with the reason beside them; neither case transfers to the other.
- A docstring can be runtime data: an `argparse` description, a Pydantic schema description, a click help text. The doc-only guard cannot see those consumers.
- Incidental lower-level exceptions are not public guarantees; docstring examples may become doctests; comments can change what a tool does even though Python ignores them.
