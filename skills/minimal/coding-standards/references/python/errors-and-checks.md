# Python Errors and Checks

Read this with [correctness and verification](../correctness-and-verification.md) when changing Python error handling, resource cleanup, `asyncio` code, or the commands that check a Python change. The rules themselves are language-agnostic; this file gives their Python form.

## Errors and resources

- **One exception root.** A package defines one exception class that its errors subclass, by what the caller would do differently. Use `TypeError` and `ValueError` for plain misuse of a function and the package's own errors for the package's logic. Carry the facts a caller acts on as attributes (`status_code`, `path`), never as message text to parse.
- **Chaining.** When wrapping, preserve the cause with `raise PackageError(...) from err`. Translate transport exceptions in one function or one context manager, as httpx does in `map_httpcore_exceptions()`.
- **Retries.** A retry loop catches a named tuple of transient exception types, not `Exception`, because the broad form also retries programming errors.
- **Cleanup.** Release acquired resources through a `with` statement, `contextlib.ExitStack`, or a `finally` block. Incidental lower-level exceptions are not public guarantees; document only the exceptions callers are meant to handle.

## Cancellation and concurrency

`asyncio.CancelledError` inherits from `BaseException`, so catching `Exception` does not cover it. Cleanup must still run and cancellation should normally propagate; structured concurrency depends on this. `TaskGroup` cancels sibling tasks when a member fails with a non-cancellation exception; `gather` can suit operations whose failures are collected independently, and neither is a universal replacement for the other. Do not block an event loop with synchronous I/O; `asyncio.to_thread` moves blocking I/O off the loop but does not accelerate CPU-bound Python code.

## Checks

Discover commands from project instructions, CI, and `pyproject.toml`. In uv-managed projects, run them through `uv run` with the declared groups, for example `uv run --locked --group test pytest` or `uv run --locked --group lint ruff check .`; group setup is in [project environment](project-environment.md). Keep one configured formatter and the repository's selected type checker (mypy, pyright, or ty); do not migrate checkers or impose `--strict` as a side effect. Do not apply Ruff's unsafe fixes automatically. In a project whose tree is not already clean, run fixes and the formatter only on the files you edited; the procedure is in [project environment](project-environment.md#fix-and-format-only-what-you-edited).

New and changed declarations carry explicit types, including locals and SDK objects, unless the touched module in a repository the user does not own consistently follows another convention; inferred-type acceptance by a checker does not meet this rule. The annotation rules are in [types and enums](types-and-enums.md).

When pytest is the selected runner and an essential contract needs a test, follow pytest's layout and import guidance and the repository's existing fixtures. Fakes at I/O seams are Protocol implementations in the test module, not `unittest.mock` patches of internal helpers.

## Sources

Checked 2026-09-29:

- [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html): exception handling, chaining, cleanup, and context managers.
- [Python task cancellation and concurrency](https://docs.python.org/3/library/asyncio-task.html): cancellation propagation, `TaskGroup`, `gather`, and thread offloading.
- [Ruff configuration](https://docs.astral.sh/ruff/configuration/): project settings and discovery.
- [Ruff fix safety](https://docs.astral.sh/ruff/linter/#fix-safety): fixes whose behavior may change runtime semantics.
- [pytest good integration practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html): test layout and import behavior when pytest is the selected runner.
- The exception-hierarchy and single-seam practice is measured in [reference repositories](reference-repositories.md).
