# mypy: disable-error-code="no-untyped-call"
from contextlib import suppress

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.base.selenium_base_bot import SeleniumBaseBot
from src.bots.safework.pages.login_page import SafeWorkLoginPage
from src.bots.safework.pages.ricerca_pdl_page import RicercaPDLPage
from src.bots.safework.pages.visualizza_attivita_page import VisualizzaAttivitaPage
from src.core.constants import URLs


class SafeworkBaseBot(SeleniumBaseBot):
    """
    Classe base specifica per SafeWork.
    Isola le logiche SafeWork da quelle del Portale Fornitori.
    """

    SAFEWORK_URL = URLs.SAFEWORK_URL
    ISAB_URL = SAFEWORK_URL

    def __init__(  # noqa: PLR0913
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = 30,
        download_path: str = "",
        account_type: str = "Esecutore",
    ) -> None:
        super().__init__(username, password, headless, timeout, download_path)
        self.account_type = account_type
        self.safework_login_page: SafeWorkLoginPage | None = None
        self.ricerca_pdl_page: RicercaPDLPage | None = None
        self.attivita_page: VisualizzaAttivitaPage | None = None

    def _configure_waits_and_pages(self) -> None:
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
            return self.safework_login_page.login(
                self.username, self.password, account_type=self.account_type
            )
        return False

    def click_robusto(self, locator: tuple[str, str], timeout: int = 10, label: str | None = None) -> None:
        """
        Tenta di cliccare un elemento gestendo overlay e intercettazioni.
        """
        if not self.driver:
            self.log("❌ Driver non inizializzato.")
            return

        if label:
            self.log(f"[CLICK] Click su {label}...")

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
                self.log(f"❌ Errore click su {label or locator}: {e}")
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
            self.log("[ATTESA] Overlay ancora presente (proseguo...)")

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
                # Fallback per idtxt E421C594 (Sìdella ricerca estesa che a volte riappare)
                modale.find_element(By.CSS_SELECTOR, "*[idtxt='E421C594']").click()
                self.log("ℹ️ Modale gestita via idtxt (Si).")

        # No sleep needed: invisibility check is sufficient
        return True

    def _attendi_caricamento_sistema(self, timeout: int = 420) -> None:
        """
        Attesa specifica per SafeWork: rileva lo span 'Caricamento...'
        e ne attende la scomparsa completa.
        """
        if not self.driver or not self.wait:
            return
        xpath_caricamento = "//span[contains(text(), 'Caricamento...')]"
        try:
            # Attendiamo che appaia (se non  gia' apparso e scomparso velocemente)
            with suppress(TimeoutException):
                WebDriverWait(self.driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, xpath_caricamento))
                )

            # Attendiamo che scompaia
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.XPATH, xpath_caricamento))
            )
        except TimeoutException:
            self.log("⚠️ Timeout attesa caricamento sistema (proseguo...)")

        self._attendi_scomparsa_overlay()

    @property
    def name(self) -> str:
        return "SafeWorkBot"

    @property
    def description(self) -> str:
        return "Bot Base SafeWork"
