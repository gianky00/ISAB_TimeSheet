"""
Bot TS - Dettagli OdA Page
Page Object Model for Dettagli OdA.
"""

import time
import traceback
from pathlib import Path
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.core.constants import Timeouts
from src.bots.dettagli_oda.locators import DettagliOdALocators

class DettagliOdAPage:

    def __init__(self, driver: WebDriver, log_callback: Optional[callable] = None):
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.long_wait = WebDriverWait(driver, Timeouts.PAGE_LOAD)
        self._log = log_callback or print

    def log(self, msg):
        self._log(msg)

    def _wait_for_overlay(self):
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            WebDriverWait(self.driver, Timeouts.OVERLAY).until(
                EC.invisibility_of_element_located((By.XPATH, xpath))
            )
            time.sleep(0.3)
        except TimeoutException:
            pass

    def navigate_to_dettagli(self) -> bool:
        try:
            self.log("Navigazione menu Report -> Oda...")
            time.sleep(1) # Ensure UI is idle

            # Click Report (using JS to avoid interception/crash)
            report_btn = self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.REPORT_MENU))
            self.driver.execute_script("arguments[0].click();", report_btn)
            self._wait_for_overlay()

            # Click Oda
            oda_btn = self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.DETTAGLI_MENU))
            self.driver.execute_script("arguments[0].click();", oda_btn)

            self.wait.until(EC.visibility_of_element_located(DettagliOdALocators.SUPPLIER_ARROW))
            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"✗ Navigazione fallita: {e}")
            self.log(f"Stacktrace: {traceback.format_exc()}")
            return False

    def setup_supplier(self, supplier: str) -> bool:
        try:
            self.log(f"Selezione fornitore: {supplier}")
            arrow = self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.SUPPLIER_ARROW))
            ActionChains(self.driver).move_to_element(arrow).click().perform()

            option_xpath = f"//li[contains(text(), '{supplier}')]"
            option = self.long_wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", option)
            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"✗ Selezione fornitore fallita: {e}")
            return False

    def process_oda(self, oda: str, contract: str, date_a: str, download_dir: Path) -> bool:
        try:
            # 1. Fill Form (Sequence: ODA -> TAB -> Date A -> TAB -> Contract -> TAB TAB -> Space)

            # WORKAROUND: Focus Supplier field and TAB to 'Numero OdA' to avoid locating issues
            supplier_input = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.SUPPLIER_INPUT))
            # Focus without clicking (to avoid opening dropdown)
            self.driver.execute_script("arguments[0].focus();", supplier_input)

            # TAB to Numero OdA
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB).pause(0.2).perform()

            # Get the active element (which should be Numero OdA)
            field_oda = self.driver.switch_to.active_element

            # Use JS to set ODA safely
            js_script = """
                var el = arguments[0];
                el.value = arguments[1];
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.focus();
            """
            self.driver.execute_script(js_script, field_oda, oda)
            time.sleep(0.5)

            # Proceed with ActionChains for the rest (already focused on ODA, so next TAB goes to next field)
            actions = ActionChains(self.driver)

            actions.send_keys(Keys.TAB).pause(0.5)

            # Date A
            actions.send_keys(date_a).pause(0.5)
            actions.send_keys(Keys.TAB).pause(0.5)

            # Contract
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).pause(0.2)
            actions.send_keys(contract).pause(0.5)

            # Flag "Verifica Presenza"
            actions.send_keys(Keys.TAB).pause(0.2)
            actions.send_keys(Keys.TAB).pause(0.2)
            actions.send_keys(Keys.SPACE).pause(0.5)

            actions.perform()

            # Click Search
            self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.SEARCH_BUTTON)).click()
            self.log("  Cerca cliccato...")
            self._wait_for_overlay()

            return self._download(download_dir, oda, contract)

        except Exception as e:
            self.log(f"  ✗ Errore processamento: {e}")
            self.log(f"Stacktrace: {traceback.format_exc()}")
            return False

    def _download(self, download_dir: Path, oda: str, contract: str) -> bool:
        try:
            files_before = {f for f in download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}

            btn = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.EXPORT_EXCEL_TEXT))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.5)
            try:
                btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", btn)

            downloaded_file = None
            start_time = time.time()
            while time.time() - start_time < Timeouts.DOWNLOAD:
                current_files = {f for f in download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}
                new_files = current_files - files_before
                if new_files:
                    downloaded_file = max(list(new_files), key=lambda f: f.stat().st_mtime)
                    break
                time.sleep(0.5)

            if downloaded_file:
                new_name = f"{oda}_{contract}.xlsx"
                new_path = download_dir / new_name

                counter = 1
                while new_path.exists() and new_path.resolve() != downloaded_file.resolve():
                    new_path = download_dir / f"{oda}_{contract}_{counter}.xlsx"
                    counter += 1

                downloaded_file.rename(new_path)
                self.log(f"  ✓ Scaricato: {new_path.name}")
                return True
            return False
        except Exception:
            return False
