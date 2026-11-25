#!/usr/bin/env python3
"""Locate document-level repetition and scope notes that sentence-level checks cannot see.

Usage:
    python3 scripts/check_structure.py <file.md> [<file.md> ...] [--level N] [--json]

A report for a reader, never a verdict. A summary may restate the main result
once, and a needed limit belongs beside its claim; the output only shows where
to read the document as a whole. The exit status is 0 after a run and 2
when an input file is missing.

Sections are split at headings of level N or shallower. By default N is the
shallowest heading level that occurs at least twice, so a title above four
field headings splits at the fields. Several files are read as the fields of
one form: each file is one section named after the file, unless --level is
given, in which case each file splits at that level too.

Fenced code and blockquotes are skipped. Inline code, link targets, and URLs
are masked, so identifiers, line anchors, and commit hashes never count as
quantities; quoted spans are masked too, so a quoted example is not a finding. Table rows count for quantities but not for sentences.

Findings:
  repeated_quantity  a measured quantity (a number with a unit, a dimension
                     such as 1024 x 768, or a number of four or more digits)
                     that appears in at least --min-sections sections.
  restated_sentence  a sentence whose content words and quantities largely
                     match a sentence in another section.
  scope_note         a sentence that says what was not run, tested, measured,
                     or written. Listed with its section so the notes can be
                     compared with the claims they limit; most are legitimate.
  vague_pointer      a pointer to another part of the document that names no
                     heading, such as "(next sections)" or "see below".

The summary also prints words per section, the share each holds, and scope
notes per 1,000 words.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

# `python3 -I` leaves the script's directory off sys.path, and the shared
# scanner lives in check_draft.py there, so add it before importing.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_draft import SENTENCE_END_RE, Block, group_blocks, is_table_row, scannable_lines

MAX_TEXT_LEN = 120
HEADING_LEVEL_RE = re.compile(r"^\s*(#{1,6})\s+(.*?)\s*#*\s*$")
LIST_MARKER_RE = re.compile(r"^(\s*)([-*+]|\d+\.)(\s)")
MASKED_SPAN_RES = [
    re.compile(r"`[^`]*`"),
    re.compile(r"\]\([^)]*\)"),
    re.compile(r"https?://\S+"),
    re.compile(r"\b[0-9a-f]{7,40}\b"),
    re.compile(r"\"[^\"\n]*\"|“[^”\n]*”|「[^」\n]*」|『[^』\n]*』"),  # quoted spans; keep last
]
# Dates, versions, and issue numbers name things; they are not measured results.
NAME_LIKE_RES = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\bv?\d+\.\d+\.\d+(?:[.\w+-]*)\b"),
    re.compile(r"#\d+\b"),
    re.compile(r"\b[A-Z]{2,}[-‑]\d[\w-]*"),
    re.compile(r"\b\d{1,2}:\d{2}\b"),
    re.compile(r"(?<![\d,.])(?:19|20)\d{2}(?![\d,.])"),  # years
]
NUMBER = r"\d[\d,]*(?:\.\d+)?"
UNIT = (
    r"(?:[KMGT]i?B|bytes?|B|ms|µs|ns|s|sec|seconds?|min|minutes?|h|hours?|%|x|"
    r"tokens?|req/s|rps|qps|fps|°C|W|GHz|MHz|"
    r"바이트|초|분|시간|개|건|회|배|명|장|줄)"
)
QUANTITY_RE = re.compile(
    rf"(?<![\w.]){NUMBER}\s*[×xX]\s*{NUMBER}(?![\w.])"  # dimensions
    rf"|(?<![\w.]){NUMBER}\s?{UNIT}(?![A-Za-z])"  # number with unit
    rf"|(?<![\w.])\d{{1,3}}(?:,\d{{3}})+(?:\.\d+)?(?![\w.])"  # 1,234,567
    rf"|(?<![\w.,])\d{{4,}}(?:\.\d+)?(?![\w.,])"  # 4+ digits
)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]+|[가-힣]{2,}")
STOPWORDS = frozenset(
    "the a an and or of to in on for with by from at as is are was were be been being this that these "
    "those it its into than then when while which who what where whose not no can could may might will "
    "would should does did do has have had also only each every same other such both one two any all "
    "there their they them our we you your his her about after before over under per via but if so".split()
)
SCOPE_NOTE_RES = [
    re.compile(
        r"\b(?:was|were|is|are|been)\s+not\s+(?:\w+\s+)?(?:tested|run|executed|measured|verified|checked|"
        r"reproduced|evaluated|confirmed|attempted|benchmarked)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:did|do|does|could)\s+not\s+(?:test|run|execute|measure|verify|check|reproduce|evaluate|try)\b", re.IGNORECASE),
    re.compile(r"\b(?:is|was|were|are|remains?|left)\s+(?:untested|unverified|unmeasured)\b", re.IGNORECASE),
    re.compile(r"\bnot (?:part of|in) the (?:archive|package|attachments?|PoC)\b|\bnot part of\s{2,}", re.IGNORECASE),  # masked code
    re.compile(r"\bno\s+(?:\w+\s+){0,2}(?:was|were)\s+(?:written|tested|run|measured|built|attempted)\b", re.IGNORECASE),
    re.compile(r"\bread in the source\b|\bsource[- ]only\b|\bnot (?:yet )?(?:tested|run|measured)\b", re.IGNORECASE),
    re.compile(r"(?:확인|실행|측정|검증|시험|재현|테스트)(?:하지|되지|을\s*하지|는\s*하지)\s*(?:않았|못했|않음|못함)"),
    re.compile(r"미확인|미측정|미검증|미실행"),
]
VAGUE_POINTER_RES = [
    re.compile(r"\(\s*(?:see\s+)?(?:the\s+)?(?:next|following|previous|later|earlier|below|above)\s+sections?\s*\)", re.IGNORECASE),
    re.compile(r"\b(?:see|described|explained|discussed|covered|shown)\s+(?:below|above|later|earlier)\b", re.IGNORECASE),
    re.compile(r"\bas\s+(?:noted|mentioned|described|explained|discussed|shown|stated)\s+(?:above|below|earlier|before|previously)\b", re.IGNORECASE),
    re.compile(r"\bin\s+(?:the\s+)?(?:next|following|previous|later)\s+sections?\b", re.IGNORECASE),
    re.compile(r"(?:앞|뒤|아래|위)(?:에서|의)\s*(?:말한|설명한|설명할|다룬|다룰|본|볼)"),
    re.compile(r"(?:다음|이후|뒤)\s*(?:절|장|섹션)(?:에서|을\s*보|참고)"),
]
RESTATED_MIN_SHARED = 5
RESTATED_MIN_JACCARD = 0.45
RESTATED_MIN_QUANTITIES = 3
CATEGORY_ORDER = ["repeated_quantity", "restated_sentence", "scope_note", "vague_pointer"]


@dataclass
class Section:
    name: str
    source: str
    start_line: int
    lines: list[tuple[int, str]] = field(default_factory=list)


@dataclass
class Sentence:
    section: int
    source: str
    line: int
    text: str
    masked: str
    words: frozenset[str]
    quantities: frozenset[str]


@dataclass
class Finding:
    category: str
    source: str
    line: int
    section: str
    text: str
    detail: str = ""


def trim(text: str) -> str:
    return text if len(text) <= MAX_TEXT_LEN else text[: MAX_TEXT_LEN - 3] + "..."


def mask(line: str, quotes: bool = True) -> str:
    for pattern in MASKED_SPAN_RES if quotes else MASKED_SPAN_RES[:-1]:
        line = pattern.sub(lambda m: " " * len(m.group(0)), line)
    return line


def heading_level(line: str) -> tuple[int, str] | None:
    match = HEADING_LEVEL_RE.match(line)
    return (len(match.group(1)), match.group(2)) if match else None


def default_level(texts: list[str]) -> int:
    counts: dict[int, int] = defaultdict(int)
    for text in texts:
        for _, line in scannable_lines(text.splitlines()):
            found = heading_level(line)
            if found:
                counts[found[0]] += 1
    repeated = [level for level, count in counts.items() if count >= 2]
    return min(repeated) if repeated else 6


def split_sections(text: str, source: str, level: int) -> list[Section]:
    sections: list[Section] = []
    current = Section(Path(source).stem, source, 1)
    for line_no, line in scannable_lines(text.splitlines()):
        found = heading_level(line)
        if found and found[0] <= level:
            if any(content.strip() for _, content in current.lines):
                sections.append(current)
            current = Section(found[1], source, line_no)
            continue
        current.lines.append((line_no, line))
    if any(content.strip() for _, content in current.lines):
        sections.append(current)
    return sections


def quantities_of(text: str) -> list[str]:
    for pattern in NAME_LIKE_RES:
        text = pattern.sub(lambda m: " " * len(m.group(0)), text)
    found: list[str] = []
    for match in QUANTITY_RE.finditer(text):
        token = re.sub(r"\s+", " ", match.group(0).strip())
        token = re.sub(r"\s*[×xX]\s*(?=\d)", " × ", token)
        found.append(token.replace(",", ""))
    return found


def prose_lines(section: Section) -> tuple[list[tuple[int, str]], dict[int, str]]:
    """Masked prose lines for splitting, plus the original lines for display.

    Table rows, headings, and images become blanks; each list item starts its
    own block. Masking keeps every line's length, so offsets in the masked text
    are offsets in the original.
    """
    out: list[tuple[int, str]] = []
    original: dict[int, str] = {}
    for line_no, line in section.lines:
        masked = mask(line)
        if heading_level(masked) or is_table_row(masked) or masked.lstrip().startswith("!["):
            out.append((line_no, ""))
            continue
        if LIST_MARKER_RE.match(masked):
            out.append((line_no, ""))
            masked = LIST_MARKER_RE.sub(lambda m: m.group(1) + " " * len(m.group(2)) + m.group(3), masked, count=1)
            line = LIST_MARKER_RE.sub(lambda m: m.group(1) + " " * len(m.group(2)) + m.group(3), line, count=1)
        out.append((line_no, masked))
        original[line_no] = line
    return out, original


def split_block(block: Block, original: dict[int, str]) -> list[tuple[int, str, str]]:
    """(line, masked sentence, original sentence) with check_draft's sentence boundaries."""
    masked = " ".join(line.rstrip("\n") for _, line in block.lines)
    shown = " ".join(original[n].rstrip("\n") for n, _ in block.lines)
    starts: list[int] = []
    offset = 0
    for line_no, line in block.lines:
        starts.append(offset)
        offset += len(line.rstrip("\n")) + 1
    ends = [m.end() for m in SENTENCE_END_RE.finditer(masked)]
    if not ends or ends[-1] != len(masked):
        ends.append(len(masked))
    result: list[tuple[int, str, str]] = []
    begin = 0
    for end in ends:
        piece = masked[begin:end]
        if piece.strip():
            lead = begin + len(piece) - len(piece.lstrip())
            index = max(i for i, s in enumerate(starts) if s <= lead)
            result.append((block.lines[index][0], piece.strip(), " ".join(shown[begin:end].split())))
        begin = end
    return result


