"""Inline markup in note.json prose, rendered to HTML or Markdown from one string.

Supported markup: ``{{counts.added}}`` tokens resolved from diff.json,
`` `code` ``, ``**bold**``, and ``[text](url)``. Everything else is text and
is escaped for the target format, because prose can quote record text written
by other people.

``scan_literals`` finds what the builder refuses: numbers typed by hand
instead of tokens, and ID-shaped strings that exist in neither version. The
number check reads rendered HTML and Markdown with the same function, so the
builder and the check agree on what counts as a number, and reads PDF text,
whose adjacent boxes join without a space, with ``scan_joined``.
"""

from __future__ import annotations

import html
import re
from typing import Any

from _diff_data import NUMBER_PATTERN, DiffData

INLINE: re.Pattern[str] = re.compile(r"\{\{\s*([^{}]+?)\s*\}\}|`([^`]+)`|\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)\s]+)\)")
ISO_DATE: re.Pattern[str] = re.compile(r"\d{4}-\d{2}-\d{2}")
URL: re.Pattern[str] = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*://[^\s<>]+")
# A run of word characters and dots: a word, a number with its unit, or an identifier such as v2.1.
WORD: re.Pattern[str] = re.compile(r"[\w.]+")
LETTER_THEN_DIGIT: re.Pattern[str] = re.compile(r"[^\W\d_]\d")


def format_value(value: Any) -> str:
    """Print a resolved token: numbers get thousands separators, labels print as they are."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:,}"
    return str(value)


def render_html(text: str, diff: DiffData) -> str:
    parts: list[str] = []
    position: int = 0
    for match in INLINE.finditer(text):
        parts.append(escape_text(text[position : match.start()], diff))
        token, code, bold, link_text, url = match.groups()
        if token is not None:
            parts.append(bound_number(token.strip(), diff.resolve(token)))
        elif code is not None:
            parts.append(f"<code>{html.escape(code)}</code>")
        elif bold is not None:
            parts.append(f"<strong>{render_html(bold, diff)}</strong>")
        else:
            parts.append(f'<a href="{html.escape(url, quote=True)}">{render_html(link_text, diff)}</a>')
        position = match.end()
    parts.append(escape_text(text[position:], diff))
    return "".join(parts)


def escape_text(text: str, diff: DiffData) -> str:
    """Escape plain text for HTML and keep each ID on one line, so a line break never splits it at its hyphen.

    A split ID reads as two tokens to a search, a copy, or the number check.
    """
    shape: re.Pattern[str] | None = diff.id_shape()
    if shape is None:
        return html.escape(text)
    pieces: list[str] = []
    position: int = 0
    for match in shape.finditer(text):
        pieces.append(html.escape(text[position : match.start()]))
        pieces.append(f'<span class="nb">{html.escape(match.group(0))}</span>')
        position = match.end()
    pieces.append(html.escape(text[position:]))
    return "".join(pieces)


def bound_number(path: str, value: Any) -> str:
    """Print a resolved value; a number carries its diff.json path so the number check can rebind it."""
    shown: str = html.escape(format_value(value))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<span data-count="{html.escape(path, quote=True)}">{shown}</span>'
    return shown


def render_markdown(text: str, diff: DiffData) -> str:
    parts: list[str] = []
    position: int = 0
    for match in INLINE.finditer(text):
        parts.append(escape_markdown(text[position : match.start()]))
        token, code, bold, link_text, url = match.groups()
        if token is not None:
            parts.append(escape_markdown(format_value(diff.resolve(token))))
        elif code is not None:
            parts.append(f"`{code}`")
        elif bold is not None:
            parts.append(f"**{render_markdown(bold, diff)}**")
        else:
            parts.append(f"[{render_markdown(link_text, diff)}]({url})")
        position = match.end()
    parts.append(escape_markdown(text[position:]))
    return "".join(parts)


def escape_markdown(text: str) -> str:
    """Escape characters GitHub would read as HTML or table syntax in plain text."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")


def scan_literals(text: str, diff: DiffData) -> tuple[list[str], list[str]]:
    """Return hand-typed numbers and unknown ID-shaped strings in prose whose words are intact.

    Intact means note.json prose, HTML text, or Markdown, where a word ends at
    a space or a markup boundary. Removed first, because none of them is a
    count: tokens, code spans, link targets and printed URLs, known IDs,
    version identifiers, ISO dates, and every word in which a letter is
    directly followed by a digit, such as ``v4.0``, ``H200``, the commit
    ``3e1f09a7``, the ``v2.1`` of a tag, or the Korean word ``제3자``.
    Digits followed only by letters stay a number with its unit or counter,
    such as ``3x`` or ``23개``. What digits remain were typed by hand.
    """
    plain, unknown = _without_non_counts(text, diff)
    plain = WORD.sub(lambda m: " " if LETTER_THEN_DIGIT.search(m.group(0)) else m.group(0), plain)
    return NUMBER_PATTERN.findall(plain), unknown


def identifier_words(text: str, diff: DiffData) -> list[str]:
    """The words ``scan_literals`` drops from ``text`` because a letter directly precedes a digit in them, in order."""
    plain, _ = _without_non_counts(text, diff)
    return [word for word in WORD.findall(plain) if LETTER_THEN_DIGIT.search(word)]


def scan_joined(text: str, diff: DiffData) -> tuple[list[str], list[str]]:
    """Return the numbers and unknown ID-shaped strings in text whose adjacent boxes join without a space.

    PDF text extraction is such text: a field label and its value in
    neighboring cells read ``우선순위4``, so a letter before a digit does not
    mark an identifier here and the word rule of ``scan_literals`` does not
    apply. The caller removes the source's ``identifier_words`` first.
    """
    plain, unknown = _without_non_counts(text, diff)
    return NUMBER_PATTERN.findall(plain), unknown


def _without_non_counts(text: str, diff: DiffData) -> tuple[str, list[str]]:
    """Blank out markup, URLs, known IDs, version identifiers, and ISO dates; also return the unknown ID-shaped strings."""
    plain: str = INLINE.sub(lambda m: " " if m.group(1) or m.group(2) else (m.group(3) or m.group(4) or ""), text)
    plain = URL.sub(" ", plain)
    unknown: list[str] = []
    shape: re.Pattern[str] | None = diff.id_shape()
    if shape is not None:
        known: set[str] = diff.known_ids()
        unknown = [m.group(0) for m in shape.finditer(plain) if m.group(0) not in known]
        plain = shape.sub(" ", plain)
    for identifier in diff.identifier_strings():
        plain = re.sub(rf"(?<![A-Za-z0-9_.]){re.escape(identifier)}(?![A-Za-z0-9_])", " ", plain)
    return ISO_DATE.sub(" ", plain), unknown
