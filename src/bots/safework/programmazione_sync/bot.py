"""
SyncroJob - SafeWork Programmazione Sync Bot
Bot per il download massivo del report di programmazione Excel.
"""

from pathlib import Path
from typing import Any, ClassVar

from selenium.webdriver.common.by import By

from src.bots.base.base_bot import StepStatus
from src.bots.base.wait_helpers import poll_for_new_file
from src.bots.safework.base import SafeworkBaseBot


class SafeWorkProgrammazioneSyncBot(SafeworkBaseBot):
    """
    Bot per scaricare il report Excel delle attivitàda SafeWork.
    Automatizza la navigazione alla sezione 'Visualizza Attività' ed esporta il report periodico.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login SafeWork"),
        ("nav", "Navigazione Attività"),
        ("filter", "Configurazione Filtri"),
        ("search", "Ricerca ed Esportazione"),
    ]

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = 30,
        download_path: str = "",
        account_type: str = "Esecutore",
    ) -> None:
        """
        Inizializza il bot di sincronizzazione programmazione.

        Args:
          username: Nome utente SafeWork.
          password: Password SafeWork.
          headless: Se avviare il browser in modalità nascosta.
          timeout: Tempo di attesa per Selenium.
          download_path: Cartella per il download degli Excel.
          account_type: Tipo di account (Esecutore/ISAB).
        """
        super().__init__(username, password, headless, timeout, download_path, account_type=account_type)
        self.downloaded_file: str | None = None

    @staticmethod
    def get_name() -> str:
        """Restituisce il nome identificativo del bot."""
        return "Sincronizzazione Programmazione"

    @property
    def name(self) -> str:
        """Restituisce l'ID del bot."""
        return "programmazione_sync"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Definisce le colonne richieste (nessuna per questo bot)."""
        return []

    def run(self, data: list[dict[str, Any]]) -> bool:
        """
        Esegue il download del report Excel.

        Args:
          data: Parametri della sessione (richiedenti, date).

        Returns:
          bool: True se il report  stato scaricato correttamente.
        """
        self.update_step("login", StepStatus.COMPLETED)

        params = data[0] if data else {}
        requesters = params.get("requesters", [])
        date_start = params.get("date_start")
        date_end = params.get("date_end")

        if not date_start or not date_end:
            return False

        # 1. Navigazione
        self.update_step("nav", StepStatus.RUNNING)
        self.log("   Navigazione in 'Visualizza Attività'...")
        self._attendi_scomparsa_overlay()
        if not self.driver:
            self.log("❌ Driver non inizializzato.")
            self.update_step("nav", StepStatus.ERROR)
            return False

        self.driver.find_element(By.ID, "topIcon-actHomePage").click()
        self._attendi_scomparsa_overlay()
        self.driver.find_element(By.ID, "sideBar-actVisualizzaAttivita").click()
        self._attendi_scomparsa_overlay()
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Setup Filtri
        self.update_step("filter", StepStatus.RUNNING)
        if not self.attivita_page:
            self.log("❌ Pagina Attivitànon inizializzata.")
            self.update_step("filter", StepStatus.ERROR)
            return False
        self.attivita_page.pulisci_pdl()
        self.attivita_page.imposta_date(date_start, date_end)
        self.attivita_page.seleziona_ditta("CO.EMI SRL")
        self.update_step("filter", StepStatus.COMPLETED)

        # 3. Selezione Richiedenti Multipli
        if requesters:
            self.log(f"   Selezione di {len(requesters)} richiedenti...")
            for req in requesters:
                self.attivita_page.seleziona_richiedente(req)

        # 4. Ricerca ed Esportazione
        self.update_step("search", StepStatus.RUNNING)
        self.log("[CERCA] Esecuzione ricerca...")
        self.attivita_page.esegui_ricerca()
        self._attendi_scomparsa_overlay(timeout_secondi=300)

        self.log("   Esportazione Excel...")
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
                self.update_step("search", StepStatus.COMPLETED)
                return True

        self.update_step("search", StepStatus.ERROR)
        return False
