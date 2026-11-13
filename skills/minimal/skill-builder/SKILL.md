---
name: skill-builder
description: >
  Create, improve, or audit reusable agent skills from real work and user
  preferences: instructions, descriptions, resources, scripts, packaging, and
  validation, including one skill that must work in both Claude Code and
  Codex. Use for "make this a skill", "improve this skill's description",
  "audit the skill pack", "skill 만들어줘", "이거 skill로 빼줘".
---

# Skill Builder

Build reusable capability from working procedures, domain knowledge, and recurring preferences.

Infer the outcome, trigger, target harness, and edit scope from the request and the package; ask only for consequential gaps. Start from evidence: successful work, a real artifact, a documented contract, a stated preference, or a correction. Improve an existing skill when it owns the task; create a new one when a distinct recurring task would otherwise be hard to select. Edit the source and affected references together. Read [local layout](references/local-skill-layout.md) when resolving repository sources or installed copies.

## What Belongs

Add what the agent cannot reliably infer: a preferred explanation style, a private schema, a subtle API contract, a required artifact, a fragile operation, or a recurring mistake. A personal or project-local skill is a first-class result; one well-understood workflow or explicit preference can justify a skill. A simple skill can be just its trigger, purpose, audience, and result format.

Use project instructions for rules that apply to every task, skills for reusable methods and judgment, tools or MCP for access, and hooks for deterministic enforcement. Prose cannot grant access or enforce a permission boundary.

When deriving a skill from sessions, work artifacts, or preferences, read [workflow extraction](references/workflow-extraction.md). Reading private material does not authorize publishing it; a shared package carries the reusable method and safe examples.

For a failed workflow, find whether information was missing, hard to retrieve, ambiguous, poorly exposed by tools, or impossible to check, and fix that cause before adding an instruction. Check co-loaded skills and project instructions for conflicts and duplication; give each shared rule one home.

## Writing the Skill

Include what changes behavior: the result and how to tell it is done, authoritative inputs and defaults, non-obvious invariants, exact steps only where order, syntax, or side effects are fragile, a fallback for a specific failure, and the verification that matters. Use decision rules where approaches may vary, and give the reason when it helps the agent adapt. Avoid mandatory planning files, fixed step sequences, universal headings, and exhaustive menus.

The description says what the skill does and when to use it, with natural trigger phrases, and does not list sibling skills or route to them. Keep it specific enough that it does not capture unrelated work. Codex budgets its initial skill listing (about 2% of context, 8,000 characters when the size is unknown) and both harnesses may truncate descriptions, so put the most distinguishing trigger first.

Capture observed gotchas as the condition, the tempting mistake, and the correction. Do not invent failures to fill a Gotchas heading.

Write Markdown prose as natural paragraphs without hard line breaks for a column limit. There is no universal size limit; the Agent Skills specification's guidance of about 500 lines and 5,000 tokens is a reason to review structure, not a rejection threshold. Keep essential instructions in SKILL.md and move optional detail to references, with the condition for reading each one beside its link. Keep schemas and enum values in one place.

Use package-relative resource paths. Document interpreter, tool, network, and service prerequisites; detect missing ones and give bounded setup, since mentioning a dependency does not authorize installing it. State non-obvious network, write, credential, or persistence effects, and store mutable user data outside replaceable package files.

When one package must work in more than one harness, such as Claude Code and Codex, read [cross-harness authoring](references/cross-harness.md). Keep authority boundaries in the body even when a host offers invocation controls.

## Verify

- **Package:** metadata, resource links, dependencies. Static checks do not establish security or model quality.
- **Artifact:** run changed scripts or templates on real or fixed input, including failure paths. Add a test only when its expected values come from a spec or a reproduced bug.
- **Behavior:** actual task feedback or existing traces. Model trials and trigger benchmarks run only on request; documentation-only edits do not need them.

The validator needs Python 3.10+ and PyYAML (verified with 6.0.3). From this skill's directory:

```bash
bash scripts/validate_skill.sh <path-to-target-package>
# With an authorized isolated dependency environment:
uv run --with PyYAML==6.0.3 bash scripts/validate_skill.sh <path-to-target-package>
```

`bash scripts/smoke_test.sh` tests the validator itself; run it after changing the validator. The Python entry point also takes `--target claude-code` for Anthropic's metadata restrictions. [Validation contract](references/validation.md) lists exact coverage.

## Publishing

Before a requested publication, inventory staged, unstaged, and untracked files; an ordinary diff omits untracked resources. Review the full intended content, attachments, and history for personal and confidential information, including Git author and committer identities, commit messages, logs, filenames, and URLs. Use synthetic examples that keep the relevant decision; changing a name alone may leave the source identifiable. Structural validation and secret scans do not establish that a package is safe to publish, and a later redaction commit does not remove earlier exposure. See [publication privacy](references/workflow-extraction.md#keep-confidential-work-out-of-public-packages).

Report what changed, why, what ran, and what remains untested.
