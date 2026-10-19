# Cost

Spot compute is cheap per hour; the full cost includes startup, failed restarts, lost partial episodes, idle waiting, and the damage interruptions do to a scored protocol.

## What bills when

- Running compute bills by the second or minute on most providers; stopped compute does not. Disks, reserved addresses, snapshots, object storage, and the restarter VM keep billing while the GPU node is stopped.
- Starts that never reached RUNNING have generally not been billed; confirm with the provider's usage export before relying on it.
- Some providers price spot dynamically, updating every few minutes and applying the new price to running instances. On some, a configured price cap is itself a preemption trigger; following the market price removes that trigger but not capacity reclamation.
- Record the price read at each start. When invoices are not available at hourly resolution, report spend as a range from the lowest and highest price read in each billed interval.

## Cost per completed episode

Compare placements by cost per completed, uninterrupted episode:

```text
cost per completed episode = price per hour × billed hours / episodes completed without interruption
```

Billed hours include successful startups, preempted startups, batch drain, idle time before power-off, and any billed failed starts. Under random preemption, the productive share of billed time is exp(−S/τ) for restart cost S and mean lifetime τ; `scripts/spot_math.py restart` computes it.

## Break-even with non-preemptible capacity

- Spot usually stays cheaper on compute even when it interrupts a large share of episodes. With fresh full-budget reruns of 2-hour episodes, expected active time grows 2.1x at τ = 1.5 h, 3.2x at τ = 1 h, and about 13x at τ = 30 min. Adding a 20-minute restart, a spot price at a quarter of on-demand costs about 65% of on-demand at τ = 1.5 h and breaks even near τ = 1 h.
- For scored runs the deciding cost is usually protocol damage, not dollars: interrupted and budget-shortened episodes change what the score measures. Put both numbers in the decision.

## Idle and waiting

- A GPU node waiting for a decision, a fix, or a review bills like one doing work. Stop it with holds in place and log the reason and time.
- After a run ends, the end handler powers off and places the restarter hold. Without the hold, idle power-off and automatic restart repeat until a loop guard trips, billing a boot and an idle period each time.

## API versus self-hosting per token

When a hosted API serves the same weights, compare per-token prices at the workload's real token mix before renting GPUs.

```text
API blended price per 1M = share_input × price_input + share_cached × price_cached + share_output × price_output
self-hosted price per 1M = node price per hour / (output tokens per second / share_output × 3600 × utilization) × 1e6
```

- Long agent loops resend their growing context, so most input tokens are prefix-cache hits. Agent runs showed prefix-cache hit rates above 90%, and a mix of about 10% uncached input, 85% cached input, and 5% output is a reasonable starting point; measure your own from serving metrics or provider usage.
- With that mix the cached-input price dominates. Synthetic example with a node at 20 per hour producing 1,000 output tokens per second: against an API at 1.00 input, 0.20 cached, 4.00 output per million, self-hosting costs about 0.28 against 0.47, so it wins. Against an API at 0.50, 0.01, and 2.00, the API costs about 0.16 against 0.33 for self-hosting at 85% utilization, so the API wins. A conclusion drawn against one provider's cached-input price does not transfer to another.
- Utilization is the productive share of billed node time: restarts, idle drain, and low concurrency all lower it.
- Pin the provider and its quantization when the API run must stand for the same weights; the cheapest route may serve a different quantization.

```bash
python3 -I scripts/spot_math.py tokens --price-input 1.00 --price-cached 0.20 --price-output 4.00 \
  --node-price-per-hour 20 --output-tokens-per-second 1000
```
