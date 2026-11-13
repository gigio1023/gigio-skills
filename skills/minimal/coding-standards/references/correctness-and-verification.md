# Correctness and Verification

Read this for changes to errors, resources, concurrency, or project documentation, for deciding how a change is verified and reported, and for deciding whether a test is warranted. Use the repository's existing test and documentation conventions where they exist. Python mechanics (exception chaining, `asyncio` cancellation, `uv run` checks, Ruff and pytest) are in [Python errors and checks](python/errors-and-checks.md).

## Contents

- Documents outside the code
- Errors and resource ownership
- Concurrency and cancellation
- Verification through real runs
- Status report and completion
- Tests
- Configured checks
- Sources

## Documents outside the code

Policy may live outside code. Put other material under `docs/` only when source-local explanations cannot convey it or a reader needs a view assembled across multiple files, such as a cross-component lifecycle or an external operational constraint. Maintain one useful explanation, link to authoritative symbols, and avoid copying code, signatures, schemas, or per-file walkthroughs. Do not create a Markdown implementation report for each task. When the change invalidates an existing explanation, update or remove that explanation in scope rather than leaving stale claims or adding a second account.

## Errors and resource ownership

Give a package one error root and subclass it, or name its cases, by what the caller would do differently, not by where the error was raised; a case raised from more than one place earns a named case. Errors carry the facts a caller acts on as fields (`status_code`, `path`, the offending value), never as text to parse. Use the language's built-in errors for plain misuse of a function, and the package's own errors for the package's logic. Translate transport and library errors into the package's errors at one seam, such as the single function that performs a request or the scoped wrapper around a driver call, so no other layer needs to know the driver's error types.

Catch the specific failures the current layer can handle. Translate an error where it becomes meaningful to a caller, preserve its cause when wrapping it, and keep cancellation or programming errors from becoming an ordinary success result. A broad catch is appropriate only for an intentional boundary with a defined recovery, reporting, or re-raise policy. A retry loop catches a named set of transient error types, not every error, because the broad form also retries programming errors.

The code that acquires a resource makes its release visible through the language's scoped-resource construct or a reliable cleanup path. A change to cleanup behavior is checked on failure, not just on successful completion. Do not scatter logging and re-raising through every layer; avoid duplicate reports and sensitive payloads in logs or public errors.

Retry only operations whose replay semantics are understood, with a bounded policy appropriate to the dependency. Do not retry deterministic schema failures or non-idempotent effects merely because the error is catchable.

## Concurrency and cancellation

Distinguish cooperative cancellation from operational failure. Cleanup must still run when work is cancelled, and cancellation normally propagates rather than becoming a result. Choose concurrency semantics before choosing an API: whether one member's failure cancels its siblings, or failures are collected independently, is a decision about the operation, not a library preference. Bound external waits and concurrency when the operation requires it, and do not block an event loop with synchronous I/O. Offloading to threads does not automatically accelerate CPU-bound work.

## Verification through real runs

Verify a change through observable effects: the real entry point a caller uses (the command, route, job, or public function) on fixed input, leaving an artifact another person can rerun and compare, such as the command, the input file or fixture, and the output, log, or report path.

| Changed surface | Real-run check |
| --- | --- |
| Public imports or entry points | Existing consumer imports still resolve; the entry point's behavior is preserved on the same input |
| Validation or parsing | Accepted and rejected inputs, including source-specific coercion and unknown-field policy |
| Serialized or persisted data | Actual output values, aliases, omissions, unknown-field retention, and compatibility with existing fixtures |
| Error translation | The error type and the caller's resulting behavior, not incidental wording unless wording is public behavior |
| Resource or concurrency lifecycle | Failure and cancellation release owned resources and preserve intended cancellation |
| Module extraction | The same output through a stable caller-facing boundary on the same input, plus relevant import checks |
| Agent loop | An episode against recorded or fake tool adapters: budget and termination reasons, permission refusals, and the trajectory record |

For a bug fix, reproduce the failure before the fix when feasible and rerun the same reproduction after it. When code being moved is insufficiently covered, compare its caller-facing entry point on the same fixed input before and after the move. An existing output is evidence of current behavior, not proof that the behavior is required. Keep a fixture when the request, documented contract, or a known consumer establishes what must remain stable.

Keep fixtures deterministic and isolated; do not require a live service when a local run against a recorded or fake adapter proves the relevant behavior. Live, paid, or state-changing runs need the authority applicable to that environment.

