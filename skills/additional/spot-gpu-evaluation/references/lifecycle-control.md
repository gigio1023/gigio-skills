# Lifecycle Control: Restarter, Holds, and Guest Units

An external restarter brings a stopped spot instance back; units inside the guest stop, resume, publish, and finally power off the run. Holds make each automatic action stoppable by an operator or by the end handler.

## Contents

- Components
- External restarter
- Holds and markers
- Stop and start procedures
- Shutdown hook
- Boot resume
- Publication follower
- Idle guard
- End handler and boot guard
- Testing the units

## Components

```text
reachable non-preemptible host          spot GPU node
+---------------------------+          +-------------------------------------+
| restarter, polls every 60s|--start-->| boot guard -> boot resume           |
|   holds/<instance-id>     |<--hold---| end handler, timer every 5 min      |
|   decisions.jsonl         |          | shutdown hook, runs at poweroff     |
| monitor reads that log    |          | publication follower -> object store|
+---------------------------+          | idle guard                          |
                                       | durable disk: run dir, guest hold,  |
                                       |   keep-alive, kill switch, markers  |
                                       +-------------------------------------+
```

## External restarter

Run it on a small regular VM with automatic recovery, reachable without the GPU node: its own address, or a private network the operator and monitor can reach. When the only route to the restarter passes through the GPU node, its log and holds are out of reach whenever that node is down; stopping the restarter VM becomes the only way to stop restarts, and its next boot starts the GPU node again after the grace period.

| Setting | Starting point | Note |
| --- | --- | --- |
| Poll interval | 60 s | One state read per instance per poll |
| Grace after STOPPED | 60 to 300 s | Shorter restarts faster; longer gives an operator time to place a hold after an unplanned stop |
| Backoff after a start that never reached RUNNING | 120 s, doubling, capped near 360 s | One failed start already takes about 5 min on some providers |
| Attempts per stop | High, bounded by the run deadline | Capacity failures are usually unbilled |
| Starts per window | Count only starts that reached RUNNING, for example 12 per 24 h | Bounds billed restarts |
| Short-run threshold | Above boot plus time to healthy plus the idle-guard delay, for example 2 h | |
| Loop guard | For example 3 short runs | Stops a start, idle power-off, start loop |

Behavior that matters:

- **Classify every STOPPED observation** by what happened since the previous one. A start call with no RUNNING read since is a capacity failure: it advances backoff and nothing else. RUNNING followed by a stop within the short-run threshold of the start is a short run and counts toward the loop guard. Anything else is a long run and resets the count.
- **Pitfall seen in practice.** A restarter that counted every return to STOPPED after a start call as a short run latched its loop guard after two failed capacity starts. The guard persisted across the restarter's own reboot until a manual reset, and the next real preemption went unrestarted for about an hour.
- **Judge a start by observing RUNNING.** Start commands can exit with an error within seconds while the provider's operation continues, and a failed operation can surface only as STARTING falling back to STOPPED.
- **Write one decision line per poll** as JSON: time, observed state, decision, reason, start outcome, and stop classification. Monitors read this log instead of calling the provider again.
- **Alert** when a guard sets or attempts run out, through a webhook or a file a watcher reads.
- **The restarter cannot know the run finished.** The guest's end handler places the restarter hold before powering off. Without that, idle power-off and restart repeat until the loop guard trips, and each cycle bills a boot and an idle period.
- **Least privilege.** Its account views, starts, and stops only the listed instances; check that a read of any other instance and a project listing are denied.

## Holds and markers

Each marker is a small file holding a reason line and the time it was placed.

| Marker | Lives on | Read by | Effect | Placed by | Removed by |
| --- | --- | --- | --- | --- | --- |
| Restarter hold, `holds/<instance-id>` | Restarter host | Restarter | No automatic starts | Operator before a planned stop; end handler before power-off | Operator when automatic restarts are wanted |
| Guest hold | Durable disk | Boot resume, boot guard | Boot resume refuses | Operator; boot guard after an end or deadline | Operator just before dispatch |
| Keep-alive | Durable disk | Idle guard | No idle power-off | Operator during setup; end handler while waiting for a follow-up run | Operator after dispatch |
| Kill switch | Durable disk | End handler | Handler takes no action | Operator before reusing the node | Operator when the handler should act again |
| Serve-on-boot marker | Durable disk | Serving auto-start unit | Server starts at boot | Operator | Operator before other uses of the node |

## Stop and start procedures

- **Planned stop.** Place the restarter hold and read it back. Place the guest hold if the run must not resume. Stop the run through its stop command if it is running and wait for it to settle. Stop the instance, confirm STOPPED, and log time, reason, and price.
- **Planned start.** Read the spot price against the cap. Start the instance with exactly one actor. When RUNNING, check durable mounts and markers. Remove the restarter hold if automatic restarts are wanted. Remove the guest hold just before dispatch.
- **Manual retry loop.** Place the restarter hold first, or the loop and the restarter race each other. Space attempts about 5 to 6 minutes apart, roughly the length of one failed start.
- **With a short grace,** a stop without a hold is restarted within about a minute. Hold first, then stop.

## Shutdown hook

