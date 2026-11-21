# Sources

Collected 2026-11-21. Read this when re-examining a rule in SKILL.md or when a model price or harness changes. "Opened" means the page was read directly while drafting; "reported" means a research subagent read it and the claim was not rechecked.

## Measured Results Behind the Rules

| Rule | Evidence | Status |
| --- | --- | --- |
| Small work stays with the lead | [fable-advisor](https://github.com/DannyMac180/fable-advisor): with Opus 5.5 at $4/$20 and Fable 5.2 at $8/$40 per MTok, Fable alone was about 2.8 times cheaper on small tasks and $3.14 against $3.53 on one larger task. Task count and method are not in the README. | Opened |
| The most capable model belongs at decomposition and design | [Cursor, 2026-07-20](https://cursor.com/blog/agent-swarm-model-economics): an Opus 4.8 planner with Composer 2.5 workers cost $1,339 against $10,565 for GPT-5.5 in both roles; workers used at least 69% of tokens. A Fable 5 planner spent fewer planning tokens but its workers used several times more. | Opened |
| Cheap models as implementers lower quality | [arXiv:2610.17471](https://arxiv.org/abs/2610.17471) abstract, ProgramBench: cheap models pay off as planners and lower reward as implementers; a lead that delegates only planning matches full delegation at half the cost; teams cost three to seven times a solo agent. | Opened, abstract only |
| Gains flatten after about four workers | Same abstract: implementers and verifiers plateau beyond four workers. | Opened, abstract only |
| The brief leaves steps to the child | Liu, arXiv:2603.26458, SWE-bench Lite subset of 50: strict plans 26, guided plans 27, guided then strict 32. | Reported |
| The brief leaves steps to the child | [Cognition, 2026-04-22](https://cognition.com/blog/multi-agents-working): managers without codebase context become over-prescriptive, and parents assume state their children do not share. | Opened |
| Acceptance rests on evidence | Smyth et al., arXiv:2609.20812: 80.4% of incomplete runs gave a misleading final response. | Reported |
| The child reports once | [gstack captain](https://github.com/garrytan/gstack/blob/main/crew/docs/captain.md): each handoff wakes the controller, whose tokens cost about 1.7 times a worker thread's. | Opened |
| Depth stops at lead, child session, and one layer of subagents | No study comparing three levels of delegation with two was found. This limit is a judgment. | No evidence |

## Borrowed Forms

- The `UNVERIFIED`, `FAILED OR SKIPPED`, and `ALSO CHANGED` report lines and the rule that only the controller creates sessions follow gstack's Captain report and thread rules.
- The `MODEL` report line follows fable-advisor, whose worker reports name the model that actually ran so a silent fallback shows.
- Returning a structural change to the lead instead of proceeding follows the executor deviation rule in [GSD Core](https://github.com/open-gsd/gsd-core) (reported).

## Harness Documentation

- [Claude Code advisor](https://code.claude.com/docs/en/advisor) and [cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging): opened.
- Claude Code subagent model order, agent teams, background sessions: reported from [sub-agents](https://code.claude.com/docs/en/sub-agents) and [agent-view](https://code.claude.com/docs/en/agent-view).
- Codex subagents, agent role files, and config keys: reported from the [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [config reference](https://learn.chatgpt.com/docs/config-file/config-reference) pages.
