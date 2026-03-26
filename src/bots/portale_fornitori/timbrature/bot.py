# mypy: disable-error-code="no-any-unimported, unused-ignore, no-untyped-def, no-untyped-call"
"""
SyncroJob - Timbrature Bot
Bot for accessing Timbrature section using Page Object Model.
"""

from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar

from src.bots.base.base_bot import BaseBot, StepStatus
from src.bots.portale_fornitori.timbrature.pages.timbrature_page import TimbraturePage
from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage


class TimbratureBot(BaseBot):
    """Bot per lo scarico e l'archiviazione automatica delle timbrature dal Portale Fornitori."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Timbrature"),
        ("filter", "Filtraggio Dati"),
        ("download", "Download Report"),
        ("import", "Importazione Database"),
    ]

    @property
    def name(self) -> str:
        """Restituisce il nome del bot."""
        return "Timbrature"

    @property
    def description(self) -> str:
        """Restituisce una descrizione delle funzionalità del bot."""
        return "Scarica e archivia le timbrature dal portale ISAB"

    @staticmethod
    def get_name() -> str:
        """Metodo statico che restituisce il nome del bot."""
        return "Timbrature"

    @staticmethod
    def get_description() -> str:
        """Metodo statico che restituisce la descrizione del bot."""
        return "Scarica e archivia le timbrature dal portale ISAB"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce le colonne per la visualizzazione dei dati."""
        return [
            {"name": "fornitore", "label": "Fornitore", "width": 150},
            {"name": "data_da", "label": "Data Da", "width": 100},
            {"name": "data_a", "label": "Data A", "width": 100},
        ]

    def __init__(self, data_da: str = "", data_a: str = "", fornitore: str = "", **kwargs):  # noqa: ANN003, ANN204
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore
        self.storage = TimbratureStorage()

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Validazione specifica per Timbrature."""
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

        # Extract rows from dict if needed
        rows: list[dict[str, Any]]
        if isinstance(data, dict):
            rows = data.get("rows", [])
            if data.get("fornitore"):
                self.fornitore = str(data.get("fornitore"))
        else:
            rows = data

        if not self.fornitore and not any("fornitore" in row for row in rows):
            return False, "Fornitore non specificato."

        if not self.data_da:
            if rows and rows[0].get("data_da"):
                self.data_da = str(rows[0].get("data_da"))
            else:
                return False, "Data Inizio non specificata."

        return True, ""

    def run(self, data: list[dict[str, Any]]) -> bool:
        """
        Executes the Timbrature workflow: Navigate -> Filter -> Download -> Import.
        """
        self.update_step("login", StepStatus.COMPLETED)

        if data and isinstance(data, list):
            row = data[0]
            self.data_da = row.get("data_da", self.data_da)
            self.data_a = row.get("data_a", self.data_a)
            self.fornitore = row.get("fornitore", self.fornitore)

        self.log(f"🚀 Inizio recupero timbrature per {self.fornitore} ({self.data_da} - {self.data_a})...")

        if not self.driver:
            return False

        page = TimbraturePage(self.driver, self.log, self.download_path)

        # 1. Navigation
        self.update_step("nav", StepStatus.RUNNING)
        if not page.navigate_to_timbrature():
            self.log("❌ Non riesco a raggiungere la sezione Timbrature.")
            self.update_step("nav", StepStatus.ERROR)
            return False
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Filter & Download
        self.update_step("filter", StepStatus.RUNNING)
        if not page.set_filters(self.fornitore, self.data_da, self.data_a):
            self.log("❌ Filtri non applicati correttamente.")
            self.update_step("filter", StepStatus.ERROR)
            return False
        self.update_step("filter", StepStatus.COMPLETED)

        self.update_step("download", StepStatus.RUNNING)
        excel_path = page.download_excel()

        # 3. Process File
        if excel_path:
            self.update_step("download", StepStatus.COMPLETED)
            self.update_step("import", StepStatus.RUNNING)
            self.log("✅ Report scaricato! Sto analizzando i dati...")
            try:
                self.storage.import_excel(excel_path, self.log)
                self.log("💾 Dati salvati nel database con successo.")
                self.update_step("import", StepStatus.COMPLETED)
            except Exception as e:
                self.log(f"❌ Errore durante il salvataggio: {e}")
                self.update_step("import", StepStatus.ERROR)
            finally:
                # Cleanup
                p = Path(excel_path)
                if p.exists():
                    with suppress(Exception):
                        p.unlink()
        else:
            self.log("⚠️ Non ho trovato dati o il download non è partito.")
            self.update_step("download", StepStatus.ERROR)

        self.log("✨ Procedura conclusa.")
        return True

    @staticmethod
    def import_to_db_static(excel_path: str, db_path: Path, log_callback=None):  # noqa: ANN001, ANN205
        """
        Static method for manual import (GUI).
        """
        return TimbratureStorage(db_path).import_excel(excel_path, log_callback)