def sentences_of(sections: list[Section]) -> list[Sentence]:
    result: list[Sentence] = []
    for index, section in enumerate(sections):
        lines, original = prose_lines(section)
        for block in group_blocks(lines):
            for line_no, masked, shown in split_block(block, original):
                words = frozenset(w.lower() for w in WORD_RE.findall(masked) if w.lower() not in STOPWORDS)
                if words:
                    result.append(Sentence(index, section.source, line_no, shown, masked, words, frozenset(quantities_of(masked))))
    return result


def word_count(section: Section) -> int:
    return sum(
        len(WORD_RE.findall(mask(line, quotes=False))) + len(re.findall(r"\d[\d,.]*", mask(line, quotes=False)))
        for _, line in section.lines
    )


def repeated_quantities(sections: list[Section], min_sections: int) -> list[Finding]:
    where: dict[str, dict[int, tuple[str, int]]] = defaultdict(dict)
    for index, section in enumerate(sections):
        for line_no, line in section.lines:
            for token in quantities_of(mask(line)):
                where[token].setdefault(index, (section.source, line_no))
    findings: list[Finding] = []
    for token, hits in where.items():
        if len(hits) >= min_sections:
            first = min(hits)
            source, line_no = hits[first]
            spots = "; ".join(f"{sections[i].name} ({Path(hits[i][0]).name}:{hits[i][1]})" for i in sorted(hits))
            findings.append(Finding("repeated_quantity", source, line_no, sections[first].name, token, f"{len(hits)} sections: {spots}"))
    findings.sort(key=lambda f: (-int(f.detail.split()[0]), f.text))
    return findings


