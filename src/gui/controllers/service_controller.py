"""
Controller per il coordinamento dei servizi di background (Telegram, Lyra, Update).
"""

from PyQt6.QtCore import QObject, QTimer

from src.core.app_updater import check_for_updates
from src.core.notification_manager import NotificationManager


class ServiceController(QObject):
    """
    Gestisce il ciclo di vita dei servizi di background e
    il coordinamento delle notifiche.
    """

    def __init__(self, main_window, telegram_service, lyra_sentinel):
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service
        self.sentinel = lyra_sentinel

    def start_all(self):
        """Avvia tutti i servizi in background con i relativi ritardi."""
        # Lyra Sentinel
        self.sentinel.anomalies_found.connect(self.mw._on_anomalies_found)
        QTimer.singleShot(2000, self.sentinel.start)

        # Telegram
        QTimer.singleShot(1000, self.telegram.start_service)

        # Aggiornamenti
        QTimer.singleShot(3000, self._check_updates)

        # Collegamento notifiche globali -> Telegram
        NotificationManager.instance().notification_added.connect(
            self._forward_notification_to_telegram
        )

        # Scheduler (ogni 60s) per task pianificati
        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self._check_scheduled_tasks)
        self.scheduler_timer.start(60000)  # 1 minuto

    def _check_scheduled_tasks(self):
        """Controlla se ci sono task pianificati da eseguire ora."""
        from datetime import datetime

        from src.core import config_manager

        config = config_manager.load_config()

        # 1. Timbrature Autopilot
        if config.get("timbrature_autopilot_enabled", False):
            target_time = config.get("timbrature_autopilot_time", "09:00")
            now = datetime.now().strftime("%H:%M")

            if now == target_time:
                # Esegui solo se il pannello è disponibile
                if hasattr(self.mw, "timbrature_bot_panel"):
                    panel = self.mw.timbrature_bot_panel
                    # Verifica che non sia già in esecuzione
                    if panel.start_btn.isEnabled():
                        # Simula avvio
                        panel.log_widget.append(
                            f"Avvio pianificato automatico ({now})..."
                        )
                        panel._on_start()

    def _check_updates(self):
        """Controlla gli aggiornamenti in background."""
        check_for_updates(
            parent=self.mw, silent=True, callback=self.mw._show_update_banner
        )

    def _forward_notification_to_telegram(self, notification):
        """Inoltra notifiche importanti al bot Telegram."""
        if notification.get("title") == "Telegram":
            return

        level = notification.get("level", "info")
        if level in ["success", "error", "warning"]:
            title = notification.get("title", "Notifica")
            msg = notification.get("message", "")
            icon = (
                "[OK]" if level == "success" else "[ERR]" if level == "error" else "[!]"
            )
            text = f"{icon} *{title}*\n{msg}"
            self.telegram.send_message_sync(text)
