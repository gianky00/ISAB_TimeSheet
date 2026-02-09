from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QEnterEvent, QMouseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QWidget,
)


class FooterItemWidget(QWidget):
    """Elemento informativo con tag e valore."""

    def __init__(
        self, label: str, value: str = "", color: str = "#607D8B", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)
        self.lbl_tag = QLabel(label)
        self.lbl_tag.setStyleSheet(
            f"color: {color}; font-weight: bold; font-size: 11px; background: transparent;"
        )
        layout.addWidget(self.lbl_tag)
        self.lbl_val = QLabel(value)
        self.lbl_val.setStyleSheet("color: #212529; font-size: 11px; background: transparent;")
        layout.addWidget(self.lbl_val)

    def set_text(self, text: str) -> None:
        self.lbl_val.setText(text)


class StartupConsole(QLabel):
    """Console per log di sistema nel footer (FASE 1: Boot)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setText("Sistema Operativo Pronto")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            "color: #546E7A; font-family: 'Segoe UI Semibold'; font-size: 10px; padding: 0 15px; background: transparent;"
        )
        self._log_queue: list[tuple[str, bool]] = []

    def log(self, message: str, is_error: bool = False) -> None:
        color = "#cc0000" if is_error else "#000000"
        self.setText(message)
        self.setStyleSheet(
            f"color: {color}; font-family: 'Consolas', monospace; font-size: 13px; padding: 0 10px;"
        )
        self._log_queue.append((message, is_error))
        if len(self._log_queue) > 100:
            self._log_queue.pop(0)


class ClickableLabel(QLabel):
    """Label con hover effect per dati interattivi."""

    clicked = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._base_style = ""
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def setBaseStyle(self, style: str) -> None:
        self._base_style = style
        self.setStyleSheet(style)

    def enterEvent(self, event: QEnterEvent | None) -> None:
        self.setStyleSheet(
            self._base_style + " background-color: #f0f0f0; border-radius: 3px; padding: 2px 4px;"
        )
        super().enterEvent(event)

    def leaveEvent(self, event: Any | None) -> None:
        self.setStyleSheet(self._base_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class StatsCard(QFrame):
    """Card widget displaying a single statistical metric."""

    def __init__(self, title: str, value: str, icon: Any, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
