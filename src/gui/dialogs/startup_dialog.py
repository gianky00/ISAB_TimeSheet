"""
Splash Screen con animazioni fluide a 60fps.
Il caricamento avviene in un thread separato per non bloccare MAI le animazioni.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QApplication, QFrame, QGraphicsDropShadowEffect, QWidget
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect,
    QPoint, pyqtProperty, QVariantAnimation, QThread, pyqtSignal, QObject
)
from PyQt6.QtGui import (
    QIcon, QColor, QPainter, QPainterPath, QLinearGradient,
    QRadialGradient, QConicalGradient, QPen, QBrush, QFont
)
import os
import random
import math


# =============================================================================
# WORKER THREAD - Caricamento in background
# =============================================================================
class InitWorker(QObject):
    """Esegue il caricamento in un thread separato."""
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(bool)

    def __init__(self, mw_instance=None):
        super().__init__()
        self.mw_instance = mw_instance

    def run(self):
        try:
            from src.core.app_initializer import AppInitializer
            success = AppInitializer.initialize(
                status_callback=lambda msg, prog: self.progress.emit(msg, prog),
                mw_instance=self.mw_instance
            )
            self.finished.emit(success)
        except Exception as e:
            import logging
            logging.getLogger("InitWorker").error(f"Error: {e}")
            self.finished.emit(False)


# =============================================================================
# PARTICLE SYSTEM
# =============================================================================
class Particle:
    """Singola particella animata."""
    def __init__(self, w, h):
        self.reset(w, h)
        self.y = random.uniform(0, h)  # Posizione iniziale casuale

    def reset(self, w, h):
        self.x = random.uniform(0, w)
        self.y = h + 10
        self.size = random.uniform(1.5, 3.5)
        self.speed = random.uniform(0.3, 0.8)
        self.opacity = random.uniform(0.2, 0.5)
        self.phase = random.uniform(0, math.pi * 2)
        self.w, self.h = w, h

    def update(self):
        self.y -= self.speed
        self.x += math.sin(self.phase) * 0.3
        self.phase += 0.02
        if self.y < -10:
            self.reset(self.w, self.h)

    def get_opacity(self):
        return self.opacity * (0.6 + 0.4 * math.sin(self.phase * 2))


class ParticleBackground(QWidget):
    """Background con particelle, connessioni e glow orbs."""
    BORDER_RADIUS = 28  # Angoli molto smussati

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.particles = []
        self.phase = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)  # 60fps

    def init_particles(self, count=60):
        self.particles = [Particle(self.width(), self.height()) for _ in range(count)]

    def _tick(self):
        self.phase += 0.015
        for p in self.particles:
            p.update()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = self.BORDER_RADIUS

        # Clip agli angoli arrotondati
        clip_path = QPainterPath()
        clip_path.addRoundedRect(0, 0, w, h, r, r)
        painter.setClipPath(clip_path)

        # Background gradient scuro
        bg = QLinearGradient(0, 0, w, h)
        bg.setColorAt(0, QColor(6, 6, 12))
        bg.setColorAt(0.5, QColor(10, 10, 18))
        bg.setColorAt(1, QColor(6, 6, 12))
        painter.fillRect(self.rect(), bg)

        # Glow orbs pulsanti
        self._draw_glow_orbs(painter, w, h)

        # Connessioni tra particelle vicine
        self._draw_connections(painter)

        # Particelle
        for p in self.particles:
            op = p.get_opacity()
            # Glow
            glow = QRadialGradient(p.x, p.y, p.size * 4)
            glow.setColorAt(0, QColor(52, 152, 219, int(op * 80)))
            glow.setColorAt(1, QColor(52, 152, 219, 0))
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(int(p.x), int(p.y)), int(p.size * 4), int(p.size * 4))
            # Core
            painter.setBrush(QColor(52, 152, 219, int(op * 255)))
            painter.drawEllipse(QPoint(int(p.x), int(p.y)), int(p.size), int(p.size))

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
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                dx, dy = p1.x - p2.x, p1.y - p2.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < max_dist:
                    opacity = (1 - dist / max_dist) * 0.12
                    pen = QPen(QColor(52, 152, 219, int(opacity * 255)), 0.5)
                    painter.setPen(pen)
                    painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

        # Reset clipping
        painter.setClipping(False)


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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = self.BORDER_RADIUS

        intensity = 0.6 + 0.4 * math.sin(self.phase * 2)

        # === OMBRE LUMINOSE ESTERNE (multiple layers) ===
        # Layer 1 - Ombra esterna diffusa grande
        outer_glow1 = QPainterPath()
        outer_glow1.addRoundedRect(-8, -8, w + 16, h + 16, r + 8, r + 8)
        painter.setPen(Qt.PenStyle.NoPen)
        outer_gradient1 = QRadialGradient(w/2, h/2, max(w, h) * 0.7)
        outer_gradient1.setColorAt(0.5, QColor(52, 152, 219, int(20 * intensity)))
        outer_gradient1.setColorAt(0.7, QColor(52, 152, 219, int(10 * intensity)))
        outer_gradient1.setColorAt(1.0, QColor(52, 152, 219, 0))
        painter.fillPath(outer_glow1, outer_gradient1)

        # Layer 2 - Glow medio
        for offset in [6, 4, 2]:
            glow_path = QPainterPath()
            glow_path.addRoundedRect(
                -offset, -offset, w + offset*2, h + offset*2,
                r + offset, r + offset
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
                trail_glow.setColorAt(0, QColor(52, 152, 219, int(80 * trail_intensity)))
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
        self._value = max(0, min(100, val))

    def paintEvent(self, event):
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
            grad.setColorAt(0.5, QColor(int(80 * intensity + 50), int(160 * intensity + 40), int(220 * intensity)))
            grad.setColorAt(1, QColor(155, 89, 182))

            progress = QPainterPath()
            progress.addRoundedRect(0, 0, pw, h, 3, 3)
            painter.fillPath(progress, grad)

            # Shimmer effect
            if 0 < self._shimmer < pw:
                shimmer = QLinearGradient(self._shimmer - 40, 0, self._shimmer + 40, 0)
                shimmer.setColorAt(0, QColor(255, 255, 255, 0))
                shimmer.setColorAt(0.5, QColor(255, 255, 255, 100))
                shimmer.setColorAt(1, QColor(255, 255, 255, 0))
                painter.setClipPath(progress)
                painter.fillRect(self._shimmer - 40, 0, 80, h, shimmer)
                painter.setClipping(False)

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
        scaled = self.pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                                     Qt.TransformationMode.SmoothTransformation)
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
        self._target = text
        self._current = ""
        self._index = 0
        self._timer.start(speed)

    def set_text_instant(self, text):
        self._timer.stop()
        self._target = text
        self._current = text
        self._index = len(text)
        self.setText(text)

    def _type(self):
        if self._index < len(self._target):
            self._index += 1
            self._current = self._target[:self._index]
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
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self._worker = None
        self._thread = None
        self._init_result = False
        self.current_logs = []

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.container = QFrame()
        self.container.setObjectName("Container")

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
        self.content.setStyleSheet("background: transparent;")

        # Shadow luminosa esterna
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(80)
        shadow.setColor(QColor(52, 152, 219, 120))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        # Content layout
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(55, 45, 55, 45)
        content_layout.setSpacing(20)

        # === HEADER ===
        header = QHBoxLayout()
        header.setSpacing(20)

        self.logo = PulsingLogo()
        self.logo.setFixedSize(85, 85)
        if os.path.exists("assets/app.ico"):
            self.logo.set_pixmap(QIcon("assets/app.ico").pixmap(64, 64))
        header.addWidget(self.logo)

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
        content_layout.addLayout(header)

        # === LOG CONSOLE ===
        self.log_frame = QFrame()
        self.log_frame.setStyleSheet(
            "background:rgba(0,0,0,0.35); border-radius:16px; border:1px solid rgba(52,152,219,0.2);"
        )
        log_layout = QVBoxLayout(self.log_frame)
        log_layout.setContentsMargins(20, 15, 20, 15)
        log_layout.setSpacing(5)

        log_header = QLabel("SYSTEM INITIALIZATION")
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

        content_layout.addWidget(self.log_frame)

        # === PROGRESS BAR ===
        self.progress = GlowingProgressBar()
        content_layout.addWidget(self.progress)

        # === FOOTER ===
        footer = QHBoxLayout()
        footer.setContentsMargins(0, 5, 0, 0)

        self.indicator = QLabel()
        self.indicator.setFixedSize(8, 8)
        self.indicator.setStyleSheet("background:#3498db; border-radius:4px;")
        footer.addWidget(self.indicator)
        footer.addSpacing(8)

        self.status = QLabel("INITIALIZING")
        self.status.setStyleSheet(
            "font-size:11px; color:rgba(255,255,255,0.5); font-weight:600; letter-spacing:2px;"
        )
        footer.addWidget(self.status)

        self.dots = QLabel("")
        self.dots.setStyleSheet("font-size:11px; color:rgba(52,152,219,0.8); font-weight:600;")
        footer.addWidget(self.dots)
        footer.addStretch()

        content_layout.addLayout(footer)
        layout.addWidget(self.container)

        # Animazioni ausiliarie
        self._dot_count = 0
        self._dot_timer = QTimer(self)
        self._dot_timer.timeout.connect(self._animate_dots)
        self._dot_timer.start(350)

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

    def _animate_dots(self):
        self._dot_count = (self._dot_count + 1) % 4
        self.dots.setText("." * self._dot_count)

    def _pulse_indicator(self):
        self._pulse_state = not self._pulse_state
        color = "#3498db" if self._pulse_state else "rgba(52,152,219,0.4)"
        self.indicator.setStyleSheet(f"background:{color}; border-radius:4px;")

    def start_initialization(self, mw_instance=None):
        """Avvia il caricamento in un thread separato - animazioni MAI bloccate."""
        self._thread = QThread()
        self._worker = InitWorker(mw_instance)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)

        self._thread.start()

    def _on_progress(self, message: str, prog: int):
        """Aggiorna UI - chiamato dal thread principale via signal."""
        self.status.setText(message.upper())

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
                is_last = (i == len(self.current_logs) - 1)
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
        return self._init_result

    def update_status(self, message: str, progress: int):
        """Compatibilità con chiamate dirette."""
        self._on_progress(message, progress)

    def closeEvent(self, event):
        """Cleanup."""
        self.particles.timer.stop()
        self.border.timer.stop()
        self.progress.timer.stop()
        self.logo.timer.stop()
        self._dot_timer.stop()
        self._pulse_timer.stop()
        for lbl in self.log_labels:
            lbl._timer.stop()
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(500)
        super().closeEvent(event)
