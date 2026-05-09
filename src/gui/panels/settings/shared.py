from PySide6.QtCore import QSize
from PySide6.QtWidgets import QGroupBox, QPushButton, QWidget

from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import StandardGroupBox


def create_group_box(title: str) -> QGroupBox:
    """Crea un QGroupBox con stile standard."""
    group = StandardGroupBox(title)
    group.setStyleSheet(
        f"""
    QGroupBox {{
      font-weight: bold;
      border: 1px solid {COLORS["border_light"]};
      border-radius: 6px;
      margin-top: 15px;
      padding-top: 15px;
      font-size: 16px;
      color: {COLORS["text_dark"]};
    }}
    QGroupBox::title {{
      subcontrol-origin: margin;
      left: 15px;
      padding: 0 5px;
    }}
  """
    )
    return group


def list_style() -> str:
    """Restituisce lo stile CSS per QListWidget."""
    return f"""
    QListWidget {{
      border: 1px solid {COLORS["border_medium"]};
      border-radius: 4px;
      padding: 5px;
      font-size: 14px;
      background-color: {COLORS["bg_white"]};
      color: {COLORS["text_dark"]};
    }}
    QListWidget::item {{
      padding: 8px;
      border-bottom: 1px solid {COLORS["bg_alt"]};
      color: {COLORS["text_dark"]};
    }}
    QListWidget::item:selected {{
      background-color: {COLORS["primary_dark"]};
      color: white;
      border: none;
    }}
    QListWidget::item:hover:!selected {{
      background-color: {COLORS["bg_light"]};
    }}
  """


def style_input(widget: QWidget) -> None:
    """Applica lo stile standard a QLineEdit e QSpinBox."""
    widget.setStyleSheet(
        f"""
    QLineEdit, QSpinBox {{
      border: 1px solid {COLORS["border_medium"]};
      border-radius: 4px;
      padding: 10px;
      font-size: 15px;
      background-color: {COLORS["bg_white"]};
      color: {COLORS["text_dark"]};
    }}
    QLineEdit:focus, QSpinBox:focus {{
      border-color: {COLORS["primary_dark"]};
    }}
    QLineEdit:read-only {{
      background-color: {COLORS["bg_light"]};
    }}
  """
    )


def style_button(button: QPushButton) -> None:
    """Applica lo stile standard ai pulsanti."""
    button.setStyleSheet(
        f"""
    QPushButton {{
      background-color: {COLORS["bg_white"]};
      color: {COLORS["text_dark"]};
      border: 1px solid {COLORS["text_dark"]};
      border-radius: 4px;
      padding: 8px 15px;
      font-weight: bold;
      font-size: 14px;
    }}
    QPushButton:hover {{
      background-color: {COLORS["bg_hover"]};
    }}
  """
    )


def style_mini_button(button: QPushButton, color: str, text_color: str = "black") -> None:
    """Applica stile per pulsanti piccoli (es. add/remove in liste)."""
    button.setFixedSize(32, 32)
    button.setIconSize(QSize(18, 18))
    button.setStyleSheet(
        f"""
    QPushButton {{
      background-color: {COLORS["bg_white"]};
      color: {COLORS["text_dark"]};
      border: 1px solid {COLORS["text_dark"]};
      border-radius: 4px;
      font-weight: bold;
      font-size: 14px;
      padding: 0px;
      margin: 0px;
    }}
    QPushButton:hover {{
      background-color: {COLORS["bg_hover"]};
      border-color: {color};
    }}
  """
    )
