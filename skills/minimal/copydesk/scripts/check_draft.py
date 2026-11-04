"""Flag sentences and table cells in a Markdown draft that tend to draw editor deletions.

A linter for human review, not a gate: it never rewrites text and never
declares a document good or bad. Zero findings do not establish factual
accuracy, useful content, semantic fidelity, or clear reasoning. Every hit is a candidate for human judgment.
A condition that changes how a number should be read (a caveat, a scope
limit, a unit note) is legitimate even when it matches status_plan -- the
pattern only says "look here," not "cut this." Categories: self_description,
status_plan, order_narration, negation_definition, session_leak, long_cell,
opening_prose. session_leak marks text that points at the drafting conversation
or a session-only path (a temp directory, a scratchpad, a harness home) that the
reader cannot open; references inside the document, such as "the table above,"
are not session_leak.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field

MAX_TEXT_LEN = 120  # trim point for reported sentences/cells
OPENING_LINE_WINDOW = 12  # how many non-empty lines after the title count as the opening
CATEGORY_ORDER = [
    "self_description", "status_plan", "order_narration",
    "negation_definition", "long_cell", "opening_prose", "session_leak",
]
# "대신하지 못한다" states a real limit, not a negation-of-identity claim -- never flag it.
NEGATION_SAFE_PHRASE = "대신하지 못한다"

SELF_DESCRIPTION = [
    r"이 문서(는|에서)", r"본 문서", r"이 절(은|에서)", r"이 섹션",
    r"아래(?:에서|에는)?\s*(?:표|그림|절)", r"다음\s*(?:절|장)에서",
    r"읽는\s*(?:기준|길|순서)", r"펼쳐\s*(?:보|읽)", r"읽기\s*안내",
    r"하려는\s*일", r"정리한\s*것이다",
    # "설명한다." only counts when the subject is the document/section/table itself.
    r"(?:이|본|아래|다음)\s*(?:문서|절|표)[^.!?]*설명한다\.?$",
    r"^This (?:document|section|page)", r"^The following (?:table|figure|section)",
    r"^Below,", r"describes how to read",
]
STATUS_PLAN = [
    r"미확인", r"미확보", r"미측정", r"아직\s*(?:확인|검증|측정|실행)(?:하지|되지)",
    r"논의\s*중", r"예정이다", r"다음\s*(?:판본|단계)에서", r"추후", r"기준일",
    r"기준으로\s*확인", r"\d{4}년\s*\d{1,2}월\s*\d{1,2}일\s*(?:기준|확인)",
    r"not yet (?:verified|confirmed|measured)", r"as of \d",
    r"to be (?:decided|determined)", r"under discussion",
]
ORDER_NARRATION = [
    r"(?:최신|오래된)\s*(?:항목|순)?\s*(?:부터|순으로)\s*(?:나열|정렬)",
    r"순서(?:로|대로)\s*(?:정리|나열)", r"내림차순", r"오름차순",
    r"sorted by", r"ordered by",
]
NEGATION_DEFINITION = [
    # "아니라고 판정" reports someone else's verdict, so it is not a definition by negation.
    r"(?:이|가)\s*아니라(?!고\s*(?:판정|보|답|말))", r"(?:은|는)\s*아니다\.?$",
    r"(?:로|으로)\s*(?:해석|간주|취급)(?:하면|해서는)\s*안\s*된다",
    r"보장하(?:지\s*않|는\s*것은\s*아니)", r"의미하지\s*않는다",
    r"does not mean", r"is not a",
    r"should not be (?:read|interpreted) as", r"cannot be treated as",
]
# Each pattern names the conversation, its participants' requests, or a path that exists only on the
# drafting machine. A reference that a reader can resolve inside the document ("위 표", "the table
# above", "앞 절") is deliberately absent.
SESSION_LEAK = [
    r"\bas (?:we|you|I) (?:discussed|agreed|asked|requested|mentioned)\b",
    r"\bas (?:you )?requested\b", r"\bper your (?:request|instructions?)\b",
    r"\b(?:in|during|from) (?:this|our) (?:session|conversation|chat)\b",
    r"\bearlier in (?:this|our|the) (?:session|conversation|chat)\b",
    r"말씀(?:하신|드린|주신)", r"요청(?:하신|주신)\s*(?:대로|바)",
    # "이 대화형 모델" is a product description, not a reference to the drafting conversation.
    r"(?<![가-힣])(?:이|이번|우리)\s+대화(?!형)", r"(?<![가-힣])이번\s*세션",
    r"앞서\s*(?:논의|이야기|얘기)(?:한|했던|하신)",
    r"(?<![\w.])/(?:private/)?tmp/", r"\bscratchpad\b",
    r"(?:~|/Users/[^/\s]+|/home/[^/\s]+)/\.(?:claude|codex)/",
]
# IGNORECASE is harmless on the Korean patterns and needed for the English ones, so one compile covers both.
CATEGORY_PATTERNS = {
    "self_description": [re.compile(p, re.IGNORECASE) for p in SELF_DESCRIPTION],
    "status_plan": [re.compile(p, re.IGNORECASE) for p in STATUS_PLAN],
    "order_narration": [re.compile(p, re.IGNORECASE) for p in ORDER_NARRATION],
    "negation_definition": [re.compile(p, re.IGNORECASE) for p in NEGATION_DEFINITION],
    "session_leak": [re.compile(p, re.IGNORECASE) for p in SESSION_LEAK],
}

# A sentence boundary is any of ./!/? followed by whitespace or end-of-text; "다."/"요." are
# already period-terminated, so a single punctuation-class pattern covers the Korean cases too.
SENTENCE_END_RE = re.compile(r"[.!?](?=\s|$)")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s)")
HEADING_RE = re.compile(r"^\s*#{1,6}\s")
H1_RE = re.compile(r"^\s*#(?!#)\s")
IMAGE_OR_FIGURE_RE = re.compile(r"^\s*(?:!\[|그림\s*\d|Figure\s*\d)", re.IGNORECASE)
BLOCKQUOTE_RE = re.compile(r"^\s*>")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
@dataclass
class Finding:
    line: int
    col: int
    category: str
    text: str

@dataclass
class Block:
    start_line: int
    lines: list[tuple[int, str]] = field(default_factory=list)
    @property
    def kind(self) -> str:
        first = self.lines[0][1] if self.lines else ""
        if HEADING_RE.match(first):
            return "heading"
        if LIST_ITEM_RE.match(first):
            return "list"
        if IMAGE_OR_FIGURE_RE.match(first):
            return "image"
        if is_table_row(first):
            return "table"
        return "prose"

def is_table_row(line: str) -> bool:
    """A line is part of a table if it has at least two pipes outside a code span."""
    return line.count("|") >= 2

def scannable_lines(lines: list[str]) -> list[tuple[int, str]]:
    """Drop fenced code and blockquotes -- editors don't judge quoted or verbatim text this way."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for i, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or BLOCKQUOTE_RE.match(line):
            continue
        out.append((i, line))
    return out

