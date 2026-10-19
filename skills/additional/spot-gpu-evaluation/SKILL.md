---
name: spot-gpu-evaluation
description: >
  Plan and operate LLM and agent evaluation runs on preemptible or spot GPU instances: spot versus on-demand placement, restart-path measurement, an external restarter with holds, guest shutdown, resume, and end handlers, continuous result publication, preemption-aware scoring, light monitoring, and cost per completed episode. Use for "run the eval on spot GPUs", "the spot node keeps getting preempted", "is spot worth it for this benchmark", "스팟 GPU로 평가 돌려줘", "선점돼도 이어서 돌게 해줘". Starts or stops billable instances only on request. NOT for training or fine-tuning (ml-experiment), campaign state across runs (evaluation-operations), what an eval measures (evaluation-design), or capacity under load (load-testing).
---

# Spot GPU Evaluation

Run LLM and agent evaluations on GPU capacity the provider can take back at any time: a model server plus many independent benchmark episodes on a spot or preemptible node. The work ends with one of two results. A placement decision states the workload's numbers and why spot, on-demand, or a non-preemptible box fits. An operated run has a measured restart path, results that reach object storage while the run is live, interruptions recorded apart from model failures, and a log of every start, stop, and preemption with its reason and price.

The method applies to any provider with interruptible capacity: Nebius preemptible VMs, AWS, GCP, and Azure spot instances, Runpod interruptible pods, and similar offers. Notice periods, restart semantics, and address behavior differ by provider and change over time; read [provider notes](references/provider-notes.md) and recheck the provider's current documentation before relying on one.

## Scope and authority

- Evaluation workloads only: serving a model and running benchmark episodes against it. Training and fine-tuning, with their checkpoints, optimizer state, and data progress, belong to `ml-experiment`. Campaign bookkeeping across many runs belongs to `evaluation-operations`; this skill supplies the node-level operation those runs depend on.
- Creating, starting, and stopping instances, disks, buckets, and addresses spends money, and deleting a disk is irreversible. Act within the user's grant: budget, hourly price cap, regions, instance types, and stop rules. A status question does not authorize a start. When a price cap exists, read the current spot price before each start.
- Keep GPUs stopped whenever they are not serving or running evaluations, including while waiting for a decision, a code change, or a review. Place the holds described below before stopping.
- Record instance IDs, addresses, bucket names, account names, and prices in the project's private run record. Shared reports carry the method and the measurements without them.

## Decide placement before building recovery

Recovery machinery keeps completed work. Whether a workload fits spot depends on three numbers: the episode length D, the mean lifetime τ of an allocation from start to preemption on the actual pool, and the restart cost S from preemption until the server serves again.

- With preemptions arriving at random, an episode of length D is interrupted at least once with probability 1 − exp(−D/τ). At τ = 2 h, a 2-hour episode is interrupted 63% of the time and a 30-minute episode 22%.
- One preemption interrupts every in-flight episode at once: a node running 16 episodes loses up to 16 partial episodes per event.
- Restart cost for a large model is usually 10 to 25 minutes: capacity retries, boot, weight loading, and JIT warmup. Startup alone adds S/P to each allocation's productive time P, so a 20-minute restart on 60 minutes of useful uptime adds 33%.
- Stopping and restarting on purpose leaves preemption risk unchanged under random preemption, because surviving so far changes nothing. When preemptions cluster soon after start, each deliberate restart passes through the riskiest window again and pays another cold start.
- Preemptions can cluster: a pool can preempt several times per hour of uptime, sometimes within a minute of boot and before the server is ever healthy. Measure τ on the actual pool and instance size. Count operator stops as censored observations and capacity waits separately.

| Situation | Placement |
| --- | --- |
| Scored runs, episodes of an hour or more, τ unknown or a few hours | On-demand, reserved, or an owned non-preemptible box |
| Pilots, smoke runs, harness debugging, minute-scale episodes | Spot with automatic restart, results labeled exploratory |
| Measured τ shorter than S plus D | Long-episode benchmarks are infeasible on spot; move them |
| Deadline-sensitive tail of a campaign | Non-preemptible fallback |
| Benchmark needs nested virtualization, its own Docker daemon, or root | Probe the node first; container pods often forbid a Docker daemon and GPU VMs often lack `/dev/kvm` |
| A hosted API serves the same weights | Compare blended per-token prices first; agent token mixes are cache-heavy |

