---
name: copydesk
description: >
  Write, revise, or review reader-facing documents and substantive prose in any language: reports, guides, proposals, delivery briefs, posts, and messages. Includes focused AI-slop revision, English clarity, and Korean semantic repair. Provides shared meaning, voice, and author-profile principles for PRs, issues, Notion pages, and the prose of design docs; draft-pr, write-issue, and write-notion own their artifact structure and publication workflows. NOT for choosing a design document's sections and design content, which belong to design-doc. Use specialized skills for drawing figures, building dashboards, and file production.
---

# Copydesk

Write for the reader's task. Select the facts and relationships they need, explain them in a useful order, and preserve what the evidence actually says. Clear writing lets the reader reconstruct the mechanism or reason for a decision without the drafting conversation.

## Scope and baseline

Infer the reader, purpose, sources, language, medium, and requested intervention from the current request and artifact. Ask only about missing information that changes meaning or authority. Read the [writing profile](references/writing-profile.md) for the active standing preferences; reuse it when already present in the session. The pack ships its maintainer's profile as the default: a user edits or replaces that file, or points their instruction file at their own profile, and the craft rules in this file apply either way. A current request or governing template takes precedence. Another author's text keeps its own voice unless a different voice was requested.

| Work | Editing scope |
| --- | --- |
| New writing | Compose from the supplied facts and inspected sources; choose the structure that serves the reader. |
| Local correction | Change the named passage or defect type. Keep unrelated passages intact; include a nearby edit when needed for grammar, references, or consistency. |
| Broad revision | Reorganize, combine, cut, and rewrite throughout the requested scope while preserving meaning, material detail, voice, and explicitly protected passages. |
| Review | Return the material findings and useful corrections. Edit or publish only when that is also requested. |

The current user-edited copy is the baseline. When an earlier version helps explain the user's choices, distinguish their edits from agent or collaborator changes. Respect intentional deletions instead of restoring the same function elsewhere. A note left for the writer guides the revision; it does not become reader-facing prose. Exact quotations, identifiers, code, and text explicitly marked to stay verbatim retain their form. Broad revision does not make all user-authored prose immutable. See [authoring and revision](references/authoring-and-revision.md) for difficult scope or voice decisions.

## Meaning before polish

Keep the actor, action, object, condition, scope, timing, negation, requirement level, and uncertainty of each retained claim. Preserve the source's decision status: a candidate remains a candidate, and a proposed mechanism remains proposed. A concise sentence must not turn “should be prepared to retry” into “retries,” or a missing trace into proof that an event never occurred.

Ground added context in available evidence. A wording edit alone does not authorize inventing a cause, criterion, example, or measurement. If background knowledge is useful, distinguish it from the source's own claims. Cite near the supported claim and keep the explanation understandable without opening every link. When a number matters, preserve the unit, population, comparison conditions, and limitation that determines its interpretation. Compute arithmetic with tools.

To shorten, remove redundant orientation, repeated claims, process narration, and inventories that serve no reader task. Keep the theory, mechanism, examples, equations, figures, and numbers needed to understand the result. Remove empty hedging while retaining uncertainty that changes the claim. For a deslop request, diagnose what the passage fails to do for its reader, then repair that failure; pattern matches do not establish authorship or justify deletion.

## Structure and explanation

Open with the subject, supported finding, or decision. Organize sections around reader questions. Section headings are professional noun phrases that identify the subject and the section's role, as in a research paper. Keep necessary technical qualifiers, but put full-sentence claims, explanations, conversational address, and reading instructions in the body. Korean endings such as `~했네요`, `~입니다`, `~해요`, and `~살펴보겠습니다` do not belong in section headings. Follow a title explicitly required by the user or a governing template. Choose the form according to the relationship being explained:

- Prose develops causes, mechanisms, interpretation, and trade-offs.
- Lists group parallel facts or actions; ordered steps show a procedure.
- Tables compare common attributes or support exact lookup.
- Diagrams show relationships, state changes, or flows that are harder to follow in prose.
- Charts show quantitative patterns; interaction helps when changing an input teaches something useful.

Use a display when it reduces the reader's work. A small comparison can be complete with a table and a paragraph; a short mechanism can be complete in prose. Avoid putting paragraphs into table cells or turning connected reasoning into fragments to satisfy a preferred format. For a new structure or overloaded display, read [information design](references/information-design.md). For a substantial explanation, read the matching [finished example](references/finished-examples.md) before treating individual style rules as a checklist.

