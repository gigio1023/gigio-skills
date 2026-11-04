#!/usr/bin/env python3
"""Countable checks on a rendered release-note PDF, plus page images for the visual read.

Usage:
    uv run --with pymupdf python scripts/check_pdf.py note.pdf --html note.html \\
        [--expected-pages N] [--png-dir pages/] [--dpi 100]

Reads the PDF with PyMuPDF and the source HTML for its headings, figure
titles, and text. Prints one JSON report; each check has a threshold, the
measured value, and ``ok``. With ``--png-dir`` it also writes one PNG per page,
a contact sheet of all pages, and a grayscale contact sheet for the
as-is and to-be distinction. The checks gate defects and drift; they do not
replace reading the page images.

A check that could not run has ``ok: null`` and the reason as its value, such
as D24 on a PDF without a text layer or D25 on a PDF that no Chromium printed;
the report lists it under ``skipped`` and stderr names it.

Exit status 0 when every check passes, 1 when any fails, 2 when none fails but
a check could not run, and 2 on a setup or input problem.
"""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

try:
    import pymupdf
except ModuleNotFoundError:
    print("check_pdf: PyMuPDF is missing; run it as `uv run --with pymupdf python scripts/check_pdf.py ...`", file=sys.stderr)
    sys.exit(2)

MIN_FONT_PT: float = 8.0
MAX_FONT_SIZES: int = 8
MAX_HUE_FAMILIES: int = 3
MAX_CHROMA_SHARE: float = 0.05
CHROMA_LEVEL: int = 31  # 0.12 of 255: below this spread between channels a color counts as neutral
MIN_INK_SHARE: float = 0.005
MAX_FIGURES_PER_PAGE: int = 2
# D25: Chromium rounds layout to whole CSS px, so a full-width table ends up to 0.2 pt past its page clip.
CLIP_TOLERANCE_PT: float = 0.75

# D24: characters that must not sit at the edge of a wrapped line.
CLOSERS: str = ")]}\uff09\uff3d\uff5d\u3009\u300b\u300d\u300f\u3011\u3015\u3017\u3019\u301b\u201d\u2019\u00bb"
OPENERS: str = "([{\uff08\uff3b\uff5b\u3008\u300a\u300c\u300e\u3010\u3014\u3016\u3018\u301a\u201c\u2018\u00ab"
EDGE_PUNCTUATION: str = ".,!?:;\u2026\u00b7\"'" + CLOSERS + OPENERS
HANGUL_SYLLABLE = re.compile(r"[\uac00-\ud7a3]")
SYMBOL_UNITS: tuple[str, ...] = ("%", "\u2030", "\u2103", "\u00b0", "\u339c", "\u339d", "\u339e", "\u338f")
LATIN_UNITS: frozenset[str] = frozenset(
    "pt px mm cm km kg mg ms ns KB MB GB TB KiB MiB GiB TiB Hz kHz MHz GHz dpi fps".split())
# Korean counters and unit nouns; one counts only when the source wrote it against the number, as in 12개.
KOREAN_UNITS: tuple[str, ...] = tuple(sorted(
    ("개 개월 건 명 년 월 일 시 시간 분 초 주 쪽 장 회 번 배 원 달러 "
     "위 차 종 줄 자 단계 가지 곳 권 대 점 퍼센트 포인트 행 열 항목 세").split(), key=len, reverse=True))
CURRENCY_PREFIXES: str = "$\u20a9\u20ac\u00a3\u00a5"


@dataclass(frozen=True)
class Check:
    id: str
    name: str
    threshold: str
    value: Any
    ok: bool | None  # None: the check could not run, and value says why


@dataclass(frozen=True)
class _Line:
    """One printed line: PyMuPDF lines on one baseline that touch, merged."""

    page: int
    x0: float
    top: float
    x1: float
    bottom: float
    size: float
    text: str


