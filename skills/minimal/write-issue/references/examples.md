# Worked Drafts

Read this when the right shape for a draft is unclear. Every example is invented. Each shows the draft, the fields, and the one-line assignee decision, followed by why it is shaped that way. Copy the judgment, not the wording: the team's own convention still wins.

## Contents

- From an agenda to a usable result
- Consolidating a fragmented portfolio
- Bug relayed from chat, ownership ambiguous
- Request to another team
- Wrong output in data or an evaluation
- Uncertain or research work, with its closing note
- Splitting one large in-progress issue
- Korean noun-phrase outline
- Overview table and a figure, with a long log cut instead of collapsed
- Local and server-only material with a pile of links

## From An Agenda To A Usable Result

A team wants better help-center search. Their records contain collected queries, several relevance-label revisions, loader changes, run notes, and candidate scores. The reader needs to know whether to change the search configuration and what evidence will support that choice. These are synthetic examples; their names, values, and URLs are invented.

The existing project gives the agenda:

```markdown
Project: Choose search configuration for help-center answers

Support agents need the correct help article while answering a customer. Compare the current search configuration with the proposed alternatives, then recommend a configuration that improves retrieval within the 250 ms p95 search budget.
```

That purpose leads to a concrete need: every candidate must face the same queries with the same relevance judgments. The dataset issue makes that result usable:

```markdown
Title: Query set for reproducing help-center search failures

Capture searches that return the wrong help article or miss a relevant one so the team can compare configurations on the same failures.

- Deliver the reviewed query set with the index snapshot, expected relevant articles, and a short rationale for each relevance judgment.
- Include queries that already retrieve the right article so a change can be checked for regressions.
- Dataset and labeling guide: https://data.example.com/help-search/revisions/4 (search team access).
```

Fields: the existing search project, with the author assigned because they own the dataset work. The draft uses no new milestone or parent.

Why these details: the first sentence makes the dataset's use explicit. The snapshot and judgments allow a comparable run; the regression cases explain a design choice; the link is where the next person gets the input. A current case count would be useful if it established the agreed coverage or delivery size. Counts from each intermediate revision, how queries were copied from chat, and every loader PR do not help someone use this result.

The comparison issue states what can be done with the evidence. Once the comparison is complete, its body reads:

```markdown
Title: Search configuration recommendation for help-center answers

Adopt the hybrid configuration for the next rollout: recall@5 improves from 0.76 to 0.84 on the reviewed query set, with p95 search latency of 180 ms against the 250 ms budget.

- Comparison uses the same query set and index snapshot for both configurations.
- Queries containing product codes still retrieve the wrong article. Keep those queries on exact-match lookup for the rollout and track the retrieval fix separately.
- Comparison table and run settings: https://docs.example.com/help-search/comparison
```

The outcome comes first, followed by the conditions that make the comparison interpretable and the remaining defect that changes the rollout. Definitions of every metric, a list of checks not performed, and the history of each experiment would dilute this decision. The unresolved product-code defect stays because someone must act on it. Neither issue needs a progress comment repeating its rewritten body.

## Consolidating A Fragmented Portfolio

The user asks to reorganize the issues in that search project. The current list reflects editing sessions: query export, label cleanup, index pinning, candidate shortlist, run configuration, parser repair, comparison dashboard, and product-code retrieval. Read their contents before choosing which records survive.

The resulting portfolio has three independently useful outcomes in this example:

| Existing work | Resulting issue | Result someone can use |
| --- | --- | --- |
| Query export, label cleanup, index pinning | Query set for reproducing help-center search failures | Runnable comparison input |
| Candidate shortlist, run configuration, parser repair, comparison dashboard | Search configuration recommendation for help-center answers | Supported rollout choice |
| Product-code retrieval defect | Exact-match lookup for product-code searches | Verified routing fix |

