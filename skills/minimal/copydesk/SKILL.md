---
name: copydesk
description: >
  Write, revise, or review reader-facing documents and substantive prose in any language: reports, guides, proposals, delivery briefs, posts, messages, and the prose of PRs, issues, and Notion pages. Includes AI-slop revision ("AI 티 빼줘", "deslop this"), English clarity, and Korean semantic repair ("글 다듬어줘", "문장 고쳐줘").
---

# Copydesk

Write for the reader's task. Select the facts and relationships they need, explain them in a useful order, and preserve what the evidence actually says. Clear writing lets the reader reconstruct the mechanism or reason for a decision without the drafting conversation.

## Scope and baseline

Infer the reader, purpose, sources, language, medium, and requested intervention from the current request and artifact. Ask only about missing information that changes meaning or authority. The [writing profile](references/writing-profile.md) holds the owner's standing preferences; it is usually already in the session. A current request or governing template takes precedence. Another author's text keeps its own voice unless a different voice was requested.

| Work | Editing scope |
| --- | --- |
| New writing | Compose from the supplied facts and inspected sources; choose the structure that serves the reader. |
| Local correction | Change the named passage or defect type. Keep unrelated passages intact; include a nearby edit when needed for grammar, references, or consistency. |
| Broad revision | Reorganize, combine, cut, and rewrite throughout the requested scope while preserving meaning, material detail, voice, and explicitly protected passages. |
| Review | Return the material findings and useful corrections. Edit or publish only when that is also requested. |

The current user-edited copy is the baseline. When an earlier version helps explain the user's choices, distinguish their edits from agent or collaborator changes. Respect intentional deletions instead of restoring the same function elsewhere. A note left for the writer guides the revision; it does not become reader-facing prose. Exact quotations, identifiers, code, and text explicitly marked to stay verbatim retain their form. Broad revision does not make all user-authored prose immutable. [Authoring and revision](references/authoring-and-revision.md) covers difficult scope or voice decisions and conversation residue.

## Meaning before polish

Keep the actor, action, object, condition, scope, timing, negation, requirement level, and uncertainty of each retained claim. Preserve the source's decision status: a candidate remains a candidate, and a proposed mechanism remains proposed. A concise sentence must not turn “should be prepared to retry” into “retries,” or a missing trace into proof that an event never occurred.

Ground added context in available evidence. A wording edit alone does not authorize inventing a cause, criterion, example, or measurement. If background knowledge is useful, distinguish it from the source's own claims. Cite near the supported claim and keep the explanation understandable without opening every link. When a number matters, preserve the unit, population, comparison conditions, and limitation that determines its interpretation. Compute arithmetic with tools.

To shorten, remove redundant orientation, repeated claims, process narration, and inventories that serve no reader task. Keep the theory, mechanism, examples, equations, figures, and numbers already present that the reader needs to understand the result. Remove empty hedging while retaining uncertainty that changes the claim. For a deslop request, diagnose what the passage fails to do for its reader, then repair that failure; pattern matches do not establish authorship or justify deletion.

## Structure and explanation

Open with the subject, supported finding, or decision, and organize sections around reader questions. Choose the form according to the relationship being explained:

- Prose develops causes, mechanisms, interpretation, and trade-offs.
- Lists group parallel facts or actions; ordered steps show a procedure.
- Tables compare common attributes or support exact lookup.

A small comparison can be complete with a table and a paragraph; a short mechanism can be complete in prose. Avoid putting paragraphs into table cells or turning connected reasoning into fragments to satisfy a preferred format.

Explain the smallest complete chain the reader needs: the problem or observation, what happens, why it matters, and an example when it makes the relationship concrete. Name actual components and operations. Define unfamiliar terms at their first useful use and use the same name for the same concept. Introduce background where the next step needs it. A condition essential to the main conclusion stays visible with it.

## Sentences and voice

Use direct, precise language with recoverable actors and references. Prefer active voice when responsibility matters. A passive sentence is useful when the affected object is the topic or the actor is unknown. Give an instruction a clear action and put a prerequisite where the reader sees it before acting. Keep causal and contrastive clauses together when that makes their relationship easier to understand.

Length and word counts are editing clues, not limits. Split a sentence when it overloads working memory or hides a relation; join fragments when separation obscures the reasoning. Keep grammar, established technical terms, meaningful modality, and natural syntax in the target language. Similar words may describe distinct actions: validate a schema, verify a signature, and confirm receipt need not share one verb.

For Korean prose, [Korean writing](references/korean-writing.md) preserves particles, endings, natural causal explanation, and the English field terms the reader uses; [correction cases](references/correction-cases.md) and [exemplar passages](references/exemplar-passages.md) show the owner's recurring repairs. For ambiguous English instructions, tool descriptions, status text, or a controlled-English request, see [English clarity](references/english-clarity.md). For a fluent sentence that may carry no fact, the [generic-sentence tests](references/authoring-and-revision.md#test-generic-sentences) help.

## Verification and delivery

Read the result without the drafting conversation. Can the reader recover the conclusion's reason, the mechanism, and its important conditions? For a document someone will act on without you, a [cold reader](references/cold-reader.md) pass can show what the conversation supplied that the page does not. Compare the revision with its source for additions, omissions, stronger claims, changed requirements, or flattened voice. For local corrections, inspect the diff for unrelated movement.

Bundled helpers use Python 3's standard library; run them from this skill directory when their signals answer a real question:

- `python3 scripts/check_slop.py <file>` reports where common LLM style patterns cluster, such as Korean connective commas and English negation-contrast frames. Its counts locate passages to reread and never grade a document.
- `python3 scripts/check_draft.py <file>` locates possible padding, dense presentation, or references to the drafting session. Zero findings say nothing about usefulness or accuracy.
- `python3 scripts/measure_length.py <before> [<after>]` counts words per heading and their change.
- `python3 scripts/protected_diff.py <previous> <revised> --allow "<heading>"` reports literal movement outside a local correction.
- `python3 scripts/trace_check.py <traced.md>` with [source tracing](references/source-tracing.md) helps a source-bound rewrite at risk of invented connective facts.

After publishing or updating a shared copy, re-fetch it and diff it against the source; a Notion replacement of 192 items once applied only 100 silently. For sharing or changed recipients, see [sharing and delivery](references/sharing-and-delivery.md). Deliver the requested text first; report only material limitations or unresolved editorial decisions.

The profile is maintained in one source file. After an authorized profile edit, `python3 scripts/sync_profile.py <instruction-file>` refreshes a copy between `<!-- writing-profile:start -->` markers, and `--check` verifies it. Updating a repository copy does not authorize editing live global instructions.

## Other references

- [Synthetic examples](references/synthetic-examples.md): table and prose repairs with before and after.
- [Measurements](references/measurements.md): measured quantities, comparison conditions, and tables of results.
- [Document forms](references/document-forms.md): genre requirements, including the delivery brief for customer- or deadline-bound work.
- [Multilingual writing](references/multilingual-writing.md): locale and voice choices beyond the short language guides.
- [Korean pattern evidence](references/korean-pattern-evidence.md): evidence behind a specific repetitive Korean pattern.
