"""
Splash Screen con animazioni fluide a 60fps.
Il caricamento avviene in un thread separato per non bloccare MAI le animazioni.
"""

import ctypes
import math
import os
import random
from contextlib import suppress
from ctypes import Structure, byref, sizeof, wintypes

from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    Qt,
    QTimer,
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


# =============================================================================
# WINDOWS MEMORY API WRAPPER (No dependencies)
# =============================================================================
class PROCESS_MEMORY_COUNTERS_EX(Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("PageFaultCount", wintypes.DWORD),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
        ("PrivateUsage", ctypes.c_size_t),
    ]


class FILETIME(Structure):
    _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]


def get_current_process_ram_mb():
    """Restituisce l'uso RAM del processo corrente in MB su Windows."""
    try:
        # 1. Check if we are on Windows and have access to windll
        if not hasattr(ctypes, "windll") or not hasattr(ctypes.windll, "psapi"):
            return 0.0

        psapi = ctypes.windll.psapi
        kernel32 = ctypes.windll.kernel32

        # 2. Configure function signatures to prevent SegFaults on 64-bit Python
        if not getattr(psapi.GetProcessMemoryInfo, "argtypes", None):
            psapi.GetProcessMemoryInfo.argtypes = (
                wintypes.HANDLE,
                ctypes.POINTER(PROCESS_MEMORY_COUNTERS_EX),
                wintypes.DWORD,
            )
            psapi.GetProcessMemoryInfo.restype = wintypes.BOOL

        # 3. Call API
        process = kernel32.GetCurrentProcess()
        counters = PROCESS_MEMORY_COUNTERS_EX()
        counters.cb = sizeof(PROCESS_MEMORY_COUNTERS_EX)

        if psapi.GetProcessMemoryInfo(process, byref(counters), sizeof(counters)):
            return counters.WorkingSetSize / 1024 / 1024
    except Exception:
        # Fail silently to avoid crashing the splash screen
        pass
    return 0.0


# =============================================================================
# PARTICLE SYSTEM (Parallax Enhanced)
# =============================================================================
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

    def init_particles(self, count=60):
        """Initialize particle array with specified count."""
        self.particles = [Particle(self.width(), self.height()) for _ in range(count)]

    def apply_parallax(self, dx, dy):
        """Applica forza di parallasse a tutte le particelle."""
        for p in self.particles:
            p.apply_force(dx, dy)
        # Non chiamiamo update() qui per non saturare l'event loop durante il drag

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

        from PyQt6.QtGui import QPixmap

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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Background (Cached)
        if not self._bg_cache:
            self._render_background_to_cache()
        painter.drawPixmap(0, 0, self._bg_cache)

        # 2. Particles (Sprite Batching)
        if not hasattr(self, "_sprite_cache") or not self._sprite_cache:
            self._render_sprite_to_cache()

        w, h = self.width(), self.height()
        r = self.BORDER_RADIUS

        # === Save painter state before clipping ===
        painter.save()

        # Clip for particles
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, r, r)
        painter.setClipPath(path)

        # Draw sprites
        for p in self.particles:
            # Calculate opacity/scale
            op = 0.6 + 0.4 * math.sin(self.phase * 2 + p.phase)  # Opacity variation

            painter.setOpacity(op * p.opacity)

            # Scale sprite? No, just draw it (scaling is slow).
            # Or use drawPixmap with target rect for hardware scaling.
            target_size = p.size * 8  # Virtual size

            # Position centered
            x = int(p.x - target_size / 2)
            y = int(p.y - target_size / 2)

            painter.drawPixmap(
                x, y, int(target_size), int(target_size), self._sprite_cache
            )

        # Reset opacity for connections
        painter.setOpacity(1.0)

        # Draw Connections (Lines are cheap)
        self._draw_connections(painter)

        # Restore painter state (removes clipping)
        painter.restore()

        # Draw Orbs (Cached or simple?) - outside clipping
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
        pen = QPen(QColor(52, 152, 219, 40), 1)  # Constant pen
        painter.setPen(pen)

        for i, p1 in enumerate(self.particles):
            # Optimize nested loop: check only next 5 particles (spatial locality approximation)
            for p2 in self.particles[i + 1 : min(i + 6, len(self.particles))]:
                dx, dy = p1.x - p2.x, p1.y - p2.y
                if abs(dx) > max_dist or abs(dy) > max_dist:
                    continue  # Fast reject

                dist_sq = dx * dx + dy * dy
                if dist_sq < max_dist * max_dist:
                    painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))


