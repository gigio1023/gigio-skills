# Cross-Harness Skills

Use this when one skill package must work in more than one harness, such as Claude Code and Codex, or when a request asks to review, modernize, or test the same skill across runtimes. A single-harness skill does not need it.

Build one portable core without flattening the harnesses' different model and runtime behavior into vague advice. The common SKILL.md defines the task contract. Harness-only invocation, metadata, hooks, permissions, and path features stay in adapters or installation documentation. If an adapter is removed, the skill should lose convenience or enforcement, not its meaning, normal execution path, or safety boundary.

## Approach

- Classify the request. A review-only request returns findings and does not edit files; a create, improve, or modernize request authorizes in-scope edits.
- Identify the intended model in each harness from the request or the user's configuration. Record unavailable model and harness combinations instead of treating one successful run as proof for both.
- Write the portable core first with the working contract in SKILL.md and the deltas below. Add only domain knowledge, fragile procedure, authority boundaries, evidence requirements, output preservation, and real stop or fallback rules.
- Read [harness adapters](cross-harness-adapters.md) before using a path, invocation syntax, tool name, frontmatter key, hook, subagent feature, or environment variable. Move a capability into an adapter when the other harness cannot interpret it with the same meaning; the core must still complete correctly without that adapter.
- In change mode, patch measured defects; do not rewrite a passing skill to mention model names.
- Validate packaging and changed executable resources as SKILL.md describes. Run model comparisons only on request, reuse existing traces when available, and keep static findings separate from behavior exercised in either harness.

## Portable Deltas To The Working Contract

The working contract in SKILL.md applies unchanged. A package that must run in both harnesses also states these in its body, because no adapter can be trusted to carry them:

- **Authority:** distinguish answer, review, or diagnosis from build or change, and name external, destructive, irreversible, or scope-expanding actions separately. A review is not authorization to edit; a change request normally includes in-scope local edits and non-destructive validation.
- **Routing:** describe the required capability and decision rule, not a built-in tool name. Sequential execution stays valid; parallel work is an optimization.
- **Output:** what the reader needs to decide or continue, including material caveats and next actions.
- **Stop and fallback:** when enough evidence exists, when to retry, and which missing input genuinely blocks completion.

Do not force these into headings. Use the smallest structure that makes the contract unambiguous for the task.

## Adapter Boundary

Portable core examples:

- `name` and `description` frontmatter, with supported optional standard fields when useful;
- forward-slash relative resource paths;
- "read the file", "search the repository", or "run the bundled validator";
- a script invocation documented from the skill root;
- optional parallelism with a sequential fallback.

Adapter-only examples:

- `/skill-name`, `$skill-name`, or another invocation syntax;
- `.claude/skills`, `.agents/skills`, or user-install locations;
- Claude Code dynamic command injection, `${CLAUDE_SKILL_DIR}`, hooks, `context: fork`, `allowed-tools`, or invocation-control frontmatter;
- Codex `agents/openai.yaml`, plugin dependencies, config, approval, or UI policy;
- hard-coded built-in tool or subagent names from either harness.

A side-effecting workflow must remain safe when adapter metadata is absent. Do not rely on Claude-only metadata to protect a side effect or on Codex-only policy to make a workflow safe. Put the authority boundary in the portable body and use an adapter only as additional enforcement or user experience.

## Keep Model Guidance Out Of The Core

Portable does not mean vague. Preserve precise domain contracts and exact safety or schema rules.

Do not copy every recommendation from each model guide into the core. Keep their task-specific intersection, and isolate divergent runtime controls such as effort, long-run memory, programmatic tool calling, and asynchronous agents in the runtime or harness layer, tuned after evaluation rather than set as domain defaults. Model names, effort, and cost routing do not belong in the portable core.

## Output

For a review, lead with findings and state that files were not changed. For a change, report the portable contract, the adapter split, accepted changes, validations actually run in each harness and model pair, and untested cells. If only static or script validation was possible, say so plainly.
