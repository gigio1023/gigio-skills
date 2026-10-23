---
name: small-model-handoff
description: >
  Use only when the user invokes small-model-handoff by name, or when another
  loaded skill explicitly names it while dispatching to a weaker executor, to turn an already researched and approved
  plan into a bounded prompt for an executor less capable than the planner.
  Covers scoped changes, test, build, and check runs, reproductions, and
  read-only evidence collection. Requires exact scope, actions, authority,
  capability assumptions, evidence, and stop rules. NOT for automatic
  invocation, model/cost/executor recommendations, peer or high-capability
  executors, discovery, planning, open-ended work, or general session handoffs.
---

# Small Model Handoff

Turn the settled current step of a plan into a narrow execution contract for a model that is less reliable than the planner at task execution, recovery, context handling, or scope control. Reduce its judgment surface; keep unresolved decisions with the planner.

## Invocation Policy

Use this skill when the user explicitly invokes it to build the bounded prompt, or when another loaded skill explicitly names it while dispatching work to a weaker executor. Model names, cost preferences, executor recommendations, and discussion or edits to this skill do not invoke it. Do not auto-apply it to a handoff. Do not use it for a peer or high-capability executor that can safely inherit open judgment. Use `session-handoff` for successor-ready session transfers.

## Quick Path

1. Resolve every Handoff Gate field from the approved plan, named artifacts, and session grants before requesting more input from the planner.
2. If a consequential field remains missing or contradictory, return the specific unresolved list and finish the settled parts of the prompt. Do not dispatch an incomplete packet or invent authority to fill a field.
3. Check the executor against the applicable routing policy in `model-routing` when it is installed; otherwise record the executor limits the user states and keep all judgment with the planner. Then select `change`, `run`, `inspect`, or an explicitly ordered `mixed` mode. Apply the mechanical boundary below only when that execution contract is selected.
4. Write one prompt from `assets/execution-prompt.template.md`; remove sections that do not apply instead of leaving empty placeholders.
5. Resolve every choice the executor cannot handle reliably.
6. Tell the executor to continue when preflight matches; the execution loop below belongs in the generated prompt and does not authorize this authoring invocation to run the task.
7. Return the copy-ready prompt plus only the assumptions the planner must resolve before use.

Read `references/prompt-patterns.md` for mode-specific scope patterns, stop reports, and examples.

## Mechanical Executor Boundary

Follow the GPT policy in `model-routing` for GPT assignments when it is installed. The `sol-clerk` role or another deliberately selected mechanical contract accepts only fixed collection, deterministic transformation, or command execution with fixed inputs, procedure, output, and mechanical acceptance. Source selection, summaries, confidence assessment, diagnosis, code implementation, review, and prose edits fall outside that contract. These restrictions describe the selected assignment, not every task a model can receive.

For a mechanical packet, name exact source locations and return raw or mechanically transformed results, exit statuses, and failed items. Use `change` only for an approved deterministic data transform. A mismatch returns to the planner without interpretation or recovery. The restrictions here support a mechanical executor; they are not default instructions for the planner, a more capable executor, or a general successor.

## Handoff Gate

Only the delegated step needs to be settled; the whole research project need not have a predetermined outcome or sequence. A valid packet answers these without new product, architecture, or recovery judgment:

| Field | Required content |
| --- | --- |
| Outcome | One observable result, artifact, or evidence packet |
| Mode | `change`, `run`, `inspect`, or an ordered combination |
| Basis | Approved decision, procedure, reproduction, or named prerequisite |
| Scope | Exact files, symbols, commands, inputs, sources, and locations |
| Authority | Permitted writes, side effects, retries, credentials, and external actions |
| Procedure | Ordered actions and the choices already resolved by the planner |
| Preservation | Contracts, state, data, formatting, or environment to keep unchanged |
| Executor profile | Selected model, applicable routing rule, and task-relevant limits |
| Evidence | Expected outputs, exit states, artifacts, diffs, or cited observations |
| Stop conditions | Mismatches that must return to the planner |

