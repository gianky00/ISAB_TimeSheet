"""SyncroJob - Service Controller (Refactored).

Controller per il coordinamento dei servizi di background, l'automazione dei report
e la gestione del parallelismo dei bot.
Delega lo scheduling temporale ad AutopilotScheduler e la gestione dei certificati
a CertCampioneAutomator per rispettare il Single Responsibility Principle (SRP).
"""

import logging
import sys
from datetime import UTC, datetime
from typing import Any

from PySide6.QtCore import QObject, QTimer

from src.application.services import config_manager
from src.application.services.app_updater import check_for_updates
from src.application.services.autopilot.cert_automation import CertCampioneAutomator
from src.application.services.autopilot.scheduler import AutopilotScheduler
from src.application.services.database.maintenance_worker import DatabaseMaintenanceWorker
from src.application.services.notification_manager import NotificationManager
from src.gui.controllers.bot_queue_manager import BotQueueManager
from src.gui.workers.autopilot_report_worker import AutopilotReportWorker

logger = logging.getLogger(__name__)

# Assicuriamoci che i log siano visibili in console per il debug
if not logger.handlers:
    _ch = logging.StreamHandler(sys.stdout)
    _ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(_ch)
    logger.setLevel(logging.INFO)


class ServiceController(QObject):
    """Gestore del ciclo di vita dei servizi asincroni e dei task pianificati (Autopilot).

    Orchestra e coordina le componenti specializzate in modo ad alta coesione.
    """

    def __init__(self, main_window: Any, telegram_service: Any) -> None:
        """Inizializza il controller dei servizi.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
            telegram_service: Istanza del servizio Telegram.
        """
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service
        self.queue_manager = BotQueueManager()

        # Istanziazione delle componenti specializzate (SRP)
        self.scheduler = AutopilotScheduler(self)
        self.cert_automator = CertCampioneAutomator(main_window)

        self._report_worker: AutopilotReportWorker | None = None

        # Collegamento dei segnali dello scheduler
        self.scheduler.bot_triggered.connect(self._on_bot_triggered)
        self.scheduler.report_triggered.connect(self._on_report_triggered)
        self.scheduler.certificati_triggered.connect(self._on_certificati_triggered)

    def start_all(self) -> None:
        """Avvia la sequenza di attivazione dei servizi di background."""
        QTimer.singleShot(1000, self.telegram.start_service)
        QTimer.singleShot(3000, self._check_updates)
        QTimer.singleShot(5000, self._run_db_maintenance)

        NotificationManager.instance().notification_added.connect(self._forward_notification_to_telegram)

        # Avvio dello scheduler temporale
        self.scheduler.start()

    def _run_db_maintenance(self) -> None:
        """Avvia il worker di manutenzione DB in un thread separato."""
        worker = DatabaseMaintenanceWorker()
        worker.start()

    def stop_all(self) -> None:
        """Ferma tutti i servizi e i timer attivi."""
        self.scheduler.stop()

        if self.telegram:
            self.telegram.stop_service()

        logger.info("Tutti i servizi di background sono stati arrestati.")

    def _on_bot_triggered(self, bot_id: str, panel_attr: str, site: str) -> None:
        """Risponde al segnale di trigger di un bot dello scheduler."""
        if hasattr(self.mw, panel_attr):
            panel = getattr(self.mw, panel_attr)
            if bot_id == "scarico_oda_generale":
                self._prepare_scarico_oda_generale(panel)
            now_time = datetime_now_str()
            self.queue_manager.schedule_bot(
                bot_id, panel, site, f"Avvio pianificato automatico ({now_time})..."
            )

    def _on_report_triggered(self, config: dict[str, Any]) -> None:
        """Risponde al segnale di trigger dell'invio report e-mail dello scheduler."""
        interval = int(config.get("report_email_autopilot_interval_days", 7))
        last_sent = config.get("report_email_autopilot_last_sent")

        should_send = last_sent is None
        if not should_send:
            try:
                last_sent_dt = datetime.fromisoformat(str(last_sent))
                if (datetime.now(UTC).astimezone() - last_sent_dt).days >= interval:
                    should_send = True
            except Exception:
                logger.exception("Errore nella validazione oraria del report")

        if should_send:
            if self._report_worker and self._report_worker.isRunning():
                return
            self._report_worker = AutopilotReportWorker()
            self._report_worker.start()

    def _on_certificati_triggered(self, config: dict[str, Any]) -> None:
        """Risponde al segnale di trigger dell'elaborazione certificati dello scheduler."""
        self.cert_automator.check_and_run(config)

    def handle_manual_sync_request(self, bot_id: str) -> None:
        """Gestisce la richiesta manuale di sincronizzazione dal widget Autopilot."""
        logger.info(f"Autopilot: Richiesta sincronizzazione manuale per {bot_id}")
        config = config_manager.load_config()

        if bot_id == "certificati":
            self.cert_automator.run(config)
        else:
            panel_map = {
                "timbrature": "timbrature_bot_panel",
                "scarico_oda_generale": "dettagli_panel",
                "ricerca_pdl": "pdl_search_panel",
            }
            attr = panel_map.get(bot_id)
            if attr and hasattr(self.mw, attr):
                panel = getattr(self.mw, attr)
                site = "portale_fornitori" if bot_id != "ricerca_pdl" else "safework"
                if bot_id == "scarico_oda_generale":
                    self._prepare_scarico_oda_generale(panel)
                self.queue_manager.schedule_bot(bot_id, panel, site, "Avvio manuale da Autopilot...")
            else:
                logger.warning(f"Autopilot: Pannello per {bot_id} non trovato o non supportato.")

    def _prepare_scarico_oda_generale(self, panel: Any) -> None:
        """Configura il pannello Dettagli OdA per uno scarico massivo senza filtri specifici."""
        if hasattr(panel, "data_table"):
            panel.data_table.set_data([])
            panel.log_widget.append("   Tabella pulita per scarico generale (senza filtro OdA)")

    def _check_updates(self) -> None:
        """Interroga il server per verificare la presenza di nuove release software."""
        check_for_updates(parent=self.mw, silent=True, callback=self.mw._show_update_banner)

    def _forward_notification_to_telegram(self, notification: dict[str, Any]) -> None:
        """Inoltra i messaggi di sistema con criticità elevata al bot Telegram registrato."""
        if notification.get("title") == "Telegram":
            return
        level = notification.get("level", "info")
        if level in ("success", "error", "warning"):
            icon = "✅" if level == "success" else "[ERR]" if level == "error" else "[!]"
            self.telegram.send_message_sync(
                f"{icon} *{notification.get('title', 'Notifica')}*\n{notification.get('message', '')}"
            )


def datetime_now_str() -> str:
    """Restituisce la stringa dell'ora locale corrente."""
    return datetime.now().strftime("%H:%M")
