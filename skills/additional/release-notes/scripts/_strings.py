"""The builder's own words in each language, from ``assets/strings.json``, with the note's record noun filled in.

A string that names the records the note compares writes the noun as a placeholder: ``{singular}``,
``{plural}``, or ``{counter}``, or with a capital first letter, such as ``{Singular}``, where the noun
starts a heading or a sentence. note.json ``record_noun`` gives exactly the forms its language's strings
use, so a heading reads "Type counts" or "유형 수" in the artifact's own term, never a fixed word.

Korean strings attach no particle whose form depends on the noun's last syllable, such as 은/는 or 이/가,
and follow a counter only with 의 or a copula that suits every counter, such as 이다, so any noun and
counter read correctly.
"""

from __future__ import annotations

import json
import re
from enum import StrEnum
from pathlib import Path

from _errors import NoteSourceError

STRINGS_PATH: Path = Path(__file__).resolve().parent.parent / "assets" / "strings.json"


class NounForm(StrEnum):
    SINGULAR = "singular"  # one record, as in "record"; Korean nouns keep this form for any number
    PLURAL = "plural"  # several records, as in "records"
    COUNTER = "counter"  # the Korean counter after a number, as in 개 or 건


# A noun placeholder as written, lower case or capitalized, mapped to its form.
SPELLINGS: dict[str, NounForm] = {**{f.value: f for f in NounForm}, **{f.value.capitalize(): f for f in NounForm}}
PLACEHOLDER: re.Pattern[str] = re.compile(r"\{(" + "|".join(SPELLINGS) + r")\}")


def load_strings(lang: str) -> dict[str, str]:
    """The language's strings as written, placeholders included."""
    table: dict[str, dict[str, str]] = json.loads(STRINGS_PATH.read_text(encoding="utf-8"))
    if lang not in table:
        raise NoteSourceError(f"no strings for lang {lang!r} in {STRINGS_PATH}")
    return table[lang]


def noun_forms(lang: str) -> set[NounForm]:
    """The noun forms the language's strings use, which note.json ``record_noun`` must give."""
    return {SPELLINGS[name] for text in load_strings(lang).values() for name in PLACEHOLDER.findall(text)}


def with_noun(strings: dict[str, str], noun: dict[NounForm, str]) -> dict[str, str]:
    """Every string with each noun placeholder replaced by its form; other placeholders stay for later formatting."""

    def fill(match: re.Match[str]) -> str:
        spelled: str = match.group(1)
        word: str = noun[SPELLINGS[spelled]]
        return word[:1].upper() + word[1:] if spelled[:1].isupper() else word

    return {key: PLACEHOLDER.sub(fill, text) for key, text in strings.items()}
