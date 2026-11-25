# Writing sources

These are maintenance pointers for the pack authors, not runtime references: `copydesk` does not load this file, and it serves only when the skill's techniques are revised. The skill links CC BY-NC-ND sources rather than republishing them, and it keeps every source claim attributed. Teaching examples' invented names and numbers, whether in the skill or in a source such as the SRE example postmortem, are never copied into real documents.

## English clarity integration

Copydesk's [English clarity](../skills/minimal/copydesk/references/english-clarity.md) adapts selected principles from Dustin Yuchen Teng's [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), inspected as version 0.4.0 on 2026-10-06. The package retains the [MIT notice](../skills/minimal/copydesk/LICENSE.asd-ste100). The useful principles are explicit actors and references, consistent terminology, clear instruction conditions, and preservation of modality and technical meaning.

This is an attributed synthesis. It does not import the third-party checker, automatic strict mode, hard sentence limits, or ASD's dictionary. Similar verbs can denote distinct actions, and an adjective can be part of a domain term. Copydesk therefore keeps schema validation, signature verification, receipt confirmation, and robust regression distinct. The external skill remains independent and is not modified by this integration. Official ASD compliance is outside the package's claim; a task requiring it needs the authorized standard and dictionary.

The earlier percentage-of-STE policy is retired. Korean follows natural Korean grammar, and English clarity work preserves useful clauses, tense, and uncertainty. The ordinary path starts with reader purpose, semantic fidelity, and [finished examples](../skills/minimal/copydesk/references/finished-examples.md). Pattern evidence is a targeted diagnostic aid rather than a routine reading requirement.

## Anti-slop survey

The [November 2026 anti-slop survey](anti-slop-survey/README.md) records the public skills, linters, tells lists, triage policies, and papers read for copydesk's structure checker and one-home rule, with pinned revisions, licenses, and a checker evaluation on real documents.

## Close readings

Use this catalog to select and closely read a public technical exemplar. The value is in the writing operation: how the author states a fact, explains a mechanism, introduces a comparison, qualifies a result, or justifies a choice. A company name or a “technical report” label does not make every sentence worth copying.

The sources below were inspected on 2026-09-15. The package contains original synthesis and small illustrative phrases, not copied reports or image collections. Source claims remain attributed; reading a benchmark is not reproducing it. The dry register is a default for technical reports, not every genre or a claim that every cited source recommends the same voice. Reader-based information selection applies across genres.

### Google developer documentation: voice without bureaucratic prose

