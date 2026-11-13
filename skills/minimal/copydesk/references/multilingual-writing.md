# Multilingual Writing

Use the relevant section when language, locale, or voice affects a drafting or revision decision. Each language keeps its natural syntax.

## Shared judgment

Follow the requested language and locale, governing terminology, genre, and approved voice sample. Keep exact identifiers, quotations, commands, official names, requirement levels, and numbers intact. Revise the surrounding explanation in the target language's natural syntax. Do not translate or localize a document merely because a clarity edit was requested.

When changing a sentence, compare its actor, action, object, scope, negation, condition, time, causal relation, and degree of certainty with the source. Keep a connector when it expresses a real relation. Punctuation follows the [writing profile](writing-profile.md).

For languages not covered below, use the same semantic checks with the supplied examples and applicable locale guidance. If translating is requested, compare the resulting claim and its conditions with the source; fluency alone does not establish fidelity.

## English

Use the established English variety and register. Contractions, fragments, first person, and passive voice can all be appropriate. Keep a personal aside that adds context or voice; remove an opener such as “it is important to note” when the proposition can stand without it.

Prefer an operation to an inflated abstraction when it preserves meaning: “The worker can retry requests” can replace “The worker provides the capability to perform request retries.” Keep capability, frequency, and permission distinctions when they are real. “Can retry” and “retries” do not make the same claim.

Check an appended `-ing` clause if it supplies an unsupported effect or an unclear actor. State the actual relation or remove the unsupported inference. A summary belongs when it synthesizes a decision, not simply because the document has reached its end.

For ambiguity in instructions, tool descriptions, or status text, use [English clarity](english-clarity.md). Preserve distinctions between technical operations even when their verbs are common synonyms elsewhere.

## Korean

Korean meaning, terminology, and synthetic examples live in [Korean writing](korean-writing.md). Specific pattern observations and their limits are optional in [Korean pattern evidence](korean-pattern-evidence.md). The house punctuation and the English field-term boundary are profile preferences in the [writing profile](writing-profile.md), which this pack ships as a default that a user can edit or replace.

## Italian

Keep the paragraph's topic and focus, even when a condition or timeframe precedes the main clause. Name an actor when responsibility depends on it and the evidence supplies it. Passive and impersonal forms are useful when the actor is unknown, immaterial, or already clear.

Replace a support-verb phrase with a direct verb when no procedural or legal distinction is lost: “effettuare la verifica” can become “verificare.” Keep a defined term that later clauses depend on. Examine a `gerundio` when its actor, cause, or result is unclear; use a finite clause to resolve that ambiguity, not as a universal replacement.

For equal alternatives, “o” or “oppure” states the relation directly. Keep “piuttosto che” when genuine preference is intended. Preserve established technical borrowings and the writer's register rather than adding formal synonyms. Retain “tuttavia” or “perché” when removing it would lose contrast or cause.

## Chinese

Resolve script and regional convention from the task, publication, or supplied text. `zh-CN`, `zh-TW`, and `zh-HK` do not share every term or punctuation convention; Traditional or Simplified script alone does not establish region. Preserve the document's convention when region is unknown and the choice does not affect use.

Keep official names, quotations, UI strings, code, and identifiers intact. Converting script can change vocabulary and locale meaning; make that change only when localization is in scope. Do not batch-replace terms such as `软件/軟體` or `用户/使用者` merely to make them uniform across regions.

Clarify dense modifiers or repeated framing when they hide the main relation. For example, “在系统发生故障的情况下” can become “系统故障时” when both express the same condition. Retain a preposition, pronoun, or `的` phrase that disambiguates scope, actor, recipient, or an official term. Reduce parallel praise when it repeats one claim; preserve genuinely different requirements or stages.

Leave line-breaking, hanging punctuation, and page-edge behavior to the renderer or typesetter. Manual spaces and source line breaks are not a general repair for Chinese typography.

## Basis and reuse

The authoring, revision, voice-preservation, and language guidance in this package adapts selected methods from [slop-aware-writing](https://github.com/gigio1023/slop-aware-writing/tree/0eb3b774d124302bdd9ed0fcbe184a50cde90ec3/slop-aware-writing), copyright 2026 gigio1023, under the [MIT notice](../LICENSE.slop-aware-writing). This synthesis selects semantic and reader-task decisions; it does not import that package's pattern-count policies. The Korean tells and the Korean clarity rules in [Korean writing](korean-writing.md) were merged from slop-aware-writing and korean-clarity at their 2026-09-21 revisions; empirical claims are retained in [Korean pattern evidence](korean-pattern-evidence.md), with their evidence class and limits. The examples here are independently synthetic. Public technical close readings remain in [writing sources](https://github.com/gigio1023/gigio-skills/blob/main/docs/writing-sources.md).
