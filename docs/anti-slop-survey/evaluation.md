# Checker evaluation on real documents

Run on 2026-11-26 with the checkers at this branch's head. Every document is a real text; nothing was seeded. Two documents are private vulnerability reports filed through GitHub private vulnerability reporting in November 2026, written with an AI assistant and reviewed by the reporter; only counts are recorded here. One more is a maintainer's draft advisory edited from one of those reports, also private. The rest are public.

## Documents

| ID | Kind | Words in prose |
| --- | --- | --- |
| Report A | Private four-field PVR report, AI-assisted | 2,587 |
| Report B | Private four-field PVR report, AI-assisted, same mechanism family | 2,282 |
| Report A revised | Report A revised under the new guidance, not filed | 2,325 |
| Maintainer draft of B | Private draft advisory the maintainer cut from Report B | 348 |
| [GHSA-5r3c-5x4v-8gjh](https://github.com/vllm-project/vllm/security/advisories/GHSA-5r3c-5x4v-8gjh) | Published vLLM advisory | 326 |
| [GHSA-25q3-v2hm-8vpf](https://github.com/vllm-project/vllm/security/advisories/GHSA-25q3-v2hm-8vpf) | Published vLLM advisory with verification and not-affected sections | 596 |
| [Qualys regreSSHion](https://www.qualys.com/2024/07/01/cve-2024-6387/regresshion.txt) | Long human research advisory, underlined headings converted to Markdown | 4,676 |
| [writing-sources.md](../writing-sources.md) | This repository's English source notes | 4,828 |
| A private English literature survey | Survey with marked unverified items | 2,899 |
| [maintenance.md](../writing-consolidation/maintenance.md) | This repository's Korean maintenance record | 672 |

Words are counted by `check_structure.py` outside code; `check_slop.py` counts 2,149 English prose words in Report A because it also skips tables and lists.

## Results

| Document | Old: `check_slop` hits | Old: `check_draft` | Old: `check_report` | New: repeated quantities | New: restated sentences | New: scope notes | New: vague pointers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Report A | 0 | 10 | 3 | 9 | 10 | 6 | 1 |
| Report B | 0 | 12 | 1 | 9 | 7 | 4 | 0 |
| Report A revised | 0 | 10 | 3 | 4 | 3 | 4 | 0 |
| Maintainer draft of B | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| GHSA-5r3c | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| GHSA-25q3 | 1 | 4 | 3 | 0 | 1 | 0 | 0 |
| regreSSHion | 0 | 1 | 9 | 1 | 5 | 0 | 0 |
| writing-sources.md | 0 | 1 | 5 | 0 | 0 | 0 | 1 |
| Survey | 0 | 7 | 6 | 0 | 0 | 1 | 0 |
| maintenance.md | 6 | 5 | 2 | 0 | 0 | 0 | 0 |

`check_report` ran with `--venue pvr` on every document so the counts are comparable; its findings on the human documents are mostly placeholders and bold that a plain-text venue would not flag.

The old checkers do not separate the AI-assisted reports from the human and maintainer texts: the reports get no `check_slop` hits, and their `check_draft` findings are 8 and 10 long table cells plus one negation sentence and one opening-paragraph flag each. The new counts do separate them. Both reports carry 9 quantities in three or four of their four fields; the maintainer's 348-word draft of Report B, cut to about 15% of its length, carries none, and neither published vLLM advisory repeats a quantity across fields.

## Precision of the new findings

Each finding was read in context.

- Report A: all 9 repeated quantities restate the same runs: two memory limits, two request sizes, one memory rise, the default budget, the 4-byte charge, and the declared and real dimensions. Of 10 restated sentences, 8 restate a Summary or Details result in Impact; one pairs two different runs that share wording, and one is a partial overlap. All 6 scope notes and the pointer are what the lead's review named.
- Report B: 9 of 9 quantities and 7 of 7 sentences are real restatements.
- GHSA-25q3: the one restated sentence is real; Proof of concept and Verification both say that either id position and any negative id trigger the defect.
- regreSSHion: 2 summary version lines matched a body sentence about one tested version, a legitimate summary; 3 matches and the one quantity came from parallel per-target sections and from code lines the plain-text conversion left in prose.
- writing-sources.md: "is discussed above" names no heading; a real, minor pointer.
- Survey: "Reflected is not executed" matched the scope-note pattern; a false positive.

## Revision under the new guidance

Report A was revised in a scratch copy following the one-home rule: Summary keeps the headline default-settings result, Impact states capability and conditions and points to the Details subsections by name, two scope notes that limited no claim were dropped (remote image URLs, an unwritten patch), "(next sections)" names its heading, and the credit heading left the Proof of concept field. Words fell from 2,587 to 2,325. Repeated quantities fell from 9 to 4; the remaining four are the core mechanism (the 4-byte charge, the declared and real dimensions) and the memory limit the Summary names, which a reader needs in each place. Restated sentences fell from 10 to 3. The four remaining scope notes each limit a specific claim. `check_slop` and `check_report` results did not change.

## Limits

- Ten documents, two of them the target failure. The thresholds (three sections, word-set Jaccard 0.45 with five shared words, three shared quantities) were set by reading these outputs, so they are fitted to this set.
- The checker sees quantities and word overlap. It does not see a repeated claim written with different words and no numbers, or whether a scope note limits a real claim; the guidance leaves both to the reader.
- No model trial: whether an agent following the revised skills writes a shorter report was not measured.
