"""
SyncroJob - Stylesheet QSS Riutilizzabili
Definizioni centralizzate per widget comuni.
"""

from typing import Final

from src.gui.styles.constants import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba

# =============================================================================
# CARD STYLES
# =============================================================================


# =============================================================================
# SHADOW STYLES
# =============================================================================
CARD_SHADOW_COLOR: Final[str] = "#30000000"
CARD_SHADOW_BLUR: Final[int] = 12


def card_style(border_color: str = COLORS["border_light"]) -> str:
    """Stile base per card con bordo colorato a sinistra."""
    return f"""
    QFrame {{
      background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS["bg_light"]}, stop:1 {COLORS["bg_white"]});
      border-radius: 12px;
      border-left: 4px solid {border_color};
      border-top: 1px solid {COLORS["border_light"]};
      border-right: 1px solid {COLORS["border_light"]};
      border-bottom: 1px solid {COLORS["border_light"]};
    }}
    QFrame:hover {{
      background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS["bg_hover"]}, stop:1 {COLORS["bg_light"]});
      border-top: 1px solid {COLORS["border_medium"]};
      border-right: 1px solid {COLORS["border_medium"]};
      border-bottom: 1px solid {COLORS["border_medium"]};
    }}
  """


CARD_STYLE_SIMPLE: Final[str] = f"""
  QFrame {{
    background-color: {COLORS["bg_white"]};
    border: 1px solid {COLORS["border_light"]};
    border-radius: 8px;
  }}
"""


# =============================================================================
# BUTTON STYLES
# =============================================================================

BUTTON_PRIMARY: Final[str] = f"""
  QPushButton {{
    background-color: {COLORS["primary_dark"]};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
  }}
  QPushButton:hover {{
    background-color: {COLORS["primary_blue"]};
  }}
  QPushButton:pressed {{
    background-color: {COLORS["primary_dark"]};
  }}
  QPushButton:disabled {{
    background-color: {COLORS["text_light"]};
  }}
"""

BUTTON_SUCCESS: Final[str] = f"""
  QPushButton {{
    background-color: {COLORS["success_dark"]};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
  }}
  QPushButton:hover {{
    background-color: {COLORS["success_green"]};
  }}
"""

BUTTON_DANGER: Final[str] = f"""
  QPushButton {{
    background-color: {COLORS["error_red"]};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
  }}
  QPushButton:hover {{
    background-color: {COLORS["error_material"]};
  }}
"""

BUTTON_SECONDARY: Final[str] = f"""
  QPushButton {{
    background-color: {COLORS["bg_light"]};
    color: {COLORS["text_dark"]};
    border: 1px solid {COLORS["border_medium"]};
    border-radius: 4px;
    padding: 8px 16px;
  }}
  QPushButton:hover {{
    background-color: {COLORS["bg_hover"]};
  }}
"""

BUTTON_TRANSPARENT: Final[str] = f"""
  QPushButton {{
    background-color: transparent;
    border: none;
  }}
  QPushButton:hover {{
    background-color: {COLORS["bg_hover"]};
    border-radius: 4px;
  }}
"""

BUTTON_ICON_ONLY: Final[str] = """
  QPushButton {
    background-color: transparent;
    border: none;
    padding: 4px;
  }
"""


# =============================================================================
# LABEL STYLES
# =============================================================================


def label_title(size: int = 14, color: str = COLORS["text_dark"]) -> str:
    """Stile per label titolo."""
    return f"""
    QLabel {{
      font-weight: 600;
      font-size: {size}px;
      color: {color};
      border: none;
      background: transparent;
    }}
  """


def label_subtitle(size: int = 12, color: str = COLORS["text_secondary"]) -> str:
    """Stile per label sottotitolo/descrizione."""
    return f"""
    QLabel {{
      font-size: {size}px;
      color: {color};
      border: none;
      background: transparent;
      font-weight: 500;
    }}
  """


LABEL_MUTED: Final[str] = f"""
  QLabel {{
    font-size: 12px;
    color: {COLORS["text_muted"]};
    border: none;
    background: transparent;
  }}
"""


# =============================================================================
# INPUT STYLES
# =============================================================================

COMBOBOX_STYLE: Final[str] = f"""
  QComboBox {{
    background-color: {COLORS["bg_white"]};
    border: 1px solid {COLORS["border_medium"]};
    border-radius: 4px;
    padding: 5px 10px;
    color: {COLORS["text_dark"]};
  }}
  QComboBox:hover {{
    border-color: {COLORS["primary_blue"]};
  }}
  QComboBox::drop-down {{
    border: none;
    width: 20px;
  }}
  QComboBox QAbstractItemView {{
    background-color: {COLORS["bg_white"]};
    border: 1px solid {COLORS["border_medium"]};
    selection-background-color: {COLORS["bg_hover"]};
  }}
"""

