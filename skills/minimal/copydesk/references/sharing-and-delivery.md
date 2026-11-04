# Sharing and Delivery

Use for publication, a change of audience, or a shared revision that changes sensitive content. Reuse known recipients, access, and authorization from the session. The checks below guide the writer; routine sharing does not require a questionnaire or a fresh approval when the user has already authorized it. The internal examples reflect this pack's default shared-report preferences, not a universal rule for every genre.

## Latest shared copy

When colleagues or the user have edited the shared copy, retrieve that version before any revision or republication and treat it as the current baseline. Reconcile differences with the local source before rebuilding; preserve intentional deletions and reconcile intervening edits within the requested revision scope. Familiarity with the original draft is not evidence that the shared copy is unchanged.

## Recipients and sources

- Match detail and attribution to the audience. Page ownership or the sharing message already names the author; no introductory byline, no "the author's synthesis" paragraph, and no sentence that repeats why the page is shared.
- Keep an action owner or observation date when it changes meaning. Preserve relevant events and accountability without personal evaluation, and add no explanation whose only job is to show caution.
- Every claim the reader must verify cites a source the reader can open: a Slack permalink, a Notion page, a GitHub blob pinned to a commit, an issue, a public source. Inspect the destinations: a bare Markdown filename linked as a website, a localhost address, a `vscode://` link, and a private local path are not team citations. Replace them with an authorized link or with the supported explanation itself. No folder inventory and no blanket source disclaimer; when essential access is unavailable, state that concrete limitation once.
- Restricted working records do not travel with the document.

| Distribution | Links allowed | Pass depth |
| --- | --- | --- |
| Author only | Anything, including local paths | Credential hygiene |
| Team | Links the team opens with normal access; internal key and system names stay | Passages about named colleagues, claims stated beyond the record |
| Whole company (Notion, all-hands) | Company-wide links only; no author-machine path | Everything below |
| Outside the company | Public sources or material explicitly cleared for these recipients | Confirm disclosure scope for private material |

## Sharing pass

Assess company and personal exposure separately using the actual audience and content. This is an editorial check, not a request to ask the user these questions. A concrete concern may need clarification; a hypothetical possibility does not create a new approval step.

1. Company exposure: private customer details, unresolved security information, unpublished deals, competitor remarks, and confidential coordinates whose disclosure is unnecessary or unauthorized.
2. Personal exposure: personnel information, unsupported judgments about named colleagues, private motives, and incidental working records that do not belong with these recipients.

For internal sharing, internal key names can stay. Tighten claims whose scope or date is stated more strongly than the record supports, such as a month written as fact when only the quarter is confirmed. Genuine past failures are not deleted because they may have been fixed since.

### People

| Keep | Change |
| --- | --- |
| Real names on facts: owner, author, speaker, decision maker | Sentences that read as evaluations of attitude, ability, or workload, rewritten as structural statements ("검토 요청이 한 채널에 몰려 있습니다" rather than "이 팀은 응답이 느립니다") |
| Customer company names and internal ticket numbers, because the person acting on the item needs them | Names of individual customer contacts |
| Unaddressed security items, flagged with a handling notice | Coordinates that would let a reader find the confidential data itself |

Return findings to their original source so the document is not the judge ("지난 분기 보고서는 이 구간을 진단했습니다" rather than "검사한 표본 대부분에 결함이 있었습니다"). Where two conventions exist, describe both. Keep open factual questions when they change interpretation. Add action guidance only when the request or evidence supplies the action. If the agreed publication workflow requires review by named colleagues, honor that requirement. Their mention alone does not require a review round or authorize contacting them.

### Sensitive content

- Credentials and secrets, including cookies and tokens visible in screenshots; write `[REDACTED]`.
- Coordinates of confidential data: repository names, file paths, Notion page titles, channel names that lead to it.
- Author, role, and result figures of submissions under anonymous review.
- Reproducible bypass values: user-agent strings, system prompt text, OAuth client identifiers, working attack prompts or payloads. Technique family, counts, sources, and judge design may stay; CBRN operational detail never does.
- Personal HR information: probation, employment terms, leave.
- Competitor mockery quoted with the speaker's name.
- Uncensored-model techniques and offensive tooling detail in defensive documents.

### Depersonalize

- Second-person address and "about my role" framing ("<이름>님께 제안된", "<이름>님의 역할은") become role language: "검토 담당자", "운영 담당 엔지니어".
- Wall-clock timestamps that reveal when the author worked become relative gaps; a sentence naming the specific small models used becomes a role description. Generalize; do not leave a hole.
- Session narration ("복구했다", "헤드리스", "폴백", "빌드 스크립트") moves to a methods appendix in the reader's language, or goes.
- Statements that assume the conversation ("이번 주", "오늘 푸시", "1차 리포트 대비") become statements verifiable inside the document. [Conversation residue](authoring-and-revision.md#remove-conversation-residue) names the home for rejected options, change narration, reassurance, and internal plan identifiers.
- Keep removed confidential coordinates in their authorized source. Create or send a separate handoff only when requested; redaction itself does not authorize contacting a security owner.

For repeated publication of a redacted derivative, a source-to-output script can keep edits reproducible. Use checks for known secrets, disallowed links, or specific redactions rather than banning every personal name or local reference regardless of audience. Inspect the resulting copy before delivery. Use a private staging copy or a separate review round when the agreed workflow or an unresolved disclosure question needs it. If text corrupts during publication, stop the batch and repair the artifact.

## Delivery

Inspect the actual destination after rendering, conversion, or publication: complete content, visible row and column labels, readable cells, list hierarchy, equations, figure size and numbering, captions, and working source links. For a collapsible document, check the initial view and representative expanded content. Distinguish a retrieved-content check from a visual check, and never report a rendered view as inspected when only its source was read. Re-fetch what was published and diff it against the source; a Notion replacement of 192 items once applied only 100 silently.

Preparing a document does not by itself authorize sending or publication. An explicit request to send, publish, or update a shared copy supplies authorization within that audience and destination; reuse it. Ask only about a consequential missing recipient, exposure, or authority, and finish the authorized preparation first so the user can review the concrete result. Return the artifact, its path or URL, and any material delivery limitation. Preserve a source copy when creating a redacted derivative; edit the original when that is the requested work.
