#!/usr/bin/env python3
"""Build the HTML and Markdown release note from note.json and diff.json.

Usage:
    python3 scripts/build_note.py --note note.json --diff diff.json --out-dir out/

Writes ``<stem>.html`` (the HTML deliverable and the PDF source) and
``<stem>.md`` (the GitHub release body), where the stem defaults to the note
file's stem. Before writing anything it refuses a note whose prose types a
number by hand or names an ID that exists in neither version: numbers enter
the note only through ``{{...}}`` tokens that resolve against diff.json.
Code spans, URLs, version labels, refs, ISO dates, and words in which a letter
directly precedes a digit, such as ``v4.0``, the commit ``3e1f09a7``, or
``제3자``, may contain digits; ``_inline.scan_literals`` holds the rule.

Python 3.11+ and the standard library only. Exit status 0 on success, 2 when
the note source or data file breaks its contract (the message lists every
problem found).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# `python3 -I` leaves the script's directory off sys.path, and the sibling
# modules live there, so add it before importing them.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _diff_data import DiffData, load_diff
from _errors import NoteSourceError, ReleaseNoteError
from _html_note import render_document
from _inline import scan_literals
from _markdown_note import render_markdown_note
from _note_content import NoteContent
from _note_source import Note, load_note


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--note", required=True, help="note source, note.json")
    parser.add_argument("--diff", required=True, help="data file written by version_diff.py")
    parser.add_argument("--out-dir", required=True, help="directory for the .html and .md outputs")
    parser.add_argument("--stem", help="output file name without extension (default: the note file's stem)")
    args: argparse.Namespace = parser.parse_args(argv)
    try:
        diff: DiffData = load_diff(Path(args.diff))
        note: Note = load_note(Path(args.note), diff)
        _refuse_literals(note, diff)
        content: NoteContent = NoteContent(note, diff)
        document: str = render_document(content)
        markdown: str = render_markdown_note(content)
    except ReleaseNoteError as err:
        print(f"build_note: {err}", file=sys.stderr)
        return 2
    out_dir: Path = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem: str = args.stem or Path(args.note).stem
    html_path: Path = out_dir / f"{stem}.html"
    md_path: Path = out_dir / f"{stem}.md"
    html_path.write_text(document, encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    print(f"wrote {html_path}")
    print(f"wrote {md_path}")
    return 0


def _refuse_literals(note: Note, diff: DiffData) -> None:
    problems: list[str] = []
    for where, text in note.prose():
        numbers, unknown_ids = scan_literals(text, diff)
        if numbers:
            problems.append(f"{where}: typed number(s) {', '.join(numbers)}; use a {{{{...}}}} token from {diff.path.name}"
                            " or add the value with version_diff.py --facts")
        if unknown_ids:
            problems.append(f"{where}: {', '.join(unknown_ids)} exist(s) in neither version")
    if problems:
        raise NoteSourceError("the note source cites values the data file does not hold:\n  " + "\n  ".join(problems))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