COMBOBOX_LIGHT_ON_DARK: Final[str] = f"""
  QComboBox {{
    background-color: {hex_to_rgba(COLORS["bg_white"], 0.2)};
    color: {COLORS["bg_white"]};
    border: 1px solid {hex_to_rgba(COLORS["bg_white"], 0.5)};
    padding: 5px 10px;
    border-radius: 4px;
  }}
  QComboBox::drop-down {{ border: none; }}
"""

LINEEDIT_STYLE: Final[str] = f"""
  QLineEdit {{
    background-color: {COLORS["bg_white"]};
    border: 1px solid {COLORS["border_medium"]};
    border-radius: 4px;
    padding: 6px 10px;
    color: {COLORS["text_dark"]};
  }}
  QLineEdit:focus {{
    border-color: {COLORS["primary_blue"]};
  }}
"""

TIMEEDIT_STYLE: Final[str] = f"""
  QTimeEdit {{
    background-color: {COLORS["bg_white"]};
    border: 1px solid {COLORS["border_medium"]};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 16px;
    font-weight: bold;
    color: {COLORS["text_dark"]};
  }}
  QTimeEdit:focus {{
    border-color: {COLORS["primary_blue"]};
  }}
  QTimeEdit::up-button, QTimeEdit::down-button {{
    width: 20px;
  }}
"""

TIMEEDIT_SMALL: Final[str] = f"""
  QTimeEdit {{
    background-color: {COLORS["bg_white"]};
    border: 1px solid {COLORS["border_medium"]};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 13px;
    color: {COLORS["text_dark"]};
  }}
"""

SPINBOX_STYLE: Final[str] = f"""
  QSpinBox {{
    background-color: {COLORS["bg_white"]};
    border: 1px solid {COLORS["border_medium"]};
    border-radius: 4px;
    padding: 4px 8px;
    color: {COLORS["text_dark"]};
  }}
  QSpinBox:focus {{
    border-color: {COLORS["primary_blue"]};
  }}
"""


# =============================================================================
# CHECKBOX STYLES
# =============================================================================

CHECKBOX_STYLE: Final[str] = f"""
  QCheckBox {{
    spacing: 8px;
    color: {COLORS["text_dark"]};
  }}
  QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid {COLORS["border_medium"]};
    background-color: {COLORS["bg_white"]};
  }}
  QCheckBox::indicator:checked {{
    background-color: {COLORS["primary_blue"]};
    border-color: {COLORS["primary_blue"]};
  }}
  QCheckBox::indicator:hover {{
    border-color: {COLORS["primary_blue"]};
  }}
"""

CHECKBOX_TOGGLE: Final[str] = f"""
  QCheckBox {{
    spacing: 8px;
  }}
  QCheckBox::indicator {{
    width: 44px;
    height: 24px;
    border-radius: 12px;
    background-color: {COLORS["border_medium"]};
  }}
  QCheckBox::indicator:checked {{
    background-color: {COLORS["success_dark"]};
  }}
"""


# =============================================================================
# CONTAINER STYLES
# =============================================================================

SCROLL_AREA_TRANSPARENT: Final[str] = """
  QScrollArea {
    background-color: transparent;
    border: none;
  }
  QScrollArea > QWidget > QWidget {
    background-color: transparent;
  }
"""

SCROLL_AREA_BORDERED: Final[str] = f"""
  QScrollArea {{
    background-color: {COLORS["bg_white"]};
    border: 1px solid {COLORS["border_light"]};
    border-radius: 8px;
  }}
"""

FRAME_HEADER: Final[str] = f"""
  QFrame {{
    background-color: {COLORS["purple"]};
    border-radius: 8px;
    padding: 10px 15px;
  }}
"""


# =============================================================================
# ICON BADGE STYLES
# =============================================================================


def icon_badge(color: str, size: int = 32) -> str:
    """Stile per badge icona circolare colorato."""
    radius = size // 2
    return f"""
    QLabel {{
      background-color: {color};
      border-radius: {radius}px;
      border: none;
      padding: 6px;
    }}
  """


# =============================================================================
# STATUS INDICATOR
# =============================================================================


def status_dot(color: str, size: int = 10) -> str:
    """Stile per dot indicatore di stato."""
    radius = size // 2
    return f"""
    QLabel {{
      background-color: {color};
      border-radius: {radius}px;
      min-width: {size}px;
      max-width: {size}px;
      min-height: {size}px;
      max-height: {size}px;
    }}
  """


LIVE_DOT: Final[str] = f"""
  QLabel {{
    background-color: {COLORS["success_green"]};
    border-radius: 5px;
    min-width: 10px;
    max-width: 10px;
    min-height: 10px;
    max-height: 10px;
  }}
"""


# =============================================================================
# EMPTY STATE
# =============================================================================

EMPTY_STATE_LABEL: Final[str] = f"""
  QLabel {{
    color: {COLORS["text_muted"]};
    font-size: 14px;
    font-style: italic;
    padding: 20px;
  }}
"""
