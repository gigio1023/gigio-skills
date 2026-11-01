#!/usr/bin/env python3
"""Check that every number and ID in a rendered release note matches the data file.

Usage:
    python3 scripts/check_numbers.py --diff diff.json --html note.html [--md note.md] [--pdf note.pdf]

Checks, each reported with what it found:

- N1 the data file reconciles: list lengths equal the counts,
  ``before - removed + added = after``, ``shared = changed + minor_only + unchanged``,
  and every group balances
- N2 every number printed in the HTML, Markdown, and PDF is a number the
  data file holds; version labels, refs, ISO dates, IDs, code spans, URLs,
  and words in which a letter directly precedes a digit (``v4.0``,
  ``3e1f09a7``, ``제3자``) are not numbers, the rule the builder applies to
  note.json
- N3 every ``data-count`` number in the HTML equals the current value at its
  path, which catches an HTML built from an older data file
- N4 every ID-shaped string exists in one of the two versions, and every
  added, removed, or changed ID appears in each output; a note built with
  ``full_list: omit`` marks that in the HTML, and then only the cited IDs
  are checked, because the data file carries the full list
- N5 the reconciliation identity is printed
- N6 the PDF's prose carries exactly the HTML prose's numbers, and the PDF
  text holds every figure text, code span, URL, and identifier word that has
  a digit; a stale or truncated PDF fails here
- N7 every ``data-label`` in the HTML reads the one label its path has in
  ``assets/strings.json`` for the note's language, and its number is bound
  to the same path; a merge count under the removed label fails here

The PDF text is read with pypdf, which maps glyphs to characters only through
the PDF's own ToUnicode tables, as copy and paste does. A PDF whose glyphs
lack that mapping, such as one drawn with a font's stylistic alternates,
loses characters from IDs here (N4.pdf) even when the page image is right.

The PDF checks read prose only. Text extraction joins adjacent boxes without
a space: SVG text runs (``2.0`` and ``3e1f09a7`` read ``2.03e1f09a7``) and
neighboring cells (``우선순위`` and ``4`` read ``우선순위4``). It also drops
code markup and breaks long URLs across lines. So every figure text, code
span, URL, and identifier word such as ``v4.0`` that the HTML holds is
removed from the PDF text first, matched with any whitespace between its
characters, and the rest is read without the word rule. Figure numbers are
checked in the HTML, where each text run is its own node.

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
from collections.abc import Callable
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

# `python3 -I` leaves the script's directory off sys.path, and the sibling
# modules live there, so add it before importing them.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _diff_data import DiffData, canonical_number, load_diff
from _errors import EnvironmentSetupError, ReleaseNoteError
from _inline import URL, format_value, identifier_words, scan_joined, scan_literals
from _note_content import expected_label, load_strings

PAGE_NUMBER: re.Pattern[str] = re.compile(r"^\s*\d+\s*/\s*\d+\s*$")
# scan_literals for text whose words are intact, scan_joined for PDF text.
Scan = Callable[[str, DiffData], tuple[list[str], list[str]]]


@dataclass(frozen=True)
class Check:
    id: str
    name: str
    ok: bool
    found: Any


class _RenderedHtml(HTMLParser):
    """The text of a rendered note, split by how the number check reads it.

    ``text`` is prose: sentences, table cells, and labels drawn as HTML text.
    ``figures`` holds the drawn text runs of each inline SVG, ``code`` each
    code span, and ``urls`` each address printed in prose. ``labels`` holds
    accessible text that is not drawn: aria labels and SVG titles and
    descriptions. Also collected: data-count and data-label bindings, the
    document language, and its title.
    """

    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []
        self.figures: list[list[str]] = []
        self.code: list[str] = []
        self.urls: list[str] = []
        self.labels: list[str] = []
        self.bindings: list[tuple[str, str]] = []
        self.label_bindings: list[tuple[str, str]] = []
        self.lang: str = ""
        self.full_list_omitted: bool = False
        self.title: str = ""
        self._stack: list[str] = []
        # One open binding at a time: (attribute, path, tag, collected text). Bound elements do not nest.
        self._open: tuple[str, str, str, list[str]] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes: dict[str, str | None] = dict(attrs)
        if tag == "svg" and "svg" not in self._stack:
            self.figures.append([])
        self._stack.append(tag)
        if attributes.get("aria-label"):
            self.labels.append(attributes["aria-label"] or "")
        if attributes.get("data-full-list") == "omitted":
            self.full_list_omitted = True
        if tag == "html":
            self.lang = attributes.get("lang") or ""
        for attribute in ("data-count", "data-label"):
            if attributes.get(attribute):
                self._open = (attribute, attributes[attribute] or "", tag, [])

    def handle_endtag(self, tag: str) -> None:
        if self._open is not None and tag == self._open[2]:
            attribute, path, _, text = self._open
            (self.bindings if attribute == "data-count" else self.label_bindings).append((path, "".join(text)))
            self._open = None
        while self._stack:
            if self._stack.pop() == tag:
                break

    def handle_data(self, data: str) -> None:
        if "svg" in self._stack:
            if "title" in self._stack or "desc" in self._stack:
                self.labels.append(data)
            elif data.strip():
                self.figures[-1].append(data)
        elif "title" in self._stack:
            self.title += data
        elif any(t in self._stack for t in ("style", "script", "head")):
            return
        elif "code" in self._stack:
            self.code.append(data)
        else:
            self.text.append(data)
            self.urls.extend(URL.findall(data))
        if self._open is not None:
            self._open[3].append(data)

    def non_prose(self) -> list[str]:
        """Each figure's text, code span, and printed URL: the strings the PDF comparison removes."""
        figures: list[str] = ["".join(runs) for runs in self.figures if runs]
        return [text for text in figures + self.code + self.urls if text.strip()]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--diff", required=True)
    parser.add_argument("--html", required=True, help="the rendered note HTML; the PDF is compared against it")
    parser.add_argument("--md", help="the rendered GitHub release Markdown")
    parser.add_argument("--pdf", help="the rendered PDF (needs pypdf)")
    args: argparse.Namespace = parser.parse_args(argv)
    try:
        diff: DiffData = load_diff(Path(args.diff))
        page = _RenderedHtml()
        page.feed(Path(args.html).read_text(encoding="utf-8"))
        checks: list[Check] = [_reconciles(diff)]
        html_prose: str = " ".join(page.text)
        figure_text: str = " ".join(run for runs in page.figures for run in runs)
        complete: bool = not page.full_list_omitted
        checks += _text_checks("html", " ".join([html_prose, figure_text, *page.labels]), diff, complete, scan_literals)
        checks.append(_bindings(page.bindings, diff))
        checks.append(_labels(page, diff))
        if args.md:
            md_text: str = re.sub(r"```(?!diff).*?```", " ", Path(args.md).read_text(encoding="utf-8"), flags=re.S)
            checks += _text_checks("md", md_text, diff, complete, scan_literals)
        if args.pdf:
            non_prose: list[str] = page.non_prose() + identifier_words(html_prose, diff)
            pdf_prose, not_in_pdf = _pdf_prose(_pdf_text(Path(args.pdf), page.title.strip()), non_prose)
            checks += _text_checks("pdf", pdf_prose, diff, complete, scan_joined)
            checks.append(_pdf_matches_html(pdf_prose, html_prose, not_in_pdf, diff))
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


