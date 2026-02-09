from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon


class LyraHeader(QFrame):
    """Intestazione del pannello Lyra con selettore modello ed export."""

    refresh_models_clicked = pyqtSignal()
    export_chat_clicked = pyqtSignal()
    model_changed = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("background-color: #6f42c1; border-radius: 8px; padding: 10px 15px;")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Lyra AI")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(title)

        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(180)
        self.model_combo.currentTextChanged.connect(lambda text: self.model_changed.emit(text))
        self.model_combo.setStyleSheet(
            """
            QComboBox {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.5);
                padding: 5px 10px;
                border-radius: 4px;
            }
            QComboBox::drop-down { border: none; }
        """
        )
        layout.addWidget(self.model_combo)

        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), "#000000"))
        self.refresh_btn.setFixedSize(32, 32)
        self.refresh_btn.setIconSize(QSize(18, 18))
        self.refresh_btn.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.refresh_btn.clicked.connect(lambda: self.refresh_models_clicked.emit())
        layout.addWidget(self.refresh_btn)

        subtitle = QLabel("Esperta Contabile")
        subtitle.setStyleSheet("color: rgba(255,255,255,0.8); margin-left: 10px;")
        layout.addWidget(subtitle)
        layout.addStretch()

        self.export_btn = QPushButton("Esporta Chat")
        self.export_btn.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.5);
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.3); }
        """
        )
        self.export_btn.clicked.connect(lambda: self.export_chat_clicked.emit())
        layout.addWidget(self.export_btn)