Read [placement](references/placement.md) for the formulas, retry-budget policies, hybrid placement, and running CPU-only benchmark infrastructure apart from the GPU node. `scripts/spot_math.py` computes the interruption, restart-overhead, and per-token comparisons.

## Qualify the node before the real run

Run these on the first node and record the results before dispatching a scored run:

1. **Platform features.** Check what the benchmark needs: `/dev/kvm` and `vmx` or `svm` CPU flags for VM-based targets, a Docker daemon the harness controls, systemd, and root. Probe on the node; provider documentation often omits these.
2. **Disk throughput.** Measure cold reads of the checkpoint with `scripts/disk_read_throughput.sh`, single and parallel streams. Documented figures for network disks can be off by more than 2x.
3. **Startup breakdown.** Time a cold start and a warm start stage by stage, as in [restart path](references/restart-path.md).
4. **Forced stop with a live run.** Stop the instance mid-episode without a hold. Check that the shutdown hook ran within the notice window, partial episodes were salvaged and marked, the restarter started the instance, the run resumed, and records written late reached object storage after reboot. Then stop again during boot resume.
5. **Records round trip.** Pull the run from object storage into an empty directory and confirm every episode can be reconstructed from what was published. A readiness verdict on the evaluation itself belongs to `evaluation-audit`.

Write stop rules into the run record before starting, for example: hold and report after 45 minutes of failed starts, after two preemptions before the server becomes healthy, or after three preemptions before 20 episodes finish.

## Shorten the restart path where it can be shortened

Measure every restart as stages, because each stage has a different owner:

| Stage | Typical | Shorten with |
| --- | --- | --- |
| Notice to instance stopped | 1 to 3 min | Nothing; provider-controlled |
| Stopped to start call | Restarter grace plus one poll | A 60 s grace once holds are reliable |
| Start call to running | 2 to 5 min; each capacity failure adds about 5 min | Only a wider pool or non-preemptible capacity |
| Running to serving start | 2 to 3 min | Serving auto-start on boot |
| Serving start to healthy | Weight read, JIT warmup, graph capture | Faster disk, persistent compile cache, memory for prefetch |
| Healthy to episodes running | Preflight and resume | A boot resume unit |

Weight reading dominates a cold start: about 700 GB at about 2 GB/s takes about 6 minutes, and at 0.45 GB/s about 26 minutes. Within one boot the page cache holds the checkpoint, so restarting only the container reloads in a couple of minutes; every preemption is a reboot and starts cold. Read [cold start](references/cold-start.md) for disk choice and measurement, RAID0, compile caches, safetensors prefetch under container memory limits, durable checkpoint disks, and serving auto-start.

## Control the lifecycle from outside and inside

Spot instances do not restart themselves on most providers. Use two cooperating parts, with holds that make every automatic action stoppable:

- **External restarter** on a small non-preemptible VM that stays reachable while the GPU node is down. It polls instance state every 60 s, waits a grace period after STOPPED, starts the instance, and writes one decision line per poll. It classifies each stop: a start that never reached RUNNING is a capacity failure and only advances backoff, capped near the length of one failed start; a run that reached RUNNING and stopped soon after counts toward a loop guard. Judge a start by observing RUNNING, because start commands can return an error while the operation continues.
- **Guest units** on the GPU node: a shutdown hook that stops the run through its own stop path inside the notice window, a boot resume unit, a publication follower, an idle guard, and an end handler that publishes, places holds, and powers off when the run completes or a deadline passes.
- **Holds.** A restarter hold per instance stops automatic starts; a guest hold on the durable disk makes boot resume refuse; a keep-alive file stops the idle guard; a kill switch disables the end handler. To stop on purpose, place the restarter hold, read it back, place the guest hold when the run should not resume, then stop. Let one actor start an instance at a time: hold the restarter while running a manual retry loop.

Read [lifecycle control](references/lifecycle-control.md) for restarter settings and guard pitfalls, the hold table, systemd unit patterns, the end-handler sequence, and dry-run tests.

## Keep results durable and interruptions visible

