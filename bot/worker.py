import time
import traceback
import logging
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

from utils.config import load_config, get_downloads_path

# --- CONFIGURAZIONE LOGGING ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)-8s - %(message)s")
logger = logging.getLogger(__name__)

LOGIN_URL = "https://portalefornitori.isab.com/Ui/"
FORNITORE_DA_SELEZIONARE = "KK10608 - COEMI S.R.L."

class BotWorker(QThread):
    # Signals to communicate with GUI
    log_signal = Signal(str)
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, download_tasks=None, data_da="01.01.2025", mode="DOWNLOAD", upload_data=None):
        """
        download_tasks: List of tuples [(oda, pos), ...]
        data_da: Start date string (dd.mm.yyyy)
        mode: "DOWNLOAD" or "UPLOAD"
        upload_data: List of dicts (from DB) for upload logic
        """
        super().__init__()
        self.download_tasks = download_tasks or []
        self.data_da = data_da
        self.mode = mode
        self.upload_data = upload_data or []
        self.config = load_config()
        self.driver = None
        self.download_dir = get_downloads_path()

    def run(self):
        try:
            self.log(f"Avvio del Bot (Mode: {self.mode})...")
            self.init_driver()
            self.login()

            if self.mode == "DOWNLOAD" and self.download_tasks:
                self.process_download_tasks()
            elif self.mode == "UPLOAD":
                 self.process_upload_tasks()

            self.log("Operazioni completate. Il browser rimarrà aperto per eventuali ispezioni.")

            # NOTE: User requested browser to stay open.
            # If we exit run(), the thread finishes, but the driver object persists if attached to self.
            # However, if we want to reuse the same browser session for subsequent tasks,
            # we need a more persistent architecture.
            # For this specific task refactoring, I will keep the browser open.

            # To keep the thread alive or just finish the task?
            # User said: "Apro GUI -> Login -> Browser resta aperto -> Poi vado su Attività -> Scarico TS"
            # This implies the browser should be a singleton or persistent resource managed by the App, not just a one-off thread.

            # Since I am refactoring `scaricaTScanoni.py` which was a script, I will currently treat this Worker
            # as the executor of the specific "Scarico TS" action.
            # Ideally, the driver should be initialized once and shared.
            # But for simplicity and stability (handling crashes), re-login or checking login is safer.
            # I will assume for now this worker handles the full flow.
            # If the user wants to keep the session alive across *different* actions triggered separately,
            # we would need a Session Manager.
            # Given requirement 3: "No, la GUI non ha bisogno di accesso login dall'utente. Quando però viene fatta un attività come per esempio Scarico TS in automatico deve partire l'apertura, login ecc.."
            # This suggests it opens, logins, does task.

            self.finished_signal.emit()

        except Exception as e:
            err_msg = f"Errore critico: {str(e)}\n{traceback.format_exc()}"
            self.log(err_msg)
            self.error_signal.emit(err_msg)

    def log(self, message):
        self.log_signal.emit(message)
        logger.info(message)

    def init_driver(self):
        self.log("Inizializzazione WebDriver Chrome...")
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": str(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "safeBrowse.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        # Ensure browser stays open after script finishes
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.popup_wait = WebDriverWait(self.driver, 7)
        self.long_wait = WebDriverWait(self.driver, 15)

    def attendi_scomparsa_overlay(self, timeout_secondi=45):
        try:
            xpath_mask = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            xpath_text = "//div[text()='Caricamento...']"
            WebDriverWait(self.driver, timeout_secondi).until(
                EC.invisibility_of_element_located((By.XPATH, f"{xpath_mask} | {xpath_text}"))
            )
            self.log(" -> Overlay di caricamento scomparso.")
            time.sleep(0.3)
            return True
        except TimeoutException:
            self.log(f"Timeout ({timeout_secondi}s) attesa overlay.")
            return False

    def login(self):
        self.log(f"Navigazione a: {LOGIN_URL}")
        self.driver.get(LOGIN_URL)

        username = self.config.get("username", "")
        password = self.config.get("password", "")

        self.log("Tentativo di login...")
        self.wait.until(EC.presence_of_element_located((By.NAME, "Username"))).send_keys(username)
        self.wait.until(EC.presence_of_element_located((By.NAME, "Password"))).send_keys(password)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Accedi' and contains(@class, 'x-btn-inner')]"))).click()

        self.attendi_scomparsa_overlay(60)

        # Pop-up handling
        try:
            ok_button_popup = self.popup_wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='OK' and contains(@class, 'x-btn-inner')]")))
            self.log("Pop-up 'OK' trovato. Click...")
            ok_button_popup.click()
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, "//span[text()='OK' and contains(@class, 'x-btn-inner')]")))
        except TimeoutException:
            pass

        self.log("Login completato.")

    def process_download_tasks(self):
        self.log("Inizio procedura Scarico TS...")

        # Navigation to Timesheet
        self.log("Navigazione menu Report -> Timesheet...")
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Report']"))).click()
            self.attendi_scomparsa_overlay()

            timesheet_menu_xpath = "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, timesheet_menu_xpath))).click()
            self.attendi_scomparsa_overlay()
            self.log("Pagina Timesheet caricata.")
        except Exception as e:
            raise Exception(f"Fallimento navigazione menu: {str(e)}")

        # Fornitore & Data Setup
        self.setup_filters()

        # Loop processing
        files_before_download = {f for f in self.download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}

        js_dispatch_events = """
        var el = arguments[0]; var ev_in = new Event('input', {bubbles:true}); el.dispatchEvent(ev_in);
        var ev_ch = new Event('change', {bubbles:true}); el.dispatchEvent(ev_ch);"""

        for oda, pos in self.download_tasks:
            self.log(f"Processo: OdA='{oda}', Pos='{pos}'")
            try:
                campo_numero_oda = self.wait.until(EC.presence_of_element_located((By.NAME, "NumeroOda")))
                self.driver.execute_script("arguments[0].value = arguments[1];", campo_numero_oda, oda)
                self.driver.execute_script(js_dispatch_events, campo_numero_oda)

                campo_posizione_oda = self.wait.until(EC.presence_of_element_located((By.NAME, "PosizioneOda")))
                self.driver.execute_script("arguments[0].value = '';", campo_posizione_oda)
                self.driver.execute_script("arguments[0].value = arguments[1];", campo_posizione_oda, pos)
                self.driver.execute_script(js_dispatch_events, campo_posizione_oda)

                # Click Cerca
                pulsante_cerca_xpath = "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Cerca' and contains(@class, 'x-btn-inner')]]"
                self.wait.until(EC.element_to_be_clickable((By.XPATH, pulsante_cerca_xpath))).click()

                self.attendi_scomparsa_overlay(90)

                # Download Excel
                excel_button_xpath = "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]"
                self.wait.until(EC.element_to_be_clickable((By.XPATH, excel_button_xpath))).click()
                self.log("  Download avviato...")

                downloaded_file_path = None
                download_start_time = time.time()
                while time.time() - download_start_time < 25:
                    current_files = {f for f in self.download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}
                    new_files = current_files - files_before_download
                    if new_files:
                        downloaded_file_path = max(list(new_files), key=lambda f: f.stat().st_mtime)
                        break
                    time.sleep(0.5)

                if downloaded_file_path:
                    # Rename file logic
                    nome_base_pos = f"-{pos}" if pos else ""
                    nuovo_nome = f"{oda}{nome_base_pos}.xlsx"
                    dest_path = self.download_dir / nuovo_nome

                    # Handle duplicates
                    counter = 1
                    while dest_path.exists():
                        dest_path = self.download_dir / f"{oda}{nome_base_pos}_{counter}.xlsx"
                        counter += 1

                    try:
                        downloaded_file_path.rename(dest_path)
                        self.log(f"  File salvato: {dest_path.name}")
                        # Update files_before_download to include this new file so next iteration works
                        files_before_download.add(dest_path)
                    except Exception as e_rename:
                        self.log(f"  Errore rinomina: {e_rename}")
                else:
                    self.log("  Timeout download.")

            except Exception as e:
                self.log(f"  Errore riga {oda}: {e}")
                traceback.print_exc()

    def setup_filters(self):
        self.log("Impostazione filtri (Fornitore, Data)...")
        fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"

        try:
            fornitore_arrow_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath)))
            ActionChains(self.driver).move_to_element(fornitore_arrow_element).click().perform()

            coemi_srl_option_xpath = f"//li[normalize-space(text())='{FORNITORE_DA_SELEZIONARE}']"
            coemi_srl_option = self.long_wait.until(EC.presence_of_element_located((By.XPATH, coemi_srl_option_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", coemi_srl_option)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", coemi_srl_option)

            self.attendi_scomparsa_overlay()

            campo_data_da = self.wait.until(EC.visibility_of_element_located((By.NAME, "DataTimesheetDa")))
            campo_data_da.clear()
            campo_data_da.send_keys(self.data_da)
        except Exception as e:
             raise Exception(f"Errore setup filtri: {str(e)}")

    def process_upload_tasks(self):
        self.log("Inizio procedura Carico TS...")

        # 1. Timesheet
        try:
            self.log("Click su 'Timesheet'...")
            # Using text based xpath as ID 1035 might be dynamic
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Timesheet']"))).click()
            self.attendi_scomparsa_overlay()
        except Exception as e:
            raise Exception(f"Errore navigazione Timesheet: {e}")

        # 2. Gestione Timesheet
        try:
            self.log("Click su 'Gestione Timesheet'...")
            # Look for button containing text
            xpath_gestione = "//span[contains(@class, 'x-btn-inner') and normalize-space(text())='Gestione Timesheet']"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_gestione))).click()
            self.attendi_scomparsa_overlay()
        except Exception as e:
            raise Exception(f"Errore navigazione Gestione Timesheet: {e}")

        # 3. Apri elenco (Fornitore)
        try:
            self.log("Selezione Fornitore 'COEMI'...")
            xpath_trigger = "//div[contains(@class, 'x-form-trigger') and contains(@class, 'x-form-trigger-default')]"

            # Use JS click to prevent double-click issues on sensitive ExtJS triggers
            trigger = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_trigger)))
            self.driver.execute_script("arguments[0].click();", trigger)

            # 4. Select Option
            coemi_xpath = f"//li[contains(text(), 'KK10608 - COEMI S.R.L.')]"
            option = self.long_wait.until(EC.element_to_be_clickable((By.XPATH, coemi_xpath)))
            self.driver.execute_script("arguments[0].click();", option) # Also use JS for option to be safe/fast

            self.attendi_scomparsa_overlay()
        except Exception as e:
            raise Exception(f"Errore selezione Fornitore: {e}")

        # Loop through rows from Database
        if not self.upload_data:
            self.log("Nessun dato trovato nel database per il Carico TS.")
            return

        # For now, we only process the first row as per implicit flow, or loop?
        # User said "lo prendi dal database partendo dalla riga 1"
        # and "continua con altre logiche che ti dirò dopo".
        # I'll loop but maybe break after first or just do the entry part.

        js_dispatch_events = """
        var el = arguments[0]; var ev_in = new Event('input', {bubbles:true}); el.dispatchEvent(ev_in);
        var ev_ch = new Event('change', {bubbles:true}); el.dispatchEvent(ev_ch);"""

        for idx, row_data in enumerate(self.upload_data):
            oda = row_data.get("numero_oda", "").strip()
            if not oda:
                self.log(f"Riga {idx+1}: Numero OdA mancante, salto.")
                continue

            self.log(f"Elaborazione Riga {idx+1}: Inserimento OdA '{oda}'...")

            try:
                # 5. Inserisci Numero OdA
                # Looking for input field. User ID: input#textfield-1177-inputEl
                # Better: Input with name or label?
                # Assuming it's the main text field that appears after selecting provider.
                # Let's try finding by class x-form-field
                # Or try to find by label if exists.
                # Fallback to generic text input if specific ID not reliable.
                # But typically OdA field has name="NumeroOda" or similar in ExtJS?
                # In 'process_download_tasks' we used By.NAME, "NumeroOda".
                # If this is the same 'Gestione Timesheet' page structure, it might have a name.
                # If not, let's look for an input that is visible.

                xpath_input = "//input[contains(@class, 'x-form-field') and contains(@class, 'x-form-text')]"
                # There might be multiple. "Posizione" might be there too?
                # User specifically pointed to one input.
                # Let's assume it's the first visible one or try to match the ID pattern if stable? No.
                # Let's try name 'NumeroOda' first as it's consistent in other parts.

                try:
                    input_oda = self.wait.until(EC.visibility_of_element_located((By.NAME, "NumeroOda")))
                except:
                    # If name not found, try the xpath and hope it's the right one
                    inputs = self.driver.find_elements(By.XPATH, xpath_input)
                    # Filter visible
                    visible_inputs = [i for i in inputs if i.is_displayed()]
                    if visible_inputs:
                        input_oda = visible_inputs[0] # Assume first
                    else:
                        raise Exception("Campo Input OdA non trovato")

                input_oda.clear()
                self.driver.execute_script("arguments[0].value = arguments[1];", input_oda, oda)
                self.driver.execute_script(js_dispatch_events, input_oda)

                # 6. Estrai OdA
                self.log("Click su 'Estrai OdA'...")
                xpath_estrai = "//span[contains(@class, 'x-btn-inner') and normalize-space(text())='Estrai OdA']"
                btn_estrai = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_estrai)))
                btn_estrai.click()

                self.attendi_scomparsa_overlay()

                self.log(f"Estrai OdA cliccato per OdA {oda}.")

                # PAUSE HERE for further instructions or next steps
                # For now, just a small sleep to let user see
                time.sleep(2)

            except Exception as e:
                self.log(f"Errore elaborazione OdA {oda}: {e}")
                traceback.print_exc()
                # Break or Continue?
                # If one fails, maybe stop?
                break
