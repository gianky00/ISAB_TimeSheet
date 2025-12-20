"""
Bot TS - Carico TS Page
Page Object Model for Carico TS.
"""
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.core.constants import Timeouts
from src.bots.carico_ts.locators import CaricoTSLocators

class CaricoTSPage:
    def __init__(self, driver: WebDriver, log_callback=None):
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.log = log_callback or print

    def _wait_overlay(self):
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            WebDriverWait(self.driver, Timeouts.OVERLAY).until(
                EC.invisibility_of_element_located((By.XPATH, xpath))
            )
            time.sleep(0.3)
        except: pass

    def navigate(self) -> bool:
        try:
            self.log("Navigazione Gestione Timesheet...")
            self.wait.until(EC.element_to_be_clickable(CaricoTSLocators.MANAGEMENT_MENU)).click()
            self._wait_overlay()
            return True
        except Exception as e:
            self.log(f"Errore navigazione: {e}")
            return False

    def select_supplier(self, supplier: str) -> bool:
        try:
            self.log(f"Selezione {supplier}...")
            arrow = self.wait.until(EC.element_to_be_clickable(CaricoTSLocators.SUPPLIER_ARROW))
            ActionChains(self.driver).move_to_element(arrow).click().perform()

            opt_xpath = f"//li[contains(text(), '{supplier}')]"
            opt = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, opt_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'nearest'});", opt)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", opt)
            self._wait_overlay()
            return True
        except Exception as e:
            self.log(f"Errore fornitore: {e}")
            return False

    def process_oda(self, oda: str) -> bool:
        try:
            self.log(f"Inserimento OdA: {oda}")
            inp = self.wait.until(EC.presence_of_element_located(CaricoTSLocators.ODA_INPUT))

            # JS Click to focus/activate
            self.driver.execute_script("arguments[0].click();", inp)
            time.sleep(0.2)

            # Use JS to set value + dispatch events
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
            time.sleep(2)
            return True
        except Exception as e:
            self.log(f"Errore processo OdA: {e}")
            return False
