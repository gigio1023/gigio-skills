# Voice and Factual Prose

Use while drafting or revising sentences and paragraphs, in any language. [Synthetic examples](synthetic-examples.md) show complete rewrites, and [multilingual writing](multilingual-writing.md) covers language-specific choices.

## Subjects, verbs, and register

Make the technical subject do the work: the scheduler assigns, the worker acknowledges, the client retries, the measurement records. Prefer the actual operation to a prestige synonym: a component does not merely “enable seamless orchestration” when it queues jobs and retries failures. Keep an established term such as backpressure or linearizability when it names the behavior precisely. Replace vague praise with the invariant, mechanism, or observed result that would justify it.

Use present tense for defined behavior and mechanisms, past tense for an observation at a known revision, and proposal language for a design that has not been implemented. State the result or change directly: “The replay recorded…” or “Store the cursor after the commit.” A heading such as “Proposed cursor storage” can establish proposal status without repeating “we propose” in each paragraph. Do not hide a proposal behind “the system supports” or turn a team's belief into a community consensus.

Default to subject-centered prose in technical and shared reports. Remove “my findings,” “the author's synthesis,” and ornamental author/date introductions when page metadata or the sharing context already supplies them. An observation date, source attribution, or action owner can still change the meaning and belongs with the relevant fact. Keep required bylines in their metadata position. First-person voice is appropriate when explicitly requested, required by the destination's genre, or needed to distinguish firsthand testimony or responsibility; merely permitting it is not a reason to add a narrator.

Replace abstract process language with the actor and action when that makes the meaning clearer: “The service owner approves the change” states a responsibility. Keep an authority relationship when the system depends on it. “The cache is not a source of truth” can distinguish a disposable copy from authoritative state; a description of a cache miss alone does not preserve that contract.

## Clear sentences

Make the relation easy to follow. Keep a connected cause, condition, or contrast in one sentence when it reads naturally; separate unrelated claims or steps that the reader needs to perform independently. A sentence does not become unclear at a fixed word count, and a paragraph does not become clear by meeting a sentence quota.

Name an actor when responsibility or a changing subject matters. Use the passive when the actor is unknown, immaterial, or already established. Keep articles, particles, endings, and predicates that carry meaning. Unpack a noun cluster when its modifiers are ambiguous, while preserving an established technical term.

Use consistent names for the same entity, not a single generic word for distinct operations. In English, schema validation, signature verification, and receipt confirmation can be different actions. “Robust regression” names a statistical method rather than praising its quality. Read [English clarity](english-clarity.md) for STE-inspired instruction and terminology work; read [Korean writing](korean-writing.md) for natural Korean syntax. Neither guide makes length or a pattern count a quality gate.

### Meaning-preserving examples

**English description.** Original: “The cache layer, which is responsible for reducing load on the database, is not a source of truth, and entries may be evicted at any time by the eviction policy, so callers should always be prepared to re-fetch data from the database if a miss is encountered.”

> The cache reduces database load but is not a source of truth. The eviction policy may remove entries at any time, so callers should always be prepared to fetch data from the database again after a cache miss.

The revision keeps the authority boundary, possible eviction, and the recommendation to prepare. It does not claim that callers already implement the fallback. The causal connection remains in the second sentence because it explains why callers need that preparation.

**Korean description.** 원문: “이 job은 실패하면 scheduler에 의해 재시도되는데, 재시도 횟수는 설정 파일에서 관리되고 있으며 최대 횟수에 도달하면 dead-letter queue로 이동되므로 운영자의 확인이 필요하지만 알림은 자동으로 발송되지 않는다.”

> job이 실패하면 scheduler가 다시 실행한다. 재시도 횟수는 설정 파일에서 관리하며 최대 횟수에 도달한 job은 dead-letter queue로 이동한다. 운영자가 확인해야 하지만 알림은 자동으로 발송되지 않는다.

재시도와 이동 조건, 운영자의 확인 필요, 자동 알림의 부재를 보존했다. 원문이 이동 주체를 명시하지 않았으므로 scheduler가 옮긴다고 추가하지 않았다. 연결어미를 세는 대신 각 조건이 어느 동작을 제한하는지 확인한다.

## Keep each author's voice in revision

When one pass revises texts by several people, or one author's notes written in different registers, keep each text's own register, stance, and recurring choices; do not converge them toward one safe middle voice. Keep hedges that mark genuine doubt, keep the author's first person and explicit causal chains, and do not swap plain words for rarer synonyms to sound polished.

## Make each paragraph carry a relation

Choose a paragraph's job: describe behavior, explain a mechanism, report an observation, compare alternatives, or justify a decision. Start where the reader can orient, then supply the evidence or technical sequence, and include the consequence if it is not already apparent. This is a reasoning pattern, not a mandatory three-sentence form.

Move from a known component or problem to the new detail. Keep a condition next to the action it constrains. When a system has multiple steps, describe the ordered state changes rather than joining component names with arrows and leaving their relationship implicit. A paragraph can end after the mechanism is clear; it does not need an inspirational takeaway.

A transition must name a real relation. “Because” requires a causal explanation; “therefore” requires an inference supported by the preceding statements. If the source shows only co-occurrence, report it without manufacturing the missing experiment.

## Test generic sentences

