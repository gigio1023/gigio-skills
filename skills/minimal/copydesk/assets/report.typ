// Optional print-first style. Import report and supply your own content.
// No fonts are bundled. Typst uses the first family in `font` that the
// rendering environment has and falls back down the list per glyph; pass your
// own list when the build machine has other fonts.
#let report(
  title: none,
  subtitle: none,
  font: ("Pretendard", "Noto Sans CJK KR", "Apple SD Gothic Neo"),
  lang: "ko",
  accent: rgb("#3157a5"),
  body,
) = {
  set document(title: title)
  set page(
    paper: "a4",
    margin: (x: 20mm, y: 18mm),
    footer: context align(right, text(size: 8pt, fill: rgb("#59616d"), counter(page).display("1"))),
  )
  set text(font: font, lang: lang, size: 10.5pt, fill: rgb("#20252c"))
  set par(leading: 0.72em)
  // Typst may break a line between any two Hangul syllables, and between a
  // Latin or digit stem and its particle, as in judge|가. Korean breaks between
  // space-separated words, so each word that contains Hangul goes in a box,
  // which moves to the next line whole. A plain [가-힣]+ pattern would still
  // split judge가. A word longer than the whole line does not overflow: its box
  // is laid out at line width and wraps inside, between syllables, so shorten
  // or rephrase such a word.
  show regex("\\S*[가-힣]\\S*"): it => box(it)
  set heading(numbering: none)
  show heading.where(level: 1): it => block(above: 1.2em, below: 0.65em)[
    #text(size: 15pt, weight: "bold", fill: accent, it.body)
  ]
  show heading.where(level: 2): it => block(above: 1em, below: 0.5em)[
    #text(size: 12pt, weight: "bold", it.body)
  ]
  if title != none {
    block(below: 1em)[#text(size: 25pt, weight: "bold", title)]
  }
  if subtitle != none {
    block(below: 1.2em)[#text(size: 10pt, fill: rgb("#59616d"), subtitle)]
  }
  body
}
