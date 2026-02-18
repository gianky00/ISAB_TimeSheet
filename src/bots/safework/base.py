from contextlib import suppress

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.base.base_bot import BaseBot
from src.bots.safework.pages.login_page import SafeWorkLoginPage
from src.bots.safework.pages.ricerca_pdl_page import RicercaPDLPage
from src.bots.safework.pages.visualizza_attivita_page import VisualizzaAttivitaPage


class SafeworkBaseBot(BaseBot):
    """
    Classe base specifica per SafeWork.
    Isola le logiche SafeWork da quelle del Portale Fornitori.
    """

    SAFEWORK_URL = "https://safework.isab.com/"
    ISAB_URL = SAFEWORK_URL

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.safework_login_page: SafeWorkLoginPage | None = None
        self.ricerca_pdl_page: RicercaPDLPage | None = None
        self.attivita_page: VisualizzaAttivitaPage | None = None

    def _configure_waits_and_pages(self):
        """Inizializza le Page Objects specifiche di SafeWork."""
        super()._configure_waits_and_pages()
        if self.driver and self.wait:
            self.safework_login_page = SafeWorkLoginPage(self.driver, self.wait, self.log)
            self.ricerca_pdl_page = RicercaPDLPage(self.driver, self.wait, self.log)
            self.attivita_page = VisualizzaAttivitaPage(self.driver, self.wait, self.log)

    def _login(self) -> bool:
        """Override del login per usare SafeWorkLoginPage."""
        if self.safework_login_page and self.driver:
            self.driver.get(self.ISAB_URL)
            return self.safework_login_page.login(self.username, self.password)
        return False

    def click_robusto(self, locator: tuple[str, str], timeout: int = 10):
        """
        Tenta di cliccare un elemento gestendo overlay e intercettazioni.
        """
        if not self.driver:
            self.log("❌ Driver non inizializzato.")
            return

        try:
            self._attendi_scomparsa_overlay()
            el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            el.click()
        except Exception:
            # Fallback JS click
            try:
                el = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception as e:
                self.log(f"❌ Errore click robusto su {locator}: {e}")
                raise

    def _attendi_scomparsa_overlay(self, timeout_secondi: int | None = 120) -> bool:
        """Logica di attesa fedele allo script originale."""
        if timeout_secondi is None:
            timeout_secondi = 120
        if not self.driver:
            return False
        try:
            # Attende la scomparsa dell'overlay grigio
            WebDriverWait(self.driver, timeout_secondi).until(
                EC.invisibility_of_element_located((By.ID, "GISWaitOverlay"))
            )
        except TimeoutException:
            self.log("⏳ Overlay ancora presente (proseguo...)")

        # Gestione modale OK/Annulla se appare
        with suppress(Exception):
            modale = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'modal') and contains(@style, 'display: block')]",
                    )
                )
            )
            # Supporta OK, Annulla, Si, Yes (anche in span/div)
            try:
                modale.find_element(
                    By.XPATH,
                    ".//*[self::button or self::span or self::a][contains(text(), 'OK') or contains(text(), 'Si') or contains(text(), 'Yes') or @data-dismiss='modal']",
                ).click()
                self.log("ℹ️ Modale gestita (OK/Annulla/Si/Yes).")
            except Exception:
                # Fallback per idtxt E421C594 (Si della ricerca estesa che a volte riappare)
                modale.find_element(By.CSS_SELECTOR, "*[idtxt='E421C594']").click()
                self.log("ℹ️ Modale gestita via idtxt (Si).")

        # No sleep needed: invisibility check is sufficient
        return True

    def _attendi_caricamento_sistema(self):
        """Implementa l'attesa specifica: compare e poi scompare."""
        if not self.driver:
            return
        xpath_caricamento = "//span[contains(text(), 'Caricamento...')]"
        try:
            self.log("⏳ Attesa comparsa caricamento...")
            WebDriverWait(self.driver, 120).until(
                EC.visibility_of_element_located((By.XPATH, xpath_caricamento))
            )
            self.log("⏳ Sistema in caricamento, attesa completamento...")
            WebDriverWait(self.driver, 420).until(
                EC.invisibility_of_element_located((By.XPATH, xpath_caricamento))
            )
            self.log("✅ Caricamento sistema completato.")
        except TimeoutException:
            self.log("⚠️ Timeout attesa caricamento (proseguo...)")

        self._attendi_scomparsa_overlay()

    @property
    def name(self) -> str:
        return "SafeWorkBot"

    @property
    def description(self) -> str:
        return "Bot Base SafeWork"
