from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QApplication, QFrame, QGraphicsDropShadowEffect, QWidget
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect,
    QPoint, QParallelAnimationGroup, QSequentialAnimationGroup,
    pyqtProperty, QVariantAnimation, QSize
)
from PyQt6.QtGui import (
    QIcon, QColor, QPainter, QPainterPath, QLinearGradient,
    QRadialGradient, QConicalGradient, QPen, QBrush, QFont, QFontDatabase
)
import os
import random
import math


class Particle:
    """Singola particella per l'effetto background."""
    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.size = random.uniform(1, 3)
        self.speed_x = random.uniform(-0.3, 0.3)
        self.speed_y = random.uniform(-0.5, -0.1)
        self.opacity = random.uniform(0.1, 0.4)
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.width = width
        self.height = height

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.pulse_phase += 0.05

        # Wrap around
        if self.y < -10:
            self.y = self.height + 10
            self.x = random.uniform(0, self.width)
        if self.x < -10:
            self.x = self.width + 10
        elif self.x > self.width + 10:
            self.x = -10

    def get_opacity(self):
        return self.opacity * (0.5 + 0.5 * math.sin(self.pulse_phase))


class ParticleBackground(QWidget):
    """Widget per il background con particelle animate."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.particles = []
        self.connection_distance = 100
        self.glow_phase = 0
        self.primary_color = QColor(52, 152, 219)  # Blue accent
        self.secondary_color = QColor(155, 89, 182)  # Purple accent

        # Timer per l'animazione
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(16)  # ~60 FPS

    def init_particles(self, count=50):
        """Inizializza le particelle."""
        self.particles = [Particle(self.width(), self.height()) for _ in range(count)]

    def _animate(self):
        """Aggiorna le particelle."""
        self.glow_phase += 0.02
        for p in self.particles:
            p.update()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(8, 8, 15))
        gradient.setColorAt(0.5, QColor(12, 12, 20))
        gradient.setColorAt(1, QColor(8, 8, 15))
        painter.fillRect(self.rect(), gradient)

        # Glow orbs in background
        self._draw_glow_orbs(painter)

        # Draw connections between particles
        self._draw_connections(painter)

        # Draw particles
        for p in self.particles:
            opacity = p.get_opacity()
            color = QColor(self.primary_color)
            color.setAlphaF(opacity)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPoint(int(p.x), int(p.y)), int(p.size), int(p.size))

            # Glow effect
            glow_color = QColor(self.primary_color)
            glow_color.setAlphaF(opacity * 0.3)
            painter.setBrush(QBrush(glow_color))
            painter.drawEllipse(QPoint(int(p.x), int(p.y)), int(p.size * 3), int(p.size * 3))

    def _draw_glow_orbs(self, painter):
        """Disegna orbs luminosi sullo sfondo."""
        # Primary glow orb (top-right)
        glow1_x = self.width() * 0.8
        glow1_y = self.height() * 0.2
        glow1_size = 150 + 20 * math.sin(self.glow_phase)

        gradient1 = QRadialGradient(glow1_x, glow1_y, glow1_size)
        gradient1.setColorAt(0, QColor(52, 152, 219, 30))
        gradient1.setColorAt(0.5, QColor(52, 152, 219, 10))
        gradient1.setColorAt(1, QColor(52, 152, 219, 0))
        painter.setBrush(QBrush(gradient1))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(glow1_x), int(glow1_y)), int(glow1_size), int(glow1_size))

        # Secondary glow orb (bottom-left)
        glow2_x = self.width() * 0.15
        glow2_y = self.height() * 0.85
        glow2_size = 120 + 15 * math.sin(self.glow_phase + math.pi)

        gradient2 = QRadialGradient(glow2_x, glow2_y, glow2_size)
        gradient2.setColorAt(0, QColor(155, 89, 182, 25))
        gradient2.setColorAt(0.5, QColor(155, 89, 182, 8))
        gradient2.setColorAt(1, QColor(155, 89, 182, 0))
        painter.setBrush(QBrush(gradient2))
        painter.drawEllipse(QPoint(int(glow2_x), int(glow2_y)), int(glow2_size), int(glow2_size))

    def _draw_connections(self, painter):
        """Disegna le connessioni tra particelle vicine."""
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                dist = math.sqrt(dx*dx + dy*dy)

                if dist < self.connection_distance:
                    opacity = (1 - dist / self.connection_distance) * 0.15
                    color = QColor(self.primary_color)
                    color.setAlphaF(opacity)
                    pen = QPen(color, 0.5)
                    painter.setPen(pen)
                    painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))


class GlowingProgressBar(QWidget):
    """Progress bar con effetto glow animato."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._glow_phase = 0
        self._shimmer_pos = 0
        self.setFixedHeight(6)

        # Timer per animazioni
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._animate)
        self.anim_timer.start(16)

    def _animate(self):
        self._glow_phase += 0.1
        self._shimmer_pos += 3
        if self._shimmer_pos > self.width() + 100:
            self._shimmer_pos = -100
        self.update()

    @pyqtProperty(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = max(0, min(100, val))
        self.update()

    def setValue(self, val):
        self._value = max(0, min(100, val))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background track
        track_rect = self.rect()
        track_path = QPainterPath()
        track_path.addRoundedRect(0, 0, track_rect.width(), track_rect.height(), 3, 3)
        painter.fillPath(track_path, QColor(20, 20, 30))

        if self._value > 0:
            # Progress fill
            progress_width = int((self._value / 100) * track_rect.width())

            # Gradient for progress
            gradient = QLinearGradient(0, 0, progress_width, 0)
            glow_intensity = 0.8 + 0.2 * math.sin(self._glow_phase)

            gradient.setColorAt(0, QColor(52, 152, 219))
            gradient.setColorAt(0.5, QColor(int(100 * glow_intensity), int(180 * glow_intensity), int(230 * glow_intensity)))
            gradient.setColorAt(1, QColor(155, 89, 182))

            progress_path = QPainterPath()
            progress_path.addRoundedRect(0, 0, progress_width, track_rect.height(), 3, 3)
            painter.fillPath(progress_path, gradient)

            # Shimmer effect
            if self._shimmer_pos < progress_width:
                shimmer_gradient = QLinearGradient(self._shimmer_pos - 50, 0, self._shimmer_pos + 50, 0)
                shimmer_gradient.setColorAt(0, QColor(255, 255, 255, 0))
                shimmer_gradient.setColorAt(0.5, QColor(255, 255, 255, 80))
                shimmer_gradient.setColorAt(1, QColor(255, 255, 255, 0))

                shimmer_path = QPainterPath()
                shimmer_path.addRoundedRect(0, 0, progress_width, track_rect.height(), 3, 3)
                painter.setClipPath(shimmer_path)
                painter.fillRect(int(self._shimmer_pos - 50), 0, 100, track_rect.height(), shimmer_gradient)
                painter.setClipping(False)

            # Glow under progress bar
            glow_gradient = QLinearGradient(0, track_rect.height(), progress_width, track_rect.height() + 10)
            glow_gradient.setColorAt(0, QColor(52, 152, 219, int(60 * glow_intensity)))
            glow_gradient.setColorAt(1, QColor(52, 152, 219, 0))
            painter.fillRect(0, track_rect.height(), progress_width, 10, glow_gradient)


class AnimatedLogLabel(QLabel):
    """Label con effetto typewriter fluido e indipendente dal caricamento."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._target_text = ""
        self._current_index = 0
        self._queue = []  # Coda di messaggi da mostrare
        self._typing_timer = QTimer(self)
        self._typing_timer.timeout.connect(self._type_next_char)
        self._is_typing = False
        self.setStyleSheet("font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;")

    def set_text_animated(self, text, speed=12):
        """Aggiunge il testo alla coda per l'animazione typewriter."""
        self._queue.append((text, speed))
        if not self._is_typing:
            self._start_next_message()

    def _start_next_message(self):
        """Avvia l'animazione del prossimo messaggio in coda."""
        if self._queue:
            self._target_text, speed = self._queue.pop(0)
            self._current_index = 0
            self._is_typing = True
            self._typing_timer.start(speed)
        else:
            self._is_typing = False

    def _type_next_char(self):
        if self._current_index < len(self._target_text):
            self._current_index += 1
            self.setText(self._target_text[:self._current_index])
        else:
            self._typing_timer.stop()
            self._is_typing = False
            # Se ci sono altri messaggi in coda, avvia il prossimo
            if self._queue:
                self._start_next_message()

    def set_text_instant(self, text):
        """Imposta il testo istantaneamente (per messaggi non più recenti)."""
        self._target_text = text
        self._current_index = len(text)
        self.setText(text)


class AnimatedBorderWidget(QWidget):
    """Widget che disegna un bordo illuminato animato."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._border_phase = 0.0
        self._glow_intensity = 0.0
        self._border_radius = 20
        self._border_width = 2

        # Colori del bordo
        self.color1 = QColor(52, 152, 219)    # Blu
        self.color2 = QColor(155, 89, 182)    # Viola
        self.color3 = QColor(46, 204, 113)    # Verde

        # Timer per l'animazione
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._animate)
        self.anim_timer.start(16)  # ~60 FPS

    def _animate(self):
        self._border_phase += 0.015  # Velocità rotazione
        if self._border_phase > 2 * math.pi:
            self._border_phase -= 2 * math.pi
        self._glow_intensity = 0.6 + 0.4 * math.sin(self._border_phase * 2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        r = self._border_radius

        # Calcola il perimetro totale approssimativo
        perimeter = 2 * (w + h - 4 * r) + 2 * math.pi * r

        # Posizione della "luce" che viaggia sul bordo (0-1)
        light_pos = (self._border_phase / (2 * math.pi))

        # Disegna il glow esterno
        self._draw_outer_glow(painter, w, h, r, light_pos)

        # Disegna il bordo principale con gradiente
        self._draw_animated_border(painter, w, h, r, light_pos)

        # Disegna highlight points
        self._draw_light_points(painter, w, h, r, light_pos)

    def _draw_outer_glow(self, painter, w, h, r, light_pos):
        """Disegna il glow esterno diffuso."""
        # Calcola la posizione della luce sul perimetro
        light_x, light_y = self._get_perimeter_point(w, h, r, light_pos)

        # Glow radiale nella posizione della luce
        glow_size = 120
        glow = QRadialGradient(light_x, light_y, glow_size)
        glow.setColorAt(0, QColor(52, 152, 219, int(80 * self._glow_intensity)))
        glow.setColorAt(0.3, QColor(155, 89, 182, int(40 * self._glow_intensity)))
        glow.setColorAt(1, QColor(52, 152, 219, 0))

        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(light_x), int(light_y)), glow_size, glow_size)

        # Secondo punto luce opposto
        light_x2, light_y2 = self._get_perimeter_point(w, h, r, (light_pos + 0.5) % 1.0)
        glow2 = QRadialGradient(light_x2, light_y2, glow_size * 0.7)
        glow2.setColorAt(0, QColor(155, 89, 182, int(50 * self._glow_intensity)))
        glow2.setColorAt(1, QColor(155, 89, 182, 0))
        painter.setBrush(QBrush(glow2))
        painter.drawEllipse(QPoint(int(light_x2), int(light_y2)), int(glow_size * 0.7), int(glow_size * 0.7))

    def _draw_animated_border(self, painter, w, h, r, light_pos):
        """Disegna il bordo con gradiente animato."""
        # Crea il path del bordo arrotondato
        border_path = QPainterPath()
        border_path.addRoundedRect(
            self._border_width / 2,
            self._border_width / 2,
            w - self._border_width,
            h - self._border_width,
            r, r
        )

        # Gradiente conico per il bordo (ruota)
        center_x, center_y = w / 2, h / 2
        gradient = QConicalGradient(center_x, center_y, -self._border_phase * 180 / math.pi)

        # Colori che sfumano lungo il bordo
        gradient.setColorAt(0.0, QColor(52, 152, 219, 200))
        gradient.setColorAt(0.15, QColor(52, 152, 219, 100))
        gradient.setColorAt(0.3, QColor(155, 89, 182, 60))
        gradient.setColorAt(0.5, QColor(155, 89, 182, 30))
        gradient.setColorAt(0.7, QColor(52, 152, 219, 60))
        gradient.setColorAt(0.85, QColor(52, 152, 219, 100))
        gradient.setColorAt(1.0, QColor(52, 152, 219, 200))

        pen = QPen(QBrush(gradient), self._border_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(border_path)

    def _draw_light_points(self, painter, w, h, r, light_pos):
        """Disegna punti luminosi che viaggiano sul bordo."""
        # Punto principale
        lx, ly = self._get_perimeter_point(w, h, r, light_pos)

        # Glow del punto
        point_glow = QRadialGradient(lx, ly, 25)
        point_glow.setColorAt(0, QColor(255, 255, 255, int(200 * self._glow_intensity)))
        point_glow.setColorAt(0.3, QColor(52, 152, 219, int(150 * self._glow_intensity)))
        point_glow.setColorAt(1, QColor(52, 152, 219, 0))
        painter.setBrush(QBrush(point_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(lx), int(ly)), 25, 25)

        # Punto centrale brillante
        painter.setBrush(QColor(255, 255, 255, int(255 * self._glow_intensity)))
        painter.drawEllipse(QPoint(int(lx), int(ly)), 3, 3)

        # Secondo punto più piccolo
        lx2, ly2 = self._get_perimeter_point(w, h, r, (light_pos + 0.5) % 1.0)
        point_glow2 = QRadialGradient(lx2, ly2, 15)
        point_glow2.setColorAt(0, QColor(155, 89, 182, int(150 * self._glow_intensity)))
        point_glow2.setColorAt(1, QColor(155, 89, 182, 0))
        painter.setBrush(QBrush(point_glow2))
        painter.drawEllipse(QPoint(int(lx2), int(ly2)), 15, 15)

    def _get_perimeter_point(self, w, h, r, t):
        """
        Calcola un punto sul perimetro del rettangolo arrotondato.
        t va da 0 a 1 rappresentando la posizione lungo il perimetro.
        """
        # Semplificazione: usa un'ellisse approssimata
        angle = t * 2 * math.pi

        # Centro
        cx, cy = w / 2, h / 2

        # Semi-assi
        a, b = (w / 2) - 5, (h / 2) - 5

        # Punto sull'ellisse
        x = cx + a * math.cos(angle)
        y = cy + b * math.sin(angle)

        return x, y


class PulsingWidget(QWidget):
    """Widget con effetto pulsante per il logo."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pulse_value = 1.0
        self._glow_opacity = 0.5
        self.pixmap = None

        # Animazione pulsante
        self.pulse_anim = QVariantAnimation(self)
        self.pulse_anim.setDuration(2000)
        self.pulse_anim.setStartValue(0.0)
        self.pulse_anim.setEndValue(2 * math.pi)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.valueChanged.connect(self._update_pulse)
        self.pulse_anim.start()

    def _update_pulse(self, value):
        self._pulse_value = 1.0 + 0.05 * math.sin(value)
        self._glow_opacity = 0.3 + 0.2 * math.sin(value)
        self.update()

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        if not self.pixmap:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        center_x = self.width() / 2
        center_y = self.height() / 2

        # Glow effect
        glow_size = 80
        glow_gradient = QRadialGradient(center_x, center_y, glow_size)
        glow_gradient.setColorAt(0, QColor(52, 152, 219, int(100 * self._glow_opacity)))
        glow_gradient.setColorAt(0.5, QColor(52, 152, 219, int(40 * self._glow_opacity)))
        glow_gradient.setColorAt(1, QColor(52, 152, 219, 0))
        painter.setBrush(QBrush(glow_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(center_x), int(center_y)), glow_size, glow_size)

        # Draw scaled pixmap
        scaled_size = int(64 * self._pulse_value)
        scaled_pixmap = self.pixmap.scaled(
            scaled_size, scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        x = int(center_x - scaled_pixmap.width() / 2)
        y = int(center_y - scaled_pixmap.height() / 2)
        painter.drawPixmap(x, y, scaled_pixmap)


class StartupDialog(QDialog):
    """Splash Screen spettacolare con animazioni moderne."""

    # Dimensioni della finestra
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 450

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Layout principale
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Container principale
        self.container = QFrame()
        self.container.setObjectName("MainContainer")

        # Background con particelle
        self.particle_bg = ParticleBackground(self.container)
        self.particle_bg.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.particle_bg.init_particles(70)

        # Bordo animato illuminato
        self.animated_border = AnimatedBorderWidget(self.container)
        self.animated_border.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Overlay per il contenuto
        self.content_overlay = QFrame(self.container)
        self.content_overlay.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.content_overlay.setStyleSheet("background: transparent;")

        # Shadow Effect sul container
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(52, 152, 219, 100))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        # Stile del container (bordo gestito da AnimatedBorderWidget)
        self.container.setStyleSheet("""
            #MainContainer {
                background-color: transparent;
                border-radius: 20px;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                background: transparent;
            }
        """)

        # Content layout
        content_layout = QVBoxLayout(self.content_overlay)
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setSpacing(20)

        # === HEADER ===
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)

        # Logo pulsante
        self.logo_widget = PulsingWidget()
        self.logo_widget.setFixedSize(90, 90)
        if os.path.exists("assets/app.ico"):
            pixmap = QIcon("assets/app.ico").pixmap(64, 64)
            self.logo_widget.set_pixmap(pixmap)
        header_layout.addWidget(self.logo_widget)

        # Title section
        title_container = QVBoxLayout()
        title_container.setSpacing(2)

        self.title_label = QLabel()
        self.title_label.setTextFormat(Qt.TextFormat.RichText)
        self.title_label.setText(
            '<span style="font-size: 38px; font-weight: 800; letter-spacing: 2px;">'
            'SYNCRO<span style="color: #3498db;">JOB</span>'
            '</span>'
        )

        from src.core.version import __version__
        self.version_label = QLabel(f"v{__version__}")
        self.version_label.setStyleSheet("""
            font-size: 13px;
            color: rgba(52, 152, 219, 0.9);
            font-weight: 600;
            letter-spacing: 3px;
        """)

        title_container.addWidget(self.title_label)
        title_container.addWidget(self.version_label)

        header_layout.addLayout(title_container)
        header_layout.addStretch()

        content_layout.addLayout(header_layout)
        content_layout.addSpacing(10)

        # === LOG CONSOLE ===
        self.log_frame = QFrame()
        self.log_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.4);
                border-radius: 12px;
                border: 1px solid rgba(52, 152, 219, 0.2);
            }
        """)

        log_layout = QVBoxLayout(self.log_frame)
        log_layout.setContentsMargins(20, 15, 20, 15)
        log_layout.setSpacing(6)

        # Header della console
        console_header = QLabel("SYSTEM INITIALIZATION")
        console_header.setStyleSheet("""
            font-size: 9px;
            color: rgba(52, 152, 219, 0.7);
            letter-spacing: 2px;
            font-weight: 600;
        """)
        log_layout.addWidget(console_header)

        # Separator
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background: rgba(52, 152, 219, 0.2);")
        log_layout.addWidget(separator)
        log_layout.addSpacing(5)

        # Log labels
        self.log_labels = []
        for i in range(5):
            lbl = AnimatedLogLabel()
            opacity = 0.25 + (i * 0.15)
            lbl.setStyleSheet(f"""
                font-size: 12px;
                color: rgba(255, 255, 255, {opacity});
                font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
                padding: 2px 0;
            """)
            log_layout.addWidget(lbl)
            self.log_labels.append(lbl)

        content_layout.addWidget(self.log_frame)

        # === PROGRESS BAR ===
        self.progress_bar = GlowingProgressBar()
        content_layout.addWidget(self.progress_bar)

        # === FOOTER ===
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 5, 0, 0)

        self.status_indicator = QLabel()
        self.status_indicator.setFixedSize(8, 8)
        self.status_indicator.setStyleSheet("""
            background-color: #3498db;
            border-radius: 4px;
        """)

        self.status_text = QLabel("INITIALIZING SYSTEM")
        self.status_text.setStyleSheet("""
            font-size: 11px;
            color: rgba(255, 255, 255, 0.5);
            font-weight: 600;
            letter-spacing: 2px;
        """)

        # Animated dots
        self.dots_label = QLabel("")
        self.dots_label.setStyleSheet("""
            font-size: 11px;
            color: rgba(52, 152, 219, 0.8);
            font-weight: 600;
        """)
        self.dots_count = 0
        self.dots_timer = QTimer(self)
        self.dots_timer.timeout.connect(self._animate_dots)
        self.dots_timer.start(400)

        footer_layout.addWidget(self.status_indicator)
        footer_layout.addSpacing(8)
        footer_layout.addWidget(self.status_text)
        footer_layout.addWidget(self.dots_label)
        footer_layout.addStretch()

        content_layout.addLayout(footer_layout)

        self.main_layout.addWidget(self.container)

        # Status pulse animation
        self._setup_status_pulse()

        # Variabili di stato
        self.current_logs = []

        # === ANIMAZIONI DI INGRESSO ===
        self._setup_entrance_animations()

    def _setup_status_pulse(self):
        """Configura l'animazione pulsante per l'indicatore di stato."""
        self.status_pulse_timer = QTimer(self)
        self.status_pulse_timer.timeout.connect(self._pulse_status)
        self.status_pulse_timer.start(1000)
        self.pulse_state = True

    def _pulse_status(self):
        self.pulse_state = not self.pulse_state
        if self.pulse_state:
            self.status_indicator.setStyleSheet("""
                background-color: #3498db;
                border-radius: 4px;
            """)
        else:
            self.status_indicator.setStyleSheet("""
                background-color: rgba(52, 152, 219, 0.5);
                border-radius: 4px;
            """)

    def _animate_dots(self):
        self.dots_count = (self.dots_count + 1) % 4
        self.dots_label.setText("." * self.dots_count)

    def _setup_entrance_animations(self):
        """Configura le animazioni di ingresso spettacolari."""
        # Fade in principale
        self.setWindowOpacity(0.0)

        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Inizialmente nascondi alcuni elementi
        self.log_frame.setStyleSheet(self.log_frame.styleSheet() + "opacity: 0;")

        # Avvia l'animazione
        self.fade_anim.start()

    def update_status(self, message: str, progress: int):
        """Aggiorna lo stato con animazioni fluide."""
        # Footer status
        self.status_text.setText(message.upper())

        # Update status indicator color based on progress
        if progress >= 90:
            color = "#2ecc71"  # Green
        elif progress >= 50:
            color = "#3498db"  # Blue
        else:
            color = "#f39c12"  # Orange

        self.status_indicator.setStyleSheet(f"""
            background-color: {color};
            border-radius: 4px;
        """)

        # Log Rolling con animazione
        timestamp_prefix = ">"
        log_entry = f"{timestamp_prefix} {message}"
        self.current_logs.append(log_entry)
        if len(self.current_logs) > 5:
            self.current_logs.pop(0)

        # Update labels con effetto fade
        for i in range(5):
            if i < len(self.current_logs):
                is_latest = (i == len(self.current_logs) - 1)
                opacity = 1.0 if is_latest else 0.3 + (i * 0.1)

                self.log_labels[i].setStyleSheet(f"""
                    font-size: 12px;
                    color: rgba(255, 255, 255, {opacity});
                    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
                    padding: 2px 0;
                """)

                if is_latest:
                    # Effetto typewriter fluido per l'ultimo log
                    self.log_labels[i].set_text_animated(self.current_logs[i], speed=6)
                else:
                    # Testo istantaneo per messaggi precedenti
                    self.log_labels[i].set_text_instant(self.current_logs[i])
            else:
                self.log_labels[i].set_text_instant("")

        # Update progress bar
        self.progress_bar.setValue(progress)

        QApplication.processEvents()

    def closeEvent(self, event):
        """Cleanup quando si chiude."""
        self.particle_bg.timer.stop()
        self.animated_border.anim_timer.stop()
        self.dots_timer.stop()
        self.status_pulse_timer.stop()
        super().closeEvent(event)
