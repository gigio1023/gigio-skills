# Note Structure

Read when choosing a note's sections, deciding which changes are material, or naming kinds of change. The order and contents below come from published release notes for taxonomies, standards, and software, listed at the end. The builder renders this order; the writer decides what goes into the parts it does not compute.

## Section order

| Section | Holds | Comes from |
| --- | --- | --- |
| Identity | Both version labels, each with its tag, commit, or release URL on its own line, and the release date | `version_diff.py` options |
| Overview figure | One drawn figure of the whole as-is to to-be change: what left, what arrived, what moved, which totals changed | `note.json` `overview`, an SVG the author draws |
| Opening | At most six one-line bullets on what changed and what it means for this reader, with nested detail | `note.json` `summary` |
| Required actions | Who must do what, by role, one line each, with the date it applies from when there is one and the IDs involved as nested bullets | `note.json` `actions` |
| Record counts | The reconciling identity, the removal kinds, and how shared records divide, then one or two figures; with an overview, the figures only | data file and `note.json` `figures` |
| Material changes | Per change: ID and title, as-is and to-be pair, why, impact, and an optional figure | `note.json` `changes` |
| New and changed field values | Both values of one field, usually the definition, for every added and changed record without its own change section | `note.json` `field_list`, values from the data file |
| ID mapping | Old and new name or parent per renamed, moved, merged, or removed ID, each removed ID with its successor or none | data file |
| Extra sections | Compatibility, migration steps, known issues, acknowledgments, as the release needs | `note.json` `sections` |
| Open questions | Undecided points, phrased as questions | `note.json` `open_questions` |
| All changes | Optional appendix: every added, removed, changed, and minor-only ID with its change kinds and one reason | data file and `note.json` `reasons`; `full_list` |
| Source of the numbers | Paths of the data file and both exports, the refs, the tool, the minor-edit rule, the reconciling sentences when an overview shows the counts, links, and each cited fact with its value and source | data file and `note.json` `links` |

Each number and ref prints once where the reader meets it. The overview already shows the totals on page one, so with an overview the reconciling sentences move to the source section. Refs print in the identity strip and the source section; prose and figures name the version by its label.

PostgreSQL's release notes put migration before the change list, and Common Changelog puts breaking changes first; the required actions sit right after the opening for the same reason. Keep the opening to the change and its consequence. A sentence that announces the note, praises the release, or narrates how it was prepared gives the reader nothing to act on.

## Page one and the word budget

Page one is the overview figure plus at most six top-level opening bullets, each one line, with nested bullets for detail. Every text on the opening and the actions is a bullet; no paragraph sits on page one. A long explanation moves to a material change, an extra section, or the appendix. `check_design.mjs` D22 fails a note whose opening has more than six top-level bullets, a top-level opening or action bullet longer than one rendered line, a nested bullet longer than two lines, a paragraph in the opening or actions, or no overview figure; `check_pdf.py` D23 fails when the opening does not end on page one.

Material changes, reasons, and impacts use bullets too when they hold more than one point. A why or impact given as one string prints inline after its label; a list prints as bullets under it.

## Overview figure

The overview shows the whole change in one drawing: a before and after column, a flow of records between groups, or annotated arrows, whatever fits the artifact. It is a figure, not a row of number cards. It carries few words: IDs, short names, version labels, and counts. The author draws it, with `technical-figure` when installed or by hand, and the builder inlines it so its text stays text in the PDF. `scripts/_overview_svg.py` checks the contract when note.json loads and lists every problem:

- Root `<svg viewBox="0 0 672 H">` with `H` at most 360 and no `width` or `height`; it prints at the 178 mm text width, one unit per CSS pixel.
- Text as `<text>` and `<tspan>`, never outlined paths. `font-family` is the note's `--font` stack, `Pretendard, 'Noto Sans CJK KR', sans-serif`, or its `--mono` stack. `font-size` is 12, 13.33, 16.67, or 20.67, the note's 9, 10, 12.5, and 15.5 pt; `font-weight` is 400 or 600.
- Paint with `fill` and `stroke` presentation attributes in the `:root` token colors of `assets/note.css`; no `style`, `class`, `href`, `filter`, `opacity`, dashes, images, or scripts.
- No box borders: a `rect` has no stroke and a radius of 4, 8, or 12. Lines, arrows, and stroked circles are data marks and may be stroked. As-is is hollow or gray, to-be filled blue, removed vermillion.
- Every `id` starts with `ov-`, such as an arrow marker `ov-arrow`, so it cannot collide with the note.

Numbers and IDs in the overview pass the same number check as the rest of the note. `overview.alt` states every value of the figure as text; the Markdown release body prints it in place of the drawing.

## Change vocabulary

The data file classifies every ID once, and the note uses these words for them. Define a kind once and use it the same way in prose, tables, and figure labels.

