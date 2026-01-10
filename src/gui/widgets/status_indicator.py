"""
SyncroJob - Status Indicator
Indicatore di stato circolare animato.
"""

from PyQt6.QtCore import QAbstractAnimation, QPropertyAnimation, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget


class StatusIndicator(QWidget):
    """
    Indicatore di stato circolare con animazione di pulsazione.
    Stati supportati: 'idle', 'running', 'success', 'error'.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setLoopCount(-1)
        self.animation.setKeyValueAt(0.0, 1.0)
        self.animation.setKeyValueAt(0.5, 0.4)
        self.animation.setKeyValueAt(1.0, 1.0)

        self.current_color = QColor("#6c757d")
        self.setToolTip("Pronto")

    def set_status(self, status: str, message: str = ""):
        self.setToolTip(message)
        if status == "running":
            self.current_color = QColor("#0d6efd")
            if self.animation.state() == QAbstractAnimation.State.Stopped:
                self.animation.start()
        elif status == "success":
            self.current_color = QColor("#198754")
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)
        elif status == "error":
            self.current_color = QColor("#dc3545")
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)
        else:
            self.current_color = QColor("#6c757d")
            self.animation.stop()
            self.opacity_effect.setOpacity(1.0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.current_color))
        painter.setPen(Qt.PenStyle.NoPen)
        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawEllipse(rect)
