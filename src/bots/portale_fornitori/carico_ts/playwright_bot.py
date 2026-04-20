# mypy: disable-error-code="no-untyped-call"
"""
SyncroJob - Playwright Carico TS Bot
Versione Playwright del bot per il caricamento dei timesheet.
"""

from typing import Any, ClassVar

from src.bots.base.base_bot import StepStatus
from src.bots.base.playwright_base_bot import PlaywrightBaseBot
from src.bots.portale_fornitori.carico_ts.playwright_page import PlaywrightCaricoTSPage
from src.core.constants import Business


class PlaywrightCaricoTSBot(PlaywrightBaseBot):
    """
    Bot per l'estrazione e il caricamento dei dati Timesheet usando Playwright.
    Automatizza la selezione dell'OdA e il caricamento massivo delle ore lavorate.
    """

    FORNITORE = Business.DEFAULT_SUPPLIER
    """Fornitore predefinito per il caricamento."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Portale"),
        ("supplier", "Selezione Fornitore"),
        ("extract", "Estrazione OdA"),
        ("cleanup", "Chiusura Sessione"),
    ]
    """Timeline operativa del bot."""

    @property
    def name(self) -> str:
        """Restituisce il nome visualizzato del bot."""
        return "Carico TS (PW)"

    @property
    def description(self) -> str:
        """Restituisce la descrizione estesa."""
        return "Caricamento automatico timesheet (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce lo schema delle colonne per la visualizzazione tabellare."""
        return [
            {"name": "numero_oda", "label": "Numero OdA", "type": "text"},
            {"name": "codice_fiscale", "label": "Codice Fiscale", "type": "text"},
            {"name": "cognome", "label": "Cognome", "type": "text"},
            {"name": "nome", "label": "Nome", "type": "text"},
            {"name": "mese", "label": "Mese", "type": "text"},
            {"name": "anno", "label": "Anno", "type": "text"},
            {"name": "g1", "label": "G 1", "type": "text"},
            {"name": "g2", "label": "G 2", "type": "text"},
            {"name": "g3", "label": "G 3", "type": "text"},
            {"name": "g4", "label": "G 4", "type": "text"},
            {"name": "g5", "label": "G 5", "type": "text"},
            {"name": "g6", "label": "G 6", "type": "text"},
            {"name": "g7", "label": "G 7", "type": "text"},
            {"name": "g8", "label": "G 8", "type": "text"},
            {"name": "g9", "label": "G 9", "type": "text"},
            {"name": "gt", "label": "G T", "type": "text"},
        ]

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Valida la presenza del numero OdA nei dati di input."""
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

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esegue il workflow principale di caricamento TS con Playwright."""
        self.update_step("login", StepStatus.COMPLETED)

        rows = data if isinstance(data, list) else data.get("rows", [])
        row = rows[0]
        oda = str(row.get("numero_oda", "")).strip()

        self.log(f"Avvio estrazione (PW) Carico TS per OdA: {oda}")

        if not self.page:
            return False

        self.update_step("nav", StepStatus.RUNNING)
        page_obj = PlaywrightCaricoTSPage(self.page, self.log)

        if not page_obj.navigate():
            self.update_step("nav", StepStatus.ERROR)
            return False
        self.update_step("nav", StepStatus.COMPLETED)

        self.update_step("supplier", StepStatus.RUNNING)
        if not page_obj.select_supplier(self.FORNITORE):
            self.update_step("supplier", StepStatus.ERROR)
            return False
        self.update_step("supplier", StepStatus.COMPLETED)

        self.update_step("extract", StepStatus.RUNNING)
        if page_obj.process_oda(oda):
            self.log("[OK] OdA estratta con successo.")
            self.update_step("extract", StepStatus.COMPLETED)
            self.update_step("cleanup", StepStatus.RUNNING)
            self.update_step("cleanup", StepStatus.COMPLETED)
            return True

        self.update_step("extract", StepStatus.ERROR)
        return False
