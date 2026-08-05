"""Small, dependency-free theme registry for terminal banners."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    primary: str
    accent: str
    reset: str = "\033[0m"


_THEMES = {
    "neon": Theme("neon", "\033[38;5;51m", "\033[38;5;213m"),
    "sunset": Theme("sunset", "\033[38;5;208m", "\033[38;5;198m"),
    "matrix": Theme("matrix", "\033[38;5;46m", "\033[38;5;118m"),
}


def get_theme(name: str = "neon") -> Theme:
    """Return a named theme, defaulting to neon for unknown names."""
    return _THEMES.get(name.lower(), _THEMES["neon"])


def list_themes() -> tuple[str, ...]:
    """Return the available theme names in stable display order."""
    return tuple(sorted(_THEMES))