Keep the existing project as the home. Reuse the best matching dataset and comparison issues, rewrite their bodies around the results above, and carry forward the current dataset revision, comparison conditions, and useful result links. Their small implementation chores remain in those issues or the linked PRs. Resolve redundant records through the tracker's supported relation or duplicate status when the reorganization request includes that authority.

Keep the product-code fix separate because the owner can deliver and verify it independently of choosing the general search configuration. If the parser repair instead prevents any comparison from completing and another engineer owns it, retain it as a separate blocker linked to the comparison. Its importance comes from that concrete handoff, not from the fact that it changes code.

This example happens to leave three issues. There is no target count and no sequence of phases: the dataset can be useful before a recommendation, and the product-code fix can proceed independently. Preserve existing completion evidence and known active work; grouping issues does not establish that they have started or finished.

Why the consolidation works: the titles now tell a teammate what the project will produce and what each result enables. The smaller list is a consequence of combining work with the same completion decision. Distinct outcomes and actionable defects remain visible.

## Bug Relayed From Chat, Ownership Ambiguous

The user pastes a message from a support colleague and says "can you file this?". The user is not on the payments team.

```markdown
Title: `payment.succeeded` webhook delivered three times after a 503

> "Merchant says they got the payment.succeeded webhook three times for one
> charge after their endpoint returned a 503. They shipped the order three times."

Reported by support in the payments help channel: https://chat.example.com/archives/C042/p1726555

- Where: webhook delivery worker, production, one merchant so far
- Observed: three deliveries for one charge after a single 503. Compare the event ids to determine whether these are retries the receiver could deduplicate.
- Expected: one delivery per event, or retries that reuse the event id so receivers can deduplicate
```

Fields: label `bug`, which the team already uses. No priority, cycle, or status set.

Assignee: left empty. The delivery worker belongs to the payments team and this is a report for their triage.

Why: the title states the symptom, because a report filed for another team's triage should not presume the fix. The reporter's words and conversation preserve the reported behavior. Checking event ids distinguishes a delivery defect from receiver deduplication, so that uncertainty changes the investigation. The issue needs no background about how webhooks work.

## Request To Another Team

The notifications team is moving email sending out of the monolith into a new service and needs the platform team to create a few things. The platform team never saw the migration. A first draft, filed with the template the platform team uses for its own engineering tickets and assigned to one of its engineers:

```markdown
Title: [Request] MSV infra setup

## Background
As part of the MSV migration we analysed current mail volume, reviewed the SMS sender setup, checked topic naming rules, and confirmed the image builds. We will use a dedicated relay for mail-sender.

## Request
Please provision the topics, the SA, and the relay limit for mail-sender by Thursday, 2026-11-04.

## Notes
- The relay limit might possibly need to be higher; we are not fully sure.
- As noted above, we need topics, an SA, and the relay limit.
```

The rewrite:

````markdown
Title: Queue topics, service account, and relay limit check for the new mail-sender service

**Summary**
- We are moving email sending out of the monolith into a new `mail-sender` service, the same way SMS sending moved: https://tracker.example.com/platform/requests/212
- We ask for 2 queue topics, 1 service account, and 1 relay limit check.

```mermaid
flowchart LR
  mono[Monolith] --> req[mail-requests topic] --> svc[mail-sender] --> relay[Outbound mail relay]
  svc --> res[mail-results topic]
  class req,res,relay ask
  classDef ask fill:#fef9c3,stroke:#a16207,color:#713f12
```
Flow of one email. Requested: the two topics and the relay limit check.

**What mail-sender is**
- A service that reads email requests from a queue and hands them to the outbound relay, so the monolith stops sending mail itself
- It touches your systems in two places: the queue cluster and the outbound relay
- Why now: the monolith's mail code blocks its framework upgrade, planned for December 2026

**What is ready**
- Service code and image, passing the staging test suite: https://git.example.com/notify/mail-sender
- Deployment manifest, reviewed by our team, in that repository under `deploy/`

**What we ask**
1. Two queue topics
   - `mail-requests` and `mail-results`, 3 partitions each, 7-day retention
   - Reason: the same layout as the SMS topics, so your existing alerts apply
