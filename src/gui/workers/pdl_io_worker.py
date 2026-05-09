"""
SyncroJob - Pdl IO Worker
Thread worker per l'esportazione asincrona dei PDL in Excel.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pandas as pd
from PySide6.QtCore import QObject, QThread, Signal

if TYPE_CHECKING:
    from src.core.pdl.pdl_dto import PdlRowDTO

logger = logging.getLogger(__name__)


class PdlIOWorker(QThread):
    """Worker per l'esportazione asincrona dei dati PDL."""

    finished_signal = Signal(bool, str, str)  # success, message, file_path

    def __init__(
        self, file_path: str, data: list[PdlRowDTO], headers: list[str], parent: QObject | None = None
    ) -> None:
        """
        Inizializza il worker.

        Args:
          file_path: Percorso del file Excel di destinazione.
          data: Lista di DTO da esportare.
          headers: Intestazioni delle colonne.
          parent: Oggetto padre (PyQt).
        """
        super().__init__(parent)
        self.file_path = file_path
        self.data = data
        self.headers = headers

    def run(self) -> None:
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
            logger.exception("PdlIOWorker Error", exc=e)
            self.finished_signal.emit(False, str(e), "")
