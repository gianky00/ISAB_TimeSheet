"""
SyncroJob - Status Indicator
Indicatore di stato circolare animato.
"""

from PyQt6.QtCore import QAbstractAnimation, QPropertyAnimation, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPaintEvent
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget

from src.gui.styles import COLORS

# Stile forzato per i tooltip in Light Mode
TOOLTIP_CSS = """
QToolTip {
    background-color: #FFFFFF;
    color: #212121;
    border: 1px solid #BBBBBB;
    border-radius: 6px;
    padding: 8px 12px;
}
"""


class StatusIndicator(QWidget):
    """
    Indicatore di stato circolare con animazione di pulsazione.
    Stati supportati: 'idle', 'running', 'success', 'error'.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.setStyleSheet(TOOLTIP_CSS)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setLoopCount(-1)
        self.animation.setKeyValueAt(0.0, 1.0)
        self.animation.setKeyValueAt(0.5, 0.4)
        self.animation.setKeyValueAt(1.0, 1.0)

        self.current_color = QColor(COLORS["text_muted"])
        self.setToolTip("Pronto")

    def set_status(self, status: str, message: str = "") -> None:
        """
        Aggiorna il colore e l'animazione dell'indicatore.

        Args:
            status: Il nuovo stato (running, success, error, idle).
            message: Messaggio per il tooltip.
        """
        self.setToolTip(message)
        if status == "running":
            self.current_color = QColor(COLORS["primary_dark"])
            if self.animation.state() == QAbstractAnimation.State.Stopped:
                self.animation.start()
        elif status == "success":
            self.current_color = QColor(COLORS["success_dark"])
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)
        elif status == "error":
            self.current_color = QColor(COLORS["error_red"])
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)
        else:
            self.current_color = QColor(COLORS["text_muted"])
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:  # noqa: N802
        """Disegna il cerchio colorato dell'indicatore."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.current_color))
        painter.setPen(Qt.PenStyle.NoPen)
        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawEllipse(rect)
        painter.end()
