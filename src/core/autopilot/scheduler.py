"""SyncroJob - Autopilot Scheduler.

Modulo responsabile esclusivamente del tracciamento del tempo (scheduling orario)
e della temporizzazione dei bot e dei task pianificati (Autopilot).
"""

import logging
from datetime import datetime
from typing import Any

from PySide6.QtCore import QObject, QTimer, Signal

from src.core import config_manager

logger = logging.getLogger(__name__)

# Massimi secondi per la visualizzazione del log del tick periodico
_MAX_TICK_LOG_SECONDS = 5


class AutopilotScheduler(QObject):
    """Motore di schedulazione temporale per i task e i bot configurati in Autopilot.

    Gestisce il ticking periodico (60 secondi) e valuta la coincidenza oraria
    con le configurazioni utente, emettendo segnali per l'avvio delle azioni.
    """

    bot_triggered = Signal(str, str, str)  # bot_id, panel_attr, site
    report_triggered = Signal(dict)  # config
    certificati_triggered = Signal(dict)  # config

    def __init__(self, parent: Any = None) -> None:
        """Inizializza lo scheduler dell'Autopilot.

        Args:
            parent: Oggetto genitore opzionale (QObject).
        """
        super().__init__(parent)
        self.scheduler_timer: QTimer | None = None

    def start(self) -> None:
        """Avvia il timer di monitoraggio dello scheduler."""
        if self.scheduler_timer and self.scheduler_timer.isActive():
            return

        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self.check_scheduled_tasks)
        self.scheduler_timer.start(60000)
        logger.info("Scheduler Autopilot avviato (tick ogni 60 secondi).")

    def stop(self) -> None:
        """Ferma il timer dello scheduler."""
        if self.scheduler_timer:
            self.scheduler_timer.stop()
            logger.info("Scheduler Autopilot arrestato.")

    def check_scheduled_tasks(self) -> None:
        """Tick periodico che confronta l'orario attuale con i task configurati."""
        now_dt = datetime.now()
        now_time = now_dt.strftime("%H:%M")

        # Registriamo il log solo nei primi secondi per non intasare l'output
        if now_dt.second < _MAX_TICK_LOG_SECONDS:
            logger.info(f"[Autopilot] Scheduler Tick - Ora locale: {now_time}")

        config = config_manager.load_config()

        # 1. Definizione e controllo orario dei bot standard
        scheduled_bots = [
            (
                "timbrature",
                "timbrature_bot_panel",
                "portale_fornitori",
                str(config.get("timbrature_autopilot_time", "09:00")),
                bool(config.get("timbrature_autopilot_enabled", False)),
            ),
            (
                "scarico_oda_generale",
                "dettagli_panel",
                "portale_fornitori",
                str(config.get("scarico_oda_generale_autopilot_time", "09:00")),
                bool(config.get("scarico_oda_generale_autopilot_enabled", False)),
            ),
            (
                "ricerca_pdl",
                "pdl_search_panel",
                "safework",
                str(config.get("ricerca_pdl_autopilot_time", "09:00")),
                bool(config.get("ricerca_pdl_autopilot_enabled", False)),
            ),
        ]

        for bot_id, panel_attr, site, target_time, enabled in scheduled_bots:
            if enabled and now_time == target_time:
                logger.info(f"[Autopilot] Orario corrispondente per bot '{bot_id}' alle {now_time}.")
                self.bot_triggered.emit(bot_id, panel_attr, site)

        # 2. Segnale per l'invio del report e-mail asincrono
        if bool(config.get("report_email_autopilot_enabled", False)):
            target_report_time = str(config.get("report_email_autopilot_time", "08:00"))
            if now_time == target_report_time:
                logger.info(f"[Autopilot] Orario corrispondente per Report E-mail alle {now_time}.")
                self.report_triggered.emit(config)

        # 3. Segnale per l'analisi dei certificati campione
        if bool(config.get("certificati_autopilot_enabled", False)):
            target_cert_time = str(config.get("certificati_autopilot_time", "08:30"))
            if now_time == target_cert_time:
                logger.info(f"[Autopilot] Orario corrispondente per Certificati alle {now_time}.")
                self.certificati_triggered.emit(config)
