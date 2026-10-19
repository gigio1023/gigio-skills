#!/usr/bin/env bash
# Cold read throughput of the disk under a directory of large files, such as checkpoint shards.
#
# Usage: disk_read_throughput.sh [-s "1 8 16"] [-k 4] [-g GLOB] [-b 16M] DIR
#
#   -s  stream counts to measure, one case each; default "1 8 16"
#   -k  files read one after another in the single-stream case; default 4
#   -g  glob selecting files inside DIR; default "*.safetensors"
#   -b  dd block size; default 16M
#
# Each case reads its own files, taken in name order without reuse, so no case
# reads data an earlier case touched. Reads use O_DIRECT (dd iflag=direct), which
# bypasses the page cache, so the result is the device and its network path, not
# memory. A case with N > 1 streams reads N files concurrently, one dd each.
#
# Output: one line per case with bytes, seconds, and MiB/s. Read-only: the script
# never writes to DIR and needs no root. Exit status 0 when every case finished,
# 1 when a dd failed (an unreadable file, or a filesystem without O_DIRECT support),
# 2 on a usage error or too few files. Requires bash, GNU coreutils dd and stat,
# and Linux.
set -euo pipefail

streams="1 8 16"
single_files=4
glob="*.safetensors"
block="16M"

usage() { sed -n '4,9p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2; }

while getopts "s:k:g:b:h" opt; do
  case "$opt" in
    s) streams=$OPTARG ;;
    k) single_files=$OPTARG ;;
    g) glob=$OPTARG ;;
    b) block=$OPTARG ;;
    *) usage ;;
  esac
done
shift $((OPTIND - 1))
[ $# -eq 1 ] || usage
dir=$1
[ -d "$dir" ] || { echo "not a directory: $dir" >&2; exit 2; }
[[ "$single_files" =~ ^[1-9][0-9]*$ ]] || { echo "-k must be a positive integer" >&2; exit 2; }

mapfile -t files < <(find "$dir" -maxdepth 1 -type f -name "$glob" -print | LC_ALL=C sort)

# Files each case needs, in order: the single-stream case reads -k files, an N-stream case N files.
needed=0
for n in $streams; do
  [[ "$n" =~ ^[1-9][0-9]*$ ]] || { echo "stream counts must be positive integers: $n" >&2; exit 2; }
  if [ "$n" -eq 1 ]; then needed=$((needed + single_files)); else needed=$((needed + n)); fi
done
if [ "${#files[@]}" -lt "$needed" ]; then
  echo "need $needed files matching '$glob' in $dir for streams '$streams' and -k $single_files; found ${#files[@]}" >&2
  exit 2
fi

next=0
status=0
for n in $streams; do
  count=$n
  [ "$n" -eq 1 ] && count=$single_files
  set_files=("${files[@]:next:count}")
  next=$((next + count))
  bytes=0
  for f in "${set_files[@]}"; do bytes=$((bytes + $(stat -c %s "$f"))); done

  start=$(date +%s.%N)
  failed=0
  if [ "$n" -eq 1 ]; then
    for f in "${set_files[@]}"; do
      dd if="$f" of=/dev/null bs="$block" iflag=direct status=none || failed=1
    done
  else
    pids=()
    for f in "${set_files[@]}"; do
      dd if="$f" of=/dev/null bs="$block" iflag=direct status=none &
      pids+=($!)
    done
    for p in "${pids[@]}"; do wait "$p" || failed=1; done
  fi
  end=$(date +%s.%N)

  if [ "$failed" -ne 0 ]; then
    echo "streams=$n files=$count FAILED: dd could not read with O_DIRECT" >&2
    status=1
    continue
  fi
  awk -v n="$n" -v c="$count" -v b="$bytes" -v s="$start" -v e="$end" 'BEGIN {
    t = e - s; if (t <= 0) t = 1e-9
    printf "streams=%d files=%d bytes=%d seconds=%.1f MiB/s=%.0f\n", n, c, b, t, b / t / 1048576
  }'
done
exit "$status"