def group_blocks(pairs: list[tuple[int, str]]) -> list[Block]:
    """Group by blank-line separation; table rows stay contiguous automatically since they're non-blank."""
    blocks: list[Block] = []
    current: Block | None = None
    for line_no, line in pairs:
        if line.strip() == "":
            current = None
            continue
        if current is None:
            current = Block(start_line=line_no)
            blocks.append(current)
        current.lines.append((line_no, line))
    return blocks

def split_sentences(block: Block) -> list[tuple[int, int, str]]:
    """Return (line, col, sentence) per sentence, mapping char offsets back to source lines."""
    chars: list[str] = []
    positions: list[tuple[int, int]] = []
    for idx, (line_no, line) in enumerate(block.lines):
        content = line.rstrip("\n")
        for col, ch in enumerate(content, start=1):
            chars.append(ch)
            positions.append((line_no, col))
        if idx != len(block.lines) - 1:
            chars.append(" ")
            positions.append((line_no, len(content) + 1))
    text = "".join(chars)

    sentences: list[tuple[int, int, str]] = []
    start = 0
    ends = [m.end() for m in SENTENCE_END_RE.finditer(text)]
    if not ends or ends[-1] != len(text):
        ends.append(len(text))
    for end in ends:
        raw = text[start:end]
        stripped = raw.strip()
        if stripped:
            lead = len(raw) - len(raw.lstrip())
            char_pos = start + lead
            line_no, col = positions[char_pos] if char_pos < len(positions) else (block.start_line, 1)
            sentences.append((line_no, col, stripped))
        start = end
    return sentences

