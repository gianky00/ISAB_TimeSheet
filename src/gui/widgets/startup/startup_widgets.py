"""
SyncroJob - Startup Widgets
Collezione di widget animati utilizzati nella Splash Screen.
"""

import math

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PyQt6.QtWidgets import QLabel, QWidget


class AnimatedBorder(QWidget):
    """Bordo con luce che scorre e ombre illuminate."""

    BORDER_RADIUS = 28

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.phase = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def _tick(self):
        self.phase += 0.018
        if self.phase > math.pi * 2:
            self.phase -= math.pi * 2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = self.BORDER_RADIUS
        intensity = 0.6 + 0.4 * math.sin(self.phase * 2)

        # OUTER GLOW SHADOWS
        outer_glow1 = QPainterPath()
        outer_glow1.addRoundedRect(-8, -8, w + 16, h + 16, r + 8, r + 8)
        painter.setPen(Qt.PenStyle.NoPen)
        outer_gradient1 = QRadialGradient(w / 2, h / 2, max(w, h) * 0.7)
        outer_gradient1.setColorAt(0.5, QColor(52, 152, 219, int(20 * intensity)))
        outer_gradient1.setColorAt(0.7, QColor(52, 152, 219, int(10 * intensity)))
        outer_gradient1.setColorAt(1.0, QColor(52, 152, 219, 0))
        painter.fillPath(outer_glow1, outer_gradient1)

        for offset in (6, 4, 2):
            glow_path = QPainterPath()
            glow_path.addRoundedRect(
                -offset, -offset, w + offset * 2, h + offset * 2, r + offset, r + offset
            )
            alpha = int((25 - offset * 3) * intensity)
            pen = QPen(QColor(52, 152, 219, alpha), offset * 1.5)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.drawPath(glow_path)

        # MAIN CONIC BORDER
        cx, cy = w / 2, h / 2
        conic = QConicalGradient(cx, cy, -math.degrees(self.phase))
        conic.setColorAt(0.0, QColor(52, 152, 219, int(255 * intensity)))
        conic.setColorAt(0.2, QColor(155, 89, 182, int(120 * intensity)))
        conic.setColorAt(0.5, QColor(100, 60, 140, int(60 * intensity)))
        conic.setColorAt(0.8, QColor(100, 180, 235, int(120 * intensity)))
        conic.setColorAt(1.0, QColor(52, 152, 219, int(255 * intensity)))

        inner_path = QPainterPath()
        inner_path.addRoundedRect(2, 2, w - 4, h - 4, r - 1, r - 1)
        pen = QPen(QBrush(conic), 2.5)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(inner_path)

        self._draw_light_points(painter, w, h, r)

    def _draw_light_points(self, painter, w, h, r):
        t = self.phase
        cx, cy = w / 2, h / 2
        a, b = (w / 2) - 6, (h / 2) - 6
        intensity = 0.5 + 0.5 * math.sin(self.phase * 3)

        for i in range(5):
            trail_t = t - i * 0.08
            trail_intensity = intensity * (1 - i * 0.2)
            px, py = cx + a * math.cos(trail_t), cy + b * math.sin(trail_t)
            if i == 0:
                glow = QRadialGradient(px, py, 50)
                glow.setColorAt(0, QColor(255, 255, 255, int(200 * trail_intensity)))
                glow.setColorAt(0.5, QColor(52, 152, 219, int(60 * trail_intensity)))
                glow.setColorAt(1, QColor(52, 152, 219, 0))
                painter.setBrush(QBrush(glow))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPoint(int(px), int(py)), 50, 50)
                painter.setBrush(QColor(255, 255, 255, int(255 * trail_intensity)))
                painter.drawEllipse(QPoint(int(px), int(py)), 4, 4)
            else:
                trail_size = 20 - i * 3
                painter.setBrush(QColor(52, 152, 219, int(80 * trail_intensity)))
                painter.drawEllipse(QPoint(int(px), int(py)), trail_size, trail_size)


class GlowingProgressBar(QWidget):
    """Progress bar con glow e shimmer."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._display_value = 0.0
        self._shimmer = -100
        self._phase = 0
        self.setFixedHeight(6)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def _tick(self):
        diff = self._value - self._display_value
        self._display_value += diff * 0.15
        self._shimmer += 4
        if self._shimmer > self.width() + 100:
            self._shimmer = -100
        self._phase += 0.08
        self.update()

    def setValue(self, val):
        self._value = max(0, min(100, val))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        track = QPainterPath()
        track.addRoundedRect(0, 0, w, h, 3, 3)
        painter.fillPath(track, QColor(15, 15, 25))

        if self._display_value > 0:
            pw = int((self._display_value / 100) * w)
            grad = QLinearGradient(0, 0, pw, 0)
            grad.setColorAt(0, QColor(52, 152, 219))
            grad.setColorAt(1, QColor(155, 89, 182))

            progress = QPainterPath()
            progress.addRoundedRect(0, 0, pw, h, 3, 3)
            painter.fillPath(progress, grad)

            if 0 < self._shimmer < pw:
                painter.save()
                shimmer = QLinearGradient(self._shimmer - 40, 0, self._shimmer + 40, 0)
                shimmer.setColorAt(0, QColor(255, 255, 255, 0))
                shimmer.setColorAt(0.5, QColor(255, 255, 255, 100))
                shimmer.setColorAt(1, QColor(255, 255, 255, 0))
                painter.setClipPath(progress)
                painter.fillRect(self._shimmer - 40, 0, 80, h, shimmer)
                painter.restore()


class PulsingLogo(QWidget):
    """Logo con effetto pulsante e glow."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = None
        self.phase = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def set_pixmap(self, pm):
        self.pixmap = pm
        self.update()

    def _tick(self):
        self.phase += 0.04
        self.update()

    def paintEvent(self, event):
        if not self.pixmap:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        cx, cy = self.width() / 2, self.height() / 2
        scale = 1.0 + 0.04 * math.sin(self.phase)
        glow_op = 0.4 + 0.3 * math.sin(self.phase)

        glow = QRadialGradient(cx, cy, 60)
        glow.setColorAt(0, QColor(52, 152, 219, int(100 * glow_op)))
        glow.setColorAt(1, QColor(52, 152, 219, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(cx), int(cy)), 60, 60)

        size = int(64 * scale)
        scaled = self.pixmap.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        painter.drawPixmap(
            int(cx - scaled.width() / 2), int(cy - scaled.height() / 2), scaled
        )


class TypewriterLabel(QLabel):
    """Label con effetto typewriter fluido."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._target, self._current, self._index = "", "", 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._type)

    def set_text_animated(self, text, speed=20):
        self._target, self._current, self._index = text, "", 0
        self._timer.start(speed)

    def set_text_instant(self, text):
        self._timer.stop()
        self._target = self._current = text
        self._index = len(text)
        self.setText(text)

    def _type(self):
        if self._index < len(self._target):
            self._index += 1
            self._current = self._target[: self._index]
            self.setText(self._current)
        else:
            self._timer.stop()
