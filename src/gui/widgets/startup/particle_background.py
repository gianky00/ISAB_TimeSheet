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
    QPen,
    QPixmap,
    QRadialGradient,
)
from PyQt6.QtWidgets import QWidget


class Particle:
    """Singola particella animata."""

    def __init__(self, w, h):
        self.reset(w, h)
        self.y = random.uniform(0, h)  # Posizione iniziale casuale

    def reset(self, w, h):
        """Reset particle to bottom with random properties."""
        self.x = random.uniform(0, w)
        self.y = h + 10
        self.size = random.uniform(1.5, 3.5)
        self.speed = random.uniform(0.3, 0.8)
        self.opacity = random.uniform(0.2, 0.5)
        self.phase = random.uniform(0, math.pi * 2)
        self.w, self.h = w, h

    def update(self):
        """Update particle position with upward drift and horizontal oscillation."""
        self.y -= self.speed
        self.x += math.sin(self.phase) * 0.3
        self.phase += 0.02
        if self.y < -10:
            self.reset(self.w, self.h)
        # Wrap orizzontale
        if self.x > self.w + 10:
            self.x = -10
        if self.x < -10:
            self.x = self.w + 10

    def apply_force(self, dx, dy):
        """Applica parallasse: le particelle più grandi (vicine) si muovono di più."""
        factor = self.size * 0.4  # Fattore di profondità
        self.x -= dx * factor
        self.y -= dy * factor

    def get_opacity(self):
        """Calculate current opacity with pulsing effect."""
        return self.opacity * (0.6 + 0.4 * math.sin(self.phase * 2))


class ParticleBackground(QWidget):
    """Background con particelle, connessioni e glow orbs."""

    BORDER_RADIUS = 28  # Angoli molto smussati

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.particles = []
        self.phase = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)  # 60fps
        self._bg_cache = None
        self._sprite_cache = None

    def init_particles(self, count=60):
        """Initialize particle array with specified count."""
        self.particles = [Particle(self.width(), self.height()) for _ in range(count)]

    def apply_parallax(self, dx, dy):
        """Applica forza di parallasse a tutte le particelle."""
        for p in self.particles:
            p.apply_force(dx, dy)

    def resizeEvent(self, event):
        """Invalidate cache on resize."""
        self._bg_cache = None
        super().resizeEvent(event)

    def _tick(self):
        self.phase += 0.015
        for p in self.particles:
            p.update()
        self.update()

    def _render_background_to_cache(self):
        """Render static background elements to pixmap."""
        w, h = self.width(), self.height()
        r = self.BORDER_RADIUS

        self._bg_cache = QPixmap(w, h)
        self._bg_cache.fill(Qt.GlobalColor.transparent)

        painter = QPainter(self._bg_cache)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Clip agli angoli arrotondati
        clip_path = QPainterPath()
        clip_path.addRoundedRect(0, 0, w, h, r, r)
        painter.setClipPath(clip_path)

        # Background gradient scuro
        bg = QLinearGradient(0, 0, w, h)
        bg.setColorAt(0, QColor(6, 6, 12))
        bg.setColorAt(0.5, QColor(10, 10, 18))
        bg.setColorAt(1, QColor(6, 6, 12))
        painter.fillRect(0, 0, w, h, bg)

        painter.end()

    def _render_sprite_to_cache(self):
        """Pre-render a single particle sprite (glowing dot)."""
        size = 64  # Max size
        self._sprite_cache = QPixmap(size, size)
        self._sprite_cache.fill(Qt.GlobalColor.transparent)

        pt = QPainter(self._sprite_cache)
        pt.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Glow
        glow = QRadialGradient(size / 2, size / 2, size / 2)
        glow.setColorAt(0, QColor(52, 152, 219, 200))
        glow.setColorAt(1, QColor(52, 152, 219, 0))
        pt.setBrush(QBrush(glow))
        pt.setPen(Qt.PenStyle.NoPen)
        pt.drawEllipse(0, 0, size, size)

        # Core
        pt.setBrush(QColor(255, 255, 255, 220))
        pt.drawEllipse(QPoint(int(size / 2), int(size / 2)), 4, 4)
        pt.end()

    def paintEvent(self, event):
        """Render cached background and sprite-based particles."""
        if self.width() <= 0 or self.height() <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Background (Cached)
        if not self._bg_cache:
            self._render_background_to_cache()
        painter.drawPixmap(0, 0, self._bg_cache)

        # 2. Particles (Sprite Batching)
        if not self._sprite_cache:
            self._render_sprite_to_cache()

        w, h = self.width(), self.height()
        r = self.BORDER_RADIUS

        painter.save()

        # Clip for particles
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, r, r)
        painter.setClipPath(path)

        # Draw sprites
        for p in self.particles:
            op = 0.6 + 0.4 * math.sin(self.phase * 2 + p.phase)
            painter.setOpacity(op * p.opacity)
            target_size = p.size * 8
            x = int(p.x - target_size / 2)
            y = int(p.y - target_size / 2)
            painter.drawPixmap(x, y, int(target_size), int(target_size), self._sprite_cache)

        painter.setOpacity(1.0)
        self._draw_connections(painter)
        painter.restore()
        self._draw_glow_orbs(painter, w, h)

    def _draw_glow_orbs(self, painter, w, h):
        """Orbs luminosi che pulsano."""
        intensity = 0.5 + 0.5 * math.sin(self.phase)

        # Orb blu (top-right)
        g1 = QRadialGradient(w * 0.85, h * 0.15, 180)
        g1.setColorAt(0, QColor(52, 152, 219, int(35 * intensity)))
        g1.setColorAt(0.5, QColor(52, 152, 219, int(15 * intensity)))
        g1.setColorAt(1, QColor(52, 152, 219, 0))
        painter.setBrush(QBrush(g1))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(w * 0.85), int(h * 0.15)), 180, 180)

        # Orb viola (bottom-left)
        g2 = QRadialGradient(w * 0.1, h * 0.9, 150)
        g2.setColorAt(0, QColor(155, 89, 182, int(30 * intensity)))
        g2.setColorAt(1, QColor(155, 89, 182, 0))
        painter.setBrush(QBrush(g2))
        painter.drawEllipse(QPoint(int(w * 0.1), int(h * 0.9)), 150, 150)

    def _draw_connections(self, painter):
        """Linee tra particelle vicine."""
        max_dist = 80
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
