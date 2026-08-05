"""Preset registry that composes banner themes with terminal layouts."""

from dataclasses import dataclass

from banner_layouts import Layout, get_layout
from banner_themes import Theme, get_theme


@dataclass(frozen=True)
class BannerPreset:
    name: str
    theme_name: str
    layout_name: str
    description: str

    @property
    def theme(self) -> Theme:
        return get_theme(self.theme_name, strict=True)

    @property
    def layout(self) -> Layout:
        return get_layout(self.layout_name)


_PRESETS = {
    "demo": BannerPreset(
        "demo",
        theme_name="aurora",
        layout_name="wide",
        description="High-impact product demonstrations and launch screens.",
    ),
    "alert": BannerPreset(
        "alert",
        theme_name="sunset",
        layout_name="compact",
        description="Compact warnings and deployment status messages.",
    ),
    "docs": BannerPreset(
        "docs",
        theme_name="paper",
        layout_name="standard",
        description="Readable examples for light terminal backgrounds.",
    ),
}

_ALIASES = {
    "default": "demo",
    "warning": "alert",
    "documentation": "docs",
}


def get_preset(name: str = "demo", *, strict: bool = False) -> BannerPreset:
    """Return a preset or alias, optionally rejecting unknown names."""
    key = name.strip().lower()
    resolved = _ALIASES.get(key, key)
    if strict and resolved not in _PRESETS:
        choices = ", ".join(list_presets())
        raise ValueError(f"Unknown preset {name!r}; choose one of: {choices}")
    return _PRESETS.get(resolved, _PRESETS["demo"])


def list_presets() -> tuple[str, ...]:
    """Return available preset names in stable display order."""
    return tuple(sorted(_PRESETS))