| Kind | Meaning |
| --- | --- |
| Added | The ID exists only in the new version |
| Removed | The ID exists only in the old version and has no successor |
| Merged | A removed ID whose successor also existed before, or several removed IDs that share one successor |
| Split | A removed ID with several successors |
| Replaced | A removed ID with one new successor, such as a renumbered record |
| Renamed | The name field changed |
| Moved | The parent field changed |
| *Field* changed | Another compared field changed beyond the minor-edit rule |
| Minor edits only | Every change differs only in letter case, punctuation, or whitespace |
| Unchanged | No compared field changed |

A changed record can have several kinds; the per-kind counts overlap and say so in the figure caption. MITRE ATT&CK separates revocation, meaning replaced by another object, from deprecation, meaning no longer used with no replacement. The successor file carries the same distinction here: a removed ID listed with a successor becomes merged, split, or replaced, and one without stays removed. CWE's diff reports count edits that touch only capitalization and punctuation as minor so that cosmetic fixes do not inflate the changed count; the data file applies the same boundary and counts minor-only records separately.

## Counts that reconcile

Print counts a reader can add up. The data file guarantees two identities, and the builder prints both, the first with its terms named, since a bare `22 − 2 + 3 = 23` does not say which term is the old total:

- `before − removed + added = after`
- `shared = changed + minor_only + unchanged`, where `shared = before − removed`

Per group, `after = before − removed − moved_out + added + moved_in`. MITRE's CWE diff report from 4.15 to 4.16 is the model: 66 entries with major changes plus 1,361 unchanged equals the 1,427 shared entries, and 1,427 shared plus 2 new equals the 1,429 entries of the new version. A number that cannot be placed in one of these identities needs its source stated beside it, through `--facts`.

## A second record set

`version_diff.py` compares one record set. When the release also changed a second set, such as test guides or attack paths beside the taxonomy records, count that set in both versions with your own script and pass each count to `--facts` with a `source` naming the script, the input, and both refs. The note cites the counts through `{{facts.<name>}}` tokens and draws before and after pairs with a `facts-dumbbell` figure. The source section lists every cited fact with its label, value, and source, so the reader can trace a number that the record diff does not hold; give each fact the `label` the note uses for that number elsewhere. Keep facts the note does not cite out of the facts file, or expect them to stay in the data file only.

## What is material

A change is material when it changes what a record means, forces someone to act, or changes a count the reader tracks. Give each material change a section with an as-is and to-be pair, the reason, and the impact. Typical material changes are a removed or merged ID, a renamed ID that people search for, a definition whose scope widened or narrowed, a moved record that changes a group total, and a changed value that drives handling, such as a priority. Minor-only edits and wording fixes that keep the meaning appear in the index and the counts, not in their own sections.

Reasons come from the people or records that made the decision: an issue, a decision record, or the user. Do not invent a reason to fill the field. When none is available, ask, or state that the reason is not recorded. Renames, moves, and removals that do not get their own section still raise the question why; give them a short reason through `reasons`. A reader who tags or classifies data also needs the new text of every added or redefined record; `field_list` prints it.

Impact names the reader role and the action or consequence: which tags to remap, which report totals move, which filter to update. When the release changes nothing a reader must do, the actions section says so in one line.

## Writing the parts the builder does not compute

- **Terms.** Name every concept with the versioned artifact's own term, from its glossary or termbase, its field names, or its decision documents, or with the field's standard term. Never coin a label for the note, in prose or in a figure. When the artifact has no term for a concept, describe it in plain words at first use.
- **Opening.** Name the version, the two or three changes that matter most, and the consequence for the reader. Counts come through tokens. When it names the groups whose totals move, take them from `groups` in the data file: every group whose before and after differ, or whose members changed.
- **Actions.** One line per role. Start with the role, then the action and the IDs, including the new IDs to start using and what to do with stored data under removed or narrowed IDs. Give `effective` when the action applies from a set date; it prints after the role.
- **Titles.** A noun phrase or a short statement of the change, such as "Slow shipping becomes Late delivery". The ID is printed beside it.
- **Captions.** The first sentence says what the figure shows for this release, with tokens for its numbers. Later sentences explain an encoding the reader would not guess.
- **Extra sections.** Compatibility, migration steps, known issues, or acknowledgments, each under a noun-phrase heading.
- **Open questions.** Undecided points stay questions in one section, not hedges spread through the note.

## Sources

Read 2026-11-01: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), [Common Changelog](https://common-changelog.org/), [PostgreSQL 18 release notes](https://www.postgresql.org/docs/current/release-18.html), [Tailwind CSS v4 upgrade guide](https://tailwindcss.com/docs/upgrade-guide) for its old and new name tables, [MITRE ATT&CK updates](https://attack.mitre.org/resources/updates/) for the change-kind key, [MITRE CWE diff report 4.15 to 4.16](https://cwe.mitre.org/data/reports/diff_reports/v4.15_v4.16.html) for reconciling counts and the minor-change rule, [ATLAS data changelog](https://github.com/mitre-atlas/atlas-data/blob/main/CHANGELOG.md) for inline "previously" and "moved from" notes, and [Bugcrowd VRT](https://github.com/bugcrowd/vulnerability-rating-taxonomy) for its FROM and TO blocks and machine-readable deprecated-node mapping.
