# Run Recipes

A run directory preserves one CLI attempt. A resumed turn gets a new directory while keeping the original thread ID. The main host owns the relationship between attempts and verifies the task outcome.

## Artifact contract

| File | Role |
| --- | --- |
| `prompt.md` | Packet copied before launch |
| `run.sh` | Fixed launch parameters and one-use wrapper |
| `result.txt` | Provenance followed by the observed terminal record |
| `events.jsonl` | Raw Codex JSONL events |
| `stderr.log` | Codex diagnostics |
| `launcher.log` | Detachment and wrapper diagnostics |
| `report.md` | Final response captured by CLI `-o` |

The wrapper records parameters with Bash quoting and uses an argument array. It never evaluates the packet or interpolates it as shell code. New run directories and files use `umask 077`. Credentials remain in the existing CLI authentication mechanism or environment; the wrapper does not serialize that environment. Raw events and reports can still contain sensitive task data. Keep them out of version control and shared logs.

`result.txt` starts with `sandbox`, `workspace`, `started`, `pgid`, `model`, `effort`, `fast_requested`, `tier`, `network`, `ignore_user_config`, `skip_git_repo_check`, `host_route`, `host_model`, `routing_reason`, and `packet_sha256`. A resume also includes `thread` and `resumed_from`. The source directory's basename is URI-encoded in `resumed_from` so spaces cannot become metadata. Workspace paths may contain spaces; do not split the whole provenance line into whitespace-delimited fields.

The terminal record is `exit=N handoff=ready|incomplete finished=...`. `ready` requires zero CLI exit and a non-empty `report.md` at capture time. The renderer also checks that the report exists now. A clean CLI exit can contain a blocker or an incorrect result; host verification determines task success.

`run.sh` is evidence for inspection. It refuses to run again once `result.txt` exists. Use a new run directory and the launcher for every continuation. The artifacts are ordinary local files. A delegate with write access to them can change them, so they are not independent attestations. Choose a run path outside its writable workspace when that separation matters.

## Launch manifest and recovery

The launcher returns six lines and no task content:

```text
run=/absolute/run/directory
result=/absolute/run/directory/result.txt
events=/absolute/run/directory/events.jsonl
report=/absolute/run/directory/report.md
thread=<thread-id|pending>
provenance=<first result.txt line>
```

Use the path selected before launch to locate a run when output delivery fails. `thread=pending` is valid. The renderer's typed-event parser tolerates JSON whitespace and warnings preceding `thread.started`:

```bash
node "$SKILL_DIR/scripts/render-events.mjs" "$RUN/events.jsonl" --thread
```

This prints only the first usable thread ID, or exits 3 when none is available. A partial last event is not a thread ID. Do not extract arbitrary `thread_id` text from command output or assume the first line contains it.

After settling the original launcher, recover with the same packet:

```bash
bash "$SKILL_DIR/scripts/launch-run.sh" \
  --recover-manifest --run-dir "$RUN" --packet "$PACKET"
```

Recovery requires `prompt.md`, `run.sh`, and provenance. It compares packet bytes, recomputes SHA-256, and checks the recorded hash and host metadata. It does not start Codex or certify completion. If the directory exists but verification fails, preserve it and inspect `launcher.log`, `stderr.log`, and workspace effects. Missing provenance may mean a partial startup. A new directory with a similar name would lose that distinction and can repeat effects.

## Sandbox and configuration

| Mission effect | Launch setting |
| --- | --- |
| Investigation without workspace changes | `--sandbox read-only` |
| Local edits or generated deliverables | `--sandbox workspace-write` |
| Shell network required for authorized work | `--network-access yes` with workspace-write |
| Machine-wide access explicitly granted | `--sandbox danger-full-access` |

For workspace-write, `network=no` passes `sandbox_workspace_write.network_access=false`; `yes` passes `true`. For other sandboxes, `network=no` means no workspace-write network override. It is not a claim that danger-full-access has no network. MCP and built-in tools have separate configuration and authority boundaries.

