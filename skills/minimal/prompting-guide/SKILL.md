---
name: prompting-guide
description: >
  Write, review, debug, or migrate system prompts, CLAUDE.md, AGENTS.md,
  skills, subagent definitions, or tool descriptions for a specific Claude or
  GPT target model, using vendor prompting guidance newer than the model's
  training. Also drafts, reviews,
  or translates Codex Goal mode and Claude Code /goal prompts. Use for "write
  the system prompt for Opus", "goal prompt 써줘", "프롬프트 고쳐줘".
---

# Prompting Guide

Each model family has its own guide. Identify the family that will run the instructions and read that guide; skip the others.

| Target model | Read |
| --- | --- |
| Claude Fable or Mythos | [Fable guide](references/fable/guide.md) |
| Claude Opus, including migration from an earlier Opus | [Opus guide](references/opus/guide.md) |
| GPT-6 family (Astra, Sol) | [GPT guide](references/gpt/guide.md) |

The target is the model that will execute the prompt, not the model doing the editing. Take it from the request, a model ID in the integration or configuration, a `model` field in the agent or skill definition, or the host's documented default. Ask only when it cannot be determined and the answer changes the advice. Each guide names the versions it covers; a newer release may have its own vendor page, so check before applying an older version's clauses to it.

For a Codex Goal mode or Claude Code `/goal` prompt (explain, draft, review, translate between the two, or activate), read the [Goal mode guide](references/goal-mode/guide.md) with the target family's guide.

When an artifact runs on more than one family, such as a skill shared by Claude Code and Codex, apply each family's guide to that family's behavior and keep the clauses distinguishable. When migrating between families, follow the target family's guide; the source family's guide only helps identify scaffolding written for the old model.

Do not port guidance between families without measurement. The model lines changed in different directions, and effort level names do not mean the same amount of thinking across models. The Fable and Opus guides share some Anthropic runtime facts (beta headers, thinking-block binding, refusal fallback); when you update one, check the other.

A model outside these families has no guide here. Say so and work from that model's official prompting documentation.
