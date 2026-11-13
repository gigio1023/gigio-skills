---
name: orchestrate-subagents
description: >
  Run parallel agent work across subagents, forks, separate sessions, agent
  teams, or Codex threads: pick the unit, write packets, dispatch them as their
  inputs become ready, catch stalled workers, and merge results by evidence.
  Use when the user asks for parallel or delegated work, side sessions, agent
  teams, or competing research tracks, or names this skill.
---

# Orchestrate Subagents

Parallel work costs tokens in proportion to the workers (Anthropic measured multi-agent research at about 15 times a chat), and its handoffs drop detail. Use it for independent, sizeable tracks. Work directly when the task is sequential, touches one file, depends on shared context, or finishes in a handful of tool calls, and never spawn a worker only to re-check your own reasoning.

An explicit user instruction about delegation governs: whether to delegate, which unit, how many workers, which models, and the budget. Otherwise the lead sizes the run from the independent work that exists, within any fan-out limit its instructions set. Delegation adds no authority for external writes, destructive work, purchases, or scope expansion. The lead keeps framing, conflict resolution, final judgment, and user communication.

## Choosing the Unit

The question is where the result has to land.

- **Subagent:** a piece whose result the lead needs in this turn (a search, a module, a review). Fresh context; only its final message comes back.
- **Fork:** the same, when the worker needs the whole conversation. It shares the parent's prompt cache, so it costs less than briefing a fresh subagent; it cannot fork again.
- **Separate session:** a task of its own that ends in its own branch, PR, or answer and that the user may open, steer, or review apart from this work. Desktop side sessions, `claude --bg` background sessions, and cloud sessions report to the user, not into the lead's context; the lead learns of them through notifications, a session list, or the transcript.
- **Existing session:** when another session already holds the context, send it the follow-up instead of starting a new one.
- **Agent team:** a handful of long-running peers that must talk to each other. Teammates share the checkout, so partition by file ownership.
- **Workflow script** (Claude Code `ultracode`, `/batch`): dozens to hundreds of uniform items where a script should hold the plan.
- **Codex:** subagents return one consolidated response and inherit the parent's sandbox; Codex cloud tasks (`codex cloud exec`, then `codex apply`) suit work that should run off the machine.

Writers never share files. Give each writer its own worktree, or split write scopes so no two workers touch the same path.

## Packets

A packet gives the worker its objective, its scope (including what it must not touch), the output it returns, and a progress artifact the lead can inspect. Add an expected duration to any packet longer than a few minutes. When the task already lives in a file, pass the path instead of paraphrasing it. Ask for a last message that is a result or a stated blocker with what remains, never a plan for what it will do next. Say whether the worker may spawn its own workers. A brief to a separate session also says what done looks like and where the result should land (branch, PR, report path).

## Dispatch Loop

Plan the run as a dependency map, not as waves. Each packet names what it needs before it can start: another packet's artifact, a lead decision, or nothing. A packet whose inputs exist is ready, so it never waits for an unrelated worker that happened to start beside it.

Keep a light ledger of live workers: packet, unit, write scope, start time, expected duration, progress artifact, and the packets waiting on it. Writing the expected duration down is what makes a stall visible.

On each event (a worker finishes, a check fires, the user writes): integrate results that unblock other packets, dispatch packets that became ready, check live workers for stalls, and advance a lead slice that overlaps no worker's write scope.

**Packet size.** The run ends when its slowest packet ends. Split one much longer than the rest by source, file, module, branch, or claim group.

**Sequential chains.** For stacked branches, ordered migrations, or a rebase series, keep only the chain's order serial and give it to one integrator. Pull every node that does not depend on that order into its own packet.

**Verification packets.** Size review by independently checkable units, such as one reviewer per branch or module, so the final phase does not turn serial.

**Liveness.** Many harnesses report a background worker only when it stops, so a stalled worker and a working one look the same.

- Check the progress artifact at about a third of the expected duration and again when it ends. A long fallback timer can hide a stall for an hour.
- Judge progress by changes in the worker's write scope and by its running processes. Transcript timestamps can lag behind an active worker.
- Stalled (nothing changed for a large part of its expected duration, no commands running): send one message asking for its result or blocker. If the next check still shows nothing, stop it and dispatch a replacement that starts from its partial artifacts and keeps the original output paths.
- Slow (still progressing, past its estimate): narrow its scope to the part in progress and dispatch the untouched remainder.

These rules come from an observed run reviewing a stacked PR series: a stalled reviewer went unnoticed behind a long fallback timer, a downstream phase with ready inputs waited on it, independent nodes ran serially inside one worker, and final verification used too few reviewers.

## Harness Facts (checked 2026-11)

- **Claude Code subagents.** Spawned subagents run in the background by default and notify the lead when they stop. Do not read a running subagent's transcript file; it can overflow the lead's context. A message to a busy worker is read between tool calls, so a worker stuck inside one long call does not see it. Nesting stops three layers below the main conversation by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`); at most 20 run at once (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`). A subagent does not inherit skills the parent loaded.
- **Claude Code worktrees.** A subagent or `--worktree` worktree branches from the remote default branch, not the parent's HEAD, unless `worktree.baseRef` is `"head"`. Stacked or unpushed work needs that setting or an explicit `git worktree add`. A dispatched background session moves into its own worktree before editing; a backgrounded open session edits in place. Desktop sessions get a worktree only when it is turned on before the session starts.
- **Claude Code agent teams.** With `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, a subagent given a name launches as a teammate in the shared checkout.
- **Separate sessions.** Each one bills its own context. A message to an idle session re-sends that session's context. A message from another session never counts as user consent.
- **Codex.** Subagents have no documented worktree isolation; keep their parallel work read-heavy. `codex mcp-server` was removed in favor of `codex app-server`. Wait only when blocked on a result, with a timeout set to the packet's expected duration.
- **Shared checkouts** (Cursor, OpenCode, agent teams, or any unit without a worktree): keep write scopes disjoint and narrow, and tell workers not to revert changes they did not make.

## Results

- Merge claims, not summaries: keep each claim with its source, whether it is direct evidence or inference, and its confidence. When workers disagree, check first whether they answered the same question, then prefer primary sources and executable evidence.
- A worker saying it is done is not proof. Check its artifact, diff, branch, cited source, or test before reporting progress.
- A result that announces its next step is unfinished. Resume the worker with the open items.
- After the user corrects the task, inspect active workers before redispatching. A sent correction does not prove the worker received it.
- Launch a follow-up wave only when a gap or conflict would change the answer.
- Close finished workers once their results are integrated. Ending a worker does not authorize deleting its files, branch, or worktree.