def trim(text: str) -> str:
    return text if len(text) <= MAX_TEXT_LEN else text[:MAX_TEXT_LEN]

def check_sentence_categories(blocks: list[Block]) -> list[Finding]:
    findings: list[Finding] = []
    for block in blocks:
        if block.kind == "table":
            continue  # table cells are judged separately by check_long_cells
        for line_no, col, sentence in split_sentences(block):
            for category, patterns in CATEGORY_PATTERNS.items():
                if category == "negation_definition" and NEGATION_SAFE_PHRASE in sentence:
                    continue  # a real limit stated as "cannot replace X" is not a negated definition
                if any(p.search(sentence) for p in patterns):
                    findings.append(Finding(line_no, col, category, trim(sentence)))
    return findings

def check_long_cells(lines: list[str], max_cell: int) -> list[Finding]:
    """A cell that runs long, or hides a second sentence, forces the reader to parse prose inside a grid."""
    findings: list[Finding] = []
    in_fence = False
    for line_no, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or BLOCKQUOTE_RE.match(line):
            continue
        if not is_table_row(line) or TABLE_SEPARATOR_RE.match(line):
            continue
        col = 1
        for part in line.split("|"):
            cell = part.strip()
            cell_col = col + (len(part) - len(part.lstrip()))
            if cell:
                hides_second_sentence = bool(re.search(r"[.!?]\s+\S", cell))
                if len(cell) > max_cell or hides_second_sentence:
                    findings.append(Finding(line_no, cell_col, "long_cell", trim(cell)))
            col += len(part) + 1
    return findings

def check_opening_prose(lines: list[str]) -> list[Finding]:
    """Locate an opening paragraph worth reviewing; its length alone is not a defect."""
    pairs = scannable_lines(lines)
    h1_index = next((i for i, (_, line) in enumerate(pairs) if H1_RE.match(line)), None)
    window_start = 0 if h1_index is None else h1_index + 1
    non_empty = [p for p in pairs[window_start:] if p[1].strip() != ""]
    window = non_empty[:OPENING_LINE_WINDOW]
    if not window:
        return []
    window_line_nos = {ln for ln, _ in window}
    blocks = group_blocks([p for p in pairs if min(window_line_nos) <= p[0] <= max(window_line_nos)])
    for block in blocks:
        if block.kind == "prose" and len(split_sentences(block)) > 2:
            return [Finding(block.start_line, 1, "opening_prose", trim(block.lines[0][1].strip()))]
    return []

def analyze(text: str, max_cell: int) -> list[Finding]:
    lines = text.splitlines()
    blocks = group_blocks(scannable_lines(lines))
    findings = check_sentence_categories(blocks) + check_long_cells(lines, max_cell) + check_opening_prose(lines)
    findings.sort(key=lambda f: (f.line, f.col))
    return findings

def render_text(findings: list[Finding]) -> str:
    out_lines = [f"{f.line}:{f.col}  {f.category}  {f.text}" for f in findings]
    counts = {cat: sum(1 for f in findings if f.category == cat) for cat in CATEGORY_ORDER}
    parts = ", ".join(f"{cat}={counts[cat]}" for cat in CATEGORY_ORDER)
    out_lines.append(f"findings: {len(findings)} ({parts})")
    return "\n".join(out_lines)

def render_json(findings: list[Finding]) -> str:
    rows = [{"line": f.line, "col": f.col, "category": f.category, "text": f.text} for f in findings]
    return json.dumps(rows, ensure_ascii=False, indent=2)

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Flag editor-deletion-prone sentences and long table cells.")
    parser.add_argument("draft", help="path to the Markdown draft")
    parser.add_argument("--max-cell", type=int, default=60, help="max table cell length before flagging")
    parser.add_argument("--json", action="store_true", help="print findings as a JSON list")
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    with open(args.draft, encoding="utf-8") as f:
        text = f.read()
    findings = analyze(text, args.max_cell)
    print(render_json(findings) if args.json else render_text(findings))
    return 0  # a linter for review, not a gate -- it never fails the run

if __name__ == "__main__":
    sys.exit(main())