2. One service account
   - `mail-sender`, with produce and consume on both topics and send on the relay
   - Reason: the service should not reuse the monolith's credentials
3. Relay limit check
   - Can the relay take 200 messages per second from `mail-sender` at peak?
   - Reason: the answer decides our next request, below

**After you finish, we do**
- Deploy `mail-sender` to staging and send 1% of mail through it for a week
- If the relay takes 200 messages per second, we will ask to route all mail through it; otherwise we will ask for a second relay.

**Schedule**
Would Wednesday, 2026-11-04 work for items 1 and 2? If not, tell us what suits you and we will adjust.
````

Fields: filed through the platform team's request form, the one the SMS sender's request used. No priority or cycle; their triage sets them.

Assignee: left empty. The platform team triages its own requests.

The companion chat message, sent because the user asked for one:

```markdown
Request for the platform team: queue topics, a service account, and a relay limit check for the new mail-sender service, following the SMS sender.
- 2 topics and 1 service account; 1 question on relay capacity
- Code and image are ready; we deploy to staging once these exist
- Would Wednesday, 2026-11-04 work?
https://tracker.example.com/platform/requests/240
```

In a Korean tracker the same ask keeps its outline and short labels, and its sentences end politely:

```markdown
1. Queue topic 2개 생성 요청드립니다
   - 이름: `mail-requests`, `mail-results`
   - 설정: 각 partition 3개, 보존 7일
   - 이유: SMS 발송과 같은 구성이라 기존 alert를 그대로 쓰실 수 있습니다

일정: 2026년 11월 4일 수요일까지 1, 2번이 가능하실까요? 어려우시면 편하신 날짜를 알려주세요. 맞춰서 진행하겠습니다.
```

Why: the rewrite answers the receivers' questions in the order they arise, from what is wanted and how much, through what the thing is, what exists, and what to create under which names, to what happens next and when. Each ask carries the names they will type and one reason. The first draft stated an undecided relay choice as the plan; the rewrite makes it depend on their answer. The deadline became a question with a fallback, and its weekday was computed with a tool, since the first draft's Thursday was a Wednesday. The coined "MSV" and "SA", the list of what was checked, the hedge, and the repeated ask are gone. The request follows the form the platform team accepted before rather than the template for its internal tickets, and the assignee is left to their triage.

## Wrong Output In Data Or An Evaluation

The user is running their own evaluation, found a systematic error, and will fix it. Because the fix is the author's own, the title names the target and the action instead of the symptom.

```markdown
Title: Fix day and month swap in receipt date extraction for en-GB receipts

| Input | Observed | Expected |
| --- | --- | --- |
| `Date: 03/04/2026` (locale en-GB) | `2026-03-04` | `2026-04-03` |

- 41 of 500 en-GB receipts in the evaluation set are affected, all with a day of 12 or lower
- Dataset revision: https://data.example.com/receipts-eval/revisions/18
- Parser settings: `doc-extraction: configs/date_parser.yaml` on `main`
```

Assignee: the author. It is the author's own evaluation work.

Why: one real input with observed and expected output says more than a description of the error class. The dataset revision is pinned, and the path names its repository and branch.

## Uncertain Or Research Work

The user wants to find out whether a reranker is worth its latency, and has named the candidates, the 1,200-query long-query set, the two metrics, and the shared experiment log. Had the user not supplied those, the draft would leave them out and the report would ask for them.

```markdown
Title: Reranker comparison table for long queries

Question: does a cross-encoder reranker raise recall@5 on queries over 30 tokens enough to justify its latency?

- Candidates: the current retriever alone, and with each of two cross-encoder rerankers
- Same 1,200-query long-query set and the same index snapshot for every run
- Deliverable: one table of recall@5 and p95 latency per candidate, with a recommendation
- Experiment log: https://docs.example.com/d/reranker-long-queries
```

Assignee: the author. No estimate, no sub-issues.

Closing note, added when the issue is closed:

```markdown
- Outcome: the larger reranker raises recall@5 from 0.71 to 0.78 at +140 ms p95. The smaller one is within run-to-run variation of the baseline.
- Decision: adopt neither for now, because the latency budget is 100 ms
- Table and runs: https://docs.example.com/d/reranker-long-queries
```

Why: the title names a deliverable, so the issue can be closed whatever the answer turns out to be, including "neither". The reasoning and the runs live in the experiment log. The issue carries two or three lines of outcome and the link.

## Splitting One Large In-Progress Issue

"Migrate the evaluation harness to the new runner" has been in progress for two weeks and the user asks to split it. Three separate lumps have shown up in the work so far.

Parent: reused as the record of the final outcome. Its existing purpose is already clear, so the split needs only the child relations.

Sub-issues created:

- Port dataset loaders to the new runner
- Check metric parity between the old and new runner on the regression set
- Add the new runner to the nightly CI job, blocked by the loader port (set as a relation, not written in the body)

Not created:

- "Finish the migration". It names the parent's outcome again and has no separate work of its own.
- "Write migration docs". No separate audience or handoff has been identified. The setup notes needed to use the new runner stay with the migration; a distinct documentation issue would need a concrete result of its own.

Assignee: the author on all three, set explicitly on each sub-issue. The user is doing this work.

Report line: "Created the loader, parity-check, and nightly-job sub-issues under the existing migration issue. The parent remains in progress; the new children are not started because the current record does not identify which is active."

Why: each sub-issue has work that can be verified separately. "Finish the migration" only repeats the parent. A real cutover with a date and rollback steps could be a distinct action once those requirements are known. Creating children does not supply evidence that each one is active.

## Korean Noun-Phrase Outline

A task the author will do, in a Korean tracker. The title is a noun phrase naming the target and the action. Parallel facts and tasks end in a noun or read `label: value`, and established English terms stay in English. Mechanisms, conditions, and causes use complete sentences when the relationship needs explanation.

```markdown
Title: 결제 webhook 5xx 응답 시 재시도 추가

- 대상: `payments-api`의 webhook 발송 worker
- 현상: 수신 서버의 503 응답에 재시도 없이 실패 처리
- 작업
  - 5xx와 timeout에 exponential backoff 재시도 3회
  - 재시도 소진 시 dead-letter queue 적재
  - 재시도 횟수 metric 추가
- 제보 원문 (지원팀 채널): https://chat.example.com/archives/C042/p1726555
```

The link line says what the link is. A bare `참고:` followed by a URL would not.

The same observed condition may use a complete sentence when explaining the failure path:

```markdown
worker는 수신 서버가 503을 반환하면 재시도 없이 webhook 발송을 실패 처리한다.
```

Avoid this for proposed work because it claims the retry and metric changes are already complete:

```markdown
수신 서버가 503을 반환했을 때 재시도를 하지 않고 실패 처리했습니다. 그래서 재시도 로직을 추가했고 metric도 넣었습니다.
```

The defect is the unsupported completion claim, not the past-tense ending. A closing note may use past tense for a supported result and complete sentences for the conditions under which it holds.

## Overview Table And A Figure, With A Long Log Cut Instead Of Collapsed

The author is moving three nightly evaluation suites to a new runner and wants one issue a teammate can take in at a glance. The content is the same three fields over three suites, and the hand-off between the runner and the result store is what people keep getting wrong. The author also has a 400-line log of the failing upload and first thought of folding it into the issue.

```markdown
Title: Move nightly evaluation suites to the batch runner

Nightly runs hit the 6 hour limit on the old runner twice last week.

| Suite | Nightly runtime now | State on the new runner |
| --- | --- | --- |
| Retrieval | 2 h 10 min | Runs, results match |
| Summarization | 3 h 40 min | Runs, 2 metrics differ |
| Long context | 5 h 50 min | Fails at result upload |

![Runner, queue, and result store](./nightly-flow.png)
Figure: the batch runner writes results to the queue and a separate worker uploads them to the result store, so an upload failure does not fail the run.

- Find why ROUGE-L and BERTScore differ on Summarization (tokenizer version is the first suspect)
- Fix the upload step for large result files: the upload worker times out after 300 s on the 2.3 GB file that Long context produces, on all three retries
- Switch the nightly schedule once all three suites match
```