The launcher sets `model_reasoning_effort`, `service_tier`, and the applicable network setting. It accepts no arbitrary `-c` passthrough and no approval or sandbox bypass flag. Existing account, project, and managed policy can impose further restrictions. A rejection is evidence to diagnose, not permission to turn those restrictions off.

`--ignore-user-config yes` skips `$CODEX_HOME/config.toml`; authentication still uses `CODEX_HOME`. It does not imply a clean environment or removal of project instructions. `--skip-git-repo-check yes` permits an intended non-Git working directory. Neither option installs or logs in to anything. These flag meanings were checked against CLI 0.159.3 and the [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) on 2026-10-06.

## Status and events

```bash
node "$SKILL_DIR/scripts/render-events.mjs" "$RUN/events.jsonl" --status
node "$SKILL_DIR/scripts/render-events.mjs" "$RUN/events.jsonl" --tail 20
```

| Evidence | State | Interpretation |
| --- | --- | --- |
| Exit zero and a non-empty report | `DONE` | Handoff available for verification |
| Exit zero with no usable handoff | `INCOMPLETE` | Task outcome needs inspection |
| Nonzero CLI exit | `EXITED` | Failure or interruption to classify |
| No terminal line, live group | `RUNNING` | Process group exists |
| No terminal line, absent group | `DIED` | Outcome unknown after process loss |
| No usable process identity | `UNKNOWN` | Liveness cannot be established |

Legacy `cancelled=` and `cancel_failed=` lines remain visible as legacy states. A legacy zero-exit line without a handoff marker needs a currently non-empty report before the renderer calls it `DONE`. Do not rewrite old records to resemble a newer format.

The renderer streams JSONL, caps action lines, omits command output and diffs, and degrades malformed or unknown events to markers. `--tail N` retains only N rendered lines. The underlying line reader can still allocate a large single line before the JSON size check. Use targeted local searches for deeper inspection instead of printing a complete raw log.

`thread.started`, `turn.*`, and `item.*` are the documented event families. `turn.failed` and a nonzero exit indicate failure. An `error` item can be a warning. `collab_tool_call` can expose root-visible child state, but the stream is not a complete census of descendant activity. Preserve the delegate's final child summary when it used subagents.

A live process group and an old log timestamp do not distinguish reasoning, waiting, and a stalled process. Diagnose stderr, outstanding work, and the task's actual time limit before cancelling. Do not auto-retry from silence or fabricate success from activity.

The packet's expected duration and progress artifact make a stall visible. Check the artifact at about a third of the expected duration and again when it ends. A running Codex turn cannot take a message, so when nothing in the mission's write scope or progress file has changed for a large part of the estimate and no task command is running, cancel through the procedure below. Then resume with a packet that starts from the partial artifacts and states what is already done; do not relaunch the original packet. A run that is still producing progress past its estimate is slow, not stalled; let it finish or narrow the next resumed turn.

## Observation across hosts

Use the host's native background completion facility when it can wake the main session. A bounded watcher can be attached there:

```bash
# Run through the host's background-job facility, not a blocking foreground wait.
while :; do
  grep -Eq '^exit=[0-9]+( |$)' "$RUN/result.txt" 2>/dev/null && break
  PG=$(sed -n '1s/.* pgid=\([0-9]*\).*/\1/p' "$RUN/result.txt" 2>/dev/null)
  case "$PG" in ''|*[!0-9]*) break ;; esac
  [ "$PG" -gt 1 ] || break
  kill -0 -"$PG" 2>/dev/null || break
  sleep 10
done
```

The watcher ending means the host should inspect status; it is not task success. A watcher can be recreated without restarting Codex. When the host has no completion notification, keep using its supported bounded checks and retain the exact run path for follow-up. Do not promise an unsolicited wake-up the host cannot deliver.

## Resume and concurrency

A resume uses a new packet, the exact source run, and a fresh path. The launcher inherits recorded sandbox, model, effort, Fast assertion, network, config, and Git-check settings unless explicitly overridden. Missing optional legacy assertions default to `no`; required sandbox, model, or effort metadata must be present or provided deliberately.

