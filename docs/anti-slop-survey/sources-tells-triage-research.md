# Tells lists, triage views, and research

Opened on 2026-11-25. Pages marked "summary" were read through a fetch tool's model summary rather than the raw text, so their wording here is a paraphrase. Venue is recorded only where the arXiv record, the publisher, or the conference listing states it; the rest are marked unverified.

## Public tells lists

### Wikipedia: Signs of AI writing

- [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), revision 1387041075 (2026-11-22 12:47 KST), CC BY-SA 4.0. Paraphrased here, not copied.
- The page calls itself descriptive and warns that fixing only the surface signs hides the underlying problems, such as unsupported synthesis. It lists perfect grammar, transition words alone, and formal or bland prose as ineffective indicators, and moved "In summary" sections, knowledge-cutoff disclaimers, and em dashes to a historical list in 2026.
- Current structural tells include rigid closing sections, title-case and "X and Y" headings, heavy bold, inline-header bullet lists, and, added in mid-2026, corrective disclaimers such as "rather than" and "does not by itself establish".
- Borrowed: the stance that a sign marks a place to read, already copydesk's rule.
- Not borrowed: a corrective-disclaimer counter. In the evaluation set those phrases occurred 0 times in the two AI-assisted reports, 4 times in a maintainer-written advisory, and 11 times in this repository's own `docs/writing-sources.md`, so a count would not separate the target failure and would mostly flag this pack's house style. Whether the house style should change is an open question in the [overview](README.md#open-questions).

### Wikipedia: Signs of AI use in comments

- [Wikipedia:Signs of AI use in comments](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_use_in_comments), revision 1387778157 (2026-11-25 20:34 KST), CC BY-SA 4.0. Only the summary and heading structure were read.
- Describes chatbot replies in discussions as a clerk-like or customer-service register: salutations and sign-offs, assurances of good faith, overjustification, requests for feedback, and long comments split into titled sections.
- Borrowed: the list of what a reply leaves out, in copydesk's comment form and vuln-report's follow-up guidance.

## Triage views of AI-generated vulnerability reports

| Source | Date | What it adds |
| --- | --- | --- |
| [Stenberg, The I in LLM stands for intelligence](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/) | 2024-01-02 | Fluent slop costs more triage time than obvious junk; a follow-up answering "where is the overflow" with more generated text instead of a location |
| [Stenberg, Death by a thousand slops](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/) | 2025-07-14 | About 5% of 2025 submissions were real vulnerabilities; slop titles pair a bug class with an unproven consequence |
| [Stenberg, The end of the curl bug-bounty](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/) | 2026-01-26 | Bounty ended under report volume |
| [curl CONTRIBUTE.md, On AI use](https://github.com/curl/curl/blob/7e1001bcd699/docs/CONTRIBUTE.md) | 2026-05-27 | Disclose AI use; explain in your own voice, briefly |
| [vLLM SECURITY.md](https://github.com/vllm-project/vllm/blob/08426d51ef1d/SECURITY.md) | 2026-09-10 | Under reporter credit, only the first reporter is credited because duplicate and AI-generated reports would create unsustainable workload; nothing on style |
| [Seth Larson, New era of slop security reports](https://sethmlarson.dev/slop-security-reports) | 2024-12-03 | Check that the flaw is in the project, not in how the PoC uses it; maintainers reply briefly and expect justification |
| [Linux kernel security-bugs.rst](https://github.com/torvalds/linux/blob/6ffecfe0805e/Documentation/process/security-bugs.rst) | 2026-08-04 | AI reports are too long with many sections; critical facts first; plain text; one verifiable impact statement instead of speculative consequences; tested reproducer and fix |
| [Django security policy](https://github.com/django/django/blob/c392a758e6d3/docs/internals/security.txt) | 2026-11-05 | Disclose AI use by task; unverified AI output closed without reply; a canary request addressed to AI tools, recorded and not followed |
| [Bugcrowd glossary: AI slop](https://www.bugcrowd.com/glossary/ai-slop/), summary | undated | Red flags: hallucinated references, generic text that fits any system, false chains, overstated impact, a reporter who disappears on follow-up |
| [HackerOne Code of Conduct](https://www.hackerone.com/policies/code-of-conduct), summary | undated | Unverified or fabricated claims and comment spam as conduct problems |
| [Bugcrowd policy changes for AI slop](https://www.bugcrowd.com/blog/bugcrowd-policy-changes-to-address-ai-slop-submissions/), summary | 2026-03-10 | Platform enforcement; no writing rules |
| [Node.js SECURITY.md](https://github.com/nodejs/node/blob/aa8d6b9384ad/SECURITY.md) | 2026-10-07 | No AI clause; asks for the minimum PoC |

Borrowed into vuln-report and submission-review: the product-name deletion test for generic text, the canary rule, the follow-up register, and the answer-with-a-location rule. The vuln-report skill already carried critical-facts-first, plain text for the kernel, and bounded impact from the same kernel and Django sources.

No source sets a length for a follow-up comment. That a good reply answers first, adds one piece of evidence or concedes, and carries no greeting or recap is an inference across curl, Larson, Bugcrowd, and the Wikipedia comments page.

## Research

| Work | Venue and date | Finding used |
| --- | --- | --- |
| Shaib, Chakrabarty, Garcia-Olano, Wallace, [Measuring AI "Slop" in Text](https://arxiv.org/abs/2509.19163) | arXiv 2025-09; venue unverified | Relevance, density, and tone predict human slop labels best; GPT-5, DeepSeek-V3, and o3-mini agree with those labels near chance; syntax features predict weakly (AUROC 0.64 to 0.68) |
| Oh, Lee, Ahn, Kim, Kang, [Science or Slop?](https://arxiv.org/abs/2610.00531) | arXiv 2026-09, preprint | Macro redundancy measured as cross-section n-gram overlap separates AI from human papers; slop-aware prompting overcorrects by dropping citations; evidence-grounded revision narrows the gap |
| Kobak et al., [Delving into LLM-assisted writing in biomedical publications through excess vocabulary](https://arxiv.org/abs/2406.07016) | Science Advances, 2025 | Source of `check_slop.py`'s verb list; tells drift by model era |
| Reinhart et al., [Do LLMs write like humans?](https://arxiv.org/abs/2410.16107) | PNAS, 2025 | Participial clauses and nominalizations overused; grammatical differences persist across models |
| Sun, Yin, Xu, Kolter, Liu, [Idiosyncrasies in Large Language Models](https://arxiv.org/abs/2502.12150) | ICML 2025 | Word choice identifies the source model: five-way classification at 97.1%, still 95.1% with punctuation and Markdown removed |
| Shaib, Elazar, Li, Wallace, [Syntactic Templates in Generated Text](https://arxiv.org/abs/2407.00211) | EMNLP 2024 | Generated text repeats part-of-speech templates more than human text |
| Padmakumar and He, [Does Writing with Language Models Reduce Content Diversity?](https://arxiv.org/abs/2309.05196) | ICLR 2024 | Co-writing with a feedback-tuned model made essays from different writers more alike; the loss came from model-written text |
| Sourati et al., [The Shrinking Landscape of Linguistic Diversity](https://arxiv.org/abs/2502.11266) | Nature Human Behaviour, 2026 per arXiv | Homogenization at population scale |
| Russell, Karpinska, Iyyer, [People who frequently use ChatGPT ... are accurate and robust detectors](https://arxiv.org/abs/2501.15654) | ACL 2025 | Experienced readers detect generated text; untrained readers near chance |
| Dubois et al., [Length-Controlled AlpacaEval](https://arxiv.org/abs/2404.04475); Saito et al., [Verbosity Bias in Preference Labeling](https://arxiv.org/abs/2310.10076) | COLM 2024; venue unverified | Model judges prefer longer answers, one reason generated reports grow |
| Paech et al., [Antislop](https://arxiv.org/abs/2510.15061) | arXiv 2025-10, preprint | Decoding and training-time suppression; outside a writing skill |
| Zamaraeva, Gude, Santos-Ríos, Gómez-Rodríguez, [The rise of antithesis in NLP papers](https://arxiv.org/abs/2610.10092) | arXiv 2026-10, preprint | "rather than" appears seven times as often in 2026 ACL-style papers as in 2019 ACL papers; two annotators seldom agreed on which uses annoy; the authors conjecture pairwise preference post-training as the cause |
| Boggia, Artificial Epanorthosis (arXiv 2607.21498) | arXiv 2026-07, preprint; read through [PsyPost coverage](https://www.psypost.org/one-of-ais-most-annoying-writing-habits-has-a-2000-year-old-history/) only | In small pilots on Qwen2.5-7B-Instruct, one prompt instruction cut the figure from 39.6 to 10.9 per 10,000 words in oratory and a self-rewriting pass reached zero |
| Rana, [Semantic Gravity Wells: Why Negative Constraints Backfire](https://arxiv.org/abs/2601.08070) | arXiv 2026-01, preprint; search summary only | On one open-weights model, naming a forbidden word in the prompt can prime it |
| Kommers et al., [Why Slop Matters](https://arxiv.org/abs/2601.06060) | ACM AI Letters per arXiv comment | Asymmetry of effort between writer and reader |
| Baltes, Cheong, Treude, [AI Slop and the Software Commons](https://arxiv.org/abs/2604.16754) | CACM per arXiv comment | Review cost lands on shared maintainer capacity |

Not opened and therefore not used: Graphite's "AI Tells" post that Wikipedia cites for corrective disclaimers, Geng and Trotta (arXiv 2404.08627), the Pangram technical report (arXiv 2402.14873), and the HackerOne statements seen only in search snippets. Liang et al., [Mapping the Increasing Use of LLMs in Scientific Papers](https://arxiv.org/abs/2404.01268), is listed by OpenReview at COLM without a year and was not used for a claim.
