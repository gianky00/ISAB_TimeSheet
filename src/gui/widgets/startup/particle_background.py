"""
SyncroJob - Particle Background
Sfondo animato con particelle e parallasse per la Splash Screen.
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
    """Singola particella animata."""

    def __init__(self, w: int, h: int) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.size: float = 0.0
        self.speed: float = 0.0
        self.opacity: float = 0.0
        self.phase: float = 0.0
        self.w: int = w
        self.h: int = h
        self.reset(w, h)
        self.y = random.uniform(0, h)  # Posizione iniziale casuale # noqa: S311

    def reset(self, w: int, h: int) -> None:
        """Reset particle to bottom with random properties."""
        self.x = random.uniform(0, w)  # noqa: S311
        self.y = float(h + 10)
        self.size = random.uniform(1.5, 3.5)  # noqa: S311
        self.speed = random.uniform(0.3, 0.8)  # noqa: S311
        self.opacity = random.uniform(0.2, 0.5)  # noqa: S311
        self.phase = random.uniform(0, math.pi * 2)  # noqa: S311
        self.w, self.h = w, h

    def update(self) -> None:
        """Update particle position with upward drift and horizontal oscillation."""
        self.y -= self.speed
        self.x += math.sin(self.phase) * 0.3
        self.phase += 0.02
        if self.y < -10:
            self.reset(self.w, self.h)
        # Wrap orizzontale
        if self.x > self.w + 10:
            self.x = -10.0
        if self.x < -10:
            self.x = float(self.w + 10)

    def apply_force(self, dx: float, dy: float) -> None:
        """Applica parallasse: le particelle più grandi (vicine) si muovono di più."""
        factor = self.size * 0.4  # Fattore di profondità
        self.x -= dx * factor
        self.y -= dy * factor

    def get_opacity(self) -> float:
        """Calculate current opacity with pulsing effect."""
        return self.opacity * (0.6 + 0.4 * math.sin(self.phase * 2))


class ParticleBackground(QWidget):
    """Background con particelle, connessioni e glow orbs."""

    BORDER_RADIUS = 28  # Angoli molto smussati

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.particles: list[Particle] = []
        self.phase: float = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)  # 60fps
        self._bg_cache: QPixmap | None = None
        self._sprite_cache: QPixmap | None = None

    def init_particles(self, count: int = 60) -> None:
        """Initialize particle array with specified count."""
        self.particles = [Particle(self.width(), self.height()) for _ in range(count)]

    def apply_parallax(self, dx: float, dy: float) -> None:
        """Applica forza di parallasse a tutte le particelle."""
        for p in self.particles:
            p.apply_force(dx, dy)

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        """Invalidate cache on resize."""
        self._bg_cache = None
        super().resizeEvent(event)

    def _tick(self) -> None:
        self.phase += 0.015
        for p in self.particles:
            p.update()
        self.update()

    def _render_background_to_cache(self) -> None:
        """Render static background elements to pixmap."""
        w, h = self.width(), self.height()
        r = float(self.BORDER_RADIUS)

        self._bg_cache = QPixmap(w, h)
        self._bg_cache.fill(Qt.GlobalColor.transparent)

        painter = QPainter(self._bg_cache)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Clip agli angoli arrotondati
        clip_path = QPainterPath()
        clip_path.addRoundedRect(0.0, 0.0, float(w), float(h), r, r)
        painter.setClipPath(clip_path)

        # Background gradient scuro
        bg = QLinearGradient(0.0, 0.0, float(w), float(h))
        bg.setColorAt(0.0, QColor(6, 6, 12))
        bg.setColorAt(0.5, QColor(10, 10, 18))
        bg.setColorAt(1.0, QColor(6, 6, 12))
        painter.fillRect(0, 0, w, h, bg)

        painter.end()

    def _render_sprite_to_cache(self) -> None:
        """Pre-render a single particle sprite (glowing dot)."""
        size = 64  # Max size
        self._sprite_cache = QPixmap(size, size)
        self._sprite_cache.fill(Qt.GlobalColor.transparent)

        pt = QPainter(self._sprite_cache)
        pt.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Glow
        glow = QRadialGradient(size / 2.0, size / 2.0, size / 2.0)
        glow.setColorAt(0.0, QColor(52, 152, 219, 200))
        glow.setColorAt(1.0, QColor(52, 152, 219, 0))
        pt.setBrush(QBrush(glow))
        pt.setPen(Qt.PenStyle.NoPen)
        pt.drawEllipse(0, 0, size, size)

        # Core
        pt.setBrush(QColor(255, 255, 255, 220))
        pt.drawEllipse(QPoint(int(size / 2.0), int(size / 2.0)), 4, 4)
        pt.end()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Render cached background and sprite-based particles with strict rounded corners clipping."""
        if event is None or self.width() <= 0 or self.height() <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        r = float(self.BORDER_RADIUS)

        # === CLIP PATH GLOBALE PER ELIMINARE PUNTE NEGLI ANGOLI ===
        # Applichiamo il ritaglio qui per assicurarci che NULLA sbordi
        path = QPainterPath()
        path.addRoundedRect(0.0, 0.0, float(w), float(h), r, r)
        painter.setClipPath(path)

        # 1. Background (Cached)
        if self._bg_cache is None:
            self._render_background_to_cache()
        if self._bg_cache is not None:
            painter.drawPixmap(0, 0, self._bg_cache)

        # 2. Particles (Sprite Batching)
        if self._sprite_cache is None:
            self._render_sprite_to_cache()

        painter.save()
        # Draw sprites
        if self._sprite_cache is not None:
            for p in self.particles:
                op = 0.6 + 0.4 * math.sin(self.phase * 2.0 + p.phase)
                painter.setOpacity(op * p.opacity)
                target_size = p.size * 8.0
                x = int(p.x - target_size / 2.0)
                y = int(p.y - target_size / 2.0)
                painter.drawPixmap(x, y, int(target_size), int(target_size), self._sprite_cache)

        painter.setOpacity(1.0)
        self._draw_connections(painter)
        painter.restore()

        # 3. GLOW ORBS (Ora protetti dal clip path globale)
        self._draw_glow_orbs(painter, w, h)
        
        painter.end()

    def _draw_glow_orbs(self, painter: QPainter, w: int, h: int) -> None:
        """Orbs luminosi che pulsano."""
        intensity = 0.5 + 0.5 * math.sin(self.phase)

        # Orb blu (top-right)
        g1 = QRadialGradient(w * 0.85, h * 0.15, 180.0)
        g1.setColorAt(0.0, QColor(52, 152, 219, int(35 * intensity)))
        g1.setColorAt(0.5, QColor(52, 152, 219, int(15 * intensity)))
        g1.setColorAt(1.0, QColor(52, 152, 219, 0))
        painter.setBrush(QBrush(g1))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(w * 0.85), int(h * 0.15)), 180, 180)

        # Orb viola (bottom-left)
        g2 = QRadialGradient(w * 0.1, h * 0.9, 150.0)
        g2.setColorAt(0.0, QColor(155, 89, 182, int(30 * intensity)))
        g2.setColorAt(1.0, QColor(155, 89, 182, 0))
        painter.setBrush(QBrush(g2))
        painter.drawEllipse(QPoint(int(w * 0.1), int(h * 0.9)), 150, 150)

    def _draw_connections(self, painter: QPainter) -> None:
        """Linee tra particelle vicine."""
        max_dist = 80.0
        pen = QPen(QColor(52, 152, 219, 40), 1)
        painter.setPen(pen)

        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i + 1 : min(i + 6, len(self.particles))]:
                dx, dy = p1.x - p2.x, p1.y - p2.y
                if abs(dx) > max_dist or abs(dy) > max_dist:
                    continue

                dist_sq = dx * dx + dy * dy
                if dist_sq < max_dist * max_dist:
                    painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))
