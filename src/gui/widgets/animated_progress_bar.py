"""SyncroJob - Animated Progress Bar.

Progress bar animata con striature, shimmer e bordo pulsante.
Supporta colori personalizzati e API asincrona.
"""

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QHideEvent,
    QLinearGradient,
    QPainter,
    QPaintEvent,
    QPen,
    QPolygonF,
    QShowEvent,
)
from PySide6.QtWidgets import QWidget

from src.gui.styles import COLORS


class AnimatedProgressBar(QWidget):
    """Progress bar animata con striature, shimmer e bordo pulsante.

    Implementa un'estetica moderna con animazioni a 30fps.

    Inizializza la barra di progresso.

    Args:
      parent: Widget genitore opzionale.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(18)
        self._value = 0
        self._stripe_offset = 0
        self._shimmer_pos = -50
        self._border_alpha = 255
        self._border_direction = -5

        # Colore predefinito
        self._accent_color = QColor(COLORS["teal_accent"])

        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._animate)
        self._anim_timer.setInterval(33)

    def set_color(self, color_hex: str) -> None:
        """Imposta il colore di accento della barra.

        Args:
          color_hex: Colore in formato esadecimale (es. #FF0000).
        """
        self._accent_color = QColor(color_hex)
        self.update()

    def set_value(self, value: int) -> None:
        """Alias per setValue (snake_case standard).

        Args:
          value: Valore intero tra 0 e 100.
        """
        self.setValue(value)

    def setValue(self, value: int) -> None:
        """Imposta il valore di avanzamento della barra.

        Args:
          value: Valore intero tra 0 e 100.
        """
        self._value = max(0, min(value, 100))
        self.update()

    def value(self) -> int:
        """Restituisce il valore corrente della barra."""
        return self._value

    def showEvent(self, event: QShowEvent) -> None:
        """Avvia l'animazione quando il widget viene mostrato."""
        super().showEvent(event)
        self._anim_timer.start()

    def hideEvent(self, event: QHideEvent) -> None:
        """Ferma l'animazione quando il widget viene nascosto per risparmiare risorse."""
        super().hideEvent(event)
        self._anim_timer.stop()

    def _animate(self) -> None:
        """Calcola i nuovi offset per l'animazione delle striature e dello shimmer."""
        self._stripe_offset = (self._stripe_offset + 2) % 20
        self._shimmer_pos += 4
        if self._shimmer_pos > self.width() + 50:
            self._shimmer_pos = -50

        self._border_alpha += self._border_direction
        if self._border_alpha <= 100:
            self._border_direction = 5
        elif self._border_alpha >= 255:
            self._border_direction = -5
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Renderizza graficamente la barra di progresso con effetti avanzati.

        Args:
          event: L'evento di pittura di Qt.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        radius = 4.0

        # 1. Sfondo
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(COLORS["border_light"]))
        painter.drawRoundedRect(QRectF(0, 0, float(w), float(h)), radius, radius)

        # 2. Chunk (parte riempita)
        chunk_width = int((self._value / 100.0) * (w - 4))
        if chunk_width > 0:
            chunk_rect = QRectF(2, 2, float(chunk_width), float(h - 4))

            # Colore Accento
            painter.setBrush(self._accent_color)
            painter.drawRoundedRect(chunk_rect, radius - 1, radius - 1)

            # 3. Striature
            painter.setClipRect(chunk_rect)
            stripe_color = QColor(255, 255, 255, 40)
            painter.setBrush(stripe_color)
            painter.setPen(Qt.PenStyle.NoPen)

            stripe_width = 10
            for x in range(-20 + self._stripe_offset, chunk_width + 20, 20):
                points = [
                    (float(x), float(h)),
                    (float(x + stripe_width), float(h)),
                    (float(x + stripe_width + 15), 0.0),
                    (float(x + 15), 0.0),
                ]
                polygon = QPolygonF([QPointF(p[0] + 2, p[1]) for p in points])
                painter.drawPolygon(polygon)

            # 4. Shimmer
            shimmer_gradient = QLinearGradient(
                float(self._shimmer_pos), 0.0, float(self._shimmer_pos + 50), 0.0
            )
            shimmer_gradient.setColorAt(0.0, QColor(255, 255, 255, 0))
            shimmer_gradient.setColorAt(0.5, QColor(255, 255, 255, 80))
            shimmer_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
            painter.setBrush(shimmer_gradient)
            painter.drawRoundedRect(chunk_rect, radius - 1, radius - 1)
            painter.setClipping(False)

        # 5. Bordo pulsante
        border_color = QColor(
            self._accent_color.red(),
            self._accent_color.green(),
            self._accent_color.blue(),
            self._border_alpha,
        )
        pen = QPen(border_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(1, 1, float(w - 2), float(h - 2)), radius, radius)
        painter.end()
