# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - SafeWork PDL Search Page
Gestisce le interazioni con la pagina di ricerca PDL.
Logica allineata al branch Main per massima stabilità.
"""

from collections.abc import Callable
from contextlib import suppress

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.common.locators import SafeWorkLocators


class RicercaPDLPage:
    """Page Object per la pagina di ricerca PDL."""

    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait[webdriver.Chrome], log_func: Callable[[str], None]
    ) -> None:
        self.driver = driver
        self.wait = wait
        self.log = log_func

    def configura_filtro_chiusi(self, exclude_closed: bool) -> None:
        """Imposta il filtro 'Escludi chiusi'."""
        try:
            checkbox = self.wait.until(
                EC.presence_of_element_located(SafeWorkLocators.ESCLUDI_CHIUSI_CHECKBOX)
            )
            if checkbox.is_selected() != exclude_closed:
                self.log(f"[CLICK] Impostazione 'Escludi chiusi': {exclude_closed}")
                # Uso JS click come nel branch main per evitare problemi di intercettazione
                self.driver.execute_script("arguments[0].click();", checkbox)  # type: ignore[no-untyped-call]
        except Exception as e:
            self.log(f"[ATTENZIONE] Errore configurazione flag 'Escludi chiusi': {e}")

    def seleziona_sito_e_cerca(self, site_name: str) -> bool:
        """
        Seleziona il sito dal menu e clicca Cerca.
        REPLICA ESATTA DEL BRANCH MAIN (search_bot.py).
        """
        try:
            self.log(f"🏢 Selezione sito: {site_name}")

            # 1. Clic Dropdown (Locator Main)
            site_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[contains(text(), 'ISAB Sud') or contains(text(), 'ISAB Nord') or contains(text(), 'IGCC') or contains(text(), 'Sito')]",
                    )
                )
            )
            site_dropdown.click()

            # 2. Clic Opzione (Locator Main - Exact Match)
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{site_name}']"))
            )
            option.click()

            # 3. Clic Cerca (Directly after option, no waits, no body clicks)
            self.log("[CLICK] Clic su Cerca...")
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnCerca"))).click()

            # 4. Attesa Overlay (Post-Search)
            self._attendi_scomparsa_overlay(timeout_secondi=300)

            return True  # noqa: TRY300
        except Exception as e:
            self.log(f"[ERRORE] Errore selezione/ricerca (Main Logic): {e}")
            return False

    def _attendi_scomparsa_overlay(self, timeout_secondi: int = 300) -> None:
        """Attende la scomparsa dell'overlay di caricamento (GISWaitOverlay)."""
        with suppress(TimeoutException):
            # Verifica preliminare se l'overlay è visibile
            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(SafeWorkLocators.OVERLAY))
            # Attesa lunga per la scomparsa
            WebDriverWait(self.driver, timeout_secondi).until(
                EC.invisibility_of_element_located(SafeWorkLocators.OVERLAY)
            )

    def esporta_excel(self) -> bool:
        """Clicca sul pulsante Esporta."""
        try:
            self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.EXPORT_BUTTON)).click()
            return True  # noqa: TRY300
        except Exception as e:
            self.log(f"[ERRORE] Errore click export: {e}")
            return False
