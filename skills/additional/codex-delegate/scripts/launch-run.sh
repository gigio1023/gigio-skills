#!/bin/bash
set -u
umask 077

SKILL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

usage() {
  cat >&2 <<'EOF'
usage: launch-run.sh --workspace DIR --packet FILE --run-dir DIR (--sandbox MODE | --resume-from RUN) [options]
       launch-run.sh --recover-manifest --run-dir DIR --packet FILE

Options:
  --model MODEL              new-thread default: gpt-6-astra
  --effort EFFORT            new-thread default: xhigh
  --fast-requested yes|no    new-thread default: yes
  --network-access yes|no    new-thread default: no; yes requires workspace-write
  --ignore-user-config yes|no
                              new-thread default: no
  --skip-git-repo-check yes|no
                              new-thread default: no
  --host-route ROUTE         launcher-subagent or direct-main
  --host-model MODEL         exact host model ID, or unavailable
  --routing-reason REASON    one whitespace-free route reason
  --resume-from RUN          inherit a prior run's thread and launch settings
  --run-dir DIR              required absent path selected by the main host
  --recover-manifest         verify and print an existing run's manifest only
EOF
}

fail() {
  printf 'launch-run: %s\n' "$*" >&2
  exit 64
}

packet_sha256() {
  local hash
  hash=$(openssl dgst -sha256 -r "$1" 2>/dev/null | awk '{print $1}') || return 1
  [ "${#hash}" -eq 64 ] || return 1
  printf '%s\n' "$hash"
}

# Scalar provenance stays one token. Paths remain quoted argv, never shell source.
validate_token() {
  case "$2" in
    ''|*[!a-zA-Z0-9._:/+-]*) fail "$1 must be a nonempty metadata token" ;;
  esac
}

read_thread() {
  "$RUNTIME" "$SKILL_DIR/scripts/render-events.mjs" "$1/events.jsonl" --thread
}

emit_manifest() {
  local provenance thread
  provenance=$(sed -n '1p' "$RUN/result.txt")
  thread=
  if [ -s "$RUN/events.jsonl" ]; then
    thread=$(read_thread "$RUN") || thread=
  fi
  if [ -z "$thread" ]; then
    thread=$(printf '%s\n' "$provenance" |
      sed -n 's/.* pgid=[0-9]* thread=\([^ ]*\) resumed_from=.*/\1/p')
  fi
  thread=${thread:-pending}

  printf 'run=%s\n' "$RUN"
  printf 'result=%s\n' "$RUN/result.txt"
  printf 'events=%s\n' "$RUN/events.jsonl"
  printf 'report=%s\n' "$RUN/report.md"
  printf 'thread=%s\n' "$thread"
  printf 'provenance=%s\n' "$provenance"
}

WORKSPACE=
SANDBOX=
SANDBOX_SET=no
PACKET=
MODEL=
MODEL_SET=no
EFFORT=
EFFORT_SET=no
FAST_REQUESTED=
FAST_REQUESTED_SET=no
NETWORK_ACCESS=
NETWORK_ACCESS_SET=no
IGNORE_USER_CONFIG=
IGNORE_USER_CONFIG_SET=no
SKIP_GIT_REPO_CHECK=
SKIP_GIT_REPO_CHECK_SET=no
RESUME_FROM=
RESUME_THREAD=
RESUMED_FROM=
RUN=
HOST_ROUTE=
HOST_MODEL=
ROUTING_REASON=
RECOVER_MANIFEST=no

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace|--sandbox|--packet|--model|--effort|--fast-requested|--network-access|--ignore-user-config|--skip-git-repo-check|--host-route|--host-model|--routing-reason|--resume-from|--run-dir)
      [ "$#" -ge 2 ] || fail "$1 requires a value"
      case "$1" in
        --workspace) WORKSPACE=$2 ;;
        --sandbox) SANDBOX=$2; SANDBOX_SET=yes ;;
        --packet) PACKET=$2 ;;
        --model) MODEL=$2; MODEL_SET=yes ;;
        --effort) EFFORT=$2; EFFORT_SET=yes ;;
        --fast-requested) FAST_REQUESTED=$2; FAST_REQUESTED_SET=yes ;;
        --network-access) NETWORK_ACCESS=$2; NETWORK_ACCESS_SET=yes ;;
        --ignore-user-config) IGNORE_USER_CONFIG=$2; IGNORE_USER_CONFIG_SET=yes ;;
        --skip-git-repo-check) SKIP_GIT_REPO_CHECK=$2; SKIP_GIT_REPO_CHECK_SET=yes ;;
        --host-route) HOST_ROUTE=$2 ;;
        --host-model) HOST_MODEL=$2 ;;
        --routing-reason) ROUTING_REASON=$2 ;;
        --resume-from) RESUME_FROM=$2 ;;
        --run-dir) RUN=$2 ;;
      esac
      shift 2
      ;;
    --recover-manifest)
      RECOVER_MANIFEST=yes
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *) fail "unknown argument: $1" ;;
  esac
