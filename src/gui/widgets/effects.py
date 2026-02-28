"""
SyncroJob - UI Effects Widgets.
Include componenti grafici con animazioni avanzate per il feedback visivo.
"""

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    pyqtProperty,  # type: ignore[attr-defined]
)
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QFrame

from src.gui.styles import COLORS


class HoverPulseFrame(QFrame):
    """
    Frame personalizzato che fa pulsare il bordo inferiore al passaggio del mouse.
    Fornisce un feedback visivo moderno per le sezioni card dell'applicazione.
    """

    def __init__(self, accent_color: str | None = None, parent=None):
        """Inizializza il frame con il colore di accento specificato."""
        super().__init__(parent)
        self._accent_color = QColor(accent_color or COLORS["text_dark"])
        self._pulse_val = 1.0

        self._anim = QPropertyAnimation(self, b"pulse_value")
        self._anim.setDuration(1500)
        self._anim.setStartValue(0.4)
        self._anim.setEndValue(1.0)
        self._anim.setLoopCount(-1)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutSine)

    def get_pulse_value(self) -> float:
        return self._pulse_val

    def set_pulse_value(self, v: float):
        self._pulse_val = v
        self.update()

    pulse_value = pyqtProperty(float, fget=get_pulse_value, fset=set_pulse_value)

    def enterEvent(self, event):
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.stop()
        self.set_pulse_value(1.0)
        super().leaveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            alpha = int(100 + (self._pulse_val * 155))
            pen = QPen(
                QColor(self._accent_color.red(), self._accent_color.green(), self._accent_color.blue(), alpha)
            )
            pen.setWidth(3)
            painter.setPen(pen)
            rect = self.rect()
            painter.drawLine(12, rect.height() - 2, rect.width() - 12, rect.height() - 2)
        finally:
            painter.end()
