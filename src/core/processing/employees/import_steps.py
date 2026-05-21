"""Passaggi di elaborazione per l'importazione dell'anagrafica dipendenti."""

import csv
from pathlib import Path
from typing import Any

from src.core.database.repositories import EmployeeRepository
from src.core.processing.base import ProcessingStep
from src.models import EmployeeRecord


class EmployeeCsvReadStep(ProcessingStep):
    """Passaggio per la lettura e il parsing del file CSV dei dipendenti."""

    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la lettura del file CSV."""
        csv_path = context.get("file_path")
        if not csv_path:
            raise ValueError("file_path mancante nel contesto")

        path = Path(csv_path)
        if not path.exists():
            context["success"] = False
            context["message"] = f"File CSV non trovato: {csv_path}"
            return

        employees_to_sync = []
        try:
            with path.open("r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=";")
                if reader.fieldnames:
                    reader.fieldnames = [name.strip() for name in reader.fieldnames]

                for row in reader:
                    id_val = row.get("id_risorsa") or row.get("ID")
                    id_risorsa = int(id_val) if id_val and str(id_val).isdigit() else None

                    emp = EmployeeRecord(
                        id_risorsa=id_risorsa,
                        cognome=row.get("Cognome", "").upper(),
                        nome=row.get("Nome", "").upper(),
                        data_nascita=row.get("Data_nascita"),
                        codice_fiscale=row.get("Codice_fiscale", "").upper(),
                        badge=row.get("Badge", ""),
                        data_assunzione=row.get("Data_assunzione"),
                        monitoraggio_attivo=1,
                    )
                    employees_to_sync.append(emp)

            context["employees"] = employees_to_sync
            context["success"] = True
        except Exception as e:
            context["success"] = False
            context["message"] = f"Errore lettura CSV: {e}"


class EmployeeDatabaseSyncStep(ProcessingStep):
    """Passaggio per la sincronizzazione dei dipendenti con il database."""

    def __init__(self, repository: EmployeeRepository | None = None) -> None:
        """Inizializza il passaggio con il repository specificato."""
        self.repo = repository or EmployeeRepository()

    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la sincronizzazione del database."""
        if not context.get("success"):
            return

        employees = context.get("employees", [])
        added_count = 0
        updated_count = 0

        for emp in employees:
            # Sincronizzazione basata su ID o Badge (logica semplificata dal repository)
            # Se ha ID risorsa, proviamo ad aggiornare
            if emp.id_risorsa:
                # Nota: la logica originale in EmployeeManager faceva check su ID
                if self.repo.save(emp):
                    updated_count += 1
            else:
                # Proviamo a vedere se esiste per badge prima di inserire
                existing = self.repo.get_by_badge(emp.badge)
                if existing:
                    emp.id_risorsa = existing.id_risorsa
                    self.repo.save(emp)
                    updated_count += 1
                else:
                    self.repo.save(emp)
                    added_count += 1

        context["added_count"] = added_count
        context["updated_count"] = updated_count
        context["total_processed"] = len(employees)
