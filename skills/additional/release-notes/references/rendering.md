# Rendering

Read when preparing a machine to render, when a render fails, or when delivering the HTML or Markdown output. One HTML file with inline CSS and inline SVG is both the HTML deliverable and the source the PDF is printed from; the Markdown body is rendered from the same `note.json` and `diff.json`. `copydesk` recommends Typst for an unconstrained print-first report; this skill prints HTML instead because one source must also yield the HTML deliverable, and Typst's HTML export is experimental.

## Prerequisites

| Need | For | Check | Setup, with the user's grant |
| --- | --- | --- | --- |
| Python 3.11+ | `version_diff.py`, `build_note.py`, `check_numbers.py` without a PDF | `python3 --version` | Any CPython 3.11 or newer |
| Node.js 20+ and `playwright` or `playwright-core` | `render_pdf.mjs`, `check_design.mjs` | `node --version`; the script reports a missing module | `npm install playwright-core` in a working directory, or point `RELEASE_NOTES_NODE_MODULES` at a `node_modules` that has it |
| A Chromium build that matches Playwright | Same | The script reports a browser that cannot start | `npx playwright install chromium`; `npx playwright install-deps chromium` needs root on Linux |
| `uv` | PyMuPDF for `check_pdf.py`, pypdf for `check_numbers.py --pdf`, WeasyPrint for the fallback | `uv --version` | `uv run --with pymupdf ...` downloads into uv's cache |
| Pretendard or Noto Sans CJK KR | All rendering | The render stops naming the font that drew text | Pretendard from its [releases](https://github.com/orioncactus/pretendard); Noto Sans CJK KR from the `fonts-noto-cjk` package |

Installing a package, browser, or font changes the machine; do it only with the user's grant, and prefer a project-local or cache-local install. A machine that already has `technical-figure`'s setup has `playwright-core` in that skill's cache, `~/.cache/technical-figure/node/node_modules` by default.

## Commands

```bash
python3 scripts/build_note.py --note note.json --diff diff.json --out-dir out [--stem name]
RELEASE_NOTES_NODE_MODULES=<node_modules> node scripts/render_pdf.mjs out/note.html out/note.pdf
```

`render_pdf.mjs` opens the HTML as print media, waits for fonts, and calls `page.pdf` with `preferCSSPageSize`, `printBackground`, `tagged`, and `outline`. The page size, margins, running title, and `n / N` page numbers come from the `@page` rule the builder writes; Chromium 131 and later draw `@page` margin boxes. Before writing, it asks Chromium which platform fonts drew the text and stops when any family is outside the stylesheet's `--font` and `--mono` stacks, and it stops on any request that is not a `file:` or `data:` URL. Rendering takes about a second for a five-page note; page images were identical across repeated runs on one machine, while the PDF bytes differ in their creation date.

## Fonts and the text layer

Chromium embeds Pretendard as Type3 fonts and maps each drawn glyph back to a character for the PDF's text layer. Glyphs that come from an OpenType feature, such as the `ss06` stylistic set or tabular figures, got no mapping on 2026-11-01: the page images were correct while pypdf and copy and paste returned `Exampe` for `Example` and private-use characters for table digits. The stylesheet therefore sets no `font-feature-settings` or `font-variant-numeric`. Ligatures are off for a related reason: Pretendard draws `->` as one arrow glyph, which the text layer returned as `→`. Keep both settings when restyling, and run the number check with `--pdf` after any font change.

The stylesheet breaks Korean at spaces (`word-break: keep-all`) with strict line breaking, which keeps words and counters whole but still strands a one-syllable last word, such as `등.`, on a line of its own. A forced break, a hand-set width, or a long unbreakable string can leave a lone syllable, a closing bracket at a line start, or a number away from its unit. `check_pdf.py` D24 finds these in the text layer and names each page; [design checks](design-checks.md) gives the rules.

## Table right edge

Chromium prints each page inside a clip path at the `@page` content box and paints nothing outside it. A table wider than the text column either makes Chromium scale every page down to fit, or loses whatever lies past the clip with no error. On 2026-11-04, a table holding two unbreakable paths, 711 px wide in a 673 px column, printed the whole page at 0.946 scale, so 10 pt body text came out at 9.46 pt; D4 sees that as extra type sizes. The `pdf-creator` skill in [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) measured the other outcome: a page clip ending at 538.90 pt with the table's right border at 545.18 pt, so the border vanished while the last column's text stayed intact and the page looked deliberate.

The clip hides the defect from coordinate readers in one case and removes the evidence in the other. Geometry that straddles the clip stays in the PDF unpainted, so PyMuPDF and pdfplumber still report it; geometry wholly outside the clip is dropped from the PDF. `check_design.mjs` D25 therefore measures every table against the printable width of the `@page` rule before printing, and `check_pdf.py` D25 reports fills, strokes, and text that run past the page clip by more than 0.75 pt, which Chromium's rounding to whole CSS px stays under. The PDF side runs only on a Chromium print: a WeasyPrint PDF has no page clip, so its D25 is reported as not run.

Neither check sees ink that lies outside an element's layout box, such as an outline or a shadow, when it also lies wholly past the clip. When a table ends at the right margin, read its right edge in the page images at 200 percent: the last column's fill or border must end where the other rows' do. Fix a wide table by letting its long cells wrap, as the source section does with `overflow-wrap: anywhere`, or by moving a column into the appendix; never by shrinking the type.

## Failure messages

| Message starts with | Cause | Fix |
| --- | --- | --- |
| `Playwright is not installed under` | No `playwright` or `playwright-core` in the named `node_modules` | Install it there, or set `RELEASE_NOTES_NODE_MODULES` |
| `Chromium could not start` | No browser for this Playwright version, or missing system libraries | `npx playwright install chromium`; the WeasyPrint fallback when no Chromium can run |
| `text was drawn with` | A glyph came from a font outside the stacks, usually because neither named font is installed or a character is missing from both | Install Pretendard or Noto Sans CJK KR; for a missing character, replace it or add a font to the stack in `assets/note.css` |
| `the note requested` | The HTML references an external resource, usually from an embedded SVG | Inline the resource or remove it |
| `build_note: the note source cites values` | Typed numbers or unknown IDs in prose | Use tokens or `--facts`; fix the ID |

## WeasyPrint fallback

Use it only when no Chromium can run, such as in a locked-down CI image:

```bash
uv run --with weasyprint python scripts/render_pdf_weasyprint.py out/note.html out/note.pdf
```

It renders the same HTML with one substitution: the font stack becomes Noto Sans CJK KR alone. On 2026-11-01, WeasyPrint 70 drew Pretendard's OTF files without hyphens, plus signs, and some letters while text extraction still returned the missing characters, and the cause was not isolated. The builder writes the font stack verbatim in the stylesheet, the page margin boxes, and every chart's `font-family` attribute, so one replacement covers the whole note. Charts carry their paint as SVG attributes because WeasyPrint does not apply document CSS inside inline SVG. The script checks with `fc-match` that Noto Sans CJK KR is installed before rendering, and requests PDF/UA-1 output, which WeasyPrint documents as not guaranteed valid. Read every page image after a fallback render; this route is where text extraction passed while glyphs were missing.

An unverified lead on that cause: WeasyPrint subset-embeds OpenType fonts with CFF outlines as CID Type 0C fonts, which macOS Preview and Adobe Reader failed to draw for PingFang SC in the `pdf-creator` skill of [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills), while Chrome's PDF viewer and `pdftoppm` showed the same pages correctly. Pretendard's OTF files have CFF outlines, and so do Noto Sans CJK KR's OTF files, which the fallback switches to; this is an inference that nobody has tested here. The cheap test is a TrueType Korean font: render one note with Pretendard OTF and with a TrueType face such as Noto Sans KR, list the embedded font types with `pdffonts`, which prints `CID Type 0C` or `CID TrueType`, and open both PDFs in Preview or Acrobat as well as in Chrome and `pdftoppm`.

## HTML deliverable

The HTML is one file with no external requests. Fonts are not embedded, so a recipient without Pretendard or Noto Sans CJK KR sees their system sans. It sets `color-scheme: light` and paints its own background, so a browser in dark mode still shows the light page. When the HTML goes to recipients who lack the fonts and the look matters, send the PDF.

## GitHub release body

`note.md` starts with the subtitle and summary, because GitHub takes the release title separately. Charts become tables of their values, card pairs become field tables with changed values in bold, text changes become `diff` blocks, and the full change list sits in a collapsed `<details>` block. Paste it into the release form, or pass it with `gh release create <tag> --notes-file out/note.md` when the user asks to publish. Publishing is the user's decision.

## Sources

The table right-edge measurements and the CID Type 0C lead come from the `pdf-creator` skill in [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) (MIT), read 2026-11-04; the scaled page was printed on macOS with Chromium 151 the same day. Checked 2026-11-01 on Ubuntu 24.04 with Chromium 151 through Playwright 1.62.1, WeasyPrint 70.0, and PyMuPDF: [Playwright `page.pdf`](https://playwright.dev/docs/api/class-page#page-pdf), [Playwright browsers](https://playwright.dev/docs/browsers), [WeasyPrint API reference](https://doc.courtbouillon.org/weasyprint/stable/api_reference.html), and [Typst HTML export status](https://typst.app/docs/reference/html/).