The source must have a usable typed thread event and either a terminal record or a recorded process group that is no longer present. A source with unknown liveness is rejected before creating a new run. The launcher checks that source attempt, not every historic resume. The host must inspect the latest known attempt and keep one active turn per thread. It must also retain the same authorized CLI account and session store; the script does not copy credentials or move a thread between accounts.

Model policy is applied when deciding the follow-up. Inspect a legacy attempt's inherited settings and select the route under the current policy; pass explicit model options and record the route reason when changing it. Widening filesystem or external authority requires the user's existing or new grant and a matching packet. Read-only roots can share a workspace; concurrent writers need isolated workspaces or worktrees. CLI thread identity alone does not coordinate writes.

Before any recovery, inspect effects that may have occurred before a lost response. For a missing final response, resume to reconstruct the handoff. For a partial implementation, continue from the existing files and evidence. For a confirmed launch failure before a thread exists, a fresh launch may be appropriate after the failure is resolved. Preserve the failed attempt.

## Cancellation

Read status and confirm that the recorded group still belongs to this run before signalling. Do not signal a terminal run or trust an old PGID by number alone. The wrapper command should reference the exact `run.sh` path:

```bash
PG=$(sed -n '1s/.* pgid=\([0-9]*\).*/\1/p' "$RUN/result.txt")
case "$PG" in ''|*[!0-9]*) exit 64 ;; esac
[ "$PG" -gt 1 ] || exit 64
# Inspect identity first. Continue only if this is the expected run wrapper.
ps -p "$PG" -o pid=,pgid=,command=
```

After confirming identity and the absence of a terminal record:

```bash
kill -INT -"$PG"
```

The wrapper catches SIGINT while Codex receives it, allowing a terminal record after the child returns. Observe the result rather than assuming a particular exit code. Historical CLI 0.145.0 evidence and current deterministic fixtures cover this path; abrupt termination can leave tool children outside the wrapper's group.

If graceful cancellation fails, inspect surviving processes before escalating to TERM or KILL on the confirmed group. Record the host action and observation in a separate `cancellation.md`; preserve `result.txt` and partial artifacts. Check for surviving task processes and external effects before resuming. Process identity checks reduce stale-PID risk but cannot make a shell check and signal atomic.

For legacy runs without PGID, do not run a broad `pkill codex` or manufacture process metadata. Inspect full process arguments for the exact report path and establish an unambiguous owner. If identity cannot be established, retain `UNKNOWN` and report that cancellation was not confirmed.

## Local artifacts

Prefer a run directory outside the repository when repository-wide tools would traverse its artifacts. Otherwise add a local exclusion from that repository:

```bash
EXCLUDE="$(git rev-parse --git-path info/exclude)"
grep -qxF '.agent-runs/' "$EXCLUDE" || printf '%s\n' '.agent-runs/' >> "$EXCLUDE"
```

A local exclusion does not change repository policy and does not stop non-Git directory walkers. Keep intentional task deliverables in their designated paths. Preserve run files until the result has been accepted or the user asks for cleanup.

## Contract fixture

Run these from the skill root with `node` on `PATH`. The contract test calls Node.js directly, so Bun alone does not run it.

```bash
CODEX_DELEGATE_KEEP_FIXTURES=yes bash scripts/test-run-contract.sh
node scripts/render-events.mjs scripts/fixtures/sample-events.jsonl --tail 20
```

The first command runs the real launcher and renderer against deterministic CLI output and processes. It uses a local `codex` fixture with no model call. It exercises detachment, packet and output preservation, completion gating, cancellation, recovery without duplicate launch, resume provenance, and explicit network settings. It prints the retained fixture directory for inspection. Omit `CODEX_DELEGATE_KEEP_FIXTURES` for automatic cleanup. The setsid branch uses a semantics-compatible local shim, so the fixture does not validate the GNU utility or account access. Real model quality and current host-specific background notifications require separate evidence.
