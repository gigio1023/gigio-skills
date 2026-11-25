# Style Rules

A report is read by someone deciding, under time pressure, whether to believe it. Sentence style matters because it changes how fast the reader finds the facts and whether they trust the rest. These rules apply to the report and to replies during triage; `copydesk`, when installed, supplies general sentence craft.

## Contents

- Sentences
- Person and tense
- Formatting by venue
- Flagged patterns
- Reading checker output

## Sentences

- Put the finding first and background after it; a reader should not scan pages to find the affected file, version, and impact (`kernel-policy`, `ghsl-advisories`).
- One claim per sentence, with its condition first: "If the server runs with the default buffer size, ..." (`h1-curl-socks5`, `ghsa-asynchttpclient`).
- Name the actor and the action. "The `/export` handler reads the path from the query string" beats "the path is read".
- Every number carries its unit and where it came from, such as the attachment that shows it (`local`).
- Use the project's own names for components, options, and messages, and established field terms for weakness classes. Invented or misused terms are read as a sign the writer does not understand the system (`cert-credibility`, `reddit-survey`).
- Policies differ on AI-drafted text. curl asks the reporter to write the report after verifying the finding, and Apple discourages long AI-generated descriptions, while Django and the kernel accept short drafts that are disclosed and verified by the person (`curl-ai-policy`, `apple-guidelines`, `django-policy`, `kernel-policy`). Whoever drafts, cut what generated reports tend to add: length, decoration, and speculative consequences (`kernel-policy`, `apple-guidelines`).
- Plain, even imperfect, English is fine. Grammar is not a credibility signal, and some programs accept reports in other languages (`cert-credibility`, `google-native-language`).
- Keep the narrative of how you found it to one sentence or a separate short section; a story preamble before the finding reads as padding (`cert-credibility`).
- Say each limit once, in the sentence it limits. Do not repeat caveats in several sections (`local`). A run of "not tested" and "not run" sentences that limit no claim in the report answers objections nobody raised; keep the ones a triager would otherwise read as covered.
- State each measured result once, in the field that owns it. The summary carries the headline result in a sentence, details or reproduction carry the figures, and impact says who can do what under which preconditions without listing the measurements again. A multi-field form invites each field to stand alone; the copies drift when one is corrected, and the triager reads the same numbers three times. Published maintainer-written advisories in the surveyed set keep the impact field to a few sentences with no repeated figures (`ghsa-vllm`, `local`).
- Point to a section by its heading. "(Next sections)" or "see below" in a form whose fields the maintainer may read in any order sends them searching (`local`).

## Person and tense

Impersonal, we, and I all appear in accepted reports (`p0-report-2026`, `oss-qualys-regresshion`, `curl-h1-uaf`). Pick one and keep it. Use I or we for opinions and judgments so they are not read as facts (`h1-curl-socks5`). Code behavior is present tense; what you did and what happened in a timeline is past tense (`ghsl-advisories`, `oss-qualys-regresshion`). Timeline lines read `YYYY-MM-DD: <actor> <event>.`, one event each, with the actor named (`oss-qualys-regresshion`, `oss-suse-screen`).

## Formatting by venue

| Venue | Use | Avoid |
| --- | --- | --- |
| Linux kernel and plain-text lists | Plain text, indented code, about 72 columns | Markdown, HTML, RST; attachments where possible (`kernel-policy`) |
| oss-security | Plain text with underlined or numbered section titles | Markdown syntax (`oss-qualys-regresshion`, `oss-suse-screen`) |
| GitHub private reporting, GHSA | Markdown headings, numbered lists, fenced code with a language, tables for version matrices | Bold runs inside prose, emoji, decorative headings (`ghsa-vllm`, `ghsa-mlflow`, `local`) |
| HackerOne, Bugcrowd | The program template, including its bold labels; code blocks for requests | Bold beyond the template's labels and one key note (`h1-node-smuggling`, `bugcrowd-guide`) |
| Vendor portals | Field by field as the portal asks | Narrative in fields meant for steps (`msrc-example`, `bmo-webgl`) |

The kernel policy asks for plain text; the 72-column width comes from the Qualys post, not from the kernel (`kernel-policy`, `oss-qualys-regresshion`).

Bold is contested: one platform guide recommends it for key notes, one research team uses it for a single contrast, and one commenter in a single community thread read bold pseudo-headings as a sign of generated text (`bugcrowd-guide`, `ghsl-advisories`, `reddit-survey`, weak). The checker found bold in 8 of 22 published reports and advisories, and no surveyed source names bold as a reason for rejection. This pack defaults to headings for structure and no bold inside sentences (`local`).

## Flagged patterns

