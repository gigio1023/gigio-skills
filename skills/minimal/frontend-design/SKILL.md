---
name: frontend-design
description: >
  Use for frontend work that can change what users perceive or operate: components, pages, layout, styling, responsive behavior, forms, data views and the interface of a dashboard or analysis report, interface states, motion, accessibility, visual assets, and UI review. Includes user-visible frontend bug fixes. Phrases include "build this page", "fix this layout", "review this UI", "화면 만들어줘", and "UI 고쳐줘". NOT for backend-only work or frontend configuration and data changes with no interface effect. NOT for deciding what a dashboard or analysis report compares, its metrics, denominators, selection behavior, and explanatory text (insight-dashboard), or technical figures (technical-figure, when installed).
---

# Frontend Design

Route user-visible frontend work through the smallest design path that protects the product, then verify the affected interface honestly.

For a data dashboard or analysis report, `insight-dashboard` decides what the view compares, its metrics and denominators, how selections change the results, and its explanatory text; this skill builds and reviews the interface that carries those decisions. Use both when building or redesigning one. An interface-only change to an existing dashboard, such as a restyle, a responsive fix, or a state bug, needs only this skill unless it changes a value, ranking, or sentence the reader sees.

## Route Before Loading References

1. Set the authority boundary:
   - **Review:** inspect and report findings. Do not edit files or turn the review into a redesign unless the user asks.
   - **Change:** implement the requested local change and non-destructive checks.
2. For a change, choose its design intensity:
   - **Preserve:** a bug fix, state change, refactor, or maintenance task whose rendered language should remain stable.
   - **Adapt:** a component, form, content region, or bounded layout change that should extend the existing product language.
   - **Direct:** a new surface, new product, or substantial redesign that needs an explicit direction.

When the boundary is unclear, choose the lowest intensity that fully covers the authorized change. Escalate only when the request or inspected product evidence requires a new visual language, a substantial hierarchy change, or a redesign. Review depth follows the reviewed scope; it is not a fourth intensity level.

### Preserve Fast Path

Do not load references for Preserve work.

- Keep the existing components, tokens, density, hierarchy, and copy style.
- Change only the requested behavior and the states that reveal it.
- Render the affected state and its nearest regression viewport when a runnable path exists.
- If rendering is unavailable, name that gap instead of claiming visual success.
- End the design branch here and continue the original frontend task.

## Load Only What the Route Needs

| Route | Guidance |
| --- | --- |
| Preserve | Use the inline fast path only. |
| Adapt | Read [quality-gate.md](references/quality-gate.md). Read [surface-patterns.md](references/surface-patterns.md) only when local patterns do not answer the change. |
| Direct | Read [surface-patterns.md](references/surface-patterns.md), [reference-research.md](references/reference-research.md), and [quality-gate.md](references/quality-gate.md). |
| Review | Read [quality-gate.md](references/quality-gate.md). Add the surface and research references only when the review covers a new or substantially changed direction. |
| Skill maintenance | Read [source-notes.md](references/source-notes.md). |

When the deliverable is a standalone HTML page, a static HTML report, or a page for a hosted artifact surface, also read [html-delivery.md](references/html-delivery.md) on the Adapt, Direct, and Review routes. It covers light and dark theme tokens, a self-contained file, and host limits that a project app would otherwise supply.

## Establish Design Context

Use evidence in this order:

1. The user's request, the screen's real job, and any reference named as a target.
2. The rendered product and the implementation already serving that job.
3. Project contracts such as components, tokens, themes, Storybook, `DESIGN.md`, and brand or content guidance.
4. User material supplied as inspiration rather than a target.
5. Shipped products that support the same workflow.
6. Standards and production design systems.
7. Galleries, awards, and third-party brand analyses.

A target reference such as “match this” is part of the requirement. An inspiration link supplies evidence but does not silently override the product's workflow, accessibility, platform, or existing design contract.

When code and a design contract disagree, Preserve and Adapt work follow the current product and report the divergence. Align both only when the request authorizes that broader change. Support a present `DESIGN.md`; do not create one or depend on a particular schema by default.

## Work the Route

### Review

Lead with the most consequential evidence-backed findings. Separate observed defects from optional direction. Do not mutate files, inflate a local issue into a rebrand, or claim a viewport or interaction was checked when it was not.

### Adapt

Use the existing framework, components, tokens, primitives, density, and content patterns first. Add the smallest new primitive that the requested behavior needs. Preserve the product's established hierarchy unless changing it is part of the request.

### Direct

Name the subject, audience, surface, and primary user job. Research references with [reference-research.md](references/reference-research.md), then record only the decisions needed to build: reading order, dominant anchor, density, key states, viewports, and existing constraints.

Derive the primary visual anchor from the subject, data, product, or user task. An anchor may be a composition, a piece of real visual material, a data view, or an interaction. It does not need to be decorative or loud.

Implement in the project's stack and reuse its reliable primitives. New art direction does not authorize unrelated features, a replacement design system, or decorative work outside the requested surface.

## Interchangeability Gate

Do not blacklist gradients, cards, glass, large type, or other motifs. Reject a result when its choices could move to an unrelated product with little loss:

- Renaming the product and copy leaves the composition equally plausible.
- Every region uses the same card, radius, border, shadow, and visual weight.
- Hierarchy disappears when decorative color and effects are removed.
- Fake metrics, testimonials, or marketing copy substitute for required data.
- Loading, empty, error, long-content, disabled, or completion states are absent.
- Only the desktop happy path appears resolved.
- A reference skin displaces the product's workflow, density, or platform norms.
- Fonts, images, icons, or brand assets are assumed without an available and permitted source.

## Verification And Output

For Adapt, Direct, and Review work, apply the risk-relevant sections of [quality-gate.md](references/quality-gate.md). Inspect an actual render when the surface is runnable. Exercise the changed interaction and the states named by the brief. Run existing build, lint, test, and accessibility checks when they cover the change.

Finish when the affected states and required project checks are covered. Add another viewport, browser, or visual pass only for a supported target, a new change, a failure, or a specific unresolved regression; the reference's full catalog is not a mandatory test matrix for every component edit.

For a change, lead with the implemented outcome, then list only the viewports, states, and commands actually verified. For a review, lead with findings and say that no files were changed. Always name missing assets, unavailable render paths, or unverified states that materially limit confidence.

## Gotchas

- A broad trigger does not justify loading Direct guidance for routine work.
- Treat an explicitly requested specialist workflow or an established project design system as operative context. Do not duplicate or silently replace it.
- Reference access does not grant permission to copy protected assets, brand identifiers, or an unrelated product's composition.
- Optional catalogs, MCP services, and design-memory formats may improve evidence, but the skill must still work without them.
