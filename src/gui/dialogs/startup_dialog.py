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
    QRadialGradient, QPen, QBrush, QFont
)
import os
import random
import math

class Particle:
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
        if self.y < -10: self.y = self.height + 10
        if self.x < -10: self.x = self.width + 10
        elif self.x > self.width + 10: self.x = -10

    def get_opacity(self):
        return self.opacity * (0.5 + 0.5 * math.sin(self.pulse_phase))

class ParticleBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.particles = []
        self.glow_phase = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(16)

    def init_particles(self, count=50):
        self.particles = [Particle(self.width(), self.height()) for _ in range(count)]

    def _animate(self):
        self.glow_phase += 0.02
        for p in self.particles: p.update()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(8, 8, 15))
        gradient.setColorAt(1, QColor(5, 5, 10))
        painter.fillRect(self.rect(), gradient)
        for p in self.particles:
            color = QColor(52, 152, 219)
            color.setAlphaF(p.get_opacity())
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(int(p.x), int(p.y)), int(p.size), int(p.size))

class GlowingProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self.setFixedHeight(4)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update)
        self.anim_timer.start(16)

    def setValue(self, val):
        self._value = val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(20, 20, 30))
        if self._value > 0:
            w = int((self._value / 100) * self.width())
            grad = QLinearGradient(0, 0, w, 0)
            grad.setColorAt(0, QColor(52, 152, 219))
            grad.setColorAt(1, QColor(155, 89, 182))
            painter.fillRect(0, 0, w, self.height(), grad)

class StartupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(600, 400)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.container = QFrame()
        
        self.particle_bg = ParticleBackground(self.container)
        self.particle_bg.setGeometry(0, 0, 600, 400)
        self.particle_bg.init_particles(60)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(52, 152, 219, 80))
        self.container.setGraphicsEffect(shadow)
        self.container.setStyleSheet("#MainContainer { background: transparent; border-radius: 20px; }")

        content_layout = QVBoxLayout(self.container)
        content_layout.setContentsMargins(50, 50, 50, 50)

        # Header
        header = QHBoxLayout()
        self.logo = QLabel()
        if os.path.exists("assets/app.ico"):
            self.logo.setPixmap(QIcon("assets/app.ico").pixmap(64, 64))
        header.addWidget(self.logo)
        
        title_vbox = QVBoxLayout()
        self.title = QLabel('SYNCRO<span style="color:#3498db;">JOB</span>')
        self.title.setStyleSheet("font-size: 36px; font-weight: 800; color: white;")
        from src.core.version import __version__
        self.ver = QLabel(f"VERSION {__version__}")
        self.ver.setStyleSheet("font-size: 12px; color: rgba(52, 152, 219, 0.8); font-weight: bold; letter-spacing: 2px;")
        title_vbox.addWidget(self.title)
        title_vbox.addWidget(self.ver)
        header.addLayout(title_vbox)
        header.addStretch()
        content_layout.addLayout(header)
        content_layout.addSpacing(20)

        # Log Area
        self.log_frame = QFrame()
        self.log_frame.setStyleSheet("background: rgba(0,0,0,0.3); border: 1px solid rgba(52,152,219,0.1); border-radius: 10px;")
        log_layout = QVBoxLayout(self.log_frame)
        self.log_labels = []
        for i in range(5):
            lbl = QLabel("")
            lbl.setStyleSheet(f"font-size: 11px; color: rgba(255,255,255,{0.2+(i*0.2)}); font-family: 'Consolas';")
            log_layout.addWidget(lbl)
            self.log_labels.append(lbl)
        content_layout.addWidget(self.log_frame)

        # Progress
        self.progress_bar = GlowingProgressBar()
        content_layout.addWidget(self.progress_bar)
        
        self.status_text = QLabel("INITIALIZING...")
        self.status_text.setStyleSheet("font-size: 9px; color: #555; font-weight: bold; letter-spacing: 1px;")
        content_layout.addWidget(self.status_text)

        self.main_layout.addWidget(self.container)
        self.current_logs = []
        
        self.setWindowOpacity(0.0)
        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(500)
        self.fade.setStartValue(0.0)
        self.fade.setEndValue(1.0)
        self.fade.start()

    def update_status(self, message: str, progress: int):
        self.status_text.setText(message.upper())
        self.current_logs.append(f"> {message}")
        if len(self.current_logs) > 5: self.current_logs.pop(0)
        for i in range(5):
            if i < len(self.current_logs):
                self.log_labels[i].setText(self.current_logs[i])
                opacity = 0.3 if i < len(self.current_logs) - 1 else 1.0
                self.log_labels[i].setStyleSheet(f"color: rgba(255,255,255,{opacity});")
        self.progress_bar.setValue(progress)
        QApplication.processEvents()
