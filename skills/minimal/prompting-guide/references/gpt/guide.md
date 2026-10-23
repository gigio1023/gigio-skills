# GPT-6 Prompting Guide

Produce a usable prompt or instruction change for GPT-6 Astra or GPT-6.1 Sol. Keep legacy GPT-6 Sol distinct when maintaining an older integration. Start from the requested outcome and the information the model needs to achieve it. Preserve useful domain knowledge and precise constraints; reconsider inherited scaffolding before adding another rule.

This package applies OpenAI's [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) and the prompting best practices in [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#prompting-best-practices). It guides prompt authors regardless of which model performs the edit. Loading it does not select a model or provide runtime capabilities.

## Astra And Sol

OpenAI publishes one set of prompts for the GPT-6 family. They address behavior observed with Astra, and OpenAI asks that they be evaluated with the chosen model and workload; there is no separate Sol prompting guide. Use the same patterns for both models, and before adding a clause for Sol, check that the Sol workload shows the behavior the clause addresses: clarification pauses, sensitivity to skill files, heavily formatted output, under-delegation, or broader testing than the change needs.

GPT-6.1 Sol is `gpt-6.1-sol`, distinct from legacy `gpt-6-sol`. Astra and Sol 6.1 require Responses for tools, and neither accepts `none`; Sol 6.1 also rejects `minimal`. Its API default effort is `medium`. [Runtime notes](runtime-notes.md) separate current model contracts from legacy settings and Codex catalog values. Model assignment belongs to the current GPT policy in `model-routing`.

## Choose The Relevant Material

| Task | Read when needed |
| --- | --- |
| Author or audit a skill, `AGENTS.md`, or an instruction stack | [Instruction design](instruction-design.md): discovery, selective reading, inherited recipes, and completion boundaries |
| Fix a concrete prompt behavior or tool description | The matching section of [prompt patterns](prompt-patterns.md): execution, clarification, conflicts, style, tools, delegation, or verification |
| Write a new task prompt | Adapt the small [prompt template](../../assets/gpt/prompt.template.md); add detail only for the task's actual decisions |
| Change an API integration or migrate from legacy Sol or GPT-5.6 | [Runtime notes](runtime-notes.md); verify applicable compatibility claims before changing settings |
| Check a model claim or source freshness | [Source notes](source-notes.md): provenance, review dates, and interpretation limits |

## Make The Change

Use the request, target artifact, and available feedback to establish scope and completion. Read the instructions that affect this task. Expand to co-loaded skills, repository guidance, or tool definitions when a conflict, unexplained behavior, or requested stack audit warrants it. A small edit does not require a repository-wide audit.

Resolve unnecessary or conflicting instructions at their source within the authorized scope. Keep exact syntax, ordering, permissions, and artifact invariants where they matter. Define a concrete stopping condition when early stopping is the problem. Routine missing preferences can use a stated assumption; missing authorization cannot. Reuse existing session grants and continue work that does not depend on an unanswered question.

Return the requested prompt, patch, or review findings with the material changes and relevant evidence. Run applicable repository checks and check affected links or templates. Use existing traces when available; distinguish static review from exercised model behavior. Model trials and benchmark suites require a corresponding request. Finish when the requested artifact and required checks are complete.