Patterns citing a receiver policy have drawn closures or corrections. Patterns citing only `local` or `reddit-survey` are this pack's choices or weak signals. The checker flags most of them; all of them need judgment rather than mechanical deletion.

| Pattern | Why it is flagged | Sources |
| --- | --- | --- |
| Severity words without a basis: critical, severe, high risk, in the title or body, or a score without a vector | Overclaims get downgraded, and exaggeration counts against credibility | `curl-h1-uaf`, `cert-credibility`, `openssf-template` |
| Self-assessment where the policy forbids it | Some projects ask for no CVSS and no verdict from the reporter | `django-policy`, `curl-policy` |
| Hype: devastating, catastrophic, complete takeover, trivially exploitable, wormable | Extraordinary claims need extraordinary evidence; dire impact for a trivially found bug is a warning sign | `cert-credibility` |
| Impact claims with neither a condition nor a status: could lead to, may allow, potentially | Theoretical or speculative impact is rated low | `google-vrp-quality`, `kernel-policy` |
| A claim written as fact that was not executed or checked | Unverified tool output is closed; source-only claims must say so | `curl-ai-policy`, `ghsa-nginx-ui`, `apple-guidelines` |
| Vague versions: latest, current, all versions, a distribution build | Not processed by some receivers; vague versions count against credibility | `kernel-policy`, `cert-credibility` |
| Scope words without the checked scope: only, all, every, any | A single counterexample breaks the claim; say what was checked | `cert-credibility`, `local` |
| Generated filler: it is important to note, in summary, delve, comprehensive, robust, leverage, plays a crucial role | Reads as unedited model output; the word list is this pack's | `local` |
| Courtesy and urgency padding: I hope this helps, please do not hesitate, urgent, ASAP | Adds nothing; one short thanks at the end is fine | `reddit-survey`, weak; `curl-h1-uaf` for the thanks |
| Em dashes | This pack's style choice | `local` |
| Emoji, decorative bold | Do not survive plain-text venues; weak community signal | `kernel-policy`, `reddit-survey`, weak |
| Placeholders: TODO, TBD, XXX, angle-bracket fields, DRAFT | Empty or placeholder reports can suspend an account and always cost a round trip | `chromium-vrp-faq`, `local` |
| Raw tool output as the report | Scanner and fuzzer output is not a vulnerability report | `cert-credibility`, `msrc-faq` |
| A video or images with no text | Imagery supports a written description and does not replace it | `cert-credibility` |
| Brand names, epigraphs, jokes in a private report | Public-post customs that distract the triager | `oss-qualys-regresshion`, `wiz-ingress` |
| CWE, CVSS vector, and narrative that disagree | A visible inconsistency reviewers catch first | `ghsa-faraday`, `cwe-mapping`, `reddit-survey` |

Hedges are not the defect. Experts use may and potentially to mark an undemonstrated possibility beside a demonstrated claim (`p0-report-2026`, `ghsl-advisories`). Flag only an Impact claim that carries neither a condition nor a status; fix it by stating the condition, demonstrating it, or marking it undemonstrated.

## Reading checker output

`scripts/check_report.py` prints findings by line with a category, then a scan coverage summary that lists every file and archive member as scanned, partial, skipped, or error. Treat each finding as a question:

- `severity-word` and `severity-no-vector`: is the word or score supported by the evidence, wanted by the venue, and accompanied by a vector?
- `impact-modal`: does the sentence carry its condition, or should it become a demonstrated statement or move to a separate conditional sentence?
- `hype`, `ai-filler`, `courtesy`: delete or replace with the fact the word was standing in for.
- `scope-word`, `vague-version`: state the checked scope or the exact version.
- `tested-version-missing`: add the executed version and commit, or say none was executed.
- `placeholder`: fill or remove before handing over.
- `em-dash`, `emoji`, `bold`, `markdown-in-plain-text`: reformat for the venue.
- `private-path`, `hostname`, `private-ip`, `token`: redact in the report and the evidence.
- `attachment-unreferenced`: cite the file from the observation it supports, or drop it.
- `scan-error`: a file or archive member could not be read, such as an encrypted or corrupt archive; open or decrypt it and check it by hand.

Zero findings do not make a report correct, and a finding can be legitimate, such as a severity word inside a quoted policy. The checker cannot tell whether a claim was verified; only the person can. `scripts/fixtures/flawed-draft.md` is a synthetic draft with most of the patterns above; run the checker on it to see the output format. On six published reports of different kinds the checker gave seven findings, median one per document, two of them real defects, so expect a finding or two on good reports too. `severity-no-vector` is off for `pvr`, `ghsa`, and `h1`, where the form carries the vector, and the ASCII ` -- ` is accepted in the plain-text venues `email`, `plain`, and `oss-security`.
