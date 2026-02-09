from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QGroupBox, QPushButton, QWidget


def create_group_box(title: str) -> QGroupBox:
    """Crea un QGroupBox con stile standard."""
    group = QGroupBox(title)
    group.setStyleSheet(
        """
        QGroupBox {
            font-weight: bold;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            margin-top: 15px;
            padding-top: 15px;
            font-size: 16px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 5px;
        }
    """
    )
    return group


def list_style() -> str:
    """Restituisce lo stile CSS per QListWidget."""
    return """
        QListWidget {
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 5px;
            font-size: 14px;
            background-color: white;
            color: black;
        }
        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f0f0f0;
            color: black;
        }
        QListWidget::item:selected {
            background-color: #0d6efd;
            color: white;
            border: none;
        }
        QListWidget::item:hover:!selected {
            background-color: #f8f9fa;
        }
    """


def style_input(widget: QWidget) -> None:
    """Applica lo stile standard a QLineEdit e QSpinBox."""
    widget.setStyleSheet(
        """
        QLineEdit, QSpinBox {
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 10px;
            font-size: 15px;
            background-color: white;
        }
        QLineEdit:focus, QSpinBox:focus {
            border-color: #0d6efd;
        }
        QLineEdit:read-only {
            background-color: #f8f9fa;
        }
    """
    )


def style_button(button: QPushButton) -> None:
    """Applica lo stile standard ai pulsanti."""
    button.setStyleSheet(
        """
        QPushButton {
            background-color: white;
            color: black;
            border: 1px solid black;
            border-radius: 4px;
            padding: 8px 15px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
    """
    )


def style_mini_button(button: QPushButton, color: str, text_color: str = "black") -> None:
    """Applica stile per pulsanti piccoli (es. add/remove in liste)."""
    button.setFixedSize(32, 32)
    button.setIconSize(QSize(18, 18))
    button.setStyleSheet(
        f"""
        QPushButton {{
            background-color: white;
            color: black;
            border: 1px solid black;
            border-radius: 4px;
            font-weight: bold;
            font-size: 14px;
            padding: 0px;
            margin: 0px;
        }}
        QPushButton:hover {{
            background-color: #f0f0f0;
            border-color: {color};
        }}
    """
    )
