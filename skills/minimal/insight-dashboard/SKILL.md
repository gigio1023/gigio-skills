---
name: insight-dashboard
description: >
  Use when creating or redesigning a data dashboard, leaderboard, interactive analysis report, operational view, or static dashboard for print. Decides what the view compares, its metrics and denominators, how selections and filters change values and rankings, and its explanatory text, so results stay selection-consistent. Phrases include "build a dashboard for these results", "make a leaderboard", "대시보드 만들어줘", and "리더보드 만들어줘". NOT for generic forms or landing pages, ordinary prose documents, interface work that changes no comparison, metric, or explanatory text, such as restyling components or fixing a layout (frontend-design), or static figures (technical-figure, when installed).
---

# Insight Dashboard

Build a data view that helps the reader answer a recurring question or choose an action. Make the useful comparison visible in the initial view, then provide a clear path to the details that explain it. Let data and the reader's task determine the layout.

This skill decides what the view compares, its metrics and denominators, how selections change the results, and its explanatory text. `frontend-design` builds and reviews the interface that carries those decisions in the project's UI stack: components, layout, states, responsive behavior, and accessibility. Use both when building or redesigning a view; an interface-only change that alters no value, ranking, or sentence the reader sees needs only `frontend-design`.

Preserve the project's data model, terminology, and requested medium. Inspect supplied data before choosing claims. Use authorized real results; mark development fixtures as synthetic. If a missing input prevents the main comparison, identify that input and build only the supported views. Review requests return findings rather than changing the application.

## Choose the first useful view

- **Communicate a finding:** lead with the supported finding and decisive comparison, then the factors, exceptions, and observations that explain it. Add exploration for a concrete follow-up question.
- **Investigate:** start with a meaningful baseline, visible selections, and enough context to choose a population. Link overview, breakdown, and record detail so the reader can narrow a question.
- **Monitor:** prioritize affected services, severity, freshness, and the next operational action. Keep severity separate from investigation status; distinguish unavailable telemetry from healthy service.
- **Review periodically:** connect previous actions to current measures and the next proposed action. Associate human commentary with its period and evidence. Add explanations where judgment matters rather than requiring a comment on every card.
- **Answer a small recurring question:** show the answer and the useful next link. A current-version page can be complete without a KPI grid or trend chart.
- **Rank candidates:** rank only rows measured under the same comparison, show each row's comparability, and keep the ranking claim true under the reader's filters. The [ranking pattern](references/pattern-examples.md#rank-candidates-on-a-fixed-comparison) covers ties, missing cells, and metrics with opposite directions.

## Compose the comparison

1. **Put the reference beside the value.** Pair the current measure with the relevant prior period, target, baseline, capacity, or denominator. Explain a changed definition where it changes the comparison.
2. **Give the decisive evidence room.** Use tables for exact lookup, aligned bars or dots for categories, lines for time, and distributions for variation. Let supporting details have less emphasis. Choose axes and grouping for the question rather than visual drama.
3. **Connect overview to variation.** Show the important subgroup, tail, or exception when an aggregate could conceal it. A rate may need its sample count; an average may need the affected records. Select these additions by their effect on interpretation.
4. **Assign text complementary roles.** The heading states a supported finding or useful question; the chart shows the comparison; labels identify quantities; a note states material conditions; prose explains the implication. Write one clear explanation instead of repeating the finding across cards and captions.
5. **Carry meaning through the states.** Derive values, rankings, titles, and explanatory text from the same selection, or visibly separate fixed analysis from exploration. Keep missing, stale, failed, and zero distinct.
6. **Make timing and sources useful.** Show the observation period or latest observation beside the result when freshness affects interpretation or action. Label retrieval time separately when it matters; a build timestamp measures neither. Preserve appropriate selection state in a hosted URL and link useful authorized definitions or source data. A URL identifies a selection, not an immutable snapshot; retain a dataset version or snapshot when reproduction requires one.

In a **synthetic service comparison**, a successful-request median alone may favor a configuration with more timeouts. Show completions alongside latency and explain the trade-off. The good result is a reader who can choose under a stated reliability requirement, not a uniformly green row of cards.

## Load the detail that changes a decision

- [Data and comparison](references/data-and-comparison.md): denominators, aggregation, uncertainty, chart selection, finding structure, and worked arithmetic.
- [Pattern examples](references/pattern-examples.md): task-matched public dashboards, actionable adaptations, and finished synthetic view specifications, including a leaderboard.
- [Interaction and static delivery](references/interaction-and-static.md): selection changes, asynchronous updates, refresh deltas, copying a selection as text, URL sharing, error states, and print.

For document-level information selection, prose, and internal sharing, use `copydesk`. For a shadcn implementation, use the [official shadcn skill](https://ui.shadcn.com/docs/skills) when available; otherwise consult the official component documentation. These companions contribute to this artifact; they do not restart intake. Without them, retain supported claims, accessible interaction, sufficient comparison conditions, and recipient-appropriate sources.

For print-first output, use a native document-production route. Web and PDF can share data and calculations while using different layouts. In the static view, expose the selected comparisons and labels that the reader otherwise accesses through tabs or hover.

## Verify the complete reader task

Independently calculate representative values and compare them with the table, chart, headline, and export. Exercise the initial view, a selection that changes the conclusion, and an empty or unavailable-data case. Verify the relevant URL restore, reset, keyboard, and drill-down paths. For live data, test freshness and failure without replacing the last valid observation with a fabricated zero.

Inspect the delivered size and a narrow viewport, plus the actual PDF or offline artifact when requested. Before delivery, check:

- Does the initial view expose the useful comparison, supported finding, or operational action for this task?
- Are material conditions beside the claims or views they change, with important failures and denominators preserved?
- Do definitions and interaction explanations answer a real reader question, with routine use handled by clear labels and controls?
- Do production details and verification records help this reader compare, reproduce, audit, or act? Omit irrelevant narration without automatically moving it to an appendix.
- Where the view contains prose, are paragraphs organized by meaning without fixed-column source wrapping? Choose rendered line width for the medium and readability; it is a separate layout decision.

Deliver the working source and requested output, with a short account of checks actually run. Keep routine build logs and verification narration in the working record. Include a record in the reader artifact only when it serves the task above, placed with the affected result or in useful source or methods detail. Publish only within the user's grant.
