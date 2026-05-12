"""
SyncroJob - Oda IO Worker
Thread worker per l'importazione ed esportazione asincrona dei dati OdA.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from PySide6.QtCore import QObject, QThread, Signal

from src.core.oda_manager import OdaManager

logger = logging.getLogger(__name__)


class OdaIOWorker(QThread):
    """Worker per operazioni pesanti di I/O su file Excel per gli OdA."""

    finished_signal = Signal(bool, str, dict)  # success, message, stats

    def __init__(
        self,
        mode: str,
        file_path: str,
        extra_data: dict[str, Any] | None = None,
        parent: QObject | None = None,
    ) -> None:
        """
        Inizializza il worker.

        Args:
          mode: 'import' o 'export'.
          file_path: Percorso del file Excel.
          extra_data: Dati per l'export (header, query, ecc).
          parent: Oggetto padre (PyQt).
        """
        super().__init__(parent)
        self.mode = mode
        self.file_path = file_path
        self.extra_data = extra_data or {}

    def run(self) -> None:
        """Esegue l'operazione richiesta in background."""
        try:
            if self.mode == "import":
                self._run_import()
            elif self.mode == "export":
                self._run_export()
        except Exception as e:
            logger.exception(f"OdaIOWorker Error ({self.mode})")
            self.finished_signal.emit(False, str(e), {})

    def _run_import(self) -> None:
        """Esegue l'importazione Excel nel DB."""
        success, message, added, removed = OdaManager.import_oda_from_excel(self.file_path)
        stats = {"added": added, "removed": removed}
        self.finished_signal.emit(success, message, stats)

    def _run_export(self) -> None:
        """Esegue l'esportazione dal DB a Excel."""
        search_text = self.extra_data.get("search_text", "")
        headers = self.extra_data.get("headers", [])

        raw_data = OdaManager.get_all_oda(search_text)
        if not raw_data:
            self.finished_signal.emit(False, "Nessun dato da esportare", {})
            return

        df = pd.DataFrame(raw_data, columns=headers)
        df.to_excel(self.file_path, index=False)

        self.finished_signal.emit(True, "Esportazione completata", {"path": self.file_path})
