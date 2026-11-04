# Interaction and Static Delivery

Use when selections, live updates, sharing, or printing change what the reader sees. Verify the data, displayed population, and interpretation as one task.

## Carry selection through the result

Make active population, period, and comparison baseline visible. Persist appropriate filter state in the hosted app's URL and restore it on reload and navigation. Validate malformed values, reconcile dependent filters, and reset to a meaningful default. Keep sensitive values out of shared URLs where the access boundary requires it.

Derive selection-dependent rows, totals, rates, rankings, title, chart, and export from the same filtered result. When commentary belongs to a fixed investigation, attach its period and population and separate it from the exploratory view. On a date change, use matching commentary or say that none has been recorded; present a hypothesis as a hypothesis.

A shared URL identifies the requested view. Live data behind that URL can change. For an immutable record, retain an authorized dataset version, snapshot, or exported result with the period and conditions needed to interpret it. Retrieval time alone does not identify an immutable dataset.

Let a finding leave an interactive view as text. A copy action can place the current selection on the clipboard as a short Markdown block holding the selection, the key values with their denominators and period, the finding sentence, the as-of time, and the view's URL. A URL-only copy suits a reader who will open the view. Build the copied text from the same filtered result as the visible view so it changes with the selection. Where clipboard access may be blocked, as in a sandboxed host frame, show the same text in a selectable block.

Distinguish observation time, retrieval time, and build time. Observation time says when the measured activity occurred; retrieval time says when the source was read; build time says when the artifact was generated. Show the first where freshness changes interpretation or action, and the others only when the reader needs them for source latency, reproduction, or artifact identity. A recent build cannot make old observations current. Put concise timing labels by affected values and longer useful provenance with sources or methods; omit production receipts that serve no reader task.

## Make asynchronous behavior intelligible

Associate each request with its selection and ensure that an older response cannot replace the result of a newer selection. During loading, either retain the previous view with a clear pending state or show a suitable placeholder. Preserve controls and keyboard focus where possible.

For monitoring, show the last observation time and the freshness rule relevant to use. A failed refresh can retain the last valid result. Show the retrieval failure and mark observations stale only when they exceed that rule. Distinguish service failure from missing telemetry. Offer pause when freezing a live time window helps investigation, and make resumed updating visible.

A view regenerated or refreshed on a schedule, such as a weekly status page or a rebuilt report, opens with its as-of time and what changed since the previous refresh. The as-of time is the latest observation the view reflects, or the retrieval time for a state snapshot such as open-item counts; label which one it is. Compute the change list from stored state: keep the previous refresh's values in the artifact or beside it and compare them instead of recalling them. List what a reader would act on, such as new and resolved items, status changes, and values that crossed a threshold or changed rank. "No change since" the previous as-of time is a complete result. A first refresh says that no earlier state exists rather than inventing a delta, and a failed retrieval keeps the previous values marked stale rather than reporting them as unchanged.

Use precise state language:

- **No matching observations:** preserve the filters and offer the relevant reset or broaden action.
- **Zero observed:** display the measured zero with its valid denominator or time window.
- **Unavailable source:** identify the failed retrieval and provide an appropriate retry or source-status path.
- **Stale observations:** retain the observation time and indicate why the value may no longer describe the present.

## Make interaction teach itself

Use visible, local labels and conventional controls. Name the parameter changed by a slider and show its value; tell the reader what the demonstration is meant to reveal. Provide keyboard operation and a reset for explorations that need a baseline. Put essential interpretation in visible text rather than only in a tooltip or color.

For overview-to-detail navigation, carry the relevant filters and provide a useful return path. For a map or canvas, offer an accessible alternative to the essential result. Adopt motion when it explains a transition, with reduced-motion support where applicable.

## Verify changes in meaning

Choose tests from the actual task:

1. Open the default view and verify a representative value and its reference.
2. Change to a population that materially changes or reverses the finding; check every dependent representation.
3. Exercise empty, failed, stale, and zero-denominator states where applicable.
4. Restore a shared URL, use browser back, and reset. Confirm the selected state and derived results match.
5. Under delayed responses, change selections rapidly and verify the final response belongs to the latest selection.
6. Use the keyboard and inspect narrow-width labels, focus, and overflow.
7. Compare an exported or copied selection with the visible data and definition.

A button click proves an action occurred, not that the intended data or explanation changed. Verify the expected output. Live values changing after a toggle, a changed screenshot hash, or a similar widget working elsewhere cannot establish that semantic result.

## Turn exploration into a printable argument

Choose the comparison and conditions the document should communicate. Replace tabs and hover details with visible panels, annotations, or a compact table. Keep the important contrary result on the reading path. Remove interaction chrome while preserving the selected period, population, source, and relevant data version.

Reuse source data and transformations across outputs, while allowing print-specific typography, layout, and light backgrounds. A native Typst or DOCX report is a valid endpoint without a web application. For a browser export, wait for data, fonts, and charts before printing, expand necessary content, and inspect the resulting PDF.

Check readable labels, searchable text, citations, page boundaries, repeated table headers where needed, and complete selected data. An offline HTML deliverable must also work from the delivered file with network access disabled. A dev-server screenshot is evidence of the development view, not of either distributable.

Foundations: [Segel and Heer, section 4.4](https://idl.uw.edu/papers/narrative), author-directed explanation and reader-directed exploration; [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines), usable controls and URL state; [Red Blob Games](https://www.redblobgames.com/grids/hexagons/), linked representations and print trade-offs. Apply these according to the reader task rather than making every report interactive.