# =============================================================================
# RESOURCE MONITOR HUD
# =============================================================================
class ResourceMonitor(QWidget):
    """HUD Monitor per Risorse (RAM/CPU Activity)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(140, 38)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Stats Layout (Vertical)
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(0)
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # RAM Indicator
        self.ram_lbl = QLabel("RAM: 0MB")
        self.ram_lbl.setStyleSheet(
            "color: rgba(52, 152, 219, 0.9); font-size: 10px; font-weight: 700; font-family: 'Consolas';"
        )

        # CPU Indicator
        self.cpu_lbl = QLabel("CPU: 0%")
        self.cpu_lbl.setStyleSheet(
            "color: rgba(46, 204, 113, 0.9); font-size: 10px; font-weight: 700; font-family: 'Consolas';"
        )

        stats_layout.addWidget(self.ram_lbl)
        stats_layout.addWidget(self.cpu_lbl)

        # Activity Indicator (Fake IO visualization)
        self.activity_bar = QFrame()
        self.activity_bar.setFixedSize(6, 28)
        self.activity_bar.setStyleSheet(
            "background: rgba(255,255,255,0.1); border-radius: 3px;"
        )

        layout.addStretch()
        layout.addLayout(stats_layout)
        layout.addWidget(self.activity_bar)

        # CPU tracking state
        self.last_proc_time = 0
        self.last_time = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(500)  # 2Hz refresh

        self._activity_level = 0

    def _get_cpu_time(self):
        """Get total kernel + user time for this process in 100ns units."""
        try:
            creation, exit, kernel, user = (
                FILETIME(),
                FILETIME(),
                FILETIME(),
                FILETIME(),
            )
            if ctypes.windll.kernel32.GetProcessTimes(
                ctypes.windll.kernel32.GetCurrentProcess(),
                byref(creation),
                byref(exit),
                byref(kernel),
                byref(user),
            ):
                # Helper to convert FILETIME to int
                def ft_to_int(ft):
                    return (ft.dwHighDateTime << 32) + ft.dwLowDateTime

                return ft_to_int(kernel) + ft_to_int(user)
        except Exception:
            pass
        return 0

    def _update_stats(self):
        import time

        # Safety check: Don't update if widget is being destroyed
        if not self.isVisible():
            return

        # Update RAM (Real)
        try:
            mb = get_current_process_ram_mb()
            self.ram_lbl.setText(f"RAM: {int(mb)}MB")
        except Exception:
            pass

        # Update CPU (Real)
        try:
            current_proc = self._get_cpu_time()
            current_time = time.time()

            if self.last_time > 0:
                delta_proc = current_proc - self.last_proc_time  # 100ns units
                delta_time = current_time - self.last_time  # seconds

                if delta_time > 0:
                    cpu_count = os.cpu_count() or 1
                    # 1 sec = 10,000,000 units of 100ns
                    cpu_percent = (
                        delta_proc / (delta_time * 10_000_000 * cpu_count)
                    ) * 100
                    self.cpu_lbl.setText(f"CPU: {cpu_percent:.1f}%")

            self.last_proc_time = current_proc
            self.last_time = current_time
        except Exception:
            self.cpu_lbl.setText("CPU: N/A")

        # Decay activity (Log based)
        try:
            self._activity_level = max(0, self._activity_level - 10)
            self._draw_activity()
        except Exception:
            pass

    def trigger_activity(self):
        """Chiamato quando c'è un log event per simulare carico CPU/IO."""
        self._activity_level = min(100, self._activity_level + 30)
        self._draw_activity()

    def _draw_activity(self):
        # Activity Bar is vertical now
        h = int((self._activity_level / 100) * 28)

        if not hasattr(self, "_bar_fill"):
            self._bar_fill = QLabel(self.activity_bar)
            self._bar_fill.setFixedWidth(6)
            self._bar_fill.move(0, 28)  # Start from bottom

        # Color gradient
        if self._activity_level > 80:
            col = "#e74c3c"
        elif self._activity_level > 40:
            col = "#f1c40f"
        else:
            col = "#2ecc71"

        self._bar_fill.setFixedHeight(max(0, h))
        self._bar_fill.move(0, 28 - h)  # Grow upwards
        self._bar_fill.setStyleSheet(f"background: {col}; border-radius: 3px;")


