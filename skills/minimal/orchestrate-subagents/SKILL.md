---
name: orchestrate-subagents
description: >
  Run parallel subagent work: split a task into packets, dispatch them as
  their inputs become ready, catch stalled or oversized workers, and merge
  results by evidence. Use when the user asks for parallel subagents,
  delegated agents, agent teams, or competing research tracks, names this
  skill, or the lead decides to run a multi-agent wave in Codex, Claude Code,
  Cursor, or a similar harness.
---

# Orchestrate Subagents

Use the harness's native subagent, task, thread, or worktree mechanism. Without one, run the same packets sequentially and say so; never describe sequential work as parallel.

An explicit user instruction about delegation governs: whether to delegate, how many workers, which models, and the budget. Without one, the lead decides and sizes the wave from the independent work that exists. A subagent that runs this skill keeps to any lower fan-out limit its instructions set for subagents. Delegation adds no authority for external writes, destructive work, purchases, or scope expansion. The lead keeps framing, conflict resolution, final judgment, and user communication.

## Packets

A packet gives the worker its objective, its scope (including what it must not touch), the output it returns, and a progress artifact the lead can inspect. Add an expected duration to any packet longer than a few minutes. When the task already lives in a file, pass the path instead of paraphrasing it. Ask for a last message that is a result or a stated blocker with what remains, never a plan for what it will do next. Say whether the worker may spawn its own subagents.

## Dispatch Loop

Plan the run as a dependency map, not as waves. Each packet names what it needs before it can start: another packet's artifact, a lead decision, or nothing. A packet whose inputs exist is ready, so it never waits for an unrelated worker that happened to start beside it.

Keep a light ledger of live workers: packet, write scope, start time, expected duration, progress artifact, and the packets waiting on it. Writing the expected duration down is what makes a stall visible.

On each event (a worker finishes, a check fires, the user writes): integrate results that unblock other packets, dispatch packets that became ready within the limit and budget, check live workers for stalls, and advance a lead slice that overlaps no worker's write scope. Before ending a turn to wait, check whether any ready packet is still undispatched.

**Packet size.** The run ends when its slowest packet ends. Estimate each packet's duration when you map it, and split one that is much longer than the rest by source, file, module, branch, or claim group. Shorter packets also make stalls visible sooner.

**Sequential chains.** For work where each step builds on the previous one, such as stacked branches, ordered migrations, or a rebase series, keep only the chain's order serial and give it to one integrator. Pull out every node that does not depend on that order (a fix that can target the base, a standalone tool, a review of a finished link, docs that need only names) into its own packet. Start the integrator when the first links' inputs exist.

**Verification packets.** Size review and verification by independently checkable units, such as one reviewer per branch, module, or claim group. A few reviewers covering many units turn the final phase serial.

**Liveness.** Many harnesses report a background worker only when it stops, so a stalled worker and a working one look the same.

- Check the progress artifact at about a third of the expected duration and again when it ends. A generic long fallback timer can hide a stall for an hour.
- Judge progress by changes in the worker's write scope and by its running processes. Transcript and log timestamps can lag behind an active worker.
- Stalled (nothing changed for a large part of its expected duration, no commands running): send one message asking for its result or blocker. If the next check still shows nothing, stop it and dispatch a replacement packet that starts from its partial artifacts, says what is done, and keeps the original output paths.
- Slow (still progressing, past its estimate, while slots sit idle): narrow its scope to the part in progress and dispatch new packets for the untouched remainder.

These rules come from an observed run reviewing and reworking a stacked PR series: a stalled reviewer went unnoticed behind a long fallback timer, a downstream phase with ready inputs waited on it, independent nodes ran serially inside one worker, and final verification used far fewer reviewers than the limit allowed.

## Harness Facts

- **Claude Code.** A background subagent notifies the lead only when it stops. Do not read its transcript file, which can overflow the lead's context, and do not treat the transcript's modification time as progress. Check its write scope (worktree diff, report file) and the process list. `SendMessage` reaches a running subagent at its next tool call, so a worker stuck inside one long call does not see it. Subagents can spawn their own subagents, and nesting stops two layers below the main conversation; remove `Agent` from a worker's tools when it may not spawn. A subagent does not inherit skills the parent loaded.
- **Codex.** Wait only when blocked on a result, with a timeout set to the packet's expected duration, and check the worker's artifacts when it expires. Never wait without a bound.
- **Shared checkouts** (Cursor, OpenCode, or any harness without worktree isolation): keep write scopes disjoint and narrow, and tell workers that others may be editing nearby files and that they must not revert changes they did not make.

## Results

- Merge claims, not summaries: keep each claim with its source, whether it is direct evidence or inference, and its confidence. When workers disagree, check first whether they answered the same question, then prefer primary sources and executable evidence.
- A worker saying it is done is not proof. Check its artifact, diff, cited source, or test before reporting progress.
- A result that announces its next step is unfinished. Resume the worker with the open items; some models, Claude Opus 5.5 among them, can end a turn on a progress note.
- After the user corrects the task, inspect active workers before redispatching. A sent correction does not prove the worker received it.
- Launch a follow-up wave only when a gap or conflict would change the answer. Re-anchor it with what is known and what remains open, not the whole conversation.
- Close finished workers once their results are integrated. Ending a worker does not authorize deleting its files or worktree.

## Gotchas

- More agents can make the answer worse when they duplicate effort, share one bad premise, or return unranked summaries.
- Use a deterministic tool path, not subagents, for filtering, joining, or aggregation that needs no judgment between calls. Keep work direct when each result decides the next move.
- Do not spawn a subagent to re-check the lead's own reasoning. A reviewer earns its cost through fresh context on the specification and artifact.
- Do not wait idly while workers run; advance non-overlapping work.
