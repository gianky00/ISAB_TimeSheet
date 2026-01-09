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
        NotificationManager.instance().notification_added.connect(self._forward_notification_to_telegram)

    def _check_updates(self):
        """Controlla gli aggiornamenti in background."""
        check_for_updates(parent=self.mw, silent=True, callback=self.mw._show_update_banner)

    def _forward_notification_to_telegram(self, notification):
        """Inoltra notifiche importanti al bot Telegram."""
        if notification.get("title") == "Telegram":
            return

        level = notification.get("level", "info")
        if level in ["success", "error", "warning"]:
            title = notification.get("title", "Notifica")
            msg = notification.get("message", "")
            icon = "✅" if level == "success" else "❌" if level == "error" else "⚠️"

            text = f"{icon} *{title}*\n{msg}"
            self.telegram.send_message_sync(text)