done

[ -s "$PACKET" ] || fail "packet is missing or empty: $PACKET"
[ -n "$RUN" ] || fail "--run-dir is required"

case "$RUN" in /*) ;; *) fail "--run-dir must be absolute" ;; esac
for input in "$RUN" "$PACKET" "$WORKSPACE" "$RESUME_FROM"; do
  case "$input" in *[[:cntrl:]]*) fail "paths must not contain control characters" ;; esac
done
command -v openssl >/dev/null 2>&1 || fail "openssl is required for packet hashing"
if command -v node >/dev/null 2>&1; then
  RUNTIME=$(command -v node)
elif command -v bun >/dev/null 2>&1; then
  RUNTIME=$(command -v bun)
else
  fail "Node.js 18+ or Bun is required for event parsing"
fi

if [ "$RECOVER_MANIFEST" = yes ]; then
  [ -d "$RUN" ] || fail "recovery run directory does not exist: $RUN"
  RUN=$(cd "$RUN" && pwd -P) || exit 64
  [ -s "$RUN/result.txt" ] || fail "recovery run has no provenance: $RUN"
  [ -f "$RUN/prompt.md" ] || fail "recovery run has no prompt.md: $RUN"
  [ -f "$RUN/run.sh" ] || fail "recovery run has no run.sh: $RUN"
  cmp -s "$PACKET" "$RUN/prompt.md" ||
    fail "recovery packet does not match prompt.md: $RUN"
  PACKET_SHA256=$(packet_sha256 "$RUN/prompt.md") ||
    fail "could not hash recovery packet: $RUN"
  RECOVERY_PROVENANCE=$(sed -n '1p' "$RUN/result.txt")
  RECOVERY_PACKET_SHA=$(printf '%s\n' "$RECOVERY_PROVENANCE" |
    sed -n 's/.* packet_sha256=\([^ ]*\).*/\1/p')
  [ "$RECOVERY_PACKET_SHA" = "$PACKET_SHA256" ] ||
    fail "recovery provenance does not match packet hash: $RUN"
  RECOVERY_HOST_ROUTE=$(printf '%s\n' "$RECOVERY_PROVENANCE" |
    sed -n 's/.* host_route=\([^ ]*\).*/\1/p')
  case "$RECOVERY_HOST_ROUTE" in
    launcher-subagent|direct-main) ;;
    *) fail "recovery provenance has no valid host route: $RUN" ;;
  esac
  RECOVERY_HOST_MODEL=$(printf '%s\n' "$RECOVERY_PROVENANCE" |
    sed -n 's/.* host_model=\([^ ]*\).*/\1/p')
  RECOVERY_ROUTING_REASON=$(printf '%s\n' "$RECOVERY_PROVENANCE" |
    sed -n 's/.* routing_reason=\([^ ]*\).*/\1/p')
  [ -n "$RECOVERY_HOST_MODEL" ] && [ -n "$RECOVERY_ROUTING_REASON" ] ||
    fail "recovery provenance is missing host metadata: $RUN"
  emit_manifest
  exit 0
fi

[ -n "$WORKSPACE" ] || fail "--workspace is required"
[ -d "$WORKSPACE" ] || fail "workspace does not exist: $WORKSPACE"
[ -n "$HOST_ROUTE" ] || fail "--host-route is required"
[ -n "$HOST_MODEL" ] || fail "--host-model is required"
[ -n "$ROUTING_REASON" ] || fail "--routing-reason is required"

case "$HOST_ROUTE" in
  launcher-subagent|direct-main) ;;
  *) fail "--host-route must be launcher-subagent or direct-main" ;;
esac

case "$HOST_MODEL" in
  *[[:space:]]*) fail "--host-model must not contain whitespace" ;;
