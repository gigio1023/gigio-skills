# Provider Notes

Checked against public documentation on 2026-10-18 unless marked as observed. Providers change these terms; recheck the linked page before relying on a value, and record the date you checked.

## Nebius preemptible VMs

- **Notice.** The [preemptible VM guide](https://docs.nebius.com/compute/virtual-machines/preemptible) describes a SIGTERM 60 seconds before the stop, then a forced stop. Observed: the guest saw an ACPI power-button press handled by `systemd-logind`, and the provider's stop operation completed one to two minutes after the guest began shutting down. Observed: preemptions also arrived during early boot, before any guest handler ran.
- **Restart.** Standalone preemptible VMs do not restart automatically, and the guide states that a `RECOVER` recovery policy is rejected for them. Use preemption action `STOP` to keep the VM and its disks. Managed Kubernetes node groups restart preempted nodes when capacity allows.
- **Capacity.** A stopped VM holds no GPU capacity. Starts and creations can fail with `NotEnoughResources`, covered by a [resource-shortage guide](https://docs.nebius.com/compute/virtual-machines/not-enough-resources); observed failed starts spent about 5 minutes before returning. The [capacity advisor](https://docs.nebius.com/compute/virtual-machines/capacity-advisor) reports HIGH, MEDIUM, or LOW allocation likelihood at a point in time, not a guarantee.
- **Storage and addresses.** Persistent disks are kept through a stop; [local SSD](https://docs.nebius.com/compute/storage/local-disks) contents are lost on stop and start. Dynamic public addresses are released on stop according to the preemptible guide, and after more than an hour stopped according to the [network guide](https://docs.nebius.com/compute/virtual-machines/network); static addresses are kept.
- **Pricing.** From 2026-10-08, preemptible VMs on current GPU platforms use dynamic spot pricing that can change at each 15-minute update while a VM runs, capped one cent per GPU-hour below on-demand ([pricing policy](https://docs.nebius.com/signup-billing/pricing-policy)). A pricing policy's per-GPU maximum price can preempt a VM when the market rises above it and also sets scheduling and preemption priority; following the spot price removes the cap trigger. The older numeric preemption priority field is deprecated even though the CLI still offers a flag for it.
- **Events.** Instance metadata exposes maintenance events; no preemption-specific event endpoint was documented.
- **SLA.** The compute terms exclude preemptible VMs from the SLA.
- Observed: an instance update that attached a disk to a stopped VM also started it.
- Observed: GPU VMs exposed no VMX flags and no `/dev/kvm`, and no nested-virtualization setting was documented.

## AWS EC2 Spot

- A two-minute interruption notice through instance metadata and EventBridge; a rebalance recommendation can arrive earlier ([Spot interruptions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-interruptions.html)).
- The [Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/) publishes interruption-frequency buckets per instance type and region over the trailing month. A bucket is not a survival probability for a given episode length.

## Google Cloud Spot VMs

- Preemption starts an ACPI soft shutdown with a short best-effort window, about 30 seconds; the documentation also describes optional additional notice through metadata, off by default ([Spot VMs](https://cloud.google.com/compute/docs/instances/spot)). Recheck the current notice options before designing the hook budget around them.
- The termination action is stop or delete; choose stop to keep persistent disks.

## Azure Spot Virtual Machines

- Eviction notice of up to 30 seconds through Scheduled Events, best effort. Eviction for capacity can happen even with maximum price set to -1. The eviction policy is deallocate or delete ([Spot VMs](https://learn.microsoft.com/azure/virtual-machines/spot-vms)).
- The portal shows an eviction rate per size and region over a recent window; treat it like other advisor buckets.

## Runpod

- Pods do not allow running your own Docker daemon inside the pod ([Pods overview](https://docs.runpod.io/pods/overview)), so a harness that controls Docker for sandboxes cannot run in a standard pod.
- Interruptible pods can stop at any time; do not assume a fixed notice period.

## Other GPU clouds

Several GPU clouds offer only on-demand or reserved capacity. They are candidates for the non-preemptible fallback, subject to stock: check that the instance is a full VM with root and a Docker daemon when the harness needs one.

## Orchestrators

- SkyPilot managed jobs, launched with `sky jobs launch`, recover from preemption by provisioning again and rerunning the task; plain `sky launch` does not ([managed jobs](https://docs.skypilot.ai/en/latest/examples/managed-jobs.html)). Application state still has to be restored by the task.
- dstack retries capacity, interruption, and error events only when its retry policy enables them ([tasks](https://dstack.ai/docs/concepts/tasks/)).
- Ray retries tasks and can restart actors when configured; keep the head node and driver on reliable capacity ([fault tolerance](https://docs.ray.io/en/latest/ray-core/fault_tolerance/nodes.html)).
- An orchestrator's temporary instance boot disk is not durable storage: replacement deletes it. Keep results in object storage or on a disk you manage.
