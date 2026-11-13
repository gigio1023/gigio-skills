# Document Forms

Use when choosing or revising a document's structure. Begin with the reader's task, genre, and governing template. When that form is unfamiliar, read a real technical exemplar; public source pointers are kept in [writing sources](https://github.com/gigio1023/gigio-skills/blob/main/docs/writing-sources.md).

Vary the explanation and reading order by purpose. A factual record's brevity is not a reason to omit mechanisms from a guide or reasons from a proposal.

## Contents

- [Guide or explanation for a new reader](#guide-or-explanation-for-a-new-reader)
- [Decision memo or proposal](#decision-memo-or-proposal)
- [Post, essay, or personal account](#post-essay-or-personal-account)
- [Technical report or experiment report](#technical-report-or-experiment-report)
- [Design proposal, RFC, or enhancement proposal](#design-proposal-rfc-or-enhancement-proposal)
- [Delivery brief](#delivery-brief)
- [Architecture or mechanism explanation](#architecture-or-mechanism-explanation)
- [Architecture decision record](#architecture-decision-record)
- [Incident report or postmortem](#incident-report-or-postmortem)
- [Periodic review or progress report](#periodic-review-or-progress-report)
- [Project overview, reference, or runbook](#project-overview-reference-or-runbook)

## Guide or explanation for a new reader

Start with the task or concrete problem that makes the subject useful. Give the reader enough context to follow the first example, then introduce the concept or distinction needed for the next step. A beginner may need a familiar term explained; an experienced reader may need only its nonstandard local meaning.

Keep prerequisites before the actions they constrain. Use examples with enough context to work, and distinguish illustrative output from verified behavior. Let the depth follow the reader's need rather than turning every guide into an exhaustive reference. End when the reader can perform the intended task or explain the concept; add a recap only if it helps retain or apply what was learned.

Introduce the concepts needed for the next example, not an obligatory textbook chapter or exhaustive glossary before the reader reaches the useful question. Use a short mechanism explanation alongside the visual; a sequence of definitions and labeled boxes alone does not teach why the system behaves as it does.

## Decision memo or proposal

Make the requested decision, recommendation, or change clear early, with the reasons needed to evaluate it. Show credible alternatives on common dimensions and name the constraint that decides this case. Preserve uncertainty that affects the choice; avoid an inventory of every hypothetical objection.

Include ownership, timing, cost, or follow-up when the decision requires them and the source supplies them. A recommendation is not an approval, and an accepted proposal is not an implementation. Short memos can make their case in a few paragraphs without an executive-summary template.

## Post, essay, or personal account

Use the requested voice and the author's perspective. An opening example, question, scene, or claim can lead when it gives the reader a reason to continue. Develop the actual idea rather than replacing it with a generic conclusion-first report.

Keep a personal detail, aside, or stylistic repetition when it advances the account or carries the writer's voice. Remove generic significance claims and stock closing advice that the piece does not earn. Distinguish the author's experience or opinion from an externally established fact, and preserve attribution for quotations. Editing for clarity does not authorize inventing experience or making the narrator more certain.

## Technical report or experiment report

The reader needs to know what was tested, what happened, why the result is informative, and what it changes. Open with the question and supported result. Then expose the decisive evidence and the method needed to interpret it. A report can lead with a negative result or an unresolved comparison; it does not need a positive product story.

Connect the chain: hypothesis or engineering question → tested intervention or comparison → measurement conditions → observed result → warranted interpretation. Put workload, baseline, version, trial unit, and exclusions where their absence would mislead. Separate the measured behavior from a suggested explanation. An ablation tests a component's contribution under its conditions; it does not by itself establish performance everywhere.

Explain why the selected workload represents the intended use and where it does not. A synthetic microbenchmark can isolate a mechanism but does not substitute for end-to-end behavior. Report relevant contrary results and side costs rather than compressing them into a single favorable aggregate. Preserve enough method detail to rerun or audit the result; link full configurations and raw results when their distribution is authorized.

End with the supported engineering implication or next discriminating test, not a ceremonial summary. If a recommendation is requested, make it and name the observation that would reverse it. [MapReduce](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) separates programming model, implementation, configuration, and experiments; [Circuit Tracing](https://transformer-circuits.pub/2025/attribution-graphs/methods.html) separates the proxy model, validation, and method-specific failures.

## Design proposal, RFC, or enhancement proposal

The reader needs to assess a change before treating it as implementation fact. State the current behavior or constraint, the proposed behavior, and why the change is needed. Explain the mechanism in enough detail to reveal its trade-offs: responsibilities, interfaces, state, data flow, compatibility, and failure behavior as applicable.

Give a concrete usage example before reference-level detail when it helps the reader understand the new interface. Then specify the semantics that the example cannot settle: ordering, lifetime, ownership, concurrency, error handling, and migration. Keep guide-level explanation and exact specification aligned. Rust RFC 2394 demonstrates this two-level structure; its historical syntax is not a current API reference.

Compare plausible alternatives against the same important constraints. Include the status quo when it is a credible option. State an alternative's advantage before the reason it loses here. Avoid an arbitrary scorecard in which invented weights make the desired answer win.

A compatibility note belongs beside the changed interface, with migration or rollback steps where someone must act. Use separate non-goals only when they prevent a likely consequential misunderstanding or a governing template requires them. Do not enumerate everything the proposal does not attempt. A short project proposal does not inherit Kubernetes' release governance, approval gates, or every production-readiness question; use the relevant technical questions without importing an unrelated organization.

Keep unresolved questions that affect the design, with the evidence or decision needed to resolve them. A list of speculative future features is not an unresolved-questions section. Preserve proposal status, decision history, and supersession when the project uses them; a merged document is not automatically an implemented feature.

## Delivery brief

Use a delivery brief for customer- or deadline-bound product work, when the people who build, accept, and decide need one short page that says what will be delivered, by when, and how acceptance will be judged. It is not a product requirements spec or a set of user stories, and it never replaces the design document: the brief states the promise, and the design document states how the system meets it. The brief links the technical design and the plan instead of restating them.

Give each part only the length its content needs:

- **Outcome and decision:** what changes for the user or customer when the work lands, and whose decision it serves, by role.
- **Workflow:** the part of the user's workflow the work touches, as it runs now and as it will run.
- **Promised behavior and exclusions:** behavior someone can observe and check at acceptance, and the explicit exclusions a reader would otherwise assume are included.
- **Priorities and deadline:** which promised behavior comes first if time runs short, and the deadline with the commitment it is tied to.
- **Acceptance:** the evidence that shows each promise is met, such as a run on named data, an evaluation result with its conditions, or a walkthrough of the workflow, and the role that accepts it.
- **Open decisions:** undecided items as questions, each with what it blocks and who settles it.
- **Links:** the technical design document and the plan or tracker project.

Write promised behavior as what the user can observe, not as implementation tasks. A behavior whose feasibility rests on an unmeasured bet stays an open decision until a measurement or the accepting role settles it. When the design, a measurement, or the deadline changes what can be delivered, update the promise, exclusions, priorities, and open decisions together. For a learned or judged component, acceptance names the metric, the data it is measured on, and the conditions, not a bare number.

## Architecture or mechanism explanation

The reader needs a usable mental model of an existing system. Start with the boundary that matters to the explanation, not a catalog of every repository or infrastructure component. Show the components involved in the path being explained and name their responsibilities. Trace a representative request, record, or job through them.

Explain the invariants and transitions: what is stored durably, what is only in memory, when ownership changes, what can be repeated, and how the system behaves when a dependency is unavailable. Distinguish control flow from data movement. Show trust boundaries when security or access determines the interaction. A box labeled “security” cannot stand in for an actual authorization check.

Keep names consistent with the code and reader-facing terminology. Do not claim current behavior from an old design document without checking the implementation.

## Architecture decision record

An ADR records a consequential choice and why it made sense under the conditions at the time. State the decision question, relevant forces, considered options, chosen option and reason, and consequences. Keep a real drawback in the decision record so the next maintainer does not rediscover it as a surprise.

Write “We chose X because Y” when a choice was actually made; use proposed status when it was not. Preserve the accepted record and supersede it through the project's process instead of rewriting history to fit a new decision. An ADR is not a retrospective benchmark or a full system design. [MADR's own format decision](https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html) makes the question, options, and outcome inspectable.

## Incident report or postmortem

Resolve whether the requested document is a factual incident record or an explanatory postmortem. A factual record can be complete with concise observations, a chronology, grouped findings, and response actions. Do not invent a root cause, recommendation, or prevention program to fill a template. An explanatory postmortem needs the supported causal reasoning and corrective actions below.

Lead with the affected service or behavior, user-visible impact, duration when known, and current recovery state. Separate the trigger from the conditions that let it become an incident. Explain the causal sequence with evidence, and mark a suspected link as suspected instead of filling it with a plausible story.

Include the timeline entries that locate detection, diagnosis, mitigation, recovery, and consequential decisions. Preserve time zones and distinguish a system event from when responders learned about it. Omit a transcript of routine activity. A change preceding recovery is not automatically the fix; explain what evidence connects them.

When corrective actions are part of the requested scope, they should address the mechanism or detection gap and have an observable completion condition. Avoid “improve monitoring” without naming the signal and response it should enable. Keep accountable ownership appropriate to the recipients without blame or erasure. The Google SRE example demonstrates separation of impact, cause, trigger, resolution, actions, and timeline; it is a fictional teaching example, not an actual Google outage.

## Periodic review or progress report

The reader needs to connect prior work to current evidence and choose the next useful action. Open with the consequential change or unresolved issue. Relate the relevant previous action, current observation, comparison, and proposed next step. A status report can be complete with a few grounded paragraphs; a dashboard can provide the supporting exploration.

Bind commentary to the period and population it explains. Link deeper evidence where recipients can access it. Keep definition changes and missing observations near the affected comparison. State a causal explanation only when its evidence supports it; otherwise distinguish the observation, working hypothesis, and next investigation. Choose sections by the work being reviewed rather than allocating an explanation slot to every metric.

## Project overview, reference, or runbook

A project overview explains what the project does, where it fits, the main entry points, and how to perform the first relevant task. Preserve enough context for a newcomer without teaching familiar infrastructure. Point to the canonical code, API, and maintenance docs rather than duplicating changing information.

A reference organizes exact interfaces and behavior for lookup: parameter or field, type, valid values, default, effect, and relevant error. Describe interactions between fields where they matter. Do not bury a required condition in a motivational introduction.

A runbook organizes actions by the actual symptom or task. State prerequisites before the action they constrain, the command or operation, the observable result, and the next step on failure. Distinguish inspection from mutation. A command example that has not been exercised is not a verified procedure. Avoid documenting credentials or copying a private environment into a public example.