esac

case "$ROUTING_REASON" in
  *[[:space:]]*) fail "--routing-reason must not contain whitespace" ;;
esac

if [ -n "$RESUME_FROM" ]; then
  [ -f "$RESUME_FROM/result.txt" ] || fail "resume source has no result.txt: $RESUME_FROM"
  [ -s "$RESUME_FROM/events.jsonl" ] || fail "resume source has no events.jsonl: $RESUME_FROM"
  ORIGINAL_PROVENANCE=$(sed -n '1p' "$RESUME_FROM/result.txt")
  RESUME_THREAD=$(read_thread "$RESUME_FROM") ||
    fail "resume source has no usable thread.started event: $RESUME_FROM"
  validate_token "thread ID" "$RESUME_THREAD"
  [ -n "$RESUME_THREAD" ] || fail "resume source has no thread ID: $RESUME_FROM"
  if ! grep -Eq '^exit=[0-9]+( |$)|^cancelled=' "$RESUME_FROM/result.txt"; then
    ORIGINAL_PG=$(printf '%s\n' "$ORIGINAL_PROVENANCE" | sed -n 's/.* pgid=\([0-9]*\).*/\1/p')
    case "$ORIGINAL_PG" in ''|*[!0-9]*) fail "resume source liveness is unknown: $RESUME_FROM" ;; esac
    [ "$ORIGINAL_PG" -gt 1 ] || fail "resume source liveness is unknown: $RESUME_FROM"
    if kill -0 -"$ORIGINAL_PG" 2>/dev/null; then
      fail "resume source is still running: $RESUME_FROM"
    fi
  fi
  [ "$SANDBOX_SET" = yes ] ||
    SANDBOX=$(printf '%s\n' "$ORIGINAL_PROVENANCE" | sed -n 's/^sandbox=\([^ ]*\).*/\1/p')
  [ "$MODEL_SET" = yes ] ||
    MODEL=$(printf '%s\n' "$ORIGINAL_PROVENANCE" | sed -n 's/.* model=\([^ ]*\).*/\1/p')
  [ "$EFFORT_SET" = yes ] ||
    EFFORT=$(printf '%s\n' "$ORIGINAL_PROVENANCE" | sed -n 's/.* effort=\([^ ]*\).*/\1/p')
  if [ "$FAST_REQUESTED_SET" = no ]; then
    FAST_REQUESTED=$(printf '%s\n' "$ORIGINAL_PROVENANCE" |
      sed -n 's/.* fast_requested=\([^ ]*\).*/\1/p')
    FAST_REQUESTED=${FAST_REQUESTED:-no}
  fi
  if [ "$NETWORK_ACCESS_SET" = no ]; then
    NETWORK_ACCESS=$(printf '%s\n' "$ORIGINAL_PROVENANCE" |
      sed -n 's/.* network=\([^ ]*\).*/\1/p')
    case "${NETWORK_ACCESS:-no}" in
      yes|true|on|enabled) NETWORK_ACCESS=yes ;;
      no|false|off|disabled) NETWORK_ACCESS=no ;;
      *) fail "resume source has invalid network provenance: $NETWORK_ACCESS" ;;
    esac
  fi
  if [ "$IGNORE_USER_CONFIG_SET" = no ]; then
    IGNORE_USER_CONFIG=$(printf '%s\n' "$ORIGINAL_PROVENANCE" |
      sed -n 's/.* ignore_user_config=\([^ ]*\).*/\1/p')
    IGNORE_USER_CONFIG=${IGNORE_USER_CONFIG:-no}
  fi
  if [ "$SKIP_GIT_REPO_CHECK_SET" = no ]; then
    SKIP_GIT_REPO_CHECK=$(printf '%s\n' "$ORIGINAL_PROVENANCE" |
      sed -n 's/.* skip_git_repo_check=\([^ ]*\).*/\1/p')
    SKIP_GIT_REPO_CHECK=${SKIP_GIT_REPO_CHECK:-no}
  fi
  RESUMED_FROM=$("$RUNTIME" -e 'process.stdout.write(encodeURIComponent(process.argv[1]))' -- "$(basename "$RESUME_FROM")") || exit 64
