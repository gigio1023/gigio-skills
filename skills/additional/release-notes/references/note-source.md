# Note Source

Read when running `version_diff.py`, writing `note.json`, or looking up a token path. The two files together are the note's content source; `build_note.py` renders both the HTML and the Markdown from them.

## Contents

- Computing the data file
- The data file
- Writing note.json
- Tokens and inline markup
- Figures and change views

## Computing the data file

`scripts/version_diff.py` reads one export per version and writes `diff.json`. Python 3.11 or newer with the standard library only.

| Option | Meaning |
| --- | --- |
| `--old`, `--new` | A directory of `*.json` files (each one record or a list), a `.json` list, a `.jsonl` file, or a `.csv` file |
| `--records-path` | Dotted key path to the record list when a `.json` file is an object, such as `items` |
| `--old-label`, `--new-label` | Version identifiers printed in the note, such as `2.0` |
| `--old-ref`, `--new-ref` | Tag, commit, or release URL of each version |
| `--date` | Release date of the new version, `YYYY-MM-DD` |
| `--key` | ID field, default `id` |
| `--name-field` | Field whose change counts as renamed; `name` when present |
| `--parent-field` | Field whose change counts as moved |
| `--group-field` | Field whose values get before and after counts; often the parent |
| `--fields` | Comma-separated fields to compare; default every field except the key |
| `--successors` | CSV with header `old_id,new_id`, one row per successor of a removed ID |
| `--facts` | JSON object `{name: {"value": number, "source": "..."}}` for numbers the versions cannot give |
| `--out` | Path of the data file |

Errors stop the run with the file, the record, and the fix: a missing key field, a duplicate ID within one version, a nested list without `--records-path`, a successor that does not exist, or a role field that appears in no record. YAML exports are not read; convert them to JSON first.

Export each version from its released state: the tag or release commit, not a working branch. When the artifact lives in a repository, check out each tag into its own directory or export from it, and pass the tag as `--old-ref` and `--new-ref` so the note names exactly what was compared.

`--facts` is for a number the note needs that the two versions cannot produce, such as the count of stored labels that need remapping. Its `source` says where the number came from, and the note cites it as `{{facts.<name>}}`. Keep facts few; most notes need none.

## The data file

`diff.json` has schema `release-notes/diff@1`. The parts a writer cites:

| Key | Holds |
| --- | --- |
| `old`, `new` | `label`, `ref`, `source` file name, `records` count |
| `date` | Release date or null |
| `roles` | Which fields are the key, name, parent, and group |
| `compared_fields` | Fields compared, name and parent first |
| `counts` | `before`, `after`, `added`, `removed`, `shared`, `changed`, `minor_only`, `unchanged`, `net` |
| `removal_kinds` | Counts of `merged`, `split`, `replaced`, `removed` |
| `field_changes` | Per field, `major` and `minor` change counts; a record can count under several fields |
| `groups` | Per group value, `before`, `after`, `added`, `removed`, `moved_in`, `moved_out` |
| `identities` | The two reconciling identities as text |
| `added`, `removed`, `changed`, `minor_only` | Records per class; changed entries hold `old`, `new`, `major_fields`, `minor_fields`, and each field `change` |
| `facts` | Values passed with `--facts` |
| `ids` | Every ID of each version, for checking IDs the note names |

## Writing note.json

Schema `release-notes/note@1`; [the example](../assets/example/note.en.json) uses every field. Unknown keys are an error, so a misspelled field fails instead of disappearing.

| Field | Required | Holds |
| --- | --- | --- |
| `schema` | yes | `release-notes/note@1` |
| `lang` | yes | `en` or `ko`; other languages need an entry in `assets/strings.json` |
| `title` | yes | Artifact name and version, usually with `{{new.label}}` |
| `subtitle` | no | The audience or scope in one line |
| `summary` | yes | List of opening paragraphs |
| `actions` | no | List of `{who, what}`; empty prints that no action is needed |
| `figures` | no | List of figures, below |
| `changes` | no | List of material changes, below |
| `sections` | no | List of `{heading, paragraphs}` for compatibility, migration, known issues |
| `open_questions` | no | List of questions |
| `links` | no | List of `{label, url}`, such as the full change list |
| `field_labels` | no | Display names for compared fields, such as `{"group": "Category"}` |
| `reasons` | no | Short reason per removed, renamed, or moved ID, `{"FB-013": "..."}`; adds a reason column to the mapping table, with "Not recorded" for IDs without one |
| `field_list` | no | A compared field, such as `definition`, whose new text is listed for every added record and every record with a major change in it |

## Tokens and inline markup

Prose fields accept `{{dotted.path}}` tokens, `` `code` ``, `**bold**`, and `[text](url)`. A token resolves against the data file: `{{counts.added}}`, `{{counts.before}}`, `{{groups.Account.after}}`, `{{field_changes.definition.major}}`, `{{removal_kinds.merged}}`, `{{old.label}}`, `{{facts.remapped_labels}}`. Numbers print with thousands separators. In the HTML, each token number carries its path in a `data-count` attribute, which `check_numbers.py` uses to catch an HTML built from an older data file.

The builder rejects digits typed in prose, with three exceptions: code spans, version labels and refs from the data file, and ISO dates. IDs that exist in either version are fine; an ID-shaped string that exists in neither is rejected. The error lists every location, so one build reports all of them. Write numbers that are not counts in words or rephrase: "Lower priority numbers are handled first" rather than citing a priority value.

## Figures and change views

| `figures[].type` | Draws | Needs |
| --- | --- | --- |
| `change-kinds` | Horizontal bars: added, removed, each field with major changes, minor-only | Nothing more; the caption gets a sentence on overlapping kinds |
| `group-dumbbell` | Per group, hollow as-is ring and filled to-be dot, sorted by change | `version_diff.py --group-field` |
| `field-dumbbell` | Per changed record, the old and new value of one numeric field | `field` naming a numeric compared field |
| `svg` | An SVG drawn elsewhere, such as by `technical-figure` | `src` relative to note.json, `alt` stating the values as text |

Every figure has a `title` and a `caption`. The `svg` type's text must be SVG text, not outlined paths, so the PDF keeps it searchable and the number check can read it; its numbers must come from the data file like any other.

| `changes[].view` | Shows | Needs |
| --- | --- | --- |
| `cards` (default) | Two field cards, as-is and to-be; changed fields in bold, unchanged in gray; an added or removed record shows "Not in" the other version, or its successor | `id` of any listed record |
| `text-diff` | One text field word by word: removed words struck through on a vermillion tint, added words bold on a blue tint | `id` of a changed record and `field` naming one of its changed text fields |

Each change also needs `title`, `why`, and `impact`, and may carry one `figure` in the same form as `figures` entries. It prints after the change's impact, which keeps a chart beside the change it explains and the overview within two charts per page.