A field may be satisfied by pointing at a durable plan document — the plan file path plus the task ID — instead of restating what it already says. Never paraphrase content that lives in the plan file; the executor reads it at the named path.

“Investigate and handle it” is not a packet. If the executor must discover the procedure, choose the fix, or decide how to recover, planning is unfinished.

## Task Modes

| Mode | Scope contract | Completion evidence |
| --- | --- | --- |
| `change` | Allowed files and symbols, exact edits, permitted generated files | Diff, changed-file audit, supplied checks |
| `run` | Exact commands, working directory, inputs, environment assumptions, retries | Command, exit status, relevant output, artifacts |
| `inspect` | Named sources and questions, read-only boundary, evidence format | Cited observations and explicit unknowns |
| `mixed` | Ordered modes with a separate authority boundary for each phase | Evidence from every phase and cumulative side effects |

Under a mechanical execution contract, questions in `inspect` must be literal fields or fixed checks, not a request to select relevant evidence or explain meaning. For `run`, a failed test or check is a result, not permission to diagnose or edit. For `inspect`, no mutation is allowed unless a later phase grants it explicitly.

## Prompt Rules

### Lead With the Optimization Target

For changes, open with:

```text
Do not optimize for completing the request as broadly as possible.
Optimize for the smallest correct and verifiable change.
```

For non-mutating work, replace the second line with:

```text
Optimize for the smallest authorized execution that produces the required evidence.
```

Then state one outcome. Do not repeat it later.

### Make Scope and Authority Mechanical

- For `change`, provide exclusive file and symbol allowlists.
- For `run`, provide exact commands, working directory, allowed retries, and whether generated artifacts may remain.
- For `inspect`, name allowed sources, questions, and the read-only boundary.
- For `mixed`, state where each phase begins and whether its authority changes.

Write operational limits, not model stereotypes. Prohibit only relevant failure modes: unplanned edits, extra commands, dependency or configuration changes, test weakening, destructive actions, secret access, or external writes.

### Treat the Plan as Fixed Input

Require a preflight consistency check against named evidence and prerequisites. If it matches, continue. Do not ask the executor to redesign, investigate adjacent issues, choose alternatives, or improvise recovery. Unexpected results belong in the report unless a supplied branch or bounded retry covers them.

### Use One Short Execution Loop

1. Preflight: confirm prerequisites, scope, authority, and current state.
2. Execute: perform only the supplied actions.
3. Collect evidence: capture the required outputs, artifacts, diffs, or findings.
4. Report: show results, side effects, assumptions, deviations, and unknowns.

If a required tool or check is unavailable, report it. Do not install packages, change configuration, access new credentials, or invent infrastructure unless the packet explicitly authorizes that action.

### Stop on Authority or Plan Mismatches

Stop before the affected action when:

- a prerequisite or approved basis contradicts current reality;
- completion requires a file, command, source, credential, or side effect outside the stated scope;
- a destructive or external action lacks explicit authority;
- an unexpected mutation or overlapping user change cannot be preserved;
- the supplied procedure has no defined branch for a result requiring judgment.

Name the mismatch, evidence, work already performed, and smallest missing decision or authority expansion.

## Output Contract

Return one copy-ready execution prompt containing the outcome, mode, approved basis and procedure, scope, authority, preservation rules, preflight, evidence, stop conditions, and final report fields. Do not execute the task, rank models, add alternative plans, or create a synthetic evaluation.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| `references/prompt-patterns.md` | Building or reviewing a bounded handoff | Packet, mode scopes, stop report, examples, and failure patterns |
| `assets/execution-prompt.template.md` | Producing the final prompt | Copy-ready multi-mode execution template |

## Gotchas

- Do not call the executor “stupid” or “weak”; state task-relevant limits.
- Do not infer lower capability from model size, speed, or price alone.
- Do not turn a failing test run into an unauthorized bug-fix task.
- Do not treat command completion as success when exit status, evidence, or expected artifacts are missing.
