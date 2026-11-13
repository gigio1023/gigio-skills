# Synthetic Examples

Use these contrasts to diagnose why a sentence or table is less useful, then keep the operation the stronger version demonstrates. Every example is independently constructed: its names, numbers, and events are not measurements of a real system or anonymized company records, and they are never copied into a real document. “Before” is the passage being repaired, not necessarily the complete input. Each “Supplied teaching facts” block gives additional facts available to that example's writer. Use those facts to repair unsupported claims or add a needed explanation; never infer them from the wording alone. When only the before passage is available, preserve its uncertainty and seek missing evidence instead.

## Contents

- Structural repairs: [paragraph table](#paragraph-table), [table split](#table-split), [heading and cell phrases](#heading-and-cell-phrases), [genre transfer](#genre-transfer), [row identity](#row-identity), [internal aliases](#internal-aliases), [list hierarchy](#list-hierarchy).
- Prose rewrites: [observation and explanation](#separate-an-observation-from-its-explanation), [broad promise](#turn-a-broad-promise-into-an-observable-test), [alternative](#compare-an-alternative-fairly), [failure sequence](#keep-the-failure-sequence-without-blame), [untested condition](#name-the-untested-condition-readers-would-assume), [definition](#define-the-measurement-not-the-familiar-word), [Korean relations](#restore-the-relation-in-korean).

## Structural repairs

### Paragraph table

**Supplied teaching facts:** Both latency measures start at request arrival. In this teaching replay, direct indexing became searchable and acknowledged at 800 ms. Queued indexing acknowledged after durable enqueue at 80 ms and became searchable at 3 s.

**Reader:** an engineer comparing two document-indexing configurations.

**Before:**

| Item | Content |
| --- | --- |
| Method | Documents are indexed either during the upload request or later by a worker. The second configuration writes a durable job first. |
| Result | Direct indexing takes 800 ms before acknowledging upload. Queued indexing takes 80 ms to acknowledge and 3 seconds to make the document searchable. |
| Meaning | Queued indexing acknowledges earlier, but users must wait for the worker before their document appears in search. |

The rows are different parts of an argument; the grid compares nothing.

**After:**

**Upload and search latency**

| Configuration | Upload acknowledgment | Search availability |
| --- | ---: | ---: |
| Direct indexing | 800 ms | 800 ms |
| Queued indexing | 80 ms | 3 s |

Queued indexing acknowledges the upload after saving a durable job. A worker then updates the search index. This shortens the upload wait while delaying search availability.

The table compares values; the paragraph explains why they differ. No paragraph explaining how to read the columns is needed.

### Table split

**Reader:** a team selecting an export path for two independent needs: output behavior and maintenance responsibility.

**Before:**

| Path | Output and delivery | Scheduling and ownership |
| --- | --- | --- |
| On demand | CSV is generated when requested and returned by HTTP; each export covers the selected account. | No schedule is used; the API team maintains the handler. |
| Scheduled | A daily Parquet file covers all accounts and is written to object storage. | The scheduler runs nightly; the data team maintains the worker. |

**After:**

**Export behavior**

| Path | Format | Delivery | Coverage |
| --- | --- | --- | --- |
| On demand | CSV | HTTP response | Selected account |
| Scheduled | Parquet | Object storage | All accounts |

**Maintenance**

| Path | Trigger | Owner |
| --- | --- | --- |
| On demand | Request | API team |
| Scheduled | Nightly schedule | Data team |

Stable path names connect the views. The second table earns its place only when maintenance affects the choice.

### Heading and cell phrases

**Supplied teaching facts:** The retry policy permits at most three retries. The operation is retried when its result remains unacknowledged at lease expiry.

**Before heading:** “Why does the worker retry the same job?” **After:** “Job retries”

**Before cell under “Retry policy”:** “The worker retries a failed job at most three times.” **After:** “Up to 3 retries”

**Explanatory sentence:** “The worker retries the job when the result is not acknowledged before the lease expires.”

Headings and cells stay compact while the sentence supplies the operation and condition. Do not apply a complete-sentence prose rule to labels. In Korean, use “작업 재시도” as the heading and “최대 3회” in the cell, and keep the relation in prose: “워커는 리스가 만료될 때까지 처리 결과가 확인되지 않으면 작업을 다시 시도한다.”

### Genre transfer

**Synthetic input:** the queue records a job's assigned worker in a lease. Reassignment must wait until that lease expires. In the observed incident, an expired lease was still treated as active and blocked reassignment. The operator reset the lease, another worker received the job, and that worker completed it. Delayed acknowledgements from the original worker are a design possibility that the proposal must handle.

**Factual incident record:**

- **Observation:** Job retained an expired lease.
- **Response:** Operator reset the lease.
- **Result:** Another worker completed the job.

**Technical explanation:** The queue records the worker assigned to a job in a lease. When that worker stops, the lease must expire before the queue assigns another worker. If reassignment still treats the expired lease as active, the job remains blocked.

**Proposal:** Allow reassignment after lease expiry and give each assignment a new generation number. Reject acknowledgments from older generations so a delayed worker cannot complete a reassigned job. A longer lease alone would delay recovery without handling stale acknowledgments.

The record is enough for its reporting task. The explanation uses the supplied mechanism; the proposal introduces a design change and explains its intended effect. The proposed generation number is not reported as an existing implementation fact. Reusing the incident bullets for all three would remove necessary content.

### Row identity

**Supplied teaching facts:** The source matrix defines the first row as immediate notice and the second as one scheduled message. These labels were lost in formatting; their meaning is not inferred from the Yes/No values.

**Before:** the columns name delivery options, but blank row headings leave the reader to infer that the rows are requirements.

| | Live updates | Daily digest |
| --- | --- | --- |
| | Yes | No |
| | No | Yes |

**After:**

| Requirement / Delivery option | Live updates | Daily digest |
| --- | --- | --- |
| Immediate notice | Yes | No |
| One scheduled message | No | Yes |

The corner heading names both dimensions, and each row states the requirement assessed. If row labels existed but their dimension was unnamed, repair the header alone.

### Internal aliases

**Supplied teaching facts:** The dataset is a labeled support-ticket collection with internal ID `review-set-r3`. Its metadata records both human review and automated rules as label sources; no validation process is documented.

**Before:** “Run the classifier on review-set-r3. This is our gold-standard dataset.”

**After:** “Evaluate the classifier on the labeled support-ticket dataset, internal ID `review-set-r3`. Labels come from a mix of human review and automated rules.”

The source establishes mixed label origins, not a validation process. The edit states the role and keeps the lookup ID without claiming that every label was validated. Use “labeled dataset” afterward, and omit the ID when readers will not look it up.

### List hierarchy

**Supplied teaching facts:** The rollout requirements define phrase queries as preserving word order and category filters as excluding other categories. The pilot starts after correctness checks pass; pilot traffic supplies the latency measurement. Incomplete indexed results trigger rollback.

**Before:**

- Search rollout: build the index, check phrase queries and category filters, compare incremental updates with a full rebuild, enable a pilot, check latency, and disable the pilot if results are incomplete.

**After:**

- Index correctness
  - Build the initial index.
  - Compare incremental updates with a full rebuild.
  - Check query behavior.
    - Phrase queries preserve word order.
    - Category filters exclude other categories.
- Pilot rollout
  - Enable search for the pilot group after correctness checks pass.
  - Measure request latency under pilot traffic.
  - Disable the pilot if indexed results are incomplete.

The hierarchy separates two workstreams, their actions, and the cases within one check; the third level exists only for that subdivision. Causal reasoning may still read better as a paragraph.

## Prose rewrites

### Separate an observation from its explanation

**Supplied teaching facts:** The replay with caching issued fewer remote reads and had lower latency. It did not isolate network wait from server-side work. These observations support a narrower claim than the draft's root-cause assertion.

**Before:** “The cache eliminated the bottleneck and proved that network traffic was the cause.”

**After:** “With the cache enabled, the replay issued fewer remote reads. The run did not measure network wait separately, so it does not establish whether the latency change came from network wait or server-side work.”

The second sentence names the competing explanations that affect the conclusion. Do not weaken the observation with vague hedges, or treat the missing measurement as evidence that neither explanation holds.

### Turn a broad promise into an observable test

**Supplied teaching facts:** In this independently synthetic completed test, the input contained 500 records. The worker stopped after writing output but before acknowledging. Reassignment wrote the same batch ID again and replaced the earlier output; the final output contained one row per input record. These are supplied test results, not predictions of the proposed test.

**Before:** “The pipeline guarantees exactly-once processing.”

**Test first:** stop the worker after it writes output and before it acknowledges, let the coordinator reassign the batch, and count output rows per input record.

**After:** “When the worker stopped between the output write and its acknowledgment, the reassigned batch left one output row for each of the 500 records; the second write replaced the first under the same batch ID.”

The promise becomes behavior a reader can check, and the sentence reports that behavior. Design the test before writing the result. If it has not run, state the check that remains instead of the promise.

### Compare an alternative fairly

**Supplied teaching facts:** Consumers already use the managed queue's delivery and retention interface. The selected configuration persists pending retries across restart. An in-process queue avoids a network call per message but loses pending work on restart unless separate persistence is added. This decision requires retries to survive restart.

**Before:** “A managed queue is the best choice because it is scalable, reliable, and easy to maintain.”

**After:** “Use the managed queue for the retry log because the consumers already use its delivery and retention interface and pending retries must survive a restart. An in-process queue avoids a network call per message, but meeting the same durability requirement would add a second persistence mechanism.”

The losing option keeps its real advantage, and the choice follows from a stated requirement. The reader can name a change that would reopen the choice: if retries could be dropped on restart, an in-process queue could meet that requirement without persistence. Other costs would still affect selection. Verify delivery and retention behavior before writing this rationale.

### Keep the failure sequence without blame

**Supplied teaching facts:** The routing log places a route change before backend readiness completed. Requests then reached that unavailable backend. The documented procedure has no readiness gate at that step, and responses resumed after the route was reverted.

**Before:** “An operator mistake caused a major outage, showing that our process needs improvement.”

**After:** “Requests reached an unavailable backend after the rollout replaced the routing rule. The rollout log places the route change before the backend's readiness check completed; the procedure has no gate between those steps. Reverting the route restored responses.”

The rewrite names the sequence and the missing control instead of a person. Event times come from the records; when the team learned each fact is investigation time and stays separate. A real postmortem distinguishes a confirmed sequence from a suspected cause. “Gate the route change on backend readiness and exercise the failed-readiness path” is an action; “improve the process” is not.

### Name the untested condition readers would assume

**Supplied teaching facts:** The reader is deciding whether to launch. The recorded configuration check passed, and no load test has run. The document is a static record; that format does not itself establish whether any check passed.

**Before:** “This document is a static snapshot rather than a live operational dashboard. It includes prepared and verified items but does not establish production readiness.”

**After:** “The configuration check passed. The service has not been run under load.” In Korean: “설정 검사를 통과했다. 부하 테스트는 아직 실행하지 않았다.”

Keep the second sentence when a reader could otherwise act as if load behavior had been tested, for example in a launch decision. Delete it when load is not part of the reader's decision; a list of everything the author did not check is cover, not a limit.

### Define the measurement, not the familiar word

**Supplied teaching facts:** The metric specification starts the timer at enqueue, ends it at the final response, and includes retry time. The generic before passage does not supply those boundaries.

**Before:** “Latency is the time a request takes. The metric must be interpreted with awareness of its definition.”

**After:** “Latency is measured from enqueue to final response, including retries.”

Keep this definition when it differs from what the intended audience would assume. If a table heading or methods section already carries the boundary, do not repeat it.

### Restore the relation in Korean

**Supplied teaching facts:** The implementation description says that the worker sends the batch acknowledgement only after saving all output. A retry may encounter already saved output. The design requirement is that writing the same batch again must not change the result. The short goal statement alone does not establish this behavior or requirement.

**Before:** “재시도 안정성 확보 및 처리 일관성 보장.”

**After:** “워커는 출력을 모두 저장한 뒤에 batch 처리 완료 응답인 ack를 보낸다. 재시도하면 이미 저장된 출력이 남아 있을 수 있으므로 같은 batch를 다시 써도 결과가 달라지지 않아야 한다.”

The rewrite uses the supplied behavior to explain who acts and in what order, then states the supplied consistency requirement. It uses Korean verbs for ordinary actions. Without those facts, revise the goal as a goal or ask for the missing mechanism; do not turn the short phrase into an implementation claim.
