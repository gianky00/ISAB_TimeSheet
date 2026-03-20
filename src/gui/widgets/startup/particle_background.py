"""
SyncroJob - Particle Background
Sfondo animato con particelle, connessioni neurali, circuiti e convergenza finale.
"""

import math
import random

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QPixmap,
    QRadialGradient,
    QResizeEvent,
)
from PyQt6.QtWidgets import QWidget


class Particle:
    """Singola particella animata con profondità."""

    def __init__(self, w: int, h: int) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.size: float = 0.0
        self.speed: float = 0.0
        self.opacity: float = 0.0
        self.phase: float = 0.0
        self.w, self.h = w, h
        self.reset(w, h)
        self.y = random.uniform(0, h)  # noqa: S311

    def reset(self, w: int, h: int) -> None:
        """Reset particle to bottom with random properties."""
        self.x = random.uniform(0, w)  # noqa: S311
        self.y = float(h + 20)
        self.size = random.uniform(1.2, 4.0)  # noqa: S311
        self.speed = random.uniform(0.2, 0.7)  # noqa: S311
        self.opacity = random.uniform(0.15, 0.45)  # noqa: S311
        self.phase = random.uniform(0, math.pi * 2)  # noqa: S311
        self.w, self.h = w, h

    def update(self) -> None:
        """Update particle position with upward drift."""
        self.y -= self.speed
        self.x += math.sin(self.phase) * 0.25
        self.phase += 0.015
        if self.y < -20:
            self.reset(self.w, self.h)
        if self.x > self.w + 20:
            self.x = -20.0
        if self.x < -20:
            self.x = float(self.w + 20)

    def apply_force(self, dx: float, dy: float) -> None:
        """Applica parallasse basata sulla dimensione."""
        factor = self.size * 0.35
        self.x -= dx * factor
        self.y -= dy * factor


