"""Check an author-drawn overview SVG against the contract in references/note-structure.md.

The overview is inlined into the note at the text width, so its units are CSS
pixels and its text is printed text. The check runs when note.json is loaded,
so a figure that would print too small, in a font outside the note's stacks,
in a color outside the tokens, or with box borders fails before rendering,
with every problem listed.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from _errors import NoteSourceError

CSS_PATH: Path = Path(__file__).resolve().parent.parent / "assets" / "note.css"
SVG_NS: str = "{http://www.w3.org/2000/svg}"
WIDTH: int = 672  # the 178 mm text column in CSS px, so one unit prints as one px
MAX_HEIGHT: int = 360  # leaves page one room for the opening bullets
# The note's own type sizes in px: 9, 10, 12.5, and 15.5 pt. The overview adds no new size to the document.
FONT_PX: tuple[float, ...] = (12, 13.33, 16.67, 20.67)
FONT_WEIGHTS: frozenset[str] = frozenset({"400", "600"})
RADII: frozenset[float] = frozenset({4, 8, 12})
ELEMENTS: frozenset[str] = frozenset({"svg", "defs", "marker", "g", "rect", "circle", "line", "path", "polygon",
                                      "polyline", "text", "tspan", "title", "desc"})
FORBIDDEN_ATTRIBUTES: frozenset[str] = frozenset({"style", "class", "href", "filter", "stroke-dasharray", "opacity"})


def check_overview(path: Path) -> None:
    """Raise NoteSourceError listing every contract problem of the overview SVG at ``path``."""
    try:
        root: ET.Element = ET.parse(path).getroot()
    except ET.ParseError as err:
        raise NoteSourceError(f"overview.src: {path} is not well-formed SVG: {err}") from err
    colors, fonts = _tokens()
    problems: list[str] = []
    if root.tag != SVG_NS + "svg":
        problems.append("the root element is not <svg> in the SVG namespace")
    view: re.Match[str] | None = re.fullmatch(rf"0 0 {WIDTH} (\d+(?:\.\d+)?)", root.get("viewBox", ""))
    if view is None:
        problems.append(f"viewBox is {root.get('viewBox')!r}; use '0 0 {WIDTH} H'")
    elif float(view.group(1)) > MAX_HEIGHT:
        problems.append(f"height {view.group(1)} is over {MAX_HEIGHT}")
    problems += [f"the root has {a}; the note sets the size" for a in ("width", "height") if a in root.attrib]
    ids: set[str] = set()
    references: set[str] = set()
    for element in root.iter():
        tag: str = element.tag.replace(SVG_NS, "")
        if tag not in ELEMENTS:
            problems.append(f"<{tag}> is not allowed; draw with shapes and text")
        if tag == "rect" and element.get("stroke", "none") != "none":
            problems.append("a <rect> has a stroke; separate boxes with fills and spacing")
        if tag == "text" and not element.get("font-family"):
            problems.append(f"<text> {(element.text or '').strip()[:20]!r} has no font-family")
        for name, value in element.attrib.items():
            name = name.split("}")[-1]
            if name in FORBIDDEN_ATTRIBUTES:
                problems.append(f"<{tag}> has {name}; use presentation attributes from the palette")
            elif name == "id":
                ids.add(value)
                if not value.startswith("ov-"):
                    problems.append(f"id {value!r} must start with 'ov-'")
            elif name in ("fill", "stroke") and value != "none" and value.upper() not in colors:
                problems.append(f"<{tag}> {name}={value} is not a token color in note.css")
            elif name == "font-family" and _families(value) not in fonts:
                problems.append(f"font-family {value!r} is not the note's --font or --mono stack")
            elif name == "font-size" and not any(abs(float(value.removesuffix("px")) - px) < 0.05 for px in FONT_PX):
                problems.append(f"font-size {value} is not one of {', '.join(f'{px:g}' for px in FONT_PX)}")
            elif name == "font-weight" and value not in FONT_WEIGHTS:
                problems.append(f"font-weight {value} is not 400 or 600")
            elif name == "rx" and float(value) not in RADII:
                problems.append(f"rx {value} is not one of 4, 8, 12")
            elif name.startswith("marker") and (m := re.fullmatch(r"url\(#(.+)\)", value)):
                references.add(m.group(1))
    problems += [f"marker #{ref} is not defined" for ref in sorted(references - ids)]
    if problems:
        listed: str = "\n  - ".join(dict.fromkeys(problems))
        raise NoteSourceError(f"overview.src: {path} breaks the overview contract "
                              f"(references/note-structure.md, Overview figure):\n  - {listed}")


def _families(stack: str) -> tuple[str, ...]:
    """A font stack as its family names, so quoting style does not matter."""
    return tuple(name.strip().strip("'\"") for name in stack.split(","))


def _tokens() -> tuple[set[str], set[tuple[str, ...]]]:
    """Token colors and the two font stacks from the :root block of note.css."""
    css: str = CSS_PATH.read_text(encoding="utf-8")
    root: re.Match[str] | None = re.search(r":root\s*\{(.*?)\}", css, re.DOTALL)
    if root is None:
        raise NoteSourceError(f"{CSS_PATH}: no :root token block")
    colors: set[str] = {c.upper() for c in re.findall(r"#[0-9A-Fa-f]{6}\b", root.group(1))}
    fonts: set[tuple[str, ...]] = {_families(m) for m in re.findall(r"--(?:font|mono):\s*([^;]+);", root.group(1))}
    return colors, fonts
