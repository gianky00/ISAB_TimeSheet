from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)

from src.core.constants import Icons
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
        self.attach_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#000000"))
        self.attach_btn.setFixedSize(45, 45)
        self.attach_btn.setIconSize(QSize(24, 24))
        self.attach_btn.setToolTip("Allega un documento (PDF)")
        self.attach_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 2px solid #ced4da;
                border-radius: 22px;
            }
            QPushButton:hover { border-color: #6f42c1; }
        """
        )
        self.attach_btn.clicked.connect(self.attach_clicked.emit)
        layout.addWidget(self.attach_btn)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Chiedi a Lyra o trascina qui un PDF...")
        self.input_field.setMinimumHeight(45)
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #ced4da;
                border-radius: 22px;
                padding: 0 15px;
                font-size: 15px;
            }
            QLineEdit:focus { border-color: #6f42c1; }
        """
        )
        self.input_field.returnPressed.connect(self._on_send)
        layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Invia")
        self.send_btn.setMinimumHeight(45)
        self.send_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border-radius: 22px;
                padding: 0 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #59359a; }
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
        self.input_field.setEnabled(enabled)
        self.attach_btn.setEnabled(enabled)
        self.send_btn.setEnabled(enabled)