Real-run checks establish that code runs and behaves as specified on the inputs tried. They do not establish the quality of learned or judged behavior, which needs an evaluation through the production interface, and they do not establish performance: latency and throughput from a functional run or an evaluation run are unloaded numbers, not capacity or latency under load.

## Status report and completion

Report three things separately, because each can be true while the others are not:

- **Runs:** the real-run checks and configured checks that ran, with their results and the rerunnable artifact.
- **Quality established:** for learned or judged behavior, the evaluation and its result, or "not evaluated". A few runs that looked right are not an evaluation.
- **Deployed:** where and at which revision, or "not deployed".

Evidence before claims. State only what a check you ran shows; name each check not run and why; report a missing prerequisite or a pre-existing failure distinctly from a passing result. "Should work", "looks correct", or a passing type check does not stand in for a run.

## Tests

The default is no new tests. Verification comes from real entry-point runs on fixed input and, for learned or judged behavior, from evaluation.

**Essential contracts only.** A test is added only for an essential module contract: one that callers or stored data depend on, whose silent break would be costly (a security decision, money, data loss, a reported number), and that a real run does not exercise cheaply. Typical cases are a parser's accept and reject boundary, a serialized or persisted format, an error mapping callers branch on, a calculation with independently known results, and an agent loop's budget, termination, and permission checks. An accepted design document lists its essential contracts under the verification split with their reasons; follow that list. Prose-only, formatting-only, and mechanical changes get no tests.

**Implement first, then test the contract.** Write the tests from the interface contract, in Detroit (classicist) style. Writing them without rereading the implementation, or handing the contract to a separate author, keeps them from restating the code; use it when it helps.

- Real collaborators inside the module; outcomes checked through the public interface.
- Fakes only at external I/O and model seams, preferably the controlled adapters the code already has.
- No mocks that mirror interactions: no assertions on call order, call counts, or arguments passed between internal helpers.
- Expected values from the requirement, the documented contract, an independent calculation, or a reproduced bug, never from running the implementation.

**Reconcile each mismatch.** When a new test fails, decide which of three it is before changing anything:

- **Implementation bug:** the code violates the contract. Fix the code.
- **Contract gap:** the contract was silent or ambiguous and the test author chose differently from the implementer. Settle the behavior from the request or design document, or ask the user when the choice is consequential; write the answer into the contract, then fix whichever side disagrees.
- **Bad test:** the test asserts something the contract does not say. Fix or drop the test.

**Not kept.** A test that merely restates the implementation is removed before the change is finished: expected values copied from the code, assertions on internal structure, or a mock setup that mirrors the helper layout.

**Ask the user.** When a team's documented policy or a reviewer asks for tests, ask the user which tests to write; the scope is the user's call. When existing tests would be removed or changed, ask first. A test that fails during a refactor is diagnosed before the question: a regression in the code is fixed in the code; a failure from stale setup or an assertion on internals goes to the user with the diagnosis and the proposed change.

**CI-enforced tests.** When CI requires tests (a coverage gate, a required test per change), write only what passing requires, against the contract, and say so in the summary.

Tests and type checks answer different questions. An annotation does not validate a provider response, a successful import does not exercise a cleanup path, and a passing linter does not establish compatibility.

## Configured checks

Discover commands from project instructions, CI, and tool configuration, and run them through the language's project runner. Keep one configured formatter and the repository's selected type-checking strategy; do not migrate checkers or impose a new strict-mode configuration as a side effect. New and changed declarations carry explicit types as the language reference specifies; a checker accepting inferred types does not meet that rule. Broader changes to untouched code remain scoped to the request.

Run the smallest set that covers the changed surface, including repository-required checks. Broaden when a shared API or dependency warrants it. Do not apply unsafe automatic lint fixes, weaken a check to obtain a pass, or repeat unchanged successful checks without a new reason.

## Sources

The exception-hierarchy and single-seam rules follow the practice measured in httpx and the OpenAI and Anthropic SDKs; see [Python reference repositories](python/reference-repositories.md). Detroit or classicist style is the testing school Martin Fowler contrasts with the mockist school in [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) (2007). The rule that completion claims rest on fresh verification evidence, "evidence before claims", is adapted from the `verification-before-completion` skill in [obra/superpowers](https://github.com/obra/superpowers) (MIT License, Jesse Vincent), rewritten here; this pack does not adopt that project's test-first rule.

The test policy is this pack's choice: no new tests by default, essential contracts only, tests written from the contract, and verification through real runs and evaluation. These references do not mandate a coverage percentage or a specific test framework.
