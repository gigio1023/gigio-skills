"""Inline markup in note.json prose, rendered to HTML or Markdown from one string.

Supported markup: ``{{counts.added}}`` tokens resolved from diff.json,
`` `code` ``, ``**bold**``, and ``[text](url)``. Everything else is text and
is escaped for the target format, because prose can quote record text written
by other people.

``scan_literals`` finds what the builder refuses: numbers typed by hand
instead of tokens, and ID-shaped strings that exist in neither version.
"""

from __future__ import annotations

import html
import re
from typing import Any

from _diff_data import NUMBER_PATTERN, DiffData

INLINE: re.Pattern[str] = re.compile(r"\{\{\s*([^{}]+?)\s*\}\}|`([^`]+)`|\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)\s]+)\)")
ISO_DATE: re.Pattern[str] = re.compile(r"\d{4}-\d{2}-\d{2}")


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
    """Return hand-typed numbers and unknown ID-shaped strings in one prose string.

    Tokens, code spans, link targets, version identifiers, ISO dates, and known
    IDs are removed first; what digits remain were typed by hand.
    """
    plain: str = INLINE.sub(lambda m: " " if m.group(1) or m.group(2) else (m.group(3) or m.group(4) or ""), text)
    unknown: list[str] = []
    shape: re.Pattern[str] | None = diff.id_shape()
    if shape is not None:
        known: set[str] = diff.known_ids()
        unknown = [m.group(0) for m in shape.finditer(plain) if m.group(0) not in known]
        plain = shape.sub(" ", plain)
    for identifier in diff.identifier_strings():
        plain = re.sub(rf"(?<![A-Za-z0-9_.]){re.escape(identifier)}(?![A-Za-z0-9_])", " ", plain)
    plain = ISO_DATE.sub(" ", plain)
    return NUMBER_PATTERN.findall(plain), unknown
