# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Carico TS Page
Page Object Model for Carico TS.
"""

from collections.abc import Callable
from contextlib import suppress

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.portale_fornitori.carico_ts.locators import CaricoTSLocators
from src.core.constants import Timeouts


class CaricoTSPage:
    """
    Page Object Model per la gestione del caricamento dei TimeSheet.
    Fornisce strumenti per navigare nell'area gestione e interagire con gli ordini.
    """

    def __init__(self, driver: WebDriver, log_callback: Callable[[str], None] | None = None) -> None:
        """
        Inizializza la pagina con il driver e la callback di logging.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.log = log_callback or print

    def _wait_overlay(self) -> None:
        """Attende la scomparsa delle maschere di caricamento del portale."""
        with suppress(Exception):
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            WebDriverWait(self.driver, Timeouts.OVERLAY).until(
                EC.invisibility_of_element_located((By.XPATH, xpath))
            )

    def navigate(self) -> bool:
        """Naviga verso il menu Gestione Timesheet."""
        try:
            self.log("Navigazione Gestione Timesheet...")
            self.wait.until(EC.element_to_be_clickable(CaricoTSLocators.MANAGEMENT_MENU)).click()
            self._wait_overlay()
        except Exception as e:
            self.log(f"Errore navigazione: {e}")
            return False
        else:
            return True

    def select_supplier(self, supplier: str) -> bool:
        """
        Seleziona il fornitore indicato dal menu a discesa.

        Args:
          supplier: Nome del fornitore.
        Returns:
          bool: True se la selezione ha avuto successo.
        """
        try:
            self.log(f"Selezione {supplier}...")
            arrow = self.wait.until(EC.element_to_be_clickable(CaricoTSLocators.SUPPLIER_ARROW))
            ActionChains(self.driver).move_to_element(arrow).click().perform()

            opt_xpath = f"//li[contains(text(), '{supplier}')]"
            opt = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, opt_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'nearest'});", opt)
            self.driver.execute_script("arguments[0].click();", opt)
            self._wait_overlay()
        except Exception as e:
            self.log(f"Errore fornitore: {e}")
            return False
        else:
            return True

    def process_oda(self, oda: str) -> bool:
        """
        Inserisce il numero OdA nel campo di input e avvia l'estrazione.

        Args:
          oda: Numero dell'Ordine di Acquisto.
        Returns:
          bool: True se l'input  stato inviato correttamente.
        """
        try:
            self.log(f"Inserimento OdA: {oda}")
            inp = self.wait.until(EC.presence_of_element_located(CaricoTSLocators.ODA_INPUT))

            # JS Click to focus/activate
            self.driver.execute_script("arguments[0].click();", inp)
            js = """
      var el = arguments[0];
      el.value = arguments[1];
      el.dispatchEvent(new Event('input', {bubbles:true}));
      el.dispatchEvent(new Event('change', {bubbles:true}));
      el.dispatchEvent(new Event('blur', {bubbles:true}));
      """
            self.driver.execute_script(js, inp, oda)

            # Click Extract
            btn = self.wait.until(EC.element_to_be_clickable(CaricoTSLocators.EXTRACT_BUTTON))
            btn.click()
            self.log("Estrai OdA cliccato.")

            # Just stopping here as per original logic (it stops after extract)
        except Exception as e:
            self.log(f"Errore processo OdA: {e}")
            return False
        else:
            return True
