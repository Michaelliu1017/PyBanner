"""Layout registry used by banner renderers and previews."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Layout:
    name: str
    width: int
    padding: int
    alignment: str = "center"


_LAYOUTS = {
    "compact": Layout("compact", width=32, padding=1),
    "standard": Layout("standard", width=48, padding=2),
    "wide": Layout("wide", width=72, padding=3),
}

_ALIASES = {
    "default": "standard",
    "full": "wide",
}


def get_layout(name: str = "standard") -> Layout:
    """Return a named layout, accepting stable aliases."""
    key = name.strip().lower()
    return _LAYOUTS.get(_ALIASES.get(key, key), _LAYOUTS["standard"])


def list_layouts() -> tuple[str, ...]:
    """Return available layout names in stable display order."""
    return tuple(sorted(_LAYOUTS))


def format_lines(lines: Iterable[str], layout: Layout) -> tuple[str, ...]:
    """Align and pad plain-text lines to the selected content width."""
    inner_width = max(1, layout.width - layout.padding * 2)
    formatted = []
    for line in lines:
        clipped = str(line)[:inner_width]
        if layout.alignment == "left":
            content = clipped.ljust(inner_width)
        elif layout.alignment == "right":
            content = clipped.rjust(inner_width)
        else:
            content = clipped.center(inner_width)
        formatted.append(" " * layout.padding + content + " " * layout.padding)
    return tuple(formatted)
