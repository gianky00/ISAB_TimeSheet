"""
SyncroJob - OdA Manager
Modulo per la gestione, l'interrogazione e l'aggiornamento del database dello Storico Ordini di Acquisto (OdA).
Gestisce la sincronizzazione tra i file Excel esportati dal portale e il database SQLite locale.
"""

import time
from collections.abc import Callable
from typing import Any

from src.core.database import db_manager
from src.core.database.repositories import OdaRepository
from src.core.logging import get_logger
from src.core.processing.base import Pipeline
from src.core.processing.oda.import_steps import OdaDatabaseSyncStep, OdaExcelReadStep
from src.core.sync_tracker import SyncTracker

logger = get_logger(__name__)


class OdaManager:
    """
    Controller per le operazioni CRUD e di ricerca sullo Storico OdA.
    Centralizza l'accesso ai dati degli ordini, permettendo ricerche testuali complesse.
    """

    _repo = OdaRepository()

    @classmethod
    def init_db(cls) -> None:
        """Inizializza lo schema del database se non esistente."""
        db_manager.init_db()

    @classmethod
    def get_all_oda(cls, search_text: str | None = None) -> list[tuple[Any, ...]]:
        """
        Recupera un elenco di ordini di acquisto dal database.
        Delegato a OdaRepository per la logica di query.
        """
        # Restituiamo tuple per compatibilità con la GUI esistente
        return cls._repo.get_all(search_text, as_objects=False)

    @classmethod
    def import_oda_from_excel(
        cls, file_path: str, progress_callback: Callable[[int, int], None] | None = None
    ) -> tuple[bool, str, int, int]:
        """Importa dati da Excel e sincronizza il DB utilizzando la Pipeline."""
        start_time = time.time()

        pipeline = Pipeline()
        pipeline.add_step(OdaExcelReadStep(progress_callback))
        pipeline.add_step(OdaDatabaseSyncStep())

        context = {"file_path": file_path}

        try:
            result = pipeline.run(context)
            success = result.get("success", False)
            total_added = result.get("total_added", 0)
            total_removed = result.get("total_removed", 0)

            if success:
                duration = time.time() - start_time
                SyncTracker.update_status("oda", total_added, total_removed, duration)

            return (
                success,
                result.get("message", ""),
                total_added,
                total_removed
            )
        except Exception:
            logger.exception("Errore nella pipeline di importazione OdA")
            return False, "Errore critico pipeline", 0, 0
