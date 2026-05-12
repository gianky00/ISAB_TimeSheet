"""
SyncroJob - Playwright Dettagli OdA Bot
Versione Playwright del bot per lo scarico dei dettagli OdA.
"""

from __future__ import annotations

import concurrent.futures
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from src.bots.base.base_bot import StepStatus
from src.bots.base.playwright_base_bot import PlaywrightBaseBot
from src.bots.portale_fornitori.dettagli_oda.playwright_page import (
    PlaywrightDettagliOdAPage,
)
from src.core.constants import Business
from src.core.oda_manager import OdaManager

if TYPE_CHECKING:
    from src.bots.base.selenium_bot_config import SeleniumBotConfig


class PlaywrightDettagliOdABot(PlaywrightBaseBot):
    """
    Bot per lo scarico dei dettagli degli Ordini di Acquisto (OdA) usando Playwright.
    Supporta sia la ricerca granulare che lo scarico massivo della lista OdA per il database.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Portale"),
        ("supplier", "Selezione Fornitore"),
        ("download", "Download OdA"),
        ("db", "Importazione Database"),
    ]
    """Timeline operativa del bot."""

    @property
    def name(self) -> str:
        """Restituisce il nome visualizzato del bot."""
        return "Dettagli OdA (PW)"

    @property
    def description(self) -> str:
        """Restituisce la descrizione estesa."""
        return "Scarica dettaglio OdA (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce lo schema delle colonne per i dati di input."""
        return [
            {"name": "numero_oda", "label": "Numero OdA", "type": "text"},
            {"name": "numero_contratto", "label": "Numero Contratto", "type": "combo", "options": []},
        ]

    def __init__(
        self,
        config: SeleniumBotConfig,
        data_da: str | None = None,
        data_a: str | None = None,
        fornitore: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Inizializza il bot con configurazione e filtri temporali."""
        super().__init__(config)
        current_year = datetime.now(UTC).astimezone().year

        self.data_da = data_da or f"01.01.{current_year}"
        self.data_a = data_a or f"31.12.{current_year}"
        self.fornitore = fornitore or Business.DEFAULT_SUPPLIER

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Verifica la validità dei parametri e la presenza delle credenziali."""
        if not self.username or not self.password:
            return False, "Credenziali mancanti nelle impostazioni."
        if not self.fornitore:
            return False, "Fornitore non specificato."
        return True, ""

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esegue il ciclo di scarico dettagli con Playwright."""
        self.update_step("login", StepStatus.COMPLETED)

        rows = self._prepare_rows(data)
        self.log(f"[AVVIO] Avvio scarico dettagli (PW) per {len(rows)} OdA...")

        if not self.page:
            return False

        page_obj = PlaywrightDettagliOdAPage(self.page, self.log)
        dest_dir = Path(self.download_path) if self.download_path else Path.home() / "Downloads"

        success = 0
        self.update_step("download", StepStatus.RUNNING)
        for i, row in enumerate(rows):
            res = self._process_single_oda(page_obj, row, i + 1, dest_dir)
            if res:
                success += 1

            callback = getattr(self, "_progress_callback", None)
            if callback:
                callback(i, res, "" if res else "Errore download")

        self.update_step("download", StepStatus.COMPLETED if success == len(rows) else StepStatus.ERROR)
        self.log("ℹ️ Procedura conclusa.")
        return success == len(rows)

    def _prepare_rows(self, data: Any) -> list[dict[str, Any]]:
        """Prepara e normalizza le righe degli OdA da processare."""
        if isinstance(data, dict):
            self.data_da = data.get("data_da", self.data_da)
            self.data_a = data.get("data_a", self.data_a)
            self.fornitore = data.get("fornitore", self.fornitore)
            rows = data.get("rows", [])
        else:
            rows = data

        if not rows:
            self.log("ℹ️ Nessun OdA specificato. Avvio ricerca per lista generale.")
            return [{"numero_oda": "", "numero_contratto": ""}]

        return list(rows)

    def _process_single_oda(
        self,
        page_obj: PlaywrightDettagliOdAPage,
        row: dict[str, Any],
        index: int,
        dest_dir: Path,
    ) -> bool:
        """Gestisce la navigazione, il filtraggio e il download per un singolo ordine."""
        self._check_stop()
        oda = str(row.get("numero_oda", "")).strip()
        contract = str(row.get("numero_contratto", "")).strip()

        self.update_step("nav", StepStatus.RUNNING)
        if not page_obj.navigate_to_dettagli(is_first_row=(index == 1)):
            self.log("❌ Problema nella navigazione.")
            self.update_step("nav", StepStatus.ERROR)
            return False
        self.update_step("nav", StepStatus.COMPLETED)

        self.update_step("supplier", StepStatus.RUNNING)
        if not page_obj.setup_supplier(self.fornitore):
            self.log("❌ Fornitore non selezionabile.")
            self.update_step("supplier", StepStatus.ERROR)
            return False
        self.update_step("supplier", StepStatus.COMPLETED)

        downloaded_path = page_obj.process_oda(oda, contract, self.data_da, self.data_a, dest_dir)

        if downloaded_path:
            if not oda:
                self.update_step("db", StepStatus.RUNNING)
                self._import_oda_to_db(downloaded_path)
                self.update_step("db", StepStatus.COMPLETED)
            return True
        return False

    def _import_oda_to_db(self, downloaded_path: Path) -> None:
        """Innesca l'importazione dei dati Excel nel database Storico OdA."""

        try:
            self.log(f"   Avvio importazione in Storico OdA da {downloaded_path.name}...")
            with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
                future = executor.submit(OdaManager.import_oda_from_excel, str(downloaded_path), None)
                ok, msg, added, _ = future.result()

            if ok:
                self.log(f"✅ Importazione completata: {msg} (Upd/Ins: {added})")
            else:
                self.log(f"⚠️ Errore importazione: {msg}")
        except Exception as e:
            self.log(f"❌ Errore critico durante l'importazione database: {e}")