Fields: no estimate. The figure is attached with the tracker's upload function, so the image reference resolves for every reader.

Assignee: the author. It is the author's own migration.

Why: the table comes right after the purpose sentence because three suites share three fields, every column has a header, the first column names each row, and no cell is longer than a few words. The figure earns its place because the hand-off it shows is the part readers misunderstand, and one visible line says what it shows. The log is cut, not collapsed: the one thing it establishes, a 300 s timeout on a 2.3 GB file on every retry, fits in the task bullet, and a shorter issue beats a folded one. A collapsed block would be justified only if whoever takes the fix had to read the full log and it had no shared home; then its summary line would carry that same conclusion. Had there been one suite, a sentence would replace the table; had the flow been a straight line, the figure would be dropped.

## Local And Server-Only Material With A Pile Of Links

The author analysed webhook latency and asks for an issue, saying "add these links". The report and plan are on the author's machine, the run output is on a batch server the team cannot log in to, and the links are a handful of loosely related pages. A first draft that points at all of it and states nothing:

```markdown
Title: Webhook latency

Details in the report: research/webhook-latency/REPORT.md
Plan: .plans/webhook-retry.md
Results: /data/runs/webhook-latency/2026-09-02/
Dashboard: http://10.0.3.17:3000/d/webhooks
An agent session ran the latency script in a local worktree; see the session notes.

Related:
- https://git.example.com/acme/payments-api/pull/398
- https://git.example.com/acme/payments-api/pull/412
- https://docs.example.com/d/queue-design-2024
- https://docs.example.com/d/webhooks-overview
- https://chat.example.com/archives/C042/p1726001
```

Running the check on each reference:

| Reference | Claim or action it supports | Opens for readers | Result |
| --- | --- | --- | --- |
| `research/.../REPORT.md`, `.plans/...` | The findings, but it stands in for them | No, author's machine only | Facts moved into the body, path removed, stated as not yet shared |
| `/data/runs/...` | The measurements | No. A bare path names no host or access condition, and the team cannot reach that server | Same |
| Dashboard on `10.0.3.17` | Lets a reader check the latency number | Only on the VPN | Kept, with the access condition beside it |
| Pull request 412 | The change the regression is attributed to | Yes | Kept, and the sentence says what it is |
| Pull request 398, two background documents, chat thread | None. Merely related | Yes | Dropped |
| "An agent session ran..." | None. Authoring context | Not applicable | Dropped |

The corrected draft:

```markdown
Title: Retry payment webhooks on 5xx responses

- p95 delivery latency rose from 0.8 s to 4.2 s after the queue change in pull request 412 (https://git.example.com/acme/payments-api/pull/412), measured over 7 days of production logs from 2 September
- Deliveries that receive a 5xx are never retried. They are 3.1% of all deliveries in that window.
- Live latency panel, to check the first number: http://10.0.3.17:3000/d/webhooks (VPN required)
- The analysis notes and the raw run output exist only on the author's machine and the batch server. There is no shared copy yet.
```

Shown to the user together with the draft before posting, because the check dropped links the user asked to include: "I put the two numbers into the issue and said plainly that the report and run output have no shared copy yet; tell me if you want them moved somewhere shared first. I dropped four links (pull request 398, two background documents, the chat thread) because no statement in the issue depends on them. I kept the dashboard with its VPN condition."

Why: the issue now commits to its findings in its own text, so a reader who opens nothing still knows what was found. Each remaining link is named and says why one would open it, and every sentence still reads correctly with its link removed. What is not shared is stated instead of hidden behind a path. The date and measurement window stay because a reader needs them to interpret the numbers; which agent ran what does not.
