# Anti-slop survey, November 2026

AI-assisted vulnerability reports that pass every lexical check can still read as slop because of structure: the same results restated in each field of a multi-field form, runs of "not tested" notes, and pointers such as "(next sections)". No public skill, linter, or rule set surveyed on 2026-11-25 counts results across sections, so copydesk gained `check_structure.py`, and copydesk, vuln-report, and the project-local submission-review skill gained a one-home rule for results and scope notes plus a casual register for follow-up comments.

| File | Content |
| --- | --- |
| [sources-skills.md](sources-skills.md) | Public skills and linters at pinned revisions, with licenses and what was borrowed |
| [sources-tells-triage-research.md](sources-tells-triage-research.md) | Wikipedia tells pages, maintainer and platform triage views, 2024 to 2026 research |
| [evaluation.md](evaluation.md) | Old and new checkers on ten real documents, precision, and a revision under the new guidance |

## Findings

- **Structure separates the target failure; words do not.** On two AI-assisted PVR reports, `check_slop.py` found nothing and `check_draft.py` found only long table cells. The new counter found 9 quantities in three or four of four fields in each report and 7 to 10 restated sentences, against 0 repeated quantities in two published vLLM advisories and in the maintainer's 348-word cut of one report ([evaluation](evaluation.md#results)).
- **Public tools stop at the section boundary.** Vale's `ContentDuplication` compares paragraphs only within one section; slop-guard counts phrase reuse across the document; unslop measures intro previews and recap loops. None counts a number across fields ([skills survey](sources-skills.md#coverage)). "Science or Slop?" measures macro redundancy as cross-section n-gram overlap in papers, the closest published method ([research](sources-tells-triage-research.md#research)).
- **A model verdict is a poor slop detector, and a slop-removal prompt overcorrects.** Language models agreed with human slop labels near chance, and slop-aware prompting dropped supported content. The checks therefore list spans for a reader, and revision compares scope notes and figures before and after.
- **Triagers describe slop by cost and evidence.** curl, the Linux kernel, Django, and Bugcrowd name length, many sections, speculative impact, generic text, unverifiable references, and follow-ups that answer with more generated prose or go silent. vuln-report already covered most of these; the additions are the product-name deletion test, the canary rule, and the follow-up register.
- **Follow-up comments have their own register.** Wikipedia's comments page lists a customer-service register (greetings, assurances, offers of help, headed sections) as a tell. The guidance now keeps the formal register for the report body and asks for a few casual sentences that answer first in comments.
- **The credit line moved out of the form.** In one filed report the credit heading sat in the Proof of concept field to stay out of the published advisory; the maintainer's draft kept it in the body anyway. GitHub PVR already credits the submitting account, so submission-review now puts a display-name request in the first comment.

## Changes

| Skill | Change | Finding |
| --- | --- | --- |
| copydesk | `scripts/check_structure.py`: repeated quantities, restated sentences, scope notes, vague pointers; several files read as one form | Structure separates the target failure |
| copydesk | One home per result in multi-section documents; scope notes once beside the claim; before-and-after scope-note comparison ([authoring and revision](../../skills/minimal/copydesk/references/authoring-and-revision.md#remove-conversation-residue)) | Same; overcorrection risk |
| copydesk | Model verdicts and slop-removal prompts named as unreliable in the AI-slop section | Shaib et al.; Oh et al. |
| copydesk | Comment or reply form; writing-profile line on comment register, synced to the repository instruction template | Follow-up register |
| copydesk | `scripts/check_slop.py` lists Korean sentences that end in a negation and negate-then-affirm frames; the Korean guide and the writing profile gain a deletion test for negative sentences (added 2026-11-26) | Owner preference; Zamaraeva et al.; Strunk's positive-form rule |
| vuln-report | Style rules: each result in its owning field, scope-note runs, named pointers; presubmit item; step 10 runs `check_structure.py` when copydesk is installed | Structure; maintainer-written advisories |
| vuln-report | Follow-up replies answer first, casual, no greeting or recap; canary requests go to the person; two catalog sources added | Triage views |
| submission-review (project-local) | Stranger read covers fields as one document; checklist items for one field per result, scope notes, generic text, tool-addressed text; follow-up comment section; credit in the first comment; evidence-grounded cuts | All of the above |

Not adopted: banned-word or metaphor-verb lists, composite slop scores, detector-evasion and voice-mimicry goals, persistent hooks, and sending private reports to third-party APIs ([skills survey](sources-skills.md)). A corrective-disclaimer counter ("rather than", "does not by itself") was not added because it did not separate the reports from human text in the evaluation set. The Korean negation lists added on 2026-11-26 make no such claim: they have no human baseline and only locate sentences for the owner's deletion test.

## Open questions

- Should this pack's English house style drop the corrective frames Wikipedia lists as mid-2026 tells? `docs/writing-sources.md` uses them 11 times; the reports used them none.
- Should the thresholds be refitted on a larger set of the owner's accepted reports, as slop-guard fits its thresholds on a reference corpus, once more reports exist?
