# Sources and Scope

Written 2026-10-19. Provider behavior in [provider notes](provider-notes.md) was checked against the linked documentation on 2026-10-18; recheck before quoting a notice period, restart rule, or price mechanism.

## Public sources

- Provider documentation linked in [provider notes](provider-notes.md): Nebius preemptible VMs, resource shortages, capacity advisor, local disks, networking, and pricing policies; AWS Spot interruptions and the Spot Instance Advisor; Google Cloud Spot VMs; Azure Spot Virtual Machines; Runpod Pods. Used for notice delivery, restart semantics, storage and address retention, and pricing mechanisms.
- John Thorpe et al., "Bamboo: Making Preemptible Instances Resilient for Affordable Training of Large DNNs," USENIX NSDI 2023. Spot interruption traces on GPU instances, including interruptions clustered within zones; used only as background that interruption rates vary by pool and time.
- [vLLM documentation](https://docs.vllm.ai/) and engine arguments for `--safetensors-load-strategy`, `--host`, and API keys. Used for the prefetch and exposure notes; the 0.9 fit threshold was read from the vLLM source of the version in use and may change.
- [systemd.unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html), [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html), [systemd-run](https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html), and [systemd-socket-proxyd](https://www.freedesktop.org/software/systemd/man/latest/systemd-socket-proxyd.html). Used for unit ordering, stop actions at shutdown, transient units, and the bridge relay.
- SkyPilot, dstack, and Ray documentation linked in [provider notes](provider-notes.md). Used for what orchestrators recover and what they leave to the application.

## Local material

The operating rules, thresholds, and rules of thumb come from the maintainer's own evaluation runs on spot GPU nodes: restart breakdowns, disk measurements, restarter and end-handler failures, publication defects, and monitoring practice. They are stated without identifying data, and every example is synthetic. The interruption and overhead formulas are standard results for exponential lifetimes, and `scripts/spot_math.py` reproduces every number quoted from them.

Package validation and the script runs establish that the files are well formed and the scripts compute what they state. They do not establish that a given provider still behaves as described, or that a particular run's recovery works; the forced-stop qualification in `SKILL.md` does that.
