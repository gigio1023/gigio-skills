---
name: read-agent-sessions
description: >
  Locate and read a Codex, Claude Code, Zcode, or Hermes session stored on this
  machine and extract a readable conversation or takeover summary from a session
  id prefix, conversation title, or remembered prompt fragment. Use for "find
  that codex session about X", "summarize this claude session", or "read session
  abc123 and continue the work".
---

# Read Agent Sessions

Turn a loose session reference — an id prefix, a title someone remembers, or a fragment of a prompt — into a verified handoff another agent can act on. All four harnesses keep complete transcripts on the machine where the session ran, so the work is resolution and faithful extraction, never reconstruction from memory. The skill applies regardless of which agent runs it; loading it grants no write access to any session store.

## Quick Start

1. Identify the deliverable: locate a session, extract a conversation, or produce a takeover summary. Preserve the requester's harness if named, and their intended consumer — another agent, the user, or both.
2. Identify the harness before touching storage. The identifier often decides it: a `sess_` prefix means Zcode, `YYYYMMDD_HHMMSS_<hex>` means Hermes, and a bare UUID is Codex or Claude Code and needs the requester's intent or both stores searched.
3. Use the resolution map below to choose the lookup route. Treat a match as a hypothesis until the file or row is opened and its first records confirm the expected conversation.
4. Follow the identified harness's reference before extracting. Each store has its own schema, duplicate-content traps, and subagent linkage; the recipes there were verified against real stores on the author's macOS machine at the versions and dates each reference states, so confirm them against the store in front of you.
5. Extract the human-readable conversation: real user turns and assistant text, skipping tool plumbing, system-injected context, and reasoning blocks. Follow subagent or child sessions when the main transcript delegates work the requester cares about.
6. Verify the summary against the extracted records before reporting. Dates, paths, decisions, and quoted claims in the handoff must appear in the transcript; a plausible summary that outruns its evidence is a failure, not a shortcut.
7. Deliver the handoff with the harness and session id so the receiver can re-read the source, plus any gaps such as encrypted reasoning or missing titles. Add the project path, time range, or resolution chain when they help.

Prerequisites: `jq` for the JSONL recipes, and the `sqlite3` CLI with JSON1 (`json_extract`) and FTS5 (`messages_fts`) for the SQLite recipes. When a tool is missing, do not install it without the user's approval; read the same files with a short Python standard-library script instead (`json` line by line for JSONL, the `sqlite3` module with a `file:...?mode=ro` URI for databases), and fall back from FTS5 to `LIKE` filters if that build lacks it.

References, one per harness:

- [Codex sessions](references/codex-sessions.md) — JSONL rollouts under `~/.codex/sessions/`, title index in `~/.codex/session_index.jsonl`. CLI and desktop app share one store.
- [Claude Code sessions](references/claude-code-sessions.md) — JSONL transcripts under `~/.claude/projects/`, titles from `custom-title` records or desktop metadata. CLI and desktop app share one store.
- [Zcode sessions](references/zcode-sessions.md) — SQLite at `~/.zcode/cli/db/db.sqlite` with `session`/`message`/`part` tables.
- [Hermes sessions](references/hermes-sessions.md) — SQLite at `~/.hermes/state.db` with FTS5 search, plus a read-only `hermes sessions` CLI.

## Resolution Map

Loose identifiers arrive in three shapes. Each has a preferred route and a fallback; when several sessions match, list the candidates with their first user message and timestamp instead of silently picking the newest.

| Identifier shape | Preferred route | Fallback |
| --- | --- | --- |
| Session id or its prefix | Direct filename or table lookup by id | Title index, then prompt history |
| Conversation title or topic | Title index (Codex `session_index.jsonl`, Claude `custom-title` or desktop metadata, Zcode `session.title`, Hermes `sessions.title`) | First-user-message scan or FTS |
| Remembered prompt fragment | Prompt history (`~/.codex/history.jsonl`, `~/.claude/history.jsonl`, Hermes `messages_fts`) | Grep raw transcripts, narrowed by date or project |

## Applying The Workflow

### Separate Missing Information From Missing Authority

Not knowing which of three matching sessions is the right one is a question of fact: resolve it with the candidates' first user messages and timestamps, and ask the requester only when the choice materially changes what gets handed over. Read access to a session store, by contrast, is a standing boundary: every lookup in this skill is read-only regardless of how clearly the task would benefit from indexing, renaming, or pruning. Open SQLite stores with `mode=ro` (both Zcode and Hermes databases are live and WAL-backed); never copy, checkpoint, or write them.

When a requested action exceeds reading — resuming a session in its own harness, deleting or editing transcripts — say so and finish the read-only portion. The handoff itself is the authorized next step: it gives the receiving agent everything needed to resume under its own authority.

### Inspect The Actual Store, Not The Documentation Of It

Session formats drift between harness versions and platforms, and the stores the references were verified on already diverged from the widely documented defaults: that Claude Code store had no `summary`-type records, and Hermes kept its transcripts in `state.db` rather than the directory named `sessions/`. When a store does not match its reference, inspect the real schema (`.schema`, or the first lines of a JSONL) and adapt the extraction; report the divergence rather than forcing the documented shape. Treat each reference's caveats as the boundary of what was confirmed on the author's machine, not as universal claims.

### Make The Handoff Verifiable

A takeover summary is only as good as its traceability. Include the session id and harness so the receiver can re-read the source; quote decisions and open threads in terms the transcript supports; and separate what the transcript proves from what you inferred. Reduce long sessions in slices — sample head and tail, count turns by role — before a full read, rather than summarizing from a partial extraction and presenting it as complete.

Subagent sessions are part of the record: Codex child rollouts link through `parent_thread_id`, Zcode subagents carry `sess_subagent_agent_` ids with `parent_id`, and Claude Code marks them `isSidechain: true`. Note when delegated work was followed and when it was skipped as out of scope.

Sessions can contain secrets the original conversation handled. Summarize their effect when the task requires it, but never copy credentials into a handoff verbatim. The rest of a transcript needs a boundary too:

- Write extract files only where the requester names. Otherwise keep them in a local temporary directory and report their location.
- Give the receiving agent the minimum summary the task needs, not the raw transcript.
- Do not send raw transcript text to another model provider, repository, or shared document without the user's direction.
- Summarize third parties' personal details and confidential work content only as far as the handoff requires.

## Output

Return the handoff summary with the harness and session id, the extract or its location if the requester needs raw turns, verified facts distinguished from inference, and material gaps: encrypted content, missing titles, ambiguous matches left for the user to decide. A session that cannot be found is reported as not found with the routes tried — an honest miss, not a reconstructed guess.

## Gotchas

- A bare UUID identifies both Codex and Claude Code sessions; searching one store and reporting a miss while the other was never checked is the most common wrong-session handoff.
- Codex `event_msg` records duplicate the transcript for streaming; build conversations from `response_item` records only.
- Tool results masquerade as user turns in Claude Code (`tool_result` content in user-type records) and Hermes (regenerated duplicate rows); use the filters in each reference or the conversation reads as self-talking.
- Codex filenames embed local time while records use UTC; reconciling the two without converting shifts sessions by hours.
- The newest match for a fuzzy title is a candidate, not an answer; recurring topics produce sibling sessions.
