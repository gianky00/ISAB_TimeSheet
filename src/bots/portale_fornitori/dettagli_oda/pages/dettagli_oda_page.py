"""
SyncroJob - Dettagli OdA Page
Page Object Model for Dettagli OdA.
"""

import shutil
import time
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.wait import WebDriverWait

from src.bots.base.wait_helpers import PollConfig, poll_for_new_file
from src.bots.portale_fornitori.common.locators import CommonLocators, LoginLocators
from src.bots.portale_fornitori.dettagli_oda.locators import DettagliOdALocators
from src.core.constants import Timeouts
from src.utils.helpers import cleanup_chrome_temp_files, sanitize_filename


class DettagliOdAPage:
    """
    Page Object Model per la gestione della pagina Dettagli OdA (Ordini di Acquisto).
    Fornisce metodi per navigare, filtrare ed esportare i dettagli degli ordini.
    """

    def __init__(self, driver: WebDriver, log_callback: Callable[[str], None] | None = None) -> None:
        """Inizializza la pagina con il driver Selenium e la callback di log."""
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.long_wait = WebDriverWait(driver, Timeouts.PAGE_LOAD)
        self._log = log_callback or print

    def log(self, msg: str) -> None:
        """Inoltra un messaggio alla callback di log configurata."""
        self._log(msg)

    def _wait_for_overlay(self, timeout: int | None = None, wait_for_appearance: bool = False) -> None:
        """
        Attende che gli overlay di caricamento di ExtJS (maschere) siano invisibili.

        Args:
          timeout: Secondi massimi di attesa. Default: Timeouts.OVERLAY.
          wait_for_appearance: Se True, attende prima che l'overlay appaia (max 2s)
                     e poi che scompaia. Evita race conditions.
        """
        t = timeout or Timeouts.OVERLAY
        xpath = (
            "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')]"
            "[not(contains(@style,'display: none'))]"
        )

        if wait_for_appearance:
            with suppress(TimeoutException):
                wait_for_appearance_sec = 2
                WebDriverWait(self.driver, wait_for_appearance_sec).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )

        with suppress(TimeoutException):
            WebDriverWait(self.driver, t).until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    def navigate_to_dettagli(self, is_first_row: bool = True) -> bool:
        """Naviga nel menu del portale fino alla pagina dei Dettagli OdA."""
        try:
            self.expand_sidebar_if_collapsed()
            self.log("Navigazione menu Report -> Oda...")

            report_btn = self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.REPORT_MENU))
            self.driver.execute_script("arguments[0].click();", report_btn)

            if not is_first_row:
                self.driver.execute_script("arguments[0].click();", report_btn)

            self._wait_for_overlay()

            oda_btn = self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.DETTAGLI_MENU))
            self.driver.execute_script("arguments[0].click();", oda_btn)

            self.wait.until(EC.visibility_of_element_located(DettagliOdALocators.SUPPLIER_ARROW))
            self._wait_for_overlay()
        except Exception as e:
            self.log(f"  Navigazione fallita: {e}")
            return False
        else:
            return True

    def setup_supplier(self, supplier: str) -> bool:
        """
        Seleziona il fornitore dal menu a discesa della pagina o tramite inserimento diretto.

        Args:
            supplier: Ragione sociale del fornitore.

        Returns:
            bool: True se la selezione ha successo, False altrimenti.
        """
        try:
            self.log(f"Selezione fornitore: {supplier}")

            # Controlliamo se la freccia fisica esiste e proviamo a cliccarla
            has_arrow = False
            try:
                arrow = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(DettagliOdALocators.SUPPLIER_ARROW)
                )
                has_arrow = True
            except Exception:
                has_arrow = False

            if has_arrow:
                ActionChains(self.driver).move_to_element(arrow).click().perform()

                option_xpath = f"//li[contains(text(), '{supplier}')]"
                option = self.long_wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)
                self.driver.execute_script("arguments[0].click();", option)
            else:
                # Inserimento diretto nell'input (senza freccia fisica)
                self.log("   Freccia non rilevata. Tento l'inserimento manuale forzato.")
                inp = self.wait.until(EC.visibility_of_element_located(DettagliOdALocators.SUPPLIER_INPUT))

                try:
                    inp.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", inp)

                self.driver.execute_script("arguments[0].value = '';", inp)
                inp.send_keys(supplier)
                time.sleep(0.5)
                inp.send_keys(Keys.ENTER)

            self._wait_for_overlay()
        except Exception as e:
            self.log(f"  Selezione fornitore fallita: {e}")
            return False
        else:
            return True

    def logout(self) -> bool:
        """Esegue la procedura di logout specifica per questa area del portale."""
        try:
            self.log("Esecuzione logout...")
            settings_btn = self.wait.until(
                EC.element_to_be_clickable(DettagliOdALocators.LOGOUT_SETTINGS_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", settings_btn)
            try:
                logout_btn = self.wait.until(EC.visibility_of_element_located(CommonLocators.LOGOUT_OPTION))
                self.driver.execute_script("arguments[0].click();", logout_btn)
            except TimeoutException:
                self.log("   Opzione Logout non apparsa nel menu.")
                return False

            try:
                self.log(" Attesa conferma logout...")
                yes_btn = self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.LOGOUT_CONFIRM_YES))
                self.driver.execute_script("arguments[0].click();", yes_btn)
                self.log(" Conferma cliccata.")
                self.wait.until(EC.visibility_of_element_located(LoginLocators.USERNAME_FIELD))
                self.log("  Logout completato con successo.")
            except TimeoutException:
                self.log("⚠️ Popup conferma non apparso o timeout.")
                return False
            else:
                return True
        except Exception as e:
            self.log(f"⚠️ Errore durante logout: {e}")
            return False

    def expand_sidebar_if_collapsed(self) -> None:
        """Espande la sidebar se collassata per rendere visibile il menu Report."""
        with suppress(Exception):
            expand_btn = self.driver.find_element(*DettagliOdALocators.SIDEBAR_EXPAND_BUTTON)
            if expand_btn.is_displayed():
                self.log(" Menu laterale collassato, espansione in corso...")
                self.driver.execute_script("arguments[0].click();", expand_btn)
                self.log(" Menu espanso.")

    def process_oda(  # noqa: PLR0913, PLR0915
        self,
        oda: str,
        contract: str,
        date_da: str,
        date_a: str,
        source_dir: Path,
        dest_dir: Path,
    ) -> Path | None:
        """Compila il form di ricerca per un OdA e avvia l'esportazione dei dati."""
        try:
            js_set_value = """
        var el = arguments[0];
        el.value = arguments[1];
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.blur();
      """

            if oda:
                field_oda = self.wait.until(
                    EC.presence_of_element_located(DettagliOdALocators.ODA_NUMBER_FIELD)
                )
                self.driver.execute_script(js_set_value, field_oda, oda)

            field_date_da = self.wait.until(
                EC.presence_of_element_located(DettagliOdALocators.DATE_FROM_FIELD)
            )
            self.driver.execute_script(js_set_value, field_date_da, date_da)

            field_date_a = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.DATE_A_FIELD))
            self.driver.execute_script(js_set_value, field_date_a, date_a)

            if contract:
                self.log(f" Inserimento contratto: {contract}")
                field_contract = self.wait.until(
                    EC.presence_of_element_located(DettagliOdALocators.CONTRACT_FIELD)
                )
                self.driver.execute_script(js_set_value, field_contract, contract)

            checkbox = self.wait.until(EC.presence_of_element_located(DettagliOdALocators.CHECKBOX_FIELD))
            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.SEARCH_BUTTON)).click()
            self.log(" Cerca cliccato...")
            self._wait_for_overlay(wait_for_appearance=True)

            try:
                count_label = self.wait.until(
                    EC.visibility_of_element_located(DettagliOdALocators.RESULTS_COUNT_LABEL)
                )
                count_text = count_label.text.strip()
                if ":" in count_text:
                    count = int(count_text.split(":")[-1].strip())
                    self.log(f" Risultati trovati: {count}")
                    empty_count = 0
                    if count == empty_count:
                        self.log(" Nessun risultato. Salto esportazione.")
                        self._close_all_tabs()
                        return None
            except Exception as e:
                self.log(f" ⚠️ Errore lettura conteggio: {e}")

            target_filename = ""
            if oda:
                self.log(" Apertura dettagli (OdA specifico)...")
                details_btn = self.wait.until(EC.element_to_be_clickable(DettagliOdALocators.DETAILS_ICON))
                self.driver.execute_script("arguments[0].click();", details_btn)
                self._wait_for_overlay()
                export_btn_locator = DettagliOdALocators.EXPORT_EXCEL_TEXT
                target_filename = f"dettaglio_oda_{sanitize_filename(oda)}.xlsx"
            else:
                self.log(" Esportazione lista generale...")
                export_btn_locator = DettagliOdALocators.GENERAL_EXPORT_BUTTON
                safe_date_a = date_a.replace(".", "-").replace("/", "-")
                target_filename = f"ODA_Generale_al_{safe_date_a}.xlsx"

            final_path = self._download(source_dir, dest_dir, target_filename, export_btn_locator)
            self._close_all_tabs()
        except Exception as e:
            self.log(f"   Errore processamento: {e}")
            with suppress(Exception):
                self._close_all_tabs()
            return None
        else:
            return final_path

    def _close_all_tabs(self) -> None:
        """Chiude tutte le schede aperte nel portale cliccando sull'icona X."""
        try:
            while True:
                try:
                    close_btn = self.driver.find_element(*DettagliOdALocators.TAB_CLOSE_BTN)
                    if close_btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", close_btn)
                    else:
                        break
                except Exception:
                    break
        except Exception as e:
            self.log(f" ⚠️ Errore chiusura tab: {e}")

    def _download(
        self,
        source_dir: Path,
        dest_dir: Path,
        target_filename: str,
        button_locator: tuple[str, str],
    ) -> Path | None:
        """Esegue il download, attende il file e lo sposta nella cartella finale."""
        try:
            source_dir = Path(source_dir).resolve()
            if not source_dir.exists():
                self.log(f"   Cartella non esiste: {source_dir}")
                # Tentiamo di crearla se possibile
                try:
                    source_dir.mkdir(parents=True, exist_ok=True)
                    self.log(f"   Cartella creata: {source_dir}")
                except Exception:
                    return None

            self.log(f" [CERCA] Monitoraggio download in: {source_dir}")
            allowed_extensions = {".xlsx", ".xls"}
            files_before = {
                f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() in allowed_extensions
            }

            if not self._click_export_button(button_locator):
                self.log("   Impossibile cliccare il pulsante di esportazione.")
                return None

            # Attesa overlay post-click esportazione (generazione file sul portale)
            self._wait_for_overlay(wait_for_appearance=True)

            # Attesa download tramite helper centralizzato robusto
            config = PollConfig(
                directory=source_dir,
                pattern=["*.xlsx", "*.xls"],
                timeout=Timeouts.DOWNLOAD,
            )
            res_path = poll_for_new_file(
                config=config,
                files_before=files_before,
            )

            if not res_path:
                self.log(f"   Nessun nuovo file Excel trovato in {source_dir} dopo {Timeouts.DOWNLOAD}s.")
                return None

            downloaded_file = Path(res_path)
            final_path = self._finalize_download(downloaded_file, dest_dir, target_filename)

            # Pulizia aggressiva residui 0 KB (post-download)
            time.sleep(Timeouts.UI_DELAY)

            removed = cleanup_chrome_temp_files(source_dir)
            for f_name in removed:
                self.log(f" [DEBUG] Rimosso residuo download: {f_name}")

        except Exception as e:
            self.log(f"   Errore download: {e}")
            return None
        else:
            return final_path

    def _click_export_button(self, locator: tuple[str, str]) -> bool:
        """Tenta di cliccare il pulsante di esportazione Excel gestendo intercettazioni."""
        try:
            btn = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            # Piccola attesa post-scroll
            time.sleep(Timeouts.UI_DELAY)
            try:
                btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
        except Exception as e:
            self.log(f" ⚠️ Errore click esportazione: {e}")
            return False
        else:
            return True

    def _finalize_download(self, src: Path, dest_dir: Path, target_name: str) -> Path | None:
        """Sposta il file scaricato nella destinazione finale rinominandolo."""
        dest_dir.mkdir(parents=True, exist_ok=True)
        target_path = dest_dir / target_name
        if target_path.exists():
            with suppress(Exception):
                target_path.unlink()
        shutil.move(str(src), str(target_path))
        self.log(f"   Scaricato: {target_path.name}")
        return target_path
