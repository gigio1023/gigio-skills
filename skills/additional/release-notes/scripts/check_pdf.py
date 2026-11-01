#!/usr/bin/env python3
"""Countable checks on a rendered release-note PDF, plus page images for the visual read.

Usage:
    uv run --with pymupdf python scripts/check_pdf.py note.pdf --html note.html \\
        [--expected-pages N] [--png-dir pages/] [--dpi 100]

Reads the PDF with PyMuPDF and the source HTML for its headings and figure
titles. Prints one JSON report; each check has a threshold, the measured
value, and ``ok``. With ``--png-dir`` it also writes one PNG per page, a
contact sheet of all pages, and a grayscale contact sheet for the
as-is and to-be distinction. The checks gate defects and drift; they do not
replace reading the page images.

Exit status 0 when every check passes, 1 when any fails, 2 on a setup or
input problem.
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


@dataclass(frozen=True)
class Check:
    id: str
    name: str
    threshold: str
    value: Any
    ok: bool


class _SourceOutline(HTMLParser):
    """Collect heading texts and figure titles from the note HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.headings: list[str] = []
        self.figure_titles: list[str] = []
        self._capture: str | None = None
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes: str = dict(attrs).get("class") or ""
        if tag in ("h1", "h2", "h3"):
            self._capture, self._buffer = "heading", []
        elif tag == "p" and "fig-title" in classes.split():
            self._capture, self._buffer = "figure", []

    def handle_endtag(self, tag: str) -> None:
        if self._capture == "heading" and tag in ("h1", "h2", "h3"):
            self.headings.append(_squash("".join(self._buffer)))
            self._capture = None
        elif self._capture == "figure" and tag == "p":
            self.figure_titles.append(_squash("".join(self._buffer)))
            self._capture = None

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)


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
    report: dict[str, Any] = {"pdf": str(pdf_path), "pages": document.page_count, "checks": [asdict(c) for c in checks]}
    if args.png_dir:
        report["images"] = _write_images(document, Path(args.png_dir), args.dpi)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0 if all(c.ok for c in checks) else 1


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
    ]


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