class _SourceOutline(HTMLParser):
    """Collect heading texts and figure titles from the note HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.headings: list[str] = []
        self.figure_titles: list[str] = []
        self.opening: list[str] = []
        self.text: list[str] = []  # all character data outside <head>, for D24
        self._section_depth: int = 0  # > 0 inside <section class="summary">
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._in_head: bool = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes: str = dict(attrs).get("class") or ""
        if tag == "head":
            self._in_head = True
        if tag == "section":
            self._section_depth += 1 if self._section_depth or "summary" in classes.split() else 0
        if tag in ("h1", "h2", "h3"):
            self._capture, self._buffer = "heading", []
        elif tag == "p" and "fig-title" in classes.split():
            self._capture, self._buffer = "figure", []

    def handle_endtag(self, tag: str) -> None:
        if tag == "head":
            self._in_head = False
        if tag == "section" and self._section_depth:
            self._section_depth -= 1
        if self._capture == "heading" and tag in ("h1", "h2", "h3"):
            self.headings.append(_squash("".join(self._buffer)))
            self._capture = None
        elif self._capture == "figure" and tag == "p":
            self.figure_titles.append(_squash("".join(self._buffer)))
            self._capture = None

    def handle_data(self, data: str) -> None:
        if not self._in_head:
            self.text.append(data)
        if self._capture:
            self._buffer.append(data)
        if self._section_depth:
            self.opening.append(data)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("pdf")
    parser.add_argument("--html", required=True, help="the HTML the PDF was printed from")
    parser.add_argument("--expected-pages", type=int, help="page count recorded before the build")
    parser.add_argument("--png-dir", help="write page PNGs and contact sheets here")
    parser.add_argument("--dpi", type=int, default=100)
    args: argparse.Namespace = parser.parse_args(argv)
    pdf_path, html_path = Path(args.pdf), Path(args.html)
    for path in (pdf_path, html_path):
        if not path.is_file():
            print(f"check_pdf: {path} does not exist", file=sys.stderr)
            return 2
    source = _SourceOutline()
    source.feed(html_path.read_text(encoding="utf-8"))
    document = pymupdf.open(pdf_path)
    checks: list[Check] = _run_checks(document, source, args.expected_pages)
    skipped: list[Check] = [c for c in checks if c.ok is None]
    report: dict[str, Any] = {"pdf": str(pdf_path), "pages": document.page_count, "checks": [asdict(c) for c in checks],
                              "skipped": [{"id": c.id, "reason": c.value} for c in skipped]}
    if args.png_dir:
        report["images"] = _write_images(document, Path(args.png_dir), args.dpi)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    for check in skipped:
        print(f"check_pdf: {check.id} did not run: {check.value}", file=sys.stderr)
    if any(c.ok is False for c in checks):
        return 1
    return 2 if skipped else 0


def _run_checks(document: Any, source: _SourceOutline, expected_pages: int | None) -> list[Check]:
    sizes: set[float] = set()
    colors: list[tuple[int, int, int]] = []
    overlaps: list[str] = []
    outside: list[str] = []
    blank: list[int] = []
    chroma: dict[int, float] = {}
    figures: dict[int, int] = {}
    stranded: list[str] = []
    headings: set[str] = set(source.headings)
    for number, page in enumerate(document, start=1):
        spans: list[dict[str, Any]] = [
            span for block in page.get_text("dict")["blocks"] if block["type"] == 0
            for line in block["lines"] for span in line["spans"] if span["text"].strip()
        ]
        for span in spans:
            sizes.add(round(span["size"], 1))
            colors.append(_int_rgb(span["color"]))
            x0, y0, x1, y1 = span["bbox"]
            if x0 < page.rect.x0 - 1 or x1 > page.rect.x1 + 1 or y1 > page.rect.y1 + 1:
                outside.append(f"p{number}: {span['text'][:30]}")
        for drawing in page.get_drawings():
            for key in ("fill", "color"):
                if drawing.get(key):
                    colors.append(tuple(round(v * 255) for v in drawing[key][:3]))  # type: ignore[arg-type]
        overlaps.extend(_overlapping_words(page, number))
        ink, chromatic = _pixel_shares(page)
        chroma[number] = round(chromatic, 4)
        if ink < MIN_INK_SHARE:
            blank.append(number)
        text: str = _squash(page.get_text())
        figures[number] = sum(1 for title in source.figure_titles if title and title in text)
        last: str = _last_body_line(spans, page)
        if last in headings:
            stranded.append(f"p{number}: {last}")
    hue_families: list[int] = sorted({int(_hue(c) // 30) * 30 for c in colors if max(c) - min(c) >= CHROMA_LEVEL})
    catalog: str = document.xref_object(document.pdf_catalog())
    language: str | None = (m.group(1) if (m := re.search(r"/Lang\s*\(([^)]*)\)", catalog)) else None)
    outline: int = len(document.get_toc())
    return [
        Check("D1", "accent hue families in the document", f"<= {MAX_HUE_FAMILIES}", hue_families,
              len(hue_families) <= MAX_HUE_FAMILIES),
        Check("D2", "chromatic pixel share per page", f"<= {MAX_CHROMA_SHARE}", chroma,
              all(v <= MAX_CHROMA_SHARE for v in chroma.values())),
        Check("D4", "distinct font sizes in pt", f"<= {MAX_FONT_SIZES}", sorted(sizes), len(sizes) <= MAX_FONT_SIZES),
        Check("D5", "smallest font size in pt", f">= {MIN_FONT_PT}", min(sizes) if sizes else None,
              bool(sizes) and min(sizes) >= MIN_FONT_PT - 0.05),
        Check("D6", "figures per page", f"<= {MAX_FIGURES_PER_PAGE}", figures,
              all(v <= MAX_FIGURES_PER_PAGE for v in figures.values())),
        Check("D7", "overlapping word boxes", "0", overlaps[:10], not overlaps),
        Check("D16", "text outside the page", "0", outside[:10], not outside),
        Check("D17", "page count and blank pages",
              (f"pages == {expected_pages}, " if expected_pages else "") + f"no page under {MIN_INK_SHARE:.1%} ink",
              {"pages": document.page_count, "blank": blank},
              not blank and (expected_pages is None or document.page_count == expected_pages)),
        Check("D18", "outline, tags, language", f"outline == {len(source.headings)} headings, tagged, /Lang set",
              {"outline": outline, "tagged": "/StructTreeRoot" in catalog, "lang": language},
              outline == len(source.headings) and "/StructTreeRoot" in catalog and bool(language)),
        Check("D21", "heading left at the bottom of a page", "0", stranded, not stranded),
        _opening_on_first_page(document, source),
        _korean_line_breaks(document, source),
        _drawn_past_page_clip(document),
    ]


def _korean_line_breaks(document: Any, source: _SourceOutline) -> Check:
    """D24: line breaks that strand a syllable, a bracket, or a unit, located by page.

    A finding needs the source HTML to run the two lines together, so table cells,
    chart labels, and other separate texts that happen to sit one above the other
    are not read as a wrapped line.
    """
    name, threshold = "Korean line breaks: lone syllable, bracket or quote at a line edge, number split from its unit", "0"
    lines: list[_Line] = [line for number, page in enumerate(document, start=1) for line in _printed_lines(page, number)]
    if not lines:
        return Check("D24", name, threshold, "the PDF has no text layer, so its line breaks cannot be read", None)
    joined: str = re.sub(r"\s+", "", "".join(source.text))
    spaced: str = _squash("".join(source.text))
    found: dict[str, list[str]] = {"lone syllable": [], "closing mark starts a line": [],
                                   "opening mark ends a line": [], "number split from its unit": []}
    for line, above in _wrapped_pairs(lines, joined):
        where: str = f"p{line.page}: \u2026{above.text[-14:]} \u23ce {line.text[:14]}"
        core: str = line.text.strip().strip(EDGE_PUNCTUATION).strip()
        if len(core) == 1 and HANGUL_SYLLABLE.fullmatch(core):
            found["lone syllable"].append(where)
        head, tail = line.text.lstrip(), above.text.rstrip()
        if head[:1] in CLOSERS or (head[:1] == '"' and tail.count('"') % 2 == 1):
            found["closing mark starts a line"].append(where)
        if tail[-1:] in OPENERS or (tail[-1:] == '"' and tail.count('"') % 2 == 1):
            found["opening mark ends a line"].append(where)
        if _splits_number_from_unit(tail, head, spaced):
            found["number split from its unit"].append(where)
    report: dict[str, Any] = {kind: places[:10] for kind, places in found.items() if places}
    return Check("D24", name, threshold, report, not report)


def _printed_lines(page: Any, number: int) -> list[_Line]:
    pieces: list[_Line] = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans: list[dict[str, Any]] = line["spans"]
            text: str = "".join(span["text"] for span in spans)
            if text.strip():
                x0, top, x1, bottom = line["bbox"]
                pieces.append(_Line(number, x0, top, x1, bottom, max(span["size"] for span in spans), text))
    pieces.sort(key=lambda p: (round(p.bottom), p.x0))
    merged: list[_Line] = []
    for piece in pieces:
        last: _Line | None = merged[-1] if merged else None
        # PyMuPDF splits a printed line at a font change; a gap wider than 0.6 em is a table column or a chart label.
        if last and abs(last.bottom - piece.bottom) < 1 and -1 < piece.x0 - last.x1 < 0.6 * piece.size:
            space: str = " " if piece.x0 - last.x1 > 0.15 * piece.size and not last.text.endswith(" ") else ""
            merged[-1] = _Line(number, last.x0, min(last.top, piece.top), piece.x1, max(last.bottom, piece.bottom),
                               max(last.size, piece.size), last.text + space + piece.text)
        else:
            merged.append(piece)
    return merged


def _wrapped_pairs(lines: list[_Line], joined_source: str) -> list[tuple[_Line, _Line]]:
    """Each printed line with the line above it, when both belong to one wrapped run of source text."""
    pairs: list[tuple[_Line, _Line]] = []
    for line in lines:
        above: list[_Line] = [
            other for other in lines
            if other.page == line.page and other is not line and other.bottom <= line.top + 1
            and line.top - other.bottom < 0.8 * line.size and other.x0 - 2 <= line.x0 < other.x1
        ]
        if not above:
            continue
        previous: _Line = max(above, key=lambda other: other.bottom)
        seam: str = re.sub(r"\s+", "", previous.text)[-12:] + re.sub(r"\s+", "", line.text)[:12]
        if seam and seam in joined_source:
            pairs.append((line, previous))
    return pairs


def _splits_number_from_unit(tail: str, head: str, spaced_source: str) -> bool:
    first: str = head.split()[0] if head.split() else ""
    if tail[-1:] in CURRENCY_PREFIXES and head[:1].isdigit():
        return True
    if not tail[-1:].isdigit():
        return False
    if head.startswith(SYMBOL_UNITS) or first.rstrip(EDGE_PUNCTUATION) in LATIN_UNITS:
        return True
    # A counter counts only when the source wrote it against the number: "12개" is split, "v2 개선" is not.
    last: str = tail.split()[-1]
    return first.startswith(KOREAN_UNITS) and f"{last}{first}" in spaced_source


def _drawn_past_page_clip(document: Any) -> Check:
    """D25: fills, strokes, or text that run past the clip Chromium puts around each page's content box.

    Chromium paints nothing outside that clip, so the right edge of a full-width table
    can vanish while the PDF still holds its geometry. Geometry lying wholly outside the
    clip is dropped from the PDF and cannot be seen here; check_design.mjs D25 measures
    the tables before printing for that case.
    """
    name, threshold = "drawing or text past the page's content clip", f"0, beyond {CLIP_TOLERANCE_PT} pt"
    found: list[str] = []
    clipped_pages: int = 0
    for number, page in enumerate(document, start=1):
        drawings: list[dict[str, Any]] = page.get_drawings(extended=True)
        clip: Any = next((d["scissor"] for d in drawings if d.get("type") == "clip" and d.get("level") == 0), None)
        if clip is None:
            continue
        clipped_pages += 1
        boxes: list[tuple[float, float, float, float]] = [
            tuple(d["rect"]) for d in drawings if d.get("type") not in ("clip", "group") and d.get("level", 0) >= 1
        ]
        boxes += [tuple(line["bbox"]) for block in page.get_text("dict")["blocks"] for line in block.get("lines", [])]
        rows: dict[int, float] = {}
        for _x0, y0, x1, y1 in boxes:
            # The running header and page number sit above and below the clip, in the page margin boxes.
            if x1 > clip.x1 + CLIP_TOLERANCE_PT and clip.y0 <= (y0 + y1) / 2 <= clip.y1:
                rows[round(y0)] = max(rows.get(round(y0), 0.0), x1)
        found.extend(f"p{number} y {y} pt: to {right:.1f} pt, clip ends at {clip.x1:.1f} pt" for y, right in sorted(rows.items()))
    if not clipped_pages:
        return Check("D25", name, threshold, "no page carries a content clip; only a Chromium print clips, "
                     "so measure the tables with check_design.mjs D25 instead", None)
    return Check("D25", name, threshold, found[:10], not found)


def _opening_on_first_page(document: Any, source: _SourceOutline) -> Check:
    """D23: the overview figure and the whole opening fit on page one, so the end of the opening prints there."""
    # Whitespace is dropped on both sides: list items meet without a space in HTML and with a line break in the PDF.
    tail: str = re.sub(r"\s+", "", "".join(source.opening))[-24:]
    first: str = re.sub(r"\s+", "", document[0].get_text())
    return Check("D23", "opening bullets end on page one", "the last opening words are on page 1", tail,
                 bool(tail) and tail in first)


def _overlapping_words(page: Any, number: int) -> list[str]:
    words: list[Any] = page.get_text("words")
    found: list[str] = []
    for i, first in enumerate(words):
        a = pymupdf.Rect(first[:4])
        for second in words[i + 1 :]:
            b = pymupdf.Rect(second[:4])
            inter = a & b
            if inter.is_valid and not inter.is_empty and inter.get_area() > 0.2 * min(a.get_area(), b.get_area()):
                found.append(f"p{number}: {first[4]} / {second[4]}")
    return found


def _pixel_shares(page: Any) -> tuple[float, float]:
    """Share of non-white pixels and of chromatic pixels, at 50 dpi."""
    pixmap = page.get_pixmap(dpi=50, alpha=False)
    samples: bytes = pixmap.samples
    total: int = pixmap.width * pixmap.height
    ink = chromatic = 0
    for i in range(0, len(samples), pixmap.n):
        r, g, b = samples[i], samples[i + 1], samples[i + 2]
        if min(r, g, b) < 245:
            ink += 1
        if max(r, g, b) - min(r, g, b) >= CHROMA_LEVEL:
            chromatic += 1
    return ink / total, chromatic / total


def _last_body_line(spans: list[dict[str, Any]], page: Any) -> str:
    # The running header and the page number sit in the margins; body text is between them.
    top, bottom = page.rect.y0 + 18 * 72 / 25.4, page.rect.y1 - 20 * 72 / 25.4
    body: list[dict[str, Any]] = [s for s in spans if top <= s["bbox"][1] <= bottom]
    if not body:
        return ""
    lowest: float = max(s["bbox"][3] for s in body)
    return _squash(" ".join(s["text"] for s in body if abs(s["bbox"][3] - lowest) < 2))


def _write_images(document: Any, out_dir: Path, dpi: int) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    pages: list[str] = []
    for number, page in enumerate(document, start=1):
        path: Path = out_dir / f"page-{number:02d}.png"
        page.get_pixmap(dpi=dpi, alpha=False).save(path)
        pages.append(str(path))
    return {"pages": pages, "contact": str(_contact_sheet(document, out_dir / "contact.png", gray=False)),
            "contact_gray": str(_contact_sheet(document, out_dir / "contact-gray.png", gray=True))}


def _contact_sheet(document: Any, path: Path, *, gray: bool) -> Path:
    columns: int = min(4, document.page_count)
    rows: int = -(-document.page_count // columns)
    width, height, gap = 210.0, 297.0, 12.0
    sheet = pymupdf.open()
    canvas = sheet.new_page(width=columns * (width + gap) + gap, height=rows * (height + gap) + gap)
    canvas.draw_rect(canvas.rect, color=None, fill=(0.85, 0.85, 0.85))
    for index in range(document.page_count):
        x: float = gap + (index % columns) * (width + gap)
        y: float = gap + (index // columns) * (height + gap)
        # PDF viewers draw pages on white paper; transparent page margins would show the sheet's gray.
        canvas.draw_rect(pymupdf.Rect(x, y, x + width, y + height), color=None, fill=(1, 1, 1))
        canvas.show_pdf_page(pymupdf.Rect(x, y, x + width, y + height), document, index)
    colorspace = pymupdf.csGRAY if gray else pymupdf.csRGB
    canvas.get_pixmap(dpi=144, colorspace=colorspace, alpha=False).save(path)
    return path


def _int_rgb(value: int) -> tuple[int, int, int]:
    return (value >> 16) & 255, (value >> 8) & 255, value & 255


def _hue(rgb: tuple[int, int, int]) -> float:
    return colorsys.rgb_to_hls(*(v / 255 for v in rgb))[0] * 360


def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