# =============================================================================
# ANIMATED BORDER - Bordi illuminati con ombre
# =============================================================================
class AnimatedBorder(QWidget):
    """Bordo con luce che scorre e ombre illuminate."""

    BORDER_RADIUS = 28  # Angoli molto smussati

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
        """Render animated border with glow shadows and traveling light points."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = self.BORDER_RADIUS

        intensity = 0.6 + 0.4 * math.sin(self.phase * 2)

        # === OUTER GLOW SHADOWS (multiple layers) ===
        # Layer 1 - Ombra esterna diffusa grande
        outer_glow1 = QPainterPath()
        outer_glow1.addRoundedRect(-8, -8, w + 16, h + 16, r + 8, r + 8)
        painter.setPen(Qt.PenStyle.NoPen)
        outer_gradient1 = QRadialGradient(w / 2, h / 2, max(w, h) * 0.7)
        outer_gradient1.setColorAt(0.5, QColor(52, 152, 219, int(20 * intensity)))
        outer_gradient1.setColorAt(0.7, QColor(52, 152, 219, int(10 * intensity)))
        outer_gradient1.setColorAt(1.0, QColor(52, 152, 219, 0))
        painter.fillPath(outer_glow1, outer_gradient1)

        # Layer 2 - Glow medio
        for offset in [6, 4, 2]:
            glow_path = QPainterPath()
            glow_path.addRoundedRect(
                -offset, -offset, w + offset * 2, h + offset * 2, r + offset, r + offset
            )
            alpha = int((25 - offset * 3) * intensity)
            glow_color = QColor(52, 152, 219, alpha)
            pen = QPen(glow_color, offset * 1.5)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(glow_path)

        # === BORDO PRINCIPALE CON GRADIENTE CONICO ===
        cx, cy = w / 2, h / 2
        conic = QConicalGradient(cx, cy, -math.degrees(self.phase))

        conic.setColorAt(0.0, QColor(52, 152, 219, int(255 * intensity)))
        conic.setColorAt(0.08, QColor(100, 180, 235, int(200 * intensity)))
        conic.setColorAt(0.2, QColor(155, 89, 182, int(120 * intensity)))
        conic.setColorAt(0.4, QColor(100, 60, 140, int(60 * intensity)))
        conic.setColorAt(0.6, QColor(155, 89, 182, int(60 * intensity)))
        conic.setColorAt(0.8, QColor(100, 180, 235, int(120 * intensity)))
        conic.setColorAt(0.92, QColor(52, 152, 219, int(200 * intensity)))
        conic.setColorAt(1.0, QColor(52, 152, 219, int(255 * intensity)))

        # Bordo interno luminoso
        inner_path = QPainterPath()
        inner_path.addRoundedRect(2, 2, w - 4, h - 4, r - 1, r - 1)
        pen = QPen(QBrush(conic), 2.5)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(inner_path)

        # === OMBRA INTERNA SOTTILE ===
        inner_shadow = QPainterPath()
        inner_shadow.addRoundedRect(3, 3, w - 6, h - 6, r - 2, r - 2)
        inner_pen = QPen(QColor(0, 0, 0, 40), 1)
        painter.setPen(inner_pen)
        painter.drawPath(inner_shadow)

        # === PUNTI LUMINOSI CHE VIAGGIANO ===
        self._draw_light_points(painter, w, h, r)

    def _draw_light_points(self, painter, w, h, r):
        """Punti di luce che scorrono sul bordo con scie."""
        t = self.phase
        cx, cy = w / 2, h / 2
        # Usa un'ellisse per approssimare il perimetro arrotondato
        a, b = (w / 2) - 6, (h / 2) - 6

        intensity = 0.5 + 0.5 * math.sin(self.phase * 3)

        # Punto principale con scia
        for i in range(5):
            trail_t = t - i * 0.08
            trail_intensity = intensity * (1 - i * 0.2)
            px = cx + a * math.cos(trail_t)
            py = cy + b * math.sin(trail_t)

            if i == 0:
                # Glow grande del punto principale
                glow = QRadialGradient(px, py, 50)
                glow.setColorAt(0, QColor(255, 255, 255, int(200 * trail_intensity)))
                glow.setColorAt(0.2, QColor(52, 152, 219, int(150 * trail_intensity)))
                glow.setColorAt(0.5, QColor(52, 152, 219, int(60 * trail_intensity)))
                glow.setColorAt(1, QColor(52, 152, 219, 0))
                painter.setBrush(QBrush(glow))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPoint(int(px), int(py)), 50, 50)

                # Core brillante
                painter.setBrush(QColor(255, 255, 255, int(255 * trail_intensity)))
                painter.drawEllipse(QPoint(int(px), int(py)), 4, 4)
            else:
                # Scia
                trail_size = 20 - i * 3
                trail_glow = QRadialGradient(px, py, trail_size)
                trail_glow.setColorAt(
                    0, QColor(52, 152, 219, int(80 * trail_intensity))
                )
                trail_glow.setColorAt(1, QColor(52, 152, 219, 0))
                painter.setBrush(QBrush(trail_glow))
                painter.drawEllipse(QPoint(int(px), int(py)), trail_size, trail_size)

        # Secondo punto opposto (viola)
        px2 = cx + a * math.cos(t + math.pi)
        py2 = cy + b * math.sin(t + math.pi)

        glow2 = QRadialGradient(px2, py2, 35)
        glow2.setColorAt(0, QColor(155, 89, 182, int(150 * intensity)))
        glow2.setColorAt(0.3, QColor(155, 89, 182, int(80 * intensity)))
        glow2.setColorAt(1, QColor(155, 89, 182, 0))
        painter.setBrush(QBrush(glow2))
        painter.drawEllipse(QPoint(int(px2), int(py2)), 35, 35)

        # Core viola
        painter.setBrush(QColor(200, 150, 220, int(200 * intensity)))
        painter.drawEllipse(QPoint(int(px2), int(py2)), 3, 3)


# =============================================================================
# GLOWING PROGRESS BAR
# =============================================================================
class GlowingProgressBar(QWidget):
    """Progress bar con glow e shimmer."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._display_value = 0.0  # Per animazione smooth
        self._shimmer = -100
        self._phase = 0
        self.setFixedHeight(6)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def _tick(self):
        # Interpolazione smooth del valore
        diff = self._value - self._display_value
        self._display_value += diff * 0.15

        self._shimmer += 4
        if self._shimmer > self.width() + 100:
            self._shimmer = -100
        self._phase += 0.08
        self.update()

    def setValue(self, val):
        """Set target progress value (0-100) with smooth interpolation."""
        self._value = max(0, min(100, val))

    def paintEvent(self, event):
        """Render progress bar with gradient, shimmer, and glow effects."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Track background
        track = QPainterPath()
        track.addRoundedRect(0, 0, w, h, 3, 3)
        painter.fillPath(track, QColor(15, 15, 25))

        if self._display_value > 0:
            pw = int((self._display_value / 100) * w)
            intensity = 0.8 + 0.2 * math.sin(self._phase)

            # Gradient progress
            grad = QLinearGradient(0, 0, pw, 0)
            grad.setColorAt(0, QColor(52, 152, 219))
            grad.setColorAt(
                0.5,
                QColor(
                    int(80 * intensity + 50),
                    int(160 * intensity + 40),
                    int(220 * intensity),
                ),
            )
            grad.setColorAt(1, QColor(155, 89, 182))

            progress = QPainterPath()
            progress.addRoundedRect(0, 0, pw, h, 3, 3)
            painter.fillPath(progress, grad)

            # Shimmer effect
            if 0 < self._shimmer < pw:
                # Save state before clipping
                painter.save()

                shimmer = QLinearGradient(self._shimmer - 40, 0, self._shimmer + 40, 0)
                shimmer.setColorAt(0, QColor(255, 255, 255, 0))
                shimmer.setColorAt(0.5, QColor(255, 255, 255, 100))
                shimmer.setColorAt(1, QColor(255, 255, 255, 0))
                painter.setClipPath(progress)
                painter.fillRect(self._shimmer - 40, 0, 80, h, shimmer)

                # Restore state (removes clipping)
                painter.restore()

            # Glow sotto la barra
            glow = QLinearGradient(0, h, 0, h + 8)
            glow.setColorAt(0, QColor(52, 152, 219, int(50 * intensity)))
            glow.setColorAt(1, QColor(52, 152, 219, 0))
            painter.fillRect(0, h, pw, 8, glow)


# =============================================================================
# PULSING LOGO
# =============================================================================
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
        """Set the logo pixmap to display."""
        self.pixmap = pm
        self.update()

    def _tick(self):
        self.phase += 0.04
        self.update()

    def paintEvent(self, event):
        """Render logo with pulsing scale and glow effect."""
        if not self.pixmap:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        cx, cy = self.width() / 2, self.height() / 2
        scale = 1.0 + 0.04 * math.sin(self.phase)
        glow_op = 0.4 + 0.3 * math.sin(self.phase)

        # Glow
        glow = QRadialGradient(cx, cy, 60)
        glow.setColorAt(0, QColor(52, 152, 219, int(100 * glow_op)))
        glow.setColorAt(0.5, QColor(52, 152, 219, int(40 * glow_op)))
        glow.setColorAt(1, QColor(52, 152, 219, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(cx), int(cy)), 60, 60)

        # Logo scalato
        size = int(64 * scale)
        scaled = self.pixmap.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = int(cx - scaled.width() / 2)
        y = int(cy - scaled.height() / 2)
        painter.drawPixmap(x, y, scaled)


# =============================================================================
# ANIMATED LOG LABEL
# =============================================================================
class TypewriterLabel(QLabel):
    """Label con effetto typewriter fluido."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._target = ""
        self._current = ""
        self._index = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._type)

    def set_text_animated(self, text, speed=20):
        """Start typewriter animation with specified speed in ms per character."""
        self._target = text
        self._current = ""
        self._index = 0
        self._timer.start(speed)

    def set_text_instant(self, text):
        """Set text immediately without animation."""
        self._timer.stop()
        self._target = text
        self._current = text
        self._index = len(text)
        self.setText(text)

    def _type(self):
        if self._index < len(self._target):
            self._index += 1
            self._current = self._target[: self._index]
            self.setText(self._current)
        else:
            self._timer.stop()


