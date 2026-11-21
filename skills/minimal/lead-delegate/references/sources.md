# Sources

Collected and checked 2026-11-21. Read this when re-examining a rule in SKILL.md or when a model price or harness changes. "Opened" means the claim was checked against the page itself; "abstract only" means the full text was not read.

## Measured Results Behind the Rules

| Rule | Evidence | Status |
| --- | --- | --- |
| Small work stays with the lead | [fable-advisor](https://github.com/DannyMac180/fable-advisor): with Opus 5.5 at $4/$20 and Fable 5.2 at $8/$40 per MTok, Fable alone was about 2.8 times cheaper on small tasks and $3.14 against $3.53 on one larger task. Task count and method are not in the README. | Opened |
| The most capable model belongs at decomposition and design | [Cursor, 2026-07-20](https://cursor.com/blog/agent-swarm-model-economics): an Opus 4.8 planner with Composer 2.5 workers cost $1,339 against $10,565 for GPT-5.5 in both roles; workers used at least 69% of tokens. A Fable 5 planner spent fewer planning tokens but its workers used several times more. | Opened |
| Cheap models as implementers lower quality | [arXiv:2610.17471](https://arxiv.org/abs/2610.17471) abstract, ProgramBench: cheap models pay off as planners and lower reward as implementers; a lead that delegates only planning matches full delegation at half the cost; teams cost three to seven times a solo agent. | Opened, abstract only |
| Gains flatten after about four workers | Same abstract: implementers and verifiers plateau beyond four workers. | Opened, abstract only |
| The brief leaves steps to the child | Liu, [arXiv:2603.26458](https://arxiv.org/html/2603.26458) Table 7, an ablation on 50 SWE-bench Lite tasks with a Sonnet 4.6 manager and a GPT-5-mini worker: strict only 26 with 8 empty patches, guided only 27 with 5, guided on the first round then strict corrections on retries 32 with none. Guided only and strict only differ by one task. | Opened |
| The brief leaves steps to the child | [Cognition, 2026-04-22](https://cognition.com/blog/multi-agents-working): managers without codebase context become over-prescriptive, and parents assume state their children do not share. | Opened |
| Acceptance rests on evidence | Smyth et al., [arXiv:2609.20812](https://arxiv.org/abs/2609.20812) abstract, OverclaimBench file reviews across 12 models: agents left a file unread in 67.9% of runs, and 80.4% of those incomplete runs were misleading, claiming a complete review or leaving the gap undisclosed; 59 to 96% per model. | Opened, abstract only |
| The child reports once | [gstack captain](https://github.com/garrytan/gstack/blob/main/crew/docs/captain.md): each handoff wakes the controller, whose tokens cost about 1.7 times a worker thread's. | Opened |
| Depth stops at lead, child session, and one layer of subagents | No study comparing three levels of delegation with two was found. This limit is a judgment. | No evidence |

## Borrowed Forms

- The `UNVERIFIED`, `FAILED OR SKIPPED`, and `ALSO CHANGED` report lines and the rule that only the controller creates sessions follow gstack's Captain report and thread rules.
- The `MODEL` report line follows fable-advisor, whose worker reports name the model that actually ran so a silent fallback shows.
- Returning a structural change to the lead instead of proceeding follows Rule 4 of the executor in [GSD Core](https://github.com/open-gsd/gsd-core/blob/main/agents/gsd-executor.md), which stops on a significant structural change and returns a checkpoint for a user decision (opened).

## Harness Documentation

- [Claude Code advisor](https://code.claude.com/docs/en/advisor) and [cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging): opened.
- Claude Code subagent model order and background sessions: opened at [sub-agents](https://code.claude.com/docs/en/sub-agents) and [agent-view](https://code.claude.com/docs/en/agent-view), with the `claude` 2.1.322 help.
- Codex subagents, custom agent files, and config keys: opened at the [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [config reference](https://learn.chatgpt.com/docs/config-file/config-reference) pages and the [models](https://learn.chatgpt.com/docs/models) page. The `spawn_agent` schema, the completion notice, and the model catalog were read in the [openai/codex](https://github.com/openai/codex) source (`codex-rs/core/src/tools/handlers/multi_agents_spec.rs`, `codex-rs/core/src/agent/control.rs`, `codex-rs/models-manager/models.json`), since the docs do not describe them.
