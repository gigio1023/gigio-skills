# Public anti-slop skills and linters

Read on 2026-11-25 at the pinned revisions below. Files were fetched as text; nothing was installed or executed. Stars and last-commit dates come from the GitHub API on that day. A license is taken from the repository's LICENSE file; a license named only in frontmatter or the API is marked.

## Sources copydesk already adopted

Copydesk adapted these on 2026-11-04 ([authoring and revision, Sources](../../skills/minimal/copydesk/references/authoring-and-revision.md#sources)). All have moved since.

| Source | Adopted | Head on 2026-11-25 | Structural change since adoption |
| --- | --- | --- | --- |
| [blader/humanizer](https://github.com/blader/humanizer) | `0ef9fe5bc357` | `a32f2440` | None; wording, a 4.0.0 release, and a guard that treats injected operator notes as material |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | `f6fbc0015ce8` | `8678c864` | Lexical only: hedge-stack and parenthetical-hedge patterns, a generated Vale style |
| [adewale/anti-slop-writing](https://github.com/adewale/anti-slop-writing) | `5cf773433c6c` | `262db2d1` | New `evals/oracles/slop_lint.py`: span reports that never fail; run detectors for three or more "no X" items or three consecutive sentences with one first word |
| [EveryInc ce-noslop](https://github.com/EveryInc/compound-engineering-plugin) | `a3bcedfc7136` | `fcb5e3ad` | An edit changes only the failing span and keeps facts from deleted spans; a note records that this narrowing let unnamed tells through |
| [MaxWolf-01/agents writing-for-humans](https://github.com/MaxWolf-01/agents) | `851789cccd16` | `b2c6d947` | Catalogue entries with keep conditions; no mechanical check |

## New sources

### tbhb/vale-ai-tells

- [Repository](https://github.com/tbhb/vale-ai-tells/tree/51f646e366ba7c9dcb078ebeae345b7ff353eb3b) at `51f646e3`, MIT, 142 stars, last commit 2026-10-11.
- A Vale style of about 150 regex rules, a separate commit-message package, and experimental Tengo scripts. Runs under Vale only; no network, no edits.
- `ContentDuplication.tengo` flags a paragraph whose word-set Jaccard with an earlier one exceeds 0.60, but only within one section, so a summary that restates the details passes. `CataphoricForecasting` flags "Three pillars..." openers and documents that Vale cannot see whether the list follows. `CommitAttribution` flags `Co-Authored-By: Claude` lines in commits, the only public rule found that treats a meta line in the wrong field as a defect.
- Borrowed: the duplication design (strip non-prose, word sets, flag the later copy), extended across sections in `check_structure.py`; separate rules per surface.
- Not borrowed: about 50 figurative-verb rules ("lands", "ships", "surfaces") that fire on ordinary technical verbs.

### eric-tramel/slop-guard

- [Repository](https://github.com/eric-tramel/slop-guard/tree/7ef2113c52f1b4765287f90ac0741b2051d66fcb) at `7ef2113c`, MIT, 169 stars, last commit 2026-07-09.
- Python CLI and MCP server scoring about 25 rules; `apps/fit.py` fits thresholds from a reference corpus. `phrase_reuse` counts 4- to 8-word phrases that recur three or more times across the whole document.
- Borrowed: none directly. Threshold fitting on the owner's accepted reports is a reasonable next step once enough of them exist.
- Not borrowed: the 0 to 100 composite score, which hides which section repeats; English word lists.

### theclaymethod/unslop

- [Repository](https://github.com/theclaymethod/unslop/tree/0f4a07f5ca8bb400b4d4450b00d67c6e4a30b85a) at `0f4a07f5`, 1,228 stars, last commit 2026-11-14. No LICENSE file; `SKILL.md` frontmatter says MIT, which is not a grant. Ideas only, no code.
- `scripts/silhouette_scan.py` measures an intro that previews the outline (`heading_preview`, `preview_fulfillment`) and a recap loop: content words in the first third, absent from the middle, returning at the end (`callback_content`). Thresholds come from a committed human reference set, and a `--genre docs` flag exempts specs, which legitimately reprise. `validate_preservation.py` requires numbers, negations, and scope words to survive a rewrite.
- Borrowed: the preservation idea, as the instruction to compare scope notes before and after a revision.
- Not borrowed: voice mimicry and rubric gates. The recap-loop metric targets essays whose ending loops to the intro; a fixed-field report repeats results field by field, which the cross-section counter measures more directly.

### JensHeitmann/humanizer-stack

- [Repository](https://github.com/JensHeitmann/humanizer-stack/tree/13f5c023189d428ffba726c75886ca1fd0dcba65) at `13f5c023`, MIT, 387 stars, last commit 2026-07-24.
- Its structural skill outlines the piece first and notes where the main point is stated and how many times, then audits the outline.
- Borrowed: counting how many sections carry each result, which `check_structure.py` now does for quantities and sentences.
- Not borrowed: the goal of reading as human and its fixes (named feelings, tangents, reader address), which conflict with a dry report.

### epoko77-ai/im-not-ai

- [Repository](https://github.com/epoko77-ai/im-not-ai/tree/e9793d75a584169108906ee5f7332b27898efef4) at `e9793d75`, MIT, 6,773 stars, last commit 2026-11-23. Korean.
- A 71-pattern Korean taxonomy and rewrite gates. C-6 deletes a summary line under every heading ("이 섹션에서는 ~를 다룬다"); G-3 counts balance hedges with a document threshold scoped to reports; a gate fails a rewrite that changes the number of hedges and modals.
- Borrowed: Korean scope-note phrases in the checker; the preservation gate as the before-and-after scope-note comparison.
- Not borrowed: whole-text rewriting by an agent chain; connective-comma rules that `check_slop.py` already covers.

### DanRWilloughby/snifftest

- [Repository](https://github.com/DanRWilloughby/snifftest/tree/3db51a7db644b7cc5a6e9486abf4e6186bd58989) at `3db51a7d`, MIT, 38 stars, last commit 2026-10-23.
- Regex rules plus judgment rules sent to an LLM API after a consent step. `restating_closer` exempts a closer that adds a number, mechanism, or condition. `self_undercutting` is off by default because documentation must state its limits. `snifftest eval` seeds one defect per rule into the user's clean text to measure recall and false alarms.
- Borrowed: the exemption logic, as the rule that a scope note stays when it limits a claim.
- Not borrowed: sending paragraphs of private reports to a third-party API.

### Other sources read

| Source | Revision | License | Note |
| --- | --- | --- | --- |
| [Syntaf/vale-llm-slop](https://github.com/Syntaf/vale-llm-slop/tree/4dda3ec6426efa219e493d88396ed5c0471f7454) | `4dda3ec6` | MIT | `VagueReasons`, `ProcessNarration`; lexical |
| [FeedHive/ai-slop-detector](https://github.com/FeedHive/ai-slop-detector/tree/95d550706040191b0e75f1d89296a648bacb126e) | `95d55070` | MIT | 120 patterns, mostly social copy; synonym cycling matches the existing one-term rule |
| [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop/tree/a906154bef375d9d49ed2ad7da13b2db16f0d3d2) | `a906154b` | MIT | Names "Fractal Summaries" and "One-Point Dilution" as review items; prompt only |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop/tree/8da1f030185bdfe8471220585162991eaeb970e9) | `8da1f030` | MIT | Self-scored 1 to 10 dimensions; nothing structural beyond copydesk |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer/tree/94b88b23703bed7df507acae7d6d5876209a0cdf) | `94b88b23` | MIT | Keeps evidence-tied hedges; a counterweight to caveat counting |
| [sam-paech/slop-score](https://github.com/sam-paech/slop-score/tree/289264ab2a0df1358ef81ced3c259610ea709514), [antislop-sampler](https://github.com/sam-paech/antislop-sampler/tree/0ae330e98fbe6f09351f2d1063a51956378a44b2) | `289264ab`, `0ae330e9` | MIT with a separate `wordfreq.js` license; Apache-2.0 | Model ranking and decoding-time bans; they do not review one document |
| [MohamedAbdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop/tree/0cf9e9e4c5a73dfef6484574cee4e52fb03603b8) | `0cf9e9e4` | MIT | Writes session hooks into `~/.codex` and offers an anti-detector mode; not borrowed |

## Coverage

No public tool found counts the same number or result across sections, measures the density of "not tested" sentences, or flags a parenthetical pointer such as "(next sections)". Within-section duplication, whole-document phrase reuse, intro-preview and recap metrics, sentence and paragraph length variance, and lexical hedge stacks exist. Register is handled only by per-surface rule sets (Vale's commit package) and genre flags. `check_structure.py` combines the cross-section duplication idea with a quantity counter and a scope-note list; that combination is this pack's, not a published method.
