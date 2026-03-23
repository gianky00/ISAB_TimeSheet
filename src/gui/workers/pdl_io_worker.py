"""
SyncroJob - Pdl IO Worker
Thread worker per l'esportazione asincrona dei PDL in Excel.
"""

import logging

import pandas as pd
from PyQt6.QtCore import QThread, pyqtSignal

from src.core.pdl.pdl_dto import PdlRowDTO

logger = logging.getLogger(__name__)


class PdlIOWorker(QThread):
    """Worker per l'esportazione asincrona dei dati PDL."""

    finished_signal = pyqtSignal(bool, str, str)  # success, message, file_path

    def __init__(self, file_path: str, data: list[PdlRowDTO], headers: list[str], parent=None):  # noqa: ANN001, ANN204
        super().__init__(parent)
        self.file_path = file_path
        self.data = data
        self.headers = headers

    def run(self):  # noqa: ANN201
        """Esegue l'esportazione in background."""
        try:
            if not self.data:
                self.finished_signal.emit(False, "Nessun dato da esportare", "")
                return

            # Estrazione dati dai DTO per il DataFrame
            raw_rows = [r.to_full_list() for r in self.data]
            df = pd.DataFrame(raw_rows, columns=self.headers)
            df.to_excel(self.file_path, index=False)

            self.finished_signal.emit(True, "Esportazione completata con successo", self.file_path)

        except Exception as e:
            logger.error(f"PdlIOWorker Error: {e}")  # noqa: TRY400
            self.finished_signal.emit(False, str(e), "")
