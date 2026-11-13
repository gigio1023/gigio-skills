---
name: terminology
description: >
  Settle which name a project uses for a concept and record it in the project's terminology.md glossary, or answer from that glossary. Use when the user asks what we call something or which name to use, corrects or bans a wording, or asks to set up or curate the glossary: "what do we call this", "which name should we use", "이 용어 뭐라고 써", "용어 정리해줘".
---

# Terminology

A project glossary answers three questions per concept: which name the project uses, what it means here, and what others call it. It is a short lookup table, not a writing guide. Terms stay in the field's standard language, usually English; meanings are written in the reader's language.

Lookup is the ordinary path: read the glossary and apply it. It is cheap, writes nothing, and never starts a source survey. Curation is the second path and runs only under the conditions in "When to curate" below.

## Lookup

Read root `terminology.md` and only the topic files the task touches. Use each adopted name with its recorded meaning in answers, documents, and code explanations. Keep confirmed local names for their recorded audience, and honor wording decisions within their scope and exceptions. Quotations, code identifiers, APIs, and data labels keep their original form.

When the user asks about a term, answer with the adopted name, its meaning here, what other sources call it, and the reference.

A field term with no row is usually undisputed: use it in its standard sense and move on. When the task needs a name the glossary does not settle, describe the thing plainly, and keep an unconfirmed local name as observed without asserting its meaning. A project without `terminology.md` has nothing to look up; curation creates one only when a curation condition holds.

## When to curate

Curate only when the current task needs the name and one of these holds:

- The glossary has no row for it and the name is in doubt: you see competing names, one name carrying different meanings, or no established name at all.
- The project uses a name with a local meaning that differs from the field's.
- A recorded entry looks wrong or stale.
- A local name has no recorded confirmation.
- The user corrects or bans a wording, or asks to add, check, change, or prune entries.

When none holds, mention a suspected gap in one line and keep working with the plain description. In a read-only task, curation returns the proposed row instead of writing it.

## Inclusion test

A concept gets a row only when at least one of these holds:

- Names compete, or one name carries different meanings across industry projects, papers, or competitor products.
- A company or local meaning differs from the field's meaning.
- The user made an explicit wording decision, such as banning a word.

Undisputed field terms stay out even when the project uses them constantly. Sentence patterns, "do not write X" advice, and project explanations are not rows.

## Survey and decision

1. Start from what lookup found. A correct entry needs no work. A wrong or stale one is updated in place and keeps its reference ID.
2. Find how two or three recognizable sources in each relevant class name the concept, and whether their meaning matches: established projects, defining papers, and competitor products. [Naming survey](references/naming-survey.md) says which sources count and how to settle a split.
3. Adopt one name in its established spelling. When no established name exists, describe the thing plainly and mark the row unresolved instead of coining one.
4. Confirm local names with the user before recording them, as in [local names](references/local-names.md).
5. Write the row and its reference records as in [records and layout](references/records-and-layout.md).

## Entry format

| Term | Meaning | Elsewhere called | Reference |
| --- | --- | --- | --- |
| subagent definition | The configured record that fixes a subagent's model, tools, and instructions | Codex: role; Claude Agent SDK: `AgentDefinition` | R002, R004 |

Meaning is one line. Elsewhere called lists `source: name` pairs, including names the project did not adopt. A one-line caveat goes under the table only where misuse actually recurs. Local names and wording decisions have their own tables.

## Scope of changes

Write records in the project being worked on. After adopting or changing a name, update the documents the current task already edits and list other affected documents rather than sweeping the repository. Quotations, code identifiers, APIs, and data labels keep their original form.

## Project instruction snippet

A skill description does not load this skill on every task; the project's instruction file does. Lookup never edits instruction files. During curation, or when the user asks to set up terminology for the project, add this snippet to the instruction file the project's harnesses read, such as `AGENTS.md` or `CLAUDE.md`, if none carries it yet. When that file is outside the task's write scope, return the snippet as a proposal.

```markdown
## Terminology

Read `terminology.md` at task start and use its recorded names, local names, and wording decisions. When a needed term is missing, contested, or wrong, or a local name is unconfirmed, use the `terminology` skill to settle it.
```

Link the glossary rather than copying it into the instruction file.

## Finish

After curation, check that every new or changed row cites a reference record that exists and that the root index reaches every topic file. Report adopted or changed names, rows left unresolved, and local names still waiting for the user.
