from datetime import datetime

from PyQt6.QtCore import QEasingCurve, QObject, QPropertyAnimation, QSize, Qt, QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QPushButton, QStatusBar

from src.core import config_manager
from src.core.constants import Icons
from src.core.license_validator import get_license_info
from src.gui.widgets.footer_stats import (
    BootTelemetryWidget,
    FooterLeftWidget,
    FooterRightWidget,
    StartupConsole,
)
from src.gui.widgets.status_card import StatusCard
from src.utils.helpers import get_asset_path, get_colored_icon


class StatusBarComponent(QObject):
    """
    Manages the StatusBar, including Footer Stats, Telemetry, and License Info.
    """

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self._footer_stats_mode = False
        self._setup_ui()
        self._init_timers()

    def _setup_ui(self):
        self.status_bar = QStatusBar()
        # Footer con gradiente sfumato e bordo superiore accentuato
        self.status_bar.setStyleSheet(
            """
            QStatusBar {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,
                    stop:1 #F5F5F5
                );
                border-top: 2px solid qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E0E0E0,
                    stop:0.5 #BDBDBD,
                    stop:1 #E0E0E0
                );
                min-height: 65px;
            }
        """
        )
        self.main_window.setStatusBar(self.status_bar)

        # Toggle Button
        self.footer_toggle_btn = QPushButton()
        self.footer_toggle_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.ACTIVITY), "#000000")
        )
        self.footer_toggle_btn.setIconSize(QSize(20, 20))
        self.footer_toggle_btn.setFixedSize(40, 40)
        self.footer_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.footer_toggle_btn.setToolTip("Toggle System Metrics / License Info")
        self.footer_toggle_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                margin: 0 5px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """
        )
        self.footer_toggle_btn.clicked.connect(self._toggle_footer_stats)
        self.status_bar.addWidget(self.footer_toggle_btn)

        # 1. LEFT: Mega Widget (Cliente, Scadenza, Login, Accounts)
        self.footer_left = FooterLeftWidget()
        self.footer_left.setVisible(True)
        # Delegating clicks to main window callbacks (will be connected by main window or signal connector)
        # For now, we expose signals or methods to connect
        self.status_bar.addWidget(self.footer_left)

        # 1b. LEFT: Boot Telemetry (Hacker Mode)
        self.boot_telemetry = BootTelemetryWidget()
        self.boot_telemetry.setVisible(True)
        self.status_bar.addWidget(self.boot_telemetry)

        # 3. STARTUP CONSOLE (Centrale)
        self.startup_console = StartupConsole()
        self.startup_console.setVisible(True)
        self.status_bar.addWidget(self.startup_console, 1)

        # 2. RIGHT: Status Cards
        self.status_portale = StatusCard("Portale Fornitori")
        self.status_safework = StatusCard("SafeWork")

        self.footer_right = FooterRightWidget(self.status_portale, self.status_safework)
        self.status_bar.addPermanentWidget(self.footer_right)

    def _init_timers(self):
        # Timer per aggiornamento automatico dello stato Autopilot (ogni 10 secondi)
        self.autopilot_timer = QTimer(self)
        self.autopilot_timer.timeout.connect(self.update_autopilot_ui)
        self.autopilot_timer.start(10000)

        # Primo aggiornamento immediato
        QTimer.singleShot(500, self.update_autopilot_ui)

    def _toggle_footer_stats(self):
        """Toggle tra System Metrics (boot_telemetry) e License Info (footer_left)."""
        self._footer_stats_mode = not self._footer_stats_mode

        if self._footer_stats_mode:
            self.footer_left.setVisible(False)
            self.boot_telemetry.setVisible(True)
            self.boot_telemetry.setGraphicsEffect(None)
            if not self.boot_telemetry.timer.isActive():
                self.boot_telemetry.timer.start(1000)
            self.boot_telemetry._update_stats()
        else:
            self.boot_telemetry.setVisible(False)
            self.footer_left.setVisible(True)
            if self.boot_telemetry.timer.isActive():
                self.boot_telemetry.timer.stop()

    def update_license_info(self):
        """Aggiorna le etichette della licenza nella status bar."""
        license_info = get_license_info()
        if license_info:
            client = license_info.get("Cliente", "N/D")
            expiry = license_info.get("Scadenza Licenza", "N/D")
            hw_id = license_info.get("Hardware ID", "N/D")
            config = config_manager.load_config()
            last_login = config.get("last_login_date", "N/D")

            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            config_manager.set_config_value("last_login_date", now_str)

            self.footer_left.update_info(client, expiry, last_login, hw_id)
            self.footer_left.setVisible(True)

    def show_operational_state(self):
        """Rimuove console e progress bar, mostra i widget operativi."""
        import logging

        logger = logging.getLogger("StatusBar")

        try:
            logger.info("Starting show_operational_state...")

            # Animazione fade-out per startup_console
            logger.info("Setting up console animation...")
            console_effect = QGraphicsOpacityEffect(self.startup_console)
            self.startup_console.setGraphicsEffect(console_effect)
            console_anim = QPropertyAnimation(console_effect, b"opacity")
            console_anim.setDuration(600)
            console_anim.setStartValue(1.0)
            console_anim.setEndValue(0.0)
            console_anim.setEasingCurve(QEasingCurve.Type.InCubic)
            console_anim.finished.connect(
                lambda: self.startup_console.setVisible(False)
            )
            console_anim.start()

            # Animazione fade-out per boot_telemetry
            logger.info("Setting up telemetry animation...")
            telemetry_effect = QGraphicsOpacityEffect(self.boot_telemetry)
            self.boot_telemetry.setGraphicsEffect(telemetry_effect)
            telemetry_anim = QPropertyAnimation(telemetry_effect, b"opacity")
            telemetry_anim.setDuration(600)
            telemetry_anim.setStartValue(1.0)
            telemetry_anim.setEndValue(0.0)
            telemetry_anim.setEasingCurve(QEasingCurve.Type.InCubic)

            def hide_and_reset_telemetry():
                try:
                    self.boot_telemetry.setVisible(False)
                    self.boot_telemetry.setGraphicsEffect(None)
                    if self.boot_telemetry.timer.isActive():
                        self.boot_telemetry.timer.stop()
                except Exception as e:
                    logger.error(f"Error in hide_and_reset_telemetry: {e}")

            telemetry_anim.finished.connect(hide_and_reset_telemetry)
            telemetry_anim.start()

            # Keep refs
            self._console_anim = console_anim
            self._telemetry_anim = telemetry_anim

            logger.info("Updating status bar...")
            self.status_bar.clearMessage()
            self.footer_right.show_operational()

            logger.info("Updating license info...")
            self.update_license_info()

            logger.info("Fading in footer...")
            self.footer_left.fade_in(400)
            self._footer_stats_mode = False

            logger.info("show_operational_state completed successfully")
        except Exception as e:
            logger.critical(f"Error in show_operational_state: {e}", exc_info=True)
            raise

    def update_autopilot_ui(self):
        """Aggiorna le card di stato con il countdown del task più imminente."""
        from PyQt6.QtCore import QTime

        config = config_manager.load_config()

        tasks = [
            (
                "PF",
                "TIMBRATURE",
                "timbrature_autopilot_enabled",
                "timbrature_autopilot_time",
            ),
            (
                "PF",
                "SCARICO ODA",
                "scarico_oda_generale_autopilot_enabled",
                "scarico_oda_generale_autopilot_time",
            ),
            (
                "SW",
                "RICERCA PDL",
                "ricerca_pdl_autopilot_enabled",
                "ricerca_pdl_autopilot_time",
            ),
        ]

        now = QTime.currentTime()
        imminent_pf = None
        imminent_sw = None
        min_secs_pf = float("inf")
        min_secs_sw = float("inf")

        for site, name, enabled_key, time_key in tasks:
            if config.get(enabled_key, False):
                target_time_str = config.get(time_key, "09:00")
                target_time = QTime.fromString(target_time_str, "HH:mm")
                if not target_time.isValid():
                    target_time = QTime.fromString(target_time_str, "H:mm")
                if not target_time.isValid():
                    continue

                secs_to = now.secsTo(target_time)
                if secs_to < 0:
                    secs_to += 24 * 3600

                if site == "PF":
                    if secs_to < min_secs_pf:
                        min_secs_pf = secs_to
                        imminent_pf = (name, secs_to)
                elif site == "SW":
                    if secs_to < min_secs_sw:
                        min_secs_sw = secs_to
                        imminent_sw = (name, secs_to)

        def format_countdown(name, secs):
            hours = secs // 3600
            mins = (secs % 3600) // 60
            countdown_text = f"TRA {hours}H {mins}M" if hours > 0 else f"TRA {mins}M"
            return f"{name}: {countdown_text}"

        if imminent_pf:
            self.status_portale.setAutopilot(True, format_countdown(*imminent_pf))
        else:
            self.status_portale.setAutopilot(False)

        if imminent_sw:
            self.status_safework.setAutopilot(True, format_countdown(*imminent_sw))
        else:
            self.status_safework.setAutopilot(False)
