"""
SyncroJob - SafeWork Visualizza Attività Page
Encapsulamento delle interazioni con la pagina di visualizzazione attività.
"""

import logging
import time
from collections.abc import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.common.locators import SafeWorkLocators

logger = logging.getLogger(__name__)


class VisualizzaAttivitaPage:
    """Gestisce l'interfaccia di 'Visualizza Attività' su SafeWork."""

    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait[webdriver.Chrome], log_func: Callable[[str], None]
    ):
        self.driver = driver
        self.wait = wait
        self.log = log_func

    def imposta_date(self, start: str, end: str):
        """Imposta il range di date programmazione."""
        self.log(f"📅 Impostazione date: {start} - {end}")
        for loc, val in ((SafeWorkLocators.DATA_DAL, start), (SafeWorkLocators.DATA_AL, end)):
            el = self.wait.until(EC.presence_of_element_located(loc))
            self.driver.execute_script("arguments[0].value = '';", el)
            self.driver.execute_script("arguments[0].value = arguments[1];", el, val)
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", el
            )

    def seleziona_ditta(self, nome_ditta: str = "CO.EMI SRL"):
        """Seleziona la ditta dal dropdown."""
        try:
            self.log(f"🏢 Selezione Ditta: {nome_ditta}")
            btn = self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.DITTA_BUTTON))
            btn.click()
            time.sleep(0.5)
            xpath = f"//div[contains(@class,'ms-drop')]//span[normalize-space()='{nome_ditta}']"
            opt = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            opt.click()
            btn.click()  # Chiudi
        except Exception as e:
            self.log(f"⚠️ Errore selezione ditta: {e}")

    def pulisci_pdl(self):
        """Pulisce il campo Numero PDL."""
        try:
            el = self.driver.find_element(*SafeWorkLocators.NUM_PERMESSO_FIELD)
            el.clear()
            el.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        except Exception:
            logger.debug("Campo Numero PDL non trovato o già vuoto.")

    def seleziona_richiedente(self, nome: str) -> bool:
        """Seleziona un richiedente tramite la ricerca nel dropdown."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.RICHIEDENTE_BUTTON))
            btn.click()
            time.sleep(0.5)

            dropdown = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.DROPDOWN_OPEN))
            search = dropdown.find_element(*SafeWorkLocators.SEARCH_INPUT_IN_DROPDOWN)
            search.clear()
            search.send_keys(nome)
            time.sleep(1)

            xpath = f".//label//span[contains(normalize-space(), '{nome}')]"
            opzioni = dropdown.find_elements(By.XPATH, xpath)

            if not opzioni:
                # Fallback cognome
                nome_short = nome.split()[0]
                xpath_short = f".//label//span[contains(normalize-space(), '{nome_short}')]"
                opzioni = dropdown.find_elements(By.XPATH, xpath_short)

            if opzioni:
                self.driver.execute_script("arguments[0].click();", opzioni[0])
                time.sleep(0.5)
                btn.click()
                return True

            self.log(f"❌ Richiedente '{nome}' non trovato.")
            btn.click()
            return False
        except Exception as e:
            self.log(f"⚠️ Errore selezione richiedente: {e}")
            return False

    def esegui_ricerca(self):
        """Clicca Cerca e attende la scomparsa dell'overlay."""
        btn = self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.SEARCH_START_BUTTON))
        btn.click()
        # Nota: l'attesa overlay è gestita esternamente dal bot base o helper

    def esporta_excel(self) -> bool:
        """Clicca su Esporta."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.EXPORT_BUTTON))
            btn.click()
            return True
        except Exception:
            return False

    def get_rows(self) -> list[WebElement]:
        """Restituisce le righe della tabella se presenti."""
        try:
            # Check 'Nessun dato'
            msg = self.driver.find_elements(*SafeWorkLocators.NO_DATA_MSG)
            if msg and msg[0].is_displayed():
                return []

            table = self.wait.until(EC.presence_of_element_located(SafeWorkLocators.RESULTS_TABLE))
            return table.find_elements(*SafeWorkLocators.ROWS)
        except Exception:
            return []