- The notice usually arrives as an ACPI power-button press, so `systemd-logind` starts a poweroff and systemd runs units' stop actions in reverse start order. A oneshot service with `RemainAfterExit=yes` does its work in `ExecStop=`. Order it after Docker, containerd, and any sandbox gateway so its stop action runs while they are still up.
- Budget: notice periods run from a few seconds to two minutes depending on provider and are best effort. Give the hook about 45 to 50 seconds through `TimeoutStopSec` on a provider with a 60-second notice. Closing 16 agent sandboxes gracefully took about 16 seconds in one harness.
- Stop the run through its own stop command, so workers write final consumption receipts and salvage partial episodes. Processes started with `docker compose exec` are killed without running their handlers when the container's init exits, so signal forwarding through the container is not enough.
- Write a shutdown marker with the cause and the monotonic clock reading of this boot, so consumption can be estimated later without trusting wall-clock jumps.
- When no run is active, exit at once.

```ini
# /etc/systemd/system/eval-shutdown-hook.service
[Unit]
Description=Stop the active evaluation run before the instance powers off
After=network-online.target docker.service containerd.service
Wants=network-online.target
RequiresMountsFor=/srv/durable

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/true
ExecStop=/srv/durable/bin/stop-active-run --budget-seconds 45
TimeoutStopSec=50

[Install]
WantedBy=multi-user.target
```

## Boot resume

- Order it `After=network-online.target docker.service` with `RequiresMountsFor=` the durable mount, and after the boot guard.
- Verify the durable volume before writing: mount source, filesystem UUID, and a sentinel file bound to the volume. An empty directory on the boot disk must never stand in for a missing mount.
- When the guest hold is present, refuse and record the refusal. Otherwise start services in order, run preflight, and resume the recorded run with its recorded identity.
- Record each boot's resume decision, so a later reader can tell "nothing to resume" from "refused".

## Publication follower

- Start it at first dispatch as well as after boot resume. A follower that waits only for a boot-resume record never starts on a fresh dispatch; test both paths.
- Unit properties for a transient follower that still runs its final pass at shutdown:

```bash
sudo systemd-run --unit eval-publish-RUN --uid eval --gid eval \
  -p DefaultDependencies=no -p After=network-online.target -p Wants=network-online.target \
  -p Conflicts=shutdown.target -p Before=shutdown.target \
  -p RequiresMountsFor=/srv/durable -p TimeoutStopSec=55 \
  /srv/durable/bin/publish-run --run /srv/durable/runs/RUN --follow --interval 60 --final-pass-timeout 45
```

- A follower that exits when the run is final must be restarted after a later operator resume in the same boot.

## Idle guard

- Power off after a fixed idle period, such as 30 minutes with no running run, unless the keep-alive file exists. Arm it from first boot.
- Share an admission lock with dispatch so the guard cannot power off a node in the middle of dispatching a run.
- Re-read its configuration on every check, so repointing it at a new run needs no restart.

## End handler and boot guard

- **Schedule.** A timer with `OnBootSec=3min` and `OnUnitActiveSec=5min` runs a oneshot service with an upper time bound. It reads local state only until an end condition holds.
- **End conditions.** The run reaches a terminal state, such as completed, completed with errors, or failed, or a deadline passes.
- **Sequence.** Stop the run gracefully if it is still running and wait for it to leave running. Wait a bounded number of ticks for publication followers to finish their final pass. Run one publication pass that must exit 0 with nothing pending, retried at the next tick a few times. Place the guest hold. Place the restarter hold over a restricted channel and read it back. Power off only after the read-back succeeds.
- **Boot guard.** Before boot resume on every boot, place the guest hold if the end sequence has started or the deadline has passed, so a restart after the end does not resume the run.
- **Follow-up runs.** To chain runs on one node, publish the first run, keep the node up with a keep-alive, and wait for the listed follow-up runs; end after they finish, after an idle limit, or at the deadline. The boot guard must then leave resume of the follow-up run possible.
- **Kill switch and persisted state.** The handler's state survives reboots, so the next boot after an end powers the node off again. Before reusing the node for other work, place the kill switch and a keep-alive immediately after boot.
- **Restricted channel to the restarter.** Give the guest a dedicated SSH key that the restarter host accepts only with a forced command, and pin the restarter's host key:

```text
restrict,command="/usr/local/bin/restarter-hold",from="GUEST_PRIVATE_IP" ssh-ed25519 AAAA... end-handler
```

The forced command accepts only `place REASON` and `check` for this instance's hold, plus the same verbs on a test hold that the restarter ignores, and refuses everything else.

## Testing the units

- Give the end handler a `--dry-run` mode with fake run states and a `--now` time, and refuse `--now` without `--dry-run`. Cover: running before the deadline, completed, deadline with the run still running, follow-up waiting, idle limit, first tick of a new boot, and each boot-guard case. Place and remove the test hold on the restarter through the real channel.
- Run the shutdown hook and boot resume through a real poweroff in a disposable VM or a systemd container before trusting them on a paid node, then once more in the forced-stop qualification.
- Keep scripts, state, and test paths on the durable disk; `/tmp` is cleared at reboot.
- `systemd-analyze verify` each unit after editing it.
