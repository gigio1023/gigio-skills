# Surface Patterns

## Contents

- [Product App](#product-app)
- [Form-Heavy Service](#form-heavy-service)
- [Dashboard Or Data Visualization](#dashboard-or-data-visualization)
- [Static HTML Report](#static-html-report)
- [Landing Or Brand Page](#landing-or-brand-page)
- [Portfolio Or Career Page](#portfolio-or-career-page)
- [Game Or Interactive Demo](#game-or-interactive-demo)
- [Docs, Guides, Or Knowledge Tools](#docs-guides-or-knowledge-tools)
- [AI Or Generative Interface](#ai-or-generative-interface)

Pick the surface by its user job. A product may combine patterns, but one job should determine the primary hierarchy.

## Product App

Purpose: repeated use, fast scanning, low friction.

Design for:

- Predictable navigation, clear entry and exit points, and one primary action per working region.
- Useful density with little decoration competing with the work.
- Loading, empty, error, success, disabled, hover, active, and focus states.
- Controls that match intent: toggles for binary state, tabs for peer views, menus for option sets, and buttons for actions.

Avoid marketing hero layouts inside the app, nested card shells, and wrappers that reduce working space without clarifying hierarchy.

## Form-Heavy Service

Purpose: collect accurate information and help a user finish a consequential task.

Design for:

- A visible task boundary, progress model, and clear distinction between saved, submitted, and incomplete work.
- Labels and help near the field they govern. Preserve user input after errors.
- Inline validation at a moment when the user can act on it, plus a useful error summary for long or multi-step forms.
- Review, correction, save-and-resume, privacy, and confirmation paths when the task warrants them.

Avoid placeholder-only labels, disabling submission without an explanation, and asking twice for information the product already has.

## Dashboard Or Data Visualization

Purpose: turn data into a decision.

`insight-dashboard` decides the comparison, metrics, denominators, selection behavior, and explanatory text. This section covers the interface that carries them.

Design for:

- A reading order of current state, meaningful change, cause, and available action.
- Numbers with unit, timeframe, comparison basis, and uncertainty when known.
- Tables and charts that survive long labels, missing values, large values, and color-independent reading.
- A visual form chosen for the question. Use tabular numerals for comparable values and keep status color distinct from selection.

Avoid chart walls without interpretation, decorative charts, and KPI cards that all carry identical weight.

## Static HTML Report

Purpose: readable, durable, shareable analysis.

A report is read from top to bottom rather than operated. Give it a reading register distinct from an operated dashboard: a calm single column of body text at about 60 to 75 characters per line, such as `max-width: 68ch`, with comfortable line height and quiet chrome. Tables and charts may extend past the column when their content needs the width; the prose returns to it.

Design for:

- Document hierarchy: title, scope and date, summary, evidence, and decision.
- Legible tables, captions, footnotes, callouts, charts, and diagrams.
- Print or export behavior when likely, including stable widths and sensible page breaks.
- Visual restraint that lets the evidence carry the page.

Avoid landing-page theatrics, oversized type that weakens reading, dashboard controls and card grids the reader has nothing to operate, and motion without an analytical purpose.

When the report ships as a standalone file or a hosted artifact, read [html-delivery.md](html-delivery.md) for theme tokens, self-containment, and host limits.

## Landing Or Brand Page

Purpose: explain an offer and create informed desire.

Design for:

- A first viewport that identifies the subject and promise.
- A dominant anchor supported by real product material, imagery, video, data, interaction, or a typographic concept grounded in the subject.
- Sections with distinct jobs: promise, proof, mechanism, detail, and action.
- Copy that identifies what the user gets and the evidence for believing it.

Avoid generic stat strips, fabricated proof, and decorative texture as the only visual substance.

## Portfolio Or Career Page

Purpose: show judgment, evidence, and fit.

Design for:

- Case evidence over slogans.
- Project summaries that reveal the problem, role, decision, and supported result.
- A visual system that fits the person's field and an accessible download or print path when the artifact doubles as application material.

Avoid hiding evidence behind animation, overly clever navigation, and giving every project equal weight.

## Game Or Interactive Demo

Purpose: play, feel, experiment.

Design for:

- Immediate affordance and a clearly primary play surface.
- Motion, sound, feedback, and controls that support the loop.
- Stable canvas or scene dimensions and relevant mobile controls.
- Proven libraries for established physics, rules, parsing, or 3D behavior when the project already relies on them.

Avoid chrome that competes with play, blank or off-frame scenes, and nonessential motion that ignores reduced-motion preferences.

## Docs, Guides, Or Knowledge Tools

Purpose: comprehension and retrieval.

Design for:

- Strong information scent through headings, search, anchors, examples, and callouts.
- Dense but readable pages with stable links and copyable commands.
- Examples close to the claim or instruction they support.

Avoid decorative cards around every paragraph and typography that weakens scanning or code legibility.

## AI Or Generative Interface

Purpose: help a user provide intent, understand system activity, inspect output, and recover from uncertain results.

Design for:

- Clear separation among user input, configuration, generated output, sources, and system status.
- Pending, streaming, partial, stopped, failed, retried, and completed states.
- Edit, retry, compare, copy, cite, or discard actions that fit the output.
- Provenance and uncertainty where the product can support them. Preserve user work across model or network failures.

Avoid a single magical text box as the whole workflow, fake citations or confidence, and animations that conceal latency or state changes.
