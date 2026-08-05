"""Small, dependency-free theme registry for terminal banners."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Theme:
    name: str
    primary: str
    accent: str
    recommended_background: str = "dark"
    contrast: str = "high"
    reset: str = "\033[0m"


_THEMES = {
    "neon": Theme("neon", "\033[38;5;51m", "\033[38;5;213m", contrast="high"),
    "sunset": Theme("sunset", "\033[38;5;208m", "\033[38;5;198m", contrast="medium"),
    "matrix": Theme("matrix", "\033[38;5;46m", "\033[38;5;118m", contrast="high"),
    "aurora": Theme("aurora", "\033[38;5;81m", "\033[38;5;141m", contrast="medium"),
    "paper": Theme(
        "paper",
        "\033[38;5;24m",
        "\033[38;5;90m",
        recommended_background="light",
        contrast="high",
    ),
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


def list_themes(background: Optional[str] = None) -> tuple[str, ...]:
    """Return all themes or only those recommended for a terminal background."""
    if background is None:
        return tuple(sorted(_THEMES))
    normalized = background.strip().lower()
    if normalized not in {"dark", "light"}:
        raise ValueError("background must be 'dark' or 'light'")
    return tuple(
        sorted(
            name
            for name, theme in _THEMES.items()
            if theme.recommended_background == normalized
        )
    )
