import time
import traceback
import logging
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from utils.config import load_config, get_downloads_path
from utils.database import update_activity_status

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
    # Signal per aggiornare la vista database
    refresh_db_signal = Signal()

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
        self.short_wait = WebDriverWait(self.driver, 5)

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

        # Pop-up "Sessione attiva" - clicca su "Si"
        try:
            # Cerca il popup con messaggio "Esiste già una sessione attiva"
            si_button_xpath = "//span[text()='Si' and contains(@class, 'x-btn-inner')]/ancestor::a[contains(@class, 'x-btn')]"
            si_button = self.popup_wait.until(EC.element_to_be_clickable((By.XPATH, si_button_xpath)))
            self.log("Pop-up 'Sessione attiva' trovato. Click su 'Si'...")
            si_button.click()
            self.attendi_scomparsa_overlay(10)
        except TimeoutException:
            pass

        # Pop-up handling generico "OK"
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
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Timesheet']"))).click()
            self.attendi_scomparsa_overlay()
        except Exception as e:
            raise Exception(f"Errore navigazione Timesheet: {e}")

        # 2. Gestione Timesheet
        try:
            self.log("Click su 'Gestione Timesheet'...")
            xpath_gestione = "//span[contains(@class, 'x-btn-inner') and normalize-space(text())='Gestione Timesheet']"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_gestione))).click()
            self.attendi_scomparsa_overlay()
        except Exception as e:
            raise Exception(f"Errore navigazione Gestione Timesheet: {e}")

        # 3. Selezione Fornitore COEMI
        try:
            self.log("Selezione Fornitore 'COEMI'...")
            self.seleziona_fornitore_upload()
        except Exception as e:
            raise Exception(f"Errore selezione Fornitore: {e}")

        # Loop through rows from Database
        if not self.upload_data:
            self.log("Nessun dato trovato nel database per il Carico TS.")
            return

        js_dispatch_events = """
        var el = arguments[0]; var ev_in = new Event('input', {bubbles:true}); el.dispatchEvent(ev_in);
        var ev_ch = new Event('change', {bubbles:true}); el.dispatchEvent(ev_ch);"""

        # Traccia gli OdA che hanno dato errore per evitare chiamate ripetute
        oda_con_errore = set()
        ultimo_oda_estratto = None

        for idx, row_data in enumerate(self.upload_data):
            activity_id = row_data.get("id")
            stato_attuale = row_data.get("stato", "da_processare")
            
            # Salta righe già processate
            if stato_attuale == "completato":
                self.log(f"Riga {idx+1}: Già completata, salto.")
                continue
            
            if stato_attuale and stato_attuale.startswith("errore"):
                self.log(f"Riga {idx+1}: Già in errore, salto.")
                continue
                
            oda = row_data.get("numero_oda", "").strip()
            data_ts = row_data.get("data_ts", "").strip()
            codice_fiscale = row_data.get("codice_fiscale", "").strip()
            
            if not oda:
                self.log(f"Riga {idx+1}: Numero OdA mancante, salto.")
                if activity_id:
                    update_activity_status(activity_id, "errore: numero OdA mancante")
                    self.refresh_db_signal.emit()
                continue

            if not data_ts:
                self.log(f"Riga {idx+1}: Data TS mancante, salto.")
                if activity_id:
                    update_activity_status(activity_id, "errore: data TS mancante")
                    self.refresh_db_signal.emit()
                continue

            if not codice_fiscale:
                self.log(f"Riga {idx+1}: Codice Fiscale mancante, salto.")
                if activity_id:
                    update_activity_status(activity_id, "errore: codice fiscale mancante")
                    self.refresh_db_signal.emit()
                continue

            self.log(f"Elaborazione Riga {idx+1}: OdA '{oda}', Data '{data_ts}', CF '{codice_fiscale}'...")

            # Controlla se questo OdA ha già dato errore
            if oda in oda_con_errore:
                self.log(f"  OdA '{oda}' già in errore precedente, salto.")
                update_activity_status(activity_id, "errore: numero OdA non trovato")
                self.refresh_db_signal.emit()
                continue

            try:
                # Solo se l'OdA è diverso dall'ultimo estratto, fai Estrai OdA
                if oda != ultimo_oda_estratto:
                    # Trova e compila il campo Numero OdA
                    input_oda = self.trova_campo_numero_oda()
                    
                    if not input_oda:
                        raise Exception("Campo Numero OdA non trovato")

                    # Pulisci e inserisci il valore
                    self.driver.execute_script("arguments[0].value = '';", input_oda)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].focus();", input_oda)
                    time.sleep(0.1)
                    input_oda.clear()
                    input_oda.send_keys(oda)
                    self.driver.execute_script(js_dispatch_events, input_oda)
                    
                    self.log(f"  Numero OdA '{oda}' inserito.")
                    time.sleep(0.5)

                    # Clicca su Estrai OdA
                    self.log("  Click su 'Estrai OdA'...")
                    xpath_estrai = "//span[contains(@class, 'x-btn-inner') and normalize-space(text())='Estrai OdA']"
                    btn_estrai = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_estrai)))
                    btn_estrai.click()

                    self.attendi_scomparsa_overlay(30)
                    time.sleep(1)

                    # Verifica se è apparsa una riga nella griglia
                    if not self.verifica_riga_trovata():
                        self.log(f"  Nessuna riga trovata per OdA {oda}.")
                        oda_con_errore.add(oda)
                        update_activity_status(activity_id, "errore: numero OdA non trovato")
                        self.refresh_db_signal.emit()
                        continue
                    
                    # OdA trovato, memorizzalo
                    ultimo_oda_estratto = oda
                    self.log(f"  Riga trovata per OdA {oda}. Procedo con inserimento dati...")

                    # Clicca sull'icona link per agganciare l'OdA
                    if not self.clicca_icona_link():
                        self.log(f"  Impossibile cliccare icona link per OdA {oda}.")
                        update_activity_status(activity_id, "errore: icona link non trovata")
                        self.refresh_db_signal.emit()
                        continue
                    
                    self.log(f"  Icona link cliccata con successo.")
                    self.attendi_scomparsa_overlay()
                    time.sleep(0.5)

                # Ora procedi con l'inserimento dei dati del timesheet
                
                # Converti data da GG/MM/AAAA a GG.MM.AAAA se necessario
                data_ts_formatted = self.formatta_data(data_ts)
                
                # Inserisci Data Timesheet
                self.log(f"  Inserimento Data Timesheet: {data_ts_formatted}")
                if not self.inserisci_data_timesheet(data_ts_formatted):
                    update_activity_status(activity_id, "errore: impossibile inserire data timesheet")
                    self.refresh_db_signal.emit()
                    continue

                # Clicca su Cerca (lente) accanto alla data
                self.log("  Click su Cerca (lente) dopo Data Timesheet...")
                if not self.clicca_cerca_data_timesheet():
                    update_activity_status(activity_id, "errore: impossibile cliccare Cerca data")
                    self.refresh_db_signal.emit()
                    continue

                # Clicca su Aggiungi Risorsa dropdown e seleziona "Aggiungi Risorsa"
                self.log("  Click su 'Aggiungi Risorsa'...")
                if not self.clicca_aggiungi_risorsa():
                    update_activity_status(activity_id, "errore: impossibile aprire Aggiungi Risorsa")
                    self.refresh_db_signal.emit()
                    continue

                # Inserisci Codice Fiscale
                self.log(f"  Inserimento Codice Fiscale: {codice_fiscale}")
                if not self.inserisci_codice_fiscale(codice_fiscale):
                    update_activity_status(activity_id, "errore: impossibile inserire codice fiscale")
                    self.refresh_db_signal.emit()
                    continue

                # Clicca Cerca nella popup
                self.log("  Click su 'Cerca' nella popup...")
                if not self.clicca_cerca_popup():
                    update_activity_status(activity_id, "errore: impossibile cliccare Cerca")
                    self.refresh_db_signal.emit()
                    continue

                time.sleep(1)

                # Verifica risultato Cerca
                trovati = self.get_trovati_count()
                self.log(f"  Trovati: {trovati}")

                if trovati == 0:
                    self.log("  Dipendente non trovato, chiudo popup...")
                    self.chiudi_popup()
                    update_activity_status(activity_id, "errore: Dipendente non censito in PF.")
                    self.refresh_db_signal.emit()
                    continue

                elif trovati >= 1:
                    self.log("  Dipendente trovato, seleziono e aggiungo...")
                    
                    # Seleziona la riga
                    if not self.seleziona_riga_dipendente():
                        update_activity_status(activity_id, "errore: impossibile selezionare dipendente")
                        self.refresh_db_signal.emit()
                        continue

                    # Clicca Aggiungi
                    if not self.clicca_aggiungi_finale():
                        update_activity_status(activity_id, "errore: impossibile cliccare Aggiungi")
                        self.refresh_db_signal.emit()
                        continue

                    self.attendi_scomparsa_overlay()
                    self.log(f"  Riga {idx+1} completata con successo!")
                    update_activity_status(activity_id, "completato")
                    self.refresh_db_signal.emit()

                time.sleep(0.5)

            except Exception as e:
                self.log(f"  Errore elaborazione riga {idx+1}: {e}")
                traceback.print_exc()
                if activity_id:
                    update_activity_status(activity_id, f"errore: {str(e)[:50]}")
                    self.refresh_db_signal.emit()

        self.log("Elaborazione completata.")

    def seleziona_fornitore_upload(self):
        """Seleziona il fornitore COEMI dal dropdown"""
        # Trova il trigger del dropdown fornitore
        # Usa un selettore più specifico basato sulla struttura della pagina
        xpath_trigger = "//div[contains(@class, 'x-form-trigger') and contains(@class, 'x-form-arrow-trigger')]"
        
        triggers = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_trigger)))
        visible_triggers = [t for t in triggers if t.is_displayed()]

        if not visible_triggers:
            raise Exception("Nessun menu a tendina visibile trovato.")

        # Il primo trigger visibile dovrebbe essere quello del fornitore
        trigger = visible_triggers[0]

        coemi_xpath = f"//li[contains(text(), '{FORNITORE_DA_SELEZIONARE}')]"

        max_retries = 3
        option = None

        for attempt in range(max_retries):
            try:
                self.log(f"  Tentativo apertura elenco fornitori {attempt+1}...")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
                time.sleep(0.5)

                ActionChains(self.driver).move_to_element(trigger).click().perform()
                time.sleep(0.5)

                option = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, coemi_xpath))
                )
                if option:
                    break
            except TimeoutException:
                self.log("  Opzione non apparsa, riprovo...")
                # Prova a chiudere eventuali dropdown aperti
                ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(0.5)

        if not option:
            raise Exception("Impossibile aprire l'elenco fornitori o opzione COEMI non trovata.")

        # Seleziona l'opzione
        self.driver.execute_script("arguments[0].click();", option)
        self.attendi_scomparsa_overlay()
        self.log("  Fornitore COEMI selezionato.")
        time.sleep(1)  # Attendi che la UI si stabilizzi

    def trova_campo_numero_oda(self):
        """
        Trova il campo input per Numero OdA.
        Questo campo è un textbox separato dal combo fornitore.
        """
        # Strategia 1: Cerca per label associata
        try:
            # Cerca un label che contiene "Numero OdA" e poi trova l'input associato
            xpath_by_label = "//label[contains(text(), 'Numero OdA')]/ancestor::div[contains(@class, 'x-field')]//input[contains(@class, 'x-form-text')]"
            input_elem = self.short_wait.until(EC.presence_of_element_located((By.XPATH, xpath_by_label)))
            if input_elem.is_displayed():
                self.log("  Campo OdA trovato tramite label.")
                return input_elem
        except TimeoutException:
            pass

        # Strategia 2: Cerca input con placeholder o attributo specifico
        try:
            # Input di tipo text che NON è dentro un combobox
            xpath_text_input = "//input[contains(@class, 'x-form-text') and contains(@class, 'x-form-field') and not(ancestor::div[contains(@class, 'x-form-type-combo')])]"
            inputs = self.driver.find_elements(By.XPATH, xpath_text_input)
            visible_inputs = [i for i in inputs if i.is_displayed() and i.is_enabled()]
            
            # Filtra per escludere i campi data (che hanno spesso format specifici)
            for inp in visible_inputs:
                # Controlla se non è un campo data
                parent_classes = inp.find_element(By.XPATH, "./ancestor::div[contains(@class, 'x-field')]").get_attribute("class")
                if "date" not in parent_classes.lower():
                    # Verifica che non sia un campo già compilato con date
                    value = inp.get_attribute("value") or ""
                    if not any(char.isdigit() and "." in value for char in value[:10]):
                        self.log("  Campo OdA trovato tramite filtro input.")
                        return inp
        except Exception as e:
            self.log(f"  Errore ricerca input: {e}")

        # Strategia 3: Cerca per aria-label o name
        try:
            xpath_aria = "//input[contains(@aria-label, 'OdA') or contains(@name, 'OdA') or contains(@name, 'oda')]"
            input_elem = self.short_wait.until(EC.presence_of_element_located((By.XPATH, xpath_aria)))
            if input_elem.is_displayed():
                self.log("  Campo OdA trovato tramite aria-label/name.")
                return input_elem
        except TimeoutException:
            pass

        # Strategia 4: Fallback - primo input text visibile dopo il combo fornitore
        try:
            # Trova tutti gli input, escludi quelli nei combo e nei date picker
            all_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input.x-form-text.x-form-field")
            for inp in all_inputs:
                if inp.is_displayed() and inp.is_enabled():
                    # Verifica che non sia dentro un combo
                    try:
                        combo_parent = inp.find_element(By.XPATH, "./ancestor::div[contains(@class, 'x-form-trigger-wrap')]")
                        # Se trova un trigger-wrap, è un combo, salta
                        continue
                    except NoSuchElementException:
                        # Non è un combo, potrebbe essere il campo OdA
                        # Verifica che non abbia un valore data
                        val = inp.get_attribute("value") or ""
                        if not (len(val) == 10 and val.count(".") == 2):  # Pattern data dd.mm.yyyy
                            self.log("  Campo OdA trovato tramite fallback.")
                            return inp
        except Exception as e:
            self.log(f"  Errore fallback: {e}")

        return None

    def verifica_riga_trovata(self):
        """
        Verifica se dopo 'Estrai OdA' è apparsa almeno una riga nella griglia.
        Ritorna True se trovata, False altrimenti.
        """
        try:
            # Cerca righe nella griglia dei risultati
            # Le righe in ExtJS sono tipicamente in elementi con classe x-grid-row o x-grid-item
            xpath_righe = "//table[contains(@class, 'x-grid-item')]//tr[contains(@class, 'x-grid-row')]"
            
            # Attendi brevemente per vedere se appaiono righe
            time.sleep(1)
            
            righe = self.driver.find_elements(By.XPATH, xpath_righe)
            righe_visibili = [r for r in righe if r.is_displayed()]
            
            if righe_visibili:
                self.log(f"  Trovate {len(righe_visibili)} righe nella griglia.")
                return True
            
            # Prova un altro selettore per le righe
            xpath_alt = "//div[contains(@class, 'x-grid-item-container')]//table"
            righe_alt = self.driver.find_elements(By.XPATH, xpath_alt)
            righe_alt_visibili = [r for r in righe_alt if r.is_displayed()]
            
            if righe_alt_visibili:
                self.log(f"  Trovate {len(righe_alt_visibili)} righe (alt) nella griglia.")
                return True

            # Controlla anche il contatore "Trovati: X"
            try:
                xpath_count = "//*[contains(text(), 'Trovati')]"
                count_elem = self.driver.find_element(By.XPATH, xpath_count)
                count_text = count_elem.text
                # Estrai il numero da "Trovati : X"
                import re
                match = re.search(r'Trovati\s*:\s*(\d+)', count_text)
                if match:
                    count = int(match.group(1))
                    self.log(f"  Contatore indica {count} risultati.")
                    return count > 0
            except:
                pass

            return False

        except Exception as e:
            self.log(f"  Errore verifica righe: {e}")
            return False

    def clicca_icona_link(self):
        """
        Clicca sull'icona link nella prima riga della griglia.
        L'icona ha classe: div.x-action-col-icon.x-action-col-0.x-fa.fa-link
        """
        try:
            # Selettore basato sull'immagine fornita
            xpath_icona = "//div[contains(@class, 'x-action-col-icon') and contains(@class, 'fa-link')]"
            
            icona = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_icona)))
            
            # Scroll e click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icona)
            time.sleep(0.3)
            
            # Prova click normale
            try:
                icona.click()
            except:
                # Fallback a JavaScript click
                self.driver.execute_script("arguments[0].click();", icona)
            
            self.attendi_scomparsa_overlay()
            return True

        except TimeoutException:
            self.log("  Icona link non trovata (timeout).")
            return False
        except Exception as e:
            self.log(f"  Errore click icona: {e}")
            return False

    def formatta_data(self, data_str):
        """
        Converte la data dal formato GG/MM/AAAA a GG.MM.AAAA
        Se già in formato GG.MM.AAAA, la restituisce così com'è
        """
        if not data_str:
            return ""
        
        # Sostituisci / con .
        return data_str.replace("/", ".")

    def inserisci_data_timesheet(self, data_str):
        """
        Inserisce la data nel campo Data Timesheet.
        Selettore: input#timesheet_timesheet_grid_timesheet_date-inputEl
        """
        try:
            js_dispatch_events = """
            var el = arguments[0]; var ev_in = new Event('input', {bubbles:true}); el.dispatchEvent(ev_in);
            var ev_ch = new Event('change', {bubbles:true}); el.dispatchEvent(ev_ch);"""

            # Cerca il campo data per ID parziale
            xpath_data = "//input[contains(@id, 'timesheet_date-inputEl') or contains(@id, 'timesheet_grid_timesheet_date')]"
            
            try:
                campo_data = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_data)))
            except TimeoutException:
                # Fallback: cerca per classe e tipo
                xpath_fallback = "//input[contains(@class, 'x-form-field') and contains(@name, 'Data')]"
                campo_data = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_fallback)))

            # Focus e clear
            self.driver.execute_script("arguments[0].focus();", campo_data)
            time.sleep(0.2)
            campo_data.clear()
            time.sleep(0.1)
            
            # Inserisci la data
            self.driver.execute_script("arguments[0].value = arguments[1];", campo_data, data_str)
            self.driver.execute_script(js_dispatch_events, campo_data)
            
            # Anche send_keys per assicurarsi che ExtJS registri
            campo_data.send_keys(Keys.TAB)
            time.sleep(0.3)
            
            return True

        except Exception as e:
            self.log(f"  Errore inserimento data timesheet: {e}")
            return False

    def clicca_cerca_data_timesheet(self):
        """
        Clicca sul pulsante Cerca (lente d'ingrandimento blu) accanto al campo Data Timesheet.
        Selettore: div#timesheet_timesheet_grid_timesheet_date-trigger-refresh
        """
        try:
            # Cerca il pulsante refresh/cerca accanto alla data
            xpath_cerca = "//div[contains(@id, 'timesheet_date-trigger-refresh') or contains(@id, 'date-trigger-refresh')]"
            
            try:
                btn_cerca = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerca)))
            except TimeoutException:
                # Fallback: cerca per classe trigger
                xpath_fallback = "//div[contains(@class, 'x-form-trigger') and contains(@class, 'x-form-search-trigger')]"
                try:
                    btn_cerca = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_fallback)))
                except TimeoutException:
                    # Altro fallback: cerca l'icona della lente vicino al campo data
                    xpath_lente = "//div[contains(@id, 'timesheet_date')]//div[contains(@class, 'x-form-trigger')]"
                    btn_cerca = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_lente)))

            # Click
            self.driver.execute_script("arguments[0].click();", btn_cerca)
            self.log("  Click su Cerca (lente) dopo Data Timesheet.")
            
            self.attendi_scomparsa_overlay()
            time.sleep(0.5)
            return True

        except Exception as e:
            self.log(f"  Errore click Cerca data timesheet: {e}")
            return False

    def clicca_aggiungi_risorsa(self):
        """
        Apre la finestra 'Aggiungi Risorsa'.
        Logica aggiornata:
        1. Clicca di nuovo sul campo Data Timesheet (refocus).
        2. Attende 2 secondi.
        3. Esegue sequenza TAB → freccia giù → INVIO.
        """
        try:
            self.log("  Refocus su campo Data Timesheet...")
            
            # 1. Recupera e clicca nuovamente il campo data per assicurare il focus corretto
            xpath_data = "//input[contains(@id, 'timesheet_date-inputEl') or contains(@id, 'timesheet_grid_timesheet_date')]"
            try:
                campo_data = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_data)))
                campo_data.click()
            except Exception as e:
                self.log(f"  Impossibile cliccare campo data per refocus: {e}")
                return False

            # 2. Attesa esplicita di 2 secondi
            self.log("  Attesa 2 secondi...")
            time.sleep(2)

            self.log("  Esecuzione sequenza tasti (TAB → ↓ → INVIO)...")
            
            # 3. Sequenza: TAB → freccia giù → INVIO
            actions = ActionChains(self.driver)
            
            # TAB per spostarsi dal campo data al pulsante Aggiungi Risorsa
            actions.send_keys(Keys.TAB)
            actions.pause(0.3)
            
            # Freccia giù per aprire il dropdown
            actions.send_keys(Keys.ARROW_DOWN)
            actions.pause(0.3)
            
            # INVIO per selezionare "Aggiungi Risorsa"
            actions.send_keys(Keys.ENTER)
            
            # Esegui la sequenza
            actions.perform()
            
            self.attendi_scomparsa_overlay()
            time.sleep(1)  # Attendi che la finestra si apra
            
            # Verifica che la finestra "Aggiungi Risorsa" sia apparsa
            try:
                xpath_finestra = "//div[contains(@class, 'x-window')]//span[contains(text(), 'Aggiungi Risorsa')]"
                self.short_wait.until(EC.presence_of_element_located((By.XPATH, xpath_finestra)))
                self.log("  Finestra 'Aggiungi Risorsa' aperta.")
            except TimeoutException:
                self.log("  Finestra non verificata, ma procedo comunque.")
            
            return True

        except Exception as e:
            self.log(f"  Errore apertura Aggiungi Risorsa: {e}")
            return False

    def inserisci_codice_fiscale(self, codice_fiscale):
        """
        Inserisce il codice fiscale nel campo apposito.
        Metodo: 6 TAB dalla finestra per raggiungere il campo, poi digita carattere per carattere.
        """
        try:
            # Attendi che la finestra sia completamente caricata
            time.sleep(1)
            
            # Clicca sulla finestra per assicurarsi che abbia il focus
            try:
                xpath_window = "//div[contains(@class, 'x-window')]//span[contains(text(), 'Aggiungi Risorsa')]"
                window_header = self.short_wait.until(EC.presence_of_element_located((By.XPATH, xpath_window)))
                self.driver.execute_script("arguments[0].click();", window_header)
                time.sleep(0.3)
            except:
                # Se non trova l'header, clicca sul body della finestra
                try:
                    xpath_body = "//div[contains(@class, 'x-window-body')]"
                    window_body = self.driver.find_element(By.XPATH, xpath_body)
                    self.driver.execute_script("arguments[0].click();", window_body)
                    time.sleep(0.3)
                except:
                    pass
            
            # Usa ActionChains per navigare con TAB fino al campo Codice Fiscale
            actions = ActionChains(self.driver)
            
            # 6 TAB per raggiungere il campo Codice Fiscale
            self.log("  Navigazione al campo Codice Fiscale (6 TAB)...")
            for i in range(6):
                actions.send_keys(Keys.TAB)
            actions.perform()
            time.sleep(0.5)
            
            # Ora il focus dovrebbe essere sul campo Codice Fiscale
            # Digita il codice fiscale carattere per carattere per sicurezza
            actions = ActionChains(self.driver)
            actions.send_keys(codice_fiscale)
            actions.perform()
            time.sleep(0.3)
            
            # Verifica che il valore sia stato inserito
            try:
                # Cerca il campo attivo o il campo CF
                active_element = self.driver.switch_to.active_element
                val_inserito = active_element.get_attribute("value") or ""
                if codice_fiscale in val_inserito:
                    self.log(f"  Codice Fiscale '{codice_fiscale}' inserito correttamente.")
                else:
                    self.log(f"  Valore nel campo: '{val_inserito}' - potrebbe non corrispondere.")
            except:
                pass
            
            self.log(f"  Codice Fiscale '{codice_fiscale}' inserito.")
            return True

        except Exception as e:
            self.log(f"  Errore inserimento codice fiscale: {e}")
            return False

    def clicca_cerca_popup(self):
        """
        Clicca sul pulsante Cerca nella popup.
        Metodo: 3 TAB + INVIO dopo aver inserito il Codice Fiscale.
        """
        try:
            self.log("  Navigazione al pulsante Cerca (3 TAB + INVIO)...")
            
            actions = ActionChains(self.driver)
            for i in range(3):
                actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            
            self.attendi_scomparsa_overlay()
            time.sleep(1)  # Attendi che i risultati vengano caricati
            return True

        except Exception as e:
            self.log(f"  Errore click Cerca popup: {e}")
            return False

    def get_trovati_count(self):
        """
        Ottiene il numero di risultati trovati dal contatore 'Trovati: X' nella popup
        Questo viene mostrato dopo aver cliccato Cerca nella popup del codice fiscale
        """
        try:
            time.sleep(1)  # Attendi che i risultati vengano caricati
            
            # Cerca il testo "Trovati : X" o "Trovati: X" nella popup
            xpath_trovati = "//div[contains(@class, 'x-window')]//*[contains(text(), 'Trovati')]"
            
            elementi = self.driver.find_elements(By.XPATH, xpath_trovati)
            
            for elem in elementi:
                if elem.is_displayed():
                    text = elem.text
                    self.log(f"  Testo contatore trovato: '{text}'")
                    # Estrai il numero
                    import re
                    match = re.search(r'Trovati\s*:\s*(\d+)', text)
                    if match:
                        count = int(match.group(1))
                        return count
            
            # Fallback: cerca in tutta la pagina
            xpath_global = "//*[contains(text(), 'Trovati')]"
            elementi = self.driver.find_elements(By.XPATH, xpath_global)
            
            for elem in elementi:
                if elem.is_displayed():
                    text = elem.text
                    import re
                    match = re.search(r'Trovati\s*:\s*(\d+)', text)
                    if match:
                        return int(match.group(1))
            
            # Se non trova nulla, controlla se ci sono righe nella griglia della popup
            xpath_rows = "//div[contains(@class, 'x-window')]//div[contains(@class, 'x-grid-item-container')]//table"
            rows = self.driver.find_elements(By.XPATH, xpath_rows)
            visible_rows = [r for r in rows if r.is_displayed()]
            
            if visible_rows:
                self.log(f"  Nessun contatore, ma trovate {len(visible_rows)} righe nella griglia.")
                return len(visible_rows)
            
            return 0

        except Exception as e:
            self.log(f"  Errore lettura Trovati: {e}")
            return 0

    def chiudi_popup(self):
        """
        Chiude la popup corrente cliccando sulla X
        """
        try:
            # Cerca il pulsante X di chiusura nella window attiva
            # In ExtJS la X è tipicamente in div.x-tool con data-qtip="Chiudi" o classe x-tool-close
            
            xpath_close_options = [
                "//div[contains(@class, 'x-window')]//div[contains(@class, 'x-tool-close')]",
                "//div[contains(@class, 'x-window')]//div[@data-qtip='Chiudi']",
                "//div[contains(@class, 'x-window')]//img[contains(@class, 'x-tool-close')]",
                "//div[contains(@class, 'x-tool') and contains(@class, 'x-tool-img')]",
                "//div[contains(@class, 'x-window-header')]//div[contains(@class, 'x-tool')]"
            ]
            
            for xpath in xpath_close_options:
                try:
                    btns = self.driver.find_elements(By.XPATH, xpath)
                    for btn in btns:
                        if btn.is_displayed():
                            self.driver.execute_script("arguments[0].click();", btn)
                            time.sleep(0.5)
                            self.log("  Popup chiusa con X.")
                            return True
                except:
                    continue
            
            # Se non trova la X, prova ESC
            self.log("  X non trovata, provo ESC...")
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.5)
            return True

        except Exception as e:
            self.log(f"  Errore chiusura popup: {e}")
            # Prova ESC come fallback
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.3)
            return True

    def seleziona_riga_dipendente(self):
        """
        Seleziona la riga del dipendente trovato.
        Metodo: 2 TAB + INVIO dopo aver cliccato Cerca.
        """
        try:
            self.log("  Selezione riga dipendente (2 TAB + INVIO)...")
            
            actions = ActionChains(self.driver)
            for i in range(2):
                actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            
            time.sleep(0.5)
            return True

        except Exception as e:
            self.log(f"  Errore selezione riga dipendente: {e}")
            return False

    def clicca_aggiungi_finale(self):
        """
        Clicca sul pulsante Aggiungi per confermare.
        Metodo: 1 TAB + INVIO dopo aver selezionato la riga.
        """
        try:
            self.log("  Click su Aggiungi (1 TAB + INVIO)...")
            
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            
            self.attendi_scomparsa_overlay()
            time.sleep(0.5)
            return True

        except Exception as e:
            self.log(f"  Errore click Aggiungi finale: {e}")
            return False