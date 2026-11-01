# Cold Reader

Read when the rendered note is ready for its reader test. A reader who has not seen the session gets only what the team will get and answers fixed questions. The answers show whether the note works without its writer; compare them with the data file, not with what the writer meant.

## When it runs

By default, whenever the harness can start a subagent. Use one reader with a fresh context. When no subagent is available, say in the report that the cold-reader pass did not run; do not answer the questions yourself as a substitute, because the writer already knows the answers.

## What the reader gets

Only the rendered output: the PDF path, or its page images and extracted text when the reader cannot open a PDF. Not `note.json`, not `diff.json`, not the session, and not the expected answers. State the reader role the note is for, such as "a support lead who tags customer feedback and has not followed this release".

## Questions

Ask all of them, in this order, and ask the reader to quote the page and sentence that answers each:

1. What changed between the two versions? Name the versions and the three changes that matter most to you.
2. What must you do? Name the IDs involved, and any date the note gives.
3. Which numbers support the changes? Give the totals before and after, and the added, removed, and changed counts.
4. Which IDs no longer exist, and what replaces each one?
5. Pick one material change. What did it look like before, what does it look like now, and why did it change?
6. Which sentence, label, or chart did you have to read twice, and what did you first take it to mean?
7. What did you expect to find that is missing?
8. Which names for concepts did you not recognize? For each, say whether the note explains it or points to where the artifact defines it.

## Turning answers into fixes

Compare answers 1 to 5 with `diff.json` and the material changes in `note.json`.

| Reader answer | Fix |
| --- | --- |
| Wrong or missing count | Move the count closer to the claim it supports, or label it; check the overview and caption tokens |
| Missed a required action | Lead the actions with the role, or move the action into the opening |
| Wrong successor for a removed ID | Add the successor to the action line and the change card; check the successor file |
| Cannot state why a change was made | Write the reason the decision record gives, or state that none is recorded |
| Reread a sentence | Apply the writing review prompts to that sentence |
| Did not recognize a concept name | Replace it with the artifact's term or the field's standard term; when it is the artifact's own term, explain it at first use |
| Misread a chart | Rewrite the caption's first sentence as the finding, or choose a different pattern |
| Expected something missing | Add it when it belongs to the net change between the versions; otherwise leave it out and say why in the report |

Fix the source, rebuild, rerun the checks, and give the revised output to a new reader only when a fix changed the structure of the note. Report each answer that disagreed with the data file and what changed because of it.

## Source

The procedure adapts the Reader Testing step of Anthropic's `doc-coauthoring` skill, which runs predicted reader questions through a fresh subagent that sees only the document ([anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring), read at commit `ca45fc4` on 2026-10-28), and the fresh-context review in [tw93/Kami](https://github.com/tw93/Kami).
