# Run Durability and Scoring

Completed work must survive any preemption, and every interruption must stay visible in the results. Recovery restores the run; scoring keeps interrupted episodes from being read as model behavior.

## Contents

- Durable run directory
- Continuous publication
- Interruption handling in the guest
- Budget settlement
- Scoring classes
- Changing conditions mid-campaign
- Event log and serving identity

## Durable run directory

- Put the run directory on a persistent disk separate from the boot disk, mounted by a stable device ID with `nofail` in fstab. The boot disk usually survives a stop too, but a separate disk also survives instance replacement and keeps results apart from rebuildable caches.
- Before every write phase, verify the mount source, filesystem type, filesystem UUID, and a sentinel file bound to the volume. Refuse when the path is a plain directory on the boot disk, which is what a missing mount looks like. Re-check during the run and stop it if the volume disappears.
- Declare everything outside the run directory that the run reads, such as checkpoints, datasets, and images, as rebuildable cache.
- Keep the run directory off object-storage mounts: their locking and rename semantics differ from a local filesystem.

## Continuous publication

- Publish each finished episode and the run-level state to object storage on a short interval, such as 60 seconds. Passes are idempotent: a second pass over unchanged files uploads nothing.
- **Integrity.** Store your own SHA-256 in object metadata; S3 ETags are not content hashes for multipart uploads. Some clients return user-metadata keys with different capitalization, for example `Sha256` for `sha256`, so compare keys case-insensitively. A case-sensitive lookup made every pass re-upload everything and every pull reject every object.
- **Concurrency.** A pass that uploads one file at a time cannot drain hundreds of files per episode for 16 interrupted episodes inside a shutdown window. Upload concurrently.
- **Empty files.** One S3-compatible endpoint left the connection waiting for the 60-second read timeout after an empty PUT sent with `Expect: 100-continue`, so every empty file cost a minute. Test empty and tiny files against the actual endpoint.
- **Exclusions.** Exclude credential-shaped files and regenerable bulk, then check that nothing excluded is the only record of something, such as the raw body of a request in flight at the stop.
- **Credentials.** Give the publisher upload and read access to one bucket without delete, so published records are append-only.
- **Shutdown.** Bound the final pass, for example to 45 seconds, inside the unit's stop timeout. What it misses goes up from the next boot.
- **Verification.** Pull the run into an empty directory, rebuild every episode's sequence of model context and actions, and count gaps. A strict reconstruction check is what catches missing logs of interrupted episodes.

## Interruption handling in the guest

1. Stop admitting new episodes.
2. Stop the run through its own stop command.
3. For each in-flight episode, stop the agent's process group: SIGTERM, then SIGKILL after a few seconds. A cancelled `docker exec` or sandbox exec does not end the process inside, and copying a log the agent is still writing yields a truncated copy.
4. Copy the agent's session and event logs out of the sandbox.
5. Write a salvage receipt per episode: files recovered, errors, elapsed time, and whether the agent was stopped.
6. Mark the episode interrupted.

Record salvage errors in the receipt. A sandbox session that refuses further commands after a cancelled exec can return an empty listing that reads as "nothing to copy" when the error is swallowed. A request issued after the stop that never reached the model has no context to show; record it as not forwarded instead of missing.

## Budget settlement

- Write a consumption receipt per attempt at graceful stop. After a hard stop, estimate consumption from evidence of the same boot, such as the attempt's start on the monotonic clock, the last heartbeat, and the shutdown marker's monotonic reading, and mark the value as estimated. Wall clocks can jump across suspend and restore; the monotonic clock is consistent within one boot.
- Set the interrupted-episode policy in configuration, as described in [placement](placement.md), and check the harness default. Enabling a different policy creates a different comparison condition.

## Scoring classes

| Class | Meaning | Report |
| --- | --- | --- |
| Judged success or failure | Episode ran to its own end and was judged | In the score |
| Harness or infrastructure error | Failure of the harness, sandbox, or verifier | Separately; rerun or exclude by protocol |
| Preemption-interrupted | At least one attempt ended by a preemption | Count, with the settled final attempt in the score per protocol |
| Budget-shortened | Final attempt had less time than an uninterrupted run would | Count, as a protocol deviation |
| Unjudged | Evidence missing to judge | Count and reason |

- Keep interrupted episodes out of both success and failure counts until they are settled.
- Report affected-only figures beside campaign-wide ones: a small mean of lost minutes across all episodes can hide large losses in the affected ones.
- Compute episodes per hour only from windows that ended naturally. A window ended by a stop finished only its shortest episodes, and a metric tool that counts interrupted episodes as finished inflates the rate.

## Changing conditions mid-campaign

- A serving or execution change, such as enabling a compile cache, changing the memory limit, or changing an output limit, starts a new run ID. Carry the unfinished task list, leave the old run stopped, and disclose which tasks ran under which condition. Regenerate any frozen record that embeds the changed setting.
- Generated service names can tie the server to the old run. A running server created under the old run's project and network may be unreachable from the new run's controller; restart the server under the new run, which is cheap within the same boot because the page cache still holds the checkpoint.

## Event log and serving identity

- Log every event with a zoned timestamp, type, actor, reason, and source: start requested, start failed, RUNNING, preempted, operator stop, hold placed or removed, dispatch, resume, end. Note the price read at each start.
- Operator stops are censored observations for lifetime estimates; preemptions and failed starts are the data.
- Record the serving identity of self-hosted runs: checkpoint repository and revision, image digest, engine version, and engine arguments that change model behavior. A self-hosted run and a hosted API of the same model name are different conditions; hosted providers may also serve a different quantization.
