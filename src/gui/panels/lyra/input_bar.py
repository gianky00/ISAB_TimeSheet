from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class ChatInputBar(QWidget):
    """Barra di input per messaggi e allegati."""

    send_clicked = pyqtSignal(str)
    attach_clicked = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.attach_btn = QPushButton()
        self.attach_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), COLORS["text_dark"]))
        self.attach_btn.setFixedSize(45, 45)
        self.attach_btn.setIconSize(QSize(24, 24))
        self.attach_btn.setToolTip("Allega un documento (PDF)")
        self.attach_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS['bg_white']};
                border: 2px solid {COLORS['border_medium']};
                border-radius: 22px;
            }}
            QPushButton:hover {{ border-color: {COLORS['purple']}; }}
        """
        )
        self.attach_btn.clicked.connect(self.attach_clicked.emit)
        layout.addWidget(self.attach_btn)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Chiedi a Lyra o trascina qui un PDF...")
        self.input_field.setMinimumHeight(45)
        self.input_field.setStyleSheet(
            f"""
            QLineEdit {{
                border: 2px solid {COLORS['border_medium']};
                border-radius: 22px;
                padding: 0 15px;
                font-size: 15px;
            }}
            QLineEdit:focus {{ border-color: {COLORS['purple']}; }}
        """
        )
        self.input_field.returnPressed.connect(self._on_send)
        layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Invia")
        self.send_btn.setMinimumHeight(45)
        self.send_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS['purple']};
                color: white;
                border-radius: 22px;
                padding: 0 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {COLORS['purple']}; opacity: 0.8; }}
        """
        )
        self.send_btn.clicked.connect(self._on_send)
        layout.addWidget(self.send_btn)

    def _on_send(self) -> None:
        text = self.input_field.text().strip()
        if text:
            self.send_clicked.emit(text)
            self.input_field.clear()

    def set_enabled(self, enabled: bool) -> None:
        """Abilita o disabilita i controlli di input durante l'elaborazione dell'AI."""
        self.input_field.setEnabled(enabled)
        self.attach_btn.setEnabled(enabled)
        self.send_btn.setEnabled(enabled)
