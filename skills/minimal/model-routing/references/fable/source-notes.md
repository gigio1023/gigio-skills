# Source Notes

Policy updated 2026-10-06. Anthropic runtime and price evidence was last checked on 2026-10-07 for the Sonnet 5.5 alias move, Ultracode, the Agent tool's `effort` argument, and prices; the older dated items below keep their dates.

## Policy Ownership

This policy owns Anthropic model choices. The GPT policy in `references/gpt/` owns GPT assignments, including GPT workers under a Fable lead. The policies are no longer mirrored. Sonnet research and Opus implementation remain Anthropic routes; the GPT policy assigns ordinary research and summaries to Sol 6.1 and consequential judgment and complex work to Astra.

The 2026-10-06 revision removes automatic frontier effort reduction and arbitrary consultation caps. `fable-builder` replaces `fable-lean-builder`, and both Fable roles inherit selected session effort. Actual user budgets remain binding. The historical policy notes below explain prior choices rather than prescribing current routes.

## Sources

Anthropic model and effort guidance, fetched 2026-09-20:

- `Prompting Claude Fable 5.1`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- `What's new in Claude Fable 5.1`: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
- `Prompting Claude Opus 5`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- Fetched 2026-09-23: `Prompting Claude Opus 5.5` (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5), `What's new in Claude Opus 5.5` (https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5), and `Introducing Claude Opus 5.5`, 2026-09-22 (https://www.anthropic.com/claude-opus-5-5)
- `Effort`: https://platform.claude.com/docs/en/build-with-claude/effort
- `Optimizing for cost and intelligence`: https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence
- `Models overview`: https://platform.claude.com/docs/en/models/overview
- `Pricing`: https://platform.claude.com/docs/en/about-claude/pricing
- `How we built our multi-agent research system` (2025-06-13): https://www.anthropic.com/engineering/multi-agent-research-system
- `Building multi-agent systems: when and how to use them` (2026-01-23): https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them

Harness mechanics, fetched 2026-09-20:

- Claude Code `Create custom subagents`: https://code.claude.com/docs/en/sub-agents
- Claude Code `Model configuration`: https://code.claude.com/docs/en/model-config
- Claude Code `Changelog` (2.1.272 to 2.1.278): https://code.claude.com/docs/en/changelog
- Claude Code 2.1.292 local changelog, read 2026-10-07: 2.1.284 added Sonnet 5.5 as the default Sonnet on the Anthropic API ($2 and $10, cache reads $0.20); 2.1.285 made Ultracode its own `/effort` toggle that no longer forces `xhigh`; 2.1.292 added an `effort` parameter to the Agent tool. `Model configuration`, `Create custom subagents`, and `Pricing` reread the same day for the alias table, default effort (Opus 5.5 and Sonnet 5.5 at `medium`), effort levels (Sonnet 5.5 accepts `low` through `max`), and the 20-subagent and three-layer defaults.
- Claude Code `Model configuration` and `Settings` rechecked on 2026-09-23 against 2.1.280 for alias resolution and effort resolution: https://code.claude.com/docs/en/settings-reference
- Claude Agent SDK `Subagents`: https://code.claude.com/docs/en/agent-sdk/subagents
- Cursor `Subagents`: https://cursor.com/docs/subagents (the old `docs/agent/subagents` path redirects; definition locations read 2026-09-23)
- OpenCode `Agents`: https://opencode.ai/docs/agents/
- Hermes Agent: configuration keys (`delegation.model`, `delegation.provider`, `agent.reasoning_effort`, `agent.reasoning_overrides`) observed in a local configuration on 2026-09-20. The delegation and Kanban documentation pages were read the same day for vocabulary, not for a key-by-key check of that configuration. The Hermes Agent v0.21.3 source, read 2026-09-23 (`tools/delegate_tool_config.py` lines 494-507), shows that children take `delegation.reasoning_effort`, else the parent's resolved effort, and never `agent.reasoning_overrides`.
- Per-invocation effort requests: anthropics/claude-code issues #43083 (closed completed, shipped the frontmatter `effort` field) and #72596 (closed not planned).

Routing evidence outside vendor docs:

- SWE-Router (Son et al., 2026, arXiv:2607.00053): prompt-only routing of agentic coding tasks has a Bayes-error floor; conditioning on three exploratory turns of trajectory improves routing.
- Routing collapse (Lai and Ye, 2026, arXiv:2602.03478): learned routers send nearly all near-tie queries to the strongest model.
- Self-correction illusion (Chen et al., 2026, arXiv:2606.05976): the same error relabeled as external input is corrected far more often than when it appears as the model's own thought.
- InflationAgent (Fu et al., 2026, arXiv:2608.13571): retry inflation on cheap models of roughly three to four times single-call cost.
- OpenAI Codex `Subagents`: https://learn.chatgpt.com/docs/agent-configuration/subagents (read-heavy work for subagents; role-to-model guidance for the GPT-5.6 family when read on 2026-09-20; by 2026-09-23 the page said to start most tasks with `gpt-6-sol`).
- Community packages read for patterns: matteoscurati/delegation-kit (mirrored Claude and Codex subagent definitions with an inverted effort curve), AqueGen/model-routing (dispatch-logging hook and one-step retry rule), obra/superpowers strict-cost design spec (pre-registered failures of cheap models on judgment).

## Historical Measurements

From Anthropic's cost and intelligence page, on its own benchmarks with unpublished protocols; first-party, unreplicated:

| Configuration | SWE-bench Pro solved | Cost per solved task |
|---|---|---|
| Opus 5 at `low` | 84.0% | $0.25 |
| Fable 5.1 at `low` | 88.6% | $0.54 |
| Sonnet 5 at default | 77.4% | $0.84 |
| Opus 5 at default | 91.7% | $1.01 |
| Fable 5.1 at default | 92.1% | $1.19 |

- Research and knowledge benchmarks: `medium` saved 13 to 31 percent of cost for one to three points; the default bought nothing measurable over `medium`. Long-horizon coding: `medium` cost about two points for half the spend, `low` about eight points for a quarter.
- "Sweep effort on your current model first." On one search benchmark a single model at `low` matched an orchestrator with a Sonnet 5 worker at 29 percent lower cost.
- Opus 5 at `low` with its failures re-run at default matched the default pass rate for half the cost, conditioned on a checker that does not pass bad work.
- Two of twenty problems carried 43 percent of one run's spend; compare models on the hardest tenth of tasks.
- Prices on 2026-09-20 per million tokens, input and output: Fable 5.1 $10 and $50 with cache reads at $0.25; Opus 5 $5 and $25 with cache reads at $0.50; Sonnet 5 $2 and $10; Haiku 4.5 $1 and $5 with no effort parameter and a 200K context. Added 2026-09-23: Opus 5.5 $4 and $20 with cache reads at $0.20 and 5-minute cache writes at $5; its fast mode $8 and $40. Added 2026-10-07: Sonnet 5.5 $2 and $10 with cache reads at $0.20.
- The cost page had not added Opus 5.5 measurements when rechecked on 2026-09-23. Anthropic's Opus 5.5 announcement claims about 40% lower cost than Opus 5 at default settings on typical workloads and performance at Fable 5.1's level on most work; these are launch claims, not per-task measurements comparable with the table.

Guidance recorded during the earlier policy review:

- Effort page: `low` is for "simpler tasks that need the best speed and lowest costs, such as subagents"; `xhigh` is for long-running agentic work with token budgets in the millions.
- Fable 5.1 page: at `low` it calls search and retrieval tools less often; at `xhigh` and `max` it may think long before a long deliverable, so that guidance recommends `high`; at `low` it is often competitive on cost per task with Opus and Sonnet at higher effort.
- Opus 5 page: it delegates readily and verifies its own work unprompted; instructions to use a subagent to verify cause over-verification, and the recommended delegation line says not to use subagents to verify or double-check its own work.
- Models overview, 2026-09-23: Anthropic recommends starting with Opus 5.5 for most workloads and reaching for Fable 5.1 for demanding reasoning and long-horizon agentic work, or when evals on Opus 5.5 at higher effort still fall short. On 2026-09-20 the same page named Opus 5.
- Opus 5.5 pages: the default effort is `medium` where Opus 5's is `high`; at a given level 5.5 thinks more per turn than Opus 5, most at `xhigh` and `max`; `xhigh` and `max` are for work where a quality gain was measured. The Opus 5 prompting patterns remain its starting point, so the delegation and over-verification guidance above still applies.
- Multi-agent posts: the 2025 post pairs an Opus lead with Sonnet workers, scales subagent count with task complexity, and reports roughly fifteen times chat token use; the 2026 post gives no model-role guidance and reports three to ten times single-agent use.

## Durable Translation

- Fable can lead difficult, long-horizon work and coordinate subagents; delegate for concurrency, isolation, fresh verification, tool fit, or a measured efficiency gain, not to keep the lead's context empty.
- Effort is the main intelligence, latency, and cost control, and level names do not transfer across models. Sonnet and Opus retain this pack's `xhigh` default; Fable inherits the selected session effort. The vendor numbers above are historical comparison points, not measured benefits for these routes.
- The shipped subagent definitions exist because Claude Code set a subagent's effort only through a definition until 2.1.292 added a per-spawn `effort` argument. The definitions remain the default route; the argument covers a level no installed definition carries. An omitted effort uses the documented session inheritance path.
- Reporting must distinguish what was read from what ran. No harness in this reference reports a subagent's applied effort to the lead. In Claude Code the user can see it in `/tasks` when the definition sets `effort`; a hook records only the requested values.

## Policy History

- 2026-08-07: opened only on explicit request, because an unrequested opening meant switching the lead model.
- 2026-09-17: standing policy when Fable already leads in Claude Code or Cursor; on-request path kept for other leads.
- 2026-09-20: scope keyed to the lead model rather than the harness, with harness mechanics moved to adapters. Effort floor of `xhigh` for models below the frontier, adjustable per route. Subagent definitions shipped as assets, named `<model>-<role>`. The reviewer route reframed as a fresh-context specification check after the Opus 5 guidance. Packet templates and the long judgment checklist removed in favor of `orchestrate-subagents` and the dispatch statement. Vocabulary follows the gigio-skills repository's `terminology.md`: subagent, subagent definition, task, dispatch, route, tier; "lane" retired because no harness documentation or routing paper uses it for these senses. Measurement of any of these policies on cost or quality has not been done.
- 2026-09-23 (later): this pack stopped routing to GPT-5.6 models. The shared core's below-frontier list names GPT-6 Sol in place of GPT-5.6 Sol, Terra, and Luna (edited in both routing skills), and the proxy-routed alternatives name GPT-6 Sol. The Hermes effort mechanism was corrected from source, the Cursor definition directories were recorded, and the Claude Code notes now cover same-family alias resolution and `/tasks`.
- 2026-10-07: Sonnet facts refreshed after Claude Code 2.1.284 moved the `sonnet` alias to Sonnet 5.5. `sonnet-collector` and `sonnet-researcher` are described as Sonnet 5.5, the default-effort and Ultracode notes follow the current docs, and the Agent tool's `effort` argument is recorded. The `xhigh` route for Sonnet is unchanged; Sonnet 5.5 accepts `xhigh` but recalibrated its levels and defaults to `medium`, so whether `xhigh` is still worth its cost on Sonnet 5.5 is listed under Not Verified.
- 2026-09-23: Opus facts refreshed after Claude Code 2.1.280 moved the `opus` alias to Opus 5.5. The shared core's below-frontier list names Opus 5.5 and Opus 5 (edited in both routing skills), `opus-builder` is described as Opus 5.5, the claim that Fable at `low` undercuts Opus on cache price was removed because Opus 5.5 is cheaper on every price line, and the Claude Code effort-resolution order was updated. The `xhigh` floor is unchanged; Anthropic's Opus 5.5 advice to reserve `xhigh` for measured gains is recorded above.
- 2026-10-12: packaged with the GPT policy in the `model-routing` skill, formerly `fable5-model-routing` and `gpt6-astra-model-routing`. This policy moved to `references/fable/policy.md` and its subagent definitions to `assets/fable/agents/`; routes, effort rules, and definition contents are unchanged.

## Not Verified

- Cost per completed task for Opus 5.5 at `xhigh` against Opus 5 at `xhigh` or Fable 5.1 at `low`; neither this pack nor Anthropic's cost page has measured it.
- Which Cursor model strings accept `effort`.
- Whether the Agent tool's per-spawn `effort` argument overrides a definition's `effort` frontmatter; the documentation did not describe it on 2026-10-07.
- Cost per completed task for Sonnet 5.5 at `xhigh` against Sonnet 5.5 at `medium`.
- Which effort a proxy-routed subagent runs at; it is read from the proxy's route string, not observed.
- The exact inheritance path for a `sonnet` or `haiku` subagent on a machine that saves `modelSettings` only for other models; the documentation says a definition without `effort` inherits the session level.
