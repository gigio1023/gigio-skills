#!/usr/bin/env python3
"""Report densities and locations of style patterns common in LLM-drafted prose.

Usage:
    python3 scripts/check_slop.py <draft.md> [--json]

A report for a reader, never a verdict. Counts and rates locate passages worth
rereading; they never grade a document, establish authorship, or justify a
deletion. A human technical document can score high and a generated one low.
The exit status is always 0.

Fenced code, blockquotes, headings, and tables are skipped with the same scanner
as check_draft.py; inline code, link targets, URLs, and double-quoted spans are
masked before counting. Each sentence is measured as Korean or English by its
script.

Korean: commas per 100 characters (whitespace excluded); commas right after a
connective ending (-고, -며, -지만, -면서, -아서/-어서, -는데, -면) per 100
sentences; sentences that open with 이는, 또한, 아울러, or 나아가. The ending
match is a regular expression without a morphological analyzer, so a noun that
ends in the same syllable can be counted and a verb excluded with a homograph
noun can be missed.

English: negation-contrast frames ("not just X but Y", "isn't X, it's Y",
"It's not X. It's Y.", "No X, no Y"), "serves as" and "stands as", "it's worth
noting", and 20 verb forms from the excess vocabulary of Kobak et al. (Science
Advances 2025; data at github.com/berenslab/llm-excess-vocab, MIT). The verbs
are the style verbs with the largest 2024 excess ratio after excluding the
underscore family, which names a character in technical text, and offering,
aligning, and aligns, whose ordinary product and ML senses dominate.

The only external baseline: in KatFish (ACL 2025, texts from 2024-era models),
human-written Korean abstracts had about 17 connective commas per 100 sentences
against 32 to 47 for LLM-generated ones. Genre, model generation, and this
script's approximation differ from that study, so the figure orients a reader
and is not a threshold.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

# `python3 -I` leaves the script's directory off sys.path, and the shared
# scanner lives in check_draft.py there, so add it before importing.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_draft import HEADING_RE, LIST_ITEM_RE, group_blocks, is_table_row, scannable_lines, split_sentences

MAX_SENTENCE_LEN = 120  # trim point for reported sentences
CATEGORY_ORDER = [
    "ko_connective_comma", "ko_initial_connective",
    "en_negation_contrast", "en_serves_as", "en_worth_noting", "en_llm_verb",
]

# Masked with spaces of equal length, so reported columns still match the source line.
MASKED_SPAN_RES = [
    re.compile(r"`[^`]*`"),
    re.compile(r"\]\([^)]*\)"),
    re.compile(r"https?://\S+"),
    re.compile(r"\"[^\"\n]*\"|“[^”\n]*”|「[^」\n]*」|『[^』\n]*』"),
]
MARKDOWN_IMAGE_RE = re.compile(r"^\s*!\[")
LIST_MARKER_RE = re.compile(r"^(\s*)([-*+]|\d+\.)(\s)")
LETTER_RE = re.compile(r"[^\W\d_]")
HANGUL_RE = re.compile(r"[가-힣]")
LATIN_RE = re.compile(r"[A-Za-z]")
ENGLISH_WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")

KO_COMMA_RE = re.compile(r"[,，]")
KO_WORD_BEFORE_COMMA_RE = re.compile(r"([가-힣]+)[,，]")
KO_CONNECTIVE_ENDINGS = (
    "면서", "지만", "는데", "은데", "인데",
    "아서", "어서", "여서", "해서", "와서", "워서", "봐서", "돼서", "져서", "쳐서", "려서", "나서", "내서", "라서",
    "고", "며", "면",
)
# Nouns and sentence-initial conjunctive adverbs that end in a connective syllable.
KO_NOT_CONNECTIVE = (
    "참고", "보고", "재고", "광고", "최고", "사고", "창고", "경고", "원고", "신고",
    "화면", "측면", "표면", "장면", "단면", "정면", "방면", "국면",
    "그리고", "하지만", "그러면",
)
KO_INITIAL_CONNECTIVE_RE = re.compile(r"^(이는|또한|아울러|나아가)(?=[\s,，]|$)")

APOSTROPHE = "['’]"
EN_NEGATION_CONTRAST_RES = [
    re.compile(r"\bnot (?:just|only|merely|simply)\b[^.!?;]{1,80}?\bbut\b", re.IGNORECASE),
    re.compile(
        rf"\b(?:is(?:n{APOSTROPHE}t| not)|are(?:n{APOSTROPHE}t| not)|was(?:n{APOSTROPHE}t| not))\b[^.!?;]{{1,60}}?"
        rf"[,;:—–]\s*(?:it{APOSTROPHE}s|it is|they{APOSTROPHE}re|they are|this is|that{APOSTROPHE}s)\b",
        re.IGNORECASE,
    ),
    re.compile(r"^No\s+\w[^,.;!?]{0,40},\s*no\s+\w[^,.;!?]{0,40}"),
]
# "It's not X. It's Y." spans two sentences; a long first sentence is ordinary exposition.
EN_NOT_OPENER_RE = re.compile(
    rf"^(?:it|this|that)(?:{APOSTROPHE}s| is) not\b|^(?:it|this|that) isn{APOSTROPHE}t\b", re.IGNORECASE
)
EN_IS_OPENER_RE = re.compile(rf"^(?:it|this|that)(?:{APOSTROPHE}s| is)\b(?! not\b)", re.IGNORECASE)
EN_NOT_OPENER_MAX_WORDS = 12
EN_SERVES_AS_RE = re.compile(r"\b(?:serves?|served|serving|stands?|stood) as\b", re.IGNORECASE)
EN_WORTH_NOTING_RE = re.compile(rf"\b(?:it{APOSTROPHE}s|it is) worth (?:noting|mentioning)\b", re.IGNORECASE)
# Recomputed from results/yearly-counts.csv.gz: 2024 frequency over the 2022 frequency plus twice
# the 2021-2022 rise, for words annotated "style" and "verb" in results/excess_words.csv.
EN_LLM_VERBS = (
    "delves", "delved", "showcasing", "delve", "surpassing", "delving", "excels", "garnered",
    "encompassed", "grappling", "emphasizing", "encompassing", "necessitating", "revolutionizing",
    "revolutionize", "consolidates", "showcases", "emphasising", "showcased", "surpasses",
)
EN_LLM_VERB_RE = re.compile(r"\b(?:" + "|".join(EN_LLM_VERBS) + r")\b", re.IGNORECASE)


@dataclass
class Sentence:
    line: int
    col: int
    text: str


@dataclass
class Hit:
    line: int
    col: int
    category: str
    match: str
    sentence: str


@dataclass
class KoreanCounts:
    sentences: int = 0
    characters: int = 0
    commas: int = 0
    connective_commas: int = 0
    initial_connectives: dict[str, int] = field(default_factory=dict)


@dataclass
class EnglishCounts:
    sentences: int = 0
    words: int = 0
    negation_contrast: int = 0
    serves_as: int = 0
    worth_noting: int = 0
    llm_verbs: int = 0


@dataclass
class Report:
    korean: KoreanCounts
    english: EnglishCounts
    hits: list[Hit]


def mask_spans(line: str) -> str:
    masked: str = line
    for pattern in MASKED_SPAN_RES:
        masked = pattern.sub(lambda m: " " * len(m.group(0)), masked)
    return masked


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Return (line number, masked line) for prose only, with a blank before each list item.

    check_draft's scanner drops fenced code and blockquotes. Headings, table rows,
    and image lines become blank so they never join a sentence. The blank inserted
    before a list item makes every item its own block, so an unterminated item is
    one sentence rather than part of the next.
    """
    out: list[tuple[int, str]] = []
    for line_no, line in scannable_lines(text.splitlines()):
        masked: str = mask_spans(line)
        if HEADING_RE.match(masked) or is_table_row(masked) or MARKDOWN_IMAGE_RE.match(masked):
            out.append((line_no, ""))
            continue
        if LIST_ITEM_RE.match(masked):
            out.append((line_no, ""))
            masked = LIST_MARKER_RE.sub(lambda m: m.group(1) + " " * len(m.group(2)) + m.group(3), masked, count=1)
        out.append((line_no, masked))
    return out


