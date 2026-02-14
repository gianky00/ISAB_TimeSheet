from contextlib import suppress

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.base.base_bot import BaseBot
from src.bots.safework.common.locators import SafeWorkLocators
from src.bots.safework.pages.login_page import SafeWorkLoginPage
from src.bots.safework.pages.ricerca_pdl_page import RicercaPDLPage
from src.bots.safework.pages.visualizza_attivita_page import VisualizzaAttivitaPage


class SafeworkBaseBot(BaseBot):
    """
    Classe base specifica per SafeWork modulare.
    """

    SAFEWORK_URL = "https://safework.isab.com/"
    ISAB_URL = SAFEWORK_URL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_page_sw: SafeWorkLoginPage | None = None
        self.attivita_page: VisualizzaAttivitaPage | None = None
        self.ricerca_pdl_page: RicercaPDLPage | None = None

    def _init_pages(self):
        """Inizializza le Page Objects dopo la creazione del driver."""
        if self.driver and self.wait:
            self.login_page_sw = SafeWorkLoginPage(self.driver, self.wait, self.log)
            self.attivita_page = VisualizzaAttivitaPage(self.driver, self.wait, self.log)
            self.ricerca_pdl_page = RicercaPDLPage(self.driver, self.wait, self.log)

    def _login(self) -> bool:
        """Login SafeWork con gestione TCL/COEMI."""
        if not self.driver or not self.wait:
            return False

        self._init_pages()
        self.log("🌐 Navigazione verso SafeWork...")
        try:
            self.driver.get(self.SAFEWORK_URL)
        except Exception as e:
            self.log(f"❌ Errore apertura URL: {e}")
            return False

        if self.login_page_sw is None:
            self.log("❌ Login Page non inizializzata.")
            return False
        if self.login_page_sw.login(self.username, self.password):
            if "fcaldarella" in self.username.lower():
                self.log("⏳ Account TCL rilevato: attendo solo overlay...")
                self._attendi_scomparsa_overlay(timeout_secondi=60)
            else:
                self.log("⏳ Account standard rilevato: attendo caricamento sistema...")
                self._attendi_caricamento_sistema()
            return True
        return False

    def _attendi_scomparsa_overlay(self, timeout_secondi: int | None = 120) -> bool:
        """Attesa overlay SafeWork con gestione race condition."""
        if not self.driver:
            return False

        import time

        # Piccola pausa per permettere agli script di attivare l'overlay
        time.sleep(0.8)

        timeout = timeout_secondi if timeout_secondi is not None else 120

        try:
            # Attendiamo che l'overlay sia effettivamente invisibile o assente
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(SafeWorkLocators.OVERLAY)
            )
            # Ulteriore mini-pausa per stabilità DOM dopo la scomparsa
            time.sleep(0.3)
        except TimeoutException:
            self.log("⏳ Overlay ancora presente dopo il timeout (proseguo con cautela...)")

        with suppress(Exception):
            modali = self.driver.find_elements(*SafeWorkLocators.MODAL_DIALOG)
            if modali and modali[0].is_displayed():
                btn = modali[0].find_element(*SafeWorkLocators.MODAL_OK_BUTTON)
                btn.click()
                self.log("ℹ️ Popup modale gestito.")
        return True

    def click_robusto(self, locator: tuple[str, str], timeout: int = 20):
        """Esegue un click gestendo eventuali intercettazioni da overlay."""
        import time

        from selenium.common.exceptions import ElementClickInterceptedException

        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                el = self.wait.until(EC.element_to_be_clickable(locator))
                el.click()
                return
            except ElementClickInterceptedException:
                self.log("⏳ Click intercettato, attendo scomparsa overlay...")
                self._attendi_scomparsa_overlay(timeout_secondi=10)
            except Exception as e:
                self.log(f"⚠️ Errore durante il click robusto: {e}")
                raise e

        # Ultimo tentativo via JS se bloccato
        self.log("🚀 Fallback: Click via JavaScript")
        el = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", el)

    def _attendi_caricamento_sistema(self):
        """Attesa specifica per account COEMI."""
        if not self.driver:
            return

        with suppress(TimeoutException):
            WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located(SafeWorkLocators.CARICAMENTO_SPAN)
            )
            WebDriverWait(self.driver, 300).until(
                EC.invisibility_of_element_located(SafeWorkLocators.CARICAMENTO_SPAN)
            )

        self._attendi_scomparsa_overlay()

    @property
    def name(self) -> str:
        return "safework_base"

    @property
    def description(self) -> str:
        return "Bot Base SafeWork Modulare"
