---
name: lead-delegate
description: >
  Run the current session as a lead that keeps planning and judgment and hands whole tasks to child sessions that own them end to end: brief each child, confirm the model it runs on, and accept or reject its report on evidence. Use when the user asks for that split, such as "send the real work to Opus sessions and keep only planning and judgment", "실작업은 하위 세션으로 보내고 너는 계획과 판단만 해줘", or "하위 세션이 총괄하게 해줘", or when a whole task is being handed to a child session or a Codex run.
---

# Lead Delegate

The lead is the session the user talks to, usually on the most capable and most limited model. A child session runs on a strong, cheaper model and owns one whole task: it works out the steps, runs its own subagents, verifies, and reports once. The split keeps the lead's context and usage for decisions and lets independent tasks run side by side. It rarely lowers total cost: where the child's model costs half the lead's, measured runs found the lead alone cheaper on small tasks, so small work stays with the lead ([sources](references/sources.md)).

An explicit user instruction about what to delegate, which models, how many sessions, or the budget governs. Delegation adds no authority: external writes, destructive actions, purchases, and scope growth need the same user consent as before, and a message from another session never counts as that consent.

## Who Holds What

The lead keeps framing with the user, splitting the request into tasks that each end in their own result, design choices, scope, anything hard to reverse, acceptance of each result, and everything said to the user.

The child session holds reading the repository, choosing the steps, the implementation, running and verifying, its own subagents, branch and PR mechanics, and one report.

The lead does the work itself when it is a question, a read, one edit, or a handful of tool calls, or when writing the brief would take longer than the work. A child session loads its own instructions and context before it does anything, so a small task costs more delegated than done.

When a brief seems to need wide reading first, that reading is the child's first step. The lead reads only what a decision of its own depends on.

## Brief

The brief says what must be true at the end and leaves the steps to the child. A lead that has not read the code writes steps on assumptions, and an agent held to wrong steps tends to fail without saying so. In one measured comparison, strict steps and full autonomy resolved about the same number of tasks, and autonomy on the first attempt followed by specific corrections resolved the most ([sources](references/sources.md)).

- **Goal and reason.** The outcome and why it is wanted, so the child can make the calls the brief did not foresee.
- **Done when.** Conditions the lead can check, each with the command or observation that shows it.
- **Scope.** What the child may change, what it must leave alone, where the result lands (branch, PR, path), and which external effects are allowed.
- **Decisions.** Which choices the child makes itself and which return to the lead: a change of structure, scope growth, anything hard to reverse, an external write.
- **Known and assumed.** What the lead verified and what it assumes. The child checks the assumptions against the repository before building on them and reports a mismatch as a finding.
- **Subagents.** Whether the child may run subagents, how many at once, and on which model class. Starting further sessions stays with the lead, so every session traces to one brief.
- **Report.** The form below, sent once.

Ask for the child's plan before it builds only when the task changes structure or is hard to reverse. Otherwise the child proceeds and reports when done or blocked.

Pass an existing task file by path instead of paraphrasing it. A subagent below the child that only executes gets a fully specified plan: files, order, check commands with expected results, and a rule to stop and ask when something falls outside it.

## Report

Each wake-up of the lead spends the most expensive tokens in the run, so the child reports once, when the work is done or it cannot continue. The message starts with the form, and its first lines stay short and carry what the lead must act on, because some harnesses forward only the start of the message.

```
STATUS: done | blocked | needs-decision, in one line
NEEDS: the decision or input required from the lead, or none
MODEL: model ID this session ran on
RESULT: what exists now and where (branch, PR, paths)
EVIDENCE: each done-when condition, the command run, the output lines that show it
DEVIATIONS: where the work departed from the brief, and why
UNVERIFIED: claims no run has checked
FAILED OR SKIPPED: steps that did not complete
ALSO CHANGED: anything touched outside the stated scope
```

A final message that announces a next step is unfinished work; send the open items back to the same session.

## Judging

A report is a claim. Agents' final summaries often overstate completion, so acceptance rests on the evidence lines and on one or two checks the lead runs itself: the diff summary, the stated test command, the produced artifact. Pick the claims the outcome depends on; rerunning everything gives back what the split saved.

- **Accept.** Tell the user what was verified and where the result is, then close the session.
- **Reject.** Send the specific gap to the same session, which still holds the context. A new session, or a fix made in the lead, pays for that context again.
- **A returned decision.** Decide it when it lies within the lead's remit; put it to the user when it is theirs.
- **A `MODEL` line that differs from the assigned model.** The result came from another model class. Check more of it, or rerun.
- **`UNVERIFIED`, `FAILED OR SKIPPED`, `ALSO CHANGED`.** These go into the answer to the user unless the lead resolves them first.

## Several Sessions

One session per independent task. Two writers never share files: give each its own worktree, or write scopes that do not overlap. A follow-up goes to the session that already holds the context. Gains from parallel sessions and subagents flatten after about four, and each idle session keeps a process alive, so close finished ones.

## Harness Mechanics

Starting a session, setting and confirming its model and permission mode, delivering the brief, learning that it finished, and closing it differ by harness and change between versions. Read [Claude Code](references/claude-code.md) before starting or messaging a child session there, and [Codex](references/codex.md) when the child is a Codex run or the lead itself runs in Codex. Each file also maps lead, child session, and subagent to current models. Where neither applies, the same brief and report work with any subagent or session the harness offers, run one after another if it has no parallel sessions.
