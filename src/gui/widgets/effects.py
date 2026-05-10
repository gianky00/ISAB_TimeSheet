"""
SyncroJob - UI Effects Widgets.
Include componenti grafici con animazioni avanzate per il feedback visivo.
"""

from __future__ import annotations

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QEvent,
    QPropertyAnimation,
    Signal,
)
from PySide6.QtGui import QColor, QEnterEvent, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QFrame, QWidget

from src.gui.styles import COLORS


class HoverPulseFrame(QFrame):
    """
    Frame personalizzato che fa pulsare il bordo inferiore al passaggio del mouse.
    Fornisce un feedback visivo moderno per le sezioni card dell'applicazione.
    """

    pulse_value_changed = Signal(float)

    def __init__(self, accent_color: str | None = None, parent: QWidget | None = None) -> None:
        """
        Inizializza il frame con il colore di accento specificato.

        Args:
          accent_color: Colore esadecimale opzionale per la linea pulsante.
          parent: Widget genitore opzionale.
        """
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
        """Restituisce il valore corrente dell'animazione pulsante."""
        return self._pulse_val

    def set_pulse_value(self, v: float) -> None:
        """Imposta il valore dell'animazione pulsante e forza il ridisegno."""
        if self._pulse_val != v:
            self._pulse_val = v
            self.pulse_value_changed.emit(v)
            self.update()

    pulse_value = Property(float, fget=get_pulse_value, fset=set_pulse_value, notify=pulse_value_changed)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Avvia l'animazione pulsante all'ingresso del mouse."""
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Ferma l'animazione pulsante all'uscita del mouse."""
        self._anim.stop()
        self.set_pulse_value(1.0)
        super().leaveEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Disegna la linea pulsante alla base del widget.

        Args:
          event: L'evento di pittura di Qt.
        """
        super().paintEvent(event)
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            alpha = int(100 + (self._pulse_val * 155))
            pen = QPen(
                QColor(
                    self._accent_color.red(),
                    self._accent_color.green(),
                    self._accent_color.blue(),
                    alpha,
                )
            )
            pen.setWidth(3)
            painter.setPen(pen)
            rect = self.rect()
            painter.drawLine(12, rect.height() - 2, rect.width() - 12, rect.height() - 2)
        finally:
            painter.end()