def sentences_of(text: str) -> list[Sentence]:
    sentences: list[Sentence] = []
    for block in group_blocks(prose_lines(text)):
        for line_no, col, sentence in split_sentences(block):
            if LETTER_RE.search(sentence):
                sentences.append(Sentence(line_no, col, sentence))
    return sentences


def is_korean(sentence: str) -> bool:
    """A Hangul syllable carries about as much as three or four Latin letters, so field terms stay Korean."""
    hangul: int = len(HANGUL_RE.findall(sentence))
    latin: int = len(LATIN_RE.findall(sentence))
    return hangul > 0 and hangul * 4 >= latin


def trim(text: str) -> str:
    return text if len(text) <= MAX_SENTENCE_LEN else text[:MAX_SENTENCE_LEN]


def is_connective_comma_word(word: str) -> bool:
    """True when the word before a comma ends in a connective; two-syllable nouns also end compounds (설정화면)."""
    if word in KO_NOT_CONNECTIVE or any(word.endswith(noun) for noun in KO_NOT_CONNECTIVE if len(noun) == 2):
        return False
    return word.endswith(KO_CONNECTIVE_ENDINGS)


def measure_korean(sentence: Sentence, counts: KoreanCounts, hits: list[Hit]) -> None:
    """Add one Korean sentence to the counts and record its hits; mutates both arguments."""
    counts.sentences += 1
    counts.characters += len(re.sub(r"\s", "", sentence.text))
    counts.commas += len(KO_COMMA_RE.findall(sentence.text))
    for m in KO_WORD_BEFORE_COMMA_RE.finditer(sentence.text):
        word: str = m.group(1)
        if is_connective_comma_word(word):
            counts.connective_commas += 1
            hits.append(Hit(sentence.line, sentence.col, "ko_connective_comma", word + ",", trim(sentence.text)))
    opener: re.Match[str] | None = KO_INITIAL_CONNECTIVE_RE.match(sentence.text)
    if opener:
        word = opener.group(1)
        counts.initial_connectives[word] = counts.initial_connectives.get(word, 0) + 1
        hits.append(Hit(sentence.line, sentence.col, "ko_initial_connective", word, trim(sentence.text)))