- Keep the run directory on a persistent disk separate from the boot disk, verified by filesystem UUID and a sentinel file before writes. Local NVMe usually loses its contents on stop and start.
- Publish each finished episode and the run state to object storage on a short interval, such as 60 s, with a bounded final pass at shutdown; the next boot uploads what the final pass missed. Verify by pulling into an empty directory.
- On interruption, stop the agent processes before copying their logs, write an interruption marker, and settle each interrupted episode by a declared policy: rerun from scratch with the remaining budget, or with a fresh full budget. Disclose which.
- Score preemption-interrupted and budget-shortened episodes as their own classes, apart from model failures and harness errors. Compute throughput only from windows that ended naturally; a window ended by a stop finished only its short episodes.
- Keep a timestamped log of every start, stop, capacity failure, and preemption with its source, reason, and the price read at start.

Read [run durability](references/run-durability.md) for durable volumes, publication pitfalls with S3-compatible stores, salvage, budget settlement, scoring classes, and the event log.

## Monitor without hammering

Check spot instance state every minute and stable hosts every 5 minutes. Take state from the restarter's own decision log instead of calling the provider API again, read run progress with one SSH call per pass, and alert only on transitions and stalls. Run monitors as timers that need no interactive login, and keep the evaluation and its end handling independent of any workstation. Read [monitoring](references/monitoring.md) for alert conditions, cadence, and waking an agent.

## Networking and credentials

Bind model servers to loopback with an API key and reach them through SSH tunnels or same-host relays; keep them off public addresses. Dynamic public addresses change after long stops. Give the restarter a service account that can only view, start, and stop the listed instances, and give the publisher write access to one bucket without delete. Some reads, such as operation details, serial console logs, and capacity advice, need permissions a least-privilege account lacks; plan to judge start results from instance state alone. Read [access and credentials](references/access-and-credentials.md).

## Cost

Compute bills while the instance runs; disks, reserved addresses, and the restarter bill while it is stopped. Dynamic spot prices can change during a run, so record the price at each start and report spend as a range. Compare options by cost per completed, uninterrupted episode, including startup, failed restarts, and lost partial episodes. Before self-hosting a model that a hosted API also serves, compare blended per-token prices with the workload's real share of cached input. Read [cost](references/cost.md).

## Checklist

Before the first scored run:

- [ ] Placement decision with D, τ, S, and the retry-budget policy written down
- [ ] Platform features probed on the node
- [ ] Disk throughput measured; checkpoint on a durable disk and hash-verified
- [ ] Cold and warm startup breakdown recorded
- [ ] Restarter on a reachable non-preemptible host with a least-privilege account; holds tested
- [ ] Shutdown hook, boot resume, publication follower, idle guard, and end handler installed and dry-run tested
- [ ] Forced stop with a live run passed; run pulled from object storage and reconstructed
- [ ] Stop rules, price cap, and deadline written in the run record
- [ ] Monitor running with transition alerts and no workstation dependency
- [ ] Event log started

At the end: the end handler published with nothing pending, both holds are placed, the instance is STOPPED, spend is recorded, and unfinished episodes are listed.

## Resources

| Read | When |
| --- | --- |
| [placement](references/placement.md) | Choosing spot, on-demand, hybrid, or a split topology |
| [restart path](references/restart-path.md) | Measuring a restart stage by stage and recording preemption events |
| [cold start](references/cold-start.md) | Making the server healthy sooner after boot |
| [lifecycle control](references/lifecycle-control.md) | Building or fixing the restarter, holds, and guest units |
| [run durability](references/run-durability.md) | Publication, salvage, budget settlement, and scoring |
| [monitoring](references/monitoring.md) | Low-traffic monitoring and alerts |
| [access and credentials](references/access-and-credentials.md) | Tunnels, addresses, and service accounts |
| [cost](references/cost.md) | Spend accounting and API versus self-hosting |
| [provider notes](references/provider-notes.md) | Provider-specific notice, restart, and address behavior |
| [sources](references/sources.md) | Maintaining this package |

Both scripts read inputs and print results without touching cloud resources. `scripts/spot_math.py` needs Python 3.10 or newer and only the standard library; run it as `python3 -I scripts/spot_math.py episode|restart|tokens ...`, with `--json` before the subcommand for machine output. `scripts/disk_read_throughput.sh` needs bash, GNU coreutils, and Linux, and reads with O_DIRECT so the page cache does not inflate the result.
