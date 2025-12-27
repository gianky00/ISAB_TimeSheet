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

# Dark Theme (Prepared but not active by default)
DARK = ColorPalette(
    # Primary - Teal Light
    primary="#4DB6AC",
    primary_variant="#80CBC4",
    on_primary="#000000",

    # Secondary - Purple Light
    secondary="#B39DDB",
    secondary_variant="#D1C4E9",
    on_secondary="#000000",

    # Background
    background="#121212",
    surface="#1E1E1E",
    surface_variant="#2D2D2D",
    on_background="#E0E0E0",
    on_surface="#FFFFFF",

    # Status
    success="#81C784",
    warning="#FFB74D",
    error="#E57373",
    info="#64B5F6",

    # Semantic
    border="#424242",
    divider="#303030",
    disabled="#757575",
    hover="#FFFFFF14",
    focus="#4DB6AC33",
)

def get_palette(theme: str = "light") -> ColorPalette:
    """Ottiene palette per tema."""
    return DARK if theme == "dark" else LIGHT
