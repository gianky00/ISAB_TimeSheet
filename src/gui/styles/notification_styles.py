"""SyncroJob - Notification Styling Engine.

Definisce le palette colori, i gradienti e le icone per i diversi livelli di notifica.
"""

from typing import Any

from src.application.services.constants import Icons
from src.gui.styles import COLORS

# Stili per livello di notifica
LEVEL_STYLES: dict[str, dict[str, Any]] = {
    "error": {
        "accent": COLORS["error_red"],
        "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})",
        "icon": Icons.X_CIRCLE,
        "icon_color": COLORS["error_red"],
        "badge_bg": "#FFEBEE",
    },
    "warning": {
        "accent": COLORS["warning_orange"],
        "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})",
        "icon": Icons.ALERT_TRIANGLE,
        "icon_color": COLORS["warning_orange"],
        "badge_bg": "#FFF3E0",
    },
    "success": {
        "accent": COLORS["success_dark"],
        "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})",
        "icon": Icons.CHECK_CIRCLE,
        "icon_color": COLORS["success_dark"],
        "badge_bg": "#E8F5E9",
    },
    "info": {
        "accent": COLORS["primary_blue"],
        "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})",
        "icon": Icons.INFO,
        "icon_color": COLORS["primary_blue"],
        "badge_bg": "#E3F2FD",
    },
}


def get_notification_qss(level: str, is_read: bool) -> str:
    """Genera lo stylesheet QSS per una card di notifica."""
    style = LEVEL_STYLES.get(level.lower(), LEVEL_STYLES["info"])
    accent_color = style["accent"]
    gradient = style["gradient"]

    # Background: gradient per non lette, bianco per lette
    bg = gradient if not is_read else COLORS["bg_white"]

    return f"""
    NotificationCard {{
      background: {bg};
      border-radius: 12px;
      border-left: 4px solid {accent_color};
      border-top: 1px solid {COLORS["border_light"]};
      border-right: 1px solid {COLORS["border_light"]};
      border-bottom: 1px solid {COLORS["border_light"]};
    }}
    NotificationCard:hover {{
      background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS["bg_hover"]}, stop:1 {COLORS["bg_white"]});
      border-left: 4px solid {accent_color};
      border-top: 1px solid {COLORS["border_medium"]};
      border-right: 1px solid {COLORS["border_medium"]};
      border-bottom: 1px solid {COLORS["border_medium"]};
    }}
  """
