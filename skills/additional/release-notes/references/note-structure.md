# Note Structure

Read when choosing a note's sections, deciding which changes are material, or naming kinds of change. The order and contents below come from published release notes for taxonomies, standards, and software, listed at the end. The builder renders this order; the writer decides what goes into the parts it does not compute.

## Section order

| Section | Holds | Comes from |
| --- | --- | --- |
| Identity | Both version labels with their tag, commit, or release URL, and the release date | `version_diff.py` options |
| Opening | One or two sentences on what changed and what it means for this reader | `note.json` `summary` |
| Counts | Records before and after, added, removed, changed, then the sentence that reconciles them | data file |
| Required actions | Who must do what, by role, with the IDs involved | `note.json` `actions` |
| Changes at a glance | One or two figures, each answering one question | `note.json` `figures`, drawn from the data file |
| Material changes | Per change: ID and title, as-is and to-be pair, why, impact, and an optional figure | `note.json` `changes` |
| New and changed field values | The new text of one field, usually the definition, for every added and changed record | `note.json` `field_list`, values from the data file |
| Renamed, moved, and removed IDs | Old and new name or parent per ID, each removed ID with its successor or none, and a short reason per ID when given | data file and `note.json` `reasons` |
| Extra sections | Compatibility, migration steps, known issues, acknowledgments, as the release needs | `note.json` `sections` |
| Open questions | Undecided points, phrased as questions | `note.json` `open_questions` |
| All changes | Every added, removed, changed, and minor-only ID with its change kinds | data file |
| Source of the numbers | Data file, both version sources, the tool, the minor-edit rule, links | data file and `note.json` `links` |

PostgreSQL's release notes put migration before the change list, and Common Changelog puts breaking changes first; the required actions sit right after the counts for the same reason. Keep the opening to the change and its consequence. A sentence that announces the note, praises the release, or narrates how it was prepared gives the reader nothing to act on.

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

Print counts a reader can add up. The data file guarantees two identities, and the builder prints both:

- `before − removed + added = after`
- `shared = changed + minor_only + unchanged`, where `shared = before − removed`

Per group, `after = before − removed − moved_out + added + moved_in`. MITRE's CWE diff report from 4.15 to 4.16 is the model: 66 entries with major changes plus 1,361 unchanged equals the 1,427 shared entries, and 1,427 shared plus 2 new equals the 1,429 entries of the new version. A number that cannot be placed in one of these identities needs its source stated beside it, through `--facts`.

## What is material

A change is material when it changes what a record means, forces someone to act, or changes a count the reader tracks. Give each material change a section with an as-is and to-be pair, the reason, and the impact. Typical material changes are a removed or merged ID, a renamed ID that people search for, a definition whose scope widened or narrowed, a moved record that changes a group total, and a changed value that drives handling, such as a priority. Minor-only edits and wording fixes that keep the meaning appear in the index and the counts, not in their own sections.

Reasons come from the people or records that made the decision: an issue, a decision record, or the user. Do not invent a reason to fill the field. When none is available, ask, or state that the reason is not recorded. Renames, moves, and removals that do not get their own section still raise the question why; give them a short reason through `reasons`. A reader who tags or classifies data also needs the new text of every added or redefined record; `field_list` prints it.

Impact names the reader role and the action or consequence: which tags to remap, which report totals move, which filter to update. When the release changes nothing a reader must do, the actions section says so in one line.

## Writing the parts the builder does not compute

- **Opening.** Name the version, the two or three changes that matter most, and the consequence for the reader. Counts come through tokens. When it names the groups whose totals move, take them from `groups` in the data file: every group whose before and after differ, or whose members changed.
- **Actions.** One line per role. Start with the role, then the action and the IDs, including the new IDs to start using and what to do with stored data under removed or narrowed IDs.
- **Titles.** A noun phrase or a short statement of the change, such as "Slow shipping becomes Late delivery". The ID is printed beside it.
- **Captions.** The first sentence says what the figure shows for this release, with tokens for its numbers. Later sentences explain an encoding the reader would not guess.
- **Extra sections.** Compatibility, migration steps, known issues, or acknowledgments, each under a noun-phrase heading.
- **Open questions.** Undecided points stay questions in one section, not hedges spread through the note.

## Sources

Read 2026-11-01: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), [Common Changelog](https://common-changelog.org/), [PostgreSQL 18 release notes](https://www.postgresql.org/docs/current/release-18.html), [Tailwind CSS v4 upgrade guide](https://tailwindcss.com/docs/upgrade-guide) for its old and new name tables, [MITRE ATT&CK updates](https://attack.mitre.org/resources/updates/) for the change-kind key, [MITRE CWE diff report 4.15 to 4.16](https://cwe.mitre.org/data/reports/diff_reports/v4.15_v4.16.html) for reconciling counts and the minor-change rule, [ATLAS data changelog](https://github.com/mitre-atlas/atlas-data/blob/main/CHANGELOG.md) for inline "previously" and "moved from" notes, and [Bugcrowd VRT](https://github.com/bugcrowd/vulnerability-rating-taxonomy) for its FROM and TO blocks and machine-readable deprecated-node mapping.
