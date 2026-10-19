# Restart Path Anatomy

Measure each restart as a chain of stages with their own start and end events. The breakdown shows which stage to work on and which only a different placement can change.

## Stages and where to read them

| Stage | From | To | Where to read it | Typical | Shortenable |
| --- | --- | --- | --- | --- | --- |
| Notice | Provider decision | Guest shutdown begins | Previous boot's journal, `journalctl -b -1`; serial console when no journal persisted | Seconds | No |
| Stop | Guest shutdown begins | Instance STOPPED | Provider operation records or state polling | 1 to 3 min | No |
| Grace | STOPPED observed | Start call | Restarter decision log | Grace plus up to one poll | Yes, grace down to about 60 s |
| Start | Start call | RUNNING | Operation records or state polling | 2 to 5 min; a failed start returns to STOPPED after about 5 min | Only with a wider pool |
| Boot | RUNNING | Boot complete, SSH up | `who -b`, `systemd-analyze` | 1 to 3 min | Little |
| Serving start | Boot complete | Serving container started | Container `StartedAt` | Operator latency, or seconds with auto-start | Yes |
| Load | Serving container started | Health endpoint OK | Serving log lines and the health endpoint | Weight read plus JIT warmup and graph capture | Yes, see [cold start](cold-start.md) |
| Resume | Healthy | Episodes running again | Preflight and resume records | Seconds to minutes | Yes, boot resume unit |

For a vLLM server, the log lines worth timing are engine start, the prefetch start and finish, the weight loading time, any compile or JIT warmup and autotune lines, CUDA graph capture, KV cache size, and application startup complete. Grep only these infrastructure lines; request content stays out of operations records.

## Per-event record

Keep one row per preemption or failed start in the run record. Times carry a zone.

| Field | Content |
| --- | --- |
| Event | Preemption, operator stop, start failure, or update-triggered start |
| Uptime before | Since the last boot or RUNNING |
| Notice seen | Power-key or shutdown line in the guest, or none |
| Run state | Not dispatched, running, or between runs |
| Hook result | Ran or not, marker written, salvage outcome |
| STOPPED at | From operations or polling |
| Start calls | Each call time, who made it, outcome |
| RUNNING at | First RUNNING read |
| Serving start, healthy | Container start and health OK |
| Episodes interrupted | Count, and how each was settled |
| Sources | Operation identifiers, journal excerpt path, decision-log lines |

Then sum the stages: preemption to STOPPED, STOPPED to start call, start call to RUNNING with failed attempts, RUNNING to serving start, serving start to healthy. The sum is S for [placement](placement.md).

## What the stages look like

- **Notice delivery.** On some providers the preemption reaches the guest as an ACPI power-button press, so `systemd-logind` starts a poweroff and units run their stop actions. The documentation may describe a SIGTERM; your process receives whatever systemd sends during shutdown. Build the shutdown hook as a systemd stop action, as in [lifecycle control](lifecycle-control.md).
- **Preemption during boot.** A preemption can arrive before userspace exists: no hook runs and no journal persists, and the serial console shows the boot cut off. Recovery has to rely on state that was already durable.
- **Attribution.** Provider operation records may omit who stopped an instance, even for operator stops. Treat a missing creator as non-diagnostic and keep your own operator log.
- **Capacity failures.** A start can sit in STARTING for about 5 minutes and fall back to STOPPED without reaching RUNNING. Several consecutive failures before a success are normal at busy times, and a capacity advisor reporting medium availability does not guarantee a start.
- **Fast repeat preemptions.** A pool can preempt again within a minute of boot. When two preemptions in a row arrive before the server is healthy, apply the stop rule instead of retrying indefinitely.
- **Weight load.** Expect checkpoint bytes divided by the measured disk rate, plus loader overhead. A load that takes about twice that long points to page-cache eviction under a container memory limit.
- **JIT and autotune.** The first start on a new engine version or GPU type compiles kernels for several minutes; with a persistent cache, later starts spend under a minute there.
- **End to end.** For a checkpoint around 700 GB, preemption to healthy took 10 to 25 minutes when one start succeeded; each failed start adds about 5 minutes.

## What cannot be shortened

The provider's stop, the wait for capacity, and firmware and kernel boot belong to the provider. The options are a wider pool, such as other regions, instance types, or providers with weights and images already staged there, or non-preemptible capacity.

## Diagnosing a restart that did not happen

1. Read the restarter's decision log: hold present, loop guard set, backoff pending, or attempts exhausted.
2. Read the instance's state history and operation records; these may need a permission the restarter's account lacks.
3. Check whether a manual retry loop and the restarter both called start.

A restarter reachable only through the GPU node cannot be inspected while that node is down. Fix the topology before the next run rather than diagnosing blind.
