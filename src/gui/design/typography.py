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
