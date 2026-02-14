"""
SyncroJob - SafeWork Programmazione Bot
Bot modulare per il monitoraggio della programmazione settimanale.
"""

import logging
from typing import Any

from selenium.webdriver.common.by import By

from src.bots.safework.base import SafeworkBaseBot
from src.bots.safework.common.locators import SafeWorkLocators

logger = logging.getLogger(__name__)


class SafeWorkProgrammazioneBot(SafeworkBaseBot):
    """Bot per monitorare i flag TCL/TGO della settimana."""

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.results: list[dict[str, Any]] = []

    @staticmethod
    def get_name() -> str:
        return "Programmazione PDL"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return []

    @property
    def name(self) -> str:
        return "programmazione_pdl"

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esecuzione principale delegata alle Page Objects."""
        params = data[0] if data else {}
        requesters = params.get("requesters", [])
        date_start = params.get("date_start")
        date_end = params.get("date_end")

        if not requesters or not date_start or not date_end:
            return False

        # 1. Navigazione
        self.log("📋 Navigazione in 'Visualizza Attività'...")
        if not self.driver:
            self.log("❌ Driver non inizializzato.")
            return False

        # Uso click_robusto per evitare ElementClickInterceptedException
        self.click_robusto(SafeWorkLocators.HOME_BUTTON)
        self._attendi_scomparsa_overlay()

        self.click_robusto(SafeWorkLocators.VISUALIZZA_ATTIVITA_BUTTON)
        self._attendi_scomparsa_overlay()

        # 2. Setup Filtri
        if not self.attivita_page:
             self.log("❌ Pagina Attività non inizializzata.")
             return False
        self.attivita_page.pulisci_pdl()
        self.attivita_page.imposta_date(str(date_start), str(date_end))
        self.attivita_page.seleziona_ditta("CO.EMI SRL")

        # 3. Ciclo Richiedenti
        self.results = []
        for req in requesters:
            self._check_stop()
            self.log(f"👤 Elaborazione: {req}...")
            if self.attivita_page.seleziona_richiedente(req):
                self.attivita_page.esegui_ricerca()
                self._attendi_scomparsa_overlay()
                self._scrap_risultati(req)

        self.log(f"✨ FINE: Trovati {len(self.results)} PDL con programmazione.")
        return True

    def _scrap_risultati(self, req_input: str):
        """Logica di scraping specifica del bot."""
        if not self.attivita_page:
             self.log("❌ Pagina Attività non inizializzata per lo scraping.")
             return
        rows = self.attivita_page.get_rows()
        if not rows:
            return

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 19:
                continue

            pdl = cells[1].text.strip()
            area = cells[2].text.strip()
            desc = cells[3].text.strip()
            richiedente = cells[18].text.strip()

            # Normalizzazione Richiedente se slittato
            if richiedente.lower() in ("si", "no"):
                for c in cells:
                    if any(n in c.text for n in req_input.split()):
                        richiedente = c.text
                        break

            prog_settimanale = []
            found = False
            for i in range(7):
                idx_tcl = 4 + (i * 2)
                idx_tgo = 5 + (i * 2)
                tcl = self._check_flag(cells[idx_tcl], "_TCL")
                tgo = self._check_flag(cells[idx_tgo], "_TGO")
                if tcl or tgo:
                    found = True
                prog_settimanale.append({"giorno": i + 1, "tcl": tcl, "tgo": tgo})

            if found:
                self.results.append(
                    {
                        "pdl": pdl,
                        "area": area,
                        "descrizione": desc,
                        "richiedente": richiedente,
                        "programmazione": prog_settimanale,
                    }
                )

    def _check_flag(self, cell, pattern: str) -> bool:
        try:
            inp = cell.find_element(By.XPATH, f".//input[contains(@id, '{pattern}')]")
            return bool(inp.get_attribute("title") and str(inp.get_attribute("title")).strip())
        except Exception:
            return False
