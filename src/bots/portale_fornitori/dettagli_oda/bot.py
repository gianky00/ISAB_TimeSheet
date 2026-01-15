"""
SyncroJob - Dettagli OdA Bot
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

from src.bots.base import BaseBot
from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import (
    DettagliOdAPage,
)


class DettagliOdABot(BaseBot):
    """Bot per lo scarico dei dettagli degli Ordini di Acquisto (OdA) dal Portale Fornitori."""
    @staticmethod
    def get_name() -> str:
        """Restituisce il nome del bot."""
        return "Dettagli OdA"

    @staticmethod
    def get_description() -> str:
        """Restituisce una descrizione sintetica del bot."""
        return "Scarica dettaglio OdA (o lista generale se OdA vuoto)"

    @staticmethod
    def get_columns() -> list:
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

    def validate_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validazione specifica per Dettagli OdA."""
        # Non chiamiamo super().validate_data(data) perché bloccherebbe se data è vuoto.
        # Verifichiamo manualmente le credenziali e il fornitore.
        if not self.username or not self.password:
            return False, "Credenziali mancanti nelle impostazioni."

        if not self.fornitore:
            return False, "Fornitore non specificato."

        # Il bot può partire anche se data è vuoto (per la lista generale)
        return True, ""

    def run(self, data: List[Dict[str, Any]]) -> bool:
        if isinstance(data, dict):
            rows = data.get("rows", [])
            self.data_da = data.get("data_da", self.data_da)
            self.data_a = data.get("data_a", self.data_a)
            self.fornitore = data.get("fornitore", self.fornitore)
        else:
            rows = data

        # Se non ci sono righe, aggiungiamo una riga vuota per far partire la ricerca generale
        if not rows:
            self.log("ℹ️ Nessun OdA specificato. Avvio ricerca per lista generale.")
            rows = [{"numero_oda": "", "numero_contratto": ""}]

        self.log(f"🚀 Avvio scarico dettagli per {len(rows)} OdA...")
        
        if not self.driver:
            return False
        assert self.driver

        page = DettagliOdAPage(self.driver, self.log)

        # Define source (System Downloads) and destination (Configured Path)
        source_dir = Path.home() / "Downloads"
        dest_dir = Path(self.download_path) if self.download_path else source_dir

        success = 0

        for i, row in enumerate(rows, 1):
            self._check_stop()
            oda = str(row.get("numero_oda", "")).strip()
            contract = str(row.get("numero_contratto", "")).strip()

            if not page.navigate_to_dettagli(is_first_row=(i == 1)):
                self.log("❌ Problema nella navigazione.")
                continue
            if not page.setup_supplier(self.fornitore):
                self.log("❌ Fornitore non selezionabile.")
                continue

            if page.process_oda(
                oda, contract, self.data_da, self.data_a, source_dir, dest_dir
            ):
                success += 1

            time.sleep(1)

        self.log("✨ Procedura conclusa.")
        return success == len(rows)
