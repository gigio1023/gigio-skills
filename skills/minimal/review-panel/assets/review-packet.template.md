# Review packet: [artifact], [axis]

You are reviewing an artifact you did not write, in a context kept separate from the session that wrote it. Report what you find in the artifact. Do not edit it.

## What to review

- Paths: [paths]
- Revision: [commit, tag, or document version]; diff range: [base..head, if any]
- Out of scope: [paths or topics]
- Where a silent failure would surface: [callers, consumers of a format, or the metric pipeline to read beside the diff; omit when a defect would fail loudly at the change site]

## Why it exists

[Purpose, the owner's goals, and who reads or uses the artifact. Facts only, with no assessment of its quality.]

## Axis and criteria

- Axis: [fidelity: does it do what [intent source at revision] asks | standards: does it meet the criteria below]
- Criteria: [quoted or summarized criteria]

## Current rules that override older records

- [Newer decision or rule, where it is recorded, and the older record it supersedes]

## Hypotheses to test

- [Optional. A suspicion of the lead, marked as a hypothesis. Confirm or refute it with evidence; do not assume it.]

## Limits

- Read-only: no edits, no commits, no posting, and no runs that change state or spend budget.
- Network: [none | granted for ...]
- Expected duration: [time]
- Output: [write only this report path | return the report as your final message]

## Required response

1. Findings ranked by impact on the purpose above. For each: a short title; evidence as `path:line`, or a section, or a command with its output; why it matters; and a concrete fix.
2. Parts checked and found sound, with the locations read.
3. Declined to judge: each part of the artifact or criterion you set aside, one line each with the reason, such as outside the criteria above, needing access or a run you did not have, or outside what you can assess. Write "none" when you set nothing aside.
4. Questions that block a finding, if any.
5. Verdict for the stated purpose: ready, ready after the listed fixes, or not ready, with the findings that decide it.

Report no finding without evidence in the artifact. Mark anything you could not verify as unverified and name the check that would settle it.
