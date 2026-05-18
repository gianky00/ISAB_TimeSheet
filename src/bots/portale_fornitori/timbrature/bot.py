"""
SyncroJob - Timbrature Bot
Bot for accessing Timbrature section using Page Object Model.
"""

from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

from src.bots.base.base_bot import StepStatus
from src.bots.base.selenium_base_bot import SeleniumBaseBot
from src.bots.base.selenium_bot_config import SeleniumBotConfig
from src.core.constants import Business

from .pages.timbrature_page import TimbraturePage
from .storage import TimbratureStorage


class TimbratureBot(SeleniumBaseBot):
    """
    Bot per lo scarico automatico delle timbrature dipendenti.
    Semplificato e uniformato al nuovo pattern asincrono.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale"),
        ("nav", "Navigazione Timbrature"),
        ("filter", "Impostazione Filtri"),
        ("download", "Scarico Excel"),
        ("import", "Importazione DB"),
    ]

    def __init__(  # noqa: PLR0913
        self,
        username: str | None = None,
        password: str | None = None,
        config: SeleniumBotConfig | None = None,
        data_da: str | None = None,
        data_a: str | None = None,
        fornitore: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Inizializza il bot Timbrature."""
        super().__init__(username, password, config)
        current_year = datetime.now(UTC).year
        self.data_da = data_da or kwargs.get("data_da") or f"01.01.{current_year}"
        self.data_a = data_a or kwargs.get("data_a") or f"31.12.{current_year}"
        self.fornitore = fornitore or kwargs.get("fornitore") or Business.DEFAULT_SUPPLIER
        self.storage = TimbratureStorage()

    @staticmethod
    def get_name() -> str:
        """Restituisce il nome visualizzato del bot."""
        return "Timbrature"

    @property
    def name(self) -> str:
        """Restituisce l'identificativo tecnico del bot."""
        return "timbrature"

    @property
    def description(self) -> str:
        """Restituisce la descrizione del bot."""
        return "Scarica e archivia le timbrature dal portale ISAB"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce le colonne richieste (nessuna)."""
        return []

    def run(self, data: list[dict[str, Any]] | dict[str, Any]) -> bool:
        """
        Workflow principale per lo scarico delle timbrature.
        """
        self.update_step("login", StepStatus.COMPLETED)

        if not self.driver:
            self.log("❌ Driver non inizializzato")
            return False

        try:
            # 1. Navigazione
            self.update_step("nav", StepStatus.RUNNING)
            page = TimbraturePage(self.driver, self.log)
            if not page.navigate_to_timbrature():
                self.log("❌ Impossibile raggiungere la sezione Timbrature")
                self.update_step("nav", StepStatus.ERROR)
                return False
            self.update_step("nav", StepStatus.COMPLETED)

            # 2. Filtro e Download
            self.update_step("filter", StepStatus.RUNNING)
            self.log(f"   Filtro: {self.fornitore} dal {self.data_da} al {self.data_a}")
            excel_path = page.download_timbrature(
                self.fornitore, self.data_da, self.data_a, self.download_path
            )
            if not excel_path:
                self.log("❌ Download fallito o nessun dato trovato.")
                self.update_step("filter", StepStatus.ERROR)
                return False
            self.update_step("filter", StepStatus.COMPLETED)
            self.update_step("download", StepStatus.COMPLETED)

            # 3. Importazione DB
            self.update_step("import", StepStatus.RUNNING)
            self.log(f"   Importazione dati da: {Path(excel_path).name}")
            success = self.storage.import_excel(excel_path, self.log)

            if not success:
                self.log("⚠️ Importazione fallita (nessun dato o errore)")
                self.update_step("import", StepStatus.ERROR)
                return False

            self.log("✅ Importazione completata con successo")
            self.update_step("import", StepStatus.COMPLETED)
            with suppress(Exception):
                Path(excel_path).unlink()

        except Exception as e:
            self.log(f"❌ Errore imprevisto bot: {e}")
            return False
        else:
            return True

    @staticmethod
    def import_to_db_static(excel_path: str, db_path: Path, log_callback: Any = None) -> Any:
        """
        Static method for manual import (GUI).
        """
        return TimbratureStorage(db_path).import_excel(excel_path, log_callback)
