# Source Notes

Last reviewed: 2026-08-13.

This skill synthesizes sources into routing, research, and verification rules. It does not copy a provider prompt, brand analysis, or bundled design fixture as an aesthetic default.

## Contents

- [Trust Tiers](#trust-tiers)
- [Provider Skills And Prompt Packs](#provider-skills-and-prompt-packs)
- [Selection And Licensing Rules](#selection-and-licensing-rules)
- [Architecture Decision](#architecture-decision)

## Trust Tiers

### 1. Standards And Platform Evidence

Use these as the authority for accessibility and platform claims:

- WCAG 2.2 and the WAI Authoring Practices Guide for conformance criteria, semantics, keyboard behavior, and widget patterns. https://www.w3.org/TR/WCAG22/ https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/
- Web Platform Baseline, Core Web Vitals guidance, and MDN for browser support, performance evidence, and CSS or Web API behavior. https://web.dev/baseline https://web.dev/articles/vitals https://developer.mozilla.org/
- W3C Internationalization guidance for language, line breaking, direction, and locale-sensitive presentation. https://www.w3.org/International/

### 2. Production Design Systems

Use these for tested patterns and implementation evidence. Adapt to the current product rather than importing their brand:

- GOV.UK Design System and Service Manual for forms, errors, task flows, and accessibility strategy. https://design-system.service.gov.uk/ https://www.gov.uk/service-manual
- GitHub Primer for production component and accessibility practices, and Microsoft HAX for accessible AI-assistant experience patterns. https://primer.style/ https://microsoft.github.io/HAXPlaybook/
- Material Design for canonical layout and interaction patterns. https://m3.material.io/
- Vercel Web Interface Guidelines for implementation review cues across focus, forms, motion, typography, content, performance, navigation, and i18n. https://github.com/vercel-labs/web-interface-guidelines

### 3. Workflow And Design-Memory Structures

Use these for process and packaging ideas. Their bundled content has mixed provenance and should not become a design authority:

- Open Design separates functional skills, rendering, reusable design-system packages, preview, and export. Its manifest and `DESIGN.md` structure are useful; bundled fixtures may carry separate licenses or generated prose. https://github.com/nexu-io/open-design
- Google's DESIGN.md experiment uses structured tokens plus rationale and can lint, diff, and export design memory. It is alpha, so this skill supports a present file without requiring its schema. https://github.com/google-labs-code/design.md
- Agentic Design System supplies an evidence loop from intent and baseline through render, review, and revision. https://github.com/aa-on-ai/agentic-design-system
- Open CoDesign shows local design memory, preview, and versioned collaboration. https://github.com/opencoworkai/open-codesign
- Raven MCP and Designlib MCP show optional runtime retrieval and audit models. Designlib's standalone repository returned 404 on 2026-09-23; the design-builder plugin from the same publisher documents and configures it. Neither service is required for this skill's normal path. https://github.com/rhinocap/raven-mcp https://github.com/app-builders-club/design-builder

### 4. Exploration Sources

Use catalogs and galleries to discover candidates. Verify an important decision against the shipped product, original material, or a stronger source:

- Mobbin, SiteInspire, Awwwards, Interface In Game, and Awesome DESIGN.md. https://mobbin.com/ https://www.siteinspire.com/ https://www.awwwards.com/ https://interfaceingame.com/ https://github.com/VoltAgent/awesome-design-md
- Datawrapper and Observable Plot are useful primary references for explaining and implementing data visualization choices. https://www.datawrapper.de/ https://observablehq.com/plot/

## Provider Skills And Prompt Packs

OpenAI, Anthropic, Microsoft, StyleSeed, and other public frontend skills reveal common model defaults and useful checks. Treat their aesthetic language as failure-mode evidence rather than design authority. Do not inherit requirements for a memorable signature, a single bold move, a fixed token palette, or one provider's preferred stack.

Relevant comparison sources:

- https://github.com/anthropics/skills/tree/main/skills/frontend-design
- https://github.com/microsoft/skills
- https://github.com/bitjaru/styleseed
- https://github.com/vercel-labs/agent-skills

Two sources added on 2026-11-04 shape specific references:

- Claude's built-in `artifact-design` skill motivated the three-block theme tokens, explicit body background, self-contained file rules, and hosted-artifact limits in `html-delivery.md`. The reference restates the ideas in original text and generic terms rather than copying the skill or tying it to one host.
- Impeccable's CLI detector supplies the optional post-build scan in `quality-gate.md`. It is Apache-2.0; version 4.8.0 was run on a probe page to record what it catches and misses. Its aesthetic opinions, such as banned typefaces and palettes, are not adopted as rules. https://github.com/pbakaus/impeccable

## Selection And Licensing Rules

Prefer a source when it changes a cross-framework decision, supplies verifiable behavior, or documents a recurring failure. Quarantine trend language, unattributed brand reconstruction, one-stack assumptions, arbitrary numbers, and landing-page advice presented as universal UI guidance.

Keep the skill a synthesis. Before copying code, imagery, fonts, icons, or a design-system package, verify the license of that exact asset. A repository's license may not cover every bundled fixture or third-party file.

## Architecture Decision

Keep `frontend-design` as a portable routing and quality layer for user-visible frontend work. Scale its cost through Preserve, Adapt, and Direct paths. Keep reference search and design-memory tools optional. Add scripts or a persistent catalog only after a repeated failure shows that model judgment and project evidence are insufficient.