def _text_checks(label: str, text: str, diff: DiffData, complete: bool, scan: Scan) -> list[Check]:
    numbers, unknown_ids = scan(text, diff)
    allowed: set[str] = diff.allowed_numbers()
    stray: list[str] = sorted({n for n in numbers if canonical_number(n) not in allowed})
    listed: list[str] = [e["id"] for s in ("added", "removed", "changed", "minor_only") for e in diff.document[s]]
    missing: list[str] = [i for i in listed if complete and not re.search(rf"(?<![A-Za-z0-9_-]){re.escape(i)}(?![0-9_-])", text)]
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


def _labels(page: _RenderedHtml, diff: DiffData) -> Check:
    """Each labelled count reads its path's label, so a merge count cannot sit under the removed label."""
    strings: dict[str, str] = load_strings(page.lang)
    roles: dict[str, str | None] = diff.document["roles"]
    bound_paths: set[str] = {path for path, _ in page.bindings}
    wrong: list[str] = []
    for path, shown in page.label_bindings:
        expected: str | None = expected_label(path, strings, roles)
        if expected is not None and shown.strip() != expected:
            wrong.append(f"{path}: labelled {shown.strip()!r}, should read {expected!r}")
        if path not in bound_paths:
            wrong.append(f"{path}: labelled but its number is not bound to the same path")
    return Check("N7", f"{len(page.label_bindings)} count labels read their path's label", not wrong, wrong)


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


def _pdf_prose(pdf_text: str, non_prose: list[str]) -> tuple[str, list[str]]:
    """Remove each non-prose string of the HTML from the PDF text once; also return those with a digit that are missing.

    Non-prose strings are figure texts, code spans, URLs, and identifier
    words. A string matches with any whitespace between its characters,
    because extraction joins SVG text runs and breaks long URLs across lines.
    Longer strings go first, and a match never starts or ends inside a
    number, so a short code span cannot cut digits out of a longer string or
    a count.
    """
    missing: list[str] = []
    for text in sorted(non_prose, key=len, reverse=True):
        spaced: str = r"\s*".join(re.escape(ch) for ch in text if not ch.isspace())
        match: re.Match[str] | None = re.search(rf"(?<!\d)(?<!\d[.,]){spaced}(?!\d)(?![.,]\d)", pdf_text)
        if match is None:
            # A missing string without a digit leaves no number behind; one with a digit is a stale or truncated PDF.
            if re.search(r"\d", text):
                missing.append(text)
            continue
        pdf_text = pdf_text[: match.start()] + " " + pdf_text[match.end() :]
    return pdf_text, missing


def _pdf_matches_html(pdf_prose: str, html_prose: str, not_in_pdf: list[str], diff: DiffData) -> Check:
    pdf_numbers: Counter[str] = Counter(canonical_number(n) for n in scan_joined(pdf_prose, diff)[0])
    html_numbers: Counter[str] = Counter(canonical_number(n) for n in scan_literals(html_prose, diff)[0])
    only_pdf: dict[str, int] = dict(pdf_numbers - html_numbers)
    only_html: dict[str, int] = dict(html_numbers - pdf_numbers)
    return Check("N6", "PDF prose carries exactly the HTML prose's numbers, and the PDF holds the HTML's other strings with digits",
                 not only_pdf and not only_html and not not_in_pdf,
                 {"only_in_pdf": only_pdf, "only_in_html": only_html, "not_in_pdf": not_in_pdf})


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