else
  [ "$SANDBOX_SET" = yes ] || fail "--sandbox is required for a new thread"
  [ "$MODEL_SET" = yes ] || MODEL=gpt-6-astra
  [ "$EFFORT_SET" = yes ] || EFFORT=xhigh
  [ "$FAST_REQUESTED_SET" = yes ] || FAST_REQUESTED=yes
  [ "$NETWORK_ACCESS_SET" = yes ] || NETWORK_ACCESS=no
  [ "$IGNORE_USER_CONFIG_SET" = yes ] || IGNORE_USER_CONFIG=no
  [ "$SKIP_GIT_REPO_CHECK_SET" = yes ] || SKIP_GIT_REPO_CHECK=no
fi

[ -n "$SANDBOX" ] || fail "sandbox provenance is missing"
[ -n "$MODEL" ] || fail "model must not be empty"
[ -n "$EFFORT" ] || fail "effort must not be empty"
validate_token model "$MODEL"
validate_token effort "$EFFORT"
validate_token host-model "$HOST_MODEL"
validate_token routing-reason "$ROUTING_REASON"

case "$SANDBOX" in
  read-only|workspace-write|danger-full-access) ;;
  *) fail "sandbox must be read-only, workspace-write, or danger-full-access" ;;
esac

case "$FAST_REQUESTED" in
  yes) SERVICE_TIER=priority ;;
  no) SERVICE_TIER=default ;;
  *) fail "--fast-requested must be yes or no" ;;
esac

case "$NETWORK_ACCESS" in
  yes)
    [ "$SANDBOX" = workspace-write ] ||
      fail "--network-access=yes requires --sandbox=workspace-write"
    ;;
  no) ;;
  *) fail "--network-access must be yes or no" ;;
esac

case "$IGNORE_USER_CONFIG" in
  yes|no) ;;
  *) fail "--ignore-user-config must be yes or no" ;;
esac

case "$SKIP_GIT_REPO_CHECK" in
  yes|no) ;;
  *) fail "--skip-git-repo-check must be yes or no" ;;
esac

command -v codex >/dev/null 2>&1 || fail "codex CLI is required"
if ! command -v setsid >/dev/null 2>&1; then
  command -v perl >/dev/null 2>&1 || fail "setsid or Perl with POSIX is required"
  perl -MPOSIX -e 1 >/dev/null 2>&1 || fail "Perl POSIX support is unavailable"
fi
DIR=$(cd "$WORKSPACE" && pwd -P) || exit 64
RUN_PARENT=$(dirname "$RUN")
mkdir -p "$RUN_PARENT" || exit 1
RUN_PARENT=$(cd "$RUN_PARENT" && pwd -P) || exit 1
RUN="$RUN_PARENT/$(basename "$RUN")"

mkdir "$RUN" || fail "run directory already exists or cannot be created: $RUN"
cp "$PACKET" "$RUN/prompt.md" || exit 1
PACKET_SHA256=$(packet_sha256 "$RUN/prompt.md") ||
  fail "could not hash copied packet: $RUN/prompt.md"

# Persist only fixed launch parameters, never the inherited credential environment.
{
  printf '#!/bin/bash\numask 077\n'
  for key in DIR SANDBOX MODEL EFFORT FAST_REQUESTED SERVICE_TIER NETWORK_ACCESS RUN \
    IGNORE_USER_CONFIG SKIP_GIT_REPO_CHECK RESUME_THREAD RESUMED_FROM \
    HOST_ROUTE HOST_MODEL ROUTING_REASON PACKET_SHA256; do
    printf '%s=%q\n' "$key" "${!key}"
  done
} > "$RUN/run.sh" || exit 1
cat >> "$RUN/run.sh" <<'EOF'
# A copied or manually replayed wrapper must not repeat external effects.
if ! (set -o noclobber; : > "$RUN/result.txt") 2>/dev/null; then
  printf 'run already started; recover its manifest instead\n' >&2
  exit 64
fi
if [ -n "$RESUME_THREAD" ]; then
  printf 'sandbox=%s workspace=%s started=%s pgid=%s thread=%s resumed_from=%s model=%s effort=%s fast_requested=%s tier=%s network=%s ignore_user_config=%s skip_git_repo_check=%s host_route=%s host_model=%s routing_reason=%s packet_sha256=%s\n' \
    "$SANDBOX" "$DIR" "$(date -u +%FT%TZ)" "$$" "$RESUME_THREAD" \
    "$RESUMED_FROM" "$MODEL" "$EFFORT" "$FAST_REQUESTED" "$SERVICE_TIER" \
    "$NETWORK_ACCESS" "$IGNORE_USER_CONFIG" "$SKIP_GIT_REPO_CHECK" \
    "$HOST_ROUTE" "$HOST_MODEL" "$ROUTING_REASON" "$PACKET_SHA256" \
    > "$RUN/result.txt"
