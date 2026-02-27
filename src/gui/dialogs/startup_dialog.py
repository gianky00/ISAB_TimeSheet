"""
SyncroJob - Splash Screen
Gestisce l'inizializzazione dell'applicazione con animazioni fluide.
"""

import logging
from contextlib import suppress
from pathlib import Path

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    QTimer,
)
from PyQt6.QtGui import (
    QColor,
    QIcon,
)
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from src.gui.styles import COLORS

# Import widget specializzati
from src.gui.widgets.startup.particle_background import ParticleBackground
from src.gui.widgets.startup.startup_widgets import (
    AnimatedBorder,
    GlowingProgressBar,
    PulsingLogo,
    TypewriterLabel,
)

logger = logging.getLogger(__name__)


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
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
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
        self.container.setStyleSheet("#Container { background: transparent; border: none; }")

        # Particle background (Estratto)
        self.particles = ParticleBackground(self.container)
        self.particles.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.particles.init_particles(70)

        # Animated border (Estratto)
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
        c = QColor(COLORS["primary_blue"])
        shadow.setColor(QColor(c.red(), c.green(), c.blue(), 120))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        layout.addWidget(self.container)

    def _setup_content(self):
        """Configura il contenuto principale (header, console, progress, footer)."""
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(30, 45, 30, 45)  # Ridotti margini laterali per logs
        content_layout.setSpacing(20)

        self._setup_header(content_layout)
        self._setup_console(content_layout)
        self._setup_progress(content_layout)
        self._setup_footer(content_layout)

    def _setup_header(self, parent_layout: QVBoxLayout):
        """Configura l'header con logo, titolo e info licenza."""
        header = QHBoxLayout()
        header.setSpacing(20)

        # Logo pulsante (Estratto)
        from src.utils.helpers import get_asset_path

        icon_path = get_asset_path("assets/app.ico")

        self.logo = PulsingLogo()
        self.logo.setFixedSize(85, 85)
        if Path(icon_path).exists():
            self.logo.set_pixmap(QIcon(icon_path).pixmap(64, 64))
        header.addWidget(self.logo)

        # Titolo e versione
        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        self.title = QLabel()
        self.title.setTextFormat(Qt.TextFormat.RichText)
        self.title.setText(
            f'<span style="font-size:40px; font-weight:800; color:{COLORS["bg_white"]}; letter-spacing:2px;">'
            f'SYNCRO<span style="color:{COLORS["primary_blue"]};">JOB</span></span>'
        )
        title_box.addWidget(self.title)

        from src.core.version import __version__

        self.version = QLabel(f"v{__version__}")
        self.version.setStyleSheet(
            f"font-size:13px; color:{COLORS['primary_blue']}; opacity: 0.9; font-weight:600; letter-spacing:3px;"
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
        license_box.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

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
        lbl.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 10px; font-weight: 600;")

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
        c = QColor(COLORS["primary_blue"])
        self.log_frame.setStyleSheet(
            f"background:rgba(0,0,0,0.35); border-radius:16px; border:1px solid rgba({c.red()},{c.green()},{c.blue()},0.2);"
        )
        log_layout = QVBoxLayout(self.log_frame)
        log_layout.setContentsMargins(10, 10, 10, 10)  # Margini ridotti
        log_layout.setSpacing(2)

        log_header = QLabel("INIZIALIZZAZIONE SISTEMA")
        log_header.setStyleSheet(
            f"font-size:9px; color:rgba({c.red()},{c.green()},{c.blue()},0.6); letter-spacing:2px; font-weight:600;"
        )
        log_layout.addWidget(log_header)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background:rgba({c.red()},{c.green()},{c.blue()},0.15);")
        log_layout.addWidget(sep)

        self.log_labels = []
        for i in range(5):
            lbl = TypewriterLabel()  # Estratto
            lbl.setWordWrap(False)  # Disabilita a capo automatico per singola riga
            lbl.setStyleSheet(
                f"font-size:10px; color:rgba(255,255,255,{0.2 + i * 0.15}); "
                f"font-family:'Consolas','Fira Code',monospace; padding:1px 0;"
            )
            log_layout.addWidget(lbl)
            self.log_labels.append(lbl)

        parent_layout.addWidget(self.log_frame)

    def _setup_progress(self, parent_layout: QVBoxLayout):
        """Configura la barra di progresso."""
        self.progress = GlowingProgressBar()  # Estratto
        parent_layout.addWidget(self.progress)

    def _setup_footer(self, parent_layout: QVBoxLayout):
        """Configura il footer con indicatore, status."""
        footer = QHBoxLayout()
        footer.setContentsMargins(0, 5, 0, 0)

        # Indicatore di stato
        self.indicator = QLabel()
        self.indicator.setFixedSize(8, 8)
        self.indicator.setStyleSheet(f"background:{COLORS['primary_blue']}; border-radius:4px;")
        footer.addWidget(self.indicator)
        footer.addSpacing(8)

        # Label status
        self.status = QLabel("AVVIO IN CORSO...")
        self.status.setStyleSheet(
            f"font-size:11px; color:{COLORS['bg_white']}; opacity: 0.5; font-weight:600; letter-spacing:2px;"
        )
        footer.addWidget(self.status)

        self.dots = QLabel("")
        self.dots.setStyleSheet(
            f"font-size:11px; color:{COLORS['primary_blue']}; opacity: 0.8; font-weight:600;"
        )
        footer.addWidget(self.dots)

        footer.addStretch()

        # Rimosso Resource Monitor

        parent_layout.addLayout(footer)

    def _setup_animations(self):
        """Configura i timer per le animazioni (dots, pulse, fade-in)."""
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

    def mousePressEvent(self, event):
        """Inizia il drag della finestra tramite mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Gestisce il trascinamento della finestra e l'effetto parallasse sulle particelle."""
        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_pos:
            new_pos = event.globalPosition().toPoint() - self._drag_pos
            dx = new_pos.x() - self.pos().x()
            dy = new_pos.y() - self.pos().y()
            self.move(new_pos)
            self.particles.apply_parallax(dx, dy)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Interrompe il drag della finestra."""
        self._drag_pos = None

    def _animate_dots(self):
        self._dot_count = (self._dot_count + 1) % 4
        self.dots.setText("." * self._dot_count)

    def _pulse_indicator(self):
        self._pulse_state = not self._pulse_state
        c = QColor(COLORS["primary_blue"])
        color = COLORS["primary_blue"] if self._pulse_state else f"rgba({c.red()},{c.green()},{c.blue()},0.4)"
        self.indicator.setStyleSheet(f"background:{color}; border-radius:4px;")

    def _on_progress(self, message: str, prog: int):
        """Aggiorna UI - chiamato dal thread principale via signal."""
        self.status.setText(message.upper())

        if prog >= 90:
            self.indicator.setStyleSheet(f"background:{COLORS['success_green']}; border-radius:4px;")
        elif prog >= 50:
            self.indicator.setStyleSheet(f"background:{COLORS['primary_blue']}; border-radius:4px;")
        else:
            self.indicator.setStyleSheet(f"background:{COLORS['warning_orange']}; border-radius:4px;")

        entry = f"> {message}"
        self.current_logs.append(entry)
        if len(self.current_logs) > 5:
            self.current_logs.pop(0)

        for i in range(5):
            if i < len(self.current_logs):
                is_last = i == len(self.current_logs) - 1
                opacity = 1.0 if is_last else 0.25 + i * 0.12
                self.log_labels[i].setStyleSheet(
                    f"font-size:10px; color:rgba(255,255,255,{opacity}); "
                    f"font-family:'Consolas','Fira Code',monospace; padding:1px 0;"
                )
                if is_last:
                    self.log_labels[i].set_text_animated(self.current_logs[i], speed=18)
                else:
                    self.log_labels[i].set_text_instant(self.current_logs[i])
            else:
                self.log_labels[i].set_text_instant("")

        self.progress.setValue(prog)

    def _on_finished(self, success: bool):
        self._init_result = success
        if self._thread:
            self._thread.quit()
            self._thread.wait(500)
        QTimer.singleShot(400, self.accept)

    def get_result(self) -> bool:
        """Restituisce il risultato dell'inizializzazione dell'app."""
        return self._init_result

    def update_status(self, message: str, progress: int):
        """Metodo pubblico per aggiornare lo stato di caricamento dal worker."""
        self._on_progress(message, progress)

    def closeEvent(self, event):
        """Cleanup - Stop all timers and threads safely."""
        with suppress(Exception):
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
