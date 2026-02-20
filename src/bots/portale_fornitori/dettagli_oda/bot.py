"""
SyncroJob - Dettagli OdA Bot
"""

from pathlib import Path
from typing import Any, ClassVar

from src.bots.base.base_bot import BaseBot, StepStatus
from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import (
    DettagliOdAPage,
)
from src.core.oda_manager import OdaManager


class DettagliOdABot(BaseBot):
    """Bot per lo scarico dei dettagli degli Ordini di Acquisto (OdA) dal Portale Fornitori."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Portale"),
        ("supplier", "Selezione Fornitore"),
        ("download", "Download OdA"),
        ("db", "Importazione Database")
    ]

    @staticmethod
    def get_name() -> str:
        """Restituisce il nome del bot."""
        return "Dettagli OdA"

    @staticmethod
    def get_description() -> str:
        """Restituisce una descrizione sintetica del bot."""
        return "Scarica dettaglio OdA (o lista generale se OdA vuoto)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Definisce le colonne richieste per l'input dei dati."""
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Numero Contratto", "type": "combo", "options": []},
        ]

    @property
    def name(self) -> str:
        return "Dettagli OdA"

    @property
    def description(self) -> str:
        return "Scarica dettaglio OdA (o lista generale se OdA vuoto)"

    def __init__(
        self,
        data_da: str = "01.01.2024",
        data_a: str = "31.12.2025",
        fornitore: str = "KK10608 - COEMI S.R.L.",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Validazione specifica per Dettagli OdA."""
        # Non chiamiamo super().validate_data(data) perché bloccherebbe se data è vuoto.
        # Verifichiamo manualmente le credenziali e il fornitore.
        if not self.username or not self.password:
            return False, "Credenziali mancanti nelle impostazioni."

        if not self.fornitore:
            return False, "Fornitore non specificato."

        # Il bot può partire anche se data è vuoto (per la lista generale)
        return True, ""

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esegue lo scarico dei dettagli per ogni Ordine di Acquisto fornito."""
        self.update_step("login", StepStatus.COMPLETED)

        rows = self._prepare_rows(data)
        self.log(f"🚀 Avvio scarico dettagli per {len(rows)} OdA...")

        if not self.driver:
            return False

        page = DettagliOdAPage(self.driver, self.log)
        self.update_step("db", StepStatus.RUNNING)
        OdaManager.init_db()
        self.update_step("db", StepStatus.COMPLETED)

        # Chrome downloads directly to download_path (if configured)
        # Source and dest are the same folder - we just rename the downloaded file
        source_dir = Path(self.download_path) if self.download_path else Path.home() / "Downloads"
        dest_dir = source_dir

        success = 0
        self.update_step("download", StepStatus.RUNNING)
        for i, row in enumerate(rows, 1):
            if self._process_single_oda(page, row, i, source_dir, dest_dir):
                success += 1

        self.update_step("download", StepStatus.COMPLETED if success == len(rows) else StepStatus.ERROR)
        self.log("✨ Procedura conclusa.")
        return success == len(rows)

    def _prepare_rows(self, data: Any) -> list[dict[str, Any]]:
        """Prepara la lista di righe da processare."""
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
        result: list[dict[str, Any]] = rows
        return result

    def _process_single_oda(
        self,
        page: DettagliOdAPage,
        row: dict[str, Any],
        index: int,
        source_dir: Path,
        dest_dir: Path,
    ) -> bool:
        """Processa un singolo OdA."""
        self._check_stop()
        oda = str(row.get("numero_oda", "")).strip()
        contract = str(row.get("numero_contratto", "")).strip()

        self.update_step("nav", StepStatus.RUNNING)
        if not page.navigate_to_dettagli(is_first_row=(index == 1)):
            self.log("❌ Problema nella navigazione.")
            self.update_step("nav", StepStatus.ERROR)
            return False
        self.update_step("nav", StepStatus.COMPLETED)

        self.update_step("supplier", StepStatus.RUNNING)
        if not page.setup_supplier(self.fornitore):
            self.log("❌ Fornitore non selezionabile.")
            self.update_step("supplier", StepStatus.ERROR)
            return False
        self.update_step("supplier", StepStatus.COMPLETED)

        downloaded_path = page.process_oda(oda, contract, self.data_da, self.data_a, source_dir, dest_dir)

        if downloaded_path:
            # Se è un ODA Generico (senza numero OdA), importiamo nel DB
            if not oda:
                self.update_step("db", StepStatus.RUNNING)
                self._import_oda_to_db(downloaded_path)
                self.update_step("db", StepStatus.COMPLETED)
            return True
        return False

    def _import_oda_to_db(self, downloaded_path: Path):
        """Helper per l'importazione nel database."""
        try:
            self.log(f"📥 Avvio importazione in Storico OdA da {downloaded_path.name}...")
            ok, msg, added, _ = OdaManager.import_oda_from_excel(str(downloaded_path))
            if ok:
                self.log(f"✅ Importazione completata: {msg} (Upd/Ins: {added})")
            else:
                self.log(f"⚠️ Errore importazione: {msg}")
        except Exception as e:
            self.log(f"❌ Errore critico durante l'importazione database: {e}")
