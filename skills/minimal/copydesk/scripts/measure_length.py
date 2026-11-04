#!/usr/bin/env python3
"""Count words under each Markdown heading, and compare two versions of a document.

Usage:
    python3 scripts/measure_length.py <before.md> [<after.md>] [--json]

With one file, it prints the words in each section and the total. With two, it
matches sections by heading text (and occurrence, for repeated headings) and
prints each section's word count before and after, the change in words, and
the percent change, then the same for the whole document. A section present in
only one version is reported as removed or added.

A word is a whitespace-separated token that contains a letter or digit, so
Korean is counted by space-separated units (어절) and Markdown punctuation such
as table pipes, bullets, and rules is not. A section's words are those between
its heading and the next heading of any level, excluding the heading line;
fenced code and tables count because the reader sees them. Headings inside
fenced code are not headings.

The numbers support a revision summary in which the editor tags each change
CUT, MERGE, MOVE, CONDENSE, or PRESERVE; the script never assigns a tag, and a
shorter version is not by itself a better one. The exit status is always 0.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

# `python3 -I` leaves the script's directory off sys.path, and the shared
# Markdown patterns live in check_draft.py there, so add it before importing.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_draft import FENCE_RE, HEADING_RE

MAX_TITLE_LEN = 48  # trim point for headings in the text table
PREAMBLE_TITLE = "(before first heading)"
WORD_RE = re.compile(r"\S*[^\W_]\S*")
HEADING_PARTS_RE = re.compile(r"^\s*(#{1,6})\s+(.*?)\s*#*\s*$")


@dataclass
class Section:
    level: int  # 0 for text before the first heading
    title: str
    words: int


@dataclass
class SectionChange:
    level: int
    title: str
    before: int | None
    after: int | None

    @property
    def status(self) -> str:
        if self.before is None:
            return "added"
        if self.after is None:
            return "removed"
        return ""

    @property
    def change(self) -> int:
        return (self.after or 0) - (self.before or 0)

    @property
    def percent(self) -> float | None:
        if not self.before or self.after is None:
            return None
        return round(self.change * 100 / self.before, 1)


def parse_sections(text: str) -> list[Section]:
    sections: list[Section] = [Section(0, PREAMBLE_TITLE, 0)]
    in_fence: bool = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        heading: re.Match[str] | None = None if in_fence or not HEADING_RE.match(line) else HEADING_PARTS_RE.match(line)
        if heading:
            sections.append(Section(len(heading.group(1)), heading.group(2), 0))
            continue
        sections[-1].words += len(WORD_RE.findall(line))
    if sections[0].words == 0 and len(sections) > 1:
        sections.pop(0)
    return sections


def keyed(sections: list[Section]) -> list[tuple[tuple[str, int], Section]]:
    """Key each section by its title and the occurrence of that title, so repeated headings pair in order."""
    seen: Counter[str] = Counter()
    out: list[tuple[tuple[str, int], Section]] = []
    for section in sections:
        seen[section.title] += 1
        out.append(((section.title, seen[section.title]), section))
    return out


def compare(before: list[Section], after: list[Section]) -> list[SectionChange]:
    """Rows in the before order, then sections that exist only after the revision, in their order."""
    after_by_key: dict[tuple[str, int], Section] = dict(keyed(after))
    before_keys: set[tuple[str, int]] = {key for key, _ in keyed(before)}
    rows: list[SectionChange] = []
    for key, section in keyed(before):
        match: Section | None = after_by_key.get(key)
        rows.append(SectionChange(section.level, section.title, section.words, match.words if match else None))
    for key, section in keyed(after):
        if key not in before_keys:
            rows.append(SectionChange(section.level, section.title, None, section.words))
    return rows


def display_width(text: str) -> int:
    """Terminal columns: Hangul and other East Asian wide characters take two."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def label(level: int, title: str) -> str:
    """The heading as a left column cell, indented by level and cut to MAX_TITLE_LEN display columns."""
    text: str = title if level == 0 else "  " * (level - 1) + "#" * level + " " + title
    if display_width(text) > MAX_TITLE_LEN:
        while display_width(text) > MAX_TITLE_LEN - 3:
            text = text[:-1]
        text += "..."
    return text + " " * (MAX_TITLE_LEN - display_width(text))


def signed(value: int) -> str:
    return f"{value:+d}" if value else "0"


def percent_text(row: SectionChange) -> str:
    if row.status:
        return row.status
    if row.percent is None:
        return "n/a"
    return "0.0%" if row.percent == 0 else f"{row.percent:+.1f}%"


def render_single(sections: list[Section]) -> str:
    total: int = sum(s.words for s in sections)
    lines: list[str] = [f"{label(0, 'section')}  {'words':>7}"]
    lines += [f"{label(s.level, s.title)}  {s.words:>7}" for s in sections]
    lines.append(f"{label(0, 'total')}  {total:>7}")
    return "\n".join(lines)


def render_comparison(rows: list[SectionChange]) -> str:
    before_total: int = sum(r.before or 0 for r in rows)
    after_total: int = sum(r.after or 0 for r in rows)
    total_row: SectionChange = SectionChange(0, "total", before_total, after_total)

    def line(name: str, row: SectionChange) -> str:
        before: str = "-" if row.before is None else str(row.before)
        after: str = "-" if row.after is None else str(row.after)
        return f"{name}  {before:>7}  {after:>7}  {signed(row.change):>7}  {percent_text(row):>8}"

    header: str = f"{label(0, 'section')}  {'before':>7}  {'after':>7}  {'change':>7}  {'percent':>8}"
    return "\n".join([header] + [line(label(r.level, r.title), r) for r in rows] + [line(label(0, "total"), total_row)])


def comparison_json(rows: list[SectionChange]) -> dict[str, object]:
    before_total: int = sum(r.before or 0 for r in rows)
    after_total: int = sum(r.after or 0 for r in rows)
    total_row: SectionChange = SectionChange(0, "total", before_total, after_total)
    return {
        "sections": [
            {**asdict(r), "change": r.change, "percent": r.percent, "status": r.status or None} for r in rows
        ],
        "total": {"before": before_total, "after": after_total, "change": total_row.change, "percent": total_row.percent},
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Count words per Markdown heading; with two files, report each section's change in words and percent. "
            "Supports a revision summary with CUT, MERGE, MOVE, CONDENSE, or PRESERVE tags, which the editor assigns."
        )
    )
    parser.add_argument("before", help="the Markdown document, or its version before revision")
    parser.add_argument("after", nargs="?", help="the revised version to compare with BEFORE")
    parser.add_argument("--json", action="store_true", help="print the counts as JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args: argparse.Namespace = parse_args(argv)
    before: list[Section] = parse_sections(Path(args.before).read_text(encoding="utf-8"))
    if args.after is None:
        if args.json:
            print(json.dumps({"sections": [asdict(s) for s in before], "total": sum(s.words for s in before)},
                             ensure_ascii=False, indent=2))
        else:
            print(render_single(before))
        return 0
    rows: list[SectionChange] = compare(before, parse_sections(Path(args.after).read_text(encoding="utf-8")))
    print(json.dumps(comparison_json(rows), ensure_ascii=False, indent=2) if args.json else render_comparison(rows))
    return 0  # a measurement for the editor, not a gate -- it never fails the run


if __name__ == "__main__":
    sys.exit(main())