def restated_sentences(sentences: list[Sentence], sections: list[Section]) -> list[Finding]:
    findings: list[Finding] = []
    for i, first in enumerate(sentences):
        for second in sentences[i + 1 :]:
            if second.section == first.section:
                continue
            shared = first.words & second.words
            jaccard = len(shared) / len(first.words | second.words)
            shared_quantities = first.quantities & second.quantities
            if (len(shared) >= RESTATED_MIN_SHARED and jaccard >= RESTATED_MIN_JACCARD) or len(shared_quantities) >= RESTATED_MIN_QUANTITIES:
                detail = (
                    f"{sections[second.section].name} ({Path(second.source).name}:{second.line}): {trim(second.text)}"
                    f" [word overlap {jaccard:.2f}, shared quantities {len(shared_quantities)}]"
                )
                findings.append(Finding("restated_sentence", first.source, first.line, sections[first.section].name, trim(first.text), detail))
    return findings


def pattern_findings(sentences: list[Sentence], sections: list[Section], category: str, patterns: list[re.Pattern[str]]) -> list[Finding]:
    return [
        Finding(category, s.source, s.line, sections[s.section].name, trim(s.text))
        for s in sentences
        if any(p.search(s.masked) for p in patterns)
    ]


def analyze(paths: list[str], level: int | None, min_sections: int) -> dict:
    texts = [Path(p).read_text(encoding="utf-8") for p in paths]
    # Several files are the fields of one form: each file is one section unless a level is given.
    split_level = level or (0 if len(texts) > 1 else default_level(texts))
    sections: list[Section] = []
    for path, text in zip(paths, texts):
        sections.extend(split_sections(text, path, split_level))
    sentences = sentences_of(sections)
    findings = (
        repeated_quantities(sections, min_sections)
        + restated_sentences(sentences, sections)
        + pattern_findings(sentences, sections, "scope_note", SCOPE_NOTE_RES)
        + pattern_findings(sentences, sections, "vague_pointer", VAGUE_POINTER_RES)
    )
    words = [word_count(s) for s in sections]
    total = sum(words) or 1
    scope_notes = sum(1 for f in findings if f.category == "scope_note")
    return {
        "level": split_level,
        "sections": [
            {"name": s.name, "source": s.source, "line": s.start_line, "words": w, "share": round(w / total, 3)}
            for s, w in zip(sections, words)
        ],
        "total_words": sum(words),
        "scope_notes_per_1000_words": round(scope_notes * 1000 / total, 1),
        "findings": [asdict(f) for f in findings],
    }


