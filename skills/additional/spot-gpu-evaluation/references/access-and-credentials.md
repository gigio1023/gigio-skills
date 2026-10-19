# Access and Credentials

Keep the model server private, keep every path to it reconnectable, and give each automated actor only the permissions its job needs.

## Model server exposure

- Bind the server to loopback, for example vLLM with `--host 127.0.0.1`, and require an API key, for example through `VLLM_API_KEY` in an owner-only environment file. When the container uses host networking, the loopback bind is what keeps the port private; with port publishing, publish to `127.0.0.1` only.
- From another machine, check that the node's public address refuses the port and that a request without the key gets 401.
- Other users and containers on a relay host can reach that host's loopback and Docker bridge. The API key is the boundary there.

## Tunnels and relays

- From an operator or controller host: `ssh -N -L 127.0.0.1:PORT:127.0.0.1:PORT gpu-node`.
- To a benchmark host that cannot reach the GPU node directly, run a remote forward from a host that reaches both: `ssh -N -R 127.0.0.1:PORT:127.0.0.1:PORT bench-host`.
- Containers on the benchmark host cannot reach its loopback. Expose the forward on the Docker bridge gateway, 172.17.0.1 by default, with a socket-activated `systemd-socket-proxyd` unit that forwards to `127.0.0.1:PORT`.
- Run each SSH forward as a unit with `Restart=always` and `RestartSec=10`, and SSH options `ExitOnForwardFailure=yes` and `ServerAliveInterval=15`. Leave tunnel units disabled while the GPU node is stopped, so they do not reconnect in a loop.
- Harness validation may reject loopback or private endpoints for hosted providers. Declare the relay explicitly in the configuration and include the upstream serving identity in the comparison condition, so the run is not mistaken for the hosted provider's.

## Addresses

- Dynamic public addresses are released when an instance stops, or after it has been stopped for a while, such as an hour, depending on the provider. Getting the same address back is luck.
- Prefer a private network between the restarter, the monitor, and the GPU node, or a static address. Accounts can have small public IPv4 quotas, which is one reason a restarter ends up without a public address; it still needs a route that does not pass through the GPU node.
- Edit SSH client configuration atomically and only with a validated address. An empty `HostName` line makes `ssh` reject the whole file, which cuts every SSH session on that machine, including other people's. After each edit, run `ssh -G HOST` for every host the file serves and require exit status 0.

## Service accounts and permissions

| Actor | Grant | Check |
| --- | --- | --- |
| Restarter | View, start, and stop the listed instances | A read of another instance and a project listing are denied |
| Publisher | Upload and read on one bucket, no delete | A delete is denied |
| Monitor | SSH to read files; provider reads only for one-off waits | No start or stop permission |
| End handler | Forced-command SSH key on the restarter host for its hold | Any other command is refused |

- Use headless CLI profiles backed by a service-account key. Federated profiles that open a browser are for interactive use and stall unattended jobs.
- Some reads that diagnosis needs are absent from least-privilege grants: operation details and their errors, serial console logs for a preemption during boot, capacity advice, price estimates, and project listings. Without them, judge a start from instance state alone. Add a narrowly scoped read grant when a diagnosis needs it, and record that it was added.
- Keep secrets in mode-600 files. Compare copies on different hosts by a hash prefix and never print values.

## Node setup

- cloud-init cannot create a user with a UID the image already uses, and UID 1000 is often taken. Leave the UID unpinned or choose a free one; when a fresh node accepts no login, read the serial console for the user-creation error.
- Images may ship Docker daemon drop-ins that change the storage driver or default shared memory. Align the daemon configuration with the reference host when results must be comparable, and record the versions.
- Nodes rarely hold source-control credentials. Ship code as a `git bundle`, check out the exact commit, and record it.
