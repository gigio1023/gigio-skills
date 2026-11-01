# Comparison Patterns

Read when choosing how to show one change between the as-is and to-be versions. Choose by what the reader must find: the size of a gap, the direction or rank, where an item went, or what a definition now says. The builder draws the patterns marked built in; draw the others with `technical-figure` when installed and include them as `svg` figures.

## Encoding rules

These hold for every pattern, built in or drawn elsewhere:

- **One meaning per hue for the whole note.** Gray is the as-is version and unchanged context, blue is the to-be version, and vermillion is a removal or something the reader must act on. A further categorical chart uses at most three hues; a fourth series becomes small multiples.
- **As-is and to-be differ without hue.** The maintainer palette's blue and vermillion have almost the same gray level, a luminance ratio of 1.21, so in grayscale print they merge. As-is marks are hollow and to-be marks filled; removed text is struck through and added text bold. In the change-kinds chart, removal bars are hollow and added bars filled, and both rows are semibold beside the gray field rows.
- **Direct labels.** Print each value beside its mark and each series name where it sits. Add a key only when marks cannot carry their own labels; the dumbbell's key is one line above the rows.
- **Text stays text.** SVG text remains `<text>` so the PDF is searchable and the number check can read chart labels. Every chart also carries its values in `aria-label`, and the Markdown output prints them as a table.
- **No axis decoration that carries numbers the data file lacks.** Tick labels are numbers too; the built-in charts print values at the marks instead of a tick scale.
- **Bars start at zero.** A dot chart may zoom; a bar chart may not.
- **At most two charts per page** and one question per chart.

## Catalog

| Reader question | Pattern | How | Label it with | Main pitfall |
| --- | --- | --- | --- | --- |
| How much changed, by kind | Bars of counts per kind | Built in: `change-kinds` | Value at the bar end; caption states that a record can count under several kinds | Stacking overlapping kinds as if they added up |
| How big is the gap per group or item | Dumbbell, hollow as-is and filled to-be | Built in: `group-dumbbell`, `field-dumbbell`, and `facts-dumbbell` for counts passed as facts | Both values at the dots, to-be in bold blue; rows sorted by change, or in the order given for facts | Unsorted rows; more than about 15 rows in one panel; facts of very different size on one scale |
| Which way did ranks or values move, for many items | Slope chart, two columns | `technical-figure` | Item name and value at both ends; changed items in blue, the rest gray | Crossing lines when many items change rank |
| What exactly are the old and new values | Table with as-is, to-be, and change columns | Built in: mapping and index tables | Short values in cells; reasons beside the table | Sign or direction shown by color alone |
| Where did a renamed, merged, or moved item go | Mapping table, or two ranked columns joined by lines | Built in: mapping table; `technical-figure` for the drawn map | Old and new IDs at the line ends; line style per kind so it survives grayscale | Many-to-one merges crossing; color-only kinds |
| How many items flowed between categories | Sankey or alluvial | `technical-figure` | Node totals; only the largest flows labeled | Clutter from many small flows; use the mapping map instead when items matter more than counts |
| Which part of a hierarchy or pipeline changed | Structure diagram, unchanged parts ghosted | `technical-figure` | Added parts in blue; removed parts in place with a struck label; caption names the encoding | Redrawing the whole structure at full weight |
| What does the definition say now | Word-level text change | Built in: `text-diff` view | Removed words struck through, added words bold; the field name beside both; unchanged text beyond the sentence around each change shortened to an ellipsis | Long blocks; red and green only |
| What does the change do to one concrete record | Two field cards, as-is and to-be | Built in: `cards` view | Same fields on both sides; changed fields bold | Choosing a flattering example; say why this record was chosen when it is not the only one |
| What changed overall, at a glance | Drawn overview: before and after columns, flows between groups, or annotated arrows | Author-drawn `overview` SVG on page one | IDs, short names, counts; few words | A row of number cards or tiles |
| Same measure across several configurations | Small multiples on one shared scale | `technical-figure` | Same axes and order in every panel; only the changed series in blue | Different scales per panel |

## Choosing for common changes

- **A renamed ID** that people search for: a row in the mapping table, and a `cards` view when the rename also changes meaning.
- **A merged or removed ID:** a `cards` view of the old record with its successor on the to-be side, and an action line telling readers what to tag instead.
- **A narrowed or widened definition:** a `text-diff` view, because the struck and added words are the change.
- **Records moving between groups:** a `group-dumbbell`, with a caption naming the IDs that moved, were added, or were removed.
- **A changed priority, weight, or threshold** on several records: a `field-dumbbell` on that field.
- **Counts from outside the record diff,** such as stored tags per record or documents in a second record set: a `facts-dumbbell` whose rows name the as-is and to-be facts.
- **A new top-level structure:** a structure diagram from `technical-figure`, the old structure ghosted in place.

## Sources

The rules follow the [UK Government Analysis Function chart guidance](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/) and [colour guidance](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-colours/) for direct labels, limits on series, and grayscale checks; [Datawrapper on text in charts](https://www.datawrapper.de/blog/text-in-data-visualizations) and [slope charts](https://www.datawrapper.de/academy/how-to-create-a-slope-chart); the [FT Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md); [data-to-viz](https://www.data-to-viz.com/graph/lollipop.html) for the dumbbell; [WCAG 2.2 non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html); and the [OWASP Top 10 2021 mapping figure](https://top10.owasp.org/2021/A00_2021_Introduction), whose two ranked columns are the drawn mapping pattern. The 1.21 luminance ratio was computed from the palette hex values on 2026-11-01.
