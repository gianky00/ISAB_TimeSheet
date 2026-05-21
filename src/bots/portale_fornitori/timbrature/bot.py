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
        Supporta modalità singola o multi-range (per Crea Database).
        """
        self.update_step("login", StepStatus.COMPLETED)

        if not self.driver:
            self.log("❌ Driver non inizializzato")
            return False

        # Normalizzazione intervalli (Copia logica Playwright per coerenza)
        rows = data if isinstance(data, list) else data.get("rows", [])
        ranges = []

        if rows:
            for row in rows:
                ranges.append({
                    "data_da": row.get("data_da", self.data_da),
                    "data_a": row.get("data_a", self.data_a),
                    "fornitore": row.get("fornitore", self.fornitore)
                })
        elif isinstance(data, dict) and data.get("ranges"):
            ranges = data["ranges"]
            self.fornitore = data.get("fornitore", self.fornitore)
        else:
            ranges = [{"data_da": self.data_da, "data_a": self.data_a}]

        if not ranges:
            self.log("❌ Nessun periodo specificato.")
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

            # 2. Ciclo di scarico
            success_count = 0
            for i, rng in enumerate(ranges, 1):
                d_da, d_a = rng["data_da"], rng["data_a"]
                forn = rng.get("fornitore", self.fornitore)

                self.log(f"[BATCH {i}/{len(ranges)}] Scarico periodo: {d_da} - {d_a}")
                self.update_step("filter", StepStatus.RUNNING)

                excel_path = page.download_timbrature(forn, d_da, d_a, self.download_path)

                if excel_path:
                    self.update_step("filter", StepStatus.COMPLETED)
                    self.update_step("download", StepStatus.COMPLETED)

                    # 3. Importazione DB
                    self.update_step("import", StepStatus.RUNNING)
                    if self.storage.import_excel(excel_path, self.log):
                        success_count += 1
                        self.update_step("import", StepStatus.COMPLETED)
                    else:
                        self.update_step("import", StepStatus.ERROR)

                    with suppress(Exception):
                        Path(excel_path).unlink()
                else:
                    self.log(f"⚠️ Download fallito per {d_da} - {d_a}")
                    self.update_step("filter", StepStatus.ERROR)

            self.log(f"✅ Completato. Periodi salvati: {success_count}/{len(ranges)}")

        except Exception as e:
            self.log(f"❌ Errore imprevisto bot: {e}")
            return False
        else:
            return success_count > 0

    @staticmethod
    def import_to_db_static(excel_path: str, db_path: Path, log_callback: Any = None) -> Any:
        """
        Static method for manual import (GUI).
        """
        return TimbratureStorage(db_path).import_excel(excel_path, log_callback)