def render_text(report: dict) -> str:
    out: list[str] = []
    for category in CATEGORY_ORDER:
        rows = [f for f in report["findings"] if f["category"] == category]
        if not rows:
            continue
        out.append(f"== {category} ({len(rows)})")
        for f in rows:
            where = f"{Path(f['source']).name}:{f['line']}"
            if category == "repeated_quantity":
                out.append(f"  {f['text']}  {f['detail']}")
            elif category == "restated_sentence":
                out.append(f"  {where} [{f['section']}] {f['text']}")
                out.append(f"    ~ {f['detail']}")
            else:
                out.append(f"  {where} [{f['section']}] {f['text']}")
    split = f"heading level {report['level']}" if report["level"] else "file"
    out.append(f"sections (split by {split}):")
    for s in report["sections"]:
        out.append(f"  {s['words']:>6} words  {s['share'] * 100:5.1f}%  {s['name']}")
    counts = {c: sum(1 for f in report["findings"] if f["category"] == c) for c in CATEGORY_ORDER}
    out.append(
        f"total {report['total_words']} words; scope notes per 1,000 words: {report['scope_notes_per_1000_words']}; "
        + ", ".join(f"{c}={n}" for c, n in counts.items())
    )
    out.append("These locate passages to read as a whole; they do not grade the document.")
    return "\n".join(out)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Locate cross-section repetition, scope notes, and vague pointers.")
    parser.add_argument("files", nargs="+", help="Markdown files, read in order as one document")
    parser.add_argument("--level", type=int, choices=range(1, 7), help="split at headings of this level or shallower")
    parser.add_argument("--min-sections", type=int, default=3, help="sections a quantity must appear in (default 3)")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    missing = [p for p in args.files if not Path(p).is_file()]
    if missing:
        print(f"check_structure.py: not a readable file: {', '.join(missing)}", file=sys.stderr)
        return 2
    report = analyze(args.files, args.level, args.min_sections)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
