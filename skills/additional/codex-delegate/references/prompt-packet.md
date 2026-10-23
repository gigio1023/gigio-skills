# Prompt Packet

The packet carries the user's intended outcome and the context missing from Codex's workspace. It can grant end-to-end judgment within a scope. Write only the structure the task needs, with sources and constraints beside the decisions they govern.

The host finalizes the packet before launch. The launcher copies it to `prompt.md` and records its SHA-256. Follow-up instructions belong in a new packet for a new resumed turn. Never edit the original packet to make it match a changed mission.

## Focused implementation example

The following example delegates implementation judgment to Astra. The command and paths are illustrative.

```markdown
Fix empty-input parsing in src/parser.py. The accepted behavior is parse("") == []. Preserve the public function signature and all other documented input behavior. Done means the focused parser suite passes and the diff contains only changes needed for this behavior.

Read the repository instructions and tests/test_parser.py. Investigate and implement the fix. You may edit the parser and add a regression case for the accepted behavior; preserve unrelated changes. Run python -m pytest tests/test_parser.py -q. Expected duration is about 15 minutes; keep your edits in the workspace as you go so the diff shows progress. If fixing this requires an API change, explain the concrete dependency before crossing that boundary.

This is local work. Do not publish or change dependencies. Use internal subagents only if an independent check would help; follow the GPT policy in model-routing for model selection. Return the result, changed paths, actual check outcome, and any unresolved limitation as the final response. The CLI captures that response as report.md; place task deliverables outside the run directory.
```

## Broader mission template

```markdown
# Outcome
[Question to resolve or result to produce, with observable acceptance.]

# Context and sources
[Decisions, preferences, failed attempts, or constraints available only in the host conversation. Point to discoverable sources instead of copying them.]

# Ownership and limits
[Work Codex owns, relevant workspace paths, and material exclusions. Grant investigation and judgment needed to finish. Name consequential decisions reserved to the host.]

[Authorized external effects, credentials to use through existing access, and actual resource limits. Pause only the dependent action when authority or a consequential fact is missing. Continue useful authorized work.]

# Internal delegation
Use supported internal subagents when independent work benefits from isolated context. Consult the GPT policy in model-routing before spawning; if it is unavailable, use codex-delegate's internal-subagent fallback. Descendants inherit this mission's limits. Integrate their evidence and settle active children before the final response.

# Expected duration and progress
[Estimate from the mission's size, such as 40 minutes.] Write progress to [a workspace notes file or the deliverable path] as you go, or keep edits in the workspace so the diff grows. Do not use report.md for progress.

# Evidence and handoff
[Required checks or evidence criteria, appropriate to the outcome.]
Return a complete final response with the conclusion, deliverable paths, material decisions, verification outcomes, and remaining limitations. Include child results and unresolved work when children were used. The launcher captures the response as report.md; this path is reserved for CLI capture.
```

Replace the internal delegation grant with a sequential-only constraint only when the user, task dependency, or runtime requires it. If delegation is allowed, the lead need not seek approval for each child inside the grant. Subagents cannot grant themselves more workspace, network, credential, or publication authority.

## Review and investigation

For a review, identify the exact base and proposed revision. Require actionable findings with a concrete failure scenario and file location. A fresh thread provides independent context; resume a prior review when continuity serves the task.

For an investigation, state the decision or question, source boundaries, and evidence needed to settle it. Codex should distinguish observations, supported conclusions, and remaining unknowns. Do not preselect the answer or demand an exhaustive source inventory without a task reason.

Use `read-only` when no workspace edits are needed. CLI final-output capture still produces the report. If the follow-up authorizes edits, update both the packet and sandbox explicitly.

## Resume packet

State the prior run, what is now verified, what remains, and any changed authority. For an unknown outcome, inspect existing effects before redoing work. If only the final report is missing, ask for a complete final response based on existing evidence rather than replaying the task. Include exact next actions only when they are already decided; otherwise grant the judgment needed to finish.