class ParticleBackground(QWidget):
    """Background con particelle, connessioni neurali, circuiti e convergenza."""

    BORDER_RADIUS = 28

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        self.particles: list[Particle] = []
        self.phase: float = 0.0
        self.progress: float = 0.0

        # Stato impulsi neurali: list of [p1_idx, p2_idx, t]
        self._pulses: list[list[float]] = []

        # Timer 60fps
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

        self._bg_cache: QPixmap | None = None
        self._sprite_cache: QPixmap | None = None
        self._circuit_cache: QPixmap | None = None

    def init_particles(self, count: int = 65) -> None:
        self.particles = [Particle(self.width(), self.height()) for _ in range(count)]

    def set_progress(self, val: float) -> None:
        self.progress = val / 100.0

    def apply_parallax(self, dx: float, dy: float) -> None:
        for p in self.particles:
            p.apply_force(dx, dy)

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        self._bg_cache = None
        self._circuit_cache = None
        super().resizeEvent(event)

    def _tick(self) -> None:
        self.phase += 0.015
        cx, cy = self.width() / 2.0, self.height() / 2.0

        for p in self.particles:
            if self.progress > 0.92:
                # Forza gravitazionale verso il centro
                strength = (self.progress - 0.92) * 8.0
                dx, dy = cx - p.x, cy - p.y
                p.x += dx * strength * 0.04
                p.y += dy * strength * 0.04
                p.speed *= 0.94
            else:
                p.update()

        # Gestione impulsi neurali
        if random.random() < 0.12 and len(self.particles) > 1:  # noqa: S311
            p1 = float(random.randint(0, len(self.particles) - 1))  # noqa: S311
            p2 = float((int(p1) + 1) % len(self.particles))
            self._pulses.append([p1, p2, 0.0])

        for pulse in self._pulses.copy():
            pulse[2] += 0.025
            if pulse[2] > 1.0:
                self._pulses.remove(pulse)

        self.update()

    def _render_background_to_cache(self) -> None:
        w, h = self.width(), self.height()
        r = float(self.BORDER_RADIUS)
        self._bg_cache = QPixmap(w, h)
        self._bg_cache.fill(Qt.GlobalColor.transparent)
        p = QPainter(self._bg_cache)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.0, 0.0, float(w), float(h), r, r)
        p.setClipPath(path)
        bg = QLinearGradient(0.0, 0.0, float(w), float(h))
        bg.setColorAt(0.0, QColor(4, 4, 10))
        bg.setColorAt(0.5, QColor(8, 8, 16))
        bg.setColorAt(1.0, QColor(4, 4, 10))
        p.fillRect(0, 0, w, h, bg)
        p.end()

    def _render_circuit_to_cache(self) -> None:
        """Disegna tracce circuitali procedurali sullo sfondo."""
        w, h = self.width(), self.height()
        self._circuit_cache = QPixmap(w, h)
        self._circuit_cache.fill(Qt.GlobalColor.transparent)
        p = QPainter(self._circuit_cache)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor(52, 152, 219, 15), 1))

        grid = 40
        for x in range(0, w, grid):
            for y in range(0, h, grid):
                if random.random() < 0.3:  # noqa: S311
                    # Traccia a 90 o 45 gradi
                    mode = random.choice(["H", "V", "D"])  # noqa: S311
                    if mode == "H":
                        p.drawLine(x, y, x + grid, y)
                    elif mode == "V":
                        p.drawLine(x, y, x, y + grid)
                    elif mode == "D":
                        p.drawLine(x, y, int(x + grid / 2), int(y + grid / 2))

                    if random.random() < 0.2:  # noqa: S311
                        # Nodo circolare
                        p.setBrush(QColor(52, 152, 219, 25))
                        p.drawEllipse(QPoint(x, y), 2, 2)
        p.end()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        if event is None or self.width() <= 0 or self.height() <= 0:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = float(self.BORDER_RADIUS)

        path = QPainterPath()
        path.addRoundedRect(0.0, 0.0, float(w), float(h), r, r)
        painter.setClipPath(path)

        if self._bg_cache is None:
            self._render_background_to_cache()
        if self._bg_cache is not None:
            painter.drawPixmap(0, 0, self._bg_cache)

        # 1. Tracce Circuitali Pulsanti
        if self._circuit_cache is None:
            self._render_circuit_to_cache()
        if self._circuit_cache is not None:
            painter.setOpacity(0.3 + 0.2 * math.sin(self.phase * 0.5))
            painter.drawPixmap(0, 0, self._circuit_cache)
            painter.setOpacity(1.0)

        # 2. Particelle e Connessioni
        self._draw_particles(painter)
        self._draw_neural_streams(painter)
        self._draw_glow_orbs(painter, w, h)
        painter.end()

    def _draw_particles(self, painter: QPainter) -> None:
        if self._sprite_cache is None:
            self._render_sprite_to_cache()
        if self._sprite_cache is None:
            return

        max_dist = 85.0
        pen = QPen(QColor(52, 152, 219, 45), 1)

        for i, p1 in enumerate(self.particles):
            # Disegno connessioni
            painter.setPen(pen)
            for p2 in self.particles[i + 1 : min(i + 5, len(self.particles))]:
                if math.dist((p1.x, p1.y), (p2.x, p2.y)) < max_dist:
                    painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

            # Disegno Sprite
            op = 0.6 + 0.4 * math.sin(self.phase * 2.0 + p1.phase)
            painter.setOpacity(op * p1.opacity)
            target_size = p1.size * (8.0 if self.progress < 0.9 else 8.0 + (self.progress - 0.9) * 60)
            painter.drawPixmap(
                int(p1.x - target_size / 2),
                int(p1.y - target_size / 2),
                int(target_size),
                int(target_size),
                self._sprite_cache,
            )
        painter.setOpacity(1.0)

    def _render_sprite_to_cache(self) -> None:
        size = 64
        self._sprite_cache = QPixmap(size, size)
        self._sprite_cache.fill(Qt.GlobalColor.transparent)
        pt = QPainter(self._sprite_cache)
        pt.setRenderHint(QPainter.RenderHint.Antialiasing)
        glow = QRadialGradient(size / 2, size / 2, size / 2)
        glow.setColorAt(0, QColor(52, 152, 219, 190))
        glow.setColorAt(1, QColor(52, 152, 219, 0))
        pt.setBrush(QBrush(glow))
        pt.setPen(Qt.PenStyle.NoPen)
        pt.drawEllipse(0, 0, size, size)
        pt.setBrush(QColor(255, 255, 255, 210))
        pt.drawEllipse(QPoint(int(size / 2), int(size / 2)), 3, 3)
        pt.end()

    def _draw_neural_streams(self, painter: QPainter) -> None:
        for p1_idx_f, p2_idx_f, t in self._pulses:
            p1_idx, p2_idx = int(p1_idx_f), int(p2_idx_f)
            if p1_idx >= len(self.particles) or p2_idx >= len(self.particles):
                continue
            p1, p2 = self.particles[p1_idx], self.particles[p2_idx]
            if math.dist((p1.x, p1.y), (p2.x, p2.y)) > 150:
                continue
            ix, iy = p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t
            glow = QRadialGradient(ix, iy, 12.0)
            glow.setColorAt(0, QColor(255, 255, 255, 180))
            glow.setColorAt(1, QColor(52, 152, 219, 0))
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(int(ix), int(iy)), 12, 12)

    def _draw_glow_orbs(self, painter: QPainter, w: int, h: int) -> None:
        intensity = 0.5 + 0.5 * math.sin(self.phase)
        for cx, cy, color, rad in (
            (w * 0.85, h * 0.15, QColor(52, 152, 219), 200),
            (w * 0.1, h * 0.9, QColor(155, 89, 182), 160),
        ):
            g = QRadialGradient(cx, cy, float(rad))
            g.setColorAt(0, QColor(color.red(), color.green(), color.blue(), int(35 * intensity)))
            g.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(QBrush(g))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(int(cx), int(cy)), rad, rad)
