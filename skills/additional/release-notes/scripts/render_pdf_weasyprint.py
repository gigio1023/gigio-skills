#!/usr/bin/env python3
"""Print a release-note HTML file to PDF with WeasyPrint, for machines where Chromium cannot run.

Usage:
    uv run --with weasyprint python scripts/render_pdf_weasyprint.py note.html note.pdf

Renders the same HTML as ``render_pdf.mjs`` with one substitution: the font
stack becomes Noto Sans CJK KR alone, because WeasyPrint 70 dropped the hyphen
and plus glyphs from Pretendard's OTF files while text extraction still
returned them (seen 2026-11-01; cause not isolated). Before rendering it asks
fontconfig whether Noto Sans CJK KR is installed and stops with the fix when
it is not. The output is tagged as PDF/UA-1, which WeasyPrint documents as
not guaranteed valid. Read every page image afterwards: this route is where
text extraction passed while glyphs were missing.

Exit status 0 on success, 2 when WeasyPrint, fontconfig, or the font is missing.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

FONT: str = "Noto Sans CJK KR"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: render_pdf_weasyprint.py note.html note.pdf", file=sys.stderr)
        return 2
    source, target = Path(argv[0]), Path(argv[1])
    problem: str | None = _missing_prerequisite()
    if problem:
        print(f"render_pdf_weasyprint: {problem}", file=sys.stderr)
        return 2
    import weasyprint

    text: str = source.read_text(encoding="utf-8")
    stack: re.Match[str] | None = re.search(r"--font:\s*([^;]+);", text)
    if stack is None or f'"{FONT}"' not in stack.group(1):
        print(f"render_pdf_weasyprint: {source} declares no --font stack naming {FONT!r}; build it with build_note.py", file=sys.stderr)
        return 2
    # The builder writes the stack verbatim in :root, the page margin boxes, and every chart's
    # font-family attribute, so one replacement moves the whole note to the Noto-first stack.
    swapped: str = f'"{FONT}", sans-serif'
    count: int = text.count(stack.group(1))
    document = weasyprint.HTML(string=text.replace(stack.group(1), swapped), base_url=str(source.parent))
    document.write_pdf(str(target), pdf_variant="pdf/ua-1")
    print(f"wrote {target} with WeasyPrint {weasyprint.__version__}; font stack {swapped} in {count} places")
    return 0


def _missing_prerequisite() -> str | None:
    try:
        import weasyprint  # noqa: F401
    except ModuleNotFoundError:
        return "WeasyPrint is missing; run this script with `uv run --with weasyprint python ...` (it needs system Pango 1.44+)"
    if shutil.which("fc-match") is None:
        return "fontconfig's fc-match is missing; install fontconfig so WeasyPrint can find fonts"
    matched: str = subprocess.run(["fc-match", "-f", "%{family}", FONT], capture_output=True, text=True, check=True).stdout
    if FONT not in matched.split(","):
        return (f"fontconfig has no {FONT!r} (it would substitute {matched!r}); install it "
                "(Debian and Ubuntu package fonts-noto-cjk, macOS `brew install --cask font-noto-sans-cjk`)")
    return None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
