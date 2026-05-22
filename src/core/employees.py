"""Modulo Employees."""

import sqlite3
import time
from typing import Any, cast

from src.core.database import db_manager
from src.core.database.repositories import EmployeeRepository
from src.core.logging import get_logger
from src.core.sync_tracker import SyncTracker
from src.models import EmployeeRecord

logger = get_logger(__name__)


class EmployeeManager:
    """Gestisce la logica di business per i dipendenti, facendo da interfaccia.

    tra la GUI/Bot e il Database SQLite.
    Delegato al nuovo EmployeeRepository per l'accesso ai dati.

    Inizializza la classe.
    """

    def __init__(self, db_manager_instance: Any = None) -> None:
        self.db = db_manager_instance or db_manager
        self._repo = EmployeeRepository(self.db)

    def get_all_employees(self, active_only: bool = True) -> list[dict[str, Any]]:
        """Restituisce tutti i dipendenti dal database come lista di dizionari."""
        results = self._repo.get_all(active_only, as_objects=False)
        # Type narrowing for mypy
        return [r for r in results if isinstance(r, dict)]

    def get_employee_by_badge(self, badge: str) -> sqlite3.Row | None:
        """Cerca un dipendente per numero di badge."""
        # Nota: il repository restituisce oggetti o dict. Per compatibilità Row, facciamo query qui o cast
        query = "SELECT * FROM dipendenti WHERE badge = ?"
        results = self.db.execute_query(self.db.DB_DIPENDENTI, query, (badge,))
        return results[0] if results else None

    def add_employee(self, employee_data: dict[str, Any]) -> bool:
        """Aggiunge un nuovo dipendente tramite repository."""
        # Convertiamo dict in Model
        emp = EmployeeRecord(
            id_risorsa=employee_data.get("id_risorsa"),
            cognome=employee_data["cognome"].upper(),
            nome=employee_data["nome"].upper(),
            badge=employee_data.get("badge", ""),
            codice_fiscale=employee_data.get("codice_fiscale", "").upper(),
            data_assunzione=employee_data.get("data_assunzione"),
            monitoraggio_attivo=1,
            data_nascita=employee_data.get("data_nascita"),
        )
        return self._repo.save(emp)

    def update_employee(self, id_risorsa: int, data: dict[str, Any]) -> bool:
        """Aggiorna i dati di un dipendente esistente tramite repository."""
        # Recuperiamo l'attuale per non perdere dati non presenti nel dict 'data'
        query = "SELECT * FROM dipendenti WHERE id_risorsa = ?"
        current = self.db.execute_query(self.db.DB_DIPENDENTI, query, (id_risorsa,))
        if not current:
            return False

        current_data = dict(current[0])
        current_data.update(data)

        emp = EmployeeRecord(**current_data)
        return self._repo.save(emp)

    def import_from_csv(self, csv_path: str) -> int:
        """Importa/Sincronizza i dipendenti dal CSV al DB tramite Pipeline.

        Ritorna il numero di record processati.
        """
        from src.core.processing.base import Pipeline  # noqa: PLC0415
        from src.core.processing.employees.import_steps import (  # noqa: PLC0415
            EmployeeCsvReadStep,
            EmployeeDatabaseSyncStep,
        )

        start_time = time.time()

        pipeline = Pipeline()
        pipeline.add_step(EmployeeCsvReadStep())
        pipeline.add_step(EmployeeDatabaseSyncStep(self._repo))

        context = {"file_path": csv_path}

        try:
            result = pipeline.run(context)
            if not result.get("success"):
                return 0

            total_added = cast("int", result.get("added_count", 0))
            total_processed = cast("int", result.get("total_processed", 0))

            duration = time.time() - start_time
            SyncTracker.update_status("dipendenti", total_added, 0, duration)

            logger.info(f"Importazione completata: {total_processed} processati ({total_added} nuovi).")
        except Exception:
            logger.exception("Errore durante l'importazione CSV tramite Pipeline")
            return 0
        else:
            return total_processed


# Istanza globale
employee_manager = EmployeeManager()
