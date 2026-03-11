from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import IconButton, StandardInput
from src.utils.helpers import get_asset_path, get_colored_icon


class ChatInputBar(QWidget):
    """Barra di input per messaggi e allegati."""

    send_clicked = pyqtSignal(str)
    attach_clicked = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 20)
        main_layout.setSpacing(0)

        # Floating Container
        self.container = QFrame()
        self.container.setObjectName("floatingInput")
        self.container.setStyleSheet(f"""
            QFrame#floatingInput {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 28px;
            }}
        """)

        # Shadow for floating effect
        from PyQt6.QtGui import QColor
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.container.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(10)

        self.attach_btn = IconButton()
        self.attach_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), COLORS["text_muted"]))
        self.attach_btn.setFixedSize(40, 40)
        self.attach_btn.setIconSize(QSize(20, 20))
        self.attach_btn.setToolTip("Allega un documento (PDF)")
        self.attach_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.attach_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS["bg_hover"]};
                border: none;
                border-radius: 20px;
            }}
            QPushButton:hover {{ background-color: {COLORS["border_light"]}; }}
        """
        )
        self.attach_btn.clicked.connect(self.attach_clicked.emit)
        layout.addWidget(self.attach_btn)

        self.input_field = StandardInput()
        self.input_field.setPlaceholderText("Messaggio per Lyra...")
        self.input_field.setMinimumHeight(40)
        self.input_field.setStyleSheet(
            f"""
            QLineEdit {{
                border: none;
                background: transparent;
                padding: 0 5px;
                font-size: 15px;
                color: {COLORS["text_dark"]};
            }}
        """
        )
        self.input_field.returnPressed.connect(self._on_send)
        layout.addWidget(self.input_field)

        self.send_btn = IconButton()
        self.send_btn.setIcon(get_colored_icon(get_asset_path(Icons.SEND), "white"))
        self.send_btn.setIconSize(QSize(18, 18))
        self.send_btn.setFixedSize(40, 40)
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS["purple"]};
                border: none;
                border-radius: 20px;
            }}
            QPushButton:hover {{ background-color: {COLORS["purple"]}; opacity: 0.9; }}
            QPushButton:disabled {{ background-color: {COLORS["text_muted"]}; }}
        """
        )
        self.send_btn.clicked.connect(self._on_send)
        layout.addWidget(self.send_btn)

        main_layout.addWidget(self.container)

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