Explain the smallest complete chain the reader needs: the problem or observation, what happens, why it matters, and an example when it makes the relationship concrete. Name actual components and operations. Define unfamiliar terms at their first useful use and use the same name for the same concept. Introduce background where the next step needs it. Optional depth can be collapsed or moved, but a condition essential to the main conclusion stays visible with it.

## Sentences and voice

Use direct, precise language with recoverable actors and references. Prefer active voice when responsibility matters. A passive sentence is useful when the affected object is the topic or the actor is unknown. Give an instruction a clear action and put a prerequisite where the reader sees it before acting. Keep causal and contrastive clauses together when that makes their relationship easier to understand.

Length and word counts are editing clues, not limits. Split a sentence when it overloads working memory or hides a relation; join fragments when separation obscures the reasoning. Keep grammar, established technical terms, meaningful modality, and natural syntax in the target language. Similar words may describe distinct actions: validate a schema, verify a signature, and confirm receipt need not share one verb.

For Korean prose or a Korean clarity repair, read the compact [Korean writing](references/korean-writing.md) guide. It preserves particles, endings, natural causal explanation, and the English field terms the reader uses. Ordinary short answers need its principles, not a full reference pass. For ambiguous English instructions, tool descriptions, status text, or a controlled-English request, read [English clarity](references/english-clarity.md). These STE-inspired methods do not impose English syntax on Korean or claim ASD dictionary compliance. Use [voice and facts](references/voice-and-facts.md) for a difficult sentence or claim-strength decision.

## Verification and delivery

Read the result without the drafting conversation. Can the reader recover the conclusion's reason, the mechanism, and its important conditions? Read the section headings together: they should form a professional topic outline, without conversational sentences or a narration of what the writer will explain. Compare the revision with its source for additions, omissions, stronger claims, changed requirements, or flattened voice. For local corrections, inspect the diff for unrelated movement. For broad revisions, inspect meaning and explicitly protected content across the changed structure.

Use bundled helpers when their signals answer a real question. Run them from this skill directory or resolve their paths from it. They use Python 3's standard library:

- `python3 scripts/check_draft.py <file>` locates possible padding, dense presentation, or references to the drafting session. Findings require judgment; zero findings provide no evidence that claims are useful, accurate, or clear.
- `python3 scripts/check_slop.py <file>` reports where common LLM style patterns cluster, such as Korean connective commas and English negation-contrast frames. Its counts locate passages to reread and never grade a document.
- `python3 scripts/measure_length.py <before> [<after>]` counts words per heading and their change, for a revision summary that tags changes CUT, MERGE, MOVE, CONDENSE, or PRESERVE.
- `python3 scripts/protected_diff.py <previous> <revised> --allow "<heading>"` reports literal movement outside a local correction. It is useful for a narrow scope or a verbatim preservation requirement, not as a retention target for a broad rewrite.
- [Source tracing](references/source-tracing.md) helps a source-bound rewrite with a risk of invented connective facts, or a requested traceable draft. It is optional for routine edits.

Check affected links, numbering, and renderer syntax after structural changes. Inspect rendered files at delivery size when layout matters. For sharing or changed recipients, read [sharing and delivery](references/sharing-and-delivery.md), verify access to cited sources, and use existing authorization for publication or sending. Deliver the requested text or artifact first; report only material limitations or unresolved editorial decisions.

The profile is maintained in one source file. After an authorized profile edit, use `python3 scripts/sync_profile.py <instruction-file>` to refresh the intended copy, then `--check` to verify it. Updating a repository copy does not authorize editing live global instructions.

## Targeted references

Open additional references only for the decision at hand:

- [Exemplar passages](references/exemplar-passages.md): natural Korean mechanism, contrast, and result explanation. Borrow the operation, not the topic or register.
- [Correction cases](references/correction-cases.md), [synthetic examples](references/synthetic-examples.md): a recurring failure or a matching repair. Supplied context is part of each example's evidence.
- [Reader value](references/reader-value.md), [explanation with depth](references/explanation-with-depth.md): difficult selection or explanation decisions.
- [Measurements and figures](references/measurements-and-figures.md): quantitative meaning, captions, and comparisons.
- [Document forms](references/document-forms.md), [document production](references/document-production.md): genre requirements, including the delivery brief for customer- or deadline-bound work, and editable or PDF output.
- [Multilingual writing](references/multilingual-writing.md): locale and voice choices beyond the short language guides.
- [Korean pattern evidence](references/korean-pattern-evidence.md): a specific repetitive pattern or maintenance of its evidence, not a routine Korean drafting dependency.
- [Composition](references/composition.md): specialist ownership and useful combinations. Maintenance provenance is in [writing sources](https://github.com/gigio1023/gigio-skills/blob/main/docs/writing-sources.md).
