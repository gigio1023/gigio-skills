# Placement: Spot, On-Demand, or a Non-Preemptible Box

Choose where an evaluation runs from measured workload numbers, then build recovery for the placement chosen. Every probability below assumes preemptions arrive at random while the node runs; `scripts/spot_math.py` reproduces the numbers for other inputs.

## Contents

- Inputs to measure
- Interruption arithmetic
- Retry-budget policy for interrupted episodes
- Restart overhead per allocation
- Batching and deliberate restarts
- Decision table
- Hybrid placement
- Benchmark infrastructure without GPUs
- Worked example

## Inputs to measure

| Input | How to get it |
| --- | --- |
| Episode length D | Median and the share that runs to the wall limit; agent benchmarks often have a large share at the cap |
| Allocation lifetime τ | Start or RUNNING to preemption on the same pool, instance size, and region; operator stops are censored observations |
| Restart cost S | Preemption to serving healthy, split into stages as in [restart path](restart-path.md) |
| Capacity wait W | Time spent in failed start attempts, kept apart from lifetimes |
| Concurrency C | Episodes in flight on one node |
| Prices | Spot and non-preemptible price per node-hour at decision time; dynamic spot prices move |

Public lifetime data for large multi-GPU spot nodes is scarce, and providers rarely publish interruption rates. Single-GPU anecdotes and another provider's advisor buckets are reference points, not substitutes for τ on the pool you will use. A short pilot on the actual pool, with every start, stop, and preemption logged, is the cheapest measurement.

## Interruption arithmetic

An episode needing D hours survives an allocation with mean lifetime τ with probability exp(−D/τ).

| τ | D = 15 min | 30 min | 1 h | 2 h |
| --- | --- | --- | --- | --- |
| 1 h | 22% | 39% | 63% | 86% |
| 2 h | 12% | 22% | 39% | 63% |
| 4 h | 6% | 12% | 22% | 39% |
| 8 h | 3% | 6% | 12% | 22% |

- A preemption interrupts all C in-flight episodes at once. With continuous refill, the partial work lost per preemption is about C times the mean elapsed time of in-flight episodes.
- When preemptions concentrate soon after start, episodes that start after the risky window face less risk than the table says, while restarts fail more often than it implies. Every restart re-enters that window.
- A planning allowance such as "add 15% for preemptions" is an assumption until measured. Startup alone can consume it when allocations are short.

## Retry-budget policy for interrupted episodes

Decide before the run how an interrupted episode continues. The choice changes cost, schedule, and what the score means; disclose it with the results.

- **Fresh full budget.** Rerun from scratch with the whole wall limit. Exposure matches an uninterrupted run. Expected active time to finish an episode needing D is τ(exp(D/τ) − 1): 1.72 D when D = τ, 3.19 D when D = 2τ, and it grows without bound as D outgrows τ.
- **Remaining budget.** Rerun from scratch with what is left of the wall limit. Total active time stays within the limit, so the campaign finishes on schedule, but the final attempt has less time than an uninterrupted one. An episode that would have used the whole limit can "finish" having lost most of its exposure. Scores bias low. Mark these episodes budget-shortened and report how many.
- **Resume in-episode state.** Only when the harness checkpoints the conversation, sandbox, and budget state. Most agent harnesses resume completed episodes only.
- **Charge the full budget and close unjudged.** Some harnesses default to this when consumption evidence is missing after a hard stop. Check the default and set the policy explicitly.

Keep the interrupted attempt's records whatever the policy.

## Restart overhead per allocation

- Startup share without preemption is S/P for productive time P per allocation:

| Productive time per start | S = 15 min | S = 20 min |
| --- | --- | --- |
| 30 min | 50% | 67% |
| 60 min | 25% | 33% |
| 120 min | 12.5% | 17% |
| 240 min | 6% | 8% |

- With random preemption, the chance that an allocation reaches a healthy server is exp(−S/τ), and the productive share of billed time is the same expression: expected billed time per allocation is τ and expected productive time is τ·exp(−S/τ). At S = 20 min this is 51% for τ = 30 min, 72% for τ = 1 h, and 85% for τ = 2 h.
- Capacity failures add wall time and are usually unbilled; confirm on the provider's usage export.
- A restart that reaches RUNNING is not the outcome to count. Count allocations that reached a healthy server and episodes completed.

