# Monitoring

Watch spot runs closely enough to act within minutes, with traffic small enough that the monitor never becomes the problem. The monitor observes and alerts; the restarter and guest units do the recovery.

## Cadence and traffic budget

| Target | Cadence | Source | Calls per hour |
| --- | --- | --- | --- |
| Spot instance state | 1 min | Last line of the restarter's decision log over a private SSH connection | 60 short reads |
| Run progress on the spot node while RUNNING | 2 min | One SSH call that reads run state, unit states, server health, and pending uploads locally | 30 |
| Run progress on a stable host | 5 min | One SSH call | 12 |
| Provider API | One-off waits only, at most every 5 min | Provider CLI with a service-account profile | 12 or fewer |

Write the budget into the monitor's own notes, so a later change can be checked against it.

## Alert conditions

Alert on transitions and stalls, once per transition:

- The instance left RUNNING: preemption or stop. Include whether a restarter hold is present.
- The instance is RUNNING again: check that resume or dispatch happened.
- The run reached a terminal state other than success.
- The run is running but its state file has not changed for a long time, such as 45 minutes, or the finished count has not moved for longer than the longest episode, such as 90 minutes for a 2-hour cap with refill.
- The run is running but no runner process exists.
- The run is running but no publication follower is active, or pending uploads exceed a threshold.
- The end-handler timer is inactive while a run is unfinished.
- GPUs idle with no run running on a node that is billing.
- The monitor's own access failed twice in a row, such as the SSH route or a VPN that carries it.

## Implementation

- Run monitors as systemd user timers with lingering enabled through `loginctl enable-linger`, so they run without a login session. Use service-account CLI profiles; profiles that need browser login prompt and stall.
- Use `ssh -n -o BatchMode=yes -o ConnectTimeout=10` under `timeout`, one call per pass, reading everything on the remote side.
- Keep the previous value of each watched field in a state file and alert only when it changes. Write status lines and alerts to separate logs.
- Keep the evaluation, its publication, and its end handling independent of the monitor and of any workstation. Stopping the monitor must not affect the run.

```bash
state=$(ssh -n -o BatchMode=yes -o ConnectTimeout=10 restarter-host \
  'tail -1 /var/lib/restarter/decisions.jsonl | jq -r .observed_state') || { alert "restarter unreachable"; exit 0; }
prev=$(cat "$STATE_DIR/instance.state" 2>/dev/null || echo none)
echo "$state" > "$STATE_DIR/instance.state"
if [ "$state" != "$prev" ]; then
  [ "$prev" = RUNNING ] && alert "left RUNNING ($prev -> $state)"
  [ "$state" = RUNNING ] && alert "RUNNING again; check resume"
fi
```

## Waking an agent

Append alert lines to a file that the agent's watch loop follows, or post them to a chat webhook the agent reads. On waking, the agent reads the restarter's decision log, the run state, and the event log before acting, and acts only within its authority: placing a hold or applying a written stop rule, for example, while new spending stays with the user.

## Anti-patterns

- Polling the provider API every few seconds from a workstation with a browser-login profile: login prompts, wasted traffic, and a run that depends on a laptop.
- Repeating an alert every minute while a state persists.
- A monitor that also starts or stops instances, racing the restarter.
