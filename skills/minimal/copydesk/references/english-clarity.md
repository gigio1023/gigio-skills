# English Clarity

Use for English instructions, tool descriptions, error and status text, or prose whose actor, condition, or terminology is easy to misread. The goal is a precise reading with the source's meaning intact. The writing profile's dry register applies where requested; another writer's voice remains part of a revision.

## Interpretation before wording

Identify what the reader must understand or do, the object they act on, and the conditions that change the action. Check references and scope before shortening. If two plausible readings would change behavior, resolve them from the source or ask about the missing fact. A smoother sentence cannot settle an ambiguity the evidence leaves open.

Useful changes include:

- Name the responsible actor when responsibility matters. Passive voice remains useful when the affected object is the topic or the actor is unknown.
- Place a prerequisite before the action it governs. Separate steps that have different actors, conditions, or failure handling; keep one naturally combined operation together.
- Replace an indirect action phrase with its verb when the distinction is unchanged: “review the log” can replace “perform a review of the log.”
- Repeat a defined term for the same concept. Check the referent before treating different words as synonyms.
- Restore an article, subject, or explicit object when omission permits the wrong reading. Unpack ambiguous modifiers without renaming an established technical term.
- Remove praise that supplies no evidence, while keeping a word that names a method, property, or observed result.
- Test a fluent sentence that may carry no fact, such as a portable claim, a figurative verb, or a contrast with no holder, with the [generic-sentence tests](authoring-and-revision.md#test-generic-sentences).

Keep useful causal and contrastive clauses. Choose sentence and paragraph boundaries by meaning and reading effort; this guide has no word, noun-stack, or sentence-count limits. Plain verbs are often easier to read, but a familiar phrasal verb is not automatically ambiguous. Keep tense and aspect when they distinguish past events, ongoing activity, completed work with current consequences, or hypothetical events.

## Semantic checks

The examples are independent teaching cases. Their unchanged wording is sometimes the correct editorial result.

| Input | Editorial decision | Meaning to preserve |
| --- | --- | --- |
| Validate the request schema. Verify the digital signature. Confirm receipt with the sender. | Keep the distinct verbs. | Schema conformance, cryptographic verification, and acknowledgement are different actions. |
| We fit a robust regression model to reduce outlier influence. | Keep `robust regression`. | It is a statistical term, not unsupported marketing praise. |
| The request may have failed. | Keep `may have failed`. | Both uncertainty and a possible past event matter. |
| The worker should retry failed requests. | Keep the recommendation level. | `Should retry` does not establish that the worker retries. |
| The job has completed, and its output is available now. | Keep current relevance. | A change to a past event alone could drop the present status. |

When a sentence combines a vague frame and real uncertainty, remove only the frame. “It is important to note that the request may have failed” can become “The request may have failed.” Do not add a diagnosis or a recovery action unless it is supplied or separately supported.

Compare before and after for actor, action, object, condition, negation, scope, time, frequency, permission, requirement, and confidence. Keep `must`, `should`, `may`, and `can` distinct where they serve those roles. In a normative standard, preserve the standard's exact keyword convention. Ordinary prose does not need standards boilerplate.

## Explicit controlled-English requests

Use ordinary clarity work by default. If the user requests a strict controlled-language specification, identify the required standard and apply the constraints that are actually in scope. Exact ASD-STE100 compliance requires the authorized current standard and its dictionary; this package cannot certify it. Resolve a conflict that would change the technical meaning instead of silently shortening away a condition. Keep the mode analysis out of the delivered text unless the user requests it.

## Tools and provenance

`check_draft.py` is an optional advisory locator for possible padding and dense presentation. It does not establish whether two verbs mean the same action, recognize every domain term, or prove semantic fidelity. Read each finding in context and keep legitimate language. A clean output can still be vague or unsupported.

These principles synthesize selected ideas from Dustin Yuchen Teng's [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), inspected at package version 0.4.0, with copydesk's meaning-preserving revision method. The [MIT notice](../LICENSE.asd-ste100) retains that source's attribution. This package does not import its checker, fixed length rules, automatic strict mode, or dictionary. ASD's official standard and dictionary are not reproduced. See the [official standard site](https://www.asd-ste100.org/) when the task requires the standard itself.