## Batching and deliberate restarts

- Refill slots continuously: start the next episode as soon as one finishes. Waiting for a fixed batch to drain before starting the next leaves slots idle behind the longest member; when a few episodes in each batch run to a 2-hour cap, batching can roughly halve throughput.
- Deliberate stop and restart to reset preemption risk has no benefit under random preemption: P(L > a + t | L > a) = P(L > t). When risk is front-loaded, it repeats the riskiest window and pays another cold start. Use planned stops only to end a work window after completed work, and stop admitting new episodes early enough to drain.

## Decision table

| Condition | Choose | Reason |
| --- | --- | --- |
| Scored runs or comparisons that feed a score, D of an hour or more | Non-preemptible capacity | Interrupted episodes change the protocol |
| Pilots, smoke runs, harness debugging, exploratory sweeps | Spot with automatic restart | Interruptions are acceptable when labeled |
| τ below S + D | Move long episodes off spot | Few episodes complete uninterrupted |
| τ unknown | A logged pilot on the actual pool first | Anecdotes from other sizes and providers do not transfer |
| Short episodes, cheap spot, budget headroom | Spot | Interruption share is small |
| Campaign deadline | Non-preemptible tail | Capacity waits are unbounded on spot |
| Nested virtualization, own Docker daemon, or root required | A node type that exposes them, probed | Many GPU VMs mask VMX; container pods forbid a Docker daemon |
| A hosted API serves the same weights | Per-token comparison in [cost](cost.md) | Self-hosting may cost more for cache-heavy agents |

On-demand starts also fail when capacity is short; once running, an on-demand instance is not preempted, though maintenance and hardware failures remain. Reserved capacity usually needs a sales contact and lead time.

## Hybrid placement

Assign runs to placements by intended use before execution. Scored runs, and every comparison that contributes to a score, go to non-preemptible capacity. Pilots, harness debugging, and exploratory sweeps go to spot. Keep their outputs apart so an interrupted exploratory run never enters a scored table. With two nodes available, both proceed in parallel.

## Benchmark infrastructure without GPUs

Sandboxes, verifiers, and VM-based targets need CPU, memory, disk, and often nested virtualization, but no GPU. GPU VMs frequently hide VMX, while bare-metal CPU hosts expose it. A split topology serves the model on the GPU node and runs the controller, sandboxes, and verifier on a CPU or bare-metal host, with model requests over an SSH tunnel.

- WAN latency adds 100 to 200 ms per model request; at about 100 requests per episode that is 10 to 20 seconds per episode.
- Decide endpoint-loss behavior before relying on it. If the tunnel drops, does the harness wait, retry, or cancel the episode, and does waiting count against the episode budget? If it cancels on endpoint loss, or refuses a restarted server as a different identity, the GPU side must be non-preemptible.
- The CPU side can run on cheap on-demand or owned hosts while the GPU side is spot, non-preemptible, or a hosted API.

## Worked example

Synthetic campaign: 2,000 agent episodes, 2-hour wall limit, 70% of episodes need about 30 minutes and 30% run to the cap, 16 concurrent, cold restart 20 minutes, measured τ = 2 h on spot.

- A capped episode is interrupted with probability 63%, a 30-minute episode 22%; about 34% of all episodes are touched at least once.
- Productive share of billed time is 85%.
- With fresh full-budget reruns, a capped episode needs 3.44 active hours on average instead of 2.
- With remaining-budget reruns, the schedule holds but about a third of episodes carry an interruption and many capped ones end budget-shortened.
- Decision: scored runs on non-preemptible capacity; pilots and harness debugging on spot, labeled exploratory.

```bash
python3 -I scripts/spot_math.py episode --duration-min 30 120 --weights 0.7 0.3 --lifetime-h 2
python3 -I scripts/spot_math.py restart --startup-min 20 --lifetime-h 2 --wait-min 10 --productive-min 60
```