def measure_english(sentence: Sentence, following: Sentence | None, counts: EnglishCounts, hits: list[Hit]) -> None:
    """Add one English sentence to the counts and record its hits; mutates both arguments."""
    counts.sentences += 1
    counts.words += len(ENGLISH_WORD_RE.findall(sentence.text))
    found: list[tuple[str, str]] = []
    for pattern in EN_NEGATION_CONTRAST_RES:
        found.extend(("en_negation_contrast", m.group(0)) for m in pattern.finditer(sentence.text))
    if (
        following is not None
        and EN_NOT_OPENER_RE.match(sentence.text)
        and len(ENGLISH_WORD_RE.findall(sentence.text)) <= EN_NOT_OPENER_MAX_WORDS
        and EN_IS_OPENER_RE.match(following.text)
    ):
        found.append(("en_negation_contrast", sentence.text + " " + following.text.split(" ", 2)[0]))
    found.extend(("en_serves_as", m.group(0)) for m in EN_SERVES_AS_RE.finditer(sentence.text))
    found.extend(("en_worth_noting", m.group(0)) for m in EN_WORTH_NOTING_RE.finditer(sentence.text))
    found.extend(("en_llm_verb", m.group(0)) for m in EN_LLM_VERB_RE.finditer(sentence.text))
    for category, matched in found:
        hits.append(Hit(sentence.line, sentence.col, category, trim(matched), trim(sentence.text)))
    counts.negation_contrast += sum(1 for c, _ in found if c == "en_negation_contrast")
    counts.serves_as += sum(1 for c, _ in found if c == "en_serves_as")
    counts.worth_noting += sum(1 for c, _ in found if c == "en_worth_noting")
    counts.llm_verbs += sum(1 for c, _ in found if c == "en_llm_verb")


def analyze(text: str) -> Report:
    sentences: list[Sentence] = sentences_of(text)
    korean: KoreanCounts = KoreanCounts()
    english: EnglishCounts = EnglishCounts()
    hits: list[Hit] = []
    for index, sentence in enumerate(sentences):
        if is_korean(sentence.text):
            measure_korean(sentence, korean, hits)
        elif LATIN_RE.search(sentence.text):
            following: Sentence | None = sentences[index + 1] if index + 1 < len(sentences) else None
            measure_english(sentence, following, english, hits)
    hits.sort(key=lambda h: (h.line, h.col, CATEGORY_ORDER.index(h.category)))
    return Report(korean, english, hits)


