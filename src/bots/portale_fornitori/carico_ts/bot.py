"""
SyncroJob - Carico TS Bot
Bot for Carico TS using POM.
"""

from typing import Any, Dict, List, Tuple

from src.bots.base import BaseBot
from src.bots.portale_fornitori.carico_ts.pages.carico_ts_page import CaricoTSPage


class CaricoTSBot(BaseBot):
    """Bot per l'estrazione e il caricamento dei dati Timesheet sul Portale Fornitori."""
    FORNITORE = "KK10608 - COEMI S.R.L."

    @staticmethod
    def get_name() -> str:
        """Restituisce il nome del bot."""
        return "Carico TS"

    @staticmethod
    def get_description() -> str:
        """Restituisce una descrizione sintetica del bot."""
        return "Caricamento automatico timesheet"

    @staticmethod
    def get_columns() -> list:
        """Definisce le colonne richieste per l'input dei dati."""
        # Full list from original code
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Codice Fiscale", "type": "text"},
            {"name": "Cognome", "type": "text"},
            {"name": "Nome", "type": "text"},
            {"name": "Mese", "type": "text"},
            {"name": "Anno", "type": "text"},
            {"name": "G 1", "type": "text"},
            {"name": "G 2", "type": "text"},
            {"name": "G 3", "type": "text"},
            {"name": "G 4", "type": "text"},
            {"name": "G 5", "type": "text"},
            {"name": "G 6", "type": "text"},
            {"name": "G 7", "type": "text"},
            {"name": "G 8", "type": "text"},
            {"name": "G 9", "type": "text"},
            {"name": "G T", "type": "text"},
        ]

    @property
    def name(self) -> str:
        return "Carico TS"

    @property
    def description(self) -> str:
        return "Caricamento automatico timesheet"

    def validate_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validazione specifica per Carico TS."""
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

        rows = data if isinstance(data, list) else data.get("rows", [])
        if not rows:
            return False, "Nessuna riga di dati fornita."

        first_row = rows[0]
        if not first_row.get("numero_oda"):
            return False, "Numero OdA mancante nella prima riga."

        return True, ""

    def run(self, data: List[Dict[str, Any]]) -> bool:
        # Il driver è garantito da execute()
        rows = data if isinstance(data, list) else data.get("rows", [])

        # Original logic: process ONLY the first row
        row = rows[0]
        oda = str(row.get("numero_oda", "")).strip()

        self.log(f"Avvio estrazione Carico TS per OdA: {oda}")

        if not self.driver:
            return False
        assert self.driver

        page = CaricoTSPage(self.driver, self.log)

        if not page.navigate():
            return False

        if not page.select_supplier(self.FORNITORE):
            return False

        if page.process_oda(oda):
            self.log("✅ OdA estratta con successo.")
            return True

        return False
