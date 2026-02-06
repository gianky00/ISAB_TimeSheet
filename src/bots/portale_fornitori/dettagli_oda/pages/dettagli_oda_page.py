"""
SyncroJob - Dettagli OdA Page
Page Object Model for Dettagli OdA.
"""

import time
import traceback
from contextlib import suppress
from pathlib import Path
from typing import Callable, Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.portale_fornitori.common.locators import CommonLocators, LoginLocators
from src.bots.portale_fornitori.dettagli_oda.locators import DettagliOdALocators
from src.core.constants import Timeouts
from src.utils.helpers import sanitize_filename


class DettagliOdAPage:
    """
    Page Object Model per la gestione della pagina Dettagli OdA (Ordini di Acquisto).
    Fornisce metodi per navigare, filtrare ed esportare i dettagli degli ordini.
    """

    def __init__(
        self, driver: WebDriver, log_callback: Optional[Callable[[str], None]] = None
    ):
        """
        Inizializza la pagina con il driver Selenium e la callback di log.

        Args:
            driver: Istanza di WebDriver.
            log_callback: Callback opzionale per l'output dei log.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.long_wait = WebDriverWait(driver, Timeouts.PAGE_LOAD)
        self._log = log_callback or print

    def log(self, msg: str):
        """Inoltra un messaggio alla callback di log configurata."""
        self._log(msg)

    def _wait_for_overlay(self):
        """Attende che gli overlay di caricamento di ExtJS (maschere) siano invisibili."""
        with suppress(TimeoutException):
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            WebDriverWait(self.driver, Timeouts.OVERLAY).until(
                EC.invisibility_of_element_located((By.XPATH, xpath))
            )

    def navigate_to_dettagli(self, is_first_row: bool = True) -> bool:
        """
        Naviga nel menu del portale fino alla pagina dei Dettagli OdA.

        Args:
            is_first_row: Se True, esegue un click singolo, altrimenti tenta il doppio click per robustezza.
        Returns:
            bool: True se la navigazione ha avuto successo.
        """
        try:
            self.expand_sidebar_if_collapsed()
            self.log("Navigazione menu Report -> Oda...")

            # Click Report (using JS to avoid interception/crash)
            # Dalla seconda riga in poi, a volte è necessario cliccare due volte
            report_btn = self.wait.until(
                EC.element_to_be_clickable(DettagliOdALocators.REPORT_MENU)
            )
            self.driver.execute_script("arguments[0].click();", report_btn)

            if not is_first_row:
                # Strategia robustezza: piccolo sleep e secondo click se necessario
                self.driver.execute_script("arguments[0].click();", report_btn)

            self._wait_for_overlay()

            # Click Oda
            oda_btn = self.wait.until(
                EC.element_to_be_clickable(DettagliOdALocators.DETTAGLI_MENU)
            )
            self.driver.execute_script("arguments[0].click();", oda_btn)

            self.wait.until(
                EC.visibility_of_element_located(DettagliOdALocators.SUPPLIER_ARROW)
            )
            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"✗ Navigazione fallita: {e}")
            self.log(f"Stacktrace: {traceback.format_exc()}")
            return False

    def setup_supplier(self, supplier: str) -> bool:
        """
        Seleziona il fornitore dal menu a discesa della pagina.

        Args:
            supplier: Nome del fornitore da selezionare.
        Returns:
            bool: True se la selezione ha avuto successo.
        """
        try:
            self.log(f"Selezione fornitore: {supplier}")
            arrow = self.wait.until(
                EC.element_to_be_clickable(DettagliOdALocators.SUPPLIER_ARROW)
            )
            ActionChains(self.driver).move_to_element(arrow).click().perform()

            option_xpath = f"//li[contains(text(), '{supplier}')]"
            option = self.long_wait.until(
                EC.presence_of_element_located((By.XPATH, option_xpath))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'nearest'});", option
            )
            self.driver.execute_script("arguments[0].click();", option)
            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"✗ Selezione fornitore fallita: {e}")
            return False

    def logout(self):
        """Esegue la procedura di logout specifica per questa area del portale."""
        try:
            self.log("Esecuzione logout...")
            # 1. Click Settings (using specific ID provided)
            settings_btn = self.wait.until(
                EC.element_to_be_clickable(DettagliOdALocators.LOGOUT_SETTINGS_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", settings_btn)
            try:
                logout_btn = self.wait.until(
                    EC.visibility_of_element_located(CommonLocators.LOGOUT_OPTION)
                )
                self.driver.execute_script("arguments[0].click();", logout_btn)
            except TimeoutException:
                self.log("  ✗ Opzione Logout non apparsa nel menu.")
                return

            # 3. Handle Confirmation Popup "Si" (using specific locator provided)
            try:
                self.log("  Attesa conferma logout...")
                # Click "Si" directly if visible
                yes_btn = self.wait.until(
                    EC.element_to_be_clickable(DettagliOdALocators.LOGOUT_CONFIRM_YES)
                )
                self.driver.execute_script("arguments[0].click();", yes_btn)
                self.log("  Conferma cliccata.")

                # Wait for Login Screen (logout complete)
                self.wait.until(
                    EC.visibility_of_element_located(LoginLocators.USERNAME_FIELD)
                )
                self.log("✓ Logout completato con successo.")

            except TimeoutException:
                self.log("⚠️ Popup conferma non apparso o timeout.")
        except Exception as e:
            self.log(f"⚠️ Errore durante logout: {e}")

    def expand_sidebar_if_collapsed(self):
        """Espande la sidebar se collassata per rendere visibile il menu Report."""
        with suppress(Exception):
            # Cerca l'elemento di espansione
            expand_btn = self.driver.find_element(
                *DettagliOdALocators.SIDEBAR_EXPAND_BUTTON
            )
            if expand_btn.is_displayed():
                self.log("  Menu laterale collassato, espansione in corso...")
                # Usa JS click per robustezza
                self.driver.execute_script("arguments[0].click();", expand_btn)
                self.log("  Menu espanso.")

    def process_oda(
        self,
        oda: str,
        contract: str,
        date_da: str,
        date_a: str,
        source_dir: Path,
        dest_dir: Path,
    ) -> Optional[Path]:
        """
        Compila il form di ricerca per un OdA e avvia l'esportazione dei dati.

        Args:
            oda: Numero OdA (opzionale).
            contract: Numero contratto.
            date_da: Data inizio (gg.mm.aaaa).
            date_a: Data fine (gg.mm.aaaa).
            source_dir: Directory di download del browser.
            dest_dir: Directory di destinazione finale.
        Returns:
            Optional[Path]: Il percorso del file scaricato se successo, altrimenti None.
        """
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
                field_oda = self.wait.until(
                    EC.presence_of_element_located(DettagliOdALocators.ODA_NUMBER_FIELD)
                )
                self.driver.execute_script(js_set_value, field_oda, oda)

            # Date From (Clear first by setting value)
            field_date_da = self.wait.until(
                EC.presence_of_element_located(DettagliOdALocators.DATE_FROM_FIELD)
            )
            self.driver.execute_script(js_set_value, field_date_da, date_da)

            # Date To
            field_date_a = self.wait.until(
                EC.presence_of_element_located(DettagliOdALocators.DATE_A_FIELD)
            )
            self.driver.execute_script(js_set_value, field_date_a, date_a)

            # Contract
            field_contract = self.wait.until(
                EC.presence_of_element_located(DettagliOdALocators.CONTRACT_FIELD)
            )
            self.driver.execute_script(js_set_value, field_contract, contract)

            # Checkbox
            checkbox = self.wait.until(
                EC.presence_of_element_located(DettagliOdALocators.CHECKBOX_FIELD)
            )
            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(
                EC.element_to_be_clickable(DettagliOdALocators.SEARCH_BUTTON)
            ).click()
            self.log("  Cerca cliccato...")
            self._wait_for_overlay()

            # Check Results Count
            try:
                count_label = self.wait.until(
                    EC.visibility_of_element_located(
                        DettagliOdALocators.RESULTS_COUNT_LABEL
                    )
                )
                count_text = count_label.text.strip()  # "Trovati : 676"
                if ":" in count_text:
                    count = int(count_text.split(":")[-1].strip())
                    self.log(f"  Risultati trovati: {count}")
                    if count == 0:
                        self.log("  Nessun risultato. Salto esportazione.")
                        self._close_all_tabs()
                        # Return dummy True or None? Logic expects Path or False.
                        # If no results, we technically finished "processing" but no file.
                        return None
                else:
                    self.log(f"  ⚠️ Impossibile parsare risultati: {count_text}")
            except Exception as e:
                self.log(f"  ⚠️ Errore lettura conteggio: {e}")

            # Decide Export Method based on ODA presence
            target_filename = ""
            if oda:
                # ODA Present: Details Export
                self.log("  Apertura dettagli (OdA specifico)...")
                details_btn = self.wait.until(
                    EC.element_to_be_clickable(DettagliOdALocators.DETAILS_ICON)
                )
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
                # Normalizza la data per il filename: GG.MM.AAAA -> GG-MM-AAAA
                safe_date_a = date_a.replace(".", "-").replace("/", "-")
                target_filename = f"ODA_Generale_al_{safe_date_a}.xlsx"

            # Export and Download (using source and dest dirs)
            final_path = self._download(
                source_dir, dest_dir, target_filename, export_btn_locator
            )

            # Cleanup
            self._close_all_tabs()
            return final_path

        except Exception as e:
            self.log(f"  ✗ Errore processamento: {e}")
            self.log(f"Stacktrace: {traceback.format_exc()}")
            # Ensure tabs are closed even on error
            with suppress(Exception):
                self._close_all_tabs()
            return None

    def _close_all_tabs(self):
        """Chiude tutte le schede aperte nel portale cliccando sull'icona X."""
        try:
            # Find all close buttons. We might need to iterate or they might be dynamic.
            # Usually ExtJS tabs have a close tool.
            # We assume clicking them one by one works.
            # Warning: clicking one might change the DOM for others.
            # It's safer to find one, click, wait, repeat until none found.
            while True:
                try:
                    # Find *visible* close buttons only
                    close_btn = self.driver.find_element(
                        *DettagliOdALocators.TAB_CLOSE_BTN
                    )
                    if close_btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", close_btn)
                    else:
                        break
                except Exception:
                    # No more close buttons found
                    break
        except Exception as e:
            self.log(f"  ⚠️ Errore chiusura tab: {e}")

    def _download(
        self,
        source_dir: Path,
        dest_dir: Path,
        target_filename: str,
        button_locator: tuple,
    ) -> Optional[Path]:
        """Esegue il download, attende il file e lo sposta nella cartella finale."""
        try:
            # Normalize path to handle forward/backward slashes
            source_dir = Path(source_dir).resolve()
            self.log(f"  [DEBUG] Cerco file in: {source_dir}")

            if not source_dir.exists():
                self.log(f"  ✗ Cartella non esiste: {source_dir}")
                return None

            files_before = {
                f
                for f in source_dir.iterdir()
                if f.is_file() and f.suffix.lower() == ".xlsx"
            }
            self.log(f"  [DEBUG] File .xlsx prima del download: {len(files_before)}")

            if not self._click_export_button(button_locator):
                return None

            downloaded_file = self._wait_for_download(source_dir, files_before)
            if not downloaded_file:
                # Debug: lista file attuali
                current_files = (
                    list(source_dir.iterdir()) if source_dir.exists() else []
                )
                self.log(
                    f"  [DEBUG] File attuali nella cartella: {[f.name for f in current_files[:10]]}"
                )
                self.log("  ✗ File non trovato nella cartella Download.")
                return None

            return self._finalize_download(downloaded_file, dest_dir, target_filename)
        except Exception as e:
            self.log(f"  ✗ Errore download: {e}")
            return None

    def _click_export_button(self, locator: tuple) -> bool:
        """Tenta di cliccare il pulsante di esportazione Excel gestendo intercettazioni."""
        try:
            btn = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", btn
            )
            try:
                btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
            return True
        except Exception:
            return False

    def _wait_for_download(self, source_dir: Path, files_before: set) -> Optional[Path]:
        """Attende il completamento del download monitorando la directory sorgente."""
        start = time.time()
        while time.time() - start < Timeouts.DOWNLOAD:
            if any(f.suffix == ".crdownload" for f in source_dir.iterdir()):
                continue

            current = {
                f
                for f in source_dir.iterdir()
                if f.is_file() and f.suffix.lower() == ".xlsx"
            }
            new_files = current - files_before
            if new_files:
                return max(list(new_files), key=lambda f: f.stat().st_mtime)
        return None

    def _finalize_download(
        self, src: Path, dest_dir: Path, target_name: str
    ) -> Optional[Path]:
        """Sposta il file scaricato nella destinazione finale rinominandolo."""
        import shutil

        dest_dir.mkdir(parents=True, exist_ok=True)
        target_path = dest_dir / target_name

        if target_path.exists():
            with suppress(Exception):
                target_path.unlink()

        shutil.move(str(src), str(target_path))
        self.log(f"  ✓ Scaricato: {target_path.name}")
        return target_path
