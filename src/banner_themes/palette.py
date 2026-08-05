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
    "aurora": Theme("aurora", "\033[38;5;81m", "\033[38;5;141m"),
}

_ALIASES = {
    "cyan": "neon",
    "green": "matrix",
    "orange": "sunset",
    "purple": "aurora",
}


def get_theme(name: str = "neon", *, strict: bool = False) -> Theme:
    """Return a named theme or alias, optionally rejecting unknown names."""
    key = name.strip().lower()
    resolved = _ALIASES.get(key, key)
    if strict and resolved not in _THEMES:
        choices = ", ".join(list_themes())
        raise ValueError(f"Unknown theme {name!r}; choose one of: {choices}")
    return _THEMES.get(resolved, _THEMES["neon"])


def list_themes() -> tuple[str, ...]:
    """Return the available theme names in stable display order."""
    return tuple(sorted(_THEMES))
