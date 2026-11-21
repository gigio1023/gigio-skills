# Claude Code

Checked 2026-11-21 against the Claude Code 2.1.330 docs and the desktop app's session tools as listed in a live session. The session tools are not in the public docs and change between app versions, so trust the tool list in front of you over this file.

## Roles and Models

Defaults when the user has set none. A user instruction, a preference file, or an installed routing policy overrides every row, and effort follows the same sources.

| Role | Model | Note |
| --- | --- | --- |
| Lead | The session the user opened | Mythos 5.2 or Fable 5.2 |
| Child session | `claude-opus-5-5` | A full session |
| Subagent with judgment | Opus 5.5 | Implementation, diagnosis, review |
| Subagent executing a fixed plan | `sonnet` | Read-only collection, fixed command runs |

A subagent with no model set runs on its parent's model, so a child session's subagents are Opus unless the spawn names another model. Per the docs the order is spawn parameter, agent definition, `CLAUDE_CODE_SUBAGENT_MODEL`, then the parent.

## Desktop App Sessions

**Start.** `start_session` takes `model`, `effort`, `permission_mode`, `name`, `use_worktree`, and `wake_when_done`. `model` must be the lead's family or cheaper; a higher one is ignored. `permission_mode` must be the lead's own or lower; a higher one is refused. Raising a child later goes through `set_session_permission_mode`, which shows the user an approval card, so a child session in `bypassPermissions` needs a lead already in that mode or the user's approval on that card. A fresh-context start also needs `background`, at least 80 characters for someone who has not seen the conversation.

**Confirm before the brief.** A child has started on the lead's model despite the request (observed 2026-11-13), and a model change applies only from the next turn. Make the first prompt a one-line instruction to wait for the brief. Then call `get_session` and read `model`, `effort`, and `permissionMode`. Correct with `set_session_model` or `set_session_effort`, read again, and only then send the brief. Repeat the check when resuming a session after a pause.

**Brief.** `SendMessage` with `to` set to the session's `local_...` id. It arrives as a user turn labelled with the lead's session title.

**Finish.** When the child ends a turn and the lead is idle, the app continues the lead with a note quoting the first 400 characters of the child's last message. The `STATUS`, `MODEL`, and `NEEDS` lines come first for that reason. Read the rest with `list_events` on the session. Polling is unnecessary. A cloud session sends no note.

**Result location.** A child in its own worktree commits to its own branch. The lead's checkout has none of that work until the branch is merged, and merging is the user's call.

**Close.** After acceptance, `archive_session` stops the session's process and by default removes its worktree; `unarchive_session` reverses it. Keep a session that has an open PR or a pending follow-up. Archive only with the user's agreement; a standing instruction to archive accepted sessions is that agreement.

## CLI Sessions

`claude --bg "<prompt>"`, or `claude agents` with `--model`, `--effort`, and `--permission-mode`, starts a background session. It reports to the user. The lead reaches it with `ListAgents` and `SendMessage`. Adding `notify_when_idle` to a `SendMessage` returns one notice when that session next goes idle; it works from the main conversation only, for sessions on the same machine, and is dropped after 12 hours.

When `crossSessionInbound` is unset, delivery depends on the two sessions' permission classes. Sessions that bypass permission prompts form one class and all others the second. A message between sessions of different classes is held for the user's approval. A terminal session shows an approval dialog; a Desktop app or VS Code session cannot show it and drops the message at `dialogExpiry`, five minutes by default. Run the lead and its child sessions in the same class, or set `crossSessionInbound` to `accept`. Whether the desktop app's own session tools follow this rule is untested.

## Advisor in the Child Session

Optional and unmeasured in this setup. With `--advisor fable`, `/advisor fable`, or the `advisorModel` setting, a child session on Opus 5 or 5.5 can consult Fable at a decision point without waking the lead, and its subagents inherit the advisor. The pairing table accepts Fable or Opus 5 and later for an Opus 5.5 main model and does not list Mythos. The feature is experimental, has no setting that caps or forces calls, re-reads the whole transcript uncached on every call, and bills a Fable advisor to usage credits on some plans.