# =============================================================================
# STARTUP DIALOG
# =============================================================================
class StartupDialog(QDialog):
    """Splash screen con animazioni fluide a 60fps."""

    WIDTH = 700
    HEIGHT = 460

    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_state()
        self._setup_container()
        self._setup_content()
        self._setup_animations()

    def _init_window(self):
        """Configura le proprietà base della finestra."""
        self.setObjectName("StartupDialog")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet("#StartupDialog { background: transparent; border: none; }")

    def _init_state(self):
        """Inizializza lo stato interno del dialog."""
        self._worker = None
        self._thread = None
        self._init_result = False
        self.current_logs = []
        self._drag_pos = None

    def _setup_container(self):
        """Configura il container principale con particelle, bordo e shadow."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.container = QFrame()
        self.container.setObjectName("Container")
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.container.setStyleSheet(
            "#Container { background: transparent; border: none; }"
        )

        # Particle background
        self.particles = ParticleBackground(self.container)
        self.particles.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.particles.init_particles(70)

        # Animated border
        self.border = AnimatedBorder(self.container)
        self.border.setGeometry(0, 0, self.WIDTH, self.HEIGHT)

        # Content overlay
        self.content = QFrame(self.container)
        self.content.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.content.setStyleSheet("background: transparent; border: none;")

        # Shadow luminosa esterna
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(80)
        shadow.setColor(QColor(52, 152, 219, 120))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        layout.addWidget(self.container)

    def _setup_content(self):
        """Configura il contenuto principale (header, console, progress, footer)."""
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(55, 45, 55, 45)
        content_layout.setSpacing(20)

        self._setup_header(content_layout)
        self._setup_console(content_layout)
        self._setup_progress(content_layout)
        self._setup_footer(content_layout)

    def _setup_header(self, parent_layout: QVBoxLayout):
        """Configura l'header con logo, titolo e info licenza."""
        header = QHBoxLayout()
        header.setSpacing(20)

        # Logo pulsante
        self.logo = PulsingLogo()
        self.logo.setFixedSize(85, 85)
        if os.path.exists("assets/app.ico"):
            self.logo.set_pixmap(QIcon("assets/app.ico").pixmap(64, 64))
        header.addWidget(self.logo)

        # Titolo e versione
        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        self.title = QLabel()
        self.title.setTextFormat(Qt.TextFormat.RichText)
        self.title.setText(
            '<span style="font-size:40px; font-weight:800; color:white; letter-spacing:2px;">'
            'SYNCRO<span style="color:#3498db;">JOB</span></span>'
        )
        title_box.addWidget(self.title)

        from src.core.version import __version__

        self.version = QLabel(f"v{__version__}")
        self.version.setStyleSheet(
            "font-size:13px; color:rgba(52,152,219,0.9); font-weight:600; letter-spacing:3px;"
        )
        title_box.addWidget(self.version)

        header.addLayout(title_box)
        header.addStretch()

        # License info box
        self._setup_license_info(header)

        parent_layout.addLayout(header)

    def _setup_license_info(self, parent_layout: QHBoxLayout):
        """Configura il box con le informazioni della licenza."""
        from src.core.license_validator import get_hardware_id, get_license_info

        lic_info = get_license_info() or {}
        client_name = lic_info.get("Cliente", "N/D").upper()
        expiry_date = lic_info.get("Scadenza Licenza", "N/D")
        hw_id = lic_info.get("Hardware ID", get_hardware_id() or "UNKNOWN")

        license_box = QVBoxLayout()
        license_box.setSpacing(2)
        license_box.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )

        license_box.addLayout(self._create_info_row("CLIENTE:", client_name))
        license_box.addLayout(self._create_info_row("HW-ID:", hw_id))
        license_box.addLayout(self._create_info_row("SCADENZA:", expiry_date))

        parent_layout.addLayout(license_box)

    def _create_info_row(self, label_text: str, value_text: str) -> QHBoxLayout:
        """Crea una riga di informazione label: valore."""
        row = QHBoxLayout()
        row.setSpacing(5)
        row.setAlignment(Qt.AlignmentFlag.AlignRight)

        lbl = QLabel(label_text)
        lbl.setStyleSheet(
            "color: rgba(255, 255, 255, 0.5); font-size: 10px; font-weight: 600;"
        )

        val = QLabel(value_text)
        val.setStyleSheet(
            "color: rgba(255, 255, 255, 0.9); font-size: 10px; font-weight: bold; font-family: 'Consolas', monospace;"
        )

        row.addWidget(lbl)
        row.addWidget(val)
        return row

    def _setup_console(self, parent_layout: QVBoxLayout):
        """Configura la console di log con TypewriterLabels."""
        self.log_frame = QFrame()
        self.log_frame.setStyleSheet(
            "background:rgba(0,0,0,0.35); border-radius:16px; border:1px solid rgba(52,152,219,0.2);"
        )
        log_layout = QVBoxLayout(self.log_frame)
        log_layout.setContentsMargins(20, 15, 20, 15)
        log_layout.setSpacing(5)

        log_header = QLabel("INIZIALIZZAZIONE SISTEMA")
        log_header.setStyleSheet(
            "font-size:9px; color:rgba(52,152,219,0.6); letter-spacing:2px; font-weight:600;"
        )
        log_layout.addWidget(log_header)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:rgba(52,152,219,0.15);")
        log_layout.addWidget(sep)

        self.log_labels = []
        for i in range(5):
            lbl = TypewriterLabel()
            lbl.setStyleSheet(
                f"font-size:12px; color:rgba(255,255,255,{0.2 + i * 0.15}); "
                f"font-family:'Consolas','Fira Code',monospace; padding:2px 0;"
            )
            log_layout.addWidget(lbl)
            self.log_labels.append(lbl)

        parent_layout.addWidget(self.log_frame)

    def _setup_progress(self, parent_layout: QVBoxLayout):
        """Configura la barra di progresso."""
        self.progress = GlowingProgressBar()
        parent_layout.addWidget(self.progress)

    def _setup_footer(self, parent_layout: QVBoxLayout):
        """Configura il footer con indicatore, status e resource monitor."""
        footer = QHBoxLayout()
        footer.setContentsMargins(0, 5, 0, 0)

        # Indicatore di stato
        self.indicator = QLabel()
        self.indicator.setFixedSize(8, 8)
        self.indicator.setStyleSheet("background:#3498db; border-radius:4px;")
        footer.addWidget(self.indicator)
        footer.addSpacing(8)

        # Label status
        self.status = QLabel("AVVIO IN CORSO...")
        self.status.setStyleSheet(
            "font-size:11px; color:rgba(255,255,255,0.5); font-weight:600; letter-spacing:2px;"
        )
        footer.addWidget(self.status)

        # Dots animati
        self.dots = QLabel("")
        self.dots.setStyleSheet(
            "font-size:11px; color:rgba(52,152,219,0.8); font-weight:600;"
        )
        footer.addWidget(self.dots)

        footer.addStretch()

        # Resource Monitor
        self.resource_mon = ResourceMonitor()
        footer.addWidget(self.resource_mon)

        parent_layout.addLayout(footer)

    def _setup_animations(self):
        """Configura i timer per le animazioni (dots, pulse, fade-in)."""
        # Dots animation
        self._dot_count = 0
        self._dot_timer = QTimer(self)
        self._dot_timer.timeout.connect(self._animate_dots)
        self._dot_timer.start(350)

        # Pulse indicator
        self._pulse_state = True
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._pulse_indicator)
        self._pulse_timer.start(800)

        # Fade in
        self.setWindowOpacity(0.0)
        self._fade = QPropertyAnimation(self, b"windowOpacity")
        self._fade.setDuration(600)
        self._fade.setStartValue(0.0)
        self._fade.setEndValue(1.0)
        self._fade.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade.start()

    def mousePressEvent(self, event):
        """Start dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle dragging with parallax effect."""
        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_pos:
            new_pos = event.globalPosition().toPoint() - self._drag_pos
            # Calcola delta per parallasse
            current_pos = self.pos()
            dx = new_pos.x() - current_pos.x()
            dy = new_pos.y() - current_pos.y()

            self.move(new_pos)

            # Applica parallasse (direzione opposta al movimento)
            self.particles.apply_parallax(dx, dy)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Stop dragging."""
        self._drag_pos = None

    def _animate_dots(self):
        self._dot_count = (self._dot_count + 1) % 4
        self.dots.setText("." * self._dot_count)

    def _pulse_indicator(self):
        self._pulse_state = not self._pulse_state
        color = "#3498db" if self._pulse_state else "rgba(52,152,219,0.4)"
        self.indicator.setStyleSheet(f"background:{color}; border-radius:4px;")

    # DEPRECATED: This method is no longer used. Initialization now happens
    # via the generator pattern in main.py for better control flow.
    # Keeping for backward compatibility but will be removed in future versions.

    def _on_progress(self, message: str, prog: int):
        """Aggiorna UI - chiamato dal thread principale via signal."""
        self.status.setText(message.upper())

        # Trigger CPU activity simulation on log event
        self.resource_mon.trigger_activity()

        # Colore indicatore
        if prog >= 90:
            self.indicator.setStyleSheet("background:#2ecc71; border-radius:4px;")
        elif prog >= 50:
            self.indicator.setStyleSheet("background:#3498db; border-radius:4px;")
        else:
            self.indicator.setStyleSheet("background:#f39c12; border-radius:4px;")

        # Log
        entry = f"> {message}"
        self.current_logs.append(entry)
        if len(self.current_logs) > 5:
            self.current_logs.pop(0)

        for i in range(5):
            if i < len(self.current_logs):
                is_last = i == len(self.current_logs) - 1
                opacity = 1.0 if is_last else 0.25 + i * 0.12
                self.log_labels[i].setStyleSheet(
                    f"font-size:12px; color:rgba(255,255,255,{opacity}); "
                    f"font-family:'Consolas','Fira Code',monospace; padding:2px 0;"
                )
                if is_last:
                    self.log_labels[i].set_text_animated(self.current_logs[i], speed=18)
                else:
                    self.log_labels[i].set_text_instant(self.current_logs[i])
            else:
                self.log_labels[i].set_text_instant("")

        self.progress.setValue(prog)

    def _on_finished(self, success: bool):
        """Caricamento completato."""
        self._init_result = success
        if self._thread:
            self._thread.quit()
            self._thread.wait(500)
        QTimer.singleShot(400, self.accept)

    def get_result(self) -> bool:
        """Return initialization result status."""
        return self._init_result

    def update_status(self, message: str, progress: int):
        """Compatibilità con chiamate dirette."""
        self._on_progress(message, progress)

    def closeEvent(self, event):
        """Cleanup - Stop all timers and threads safely."""
        import logging

        logger = logging.getLogger("StartupDialog")

        try:
            logger.info("Closing splash screen - stopping timers...")

            # Stop all timers with safety checks
            with suppress(Exception):
                self.particles.timer.stop()
            with suppress(Exception):
                self.border.timer.stop()
            with suppress(Exception):
                self.progress.timer.stop()
            with suppress(Exception):
                self.logo.timer.stop()
            with suppress(Exception):
                self._dot_timer.stop()
            with suppress(Exception):
                self._pulse_timer.stop()
            with suppress(Exception):
                self.resource_mon.timer.stop()

            for lbl in self.log_labels:
                with suppress(Exception):
                    lbl._timer.stop()

            # Clean up thread
            if self._thread and self._thread.isRunning():
                logger.info("Waiting for worker thread to finish...")
                self._thread.quit()
                self._thread.wait(500)

            logger.info("Splash screen closed successfully")
        except Exception as e:
            logger.error(f"Error during splash cleanup: {e}", exc_info=True)

        super().closeEvent(event)
