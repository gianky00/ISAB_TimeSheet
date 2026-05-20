"""
SyncroJob - Playwright SafeWork Programmazione Sync Bot
Versione Playwright del bot per il download massivo del report di programmazione Excel.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from src.bots.base.base_bot import StepStatus
from src.bots.safework.pages.playwright_visualizza_attivita_page import (
    PlaywrightVisualizzaAttivitaPage,
)
from src.bots.safework.playwright_base import PlaywrightSafeworkBaseBot

if TYPE_CHECKING:
    from src.bots.base.selenium_bot_config import SeleniumBotConfig


class PlaywrightSafeWorkProgrammazioneSyncBot(PlaywrightSafeworkBaseBot):
    """
    Bot per il download massivo delle attività SafeWork (Syncro) usando Playwright.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login SafeWork"),
        ("nav", "Navigazione Attività"),
        ("filter", "Configurazione Filtri"),
        ("search", "Ricerca ed Esportazione"),
    ]

    def __init__(
        self,
        config: SeleniumBotConfig,
        account_type: str = "Esecutore",
    ) -> None:
        super().__init__(config, account_type=account_type)
        self.downloaded_file: str | None = None
        self.attivita_page: PlaywrightVisualizzaAttivitaPage | None = None

    @property
    def name(self) -> str:
        return "Sincronizzazione Programmazione (PW)"

    @property
    def description(self) -> str:
        return "Download massivo report attività SafeWork (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Nessun input a righe: il bot usa solo i filtri data/richiedenti."""
        return []

    def run(self, data: list[dict[str, Any]] | dict[str, Any]) -> bool:
        """Esegue download massivo report e sincronizzazione sul database locale."""
        self.update_step("login", StepStatus.COMPLETED)

        params = data[0] if isinstance(data, list) and data else data if isinstance(data, dict) else {}
        requesters = params.get("requesters", [])
        date_start = params.get("date_start")
        date_end = params.get("date_end")

        if not date_start or not date_end:
            return False

        if not self.page:
            return False

        self.attivita_page = PlaywrightVisualizzaAttivitaPage(self.page, self.log)

        # 1. Navigazione
        self.update_step("nav", StepStatus.RUNNING)
        self.log("   Navigazione in 'Visualizza Attività'...")

        self.page.click("#topIcon-actHomePage")
        self._attendi_scomparsa_overlay()
        self.page.click("#sideBar-actVisualizzaAttivita")
        self._attendi_scomparsa_overlay()
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Setup Filtri
        self.update_step("filter", StepStatus.RUNNING)
        self.attivita_page.pulisci_pdl()
        self.attivita_page.imposta_date(date_start, date_end)
        self.attivita_page.seleziona_ditta("CO.EMI SRL")
        self.update_step("filter", StepStatus.COMPLETED)

        # 3. Selezione Richiedenti
        if requesters:
            self.log(f"   Selezione di {len(requesters)} richiedenti...")
            self.attivita_page.seleziona_richiedente(requesters)

        # 4. Ricerca ed Esportazione
        self.update_step("search", StepStatus.RUNNING)
        self.log("[CERCA] Esecuzione ricerca...")
        self.attivita_page.esegui_ricerca()
        self._attendi_scomparsa_overlay()

        self.log("   Esportazione Excel...")
        try:
            # Usa il doppio del timeout globale per l'esportazione pesante
            download_timeout_ms = self.config.timeout * 2 * 1000
            with self.page.expect_download(timeout=download_timeout_ms) as download_info:
                if self.attivita_page.esporta_excel():
                    download = download_info.value
                    dest = Path(self.download_path) / download.suggested_filename
                    download.save_as(str(dest))
                    self.downloaded_file = str(dest)
                    self.log(f"✅ Report scaricato: {dest.name}")
                    self.update_step("search", StepStatus.COMPLETED)
                    return True
        except Exception as e:
            self.log(f"❌ Errore download Excel: {e}")

        self.update_step("search", StepStatus.ERROR)
        return False
