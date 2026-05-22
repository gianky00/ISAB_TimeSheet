"""SyncroJob - Autopilot Certificati Worker.

Worker asincrono per l'analisi automatica delle scadenze certificati.
Evita il freeze della GUI durante le query SQL e l'automazione Outlook (Fallback).
"""

import logging
from typing import Any

from PySide6.QtCore import QThread, Signal

from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.contabilita_manager import ContabilitaManager
from src.core.contabilita_queries import ContabilitaQueries

logger = logging.getLogger(__name__)


class AutopilotCertWorker(QThread):
    """Worker che esegue l'analisi dei certificati in background quando la UI non  accessibile."""

    finished_signal = Signal(bool)

    def run(self) -> None:
        """Esegue l'analisi e genera la bozza Outlook."""
        try:
            logger.info("[AutopilotCertWorker] Avvio analisi scadenze (Fallback mode)...")

            engine = CertificatiEngine()
            engine.load_exclusions()
            data = ContabilitaManager.get_certificati_campione_data()

            if not data:
                logger.warning("AutopilotCertWorker: Nessun dato trovato nel database.")
                self.finished_signal.emit(True)
                return

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

            self.finished_signal.emit(True)

        except Exception:
            logger.exception("Errore durante l'analisi automatica certificati (Fallback)")
            self.finished_signal.emit(False)
