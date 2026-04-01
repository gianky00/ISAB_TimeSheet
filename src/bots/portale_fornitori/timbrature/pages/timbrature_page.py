# mypy: disable-error-code="no-any-unimported, name-defined, no-untyped-call"
"""
SyncroJob - Timbrature Page
Page Object Model for the Timbrature section of the ISAB portal.
"""

import shutil
import time
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from typing import Any

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.base.wait_helpers import poll_for_new_file
from src.bots.portale_fornitori.timbrature.locators import TimbratureLocators
from src.core.constants import Timeouts
from src.core.paths import CONFIG_DIR


class TimbraturePage:
    """Encapsulates interactions with the Timbrature page."""

    def __init__(
        self,
        driver: WebDriver,
        log_callback: Callable[[str], None] | None = None,
        download_path: str = "",
    ) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.long_wait = WebDriverWait(driver, Timeouts.PAGE_LOAD)
        self._log = log_callback or print
        self.download_path = download_path

    def log(self, msg: str) -> None:
        """Proxy per il logging."""
        self._log(msg)

    def _wait_for_overlay(self) -> None:
        """Waits for loading overlay to disappear."""
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"

            WebDriverWait(self.driver, Timeouts.OVERLAY).until(
                EC.invisibility_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            self.log("⚠️ Timeout attesa overlay.")

    def navigate_to_timbrature(self) -> bool:
        """Navigates to Report -> Timbrature."""
        try:
            self.log("Navigazione verso pagina Timbrature...")
            report_element = self.wait.until(EC.element_to_be_clickable(TimbratureLocators.REPORT_MENU))
            report_element.click()

            # Keyboard navigation to tab
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.ENTER).perform()
            self._wait_for_overlay()
            return True  # noqa: TRY300
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

            actions = ActionChains(self.driver)

            # Focus Date From
            actions.send_keys(Keys.TAB).pause(0.5)
            if data_da:
                actions.send_keys(data_da).pause(0.5)

            # Focus Date To
            actions.send_keys(Keys.TAB).pause(0.5)
            if data_a:
                actions.send_keys(data_a).pause(0.5)

            # Checkbox "Verifica Presenza Timesheet"
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

            self.log("Caricamento terminato.")
            return True  # noqa: TRY300

        except Exception as e:
            self.log(f"Errore impostazione filtri: {e}")
            return False

    def _select_supplier(self, fornitore: str) -> None:
        """Seleziona il fornitore dal menu a tendina."""
        self.log(f"Seleziono fornitore: {fornitore}")
        try:
            self._wait_for_overlay()

            arrow_element = None
            for _attempt in range(3):
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
                        try:
                            ActionChains(self.driver).move_to_element(arrow_element).click().perform()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", arrow_element)
                        break
                except Exception:
                    with suppress(Exception):
                        pass

            if not arrow_element:
                raise Exception("Impossibile trovare la freccia del fornitore.")  # noqa: TRY002, TRY003, TRY301

            option_xpath = f"//li[contains(text(), '{fornitore}')]"
            option = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, option_xpath))
            )

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)

            try:
                option.click()
            except (ElementClickInterceptedException, Exception):
                self.driver.execute_script("arguments[0].click();", option)
            self._wait_for_overlay()

        except Exception as e:
            self.log(f"⚠️ Errore selezione fornitore: {e}")

    def download_excel(self) -> str:
        """Finds and clicks the Excel download button, returning the file path."""
        try:
            self.log("Cerco pulsante Excel...")
            excel_btn = self._find_excel_button()

            if not excel_btn:
                self.log("⚠️ Pulsante Excel non trovato.")
                return ""

            # Snapshot dei file esistenti prima del click
            source_dir = Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"
            allowed_ext = {".xlsx", ".xls"}
            files_before = {f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() in allowed_ext}

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", excel_btn)

            self.log("Clicco su Excel...")
            try:
                excel_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", excel_btn)

            self.log("Attendo download...")

            # Utilizza helper centralizzato robusto
            res_path = poll_for_new_file(
                directory=source_dir,
                files_before=files_before,
                pattern=["*.xlsx", "*.xls"],
                timeout=Timeouts.DOWNLOAD,
            )

            if not res_path:
                self.log("✗ Download non rilevato o timeout.")
                return ""

            # Spostamento in cartella temp per elaborazione
            dest_dir = CONFIG_DIR / "temp"
            dest_dir.mkdir(parents=True, exist_ok=True)

            downloaded_file = Path(res_path)
            new_path = dest_dir / f"timbrature_{int(time.time())}.xlsx"

            shutil.move(str(downloaded_file), str(new_path))
            self.log(f"✓ File scaricato e preparato: {new_path.name}")
            return str(new_path)

        except Exception as e:
            self.log(f"⚠️ Errore download Excel: {e}")
            return ""

    def _find_excel_button(self) -> Any:
        """Tenta di individuare il pulsante di download Excel."""
        strategies = [
            TimbratureLocators.DOWNLOAD_BTN_TEXT,
            TimbratureLocators.DOWNLOAD_BTN_ICON,
            TimbratureLocators.DOWNLOAD_BTN_ARIA,
        ]

        for locator in strategies:
            try:
                return WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(locator))
            except TimeoutException:
                continue
        return None
