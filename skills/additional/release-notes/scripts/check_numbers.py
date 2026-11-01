#!/usr/bin/env python3
"""Check that every number and ID in a rendered release note matches the data file.

Usage:
    python3 scripts/check_numbers.py --diff diff.json --html note.html [--md note.md] [--pdf note.pdf]

Checks, each reported with what it found:

- N1 the data file reconciles: list lengths equal the counts,
  ``before - removed + added = after``, ``shared = changed + minor_only + unchanged``,
  and every group balances
- N2 every number printed in the HTML and Markdown is a number the data file
  holds (version labels, refs, ISO dates, IDs, and code spans are not counts)
- N3 every ``data-count`` number in the HTML equals the current value at its
  path, which catches an HTML built from an older data file
- N4 every ID-shaped string exists in one of the two versions, and every
  added, removed, or changed ID appears in each output
- N5 the reconciliation identity is printed
- N6 the PDF text carries exactly the HTML's numbers, after removing the
  running header and page numbers; a stale or truncated PDF fails here

The PDF text is read with pypdf, which maps glyphs to characters only through
the PDF's own ToUnicode tables, as copy and paste does. A PDF whose glyphs
lack that mapping, such as one drawn with a font's stylistic alternates,
loses characters from IDs here (N4.pdf) even when the page image is right.

HTML and Markdown need only the standard library. ``--pdf`` needs pypdf:
run the script with ``uv run --with pypdf python scripts/check_numbers.py``.
Exit status 0 when every check passes, 1 when any fails, 2 on a setup or
input problem.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from _diff_data import DiffData, canonical_number, load_diff
from _errors import EnvironmentSetupError, ReleaseNoteError
from _inline import format_value, scan_literals

PAGE_NUMBER: re.Pattern[str] = re.compile(r"^\s*\d+\s*/\s*\d+\s*$")


@dataclass(frozen=True)
class Check:
    id: str
    name: str
    ok: bool
    found: Any


class _RenderedHtml(HTMLParser):
    """Visible text, code text, aria labels, data-count bindings, and the title of a note."""

    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []
        self.code: list[str] = []
        self.labels: list[str] = []
        self.bindings: list[tuple[str, str]] = []
        self.title: str = ""
        self._stack: list[str] = []
        self._binding: str | None = None
        self._bound: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes: dict[str, str | None] = dict(attrs)
        self._stack.append(tag)
        if attributes.get("aria-label"):
            self.labels.append(attributes["aria-label"] or "")
        if attributes.get("data-count"):
            self._binding, self._bound = attributes["data-count"], []

    def handle_endtag(self, tag: str) -> None:
        if self._binding is not None and tag == "span":
            self.bindings.append((self._binding, "".join(self._bound)))
            self._binding = None
        while self._stack:
            if self._stack.pop() == tag:
                break

    def handle_data(self, data: str) -> None:
        if "title" in self._stack:
            self.title += data
        elif any(t in self._stack for t in ("style", "script", "head")):
            return
        elif "code" in self._stack:
            self.code.append(data)
        else:
            self.text.append(data)
        if self._binding is not None:
            self._bound.append(data)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--diff", required=True)
    parser.add_argument("--html", required=True, help="the rendered note HTML; the PDF is compared against it")
    parser.add_argument("--md", help="the rendered GitHub release Markdown")
    parser.add_argument("--pdf", help="the rendered PDF (needs PyMuPDF)")
    args: argparse.Namespace = parser.parse_args(argv)
    try:
        diff: DiffData = load_diff(Path(args.diff))
        page = _RenderedHtml()
        page.feed(Path(args.html).read_text(encoding="utf-8"))
        checks: list[Check] = [_reconciles(diff)]
        html_text: str = " ".join(page.text)
        checks += _text_checks("html", html_text + " " + " ".join(page.labels), diff)
        checks.append(_bindings(page.bindings, diff))
        if args.md:
            md_text: str = re.sub(r"```(?!diff).*?```", " ", Path(args.md).read_text(encoding="utf-8"), flags=re.S)
            checks += _text_checks("md", md_text, diff)
        if args.pdf:
            pdf_text: str = _pdf_text(Path(args.pdf), page.title.strip())
            checks += _text_checks("pdf", pdf_text, diff)
            checks.append(_pdf_matches_html(pdf_text, " ".join(page.text + page.code), diff))
    except (ReleaseNoteError, OSError) as err:
        print(f"check_numbers: {err}", file=sys.stderr)
        return 2
    print(json.dumps({"diff": args.diff, "checks": [asdict(c) for c in checks]}, ensure_ascii=False, indent=1))
    return 0 if all(c.ok for c in checks) else 1


def _reconciles(diff: DiffData) -> Check:
    doc: dict[str, Any] = diff.document
    c: dict[str, int] = doc["counts"]
    problems: list[str] = []
    for name in ("added", "removed", "changed", "minor_only"):
        if len(doc[name]) != c[name]:
            problems.append(f"{name}: {len(doc[name])} listed, counts say {c[name]}")
    if len(doc["ids"]["old"]) != c["before"] or len(doc["ids"]["new"]) != c["after"]:
        problems.append("ID lists do not match before and after counts")
    if c["before"] - c["removed"] + c["added"] != c["after"]:
        problems.append(f"{c['before']} - {c['removed']} + {c['added']} != {c['after']}")
    if c["before"] - c["removed"] != c["shared"] or c["shared"] != c["changed"] + c["minor_only"] + c["unchanged"]:
        problems.append(f"shared {c['shared']} != changed + minor_only + unchanged")
    for name, g in doc["groups"].items():
        if g["before"] - g["removed"] - g["moved_out"] + g["added"] + g["moved_in"] != g["after"]:
            problems.append(f"group {name} does not balance")
    return Check("N1", "data file reconciles", not problems, problems)


def _text_checks(label: str, text: str, diff: DiffData) -> list[Check]:
    numbers, unknown_ids = scan_literals(text, diff)
    allowed: set[str] = diff.allowed_numbers()
    stray: list[str] = sorted({n for n in numbers if canonical_number(n) not in allowed})
    listed: list[str] = [e["id"] for s in ("added", "removed", "changed", "minor_only") for e in diff.document[s]]
    missing: list[str] = [i for i in listed if not re.search(rf"(?<![A-Za-z0-9_-]){re.escape(i)}(?![0-9_-])", text)]
    identity: str = diff.document["identities"][0]
    squashed: str = re.sub(r"\s+", " ", text.replace("−", "-"))
    return [
        Check(f"N2.{label}", f"numbers in the {label} come from the data file", not stray, stray),
        Check(f"N4.{label}", f"IDs in the {label} exist, and every listed ID appears",
              not unknown_ids and not missing, {"unknown": sorted(set(unknown_ids)), "missing": missing}),
        Check(f"N5.{label}", f"reconciliation identity printed in the {label}", identity in squashed, identity),
    ]


def _bindings(bindings: list[tuple[str, str]], diff: DiffData) -> Check:
    stale: list[str] = []
    for path, shown in bindings:
        expected: str = format_value(diff.resolve(path))
        if shown.strip() != expected:
            stale.append(f"{path}: shows {shown.strip()}, data file has {expected}")
    return Check("N3", f"{len(bindings)} bound numbers equal the data file", not stale, stale)


def _pdf_text(pdf: Path, title: str) -> str:
    """Text of every page without the running header and the page number lines."""
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as err:
        raise EnvironmentSetupError("--pdf needs pypdf: run `uv run --with pypdf python scripts/check_numbers.py ...`") from err
    lines: list[str] = []
    for page in PdfReader(pdf).pages:
        lines.extend(line for line in page.extract_text().splitlines() if not PAGE_NUMBER.match(line) and line.strip() != title)
    return " ".join(lines)


def _pdf_matches_html(pdf_text: str, html_text: str, diff: DiffData) -> Check:
    pdf_numbers: Counter[str] = Counter(canonical_number(n) for n in scan_literals(pdf_text, diff)[0])
    html_numbers: Counter[str] = Counter(canonical_number(n) for n in scan_literals(html_text, diff)[0])
    only_pdf: dict[str, int] = dict(pdf_numbers - html_numbers)
    only_html: dict[str, int] = dict(html_numbers - pdf_numbers)
    return Check("N6", "PDF text carries exactly the HTML's numbers", not only_pdf and not only_html,
                 {"only_in_pdf": only_pdf, "only_in_html": only_html})


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
