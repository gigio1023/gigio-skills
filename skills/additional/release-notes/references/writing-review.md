# Writing Review

Read when reviewing the prose of a drafted note. A release note is usually written at the end of a long session, full of labels the session coined and phrasing compressed to save words. A 2026 study measured that kind of compression in model text, and the prompts below turn its measured features, plus reader complaints about model-written prose, into questions a reviewer can answer about one draft.

These are review prompts, not limits. The features are over-represented in model text, not wrong in themselves, so a reviewer judges each hit by whether it costs this reader. Sentence length and noun runs are clues to inspect, consistent with `copydesk`, which sets no hard caps.

## Running the review

Give a fresh-context reviewer the rendered note text or `note.json`, the reader description, and the prompts below. A reviewer who did not take part in the session sees the coined labels that the writer no longer notices. The reviewer returns findings with the sentence and a proposed rewrite; the writer checks each against the data file and the sources before applying it, because a rewrite can change a claim. For sentence-level rules beyond these prompts, apply `copydesk` when installed, and its Korean writing reference for Korean notes.

## Word budget

The opening and the actions are bullets, and page one holds the overview figure plus at most six top-level bullets of one line each, with nested bullets for detail. Ask of the draft: does any top-level bullet run past one line, does a bullet hold two points, and does an explanation sit on page one that belongs in a material change, an extra section, or the appendix? Split, cut, or move it. D22 and D23 in [design-checks.md](design-checks.md) measure the same budget on the rendered note; this review catches the bullet that fits but says too much.

## Prompts

| # | Ask of each sentence | Rewrite toward | Evidence |
| --- | --- | --- | --- |
| W1 | Is the subject the actor or the changed thing, or an inanimate subject doing something only a person does? | The actual action: "returns an empty list", not "swallows the error"; "the definition now covers", not "the definition embraces" | Inanimate subjects with animate verbs were over-used by all nine frontier models measured |
| W2 | Do three or more nouns stack before a noun, outside an established field term? | Unpack with a preposition or a clause: "validating the latency of state transitions", not "state transition latency validation" | Stacked noun compounds, three or more nouns, measured as a difficulty feature |
| W3 | Is every term the name the reader already has: the artifact's own record name, a field term, or an earlier release's wording? | The record's official name at first mention with its ID; no label coined during the work | Readers reported models inventing jargon as a conversation grows; effects were largest in long chat and coding sessions |
| W4 | Is a verb made from a noun or used as a metaphor where a plain verb exists? | "is listed", "is added", "moved to", not "surfaces", "lands", "stages" | Ad hoc denominal verbs measured as over-used |
| W5 | Is an unusual word combination doing work an ordinary phrase would do? | The wording the field or the artifact uses | Rare word pairs and higher n-gram perplexity than a meaning-preserving paraphrase, in all three settings measured |
| W6 | Does a clause sit between a subject and its verb, or a verb and its object, long enough to hold the reader's memory? | Split the sentence, or move the clause after the main statement | Longer dependency arcs than human baselines in conversation |
| W7 | Was an optional "that" dropped where a noun is followed by a noun and then a verb? | Keep "that", or make the clause active | Models skip the optional word; a length penalty drove the omission above 98 percent in the paper's training experiment |
| W8 | Does a sentence announce, recap, or praise rather than state? | Delete it: "This release lays the foundation", "Here is how the changes compare", "This is a significant improvement" | Reader complaints about filler lead-ins and summary transitions |
| W9 | Does each sentence carry an ID, a count, an example, a condition, or an action, and only the net difference between the two released versions? | Strike work-history residue: "we removed X" for something never released, "does not support Z" because someone once asked | Readers reported documentation that carried the drafting conversation |
| W10 | Can the stated reader act on the note without the session? | Name the reader and the decision; test with the cold reader | A frequent complaint was that the model did not infer its audience |
| W11 | Does each list or table hold items that share attributes? | Prose for a cause, a mechanism, or a trade-off; a table for comparable attributes | Raters were reported to reward lists, headings, and vivid phrases regardless of use |

## Korean notes

The study measured English only. Korean shows the same habits in different forms, so apply the prompts this way and let copydesk's Korean writing reference govern the sentence rules.

| Prompt | Korean form to look for |
| --- | --- |
| W1 | A personified subject: "정의가 범위를 품는다", "결과가 시사한다"; rewrite with the actor or the plain change: "정의가 다루는 범위가 넓어졌다" |
| W2 | A noun chain without particles: "분류 체계 정의 변경 영향 범위"; restore particles or make a clause, keeping established compound terms |
| W4 | An English stem plus 하다 or a calqued metaphor where a plain Korean verb exists: "enqueue한다" for "queue에 넣는다" |
| W5 | Calques and translation-style phrases such as "~를 통해", "~에 의해 만들어진" where a direct phrase exists |
| W6 | A long modifier clause before the head noun, or a chain of connective endings that hides which clause depends on which; split where the relation is lost |
| W7 | No Korean counterpart; skip |
| W8 | "요약하면 다음과 같다", "주목할 만한 변화다", "시사하는 바가 크다" |

Keep English field terms the reader uses, and record names as the artifact spells them.

## Limits

The paper links its features to human processing difficulty through earlier psycholinguistic work and does not run its own reading or comprehension test, and no source tested these prompts on release notes. Treat a finding as a reason to look, and the cold reader as the test of whether the note works.

## Sources

Clark, Martin, and Mahowald, "Why is AI-generated language so hard to understand?", [arXiv 2610.29162](https://arxiv.org/abs/2610.29162), 2026-10-21, sections 3 to 5 and Table 2; the [Hacker News discussion](https://news.ycombinator.com/item?id=50223647) for reader complaints (comment IDs 50235990, 50224324, 50226391, 50236916, 50224350, 50224417); the [GeekNews topic](https://news.hada.io/topic?id=35947) for the Korean observation. All read 2026-11-01.
