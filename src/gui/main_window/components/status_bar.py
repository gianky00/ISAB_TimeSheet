"""
SyncroJob - Status Bar Component
Gestore della barra di stato principale che coordina telemetria, info licenza e stato bot.
Gestisce le transizioni visive tra la fase di avvio e quella operativa dell'applicazione.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from PySide6.QtCore import QEasingCurve, QObject, QPropertyAnimation, QSize, Qt, QTimer
from PySide6.QtWidgets import QGraphicsOpacityEffect, QStatusBar

from src.core import config_manager
from src.core.constants import Icons
from src.core.license_validator import get_license_info
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    IconButton,
)
from src.gui.widgets.footer import (
    BootTelemetryWidget,
    FooterLeftWidget,
    FooterRightWidget,
    StartupConsole,
)
from src.gui.widgets.status_card import StatusCard
from src.utils.helpers import get_asset_path, get_colored_icon

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow


class StatusBarComponent(QObject):
    """
    Componente responsabile della gestione della QStatusBar.
    Organizza i widget del footer in zone (Sinistra: Info/Telemetria, Centro: Console, Destra: Stati Bot).
    Implementa logica di aggiornamento per licenza e countdown Autopilot.
    """

    def __init__(self, main_window: MainWindow) -> None:
        """
        Inizializza il componente della barra di stato.

        Args:
          main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.main_window = main_window
        self._footer_stats_mode = False

        # Animations
        self._console_anim: QPropertyAnimation | None = None
        self._telemetry_anim: QPropertyAnimation | None = None

        # UI Attributes
        self.status_bar: QStatusBar
        self.footer_toggle_btn: IconButton
        self.footer_left: FooterLeftWidget
        self.boot_telemetry: BootTelemetryWidget
        self.startup_console: StartupConsole
        self.status_portale: StatusCard
        self.status_safework: StatusCard
        self.footer_right: FooterRightWidget

        self._setup_ui()
        self._init_timers()

    def _setup_ui(self) -> None:
        """Configura lo stile della barra di stato e inserisce i widget modulari."""
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(
            f"""
      QStatusBar {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS["bg_white"]}, stop:1 {COLORS["bg_light"]});
        border-top: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLORS["border_light"]}, stop:0.5 {COLORS["border_medium"]}, stop:1 {COLORS["border_light"]});
        min-height: 65px;
      }}
    """
        )
        self.main_window.setStatusBar(self.status_bar)

        # Pulsante Toggle Metriche/Licenza
        self.footer_toggle_btn = IconButton()
        self.footer_toggle_btn.setIcon(get_colored_icon(get_asset_path(Icons.ACTIVITY), COLORS["text_dark"]))
        self.footer_toggle_btn.setIconSize(QSize(20, 20))
        self.footer_toggle_btn.setFixedSize(40, 40)
        self.footer_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.footer_toggle_btn.setToolTip("Toggle System Metrics / License Info")
        self.footer_toggle_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; border: none; border-radius: 8px; margin: 0 5px; }} QPushButton:hover {{ background-color: {COLORS['bg_hover']}; }}"
        )
        self.footer_toggle_btn.clicked.connect(self._toggle_footer_stats)
        self.status_bar.addWidget(self.footer_toggle_btn)

        # Widget Sinistro (Info Business / Telemetria)
        self.footer_left = FooterLeftWidget()
        self.status_bar.addWidget(self.footer_left)

        self.boot_telemetry = BootTelemetryWidget()
        self.status_bar.addWidget(self.boot_telemetry)

        # Widget Centrale (Console di startup)
        self.startup_console = StartupConsole()
        self.status_bar.addWidget(self.startup_console, 1)

        # Widget Destro (Cards di stato Bot)
        self.status_portale = StatusCard("Portale Fornitori")
        self.status_safework = StatusCard("SafeWork")
        self.footer_right = FooterRightWidget(self.status_portale, self.status_safework)
        self.status_bar.addPermanentWidget(self.footer_right)

    def _init_timers(self) -> None:
        """Inizializza i timer per gli aggiornamenti ricorrenti dell'interfaccia."""
        self.autopilot_timer = QTimer(self)
        self.autopilot_timer.timeout.connect(self.update_autopilot_ui)
        self.autopilot_timer.start(10000)
        QTimer.singleShot(500, self.update_autopilot_ui)

    def _toggle_footer_stats(self) -> None:
        """Alterna la visualizzazione tra le informazioni di licenza e le metriche di sistema."""
        self._footer_stats_mode = not self._footer_stats_mode

        if self._footer_stats_mode:
            self.footer_left.setVisible(False)
            self.boot_telemetry.setVisible(True)
            if not self.boot_telemetry.timer.isActive():
                self.boot_telemetry.timer.start(1000)
            self.boot_telemetry._update_stats()
        else:
            self.boot_telemetry.setVisible(False)
            self.footer_left.setVisible(True)
            if self.boot_telemetry.timer.isActive():
                self.boot_telemetry.timer.stop()

    def update_license_info(self) -> None:
        """Recupera le informazioni sulla licenza e aggiorna le etichette nel footer."""
        license_info = get_license_info()
        if license_info:
            client = str(license_info.get("Cliente", "N/D"))
            expiry = str(license_info.get("Scadenza Licenza", "N/D"))
            hw_id = str(license_info.get("Hardware ID", "N/D"))
            config = config_manager.load_config()
            last_login = str(config.get("last_login_date", "N/D"))

            now_str = datetime.now(UTC).astimezone().strftime("%d/%m/%Y %H:%M")
            config_manager.set_config_value("last_login_date", now_str)

            self.footer_left.update_info(client, expiry, last_login, hw_id)
            self.footer_left.setVisible(True)

    def show_operational_state(self) -> None:
        """
        Transiziona la barra di stato alla modalità operativa.
        Esegue animazioni di fade-out sui widget di avvio e attiva quelli di monitoraggio.
        """
        import logging

        logger = logging.getLogger("StatusBar")

        try:
            # Animazione console
            console_effect = QGraphicsOpacityEffect(self.startup_console)
            self.startup_console.setGraphicsEffect(console_effect)
            self._console_anim = QPropertyAnimation(console_effect, b"opacity")
            self._console_anim.setDuration(600)
            self._console_anim.setStartValue(1.0)
            self._console_anim.setEndValue(0.0)
            self._console_anim.setEasingCurve(QEasingCurve.Type.InCubic)
            self._console_anim.finished.connect(lambda: self.startup_console.setVisible(False))
            self._console_anim.start()

            # Animazione telemetria
            telemetry_effect = QGraphicsOpacityEffect(self.boot_telemetry)
            self.boot_telemetry.setGraphicsEffect(telemetry_effect)
            self._telemetry_anim = QPropertyAnimation(telemetry_effect, b"opacity")
            self._telemetry_anim.setDuration(600)
            self._telemetry_anim.setStartValue(1.0)
            self._telemetry_anim.setEndValue(0.0)
            self._telemetry_anim.setEasingCurve(QEasingCurve.Type.InCubic)

            def hide_and_reset_telemetry() -> None:
                """Nasconde il widget di telemetria e ferma il timer al termine dell'animazione."""
                self.boot_telemetry.setVisible(False)
                self.boot_telemetry.setGraphicsEffect(None)  # type: ignore[arg-type]
                if self.boot_telemetry.timer.isActive():
                    self.boot_telemetry.timer.stop()

            self._telemetry_anim.finished.connect(hide_and_reset_telemetry)
            self._telemetry_anim.start()

            self.status_bar.clearMessage()
            self.footer_right.show_operational()
            self.update_license_info()
            self.footer_left.fade_in(400)
            self._footer_stats_mode = False
        except Exception as e:
            logger.critical(f"Error in show_operational_state: {e}", exc_info=True)

    def update_autopilot_ui(self) -> None:
        """
        Analizza i bot programmati nell'Autopilot e calcola il countdown per il task più imminente.
        Aggiorna le card di stato nella parte destra della barra.
        """
        from PySide6.QtCore import QTime

        config = config_manager.load_config()

        tasks = [
            ("PF", "TIMBRATURE", "timbrature_autopilot_enabled", "timbrature_autopilot_time"),
            (
                "PF",
                "SCARICO ODA",
                "scarico_oda_generale_autopilot_enabled",
                "scarico_oda_generale_autopilot_time",
            ),
            ("SW", "RICERCA PDL", "ricerca_pdl_autopilot_enabled", "ricerca_pdl_autopilot_time"),
        ]

        now = QTime.currentTime()
        imminent_pf: tuple[str, int] | None = None
        imminent_sw: tuple[str, int] | None = None
        min_secs_pf, min_secs_sw = float("inf"), float("inf")

        for site, name, enabled_key, time_key in tasks:
            if config.get(enabled_key, False):
                time_str = str(config.get(time_key, "09:00"))
                target_time = QTime.fromString(time_str, "HH:mm")
                if not target_time.isValid():
                    target_time = QTime.fromString(time_str, "H:mm")
                if not target_time.isValid():
                    continue

                secs_to = now.secsTo(target_time)
                if secs_to < 0:
                    secs_to += 24 * 3600

                if site == "PF" and secs_to < min_secs_pf:
                    min_secs_pf, imminent_pf = secs_to, (name, secs_to)
                elif site == "SW" and secs_to < min_secs_sw:
                    min_secs_sw, imminent_sw = secs_to, (name, secs_to)

        def format_countdown(name: str, secs: int) -> str:
            """Formatta il tempo rimanente in una stringa leggibile (H/M)."""
            h, m = secs // 3600, (secs % 3600) // 60
            return f"{name}: {'TRA ' + str(h) + 'H ' + str(m) + 'M' if h > 0 else 'TRA ' + str(m) + 'M'}"

        self.status_portale.setAutopilot(
            bool(imminent_pf), format_countdown(*imminent_pf) if imminent_pf else ""
        )
        self.status_safework.setAutopilot(
            bool(imminent_sw), format_countdown(*imminent_sw) if imminent_sw else ""
        )