Source: [Voice and tone](https://developers.google.com/style/tone), particularly the body guidance, avoidance list, and informal/right/formal examples.

Read how the examples preserve the operation while removing either enthusiasm or unnecessary formality. An API is described by what it lets a caller do, not by praise and not by a chain of abstract nouns. The guidance prioritizes useful information for a reader in a hurry and discourages placeholder framing such as “please note.” Use concrete subjects, direct instructions where the genre is procedural, and consistent terms.

The source explicitly favors a conversational, friendly voice rather than a super-dry one. This skill retains directness and semantic completeness while choosing a more restrained register for technical reports. Do not misattribute that preference to Google, copy the page's generated summary as language authority, or turn its English examples into rules against natural Korean syntax.

### Google engineering documentation: audience, decisions, and canonical sources

Source: Tom Manshreck's [Documentation chapter in Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch10.html), “Know Your Audience,” “Documentation Is Like Code,” and “Design Docs.”

Read the difference between a design document for decision makers, a tutorial for a newcomer, and a reference for lookup. The design-doc discussion names implementation strategy, key decisions, and alternatives with strengths and weaknesses. The documentation-ownership discussion explains why competing editable documents become inconsistent.

Transfer the reader-specific depth and the record of why a design was chosen. Keep an existing source of truth and update the document with the system it describes. Do not import Google's review organization or approval dependencies into an unrelated project. The chapter's prose, examples, and book layout are not bundled; its public license is CC BY-NC-ND 4.0, so link to the original rather than republishing a rewritten chapter or its assets.

Supporting source: [Google's Markdown style guide](https://google.github.io/styleguide/docguide/style.html), “Minimum viable documentation,” headings, links, and tables. The useful details are descriptive headings, manageable link text, and tables whose rows share real dimensions. Its Gitiles-specific features and fixed-column wrapping are not this package's format policy; preserve the destination renderer and repository conventions.

### Kubernetes KEP template: make a design operationally reviewable

Source: [KEP template at revision 6ab9bf717d1228928740bdbfe761b6e62b870902](https://github.com/kubernetes/enhancements/blob/6ab9bf717d1228928740bdbfe761b6e62b870902/keps/NNNN-kep-template/README.md), “Proposal,” “Design Details,” “Production Readiness Review Questionnaire,” and “Alternatives.”

Read the separation between the desired outcome and the implementation detail. The production-readiness questions ask for observable behavior under enablement, rollback, version skew, load, dependency failure, and troubleshooting. These questions expose whether a design description has explained its system consequences rather than merely listed components.

Transfer the relevant question and answer, not the entire template. A new stateful protocol may need upgrade and rollback semantics; a short analysis memo does not need release signoff or every scaling question. Required headings remain required when actually contributing a KEP. Non-goals and review procedures belong only where the project's process or a consequential ambiguity requires them. KEP status and implementation status are not interchangeable.

### Rust RFC 2394: observable behavior, then reference semantics

Source: [async/await RFC at revision f17e8623ee2e2854570dcdb936a9f4ab08c0fcd4](https://github.com/rust-lang/rfcs/blob/f17e8623ee2e2854570dcdb936a9f4ab08c0fcd4/text/2394-async_await.md), “Guide-level explanation,” “Reference-level explanation,” “Rationale and alternatives,” and “Unresolved questions.”

The guide-level section explains delayed execution and uses a short program with observable print order. The reference-level section explains the generated state, captured lifetimes, and trait implications. The rationale compares return-type choices through their effect on lifetime elision and usability. Rejected designs and postponed extensions remain separate.

Transfer this movement between reader levels and the specific cost of an alternative. Keep the effect visible before explaining a compiler mechanism. Preserve an exact contract when readers need it; do not compress lifetimes or evaluation order into “works like synchronous code.” This is a historical design proposal with provisional syntax, including `await!`; it is not evidence of today's Rust API or a runnable modern example without rechecking.

### Python PEP 703: distinguish intended capability from measured overhead

Source: [PEP 703](https://peps.python.org/pep-0703/), especially “Backwards Compatibility,” “Performance,” “Reference Implementation,” “Alternatives,” and “Rejected Ideas.” The inspected [source revision](https://github.com/python/peps/blob/f866e77409305866038471574f075cd8d83eee9e/peps/pep-0703.rst) is retained for the historical comparison.

The performance section identifies the build mode, separates single-threaded and multithreaded execution overhead, names hardware and benchmark version, and supplies baseline revision `018be4c`. It then connects the overhead to implementation mechanisms. The compatibility section distinguishes C-API/ABI effects from Python-code effects and conditions them on the affected build configuration. The reference implementations have different evaluation uses rather than being presented as interchangeable.

Transfer the placement of conditions in the specific result and the distinction between an intended capability and its measured cost. Do not turn the historical performance table into a claim about current CPython releases or assume that a proposal's acceptance validates every old benchmark. In prose, a short configuration qualifier often does more work than a general disclaimer.

### MapReduce: connect system design to controlled experiments

Source: Dean and Ghemawat, [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI 2004; [paper PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4449.pdf). Read sections 2–3 for the programming model/implementation separation and sections 5.1–5.5, especially Figure 3, for the experimental argument.

The interface explanation specifies inputs, intermediate grouping, and outputs before describing the distributed implementation. The evaluation names the computations and cluster configuration. The matched panels expose normal execution, disabled backup tasks, and killed workers. The prose links curve features to scheduling, data transfer, output replication, and startup costs.

Transfer the description of what is held constant, the observable difference, and the mechanism that explains it. Keep total elapsed time separate from a peak rate. The paper's historical hardware, production-use counts, and evaluative adjectives are not defaults for new reports. Inspect the original figure before reusing its panel structure; text extraction alone cannot establish its layout.

### Circuit Tracing: test the explanation, not only the output

Source: Ameisen and colleagues, [Circuit Tracing: Revealing Computational Graphs in Language Models](https://transformer-circuits.pub/2025/attribution-graphs/methods.html), introduction, replacement-model description, perturbation validation, and “Limitations,” particularly “Missing Attention Circuits.”

The opening identifies the method's object: a replacement model that approximates components of the original model. The validation discussion tests graph-derived mechanisms through interventions rather than treating output agreement as sufficient. The limitations section links a methodological choice, fixed attention patterns, to computations that the graph cannot explain, then supplies concrete counterexamples.

Transfer the language separating the instrument, the observation, and the inference about the underlying system. Preserve a limitation when it changes what the figure can establish. Do not replace such detail with a generic “results may vary,” or copy rhetorical excitement because it appears in a research paper. Its large interactive graph is useful for investigation; a static report needs a selected explanatory view, not a screenshot of every control.

### AlphaEvolve: separate the system mechanism from applications

Source: Google DeepMind, [AlphaEvolve white paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf), system description, Table 1, and Figures 1–2.

Read the representation of candidates as programs, their modification by language models, and the role of automated evaluators. The comparison with prior work and the application-specific results answer different questions. Transfer the named components and feedback relation, then retain each application's own objective, evaluator, and comparison conditions.

Do not inherit the paper's broad promotional language or treat passing an evaluator as an unrestricted correctness guarantee. An evaluator establishes only the properties it actually checks. A single public white paper can contain useful technical description and claims that still need independent support.

### SRE example: impact, mechanism, and corrective action

Source: [Google SRE's Example Postmortem](https://sre.google/sre-book/example-postmortem/), summary/impact, root causes/trigger, resolution/detection, action items, and timeline.

The useful structure separates the user-visible effect, latent conditions, immediate trigger, mitigation, recovery, and corrective work. The timeline distinguishes outage and incident milestones; action items are linked to work rather than left as general intentions. This is a fictional teaching example with humorous elements, not an observed Google outage.

Transfer the causal separation and action specificity. Do not copy its invented incident identifiers, numbers, people, humor, or internal-looking links into a new document. In a real report, evidence must support each material event and causal link, and attribution must fit the recipients.

### MADR: preserve the decision and its reason

Source: [Use Markdown Architectural Decision Records](https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html), context/problem, considered options, and decision outcome.

The record asks a concrete format question, names alternative approaches, and records the chosen option with reasons. Transfer the inspectable question-to-choice relationship and preservation of the decision. For engineering decisions, prefer reasons tied to constraints and consequences; broad claims such as a project's liveliness should not replace the technical rationale.

Supporting source: [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) for documents that explicitly adopt BCP 14 requirement language. Preserve its uppercase convention where used; do not import the RFC's publication boilerplate into unrelated project prose.

### Broader foundations and selective transfer

The [example library](#example-library) below connects project specifications, engineering investigations, and visual explanations to original writing actions. `insight-dashboard` maintains the complementary operational and analysis library. For a shadcn implementation, use the [official shadcn skill](https://ui.shadcn.com/docs/skills) directly. These reading paths extend, rather than replace, the close readings above.

The earlier collection also informs these choices:

- **Reader problem and consequential questions:** [Amazon's product-management discussion](https://aws.amazon.com/executive-insights/content/product-management-at-amazon/) motivates starting from a concrete reader or user need. Adapt the question, not its press-release voice or a compulsory PR/FAQ template.
- **Value, comparison, and local source placement:** [Stripe's annual update](https://stripe.com/annual-updates/2025) provides a visual reference for readable comparison and labeling. Treat it as presentation evidence, not the default voice of an engineering report.
- **Population-specific findings:** [Anthropic's geographic economic analysis](https://www.anthropic.com/research/economic-index-geography) and [GitHub Octoverse](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) illustrate linking findings to data views. Keep each observed population and measure explicit rather than generalizing to all users or developers.
- **Evaluation conditions:** [OpenAI's reasoning report](https://openai.com/index/learning-to-reason-with-llms/) connects comparisons with compute and sampling choices. Preserve those conditions and the attribution of reported results. AlphaEvolve's system and application distinction is discussed above.
- **Explanatory sequence and exploration:** [Distill on momentum](https://distill.pub/2017/momentum/) and [Segel and Heer](https://idl.uw.edu/papers/narrative), section 4.4, inform concrete-to-general explanation and the relationship between authored findings and reader exploration. Choose interaction when it answers a useful question.
- **Chart composition and text:** [IBM Carbon dashboards](https://carbondesignsystem.com/data-visualization/dashboards), [Datawrapper on text](https://datawrapper.de/blog/text-in-data-visualizations), and [Wilke on making a point](https://clauswilke.com/dataviz/telling-a-story.html) inform reading order, useful detail, and complementary titles, labels, annotations, and prose.
- **Direct language:** [Microsoft's style tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice) and [Vercel's writing guidelines](https://github.com/vercel-labs/writing-guidelines) inform concrete wording and efficient editing. Apply the destination's language and register; preserve facts and natural Korean relations.
- **Interface execution:** [Vercel's interface guidelines](https://vercel.com/design/guidelines), [official shadcn skills](https://ui.shadcn.com/docs/skills), and [shadcn MCP](https://ui.shadcn.com/docs/mcp) inform usable state and project-aware implementation. Use the official skill directly; component documentation remains authoritative for APIs.
- **Document rendering:** [Typst](https://typst.app/docs/), [Quarto](https://quarto.org/docs/output-formats/pdf-basics.html), and [Pandoc](https://pandoc.org/MANUAL.html#creating-a-pdf) inform the native and conversion routes in [document production](../skills/minimal/copydesk/references/document-production.md). Select the renderer by the recipient workflow and existing source.

Use each source for the property actually inspected. A saved text supports a textual reading; a diagram's layout or an interaction's effect requires the corresponding visual or behavioral inspection. Borrow the explanatory technique in original wording while preserving the actual project's evidence and current API.

### Selecting another exemplar

Prefer a primary method paper, specification, design proposal, decision record, engineering reference, or well-evidenced postmortem over an announcement, annual letter, product brochure, or adoption survey. Match the genre and reader task before the brand. Read the relevant prose and actual figures, then identify what to transfer at sentence, paragraph, evidence, table, caption, and document levels. Reuse the technique in original wording; preserve licenses and attribution when actual content or assets are reused.

## Notion block use

The block rules in `write-notion` were checked against these sources on 2026-11-20. They are maintenance pointers; the skill states the rules without loading this section.

- First block states the result: Nielsen Norman Group, [Inverted Pyramid](https://www.nngroup.com/articles/inverted-pyramid/), where readers can stop at any point and still have the main point.
- Toggles hold detail only some readers need: GOV.UK Design System, [Accordion](https://design-system.service.gov.uk/components/accordion/), which says not to use an accordion for content all users need; Nielsen Norman Group, [Accordions on Desktop](https://www.nngroup.com/articles/accordions-on-desktop/), on hidden content being missed and on deep hierarchies.
- Bold labels and emphasis: Martin Fowler, [Excessive Bold](https://martinfowler.com/bliki/ExcessiveBold.html), and Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), which lists bold-label bullets and emoji-led headings. Zhang et al., [From Lists to Emojis](https://arxiv.org/abs/2409.11704) (ACL 2025), measures reward-model and human preference for lists, bold, and emoji.
- Callouts and tables: Google developer documentation style guide, [Notices](https://developers.google.com/style/notices), and Google Technical Writing One, [Lists and tables](https://developers.google.com/tech-writing/one/lists-and-tables).
- Headings: Nielsen Norman Group, [F-Shaped Pattern](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/), on starting headings with the information-carrying words; Toss, [technical-writing](https://github.com/toss/technical-writing), on keeping one topic per page and shallow heading depth.
- Cut pass after drafting: Chakrabarty et al., [Can AI writing be salvaged?](https://arxiv.org/abs/2409.14509) (CHI 2025), which measures redundancy and cliché in model-written paragraphs and the effect of edit passes; Zhang et al., [Verbosity ≠ Veracity](https://arxiv.org/abs/2411.07858), on models padding answers when uncertain. Neither tests a plain instruction to be concise.
- Limits on cutting: Google Technical Writing One, [Paragraphs](https://developers.google.com/tech-writing/one/paragraphs), and Michael Nygard, [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), which keeps reasoning in full sentences.

## Example library

Use this library to find a public work close to the current reader task. The entries identify a passage and an original adaptation, not a prescribed template. Choose the relevant example, read its passage, and apply the technique to the actual project evidence. The skill's [synthetic examples](../skills/minimal/copydesk/references/synthetic-examples.md) hold finished synthetic rewrites; the [close readings](#close-readings) above hold the original technical foundations.

These are text and information-structure reading pointers. Inspect the actual figure or control before treating its visual meaning or behavior as evidence. Historical proposals, archived editions, and demos remain historical sources; current implementation claims require current documentation. Operational data-view examples are maintained in `insight-dashboard`.

### Design documents and exact references

- **[TigerBeetle Architecture (docs/ARCHITECTURE.md)](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/ARCHITECTURE.md)**: Read Design Decisions. Tie each design choice to the workload property that makes it useful. Give consequential decisions stable headings.

- **[FoundationDB Architecture (공식 문서)](https://apple.github.io/foundationdb/architecture.html)**: Read role descriptions. Explain component responsibilities in a consistent order, and trace the interaction that connects them.

- **[CockroachDB RFC: Distributing SQL queries (2016)](https://github.com/cockroachdb/cockroach/blob/master/docs/RFCS/20160421_distributed_sql.md)**: Read numbered examples and alternatives. Increase example complexity as the explanation needs it, then compare alternatives on the same constraints.

- **[SQLite Tokenizer Requirements (HLR 명세)](https://sqlite.org/draft/tokenreq.html)**: Read token requirements. For a testable specification, state the condition and required behavior precisely; use requirement IDs when traceability needs them.

- **[The Lemon Parser Generator (프로젝트 기술 문서)](https://www.sqlite.org/src/doc/trunk/doc/lemon.html)**: Read operation, syntax, and error processing. Introduce the operating model before syntax details, and place trust assumptions beside the input they constrain.

- **[React RFC 0188: Server Components](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md)**: Read basic example and component constraints. Show observable behavior before reference semantics, then explain adoption and compatibility for the affected callers.

- **[Svelte 5 소개 글: Runes (공식 블로그)](https://svelte.dev/blog/runes)**: Read old and new code examples. Explain a changed programming model with corresponding code examples; preserve the proposal date and recheck current syntax.

- **[SQLite Release 3.45.0 Changelog](https://www.sqlite.org/releaselog/3_45_0.html)**: Read changed defaults and release identity. Put a changed default, its effect, and the relevant override together; link the exact release being described.

- **[Zig 언어 레퍼런스 (0.16.0)](https://ziglang.org/documentation/0.16.0/)**: Read alignment and reference navigation. State the concept in a complete sentence before its numeric boundary; make exact interfaces easy to locate.

- **[SRFI-1 List Library (Olin Shivers)](https://srfi.schemers.org/srfi-1/srfi-1.html)**: Read rationale and function specifications. Explain how existing implementations informed an interface, then keep exact function behavior available for lookup.

- **[PEP 683 — Immortal Objects, Using a Fixed Refcount](https://peps.python.org/pep-0683/)**: Read acceptance conditions and historical status. Keep conditional acceptance visible and distinguish a design record from the current implementation reference.

- **[LangGraph Overview (공식 문서)](https://docs.langchain.com/oss/python/langgraph/overview)**: Read overview and acknowledged influences. Explain the orchestration responsibilities and suitable use case. Use the overview for orientation, not promotional phrasing as a technical voice.

- **[KEP-4603: Tune CrashLoopBackoff (Kubernetes Enhancement Proposal)](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/4603-tune-crashloopbackoff/README.md)**: Read design details and current/proposed behavior. Connect a proposed policy to its changed behavior and relevant operational checks; adapt the questions to the project.

- **[ClickHouse MergeTree 테이블 엔진 문서](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree)**: Read physical organization and CREATE TABLE syntax. Connect storage structure to the interface the reader uses, then explain the parameters that change behavior.

- **[Pijul Manual, Theory 장 (웨이백 스냅샷)](https://web.archive.org/web/20210307215344/https://pijul.org/manual/theory.html)**: Read graph definitions and dependencies. Give formal objects concrete identities and explain the operations on them. Read the archived edition for historical rationale.

- **[draft-toomim-httpbis-braid-http-04 (Braid-HTTP Internet-Draft)](https://www.ietf.org/archive/id/draft-toomim-httpbis-braid-http-04.txt)**: Read independent protocol extensions. Explain each independently adoptable capability and its concrete use case before describing their combination; preserve draft status.

- **[KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum](https://cwiki.apache.org/confluence/display/kafka/kip-500:+replace+zookeeper+with+a+self-managed+metadata+quorum)**: Read metadata as an event log. Explain the architectural constraint and the mechanism chosen to resolve it; keep a decision record connected to its discussion.

- **[SE-0393: Value and Type Parameter Packs (Swift Evolution)](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0393-parameter-packs.md)**: Read motivation and detailed design. Derive the proposed abstraction from a concrete maintenance cost, and introduce dependent concepts in dependency order.

- **[Go 제네릭 구현 설계: Dictionaries + Gcshape Stenciling (Go 1.18)](https://go.googlesource.com/proposal/+/refs/heads/master/design/generics-implementation-dictionaries-go1.18.md)**: Read gcshapes and dictionary format. Define the equivalence conditions precisely and relate the concrete design to earlier proposals on the same subject.

- **[Rust RFC 131: Target Specification](https://rust-lang.github.io/rfcs/0131-target-specification.html)**: Read target settings and their combinations. State conditional configuration behavior so readers can predict the effect of combining options.

- **[SQLite Database File Format 명세](https://www.sqlite.org/fileformat.html)**: Read database header and record format. Present offsets, sizes, and meanings in a consistent lookup structure, with the version boundary that makes the format applicable.

- **[PyPA Binary Distribution Format (Wheel) 명세](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)**: Read filename rules and RECORD. Keep naming, integrity records, and installation-relevant behavior in the format specification where implementers can find them.

- **[PostgreSQL 18 Release Notes](https://www.postgresql.org/docs/current/release-18.html)**: Read migration and compatibility. Put upgrade consequences where operators will see them before acting, then describe new capabilities in their relevant groups.

- **[Django 5.1 Release Notes](https://docs.djangoproject.com/en/6.1/releases/5.1/)**: Read compatibility and paired code examples. Show the old and new use of an interface with comparable code, and keep supported-version information beside migration guidance.

- **[PostgreSQL Wiki: Don't Do This](https://wiki.postgresql.org/wiki/Don%27t_Do_This)**: Read rationale and appropriate exceptions. Pair a discouraged practice with the preferred alternative and the condition under which an exception is useful.

- **[RFC 9110: HTTP Semantics (표준)](https://www.rfc-editor.org/rfc/rfc9110.txt)**: Read method and status semantics. Preserve exact requirement levels and cross-reference definitions when writing a normative protocol specification.

- **[NEP 18: NumPy Array Function Protocol](https://numpy.org/neps/nep-0018-array-function-protocol.html)**: Read motivation and alternatives. Use concrete ecosystem needs to explain an interface extension, and state how experimental behavior will evolve.

- **[Git hash-function-transition 설계 문서 (Documentation/technical)](https://github.com/git/git/blob/master/Documentation/technical/hash-function-transition.adoc)**: Read goals and transition procedures. Explain compatibility during a staged format transition and show the ordered operations needed to preserve it.

- **[CPython Argument Clinic (Developer's Guide)](https://devguide.python.org/development-tools/clinic/)**: Read background, tutorial, reference, and how-to. Separate learning from exact lookup while keeping one current home for the documentation.

### Engineering reports and investigations

- **[Cloudflare outage on November 18, 2025](https://blog.cloudflare.com/18-november-2025-outage/)**: Read request processing and the outage. Connect recurring symptoms to the described configuration mechanism; derive event times from the source rather than an inferred chart timeline.

- **[Slack's Incident on 2-22-22](https://slack.engineering/slacks-incident-on-2-22-22/)**: Read mitigation and datastore load. Explain the immediate mitigation and its cost, then trace the conditions that caused the incident.

- **[Incident Report: Spotify Outage on April 16, 2025](https://engineering.atspotify.com/2025/5/incident-report-spotify-outage-on-april-16-2025/)**: Read impact and cause analysis. Separate affected populations in the prose and explain why their conditions differed; inspect the chart before asserting a visual encoding.

- **[Upgrading GitHub.com to MySQL 8.0](https://github.blog/engineering/infrastructure/upgrading-github-com-to-mysql-8-0/)**: Read upgrade plan, rollback, and challenges. Give migration stages concrete validation and recovery points, and explain gaps between test and production behavior.

- **[Partitioning GitHub's relational databases to handle scale](https://github.blog/engineering/infrastructure/partitioning-githubs-relational-databases-scale/)**: Read virtual partitions. Explain logical boundary enforcement before physical movement. Keep query rates distinct from the number of partitions.

- **[How GitHub uses eBPF to improve deployment safety](https://github.blog/engineering/how-github-uses-ebpf-to-improve-deployment-safety/)**: Read dependency types and filtering. Classify the actual failure modes before presenting the mechanism that addresses them.

- **[How Figma's multiplayer technology works](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)**: Read OT/CRDT influences and central authority. State the assumptions that permit a simpler custom design; this source describes CRDT-inspired structures, not adoption of OT.

- **[Rust in production at Figma](https://www.figma.com/blog/rust-in-production-at-figma/)**: Read performance and benefits/drawbacks. Relate a language choice to the service workload, its measured behavior, and the costs that remain.

- **[How Discord Scaled Elixir to 5,000,000 Concurrent Users](https://discord.com/blog/how-discord-scaled-elixir-to-5-000-000-concurrent-users)**: Read fanout, shared data, and concurrency. Organize the explanation around bottlenecks, showing how observations changed the attempted solution.

- **[The Data Canary: How Netflix Validates Catalog Metadata](https://netflixtechblog.com/the-data-canary-how-netflix-validates-catalog-metadata-18b699d58e36)**: Read controlled failure injection. Explain the validation system through its constraints, then describe a test that checks the validator itself.

- **[A Closer Look at the Christmas Eve Outage](https://netflixtechblog.com/a-closer-look-at-the-christmas-eve-outage-d7b409a529ee)**: Read dependency postmortem and service impact. Attribute the provider explanation separately from the impact observed in the dependent service.

- **[How we cut CDN metadata lookup latency by 91%](https://vercel.com/blog/how-we-cut-cdn-metadata-lookup-latency-by-91-percent)**: Read lookup stages and rollout trade-offs. Show how each change addresses a particular cost, including the evidence-based reason to stop optimizing.

- **[Reasons why bugs might feel "impossible"](https://jvns.ca/blog/2021/06/08/reasons-why-bugs-might-feel-impossible/)**: Read debugging difficulty categories. Turn a vague difficulty into a concrete information gap and the next useful way to investigate it.

- **[How web bloat impacts users with slow connections](https://danluu.com/web-bloat/)**: Read connection-speed comparison and tail behavior. Choose comparison dimensions that represent different user conditions, and preserve important variation beyond the average.

- **[Postgres Job Queues & Failure By MVCC](https://brandur.org/postgres-queues)**: Read test bench, lock time, and dead tuples. Descend from symptom to mechanism with an observation at each layer; keep the reproduction setup retrievable.

- **[AI Flame Graphs](https://www.brendangregg.com/blog/2024-10-29/ai-flame-graphs.html)**: Read profiling units and sample search. Explain what the visualization measures before interpreting its shapes, and state relevant collection overhead.

- **[A dynamic linker murder mystery](https://fasterthanli.me/articles/a-dynamic-linker-murder-mystery)**: Read investigation and counterexamples. Retain the observation that disproved a hypothesis; introduce background at the point the reader needs it.

- **[Jepsen: etcd 3.4.3](https://jepsen.io/analyses/etcd-3.4.3)**: Read consistency documentation, tests, and results. Translate a guarantee into observable behavior, then distinguish the test design from what the tests found.

- **[Problems with the heap](https://rachelbythebay.com/w/2025/03/26/atop/)**: Read reproduction blocks. Use a minimal observed failure to anchor an investigation; keep reproduction instructions separate from unsupported generalization.

- **[Stack Overflow: How We Do Monitoring - 2018 Edition](https://nickcraver.com/blog/2018/11/29/stack-overflow-how-we-do-monitoring/)**: Read data types and alerting. Organize a monitoring explanation by signals and operator tasks before listing the tools that implement them.

- **[Etsy's Debriefing Facilitation Guide for Blameless Postmortems](https://www.etsy.com/codeascraft/debriefing-facilitation-guide)**: Read debriefing questions and dialogue. Show questions that recover the information available at decision time, then connect that context to procedural improvement.

- **[How Uber Executed A JUnit Migration at Massive Scale](https://www.uber.com/blog/junit-migration/)**: Read migration prerequisites and recipe. Connect each automation stage to its concrete input, output, and check; use usage evidence to prioritize work.

- **[서버 증설 없이 처리하는 대규모 트래픽](https://toss.tech/article/monitoring-traffic)**: Read bottlenecks and improvement iterations. Connect each intervention to the observed bottleneck and its subsequent measurement; retain natural, complete Korean sentences.

- **[Feign 코드 분석과 서버 성능 개선](https://toss.tech/article/engineering-note-3)**: Read problem analysis and library behavior. Follow the observed symptom into the library mechanism before explaining why the change affects performance.

- **[BFF 서버에 SSE를 도입한 이유: 전시 서버의 통신 구조 재설계](https://techblog.woowahan.com/26507/)**: Read communication design and SSE choice. Explain the interface constraint, compare plausible transports, and describe the selected request flow.

- **[스마트스토어센터 Oracle에서 MySQL로의 무중단 전환기](https://d2.naver.com/helloworld/6512234)**: Read dual writes and consistency validation. Describe the migration mechanism and the checks needed to maintain consistent data during the transition.

- **[같은 장애를 두 번 겪지 않기 위해, 배포 전에 리뷰합니다 — KRIS 개발기](https://tech.kakao.com/posts/831)**: Read rule checks and model judgment. Explain which mechanism makes each decision and why the responsibilities are separated; use scope detail only where it affects the reader.

- **[개인화된 Airflow 테스트 환경 구축 및 운영 경험](https://tech.kakao.com/posts/829)**: Read environment design and lifecycle examples. Derive requirements from existing workflow friction, then show creation, use, and cleanup as concrete reader tasks.

- **[Profiling a simple performance issue in a JVM-based server](https://engineering.linecorp.com/en/blog/profiling-a-simple-performance-issue-in-a-jvm-based-server/)**: Read hotspot investigation and conclusion. Show the evidence behind continuing or stopping an optimization, with the interpretation limits of profiling samples.

- **[How adding Kubernetes label selectors caused an outage in Grafana Cloud Logs — and how we resolved it](https://grafana.com/blog/how-adding-kubernetes-label-selectors-caused-an-outage-in-grafana-cloud-logs-and-how-we-resolved-it/)**: Read investigation queries and label behavior. Connect the configuration change to traffic distribution and explain meaningful differences between affected and unaffected environments.

### Visual and data explanations

- **[GPS (interactive essay)](https://ciechanow.ski/gps/)**: Read simple positioning and time of flight. Begin with a small model, name the variable the reader changes, and add complexity when the earlier model reaches its limit.

- **[Sound (interactive essay)](https://ciechanow.ski/sound/)**: Read waves and oscillation. Let a concrete experiment introduce a parameter, then state the approximation conditions of the explanation.

- **[Curves and Surfaces (interactive essay)](https://ciechanow.ski/curves-and-surfaces/)**: Read splines and continuity. Show the failure of the initial construction, the improvement, and the next constraint that remains.

- **[Moon (interactive essay)](https://ciechanow.ski/moon/)**: Read brightness baseline and scene notation. Establish the comparison model and explain the simplifications that change how a diagram should be read.

- **[Hexagonal Grids (reference article)](https://www.redblobgames.com/grids/hexagons/)**: Read coordinate systems and conversions. Organize a reference by implementation task; keep linked representations consistent when a parameter changes.

- **[Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)**: Read paired search examples. Hold the input constant while changing one algorithmic condition, then explain the observed difference.

- **[Probability for RPG Damage](https://www.redblobgames.com/articles/probability/damage-rolls.html)**: Read distribution explanation. Explain unfamiliar encodings at first use and connect the distribution to the design choice it informs.

- **[2D Visibility algorithm](https://www.redblobgames.com/articles/visibility/)**: Read algorithm summary. Conclude a mechanism explanation with its usable ordered operations and a clear distinction between implemented and untried approaches.

- **[CO₂ and Greenhouse Gas Emissions landing page](https://ourworldindata.org/co2-and-greenhouse-gas-emissions)**: Read key insights and baseline. Make the supported finding prominent, with the baseline and uncertainty needed to interpret its evidence. Adapt headline wording to this skill's noun-phrase title default; state the finding in the nearby text.

- **[Air Pollution topic page](https://ourworldindata.org/air-pollution)**: Read metric definition and evidence. Define the measurement boundary before the result when that boundary is necessary for interpretation.

- **[Can an AI make a data-driven, visual story?](https://pudding.cool/2024/07/ai/)**: Read production stages and editorial feedback. Make tool output and reviewer judgment visibly distinct; retain representative failures as evidence in an adoption assessment.

- **[Why I changed my mind on dual-axis charts](https://datawrapper.de/blog/why-i-changed-my-mind-on-dual-axis-charts)**: Read alternative chart forms. Compare encodings using the same data and choose according to the reader question, preserving what each view makes harder to see.

- **[Plotting fall temperatures with range & value overlays (Weekly Chart)](https://datawrapper.de/blog/span-chart-range-value-overlays-in-column-charts)**: Read input columns, overlays, and annotations. Describe the input shape and transformation, then distinguish annotations that define the display from those that explain a finding.

- **[Up and Down the Ladder of Abstraction](https://worrydream.com/LadderOfAbstraction/)**: Read concrete, trajectory, and aggregate views. Move between individual behavior and aggregate structure, explaining what the reader is looking at after each change of level.

- **[Parable of the Polygons](https://ncase.me/polygons/)**: Read manual and automated simulations. Introduce the rule through a small manual example before moving to repeated aggregate behavior.

- **[How To Remember Anything Forever-ish](https://ncase.me/remember/)**: Read guided explanation and sources. Make the next learning action clear and keep supporting sources retrievable; retain a restrained register for technical work.

- **[Histogram (D3 notebook)](https://observablehq.com/@d3/histogram)**: Read input, transformation, and rendered result. Separate an analysis into reusable computational steps and preserve the rendered output for static readers.

- **[Blockchain Explained (Reuters visual guide)](https://www.reuters.com/graphics/TECHNOLOGY-BLOCKCHAIN/010070P11GN/index.html)**: Read components and transaction stages. Follow the same concrete record through the stages so the reader can connect the mechanism end to end.

- **[Feature Visualization (Distill)](https://distill.pub/2017/feature-visualization/)**: Read figure explanations and method questions. Give a technical figure enough local context to be interpreted, and organize unfamiliar methods around reader questions.

- **[Vital Signs: Global Temperature (NASA)](https://climate.nasa.gov/vital-signs/global-temperature/)**: Read takeaway, baseline, and measurement uncertainty. State the baseline beside the result and choose comparison language that matches the available uncertainty evidence.

- **[Climate change: global temperature (NOAA Climate.gov explainer)](https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature)**: Read definitions, captions, and archive notice. Define unfamiliar measurements where used, attribute the data behind a figure, and make an archived document recognizable.

- **[Attention in transformers, step-by-step (3Blue1Brown)](https://www.3blue1brown.com/lessons/attention)**: Read diagram notation and attention explanation. Explain what the diagram symbols and transformations mean before asking the reader to interpret them.

- **[[데이터로 보는 뉴스] 서울 아파트 전세값, 매매값의 70%](https://www.hani.co.kr/arti/economy/property/714189.html)**: Read aggregation method and sparse transactions. State the grouping rule and use a concrete small-sample case to explain why an apparent extreme needs care.

- **[퀀트 전략을 이용한 종목선정 (심화) — R 퀀트 쿡북](https://hyunyulhenry.github.io/quant_cookbook/%ED%80%80%ED%8A%B8-%EC%A0%84%EB%9E%B5%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%A2%85%EB%AA%A9%EC%84%A0%EC%A0%95-%EC%8B%AC%ED%99%94.html)**: Read problem, code, and explanation. Introduce the task before its code, then explain the transformation in natural Korean with a consistent register.

- **[Population structure and ageing (Eurostat Statistics Explained)](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Population_structure_and_ageing)**: Read highlights and extraction date. Pair a broad trend with important exceptions and distinguish data extraction time from the next planned update.

- **[An Intuitive Guide To Exponential Functions & e](https://betterexplained.com/articles/an-intuitive-guide-to-exponential-functions-e/)**: Read intuition and formal definition. Use a familiar structural relation to introduce a concept, then connect the intuition to its precise definition.

### Periodic reviews

- **[Evidence weekly review](https://business-review-demo.netlify.app/weekly-reports/2021/52)**: Read previous actions, measures with commentary, and next actions. Borrow the organization, not the demo's inconsistent chronology or unsupported causal comments.

- **[Wikimedia Movement Metrics, February 2025](https://upload.wikimedia.org/wikipedia/commons/a/ab/February_2025_Wikimedia_movement_metrics.pdf)**: Read metric explanations, definition changes, and missing-data notes. Attach commentary to the same period and population as the data.
