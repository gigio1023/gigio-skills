# Feedback Loops

Read this when the right loop for a failure is not obvious, when a loop is slow or noisy, when an intermittent failure needs a higher reproduction rate, when an agent or pipeline failure needs a replay, or when shrinking a reproduction. The skill's main file says when a loop is not possible and what to do instead.

## Choose a loop

Pick the cheapest loop that drives the real failing path and checks the reported symptom. The options below run roughly from most direct to most effort; skip any that cannot reach the failure.

1. A failing test at the lowest level that still reaches the failing path, whether unit, integration, or end to end. If the project does not allow new tests in that code, write the same check as a scratch script outside the test suite.
2. An HTTP request script against a locally running service, checking the response that showed the symptom.
3. A command-line run on a fixed input, comparing its output with a known-good result.
4. A headless browser script that drives the interface and checks the page, console, or network traffic.
5. A replay of a captured artifact: a saved request, payload, event log, or message sequence fed through the failing component alone.
6. A minimal harness that runs one component with its dependencies stubbed and calls the failing path directly.
7. A property or fuzz loop over many generated inputs, when the symptom is output that is sometimes wrong.
8. A bisection script between a known good and a known bad state, such as a commit, a dependency version, a dataset, or a configuration, that `git bisect run` or a plain loop can drive.
9. A differential run that sends the same input through two versions or configurations and compares the outputs.
10. A guided script for a person, when a step needs one, such as a hardware device, a third-party dashboard, or a sign-in. The script prints one instruction at a time, waits for confirmation, and records the person's observations as `KEY=VALUE` lines the agent can read. Leave signing in to the person as an instruction and never capture credentials in the script.

## Replay agent and pipeline failures

A rare failure in an agent or model pipeline often becomes deterministic once the stochastic step is fixed. Save the trajectory, tool results, and model responses from a failing run, then replay from the step before the failure with recorded responses in place of live model calls. If the failure persists under replay, the cause is in the surrounding code, such as parsing, state handling, truncation, retries, or tool wiring, and the replay is a fast loop for it. If the failure disappears under replay and depends on what the model sampled, the question has become a rate across samples, which needs a sampled comparison rather than a mechanism hunt.

## Improve the loop

Once a loop exists, improve it along three axes.

- Faster: reuse expensive setup, drop initialization the failure does not need, and narrow the scope to the failing path.
- Sharper: check the specific symptom, such as the error text, the wrong value, or a latency threshold, rather than the absence of a crash.
- More deterministic: pin the clock, seed random generators, isolate the filesystem and network, and control concurrency.

A slow loop with an unstable verdict tests few hypotheses; a loop that returns the same verdict in seconds can test many.

## Raise the reproduction rate of an intermittent failure

- Repeat the trigger many times and count, reporting the rate with its run count, such as 37 of 200.
- Run copies in parallel, add CPU or I/O load, shorten timeouts, or insert delays at suspected race points.
- Change one condition at a time and record which ones raise the rate; each is evidence about the mechanism.
- Compare rates between conditions only with enough runs that the difference is larger than run-to-run variation.

## Shrink the reproduction

Remove one element at a time, such as an input field, a step, a configuration value, or a caller, and run the loop again after every removal. Keep a cut when the loop still fails and undo it when the loop passes. The reproduction is minimal when removing any remaining element makes the failure disappear. Keep the original scenario as well; the final verification runs against it, not only against the minimal case.
