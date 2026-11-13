---
name: coding-standards
description: >
  The owner's code defaults for writing, structuring, refactoring, or reviewing code in any language: module layout, explicit domain types, annotations, verification through real runs, and when a test is worth writing. Use for "how should I structure this", "split this module", "add type hints", "does this need tests", "구조 잡아줘", "리팩토링해줘", "타입 힌트 달아줘", "테스트 짜줘", "docstring 추가".
---

# Coding Standards

These are the owner's defaults where a frontier model would otherwise choose differently. The current request comes first, then the repository's written rules and consistent local conventions, then these defaults, which apply to new and changed code. Preserve existing public imports, accepted inputs, serialized values, and configured tooling unless the request covers changing them.

A change request includes its relevant local checks and nothing more: no repository-wide migration, cleanup, restructuring, or publication. A pre-existing problem met on the way is a follow-up in the summary. A review or diagnosis returns findings without edits.

## Structure

- Directories split by domain first, then by responsibility. Each file holds one responsibility a reader can state in a sentence. Around 500 handwritten lines is a prompt to split at a boundary you can name; a file past 1,000 lines deserves a reason in the summary.
- Abstractions follow triggers: no interface with one implementation, no repository over an ORM for CRUD, no service that only forwards, no DI container while the composition root fits on one screen. A port appears for a second implementation (a recorded or fake adapter counts), a second entry point, or a vendor library a check would otherwise mock.
- A "one-time operation" that needs no helper is a statement or two. A named responsibility called once is still a function; reading the phrase as "inline every single-caller step" produces the giant function it warns against.

## Types

- Model domain concepts as explicit types. A record that crosses a boundary is parsed once into a validated type. Closed sets are enums with explicit, stable values.
- Annotate wherever the language allows, including locals. The annotation is for a reader of a diff without a language server. Use the SDK's real client, request, and response types; add no cast or suppression just to make an annotation present.
- Python: uv for setup and dependencies (`uv add`, `uv sync`, `uv run`), never `pip install` as routine setup. Pydantic `BaseModel` is the default for application-owned structured data, including domain entities and values passed between phases. A library or SDK whose users must not inherit Pydantic, or a measured hot path, uses dataclasses or plain classes and says so beside the record.

## Documentation

Explain what the code cannot show: a function's contract (units, ordering, ownership, failures, side effects), a reason, a workaround, or a rejected alternative. A public name without documentation is a defect. Do not narrate statements or invent rationale.

A documentation-only request authorizes no executable change. For Python, check it after the edit, from inside the edited repository, with the script in this skill's directory:

```bash
python3 <skill-dir>/scripts/verify_doc_only_diff.py --base HEAD -- path/to/file.py
```

It fails on any executable AST change or changed tool directive. For another language, inspect the diff by hand and say so.

## Verification

- Verify through the real entry point (command, route, job, or public function) on fixed input, and leave something another person can rerun: the command, the input, and the output or log path.
- Report separately whether it runs, whether quality is established (learned or judged behavior needs an evaluation, not a few good-looking runs), and whether it is deployed. Name each check not run.
- Code that computes a view, leaderboard, or summary derives its values, ranks, and generated sentences from the same selection, and keeps missing, stale, and zero distinct instead of filling a zero.

## Tests

- The default is no new tests; verification comes from real runs. Add a test only for an essential contract that callers or stored data depend on, whose silent break is costly, and that a real run does not exercise cheaply: a parser's accept and reject boundary, a serialized format, an error mapping callers branch on.
- Write such a test from the contract, not from the implementation's current output, and drop any test that merely restates the code.
- Ask the user before removing or changing existing tests, or when a team policy or reviewer asks for tests. When CI enforces tests, write only what passing requires and say so.

## References

Read these only when the task needs the depth:

- [Python](references/python/overview.md): the Python form of these rules, linking project environment, types and enums, Pydantic, docstrings, errors, and measured reference repositories.
- [Architecture selection](references/architecture-selection.md): layouts, triggers for ports, the composition root, implementing from a design document, and agent-loop shape.
- [Functions and modules](references/functions-and-modules.md): the optional skeleton pass, size prompts, and moving code safely.
- [Correctness and verification](references/correctness-and-verification.md): error hierarchy, cleanup, cancellation, status reporting, and the full test policy.
- [Docstrings and comments](references/python/docstrings-and-comments.md): the contract map and the doc-only guard's limits.