Use these tests when a sentence reads fluently but may carry no fact. They apply in any language; the examples are English. A failed test marks a sentence for repair, and several distinct failures in one passage mark the passage, as [authoring and revision](authoring-and-revision.md#revise-explicit-ai-slop-requests) describes.

- **Portability.** Could the sentence move into another project's document unchanged? Then it says nothing about this one. "Reliability is a core priority for the team" fits any team; "Each write is acknowledged after two replicas persist it" fits one system. Replace the portable sentence with the fact it stood in for, or delete it.
- **Literal operation.** Name the operation instead of borrowing a metaphor or a figurative verb for it. Code and configuration do not know, want, or care: "the config knows about the queue" becomes "the config lists the queue". A lever, surface, or flywheel becomes the change, interface, or feedback loop it stands for. Verbs for literal operations, such as reads, rejects, and validates, stay, and so do established terms such as backpressure.
- **Contrast with a real holder.** The negative half of a contrast needs someone who holds that view: the reader, a cited source, or an earlier section. Two patterns add weight without adding a claim: a contrast split across two sentences, such as "This does not mean X. It means Y.", and a rebuttal of a position nobody in the document holds. State Y directly. Keep the contrast when it corrects a belief the reader is likely to bring.
- **Emphasis source.** Flatten the sentence: remove its cadence, contrast, and intensifiers while keeping the claim. If the flat version still names an actor, a mechanism, or a limit, the claim stands; prefer the flat version unless the original emphasis serves the reader. If nothing remains, the emphasis came from the pattern, and the sentence goes.
- **Syntax relation.** When syntax implies a relation, as with two short sentences side by side, a dash, or a colon, restate that relation with because, although, or so that. If the evidence supplies the connective, write it. If no connective can be supplied without inventing it, the syntax stood in for a relation the source does not establish: report the facts separately or ask the author.

The portability and literal-operation tests adapt EveryInc's `ce-noslop` skill in [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin/tree/a3bcedfc7136/skills/ce-noslop), whose catalog also supplies the config example. The contrast test adapts the "Not X but Y" and "Arguing with no one" patterns in [blader/humanizer](https://github.com/blader/humanizer/tree/0ef9fe5bc357). The emphasis-source and syntax-relation tests adapt [adewale/anti-slop-writing](https://github.com/adewale/anti-slop-writing/tree/5cf773433c6c). All were read on 2026-11-04.

## Express the status inside the fact

| What is known | Useful construction | Do not silently turn it into |
| --- | --- | --- |
| Observed behavior | “In the replay, the worker retried the rejected items.” | A guarantee for all workloads |
| Measured comparison | “At the tested concurrency, p95 latency was lower with the bounded queue.” | A universal performance advantage |
| Estimate | “The estimate uses completed requests and the observed mean payload size.” | A measured total |
| Hypothesis | “Queue contention may explain the tail; the run did not measure lock wait.” | A confirmed root cause |
| Proposal | “Store the cursor after the batch commit so a retry can resume from the last durable batch.” | Existing implementation behavior |
| Decision | “Use the bounded queue because the consumer's drain rate limits useful parallelism.” | A choice attributed to people who did not approve it |
| Unknown | “The trace ends before the worker exits.” | “The worker never exited.” |

State the actual gap rather than hedging every clause. “No measurements were collected above this concurrency” identifies the unsupported range. Repeated “may,” “potentially,” and “not guaranteed” language is not a substitute for naming the missing evidence. A status word should describe the subject's state, not the author's confidence in the document.

Preserve the force of requirements. In ordinary project prose, distinguish a required precondition from a recommended default and an optional choice. When the destination adopts BCP 14 terminology, preserve its convention and exact uppercase keywords; do not import standards boilerplate into a memo merely to make it sound authoritative. [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) explains the uppercase convention.

## Technical explanation and definitions

Introduce a definition when the reader needs a nonstandard meaning, a precise measurement boundary, or a new abstraction to follow the next step. Put it at first useful use. An experienced audience does not need an explanation of what a dashboard, latency, or a caption is. It may need to know whether this latency includes queueing and retries.

An internal nickname is not a definition. Prefer the established domain term for what the artifact actually is; if none fits, use a plain functional description. Introduce an exact local alias once when lookup requires it, attached with a colon or apposition rather than parentheses, then use the meaningful name consistently. For example, “the labeled evaluation dataset, internal ID `review-set-r3`” explains the role while preserving the identifier. It does not claim that every label was reviewed by a person. Terms such as “gold standard,” “validated,” and “ground truth” require corresponding evidence or an explicitly defined convention; a local filename cannot establish those properties.

Explain an abstraction through its contract and an example: input, transformation, output, ownership, and relevant failure behavior. Use pseudocode when execution order or state transition is difficult to express unambiguously in prose. Explain what the pseudocode abstracts away only when the omission matters. A mechanism diagram and the surrounding text should use the same component names.

Distinguish an analogy from an implementation. If an analogy needs a paragraph explaining everything that does not map, use the actual mechanism instead. A familiar example can teach a concept, but it cannot provide evidence for the system being evaluated.

## Sources, citations, and detail placement

Place a citation where its scope is clear: beside the reported value, mechanism, comparison, or attributed claim. Prefer the paper's relevant section/table, a source permalink, or a maintained specification to a product home page. Preserve source versions when an API, policy, or result could change. Summarizing several sources does not make them independent evidence if they all repeat one experiment.

A caption or lead-in that only restates the command or code below it, such as “다음 명령어로 의존성을 설치합니다” above `uv sync`, is deleted. Keep it when it says why, when, for whom, or with what scope the command runs, which the command itself does not show.
