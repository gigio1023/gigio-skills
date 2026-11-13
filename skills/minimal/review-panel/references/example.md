# Worked Example: Proration in a Billing Service

A synthetic review. Paths, revisions, dates, and amounts are invented to show the shape and depth of a judgment table.

## Setup

The session implemented mid-cycle plan changes with proration in a billing service, following `docs/design/proration.md`. The user wrote: "Review this with Fable and Codex before I merge."

The panel was Claude Fable and GPT-6 Astra, the latter through `codex-delegate` in a read-only sandbox with no network. Each family ran the fidelity axis and the standards axis in separate contexts, four contexts in all, because a billing error reaches customer invoices and fails silently. The packets named revision `a1b2c3d`, diff range `main..a1b2c3d`, and the design document as the intent source. The fidelity packet left out decision log entry D4 of 2026-09-30, which replaced the design document's daily-rate formula with a per-second formula to match the payment provider.

## Judgment table

| ID | Finding | Raised by | Evidence checked | Judgment | Action |
| --- | --- | --- | --- | --- | --- |
| F1 | Rounds each line, not the invoice total | Astra, fidelity | `billing/proration.py:42`, design Rounding section, preview run | Valid | Fixed |
| F2 | Naive datetimes miscount days for other time zones | Fable, standards | `api/handlers.py:55`, `billing/periods.py:18`, `jobs/renewal.py:31`, renewal dry run | Partially valid | Fixed after user approval |
| F3 | Per-second ratio instead of the design's daily rate | Fable and Astra, fidelity | Design Formula section, decision log D4 | Rejected | None |

- **F1, valid.** `billing/proration.py:42` rounds each prorated line to cents, while the design document's Rounding section says to round once at the invoice total. `python -m billing.preview --fixture fixtures/upgrade_mid_cycle.json` printed a total of 30.01 against the 30.00 the fixture expects. One reviewer raised it, and the run settles it. The fix sums `Decimal` amounts and rounds once; the same run now prints 30.00.
- **F2, partially valid.** The stated cause does not hold: the API normalizes every timestamp to UTC at `api/handlers.py:55`, so a customer's time zone never reaches period arithmetic. A narrower defect does: `billing/periods.py:18` builds naive datetimes, the renewal job passes an aware one from `jobs/renewal.py:31`, and comparing them raises `TypeError`. A dry run of the renewal job on `fixtures/renewal_month_end.json` reproduced it. The fix makes period boundaries aware UTC datetimes, not per-customer time zones as proposed. Because it changes the renewal job, which the reviewed change did not touch, the table went to the user before the fix was applied.
- **F3, rejected.** Both fidelity reviewers cited the design document's Formula section, which decision log entry D4 superseded on 2026-09-30; the code follows D4. Their agreement rests on one stale premise, the packet's omission, so it adds no evidence. The lead added D4 to the packet's section on current rules for any later round.

## Re-check and report

After both fixes, the lead re-ran the preview and the renewal dry run on their fixtures and ran the existing test suite; all passed, and no tests were added. The report opened with "ready to merge; F1 and F2 are fixed", then gave the table, the two runs with their output, F3 with its reason, and the panel as run: four contexts, each reviewer's model and effort, read-only access, no network.

## What the example shows

- The finding one reviewer raised was valid, and the finding both raised was rejected; each judgment came from the artifact.
- Partially valid kept the real defect, dropped the wrong cause, and fixed the defect rather than applying the reviewer's proposal.
- The fix that reached beyond the reviewed change went to the user first; the fix inside it did not.
- The rejection exposed a packet gap, a current rule missing from the override section, and the packet was corrected.
