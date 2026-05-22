"""SyncroJob - Playwright Timbrature Bot.

Versione Playwright del bot per lo scarico delle timbrature.
"""

from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar

from src.bots.base.base_bot import StepStatus
from src.bots.base.playwright_base_bot import PlaywrightBaseBot
from src.bots.portale_fornitori.timbrature.playwright_page import PlaywrightTimbraturePage
from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage


class PlaywrightTimbratureBot(PlaywrightBaseBot):
    """Bot per lo scarico e l'archiviazione automatica delle timbrature usando Playwright."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Timbrature"),
        ("filter", "Filtraggio Dati"),
        ("download", "Download Report"),
        ("import", "Importazione Database"),
    ]
    """Timeline operativa del bot."""

    @property
    def name(self) -> str:
        """Restituisce il nome visualizzato del bot."""
        return "Timbrature (PW)"

    @property
    def description(self) -> str:
        """Restituisce la descrizione estesa."""
        return "Scarica e archivia le timbrature dal portale ISAB (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce lo schema delle colonne per i dati di input."""
        return [
            {"name": "fornitore", "label": "Fornitore", "width": 150},
            {"name": "data_da", "label": "Data Da", "width": 100},
            {"name": "data_a", "label": "Data A", "width": 100},
        ]

    def __init__(self, data_da: str = "", data_a: str = "", fornitore: str = "", **kwargs: Any) -> None:
        """Inizializza il bot con i parametri temporali e il fornitore."""
        kwargs.pop("societa", None)
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore
        self.storage = TimbratureStorage()

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Valida la presenza della data di inizio e del fornitore."""
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

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

    def _normalize_ranges(self, data: list[dict[str, Any]] | dict[str, Any]) -> list[dict[str, Any]]:
        """Normalizza i dati di input in una lista di intervalli temporali.

        Args:
          data: Dati grezzi ricevuti dal worker.

        Returns:
          list: Lista di dizionari contenenti data_da, data_a e fornitore.
        """
        from typing import cast

        rows = data if isinstance(data, list) else data.get("rows", [])
        if rows:
            # Se abbiamo più righe, le trattiamo come una coda di intervalli
            return [
                {
                    "data_da": row.get("data_da", self.data_da),
                    "data_a": row.get("data_a", self.data_a),
                    "fornitore": row.get("fornitore", self.fornitore),
                }
                for row in rows
            ]

        if isinstance(data, dict) and data.get("ranges"):
            # Modalità esplicita multi-range (usata da Crea Database)
            self.fornitore = data.get("fornitore", self.fornitore)
            return cast("list[dict[str, Any]]", data["ranges"])

        # Fallback singolo range (default)
        return [
            {
                "data_da": (data.get("data_da") if isinstance(data, dict) else None) or self.data_da,
                "data_a": (data.get("data_a") if isinstance(data, dict) else None) or self.data_a,
                "fornitore": (data.get("fornitore") if isinstance(data, dict) else None) or self.fornitore,
            }
        ]

    def run(self, data: list[dict[str, Any]] | dict[str, Any]) -> bool:
        """Esegue il workflow completo di recuperòe importazione delle timbrature."""
        self.update_step("login", StepStatus.COMPLETED)

        # Gestione parametri da input (modalità singola o multi-range)
        ranges = self._normalize_ranges(data)

        if not ranges:
            self.log("❌ Nessun intervallo temporale specificato.")
            return False

        if not self.page:
            return False

        page_obj = PlaywrightTimbraturePage(self.page, self.log, self.download_path)

        # 1. Navigation (una sola volta per sessione)
        self.update_step("nav", StepStatus.RUNNING)
        if not page_obj.navigate_to_timbrature():
            self.log("❌ Non riesco a raggiungere la sezione Timbrature.")
            self.update_step("nav", StepStatus.ERROR)
            return False
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Ciclo di scarico per ogni intervallo
        success_count = self._process_download_ranges(page_obj, ranges)

        self.log(f"ℹ️ Procedura conclusa. Periodi scaricati: {success_count}/{len(ranges)}")
        return success_count > 0

    def _process_download_ranges(
        self, page_obj: PlaywrightTimbraturePage, ranges: list[dict[str, Any]]
    ) -> int:
        """Cicla sugli intervalli e gestisce download e importazione.

        Args:
          page_obj: Page Object per l'interazione Playwright.
          ranges: Lista di intervalli da processare.

        Returns:
          int: Numero di periodi scaricati e importati con successo.
        """
        success_count = 0
        total_ranges = len(ranges)

        for i, rng in enumerate(ranges, 1):
            d_da, d_a = rng["data_da"], rng["data_a"]
            forn = rng.get("fornitore", self.fornitore)

            self.log(f"[BATCH {i}/{total_ranges}] Scarico periodo: {d_da} - {d_a}")

            # Filtro
            self.update_step("filter", StepStatus.RUNNING)
            if not page_obj.set_filters(forn, d_da, d_a):
                self.log(f"⚠️ Filtri falliti per {d_da}-{d_a}. Passo al prossimo.")
                self.update_step("filter", StepStatus.ERROR)
                continue
            self.update_step("filter", StepStatus.COMPLETED)

            # Download
            self.update_step("download", StepStatus.RUNNING)
            excel_path = page_obj.download_excel()

            if excel_path:
                self.update_step("download", StepStatus.COMPLETED)
                # Import
                self.update_step("import", StepStatus.RUNNING)
                try:
                    self.storage.import_excel(excel_path, self.log)
                    success_count += 1
                    self.update_step("import", StepStatus.COMPLETED)
                except Exception as e:
                    self.log(f"❌ Errore import {Path(excel_path).name}: {e}")
                    self.update_step("import", StepStatus.ERROR)
                finally:
                    with suppress(Exception):
                        Path(excel_path).unlink()
            else:
                self.log(f"⚠️ Nessun dato trovato per il periodo {d_da} - {d_a}")
                self.update_step("download", StepStatus.ERROR)
        return success_count
