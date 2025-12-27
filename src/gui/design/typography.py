"""
Bot TS Design System - Typography
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class TextStyle:
    """Stile tipografico."""
    family: str
    size: int
    weight: str  # normal, bold, 500, 600, etc.
    line_height: float = 1.5

class Typography:
    """Sistema tipografico."""

    # Font Stack
    FONT_FAMILY = "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"
    FONT_MONO = "'Cascadia Code', 'Fira Code', 'Consolas', monospace"

    # Scale
    h1 = TextStyle(FONT_FAMILY, 32, "bold", 1.2)
    h2 = TextStyle(FONT_FAMILY, 24, "600", 1.3)
    h3 = TextStyle(FONT_FAMILY, 20, "600", 1.4)
    h4 = TextStyle(FONT_FAMILY, 18, "500", 1.4)

    body1 = TextStyle(FONT_FAMILY, 14, "normal", 1.5)
    body2 = TextStyle(FONT_FAMILY, 13, "normal", 1.5)

    caption = TextStyle(FONT_FAMILY, 12, "normal", 1.4)
    overline = TextStyle(FONT_FAMILY, 11, "500", 1.5)

    button = TextStyle(FONT_FAMILY, 14, "600", 1.0)

    code = TextStyle(FONT_MONO, 13, "normal", 1.6)
