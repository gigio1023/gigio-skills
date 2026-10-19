# Cold Start: Making the Server Healthy Sooner

After boot, the model server's time to healthy is the largest stage you control. It is mostly the checkpoint read, then kernel compilation and graph capture.

## Contents

- Measure the disk before choosing it
- Download and stage once
- Persistent compile and JIT caches
- safetensors prefetch and memory limits
- Page cache across restarts
- Serving auto-start on boot
- What does not help

## Measure the disk before choosing it

- Read the checkpoint with O_DIRECT, which bypasses the page cache and measures the device and its network path: `bash scripts/disk_read_throughput.sh -s "1 8 16" CHECKPOINT_DIR`. Use files no case has read recently; repeated reads of the same files can be served from a hypervisor or storage cache and report several times the real rate.
- Measure single and parallel streams. On one GPU cloud, a replicated network SSD boot disk read about 0.45 GB/s whatever the parallelism, well below its documented estimate, while a non-replicated, high-throughput network disk read about 2 GB/s from a single stream. Documented formulas may depend on disk size and type; trust the measurement.
- Local NVMe is fastest, but on many providers its contents are lost when a spot instance stops. It can serve only as a cache refilled from a durable copy, which brings the slow read back.
- Use RAID0 across network disks only after measuring that the VM's aggregate disk cap exceeds one disk's rate: attach a second disk and read both in parallel first.
- Non-replicated disks can be lost. Keep a re-downloadable source or a slower replicated copy as fallback, and verify the fast copy by file hashes before serving from it.
- For bulk copies between network disks, the default readahead, often 128 KiB, can halve sequential throughput. Raise `/sys/block/<dev>/queue/read_ahead_kb` for the copy and restore it afterwards.
- Create and attach new disks while the instance is stopped, so a running spot instance never needs a stop for an attach. On some providers the update call that attaches a disk also starts the stopped instance, and billing with it.

## Download and stage once

- Download the checkpoint once to a durable disk, pinned to a revision, and verify checksums. Parallel Hugging Face downloads, for example `hf download REPO --revision REV --max-workers 16`, reached 0.5 to 1.5 GB/s on cloud VMs. Read the transfer result in the output as well as the exit code, and record the CLI version.
- Pull serving images by digest onto the boot disk ahead of time. Copy custom images with `docker save | docker load` at low priority, using `nice -n 19` and `ionice -c3` on the source, when a registry is unavailable or the source host is busy.
- A node without Git credentials can receive code as a `git bundle`; check out the exact commit and record it.

## Persistent compile and JIT caches

- Serving engines compile and tune kernels on first start: torch.compile, Triton, DeepGEMM, FlashInfer autotune, and CUDA graph capture. Mount a cache directory from a persistent disk into the serving container and point the engine's cache locations at it.
- Key the directory by engine version and GPU type. A cache from another version may be ignored or may break the start.
- Make the directory writable by the user the container actually runs as. An image that declares no user runs as root, and some image-inspection paths omit an empty user field, so read the effective UID rather than the image metadata alone.
- Effect seen in practice: several minutes of first-boot warmup fell to under a minute on later boots.

## safetensors prefetch and memory limits

- vLLM's `--safetensors-load-strategy prefetch` reads checkpoint files into the page cache ahead of the loader. Page-cache pages are charged to the memory cgroup that first reads them, so they count against the serving container's memory limit.
- When that limit is smaller than the checkpoint, prefetched pages are evicted before the loader uses them and the disk is read about twice. In one case weight loading took about 2x the single-pass time.
- Signs: the cgroup's `memory.events` `max` counter rising during load, disk read bytes near twice the checkpoint size, and the engine warning that the checkpoint does not fit in available RAM.
- Fix: when host RAM allows, set the container memory limit above checkpoint size divided by 0.9, the fit threshold vLLM applied in the version checked, and confirm other admission limits still fit. Otherwise leave the load strategy at its default.
- One prefetch thread per tensor-parallel rank was enough to saturate a 2 GB/s disk with 8 ranks; more threads do not help a disk at its cap.
- Warming the page cache with a host-side sequential read before starting the container charges the pages outside the container's cgroup and should avoid the eviction. This is a candidate, not measured here.

## Page cache across restarts

- Within one boot, restarting the container while the checkpoint is still in the host page cache reloaded weights in under a minute instead of about 6 minutes cold. Chain runs on the same boot when possible.
- A new boot is always cold, and every preemption is a new boot.

## Serving auto-start on boot

Start the server from systemd at boot so the stage between RUNNING and serving start needs no operator. Gate it with a marker file so the node can boot for other work.

```ini
# /etc/systemd/system/model-serving.service
[Unit]
Description=Start the model server at boot when the serve-on-boot marker exists
After=docker.service network-online.target
Wants=network-online.target
Requires=docker.service
RequiresMountsFor=/srv/ckpt /srv/compile-cache /srv/durable
ConditionPathExists=/srv/durable/serve-on-boot

[Service]
Type=simple
User=serving
ExecStart=/srv/durable/bin/serve-model.sh
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Remove the marker before booting the node for any other work; otherwise the server takes every GPU. The serving script binds to loopback and reads its API key from an owner-only environment file, as in [access and credentials](access-and-credentials.md).

## What does not help

- More prefetch threads or parallel readers on a disk already at its cap.
- Restarting more often, or restarting on a schedule.
- A larger instance when the bottleneck is the disk.
