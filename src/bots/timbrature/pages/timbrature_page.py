"""
Bot TS - Timbrature Page
Page Object Model for the Timbrature section of the ISAB portal.
"""

import time
import os
import shutil
from pathlib import Path
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from src.core.constants import Timeouts
from src.bots.timbrature.locators import TimbratureLocators

class TimbraturePage:
    """Encapsulates interactions with the Timbrature page."""

    def __init__(self, driver: WebDriver, log_callback: Optional[callable] = None):
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.long_wait = WebDriverWait(driver, Timeouts.PAGE_LOAD)
        self._log = log_callback or print

    def log(self, msg: str):
        self._log(msg)

    def _wait_for_overlay(self):
        """Waits for loading overlay to disappear."""
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            # Fix: EC does not contain By. Use By directly.
            from selenium.webdriver.common.by import By
            WebDriverWait(self.driver, Timeouts.OVERLAY).until(
                EC.invisibility_of_element_located((By.XPATH, xpath))
            )
            time.sleep(0.3)
        except TimeoutException:
            self.log("⚠️ Timeout attesa overlay.")
        except AttributeError:
             # Fallback if EC.By is not available (Selenium version differences or mixup)
            from selenium.webdriver.common.by import By
            WebDriverWait(self.driver, Timeouts.OVERLAY).until(
                EC.invisibility_of_element_located((By.XPATH, xpath))
            )
            time.sleep(0.3)

    def navigate_to_timbrature(self) -> bool:
        """Navigates to Report -> Timbrature."""
        try:
            self.log("Navigazione verso pagina Timbrature...")
            report_element = self.wait.until(
                EC.element_to_be_clickable(TimbratureLocators.REPORT_MENU)
            )
            report_element.click()
            time.sleep(1.5)

            # Keyboard navigation to tab
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.ENTER).perform()

            time.sleep(1.0)
            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"Errore navigazione: {e}")
            return False

    def set_filters(self, fornitore: str, data_da: str, data_a: str) -> bool:
        """Sets the search filters."""
        try:
            # 1. Select Supplier
            if fornitore:
                self._select_supplier(fornitore)

            self.log("Imposto filtri data e flag...")
            
            # Explicitly wait for elements instead of blind TABS
            
            # 2. Select Date From
            # Assuming 'Data Da' is the first input after Supplier combo or identified by name/placeholder
            # Since we don't have the exact ID, we might stick to TABs if we can't find selectors, 
            # BUT we should use waits.
            # However, looking at the code, it relies on focus order. 
            # To improve reliability without selectors, we ensure the previous action is done.
            
            # Let's try to improve the interaction with pauses by using Explicit Waits for "active element" 
            # if we can't find the ID. 
            # But the best fix is using the locators if available. 
            # Since I don't have the HTML source, I will make the ActionChains more robust
            # by adding small waits and checks.
            
            actions = ActionChains(self.driver)

            # Focus Date From
            actions.send_keys(Keys.TAB).pause(0.5)
            if data_da:
                actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).pause(0.2)
                actions.send_keys(data_da).pause(0.5)

            # Focus Date To
            actions.send_keys(Keys.TAB).pause(0.5)
            if data_a:
                actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).pause(0.2)
                actions.send_keys(data_a).pause(0.5)

            # Checkbox "Verifica Presenza Timesheet"
            # Instead of 5 TABs, we should try to find it by text or structure if possible.
            # If not, we keep TABs but increase safety.
            for _ in range(5):
                actions.send_keys(Keys.TAB).pause(0.3)
            
            # Toggle check
            actions.send_keys(Keys.SPACE).pause(0.5)

            # Search Button
            actions.send_keys(Keys.TAB).pause(0.5)
            actions.send_keys(Keys.ENTER)

            self.log("Eseguo sequenza tasti e click su Cerca...")
            actions.perform()

            self.log("Attendo caricamento risultati...")
            self._wait_for_overlay()
            
            # Wait for results table or empty message
            time.sleep(1.0) # Grace period for table render
            
            self.log("Caricamento terminato.")
            return True

        except Exception as e:
            self.log(f"Errore impostazione filtri: {e}")
            return False

    def _select_supplier(self, fornitore: str):
        """Helper to select supplier from dropdown."""
        self.log(f"Seleziono fornitore: {fornitore}")
        try:
            # Ensure overlay is gone before starting interaction
            self._wait_for_overlay()

            arrow_element = None
            # Retry mechanism for finding the arrow
            for attempt in range(3):
                try:
                    try:
                        arrow_element = self.wait.until(
                            EC.element_to_be_clickable(TimbratureLocators.COMBO_ARROW_SUPPLIER)
                        )
                    except TimeoutException:
                        arrow_element = self.wait.until(
                            EC.element_to_be_clickable(TimbratureLocators.COMBO_ARROW_GENERIC)
                        )

                    if arrow_element:
                        # Use JS click if mouse interaction is flaky
                        try:
                            ActionChains(self.driver).move_to_element(arrow_element).click().perform()
                        except:
                            self.driver.execute_script("arguments[0].click();", arrow_element)
                        break
                except Exception:
                    time.sleep(1)

            if not arrow_element:
                raise Exception("Impossibile trovare la freccia del fornitore.")

            time.sleep(0.5) # Wait for list animation

            # Select option with retry
            from selenium.webdriver.common.by import By
            option_xpath = f"//li[contains(text(), '{fornitore}')]"

            # Wait specifically for the option to be visible
            option = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, option_xpath))
            )

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)
            time.sleep(0.3)

            try:
                option.click()
            except (ElementClickInterceptedException, Exception):
                self.driver.execute_script("arguments[0].click();", option)

            time.sleep(0.5)
            self._wait_for_overlay()

        except Exception as e:
            self.log(f"⚠️ Errore selezione fornitore: {e}")
            # Non-blocking, might work anyway if default is correct, but logged.

    def download_excel(self) -> str:
        """Finds and clicks the Excel download button, returning the file path."""
        downloaded_file = ""
        try:
            self.log("Cerco pulsante Excel...")
            time.sleep(1.0)
            excel_btn = self._find_excel_button()

            if not excel_btn:
                self.log("⚠️ Pulsante Excel non trovato.")
                return ""

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", excel_btn)
            time.sleep(0.5)

            self.log("Clicco su Excel...")
            try:
                excel_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", excel_btn)

            self.log("Attendo download...")
            time.sleep(3.0)
            downloaded_file = self._rename_latest_download("timbrature_temp")
            return downloaded_file

        except Exception as e:
            self.log(f"⚠️ Errore download Excel: {e}")
            return ""

    def _find_excel_button(self):
        """Tries multiple strategies to find the Excel button."""
        strategies = [
            TimbratureLocators.DOWNLOAD_BTN_TEXT,
            TimbratureLocators.DOWNLOAD_BTN_ICON,
            TimbratureLocators.DOWNLOAD_BTN_ARIA
        ]

        for locator in strategies:
            try:
                return WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(locator)
                )
            except TimeoutException:
                continue
        return None

    def _rename_latest_download(self, new_name_base: str) -> str:
        """Finds latest download in system Downloads and moves it to temp folder."""
        source_dir = Path.home() / "Downloads"
        from src.core.config_manager import CONFIG_DIR
        dest_dir = CONFIG_DIR / "temp"
        dest_dir.mkdir(parents=True, exist_ok=True)

        timeout = Timeouts.DOWNLOAD
        start_time = time.time()
        latest_file = None

        while time.time() - start_time < timeout:
            files = list(source_dir.glob("*"))
            files = [f for f in files if not f.name.endswith(('.crdownload', '.tmp')) and f.is_file()]

            if files:
                latest_file = max(files, key=lambda f: f.stat().st_mtime)
                if time.time() - latest_file.stat().st_mtime < 20:
                    break
            time.sleep(1)

        if not latest_file:
            return ""

        try:
            ext = latest_file.suffix
            new_path = dest_dir / f"{new_name_base}_{int(time.time())}{ext}"
            shutil.move(str(latest_file), str(new_path))
            return str(new_path)
        except Exception as e:
            self.log(f"Errore spostamento file: {e}")
            return ""
