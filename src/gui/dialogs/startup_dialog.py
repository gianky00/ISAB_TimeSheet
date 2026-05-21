"""
SyncroJob - Splash Screen
Gestisce l'inizializzazione dell'applicazione con animazioni fluide e effetti 3D.
"""

import logging
from contextlib import suppress
from pathlib import Path
from typing import Any

from PySide6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    Qt,
    QThread,
    QTimer,
    Slot,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
    QMouseEvent,
)
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

# Rimossa dipendenza sincrona a get_hardware_id e get_license_info per reattività all'avvio
from src.core.version import __version__
from src.gui.styles import COLORS

# Import widget specializzati
from src.gui.widgets.startup.particle_background import ParticleBackground
from src.gui.widgets.startup.startup_widgets import (
    AnimatedBorder,
    ChangelogTicker,
    ConsoleOverlay,
    GlowingProgressBar,
    PulsingLogo,
    TechBlueprint,
    TypewriterLabel,
)
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class StartupDialog(QDialog):
    """Splash screen con animazioni fluide a 60fps e effetti 3D."""

    # Dimensioni del contenuto visibile (Innalzate proporzionalmente)
    CONTENT_WIDTH = 850
    CONTENT_HEIGHT = 560
    # Margine per l'ombra
    SHADOW_MARGIN = 50

    _thread: QThread | None
    _worker: Any
    _drag_pos: QPoint | None

    def __init__(self) -> None:
        super().__init__()
        self.setMouseTracking(True)  # Fondamentale per il Tilt 3D
        self._init_window()
        self._init_state()
        self._setup_container()
        self._setup_content()
        self._setup_animations()

    def _init_window(self) -> None:
        """Configura le proprietà base della finestra."""
        self.setObjectName("StartupDialog")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        # Dimensione totale = Contenuto + Margini per l'ombra
        total_w = self.CONTENT_WIDTH + (self.SHADOW_MARGIN * 2)
        total_h = self.CONTENT_HEIGHT + (self.SHADOW_MARGIN * 2)
        self.setFixedSize(total_w, total_h)
        self.setStyleSheet("background: transparent; border: none;")

    def _init_state(self) -> None:
        """Inizializza lo stato interno del dialog."""
        self._worker = None
        self._thread = None
        self._init_result = False
        self.current_logs: list[str] = []
        self._drag_pos = None
        self._tilt_x = 0.0
        self._tilt_y = 0.0

    def _setup_container(self) -> None:
        """Configura il container principale con particelle, bordo e shadow."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            self.SHADOW_MARGIN, self.SHADOW_MARGIN, self.SHADOW_MARGIN, self.SHADOW_MARGIN
        )

        self.container = QFrame()
        self.container.setObjectName("Container")
        self.container.setFixedSize(self.CONTENT_WIDTH, self.CONTENT_HEIGHT)
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.container.setStyleSheet("#Container { background: transparent; border: none; }")

        # Particle background
        self.particles = ParticleBackground(self.container)
        self.particles.setGeometry(0, 0, self.CONTENT_WIDTH, self.CONTENT_HEIGHT)
        num_particles = 70
        self.particles.init_particles(num_particles)

        # Animated border
        self.border = AnimatedBorder(self.container)
        self.border.setGeometry(0, 0, self.CONTENT_WIDTH, self.CONTENT_HEIGHT)

        # Content overlay
        self.content = QFrame(self.container)
        self.content.setGeometry(0, 0, self.CONTENT_WIDTH, self.CONTENT_HEIGHT)
        self.content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.content.setStyleSheet("background: transparent; border: none;")

        # Shadow luminosa esterna
        shadow = QGraphicsDropShadowEffect()
        blur_radius = 60
        shadow.setBlurRadius(blur_radius)
        c = QColor(COLORS["primary_blue"])
        shadow_opacity = 100
        shadow.setColor(QColor(c.red(), c.green(), c.blue(), shadow_opacity))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        layout.addWidget(self.container)

    def _setup_content(self) -> None:
        """Configura il contenuto principale (header, console, progress, footer)."""
        content_layout = QVBoxLayout(self.content)
        layout_margin_side = 30
        layout_margin_v = 45
        content_layout.setContentsMargins(
            layout_margin_side, layout_margin_v, layout_margin_side, layout_margin_v
        )
        layout_spacing = 20
        content_layout.setSpacing(layout_spacing)

        self._setup_header(content_layout)
        self._setup_console(content_layout)
        self._setup_progress(content_layout)
        self._setup_footer(content_layout)

    def _setup_header(self, parent_layout: QVBoxLayout) -> None:
        """Configura l'header con logo, blueprint e titoli."""
        header_container = QFrame()
        header_height = 100
        header_container.setFixedHeight(header_height)
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_spacing = 20
        header_layout.setSpacing(header_spacing)

        # Blueprint olografico (dietro il logo)
        self.blueprint = TechBlueprint(header_container)
        blueprint_size = 100
        self.blueprint.setFixedSize(blueprint_size, blueprint_size)
        blueprint_offset = -8
        self.blueprint.move(blueprint_offset, blueprint_offset)  # Centratura rispetto al logo

        icon_path = get_asset_path("assets/app.ico")

        self.logo = PulsingLogo(header_container)
        logo_size = 85
        self.logo.setFixedSize(logo_size, logo_size)
        if Path(icon_path).exists():
            icon_px = 64
            self.logo.set_pixmap(QIcon(icon_path).pixmap(icon_px, icon_px))
        header_layout.addWidget(self.logo)

        title_box = QVBoxLayout()
        title_spacing = 4
        title_box.setSpacing(title_spacing)
        self.title = QLabel()
        self.title.setTextFormat(Qt.TextFormat.RichText)
        self.title.setText(
            f'<span style="font-size:40px; font-weight:900; color:{COLORS["bg_white"]}; letter-spacing:2px;">'
            f'SYNCRO<span style="color:{COLORS["primary_blue"]};">JOB</span></span>'
        )
        # Effetto ombra per il titolo per farlo risaltare
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(15)
        title_shadow.setColor(QColor(0, 0, 0, 200))
        title_shadow.setOffset(2, 2)
        self.title.setGraphicsEffect(title_shadow)
        title_box.addWidget(self.title)

        self.version = QLabel(f"v{__version__}")
        self.version.setStyleSheet(
            f"font-size:13px; color:{COLORS['primary_blue']}; opacity: 0.9; font-weight:600; letter-spacing:3px;"
        )
        title_box.addWidget(self.version)
        header_layout.addLayout(title_box)
        header_layout.addStretch()

        self._setup_license_info(header_layout)
        parent_layout.addWidget(header_container)

    def _setup_license_info(self, parent_layout: QHBoxLayout) -> None:
        """Configura il box con le informazioni della licenza in modo asincrono (placeholder iniziali)."""
        license_box = QVBoxLayout()
        license_spacing = 2
        license_box.setSpacing(license_spacing)
        license_box.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        lay_c, self.lbl_val_cliente = self._create_info_row("CLIENTE:", "ATTESA...")
        lay_h, self.lbl_val_hwid = self._create_info_row("HW-ID:", "ATTESA...")
        lay_s, self.lbl_val_scadenza = self._create_info_row("SCADENZA:", "ATTESA...")

        license_box.addLayout(lay_c)
        license_box.addLayout(lay_h)
        license_box.addLayout(lay_s)

        parent_layout.addLayout(license_box)

    @Slot(str, str, str)
    def update_license_display(self, cliente: str, hw_id: str, scadenza: str) -> None:
        """Aggiorna le informazioni di licenza visualizzate (chiamato asincronamente)."""
        if hasattr(self, "lbl_val_cliente") and self.lbl_val_cliente:
            self.lbl_val_cliente.setText(cliente.upper())
        if hasattr(self, "lbl_val_hwid") and self.lbl_val_hwid:
            self.lbl_val_hwid.setText(hw_id)
        if hasattr(self, "lbl_val_scadenza") and self.lbl_val_scadenza:
            self.lbl_val_scadenza.setText(scadenza)

    def _create_info_row(self, label_text: str, value_text: str) -> tuple[QHBoxLayout, QLabel]:
        """Crea una riga di informazione label: valore e restituisce il layout e la label del valore."""
        row = QHBoxLayout()
        row_spacing = 5
        row.setSpacing(row_spacing)
        row.setAlignment(Qt.AlignmentFlag.AlignRight)

        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 10px; font-weight: 600;")

        val = QLabel(value_text)
        val.setStyleSheet(
            "color: rgba(255, 255, 255, 0.9); font-size: 10px; font-weight: bold; font-family: 'Consolas', monospace;"
        )

        row.addWidget(lbl)
        row.addWidget(val)
        return row, val

    def _setup_console(self, parent_layout: QVBoxLayout) -> None:
        """Configura la console di log con TypewriterLabels e overlay CRT."""
        self.log_frame = QFrame()
        self.log_frame.setObjectName("LogConsole")
        c = QColor(COLORS["primary_blue"])
        log_border_opacity = 0.4
        self.log_frame.setStyleSheet(
            f"#LogConsole {{ "
            f"  background: rgba(0, 0, 0, 0.6); "
            f"  border-radius: 16px; "
            f"  border: 1px solid rgba({c.red()}, {c.green()}, {c.blue()}, {log_border_opacity}); "
            f"}}"
        )
        log_layout = QVBoxLayout(self.log_frame)
        log_layout.setContentsMargins(20, 15, 20, 15)
        log_layout.setSpacing(6)

        log_header = QLabel("[ DIAGNOSTICA DI SISTEMA ]")
        header_letter_spacing = 2
        log_header.setStyleSheet(
            f"font-size: 11px; "
            f"color: {COLORS['primary_blue']}; "
            f"letter-spacing: {header_letter_spacing}px; "
            f"font-weight: 900;"
        )
        log_layout.addWidget(log_header)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep_opacity = 0.3
        sep.setStyleSheet(f"background:rgba({c.red()},{c.green()},{c.blue()},{sep_opacity});")
        log_layout.addWidget(sep)

        self.log_labels = []
        max_log_lines = 5
        for _i in range(max_log_lines):
            lbl = TypewriterLabel()
            lbl.setWordWrap(False)
            lbl.setTextFormat(Qt.TextFormat.RichText)
            lbl.setStyleSheet("font-size:10px; font-family:'Consolas','Fira Code',monospace; padding:1px 0;")
            log_layout.addWidget(lbl)
            self.log_labels.append(lbl)

        # Overlay CRT (Scanlines + Grid)
        self.console_overlay = ConsoleOverlay(self.log_frame)
        parent_layout.addWidget(self.log_frame)

    def _setup_progress(self, parent_layout: QVBoxLayout) -> None:
        """Configura la barra di progresso."""
        self.progress = GlowingProgressBar()
        parent_layout.addWidget(self.progress)

    def _load_current_changelog_notes(self) -> list[str]:
        """Carica le note di changelog per la versione corrente dell'applicazione."""
        try:
            import json

            changelog_path = Path(__file__).resolve().parent.parent.parent / "core" / "changelog.json"
            if changelog_path.exists():
                with open(changelog_path, encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for entry in data:
                            if entry.get("version") == __version__:
                                return list(entry.get("notes", []))
                        # Se non trova la versione esatta, restituisce le note dell'ultima versione disponibile
                        if data:
                            return list(data[0].get("notes", []))
        except Exception:
            logger.exception("Errore nel caricamento del changelog nello splash screen")
        return []

    def _setup_footer(self, parent_layout: QVBoxLayout) -> None:
        """Configura la riga dello status di caricamento."""
        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 5, 0, 0)

        self.indicator = QLabel()
        indicator_size = 8
        self.indicator.setFixedSize(indicator_size, indicator_size)
        self.indicator.setStyleSheet(f"background:{COLORS['primary_blue']}; border-radius:4px;")
        status_row.addWidget(self.indicator)
        status_row.addSpacing(8)

        self.status = QLabel("AVVIO IN CORSO...")
        self.status.setStyleSheet(
            f"font-size:11px; color:{COLORS['bg_white']}; opacity: 0.5; font-weight:600; letter-spacing:2px;"
        )
        status_row.addWidget(self.status)

        self.dots = QLabel("")
        self.dots.setStyleSheet(
            f"font-size:11px; color:{COLORS['primary_blue']}; opacity: 0.8; font-weight:600;"
        )
        status_row.addWidget(self.dots)
        status_row.addStretch()

        parent_layout.addLayout(status_row)

        # Riga dedicata per il Ticker Novità (Sotto lo Status)
        self._setup_ticker_row(parent_layout)

    def _setup_ticker_row(self, parent_layout: QVBoxLayout) -> None:
        """Posiziona il ticker del changelog multi-riga centrato in basso."""
        ticker_layout = QHBoxLayout()
        # Riduciamo il margine superiore per far stare comodamente 3 righe
        ticker_layout.setContentsMargins(0, 5, 0, 0)

        self.ticker = ChangelogTicker()
        notes = self._load_current_changelog_notes()
        self.ticker.set_notes(notes)

        ticker_layout.addStretch(1)
        ticker_layout.addWidget(self.ticker, alignment=Qt.AlignmentFlag.AlignCenter)
        ticker_layout.addStretch(1)

        parent_layout.addLayout(ticker_layout)

    def _setup_animations(self) -> None:
        """Configura i timer per le animazioni (dots, pulse, fade-in)."""
        self._dot_count = 0
        self._dot_timer = QTimer(self)
        self._dot_timer.timeout.connect(self._animate_dots)
        dot_interval_ms = 350
        self._dot_timer.start(dot_interval_ms)

        self._pulse_state = True
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._pulse_indicator)
        pulse_interval_ms = 800
        self._pulse_timer.start(pulse_interval_ms)

        # Fade in
        self.setWindowOpacity(0.0)
        self._fade = QPropertyAnimation(self, b"windowOpacity")
        fade_duration_ms = 600
        self._fade.setDuration(fade_duration_ms)
        self._fade.setStartValue(0.0)
        self._fade.setEndValue(1.0)
        self._fade.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade.start()

    def resizeEvent(self, event: Any) -> None:
        """Gestisce il ridimensionamento dell'overlay della console."""
        super().resizeEvent(event)
        if hasattr(self, "console_overlay"):
            self.console_overlay.setGeometry(self.log_frame.rect())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Inizia il drag della finestra tramite mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Gestisce il trascinamento e l'effetto 3D Tilt."""
        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_pos:
            new_pos = event.globalPosition().toPoint() - self._drag_pos
            dx = new_pos.x() - self.pos().x()
            dy = new_pos.y() - self.pos().y()
            self.move(new_pos)
            self.particles.apply_parallax(dx, dy)
            event.accept()
        else:
            # Effetto 3D Tilt basato sulla posizione del mouse
            pos = event.position()
            rel_x = (pos.x() - self.width() / 2) / (self.width() / 2)
            rel_y = (pos.y() - self.height() / 2) / (self.height() / 2)

            # Inclinazione massima 3 gradi
            self._tilt_x = rel_y * 3.0
            self._tilt_y = -rel_x * 3.0
            # Sostituiamo apply_tilt con parallasse soft per performance e compatibilità shadow
            parallax_factor = 5
            self.particles.apply_parallax(rel_x * parallax_factor, rel_y * parallax_factor)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Interrompe il drag della finestra."""
        self._drag_pos = None

    def _animate_dots(self) -> None:
        max_dots = 4
        self._dot_count = (self._dot_count + 1) % max_dots
        self.dots.setText("." * self._dot_count)

    def _pulse_indicator(self) -> None:
        self._pulse_state = not self._pulse_state
        c = QColor(COLORS["primary_blue"])
        color = COLORS["primary_blue"] if self._pulse_state else f"rgba({c.red()},{c.green()},{c.blue()},0.4)"
        self.indicator.setStyleSheet(f"background:{color}; border-radius:4px;")

    def _on_progress(self, message: str, prog: int) -> None:
        """Aggiorna UI e particelle per convergenza."""
        full_entry = f"> {message}"
        self.status.setText(message.upper())
        self.particles.set_progress(prog)  # Sincronizza convergenza particelle

        threshold_success = 90
        threshold_blue = 50

        if prog >= threshold_success:
            self.indicator.setStyleSheet(f"background:{COLORS['success_green']}; border-radius:4px;")
        elif prog >= threshold_blue:
            self.indicator.setStyleSheet(f"background:{COLORS['primary_blue']}; border-radius:4px;")
        else:
            self.indicator.setStyleSheet(f"background:{COLORS['warning_orange']}; border-radius:4px;")

        self.current_logs.append(full_entry)
        max_log_history = 5
        if len(self.current_logs) > max_log_history:
            self.current_logs.pop(0)

        for i in range(max_log_history):
            if i < len(self.current_logs):
                is_last = i == len(self.current_logs) - 1
                opacity = 1.0 if is_last else 0.2 + i * 0.15

                self.log_labels[i].setStyleSheet(
                    f"font-size:10px; font-family:'Consolas',monospace; color:white; opacity:{opacity};"
                )

                if is_last:
                    anim_speed = 15
                    self.log_labels[i].set_text_animated(self.current_logs[i], speed=anim_speed)
                else:
                    self.log_labels[i].set_text_instant(self.current_logs[i])
            else:
                self.log_labels[i].set_text_instant("")

        self.progress.setValue(prog)

    def _on_finished(self, success: bool) -> None:
        self._init_result = success
        if self._thread:
            self._thread.quit()
            thread_wait_ms = 500
            self._thread.wait(thread_wait_ms)
        close_delay_ms = 400
        QTimer.singleShot(close_delay_ms, self.accept)

    def get_result(self) -> bool:
        """Restituisce il risultato dell'inizializzazione dell'app."""
        return self._init_result

    def update_status(self, message: str, progress: int) -> None:
        """Metodo pubblico per aggiornare lo stato di caricamento dal worker."""
        self._on_progress(message, progress)

    def closeEvent(self, event: Any) -> None:
        """Cleanup - Stop all timers and threads safely."""
        with suppress(Exception):
            self.particles.timer.stop()
            self.border.timer.stop()
            self.progress.timer.stop()
            self._dot_timer.stop()
            self._pulse_timer.stop()
            if hasattr(self, "ticker"):
                self.ticker.cycle_timer.stop()
                if hasattr(self.ticker, "fade_anim"):
                    self.ticker.fade_anim.stop()
            for lbl in self.log_labels:
                lbl._timer.stop()
            if self._thread and self._thread.isRunning():
                self._thread.quit()
                thread_wait_ms = 500
                self._thread.wait(thread_wait_ms)
        super().closeEvent(event)
