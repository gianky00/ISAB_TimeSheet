"""
SyncroJob - SafeWork Programmazione Sync Bot
Bot per il download massivo del report di programmazione Excel.
"""

from pathlib import Path
from typing import Any

from selenium.webdriver.common.by import By

from src.bots.base.wait_helpers import poll_for_new_file
from src.bots.safework.base import SafeworkBaseBot


class SafeWorkProgrammazioneSyncBot(SafeworkBaseBot):
    """Bot per scaricare il report Excel delle attività da SafeWork."""

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.downloaded_file: str | None = None

    @staticmethod
    def get_name() -> str:
        return "Sincronizzazione Programmazione"

    @property
    def name(self) -> str:
        return "programmazione_sync"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return []

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esegue il download del report Excel."""
        params = data[0] if data else {}
        requesters = params.get("requesters", [])
        date_start = params.get("date_start")
        date_end = params.get("date_end")

        if not date_start or not date_end:
            return False

        # 1. Navigazione
        self.log("📋 Navigazione in 'Visualizza Attività'...")
        self._attendi_scomparsa_overlay()
        if not self.driver:
            self.log("❌ Driver non inizializzato.")
            return False
            
        self.driver.find_element(By.ID, "topIcon-actHomePage").click()
        self._attendi_scomparsa_overlay()
        self.driver.find_element(By.ID, "sideBar-actVisualizzaAttivita").click()
        self._attendi_scomparsa_overlay()

        # 2. Setup Filtri
        if not self.attivita_page:
            self.log("❌ Pagina Attività non inizializzata.")
            return False
        self.attivita_page.pulisci_pdl()
        self.attivita_page.imposta_date(date_start, date_end)
        self.attivita_page.seleziona_ditta("CO.EMI SRL")

        # 3. Selezione Richiedenti Multipli
        if requesters:
            self.log(f"👥 Selezione di {len(requesters)} richiedenti...")
            # Qui servirebbe una logica di multiselezione nel dropdown
            # Per semplicità usiamo quella della pagina ma ripetuta
            for req in requesters:
                self.attivita_page.seleziona_richiedente(req)

        # 4. Ricerca ed Esportazione
        self.log("🔍 Esecuzione ricerca...")
        self.attivita_page.esegui_ricerca()
        self._attendi_scomparsa_overlay(timeout_secondi=300)

        self.log("📥 Esportazione Excel...")
        files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*") if f.is_file()}

        if self.attivita_page.esporta_excel():
            self.downloaded_file = poll_for_new_file(
                directory=self.download_path,
                files_before=files_before,
                pattern="Programmazione*.xlsx",
                timeout=600,
            )
            if self.downloaded_file:
                self.log(f"✅ Report scaricato: {Path(self.downloaded_file).name}")
                return True

        return False
