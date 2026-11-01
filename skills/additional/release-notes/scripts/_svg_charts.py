"""Inline SVG charts for a release note, drawn from diff.json values.

Each chart is 640 units wide: the A4 text column at 16 mm side margins is
178 mm, about 673 px at 96 px per inch, and the figure panel's 16 px padding
leaves 640 px inside it. Charts therefore print at 1:1, and 12 px chart text
prints at 9 pt like table text. Text stays SVG ``<text>``, so the PDF keeps a
text layer and the number check can read chart labels.

Colors and the font stack arrive as a ``Palette`` read from the ``:root``
tokens of ``assets/note.css`` and are written as SVG presentation
attributes. Attributes, not stylesheet classes, carry the paint because
WeasyPrint does not apply document CSS inside inline SVG. The class names
stay on the elements for meaning and for the design checks.

As-is and to-be differ by more than hue: as-is marks are hollow rings, to-be
marks are filled, and every value is printed beside its mark, so the chart
reads in grayscale and without a legend lookup.
"""

from __future__ import annotations

import html
import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

WIDTH: int = 640
FONT_PX: float = 12.0
VALUE_SPACE: int = 56


@dataclass(frozen=True)
class Palette:
    """Token values from the stylesheet's :root block."""

    bg: str
    ink: str
    ink_2: str
    line: str
    blue: str
    blue_text: str
    vermillion: str
    font: str

    @classmethod
    def from_css(cls, css: str) -> Palette:
        block: re.Match[str] | None = re.search(r":root\s*\{([^}]*)\}", css)
        if block is None:
            raise ValueError("stylesheet has no :root block of tokens")
        tokens: dict[str, str] = dict(re.findall(r"--([\w-]+)\s*:\s*([^;]+);", block.group(1)))
        names: dict[str, str] = {"bg": "bg", "ink": "ink", "ink_2": "ink-2", "line": "line", "blue": "blue",
                                 "blue_text": "blue-text", "vermillion": "vermillion", "font": "font"}
        missing: list[str] = [token for token in names.values() if token not in tokens]
        if missing:
            raise ValueError(f"stylesheet :root lacks tokens {missing}")
        return cls(**{field: tokens[token].strip() for field, token in names.items()})


@dataclass(frozen=True)
class BarRow:
    label: str
    value: int
    tone: str  # "added", "removed", or "neutral"


@dataclass(frozen=True)
class PairRow:
    label: str
    before: float
    after: float


def change_kind_bars(rows: list[BarRow], aria_label: str, palette: Palette) -> str:
    """Horizontal bars of record counts per kind of change, values at the bar ends."""
    fills: dict[str, str] = {"added": palette.blue, "removed": palette.vermillion, "neutral": palette.line}
    label_width: float = _label_column(r.label for r in rows)
    x0: float = label_width + 12
    span: float = WIDTH - VALUE_SPACE - x0
    top_value: int = max([r.value for r in rows] + [1])
    row_h, bar_h = 24, 12
    parts: list[str] = []
    for i, row in enumerate(rows):
        mid: float = 4 + i * row_h + row_h / 2
        length: float = span * row.value / top_value
        parts.append(_text(palette, 0, mid + 4, row.label, "label", palette.ink))
        if length > 0:
            parts.append(f'<rect class="bar bar-{row.tone}" x="{x0:.1f}" y="{mid - bar_h / 2:.1f}" width="{length:.1f}" '
                         f'height="{bar_h}" rx="2" fill="{fills[row.tone]}"/>')
        parts.append(_text(palette, x0 + length + 8, mid + 4, _number(row.value), "value", palette.ink_2))
    return _svg(4 + len(rows) * row_h + 4, aria_label, parts)


