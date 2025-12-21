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
from src.utils.helpers import sanitize_filename
from src.bots.dettagli_oda.locators import DettagliOdALocators
from src.bots.common.locators import LoginLocators, CommonLocators

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

    def logout(self):
        try:
            self.log("Esecuzione logout...")
            # Click Settings
            settings_btn = self.wait.until(EC.element_to_be_clickable(CommonLocators.SETTINGS_BUTTON))
            self.driver.execute_script("arguments[0].click();", settings_btn)
            time.sleep(0.5)

            # Click Logout
            logout_btn = self.wait.until(EC.element_to_be_clickable(CommonLocators.LOGOUT_OPTION))
            self.driver.execute_script("arguments[0].click();", logout_btn)

            # Handle Confirmation Popup "Attenzione"
            try:
                self.log("  Attesa conferma logout...")
                # Wait for header "Attenzione"
                self.wait.until(EC.visibility_of_element_located(CommonLocators.POPUP_ATTENTION_HEADER))

                # Click "Si"
                yes_btn = self.wait.until(EC.element_to_be_clickable(CommonLocators.POPUP_YES_BUTTON))
                self.driver.execute_script("arguments[0].click();", yes_btn)
                self.log("  Conferma cliccata.")

                # Wait for Login Screen (logout complete)
                self.wait.until(EC.visibility_of_element_located(LoginLocators.USERNAME_FIELD))
                self.log("✓ Logout completato con successo.")

            except TimeoutException:
                self.log("⚠️ Popup conferma non apparso o timeout.")

            time.sleep(1)
        except Exception as e:
            self.log(f"⚠️ Errore durante logout: {e}")

    def process_oda(self, oda: str, contract: str, date_da: str, date_a: str, download_dir: Path) -> bool:
        try:
            # 1. Fill Form
            js_set_value = """
                var el = arguments[0];
                el.value = arguments[1];
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.blur();
            """

            # ODA - Only fill if provided
            if oda:
                field_oda = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.ODA_NUMBER_FIELD))
                self.driver.execute_script(js_set_value, field_oda, oda)

            # Date From (Clear first by setting value)
            field_date_da = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.DATE_FROM_FIELD))
            self.driver.execute_script(js_set_value, field_date_da, date_da)

            # Date To
            field_date_a = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.DATE_A_FIELD))
            self.driver.execute_script(js_set_value, field_date_a, date_a)

            # Contract
            field_contract = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.CONTRACT_FIELD))
            self.driver.execute_script(js_set_value, field_contract, contract)

            # Checkbox
            checkbox = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.CHECKBOX_FIELD))
            if not checkbox.is_selected():
                 self.driver.execute_script("arguments[0].click();", checkbox)

            time.sleep(0.5)

            # Click Search
            self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.SEARCH_BUTTON)).click()
            self.log("  Cerca cliccato...")
            self._wait_for_overlay()

            # Check Results Count
            try:
                count_label = self.wait.until(EC.visibility_of_element_located(DettagliOdALocators.RESULTS_COUNT_LABEL))
                count_text = count_label.text.strip() # "Trovati : 676"
                if ':' in count_text:
                    count = int(count_text.split(':')[-1].strip())
                    self.log(f"  Risultati trovati: {count}")
                    if count == 0:
                        self.log("  Nessun risultato. Salto esportazione.")
                        self._close_all_tabs()
                        return True
                else:
                    self.log(f"  ⚠️ Impossibile parsare risultati: {count_text}")
            except Exception as e:
                self.log(f"  ⚠️ Errore lettura conteggio: {e}")

            # Decide Export Method based on ODA presence
            target_filename = ""
            if oda:
                # ODA Present: Details Export
                self.log("  Apertura dettagli (OdA specifico)...")
                details_btn = self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.DETAILS_ICON))
                self.driver.execute_script("arguments[0].click();", details_btn)
                self._wait_for_overlay()

                # Wait for Inner Export button
                export_btn_locator = DettagliOdALocators.EXPORT_EXCEL_TEXT
                safe_oda = sanitize_filename(oda)
                target_filename = f"dettaglio_oda_{safe_oda}.xlsx"
            else:
                # ODA Empty: General List Export
                self.log("  Esportazione lista generale...")
                export_btn_locator = DettagliOdALocators.GENERAL_EXPORT_BUTTON
                target_filename = "lista_generale_oda.xlsx"

            # Export and Download
            res = self._download(download_dir, target_filename, export_btn_locator)

            # Cleanup
            self._close_all_tabs()
            return res

        except Exception as e:
            self.log(f"  ✗ Errore processamento: {e}")
            self.log(f"Stacktrace: {traceback.format_exc()}")
            # Ensure tabs are closed even on error
            try:
                self._close_all_tabs()
            except:
                pass
            return False

    def _close_all_tabs(self):
        """Closes all open tabs using the X button."""
        try:
            # Find all close buttons. We might need to iterate or they might be dynamic.
            # Usually ExtJS tabs have a close tool.
            # We assume clicking them one by one works.
            # Warning: clicking one might change the DOM for others.
            # It's safer to find one, click, wait, repeat until none found.
            while True:
                try:
                    # Find *visible* close buttons only
                    close_btn = self.driver.find_element(*DettagliOdALocators.TAB_CLOSE_BTN)
                    if close_btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", close_btn)
                        time.sleep(0.5)
                    else:
                        break
                except Exception:
                    # No more close buttons found
                    break
        except Exception as e:
            self.log(f"  ⚠️ Errore chiusura tab: {e}")

    def _download(self, download_dir: Path, target_filename: str, button_locator: tuple) -> bool:
        try:
            files_before = {f for f in download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}

            btn = self.wait.until(EC.presence_of_element_located(button_locator))
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
                new_path = download_dir / target_filename

                # Handle overwrite/uniqueness if needed, though user asked for specific name.
                # If "lista_generale_oda.xlsx" exists, we might overwrite or append counter.
                # Assuming overwrite is NOT desired for safe automation, adding counter if exists.
                if new_path.exists():
                    stem = new_path.stem
                    suffix = new_path.suffix
                    counter = 1
                    while new_path.exists() and new_path.resolve() != downloaded_file.resolve():
                        new_path = download_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                downloaded_file.rename(new_path)
                self.log(f"  ✓ Scaricato: {new_path.name}")
                return True
            return False
        except Exception as e:
            self.log(f"  ✗ Errore download: {e}")
            return False
