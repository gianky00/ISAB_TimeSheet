"""
Bot TS - Scarico TS Page
Page Object Model for the Scarico TS section.
"""

import time
from pathlib import Path
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from src.core.constants import Timeouts
from src.bots.scarico_ts.locators import ScaricoTSLocators
from selenium.webdriver.common.by import By # Explicit import for internal use

class ScaricoTSPage:
    """Encapsulates interactions with the Scarico TS page."""

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
            WebDriverWait(self.driver, Timeouts.OVERLAY).until(
                EC.invisibility_of_element_located((By.XPATH, xpath))
            )
            time.sleep(0.3)
        except TimeoutException:
            self.log("⚠️ Timeout attesa overlay.")

    def navigate_to_timesheet(self) -> bool:
        """Navigates to Report -> Timesheet."""
        try:
            self.log("Navigazione menu Report -> Timesheet...")

            # Click Report
            self.wait.until(
                EC.element_to_be_clickable(ScaricoTSLocators.REPORT_MENU)
            ).click()
            self._wait_for_overlay()

            # Click Timesheet
            self.wait.until(
                EC.element_to_be_clickable(ScaricoTSLocators.TIMESHEET_MENU)
            ).click()

            # Wait for page load (check for supplier arrow)
            self.wait.until(
                EC.visibility_of_element_located(ScaricoTSLocators.SUPPLIER_DROPDOWN_ARROW)
            )
            self._wait_for_overlay()
            return True

        except Exception as e:
            self.log(f"✗ Errore navigazione menu: {e}")
            return False

    def setup_filters(self, supplier: str, date_from: str) -> bool:
        """Sets the initial filters (Supplier and Date)."""
        try:
            # Select Supplier
            self.log(f"  Selezione fornitore: '{supplier}'...")
            arrow = self.wait.until(
                EC.element_to_be_clickable(ScaricoTSLocators.SUPPLIER_DROPDOWN_ARROW)
            )
            ActionChains(self.driver).move_to_element(arrow).click().perform()

            # Click Option
            option_xpath = f"//li[normalize-space(text())='{supplier}']"
            option = self.long_wait.until(
                EC.presence_of_element_located((By.XPATH, option_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", option)
            self._wait_for_overlay()

            # Set Date
            self.log(f"  Inserimento data '{date_from}'...")
            date_field = self.wait.until(
                EC.visibility_of_element_located(ScaricoTSLocators.DATE_FROM_FIELD)
            )
            date_field.clear()
            date_field.send_keys(date_from)

            return True
        except Exception as e:
            self.log(f"✗ Errore impostazione filtri: {e}")
            return False

    def search_and_download(self, oda_number: str, oda_position: str, download_dir: Path) -> bool:
        """Performs search for specific OdA and downloads the Excel."""
        try:
            # JS for events
            js_dispatch_events = """
                var el = arguments[0];
                var ev_in = new Event('input', {bubbles:true}); el.dispatchEvent(ev_in);
                var ev_ch = new Event('change', {bubbles:true}); el.dispatchEvent(ev_ch);
            """

            # Input OdA
            field_oda = self.wait.until(EC.presence_of_element_located(ScaricoTSLocators.ODA_NUMBER_FIELD))
            self.driver.execute_script("arguments[0].value = arguments[1];", field_oda, oda_number)
            self.driver.execute_script(js_dispatch_events, field_oda)

            # Input Position
            field_pos = self.wait.until(EC.presence_of_element_located(ScaricoTSLocators.ODA_POSITION_FIELD))
            self.driver.execute_script("arguments[0].value = '';", field_pos)
            self.driver.execute_script("arguments[0].value = arguments[1];", field_pos, oda_position)
            self.driver.execute_script(js_dispatch_events, field_pos)

            # Search
            self.wait.until(EC.element_to_be_clickable(ScaricoTSLocators.SEARCH_BUTTON)).click()
            self.log("  Pulsante 'Cerca' cliccato. Attesa risultati...")
            self._wait_for_overlay() # Wait for loading

            # Download
            return self._download_excel(download_dir, oda_number, oda_position)

        except Exception as e:
            self.log(f"  ✗ Errore ricerca/download: {e}")
            return False

    def _download_excel(self, download_dir: Path, oda_number: str, oda_position: str) -> bool:
        """Handles the file download logic."""
        try:
            files_before = {f for f in download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}

            # Click Export
            self.wait.until(
                EC.element_to_be_clickable(ScaricoTSLocators.EXPORT_EXCEL_BUTTON)
            ).click()

            # Wait for file
            downloaded_file = None
            start_time = time.time()
            while time.time() - start_time < Timeouts.DOWNLOAD:
                current_files = {f for f in download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}
                new_files = current_files - files_before
                if new_files:
                    downloaded_file = max(list(new_files), key=lambda f: f.stat().st_mtime)
                    break
                time.sleep(0.5)

            if downloaded_file and downloaded_file.exists():
                # Rename
                pos_suffix = f"-{oda_position}" if oda_position else ""
                new_name = f"{oda_number}{pos_suffix}.xlsx"
                new_path = download_dir / new_name

                # Handle duplicates
                counter = 1
                while new_path.exists() and new_path.resolve() != downloaded_file.resolve():
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    new_path = download_dir / f"{oda_number}{pos_suffix}-{timestamp}_{counter}.xlsx"
                    counter += 1

                downloaded_file.rename(new_path)
                self.log(f"  ✓ File scaricato: {new_path.name}")
                return True
            else:
                self.log("  ✗ Download fallito o file non trovato.")
                return False

        except Exception as e:
            self.log(f"  ✗ Errore click download: {e}")
            return False
