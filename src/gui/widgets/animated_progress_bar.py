"""
SyncroJob - Animated Progress Bar
Progress bar animata con striature, shimmer e bordo pulsante.
Estratto da footer_stats.py per riutilizzabilità.
"""

from PyQt6.QtCore import QPointF, QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QLinearGradient, QPainter, QPen, QPolygonF
from PyQt6.QtWidgets import QWidget


class AnimatedProgressBar(QWidget):
    """
    Progress bar animata con striature, shimmer e bordo pulsante.
    Effetto hacker-style professionale.

    Features:
    - Striature diagonali animate che scorrono
    - Shimmer (riflesso luminoso) che attraversa
    - Bordo pulsante con alpha variabile
    - Ottimizzato per ~30 FPS

    Usage:
        bar = AnimatedProgressBar()
        bar.setValue(50)  # 0-100
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 18)

        self._value = 0
        self._stripe_offset = 0
        self._shimmer_pos = -50
        self._border_alpha = 255
        self._border_direction = -5

        # Timer per animazioni (leggero, 30 FPS)
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._animate)
        self._anim_timer.setInterval(33)  # ~30 FPS

    def setValue(self, value: int):
        """Imposta il valore della progress bar (0-100)."""
        self._value = max(0, min(value, 100))
        self.update()

    def value(self) -> int:
        """Restituisce il valore corrente."""
        return self._value

    def showEvent(self, event):
        """Avvia le animazioni quando il widget diventa visibile."""
        super().showEvent(event)
        self._anim_timer.start()

    def hideEvent(self, event):
        """Ferma le animazioni quando il widget viene nascosto."""
        super().hideEvent(event)
        self._anim_timer.stop()

    def _animate(self):
        """Aggiorna le animazioni."""
        # Striature che scorrono
        self._stripe_offset = (self._stripe_offset + 2) % 20

        # Shimmer che attraversa
        self._shimmer_pos += 4
        if self._shimmer_pos > self.width() + 50:
            self._shimmer_pos = -50

        # Bordo pulsante
        self._border_alpha += self._border_direction
        if self._border_alpha <= 100:
            self._border_direction = 5
        elif self._border_alpha >= 255:
            self._border_direction = -5

        self.update()

    def paintEvent(self, event):
        """Disegna la progress bar con tutti gli effetti."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        radius = 4

        # 1. Sfondo
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(224, 224, 224))  # #E0E0E0
        painter.drawRoundedRect(QRectF(0, 0, w, h), radius, radius)

        # 2. Chunk (parte riempita)
        chunk_width = int((self._value / 100) * (w - 4))
        if chunk_width > 0:
            chunk_rect = QRectF(2, 2, chunk_width, h - 4)

            # Gradiente base nero
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRoundedRect(chunk_rect, radius - 1, radius - 1)

            # 3. Striature diagonali animate
            painter.setClipRect(chunk_rect)
            stripe_color = QColor(60, 60, 60)  # Grigio scuro per contrasto
            painter.setBrush(stripe_color)
            painter.setPen(Qt.PenStyle.NoPen)

            stripe_width = 10
            for x in range(-20 + self._stripe_offset, int(chunk_width) + 20, 20):
                points = [
                    (x, h),
                    (x + stripe_width, h),
                    (x + stripe_width + 15, 0),
                    (x + 15, 0),
                ]
                polygon = QPolygonF([QPointF(p[0] + 2, p[1]) for p in points])
                painter.drawPolygon(polygon)

            # 4. Shimmer (riflesso luminoso)
            painter.setClipRect(chunk_rect)
            shimmer_gradient = QLinearGradient(
                self._shimmer_pos, 0, self._shimmer_pos + 50, 0
            )
            shimmer_gradient.setColorAt(0.0, QColor(255, 255, 255, 0))
            shimmer_gradient.setColorAt(0.5, QColor(255, 255, 255, 80))
            shimmer_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
            painter.setBrush(shimmer_gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(chunk_rect, radius - 1, radius - 1)

            painter.setClipping(False)

        # 5. Bordo pulsante
        border_color = QColor(0, 0, 0, self._border_alpha)
        pen = QPen(border_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), radius, radius)

        painter.end()
