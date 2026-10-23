# Small Model Handoff Prompt Patterns

GPT packets must satisfy the current GPT policy in `model-routing`, when installed, before using these patterns. The `sol-clerk` role or another deliberately selected mechanical contract permits only fixed collection, approved deterministic data transforms, or command execution; return raw evidence and failures to the planner for interpretation. Apply those restrictions to that contract, not to every assignment on the selected model.

## Contents

- Planner handoff packet
- Compact executor preamble
- Mode-specific scope
- Preflight without a pause
- Evidence and final report
- Stop report
- Change example
- Test-run example
- Read-only inspection example
- Failure diagnosis

## Planner Handoff Packet

Complete this before writing the executor prompt:

```text
Outcome: [one observable result, artifact, or evidence packet]
Mode: [change | run | inspect | ordered mixed phases]
Approved basis: [decision, procedure, reproduction, or prerequisite evidence]
Executor: [exact model, supported effort, and applicable routing rule]
Executor limits: [choices or recovery this assignment must not perform; no semantic judgment under a mechanical contract]
Allowed scope:
- Files/symbols: [exclusive mutation targets, or none]
- Commands: [exact commands and working directory, or none]
- Sources/inputs: [exact artifacts, paths, URLs, or data]
Authority: [writes, external effects, credentials, artifacts, retries]
Procedure:
1. [exact action]
Preserve: [contracts, state, data, formatting, environment]
Evidence: [outputs, exit states, artifacts, diffs, or observations]
Accept when: [observable completion criteria]
Stop if: [contradictions, missing authority, or undefined recovery]
```

If the procedure still contains choices such as “A or B,” return it to the planner unless the packet gives a mechanical rule for choosing.

## Compact Executor Preamble

For a change:

```text
Do not optimize for completing the request as broadly as possible.
Optimize for the smallest correct and verifiable change.
```

For a run or inspection:

```text
Do not optimize for completing the request as broadly as possible.
Optimize for the smallest authorized execution that produces the required evidence.
```

Then add:

```text
Execute only the approved task below. Planning and decisions outside your stated authority are complete. Verify the packet against current reality, then continue without waiting unless a stop condition is met.
```

## Mode-Specific Scope

### Change

```text
Allowed mutations
- `src/foo.py`: `parse_foo` only
- `tests/test_foo.py`: one regression case only

No other file or symbol may change. Stop if the approved edit requires another target.
```

### Run

```text
Allowed commands
- Working directory: `<repo-root>`
- Run once: `pytest tests/test_foo.py -q`
- Retry: none
- Generated artifacts: none may remain

Do not edit files, install dependencies, change configuration, or run additional diagnostics. A failing command is evidence to report, not permission to fix it.
```

### Inspect

```text
Allowed sources
- `logs/test-run.txt`
- `artifacts/results.json`

Answer only: [named questions]. This phase is read-only. Do not modify, regenerate, or fetch replacement artifacts.
```

For mixed work, place phases in order and repeat the authority boundary when it changes. Never let a read-only or command-only phase inherit mutation authority.

## Preflight Without a Pause

```text
Before execution:
1. Confirm the approved basis and prerequisites against named evidence.
2. Confirm every action fits the allowed files, commands, sources, and effects.
3. Check for overlapping user work or unexpected state where relevant.
4. Confirm the required evidence can be captured with the supplied procedure.

If all checks pass, proceed directly. Stop only under the listed conditions.
```

## Evidence and Final Report

Require only fields relevant to the mode:

```text
- Preflight consistency result
- Actions performed in order
- Commands with working directory, exit status, and relevant output
- Evidence tied to named sources; raw or mechanically transformed results under a mechanical contract
- Created, modified, or deleted files and artifacts
- Acceptance criteria result
- Failed, skipped, unavailable, and unverified items
- Assumptions, deviations, side effects, and remaining unknowns
```

Do not require a diff for a read-only run. Do require an explicit changed-file or artifact audit so “no mutation” is evidence-backed.

## Stop Report

```text
Stopped before the unauthorized or undefined action.

Mismatch: [what contradicted the packet]
Evidence: [file, command output, source, state, or diff]
Work performed: [none, or exact completed actions]
Side effects: [files, artifacts, external state, or none]
Missing decision or authority: [smallest required addition]
Verification state: [evidence captured and not captured]
```

## Change Example For An Authorized Change Executor

```text
Do not optimize for completing the request as broadly as possible.
Optimize for the smallest correct and verifiable change.

Outcome
- Fix only [described issue].

Mode and approved basis
- Mode: change.
- Root cause: [cause], confirmed by [evidence].
- Approved edit: [exact edit].

Allowed scope
- `src/foo.py`: [symbol]
- `tests/test_foo.py`: [test region]

Authority and preservation
- Modify only the targets above; create no other artifacts.
- Preserve [public contract and relevant invariants].
- Do not refactor, rename public symbols, change configuration, or weaken tests.

Procedure
1. Verify the basis and target state.
2. Apply [exact source edit].
3. Add [exact regression case].
4. Run `[focused test]`, `[type check]`, and `[lint]`.

Stop if the basis is contradicted or another target is required. Report the diff, commands and results, changed files, deviations, and unverified items.
```

## Test-Run Example

```text
Do not optimize for completing the request as broadly as possible.
Optimize for the smallest authorized execution that produces the required evidence.

Outcome
- Determine whether the approved regression test passes in the current checkout.

Mode and scope
- Mode: run.
- Working directory: [absolute or repository-relative directory].
- Run exactly once: `pytest tests/test_foo.py::test_regression -q`.
- Do not run other tests or diagnostics.

Authority
- Read repository files required by the test runner.
- Do not edit files, install packages, change configuration, access new secrets, or retain generated artifacts outside the runner's normal temporary output.

Report the command, working directory, exit status, concise relevant output, any artifacts, and whether the stated acceptance criterion passed. A failure is the final result; do not investigate or fix it.
```

## Read-Only Inspection Example

```text
Do not optimize for completing the request as broadly as possible.
Optimize for the smallest authorized execution that produces the required evidence.

Outcome
- Report which of [named checks] failed in `artifacts/results.json`.

Mode and scope
- Mode: inspect.
- Read only `artifacts/results.json`.
- Do not run commands, fetch data, regenerate artifacts, or modify files.

Report each failed check with its exact identifier and recorded message. Mark any requested field absent from the artifact as unknown; do not infer it.
```

## Failure Diagnosis

| Symptom | Prompt defect | Correction |
| --- | --- | --- |
| Executor redesigns the solution | Procedure is missing or optional | Supply one procedure or a mechanical branch rule |
| Failed test triggers edits | Run mode lacks an authority boundary | State that failure is evidence and mutation is forbidden |
| Executor runs broad diagnostics | Command list is advisory | Make commands exclusive and bound retries |
| Inspection changes artifacts | Read-only boundary is implicit | Name sources and forbid regeneration or writes |
| Executor stops after preflight | Checklist implies an approval gate | Continue automatically when checks pass |
| Executor improvises recovery | Unexpected-result branch is absent | Supply a bounded branch or require a stop report |
| Final answer hides missing evidence | Report fields are generic | Require mode-specific outputs, side effects, and unknowns |
