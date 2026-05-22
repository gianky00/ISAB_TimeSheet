"""SyncroJob - Certificati Worker.

Worker asincrono per il caricamento e raggruppamento dei certificati campione.
Evita il freeze della GUI durante l'elaborazione di migliaia di record.
"""

import logging

from PySide6.QtCore import QThread, Signal

from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.contabilita_manager import ContabilitaManager

logger = logging.getLogger(__name__)


class CertificatiWorker(QThread):
    """Worker per il caricamento asincrono dei certificati.

    Delega l'elaborazione pesante (SQL, Raggruppamento, Priorità) a un thread secondario.

    Inizializza il worker.

    Args:
      engine: Istanza di CertificatiEngine da utilizzare per il raggruppamento.

    Attributes:
        error_signal: Segnale o attributo della classe.
        finished_signal: Segnale o attributo della classe.
    """

    finished_signal = Signal(list)  # Restituisce la lista di gruppi prioritizzati
    error_signal = Signal(str)

    def __init__(self, engine: CertificatiEngine) -> None:
        super().__init__()
        self.engine = engine

    def run(self) -> None:
        """Esegue l'estrazione e l'elaborazione dei dati."""
        try:
            logger.info("[CertificatiWorker] Inizio caricamento certificati...")

            # 1. Recupero dati dal DB (Sincrono sicuro in thread)
            data = ContabilitaManager.get_certificati_campione_data()

            # 2. Raggruppamento e prioritizzazione delegata all'engine
            id_groups = self.engine.group_data_by_id_coemi(data)
            prioritized_groups = self.engine.prepare_groups_with_priority(id_groups)

            # 3. Ordinamento finale per priorità (scadenza)
            import operator

            prioritized_groups.sort(key=operator.itemgetter("priority"))

            logger.info(f"[CertificatiWorker] Elaborati {len(prioritized_groups)} gruppi di certificati.")
            self.finished_signal.emit(prioritized_groups)

        except Exception as e:
            logger.exception("[CertificatiWorker] Errore critico nel caricamento certificati")
            self.error_signal.emit(str(e))
