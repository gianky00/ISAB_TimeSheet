"""
SyncroJob - Palette Helpers
Utility per la manipolazione dinamica dei colori e generazione di stili QSS.
"""

from PyQt6.QtGui import QColor

from src.gui.styles.constants import COLORS


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Converte un HEX in stringa rgba() per QSS."""
    color = QColor(hex_color)
    return f"rgba({color.red()}, {color.green()}, {color.blue()}, {alpha})"


def get_glass_gradient(vertical: bool = True) -> str:
    """Ritorna il gradiente Glass standard dell'applicazione."""
    direction = "x1:0, y1:0, x2:0, y2:1" if vertical else "x1:0, y1:0, x2:1, y2:0"
    return f"qlineargradient({direction}, stop:0 {COLORS['glass_dark']}, stop:1 {COLORS['glass_deep']})"


def get_status_color(status: str) -> str:
    """Mappa uno stato testuale al colore HEX corrispondente nelle costanti."""
    return {
        "success": COLORS["success_dark"],
        "error": COLORS["error_red"],
        "warning": COLORS["warning_orange"],
        "info": COLORS["info_blue"],
        "running": COLORS["primary_dark"],
        "pending": COLORS["warning_yellow"],
    }.get(status.lower(), COLORS["text_muted"])
