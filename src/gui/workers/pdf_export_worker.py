"""SyncroJob - PDF Export Worker.

Worker asincrono per l'esportazione di report PDF.
Evita il freeze della GUI durante la generazione di documenti complessi con paginazione.
"""

import logging
from typing import Any

from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)


class PDFExportWorker(QThread):
    """Worker che delega l'esportazione PDF a un thread secondario.

    Nota: Sebbene QPdfWriter richieda un QPainter (che di solito è Main Thread),
    la preparazione dei dati e dei documenti può essere asincrona.
    """

    finished_signal = Signal(bool, str)  # (success, message)

    def __init__(self, exporter_instance: Any, file_path: str) -> None:
        """Inizializza il worker.

        Args:
          exporter_instance: Istanza di CertificatiPdfExporter o simile.
          file_path: Percorso di salvataggio.
        """
        super().__init__()
        self.exporter = exporter_instance
        self.file_path = file_path

    def run(self) -> None:
        """Esegue l'esportazione in background."""
        try:
            logger.info(f"[PDFExportWorker] Avvio generazione PDF: {self.file_path}")
            # L'exporter deve essere progettato per essere thread-safe (non manipolare widget UI direttamente)
            # Nel nostro caso, l'exporter legge dati già estratti o passa riferimenti sicuri.
            success, message = self.exporter.export(self.file_path)
            self.finished_signal.emit(success, message)
        except Exception as e:
            logger.exception("Errore durante l'esportazione asincrona PDF")
            self.finished_signal.emit(False, str(e))