else
  printf 'sandbox=%s workspace=%s started=%s pgid=%s model=%s effort=%s fast_requested=%s tier=%s network=%s ignore_user_config=%s skip_git_repo_check=%s host_route=%s host_model=%s routing_reason=%s packet_sha256=%s\n' \
    "$SANDBOX" "$DIR" "$(date -u +%FT%TZ)" "$$" "$MODEL" "$EFFORT" \
    "$FAST_REQUESTED" "$SERVICE_TIER" "$NETWORK_ACCESS" \
    "$IGNORE_USER_CONFIG" "$SKIP_GIT_REPO_CHECK" "$HOST_ROUTE" \
    "$HOST_MODEL" "$ROUTING_REASON" "$PACKET_SHA256" > "$RUN/result.txt"
fi
trap ':' INT
if [ -n "$RESUME_THREAD" ]; then
  CODEX_ARGS=(exec -C "$DIR" --sandbox "$SANDBOX" resume "$RESUME_THREAD"
    --json -m "$MODEL" -c "model_reasoning_effort=$EFFORT"
    -c "service_tier=$SERVICE_TIER")
else
  CODEX_ARGS=(exec --json -C "$DIR" --sandbox "$SANDBOX" -m "$MODEL"
    -c "model_reasoning_effort=$EFFORT" -c "service_tier=$SERVICE_TIER")
fi
if [ "$SANDBOX" = workspace-write ]; then
  if [ "$NETWORK_ACCESS" = yes ]; then
    CODEX_ARGS+=(-c sandbox_workspace_write.network_access=true)
  else
    CODEX_ARGS+=(-c sandbox_workspace_write.network_access=false)
  fi
fi
if [ "$IGNORE_USER_CONFIG" = yes ]; then
  CODEX_ARGS+=(--ignore-user-config)
fi
if [ "$SKIP_GIT_REPO_CHECK" = yes ]; then
  CODEX_ARGS+=(--skip-git-repo-check)
fi
codex "${CODEX_ARGS[@]}" -o "$RUN/report.md" - < "$RUN/prompt.md" \
  > "$RUN/events.jsonl" 2> "$RUN/stderr.log"
CODEX_EXIT=$?
trap - INT
if [ "$CODEX_EXIT" -eq 0 ] && [ -s "$RUN/report.md" ]; then
  HANDOFF=ready
else
  HANDOFF=incomplete
fi
printf 'exit=%s handoff=%s finished=%s\n' \
  "$CODEX_EXIT" "$HANDOFF" "$(date -u +%FT%TZ)" >> "$RUN/result.txt"
exit "$CODEX_EXIT"
EOF
chmod +x "$RUN/run.sh"

if command -v setsid >/dev/null 2>&1; then
  setsid -f /bin/bash "$RUN/run.sh" </dev/null >>"$RUN/launcher.log" 2>&1
else
  perl -e 'exit 0 if fork; use POSIX (); POSIX::setsid() or die; exec @ARGV or die' \
    /bin/bash "$RUN/run.sh" </dev/null >>"$RUN/launcher.log" 2>&1
fi

TRIES=0
while [ ! -s "$RUN/result.txt" ]; do
  TRIES=$((TRIES + 1))
  [ "$TRIES" -lt 100 ] || fail "run launched but provenance did not appear: $RUN"
  sleep 0.05
done

if [ -n "$RESUME_THREAD" ]; then
  THREAD=$RESUME_THREAD
else
  THREAD=pending
  TRIES=0
  while [ "$THREAD" = pending ] && [ "$TRIES" -lt 100 ]; do
    if [ -s "$RUN/events.jsonl" ]; then
      THREAD=$(read_thread "$RUN") || THREAD=pending
      [ -n "$THREAD" ] || THREAD=pending
    fi
    TRIES=$((TRIES + 1))
    grep -q '^exit=' "$RUN/result.txt" 2>/dev/null && break
    [ "$THREAD" != pending ] || sleep 0.05
  done
fi

emit_manifest