def rate(count: int, denominator: int, per: int) -> float | None:
    return None if denominator == 0 else round(count * per / denominator, 2)


def rates_of(report: Report) -> dict[str, float | None]:
    ko: KoreanCounts = report.korean
    en: EnglishCounts = report.english
    return {
        "ko_commas_per_100_chars": rate(ko.commas, ko.characters, 100),
        "ko_connective_commas_per_100_sentences": rate(ko.connective_commas, ko.sentences, 100),
        "ko_initial_connectives_per_100_sentences": rate(sum(ko.initial_connectives.values()), ko.sentences, 100),
        "en_negation_contrast_per_100_sentences": rate(en.negation_contrast, en.sentences, 100),
        "en_serves_as_per_100_sentences": rate(en.serves_as, en.sentences, 100),
        "en_worth_noting_per_100_sentences": rate(en.worth_noting, en.sentences, 100),
        "en_llm_verbs_per_1000_words": rate(en.llm_verbs, en.words, 1000),
    }


def shown(value: float | None) -> str:
    return "n/a" if value is None else f"{value:g}"


def render_text(report: Report) -> str:
    ko: KoreanCounts = report.korean
    en: EnglishCounts = report.english
    r: dict[str, float | None] = rates_of(report)
    openers: str = ", ".join(f"{w}={n}" for w, n in sorted(ko.initial_connectives.items())) or "none"
    lines: list[str] = [f"{h.line}:{h.col}  {h.category}  {h.match}  | {h.sentence}" for h in report.hits]
    lines += [
        f"korean: {ko.sentences} sentences, {ko.characters} characters without whitespace",
        f"  commas: {ko.commas} ({shown(r['ko_commas_per_100_chars'])} per 100 characters)",
        f"  connective commas: {ko.connective_commas} ({shown(r['ko_connective_commas_per_100_sentences'])} per 100 sentences)",
        f"  sentence-initial 이는/또한/아울러/나아가: {sum(ko.initial_connectives.values())}"
        f" ({shown(r['ko_initial_connectives_per_100_sentences'])} per 100 sentences; {openers})",
        f"english: {en.sentences} sentences, {en.words} words",
        f"  negation-contrast frames: {en.negation_contrast} ({shown(r['en_negation_contrast_per_100_sentences'])} per 100 sentences)",
        f"  serves as / stands as: {en.serves_as} ({shown(r['en_serves_as_per_100_sentences'])} per 100 sentences)",
        f"  it's worth noting: {en.worth_noting} ({shown(r['en_worth_noting_per_100_sentences'])} per 100 sentences)",
        f"  LLM-era verbs: {en.llm_verbs} ({shown(r['en_llm_verbs_per_1000_words'])} per 1,000 words)",
        "These counts locate passages to reread; they do not grade the document.",
    ]
    return "\n".join(lines)


def render_json(report: Report) -> str:
    payload: dict[str, object] = {
        "korean": asdict(report.korean),
        "english": asdict(report.english),
        "rates": rates_of(report),
        "hits": [asdict(h) for h in report.hits],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Report densities and locations of style patterns common in LLM-drafted prose. "
            "Counts locate passages for a reader and never grade a document."
        ),
        epilog=(
            "Only external baseline: KatFish (ACL 2025, 2024-era models) found about 17 connective commas "
            "per 100 sentences in human Korean abstracts against 32 to 47 for LLMs. It is not a threshold."
        ),
    )
    parser.add_argument("draft", help="path to the Markdown draft")
    parser.add_argument("--json", action="store_true", help="print counts, rates, and hits as JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args: argparse.Namespace = parse_args(argv)
    text: str = Path(args.draft).read_text(encoding="utf-8")
    report: Report = analyze(text)
    print(render_json(report) if args.json else render_text(report))
    return 0  # a report for a reader, not a gate -- it never fails the run


if __name__ == "__main__":
    sys.exit(main())
