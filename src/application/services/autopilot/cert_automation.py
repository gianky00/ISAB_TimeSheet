"""SyncroJob - CertCampioneAutomator.

Modulo responsabile dell'automazione del flusso dei certificati campione:
aggiornamento del database, analisi scadenze e generazione di bozze Outlook.
"""

import logging
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.application.services import config_manager
from src.application.services.notification_manager import NotificationManager

logger = logging.getLogger(__name__)


class CertCampioneAutomator:
    """Gestore automatizzato per il monitoraggio e l'elaborazione dei certificati campione."""

    def __init__(self, main_window: Any) -> None:
        """Inizializza l'automatore dei certificati.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
        """
        self.mw = main_window
        self._cert_worker: Any = None
        self._fallback_worker: Any = None

    def check_and_run(self, config: dict[str, Any]) -> None:
        """Verifica se l'intervallo di giorni dall'ultimo invio è stato raggiunto ed avvia.

        Args:
            config: Configurazione corrente dell'applicazione.
        """
        interval = int(config.get("certificati_autopilot_interval_days", 1))
        last_sent = config.get("certificati_autopilot_last_sent")

        should_run = last_sent is None
        if not should_run:
            with suppress(Exception):
                last_sent_dt = datetime.fromisoformat(str(last_sent))
                diff_days = (datetime.now() - last_sent_dt.replace(tzinfo=None)).days
                if diff_days >= interval:
                    should_run = True

        if should_run:
            self.run(config)
        else:
            logger.info(
                f"Autopilot Certificati: Match orario ma intervallo giorni ({interval}) non ancora raggiunto."
            )

    def run(self, config: dict[str, Any]) -> None:
        """Avvia la pipeline di sincronizzazione ed analisi dei certificati.

        Args:
            config: Configurazione corrente dell'applicazione.
        """
        cert_path = config.get("certificati_campione_path", "")
        if not cert_path or not Path(cert_path).exists():
            logger.warning("Autopilot Certificati: Path non configurato o non valido.")
            return

        from src.application.services.contabilita_worker import ContabilitaWorker  # noqa: PLC0415

        logger.info("Autopilot Certificati: Avvio aggiornamento database...")
        self._cert_worker = ContabilitaWorker(
            file_path="", giornaliere_path="", attivita_path="", certificati_path=cert_path
        )
        self._cert_worker.finished_signal.connect(self._on_worker_finished)
        self._cert_worker.start()

    def _on_worker_finished(self, success: bool, msg: str, added: int, removed: int, duration: float) -> None:
        """Callback al completamento dell'aggiornamento database.

        Args:
            success: Flag di successo del worker.
            msg: Messaggio di ritorno del worker.
            added: Record inseriti.
            removed: Record rimossi.
            duration: Durata esecuzione.
        """
        logger.info(
            f"Autopilot Certificati: Aggiornamento terminato. Success: {success}, Added: {added}, Removed: {removed}"
        )

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
                self._generate_outlook_draft()

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

    def _generate_outlook_draft(self) -> None:
        """Genera la bozza Outlook delegando alla UI o avviando il worker di fallback."""
        from src.gui.main_window.page_index import PageIndex  # noqa: PLC0415

        # Tentiamo di recuperare il widget dei certificati dalla MainWindow per usare la logica con screenshot + PDF
        if hasattr(self.mw, "navigation_controller"):
            panel = self.mw.navigation_controller.get_panel(PageIndex.STRUMENTALE)
            if panel and hasattr(panel, "certificati_widget"):
                logger.info("Autopilot Certificati: Utilizzo logica UI per generazione email...")
                panel.certificati_widget.refresh_data()
                panel.certificati_widget._run_analysis_and_send_email()
                return

        # Logica di Fallback Asincrona (Se la UI o il widget non sono accessibili)
        from src.gui.workers.autopilot_cert_worker import AutopilotCertWorker  # noqa: PLC0415

        if self._fallback_worker and self._fallback_worker.isRunning():
            return

        self._fallback_worker = AutopilotCertWorker()
        self._fallback_worker.start()
