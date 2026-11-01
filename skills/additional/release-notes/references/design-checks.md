# Design Checks

Read when interpreting a check report, changing the stylesheet, or reading the rendered pages. "Restrained" is defined here as counts: hue families, type sizes, borders, spacing, and contrast that a script can measure on the HTML and the PDF. The counts gate drift and defects. They do not show that a chart answers its question or that the page reads well, so the visual read below is part of every check run.

## Tokens and layout

| Item | Value |
| --- | --- |
| Page | A4 portrait; margins 18 mm top, 16 mm sides, 20 mm bottom; text column 178 mm, about 673 px |
| Type | Pretendard, then Noto Sans CJK KR; weights 400 and 600; 28 pt title, 15.5 pt section heading and stat number, 12.5 pt subheading, 10 pt body, 9 pt tables, code, and chart text, 8.5 pt captions and table headers, 8 pt running header and page number |
| Color | Background `#FFFFFF`, surface `#F4F3F1`, ink `#2C2C2B`, secondary ink `#5F5E5B`, line `#8E8B86`; to-be blue `#2769B7` with text variant `#1E5BA1` and tint `#E5F1FF`; removed vermillion `#C55123` with text variant `#A63C0C` and tint `#FFEBE4` |
| Spacing | Multiples of 4 px |
| Radius | 4 px table stripes and code, 8 px cards, 12 px figure panels |
| Separation | Surface fills, spacing, and radius; tables alternate row fills; no borders, rules, dashed separators, shadows, or gradients |

All values live in `assets/note.css`; the charts read the `:root` tokens through the builder, so a token change restyles both. The palette and type values follow the maintainer's figure tokens in `technical-figure`; the contrast values below were computed from them.

## Checks

`check_design.mjs` measures the HTML in print emulation at the column width, and `check_pdf.py` measures the PDF. `check_numbers.py` owns the number checks N1 to N7, N7 being that each count label in a chart reads its path's label, described in its header; its PDF pass also catches a text layer that lost characters, which no design check sees.

| ID | Check | Threshold | Script | Basis |
| --- | --- | --- | --- | --- |
| D1 | Accent hue families, chroma above 0.12 bucketed by 30 degrees | At most 3 per document, at most 2 per figure | both | One meaning per hue; the Analysis Function's limit of about four categories |
| D2 | Chromatic pixel share per page | At most 5 percent | PDF | Maintainer token `chroma_area_max` |
| D3 | Fonts that drew text | Only the stylesheet's stacks | HTML; the renderer enforces it | One typographic voice |
| D4 | Distinct font sizes | At most 8 | both | A deck with 16 sizes read as uncalm; GOV.UK uses five steps |
| D5 | Smallest font size | At least 8 pt, chart text at its printed size | both | Chart labels stay at the maintainer's 12 px floor |
| D6 | Figures per page | At most 2 | PDF, by figure titles | Restraint budget |
| D7 | Overlapping word boxes | 0 pairs overlapping by more than 20 percent | PDF | Label collisions |
| D8 | Text contrast | At least 4.5:1 against the effective background; SVG text against the shape painted under it | HTML | WCAG 1.4.3 |
| D9 | Chart mark contrast | At least 3:1 against the figure background | HTML | WCAG 1.4.11 |
| D10 | As-is and to-be marks differ without hue | As-is hollow, or luminance ratio at least 1.5, in charts and in every card pair and text difference, whose heads carry the chart marks | HTML | Card fills measure 1.03 apart in grayscale |
| D11 | Borders, shadows, gradients | 0 | HTML | Borderless separation |
| D12 | Corner radii | Within 4, 8, 12 px | HTML | Radius tokens |
| D13 | Spacing off the 4 px scale | 0 | HTML | Spacing tokens |
| D14 | Tables without alternating row fills | 0 | HTML | Stripes instead of rules |
| D15 | Emoji | 0 | HTML | No decoration |
| D16 | Clipped boxes, chart text outside its chart, text outside the page | 0 | both | Overflow hidden is not a check |
| D17 | Page count and blank pages | Equals the expected count when given; no page under 0.5 percent ink | PDF | Silent page splits |
| D18 | Outline, tags, language | Outline entries equal headings; structure tree present; `/Lang` set | PDF | Navigable, tagged output |
| D19 | Same hue, same meaning | Gray as-is, blue to-be, vermillion removed or action | manual | One meaning per hue |
| D20 | Dashed or dotted strokes | 0 | HTML | No dashed separators |
| D21 | Heading left at the bottom of a page | 0 | PDF | Page-break sanity |
| D22 | Page-one budget | Overview figure present; at most 6 top-level opening bullets of one line; action leads one line; nested bullets at most two lines; no paragraphs in the opening or actions | HTML | A page of paragraphs went unread |
| D23 | Opening on page one | The last opening words print on page 1 | PDF | The overview and opening are read together |
| A1 | One `h1`, `lang` set, every chart `role="img"` with `aria-label`, table headers scoped | All | HTML | Accessible structure |

Thresholds are this skill's rules, not external standards except where WCAG is named. A failure is a defect to fix or a deliberate exception to state in the report with its reason.

## Reading the pages

`check_pdf.py --png-dir` writes one PNG per page, `contact.png` with all pages, and `contact-gray.png` in grayscale. Read them in this order:

1. The contact sheet: page rhythm, a figure or card split across pages, a near-empty last page, one page much denser than the rest.
2. Every page at full size: clipped or overlapping text, a value beside the wrong mark, a struck or bold word that is not part of the change, a missing glyph, a heading stranded at the bottom, a card whose fields do not line up.
3. The grayscale sheet: every as-is and to-be pair still distinct by shape, fill, strike, or weight.
4. `check_design.mjs --shots` screenshots at 794 and 1280 px for the HTML deliverable.

Cards and figures keep together across page breaks, which can leave white space at the bottom of a page. That is expected; do not shrink type or remove content to close the gap. Fix only the flagged element, rebuild, and rerun the affected checks and neighboring pages. Two automatic fix rounds is the limit; refinement past that was not monotonic in the slide-generation work this loop rule comes from, so report what remains.

## Sources

[UK Government Analysis Function, charts](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/) and [colours](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-colours/); [GOV.UK type scale](https://design-system.service.gov.uk/styles/type-scale/) and [table](https://design-system.service.gov.uk/components/table/) components; [WCAG 2.2 non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). All read 2026-11-01. The countable-check approach adapts slop pre-flight counts from published design-skill reviews, whose authors note that such counts measure a skill's own rules rather than quality.
