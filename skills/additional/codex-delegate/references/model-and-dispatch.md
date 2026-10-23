# Model and Dispatch

New delegated mission leads default to GPT-6 Astra at `xhigh`. The GPT policy in `model-routing` owns task eligibility and child assignments. This is this pack's operating policy, not a claim that CLI availability or model quality was established for every account; a user's explicit model choice or their own routing policy overrides it.

## Selection

| Work | Default model | Effort |
| --- | --- | --- |
| New mission lead | `gpt-6-astra` | `xhigh` |
| Ordinary research or mechanical mission, when deliberately selected | `gpt-6.1-sol` | `xhigh` |
| Explicit user model or effort choice | User selection | User selection |

A deliberately selected Sol mission may choose sources, refine queries, organize evidence, produce cited summaries, and compare source-supported facts within its scope. Complex design, implementation, difficult diagnosis, consequential judgments, decision-oriented synthesis, and final review belong to Astra under the current routing policy.

Keep inseparable research and consequential judgment on Astra. Do not make a cheaper trial a prerequisite, lower frontier effort automatically, or impose an arbitrary limit on frontier consultations. Honor the actual mission's cost, time, and concurrency limits. If the requested route is unavailable, report the limitation or use an already authorized alternative.

The launcher passes model and `model_reasoning_effort` explicitly. A resume preserves recorded settings unless the host overrides them. Inspect a legacy source before resuming and select the follow-up route under the current policy. Pass explicit model options and record a reason such as `resume-policy-migration` when changing the route. A user's deliberate model choice still wins.

## Service tier

New runs use `--fast-requested no`, which records `tier=default`. An explicit Fast request permits `yes`, which records `tier=priority`. The assertion records the host's authorization decision; the script cannot verify a conversation it does not receive. Resume may preserve the grant for the same mission. A legacy source with no assertion defaults to `no`.

The current [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) describes `fast` as mapping to request tier `priority`. Requested settings in provenance are not a server receipt. Inspect CLI warnings when availability matters and report an unsupported tier rather than claiming it was applied. Service tier does not change the selected reasoning effort.

## Internal subagents

The delegate uses the GPT policy of the sibling `model-routing` skill for available roles, model settings, and host-specific overrides. Mission work is eligible for useful internal delegation.

- Apply the current task split to named, unnamed, and nested workers; the mission lead's model does not determine every child's model.
- Preserve the mission's authority, data boundary, and resource limits at every depth.
- Follow the runtime's supported model-override contract. Do not invent roles, pass unsupported overrides, or install global agent defaults as part of a task launch.
- If the routing skill is absent, use Sol 6.1 for ordinary research, source selection, query refinement, cited summaries, factual comparisons, and mechanical execution. Use Astra for complex design, implementation, difficult diagnosis, consequential judgments, decision-oriented synthesis, and final review. If suitable subagent tools are unavailable, work sequentially.

Delegate independent work with a clear integration owner. Shared writes need isolated workspaces or disjoint ownership that the lead can integrate safely. Account for host roots and internal children together when a resource limit matters. No fixed root count disables useful children automatically.

Before handoff, the delegate integrates child evidence and waits for or intentionally stops its active children. A root event log exposes only partial child state; it does not certify every descendant's completion.

## Host launch ownership

The main host owns the packet, model route, authority, source workspace, run path, observation, result acceptance, and recovery decision. Calling the deterministic launcher directly is sufficient for a durable run.

An optional native host subagent can launch a fixed packet or batch. Its inputs are packet paths, absent run paths, and resolved scalar settings. It returns the manifest unchanged and stops. It does not interpret reports, rewrite packets, widen authority, or retry. For GPT host helpers, the same Astra/Sol policy applies; their mechanical role may qualify for Sol 6.1. Other host model families follow the user's applicable routing policy.

Lost manifest delivery does not establish failed execution. The main host first settles the launcher and then recovers the exact run. A recovered run retains its original `host_route` and `host_model`; recovery must not relabel how it was launched.

## Durability and evidence

A separate process session keeps Codex outside the launching command's process group. The script uses util-linux `setsid -f` or Perl's POSIX `setsid`. It detaches standard input and redirects wrapper diagnostics to `launcher.log`. `&` or `nohup` alone does not establish this separation.

Historical package checks on CLI 0.145.0 observed a detached run surviving its launching command and a SIGINT-interrupted thread retaining context on resume. Current deterministic fixtures exercise the wrapper lifecycle. Neither establishes every host's process cleanup behavior or current model performance. A host that kills all descendants or containers may require its supported durable-job mechanism.

CLI help was inspected on 0.159.3 on 2026-10-06. [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) documents JSONL events, output capture, and explicit-session resume. The [GPT-6 instruction guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) supports outcome-led prompts and conditional scaffolding; the local mission and authority contract remains this skill's responsibility.