def pair_dumbbell(rows: list[PairRow], before_key: str, after_key: str, aria_label: str, palette: Palette) -> str:
    """One row per item: hollow as-is ring, filled to-be dot, both values printed.

    The axis starts at zero so dot positions compare as magnitudes; rows keep
    the order given, which the caller sorts by change.
    """
    label_width: float = _label_column(r.label for r in rows)
    x0: float = label_width + 12 + 40
    x1: float = WIDTH - VALUE_SPACE
    top_value: float = max([max(r.before, r.after) for r in rows] + [1])

    def x(value: float) -> float:
        return x0 + (x1 - x0) * value / top_value

    key_y: float = 12
    second_key: float = x0 + 24 + _text_width(before_key) + 16
    parts: list[str] = [
        _ring(palette, x0, key_y - 4, 5),
        _text(palette, x0 + 12, key_y, before_key, "key", palette.ink_2),
        _dot(palette, second_key, key_y - 4),
        _text(palette, second_key + 12, key_y, after_key, "key", palette.ink_2),
    ]
    row_h: int = 26
    for i, row in enumerate(rows):
        mid: float = 36 + i * row_h
        xb, xa = x(row.before), x(row.after)
        parts.append(_text(palette, 0, mid + 4, row.label, "label", palette.ink))
        parts.append(f'<line class="link" x1="{min(xb, xa):.1f}" y1="{mid}" x2="{max(xb, xa):.1f}" y2="{mid}" '
                     f'stroke="{palette.line}" stroke-width="1.5"/>')
        if row.after == row.before:
            # One printed value stands for both versions; the ring around the dot shows they coincide.
            parts.append(_text(palette, xa + 14, mid + 4, _number(row.after), "value", palette.ink_2))
        elif row.after > row.before:
            parts.append(_text(palette, xb - 10, mid + 4, _number(row.before), "value", palette.ink_2, anchor="end"))
            parts.append(_text(palette, xa + 10, mid + 4, _number(row.after), "value value-to-be", palette.blue_text, bold=True))
        else:
            parts.append(_text(palette, xa - 10, mid + 4, _number(row.after), "value value-to-be", palette.blue_text,
                               anchor="end", bold=True))
            parts.append(_text(palette, xb + 10, mid + 4, _number(row.before), "value", palette.ink_2))
        parts.append(_ring(palette, xb, mid, 8 if row.after == row.before else 5))
        parts.append(_dot(palette, xa, mid))
    return _svg(36 + len(rows) * row_h - 8, aria_label, parts)


def embedded_svg(src: Path, aria_label: str) -> str:
    """Inline an SVG drawn elsewhere, such as by technical-figure, with the note's accessible label."""
    text: str = src.read_text(encoding="utf-8")
    text = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", text).strip()
    match: re.Match[str] | None = re.search(r"<svg\b[^>]*>", text)
    if match is None:
        raise ValueError(f"{src}: no <svg> element")
    root: str = re.sub(r'\s(role|aria-label)="[^"]*"', "", match.group(0))
    root = root.replace("<svg", f'<svg role="img" aria-label="{html.escape(aria_label, quote=True)}"', 1)
    return text[: match.start()] + root + text[match.end() :]


def _svg(height: float, aria_label: str, parts: list[str]) -> str:
    body: str = "".join(parts)
    return (f'<svg class="chart" viewBox="0 0 {WIDTH} {height:.0f}" role="img" '
            f'aria-label="{html.escape(aria_label, quote=True)}">{body}</svg>')


def _ring(palette: Palette, cx: float, cy: float, r: int) -> str:
    return (f'<circle class="mark-as-is" cx="{cx:.1f}" cy="{cy}" r="{r}" fill="{palette.bg}" '
            f'stroke="{palette.ink_2}" stroke-width="1.5"/>')


def _dot(palette: Palette, cx: float, cy: float) -> str:
    return f'<circle class="mark-to-be" cx="{cx:.1f}" cy="{cy}" r="5" fill="{palette.blue}"/>'


def _text(palette: Palette, x: float, y: float, content: str, cls: str, fill: str, *, anchor: str = "start",
          bold: bool = False) -> str:
    extra: str = (f' text-anchor="{anchor}"' if anchor != "start" else "") + (' font-weight="600"' if bold else "")
    # The font stack goes in single quotes so it appears in the HTML exactly as in the stylesheet.
    return (f"<text class=\"{cls}\" x=\"{x:.1f}\" y=\"{y:.1f}\" font-family='{palette.font}' font-size=\"{FONT_PX:g}\" "
            f'fill="{fill}"{extra}>{html.escape(content)}</text>')


def _number(value: float) -> str:
    return f"{int(value):,}" if float(value).is_integer() else f"{value:,}"


def _text_width(text: str) -> float:
    """Estimate rendered width at 12 px: about 0.86 em per wide (Hangul, CJK) character, 0.56 em otherwise."""
    return sum(FONT_PX * (0.86 if unicodedata.east_asian_width(ch) in "WF" else 0.56) for ch in text)


def _label_column(labels: Iterable[str]) -> float:
    return min(max([_text_width(label) for label in labels] + [40.0]), 300.0)
