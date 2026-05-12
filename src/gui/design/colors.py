"""
Bot TS Design System - Color Palette
Basato su Material Design 3 con adattamenti per dark mode.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    """Palette colori per un tema."""

    # Primary
    primary: str
    primary_variant: str
    on_primary: str

    # Secondary
    secondary: str
    secondary_variant: str
    on_secondary: str

    # Background
    background: str
    surface: str
    surface_variant: str
    on_background: str
    on_surface: str

    # Status
    success: str
    warning: str
    error: str
    info: str

    # Semantic
    border: str
    divider: str
    disabled: str
    hover: str
    focus: str


# Light Theme
LIGHT = ColorPalette(
    # Primary - Teal (dal logo TS)
    primary="#009688",
    primary_variant="#00796B",
    on_primary="#FFFFFF",
    # Secondary - Deep Purple
    secondary="#673AB7",
    secondary_variant="#512DA8",
    on_secondary="#FFFFFF",
    # Background
    background="#FAFAFA",
    surface="#FFFFFF",
    surface_variant="#F5F5F5",
    on_background="#212121",
    on_surface="#424242",
    # Status
    success="#4CAF50",
    warning="#FF9800",
    error="#F44336",
    info="#2196F3",
    # Semantic
    border="#E0E0E0",
    divider="#EEEEEE",
    disabled="#BDBDBD",
    hover="#00000014",  # 8% black
    focus="#00968833",  # Primary with alpha
)


def get_palette(theme: str = "light") -> ColorPalette:
    """Ottiene palette per tema (attualmente solo light supportato)."""
    return LIGHT
