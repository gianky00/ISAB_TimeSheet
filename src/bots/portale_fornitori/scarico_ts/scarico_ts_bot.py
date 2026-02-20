"""
SyncroJob - Scarico TS Bot
Bot for downloading timesheets using Page Object Model.
"""

from pathlib import Path
from typing import Any, ClassVar

from src.bots.base.base_bot import BaseBot, StepStatus
from src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page import ScaricoTSPage


class ScaricaTSBot(BaseBot):
    """
    Bot for automatic timesheet download.
    """

    # Default supplier
    FORNITORE = "KK10608 - COEMI S.R.L."

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Portale"),
        ("filters", "Impostazione Filtri"),
        ("download", "Download Timesheet"),
        ("cleanup", "Chiusura Sessione")
    ]

    @staticmethod
    def get_name() -> str:
        """Restituisce il nome del bot."""
        return "Scarico TS"

    @staticmethod
    def get_description() -> str:
        """Restituisce una descrizione del bot."""
        return "Scarica i timesheet dal portale ISAB"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce le colonne richieste per l'input dati."""
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
        ]

    @property
    def name(self) -> str:
        return "Scarico TS"

    @property
    def description(self) -> str:
        return "Scarica i timesheet dal portale ISAB"

    def __init__(self, data_da: str = "01.01.2025", **kwargs):
        # Clean kwargs for BaseBot
        kwargs.pop("fornitore", None)
        kwargs.pop("data_a", None)
        super().__init__(**kwargs)
        self.data_da = data_da

    def run(self, data: list[dict[str, Any]] | dict[str, Any]) -> bool:
        """
        Executes the download workflow.
        """
        if not self.driver:
            return False

        # Login is already marked as COMPLETED by BaseBot if we reach here
        self.update_step("login", StepStatus.COMPLETED)

        rows: list[dict[str, Any]]
        if isinstance(data, dict):
            rows = data.get("rows", [])
            self.data_da = data.get("data_da", self.data_da)
        else:
            rows = data

        if not rows:
            self.log("Nessun dato da processare")
            return True

        self.update_step("nav", StepStatus.RUNNING)
        page = ScaricoTSPage(self.driver, self.log)

        # 1. Navigation
        if not page.navigate_to_timesheet():
            self.update_step("nav", StepStatus.ERROR)
            return False
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Setup Filters
        self.update_step("filters", StepStatus.RUNNING)
        if not page.setup_filters(self.FORNITORE, self.data_da):
            self.update_step("filters", StepStatus.ERROR)
            return False
        self.update_step("filters", StepStatus.COMPLETED)

        # 3. Process Rows
        self.update_step("download", StepStatus.RUNNING)
        success_count = 0
        # Chrome downloads directly to download_path (if configured)
        download_dir = Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"

        for i, row in enumerate(rows, 1):
            self._check_stop()

            numero_oda = str(row.get("numero_oda", "")).strip()
            posizione_oda = str(row.get("posizione_oda", "")).strip()

            if not numero_oda:
                self.log(f"Riga {i}: Numero OdA mancante, saltata")
                continue

            self.log(f"Riga {i}/{len(rows)}: OdA='{numero_oda}', Pos='{posizione_oda}'")

            if page.search_and_download(numero_oda, posizione_oda, download_dir):
                success_count += 1

        self.update_step("download", StepStatus.COMPLETED)
        self.log("-" * 40)
        self.log(f"Completato: {success_count}/{len(rows)} download riusciti")

        self.update_step("cleanup", StepStatus.RUNNING)
        # Logout is handled by execute() in BaseBot or orchestrator
        self.update_step("cleanup", StepStatus.COMPLETED)
        return success_count == len(rows)
