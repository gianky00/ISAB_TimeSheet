"""
SyncroJob - Service Controller
Controller per il coordinamento dei servizi di background, l'automazione dei report e la gestione del parallelismo bot.
Implementa una logica di scheduling intelligente che permette l'esecuzione contemporanea di bot su portali diversi
(es. Portale Fornitori e SafeWork) garantendo al contempo la sequenzialità delle operazioni sullo stesso sito.
Gestisce inoltre l'inoltro automatico delle notifiche critiche al bot Telegram e il check periodico degli aggiornamenti.
"""

import logging
import sys
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Final

from PySide6.QtCore import QObject, QTimer

from src.core import config_manager
from src.core.app_updater import check_for_updates
from src.core.database.maintenance_worker import DatabaseMaintenanceWorker
from src.core.notification_manager import NotificationManager
from src.core.report_service import ReportService
from src.gui.controllers.bot_queue_manager import BotQueueManager

logger = logging.getLogger(__name__)

# Assicuriamoci che i log siano visibili in console per il debug dell'utente
if not logger.handlers:
    _ch = logging.StreamHandler(sys.stdout)
    _ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(_ch)
    logger.setLevel(logging.INFO)


class ServiceController(QObject):
    """
    Gestore del ciclo di vita dei servizi asincroni e dei task pianificati (Autopilot).
    Coordina:
    - TelegramService per il monitoraggio remoto e l'invio di documenti.
    - Scheduler dei Bot per lo scarico automatico di timbrature, OdA e PDL.
    - Generazione e invio automatico dei report email via Outlook.
    """

    REPORT_WARNING_MIN: Final[int] = 21
    REPORT_EXPIRED_MIN: Final[int] = 30
    DEFAULT_INTERVAL_DAYS: Final[int] = 7

    def __init__(self, main_window: Any, telegram_service: Any) -> None:
        """
        Inizializza il controller dei servizi e le code di gestione del parallelismo.

        Args:
          main_window: Riferimento alla MainWindow dell'applicazione.
          telegram_service: Istanza del servizio Telegram.
        """
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service
        self.queue_manager = BotQueueManager()

        self.scheduler_timer: QTimer | None = None
        self._cert_worker: Any = None

    def start_all(self) -> None:
        """Avvia la sequenza di attivazione dei servizi di background."""
        QTimer.singleShot(1000, self.telegram.start_service)
        QTimer.singleShot(3000, self._check_updates)
        QTimer.singleShot(5000, self._run_db_maintenance)  # Manutenzione DB all'avvio

        NotificationManager.instance().notification_added.connect(self._forward_notification_to_telegram)

        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self._check_scheduled_tasks)
        self.scheduler_timer.start(60000)

    def _run_db_maintenance(self) -> None:
        """Avvia il worker di manutenzione DB in un thread separato."""
        worker = DatabaseMaintenanceWorker()
        worker.start()

    def stop_all(self) -> None:
        """Ferma tutti i servizi e i timer attivi."""
        if self.scheduler_timer:
            self.scheduler_timer.stop()

        if self.telegram:
            self.telegram.stop_service()

        logger.info("Tutti i servizi di background sono stati arrestati.")

    def _check_scheduled_tasks(self) -> None:
        """
        Verifica il match orario per i bot configurati in modalità Autopilot.
        Applica la logica di parallelismo intelligente per l'accodamento dei task.
        """
        # Usiamo l'ora locale per il confronto con la UI
        now_dt = datetime.now()
        now_time = now_dt.strftime("%H:%M")

        # Log INFO visibile per debug rapido dell'utente
        if now_dt.second < 5:  # Logghiamo solo all'inizio del minuto per non intasare
            logger.info(f"[Autopilot] Scheduler Tick - Ora locale: {now_time}")

        config = config_manager.load_config()

        scheduled_bots = [
            (
                "timbrature",
                "timbrature_bot_panel",
                "portale_fornitori",
                str(config.get("timbrature_autopilot_time", "09:00")),
                bool(config.get("timbrature_autopilot_enabled", False)),
                None,
            ),
            (
                "scarico_oda_generale",
                "dettagli_panel",
                "portale_fornitori",
                str(config.get("scarico_oda_generale_autopilot_time", "09:00")),
                bool(config.get("scarico_oda_generale_autopilot_enabled", False)),
                self._prepare_scarico_oda_generale,
            ),
            (
                "ricerca_pdl",
                "pdl_search_panel",
                "safework",
                str(config.get("ricerca_pdl_autopilot_time", "09:00")),
                bool(config.get("ricerca_pdl_autopilot_enabled", False)),
                None,
            ),
        ]

        for bot_id, panel_attr, site, target_time, enabled, prepare_cb in scheduled_bots:
            if enabled and now_time == target_time and hasattr(self.mw, panel_attr):
                panel = getattr(self.mw, panel_attr)
                if prepare_cb:
                    prepare_cb(panel)
                self.queue_manager.schedule_bot(
                    bot_id, panel, site, f"Avvio pianificato automatico ({now_time})..."
                )

        self._check_report_email_schedule(config, now_time)
        self._check_certificati_schedule(config, now_time)

    def _check_report_email_schedule(self, config: dict[str, Any], now_time: str) -> None:
        """Gestisce l'invio del report email basandosi su orario e intervallo di giorni configurati."""
        if not config.get("report_email_autopilot_enabled", False):
            return
        if now_time != str(config.get("report_email_autopilot_time", "08:00")):
            return

        interval = int(
            config.get("report_email_autopilot_interval_days", ReportService.DEFAULT_INTERVAL_DAYS)
        )
        last_sent = config.get("report_email_autopilot_last_sent")

        should_send = last_sent is None
        if not should_send:
            with suppress(Exception):
                last_sent_dt = datetime.fromisoformat(str(last_sent))
                if (datetime.now(UTC).astimezone() - last_sent_dt).days >= interval:
                    should_send = True

        if should_send:
            ReportService.send_scheduled_report_email()

    def _check_certificati_schedule(self, config: dict[str, Any], now_time: str) -> None:
        """Gestisce l'automazione dei certificati campione (aggiornamento DB + analisi scadenze)."""
        enabled = config.get("certificati_autopilot_enabled", False)
        target_time = str(config.get("certificati_autopilot_time", "08:30"))

        if not enabled:
            return

        if now_time == target_time:
            logger.info(f"Autopilot Certificati: Match orario trovato ({now_time})")
        else:
            return

        interval = int(config.get("certificati_autopilot_interval_days", 1))
        last_sent = config.get("certificati_autopilot_last_sent")

        should_run = last_sent is None
        if not should_run:
            with suppress(Exception):
                last_sent_dt = datetime.fromisoformat(str(last_sent))
                # Calcolo giorni passati usando date ingenue per semplicità di test locale
                diff_days = (datetime.now() - last_sent_dt.replace(tzinfo=None)).days
                logger.info(
                    f"Autopilot Certificati: Check intervallo - Ultimo: {last_sent}, Giorni passati: {diff_days}, Richiesti: {interval}"
                )
                if diff_days >= interval:
                    should_run = True

        if should_run:
            self._run_certificati_autopilot(config)
        else:
            logger.info(
                f"Autopilot Certificati: Orario match ma intervallo giorni ({interval}) non ancora raggiunto."
            )

    def _run_certificati_autopilot(self, config: dict[str, Any]) -> None:
        """Avvia il worker per l'aggiornamento dei certificati campione."""
        cert_path = config.get("certificati_campione_path", "")
        if not cert_path or not Path(cert_path).exists():
            logger.warning("Autopilot Certificati: Path non configurato o non valido.")
            return

        from src.core.contabilita_worker import ContabilitaWorker

        logger.info("Autopilot Certificati: Avvio aggiornamento database...")
        worker = ContabilitaWorker(
            file_path="", giornaliere_path="", attivita_path="", certificati_path=cert_path
        )
        # Salviamo il riferimento per evitare garbage collection
        self._cert_worker = worker
        worker.finished_signal.connect(self._on_certificati_worker_finished)
        worker.start()

    def _on_certificati_worker_finished(
        self, success: bool, msg: str, added: int, removed: int, duration: float
    ) -> None:
        """Al termine dell'aggiornamento DB, avvia l'analisi scadenze e la creazione della bozza Outlook."""
        logger.info(
            f"Autopilot Certificati: Aggiornamento terminato. Success: {success}, Added: {added}, Removed: {removed}"
        )

        # Procediamo sempre all'analisi se non ci sono errori critici bloccanti,
        # perché potremmo avere già dati nel DB da analizzare.
        if not success and "Errore critico" in msg:
            logger.error(f"Autopilot Certificati: Aggiornamento fallito per errore critico: {msg}")
            NotificationManager.instance().add_notification(
                title="Errore Autopilot Certificati",
                message=f"Aggiornamento database fallito: {msg}",
                level="error",
            )
        else:
            try:
                logger.info("Autopilot Certificati: Avvio analisi scadenze e generazione bozza...")
                self._generate_certificati_outlook_draft()

                config_manager.set_config_value(
                    "certificati_autopilot_last_sent", datetime.now(UTC).astimezone().isoformat()
                )

                status_msg = "Aggiornamento e Analisi completati."
                if not success:
                    status_msg = "Analisi completata (Aggiornamento DB saltato o nessun nuovo dato)."

                NotificationManager.instance().add_notification(
                    title="Autopilot Certificati",
                    message=f"{status_msg} Bozza Outlook creata.",
                    level="success",
                )
            except Exception as e:
                logger.exception("Errore durante l'analisi automatica certificati")
                NotificationManager.instance().add_notification(
                    title="Errore Autopilot Certificati",
                    message=f"Errore durante l'analisi: {e}",
                    level="error",
                )
        self._cert_worker = None

    def _generate_certificati_outlook_draft(self) -> None:
        """Esegue l'analisi delle scadenze e crea una bozza Outlook tramite l'interfaccia UI (per uniformità)."""
        from src.gui.main_window.page_index import PageIndex

        # Tentiamo di recuperare il widget dei certificati dalla MainWindow per usare la logica ricca (screenshot + PDF)
        panel = self.mw.navigation_controller.get_panel(PageIndex.STRUMENTALE)
        if panel and hasattr(panel, "certificati_widget"):
            logger.info("Autopilot Certificati: Utilizzo logica UI per generazione email audit...")
            # Assicuriamoci che i dati nel widget siano rinfrescati prima dell'analisi
            panel.certificati_widget.refresh_data()
            # Invio email identica alla versione manuale del tab
            panel.certificati_widget._run_analysis_and_send_email()
            return

        # Logica di Fallback (Solo se la UI non fosse accessibile)
        from src.core.contabilita.certificati_engine import CertificatiEngine
        from src.core.contabilita_manager import ContabilitaManager

        engine = CertificatiEngine()
        engine.load_exclusions()
        data = ContabilitaManager.get_certificati_campione_data()

        if not data:
            logger.warning("Autopilot Certificati: Nessun dato trovato nel database.")
            return

        from src.core.contabilita_queries import ContabilitaQueries

        groups: dict[str, list[tuple[Any, ...]]] = {}
        for r in data:
            key = (
                str(r[ContabilitaQueries.CERT_IDX_ID_STRUMENTO]).strip()
                or str(r[ContabilitaQueries.CERT_IDX_MATRICOLA]).strip()
            )
            if key not in groups:
                groups[key] = []
            groups[key].append(r)

        certs_to_report = []
        for certs in groups.values():
            latest = max(certs, key=lambda x: str(x[ContabilitaQueries.CERT_IDX_EMISSIONE]))
            matricola = str(latest[ContabilitaQueries.CERT_IDX_MATRICOLA]).strip()

            if matricola in engine._exclusions:
                continue

            scadenza = latest[ContabilitaQueries.CERT_IDX_SCADENZA]
            days, _ = engine.calculate_days_and_status(scadenza)

            if days is not None and days <= engine.EXPIRING_THRESHOLD:
                certs_to_report.append(
                    {
                        "id": latest[ContabilitaQueries.CERT_IDX_ID_STRUMENTO],
                        "matricola": matricola,
                        "modello": latest[ContabilitaQueries.CERT_IDX_MODELLO],
                        "scadenza": scadenza,
                        "giorni": days,
                    }
                )

        if certs_to_report:
            engine.generate_outlook_draft(certs_to_report)
        else:
            logger.info("Autopilot Certificati: Nessun certificato in scadenza da segnalare.")

    def handle_manual_sync_request(self, bot_id: str) -> None:
        """Gestisce la richiesta manuale di sincronizzazione dal widget Autopilot."""
        logger.info(f"Autopilot: Richiesta sincronizzazione manuale per {bot_id}")
        config = config_manager.load_config()

        if bot_id == "certificati":
            self._run_certificati_autopilot(config)
        else:
            # Per gli altri bot, cerchiamo il pannello corrispondente e avviamo
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
