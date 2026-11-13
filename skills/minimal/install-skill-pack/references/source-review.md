# Source Review

For a third-party source, read the complete selected package before installation and judge it as a whole, including whether its powers are necessary and proportionate to the user's request.

## Identity And Completeness

- Confirm the selected directory, frontmatter name, repository remote, revision mode, and reviewed commit. Distinguish a default-branch HEAD, named branch, and exact commit rather than assuming a branch name.
- Inventory every file, including hidden files, references, scripts, assets, templates, configuration, and executable bits.
- Reject path escapes, unexpected submodules, and symlinks that resolve outside the package.
- Inspect binaries, encoded payloads, generated blobs, and minified or obfuscated content. If their behavior cannot be established with available tools, block rather than infer safety.

## Commands And Dependencies

- Trace every command, script, hook, executable template, and fetched dependency.
- Check argument quoting, untrusted interpolation, `eval` or indirect shell execution, download-and-execute flows, package lifecycle scripts, path traversal, broad permission changes, and destructive targets.
- Treat fetched or dynamically selected code as unreviewed until its source, version, integrity boundary, and executed behavior are understood.

## Data And Authority

- Identify every network destination and every read of credentials, environment variables, private files, browser state, or user data.
- Block unexplained collection, transmission, logging, or persistence of sensitive material.
- Inspect instructions for hidden scope expansion: bypassing approval, self-modification, persistence, prompt injection, covert tool chaining, automatic external writes, delegated authority, or requests to conceal actions from the user.
- Distinguish an inherent capability risk from an unnecessary one. A skill may legitimately run commands, access a named service, or edit files when that is its disclosed purpose and the user's authority still bounds those actions. Undisclosed or unnecessarily broad behavior fails review.

## Decision

For each selected skill, report the inspected files, intended capability, commands and external access, material findings, mitigations or authority boundaries, and a `pass` or `block` decision. Report observable evidence and a concise rationale.

External audit tables may point to code worth inspecting, but they do not make the decision. Investigate a positive finding against the reviewed source. Missing, delayed, or unavailable partner results do not replace the source review and do not independently block installation.
