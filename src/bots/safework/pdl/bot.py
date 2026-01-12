import glob
import os
import time
import traceback
from typing import Any, Dict, List, Tuple

import fitz  # PyMuPDF
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.base import SafeworkBaseBot
from src.core import config_manager
from src.utils.printing import print_pdf


class SafeWorkPDLBot(SafeworkBaseBot):
    """
    Bot per lo scarico e la stampa dei PDL da SafeWork.
    Logica ricalcata dallo script originale funzionante.
    """

    def __init__(
        self, username, password, headless=False, timeout=30, download_path=""
    ):
        super().__init__(username, password, headless, timeout, download_path)
        if not self.download_path:
            from src.core.config_manager import get_download_path

            self.download_path = get_download_path()

        # Setup File Logging
        try:
            log_dir = config_manager.CONFIG_DIR / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            # Nome file in maiuscolo come richiesto dall'utente
            self.log_file = log_dir / "pdl_bot_debug.TXT"
            # PULIZIA LOG: Usa 'w' invece di 'a' per resettare il file ad ogni avvio
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write(
                    f"--- SESSIONE DEBUG PDL BOT (DETTAGLIO MASSIMO) --- \nAvvio: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Config: User={username}, Headless={headless}, Timeout={timeout}\n"
                    f"Download Path: {self.download_path}\n"
                    f"{'-'*50}\n"
                )
        except Exception as e:
            print(f"Errore setup log file: {e}")
            self.log_file = None
        self.downloaded_files = []
        self.merged_pdf_path = None  # Inizializza qui

    def log(self, message: str):
        """Override log per salvare su file con massimo dettaglio."""
        super().log(message)
        if hasattr(self, "log_file") and self.log_file:
            try:
                timestamp = time.strftime("%H:%M:%S")
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] {message}\n")
            except Exception:
                pass

    def log_error(self, context: str, exception: Exception):
        """Logga un errore dettagliato con stack trace."""
        err_msg = f"❌ ERRORE CRITICO in {context}: {str(exception)}"
        self.log(err_msg)
        if hasattr(self, "log_file") and self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"--- DETTAGLIO ERRORE ---\nURL Corrente: {self.driver.current_url if self.driver else 'N/A'}\n")
                    f.write(f"STACK TRACE:\n{traceback.format_exc()}\n{'-'*50}\n")
            except Exception:
                pass

    @property
    def name(self) -> str:
        return "scarico_pdl"

    @property
    def description(self) -> str:
        return "Scarica e stampa Permessi di Lavoro da SafeWork"

    def validate_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validazione specifica per SafeWork PDL."""
        self.log("🔍 Avvio validazione dati...")
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            self.log(f"❌ Validazione base fallita: {base_msg}")
            return False, base_msg

        if not data:
            self.log("❌ Lista dati vuota.")
            return False, "Nessun dato da elaborare."

        # Verifica che almeno una riga abbia un PDL
        found_pdl = False
        for i, item in enumerate(data):
            pdl = item.get("pdl_number") or item.get("numero_pdl")
            if pdl:
                found_pdl = True
                self.log(f"✅ Riga {i+1}: Trovato PDL {pdl}")
            else:
                self.log(f"⚠️ Riga {i+1}: PDL mancante")

        if not found_pdl:
            self.log("❌ Nessun numero PDL trovato nei dati forniti.")
            return False, "Nessun numero PDL trovato nei dati forniti."

        self.log("✅ Validazione completata con successo.")
        return True, ""

    def _login(self) -> bool:
        """Login SafeWork ricalcato dall'originale."""
        if not self.driver or not self.wait:
            self.log("❌ Driver o Wait non inizializzati.")
            return False
            
        self.log("🌐 Navigazione verso l'URL SafeWork...")
        try:
            self.driver.get(self.SAFEWORK_URL)
            self.log(f"📍 URL caricato. Titolo pagina: {self.driver.title}")
        except Exception as e:
            self.log_error("Apertura URL", e)
            return False

        try:
            self.log("⏳ Cerco pulsante selezione sito (ms-choice)...")
            btn_sito = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='ms-choice']"))
            )
            btn_sito.click()
            self.log("🖱️ Menu siti aperto. Cerco 'ISAB Sud'...")
            
            opzione_isab = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']",
                    )
                )
            )
            opzione_isab.click()
            self.log("✅ Sito ISAB Sud selezionato.")
        except Exception as e:
            self.log(f"ℹ️ Selezione sito non necessaria o fallita (proseguo): {e}")

        try:
            self.log(f"🔐 Inserimento credenziali per utente: {self.username}")
            u_field = self.wait.until(EC.visibility_of_element_located((By.ID, "inpUtente")))
            u_field.clear()
            u_field.send_keys(self.username)
            self.log("⌨️ Username inserito.")
            
            p_field = self.wait.until(EC.visibility_of_element_located((By.ID, "inpPassword")))
            p_field.clear()
            p_field.send_keys(self.password)
            self.log("⌨️ Password inserita.")
            
            self.log("🖱️ Clic su pulsante Login...")
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()
        except Exception as e:
            self.log_error("Inserimento credenziali login", e)
            return False

        self.log("⏳ Attendo il caricamento del sistema (overlay/caricamento)...")
        try:
            self._attendi_caricamento_sistema()
            self.log("✅ Login a Safework completato. Dashboard pronta.")
        except Exception as e:
            self.log_error("Attesa post-login", e)
            return False
            
        return True

    def _safe_remove(self, path):
        """Rimuove un file ignorando errori se in uso."""
        try:
            if os.path.exists(path):
                os.remove(path)
                self.log(f"🗑️ Rimosso file temporaneo: {os.path.basename(path)}")
        except Exception as e:
            self.log(f"⚠️ Impossibile rimuovere file temp (in uso?): {path} - {str(e)}")

    def run(self, data: List[Dict[str, Any]]) -> bool:
        # Driver e wait sono garantiti da execute()
        success_count = 0
        total = len(data)
        self.downloaded_files = []
        all_downloaded_pdl_paths = []  # Tutti i PDL scaricati per l'unione finale
        self.merged_pdf_path = None
        
        self.log(f"🚀 Inizio elaborazione di {total} righe di dati.")

        for index, item in enumerate(data):
            try:
                self._check_stop()
                pdl_raw = item.get("pdl_number") or item.get("numero_pdl")
                print_enabled = item.get("print_enabled", False)
                printer_name = item.get("printer_name", "")
                
                self.log(f"--- Elaborazione Riga {index + 1}/{total} ---")
                
                if not pdl_raw:
                    self.log(f"⚠️ PDL non valido o mancante nella riga {index + 1}. Salto.")
                    continue

                # --- SANITIZZAZIONE PDL ---
                pdl_num = str(pdl_raw).strip().upper().replace(" ", "")
                if pdl_num.isdigit() and len(pdl_num) == 6:
                    num = int(pdl_num)
                    suffix = "/S" if num < 400000 else "/C"
                    pdl_num = f"{pdl_num}{suffix}"
                    self.log(f"ℹ️ PDL auto-completato: {pdl_raw} -> {pdl_num}")
                else:
                    self.log(f"ℹ️ PDL già formattato o non standard: {pdl_num}")

                self.log(f"🔄 Ricerca PdL {pdl_num} in interfaccia...")
                try:
                    campo_ricerca = self.wait.until(
                        EC.visibility_of_element_located((By.ID, "fldRicercaPdLVeloce"))
                    )
                    campo_ricerca.clear()
                    campo_ricerca.send_keys(pdl_num)
                    time.sleep(0.5)
                    val_inserito = campo_ricerca.get_attribute("value")
                    self.log(f"⌨️ Valore inserito nel campo: '{val_inserito}'")
                    campo_ricerca.send_keys(Keys.ENTER)
                    self.log("⌨️ Inviato tasto ENTER per ricerca.")
                except Exception as e:
                    self.log_error(f"Interazione campo ricerca PDL {pdl_num}", e)
                    continue

                if self._gestisci_alert_ricerca():
                    # NOTA IMPORTANTE: Se appare l'alert "PdL non in programmazione", non facciamo 'continue'.
                    # È sempre un avviso informativo. Attendiamo 2 secondi per permettere al sistema
                    # di caricare comunque i dati del PDL a video, garantendo la resilienza del bot.
                    self.log(f"⚠️ Rilevato alert durante la ricerca del PdL {pdl_num}. Provo a procedere comunque...")
                    time.sleep(2)
                    # Verifica se il PDL è effettivamente caricato nonostante l'alert
                    try:
                        # Se l'overlay sparisce e siamo ancora sulla pagina di ricerca, 
                        # verifichiamo se i dati sono apparsi
                        self._attendi_scomparsa_overlay(timeout_secondi=5)
                    except:
                        pass
                else:
                    self.log("⏳ Attesa scomparsa overlay post-ricerca...")
                    self._attendi_scomparsa_overlay()
                
                self.log(f"✅ Verifica stato post-ricerca per {pdl_num}. URL: {self.driver.current_url}")

                # --- PARTE PRIMA ---
                self.log(f"⬇️ Avvio scarico Parte Prima per PdL {pdl_num}...")
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                ts_1 = time.time()
                
                try:
                    self.log("🖱️ Clic pulsante Anteprima Stampa...")
                    self.wait.until(
                        EC.element_to_be_clickable(
                            (By.ID, "topIcon-acticonAnteprimaStampaMenu")
                        )
                    ).click()
                    time.sleep(0.5)
                    self.log("🖱️ Selezione lingua 'Italiano'...")
                    self.wait.until(EC.element_to_be_clickable((By.ID, "appItaliano"))).click()
                except Exception as e:
                    self.log_error(f"Click stampa Parte 1 PDL {pdl_num}", e)
                    continue

                self.log("⏳ Attesa download file PDF (Parte 1)...")
                pdf_1 = self._attendi_e_ritorna_nuovo_pdf(ts_1)
                if not pdf_1:
                    self.log(f"❌ Timeout scarico Parte 1 per PdL {pdl_num}.")
                    continue
                self.log(f"✅ Parte 1 scaricata: {os.path.basename(pdf_1)}")

                path_temp_1 = os.path.join(self.download_path, f"temp_p1_{int(ts_1)}.pdf")
                self._safe_remove(path_temp_1)
                try:
                    os.rename(pdf_1, path_temp_1)
                    self.log(f"📂 File rinominato in: {os.path.basename(path_temp_1)}")
                except Exception as e:
                    self.log(f"⚠️ Errore rinomina Parte 1: {e}")
                    path_temp_1 = pdf_1 # Prova a usare l'originale se rename fallisce

                # --- PULIZIA PARTE PRIMA ---
                try:
                    self.log(f"🔍 Controllo pagine Parte 1: {path_temp_1}")
                    doc_p1 = fitz.open(path_temp_1)
                    pagine_orig = doc_p1.page_count
                    if pagine_orig >= 2:
                        self.log(f"✂️ Parte 1 ha {pagine_orig} pagine. Rimuovo la pagina 2.")
                        doc_p1.delete_page(1) 
                        tmp_clean = path_temp_1 + "_clean.pdf"
                        doc_p1.save(tmp_clean)
                        doc_p1.close()
                        self._safe_remove(path_temp_1)
                        os.rename(tmp_clean, path_temp_1)
                        self.log("✅ Pagina 2 rimossa correttamente.")
                    else:
                        self.log(f"ℹ️ Parte 1 ha {pagine_orig} pagine. Nessuna rimozione necessaria.")
                        doc_p1.close()
                except Exception as e:
                    self.log(f"⚠️ Errore pulizia Parte 1: {e}")

                # --- PARTE SECONDA ---
                try:
                    self.log(f"⏳ Verifica apertura sezione Parte Seconda...")
                    if not self.driver.find_element(By.ID, "lblPAFoglio").is_displayed():
                        self.log("🖱️ Parte Seconda non visibile, clicco per espandere...")
                        try:
                            self.driver.find_element(By.ID, "lblTitoloParteSeconda").click()
                        except Exception:
                            self.driver.find_element(
                                By.XPATH, "//span[contains(text(), 'PARTE SECONDA')]"
                            ).click()
                        time.sleep(1)
                    self.wait.until(
                        EC.visibility_of_element_located((By.ID, "lblPAFoglio"))
                    )
                    self.log("✅ Sezione Parte Seconda aperta.")
                except Exception as e:
                    self.log(f"⚠️ Errore apertura Parte Seconda: {e}")

                self.log(f"⬇️ Avvio scarico Parte Seconda per PdL {pdl_num}...")
                self._attendi_scomparsa_overlay()
                self.driver.execute_script("window.scrollTo(0, 0);")
                ts_2 = time.time()

                try:
                    self.log("🖱️ Clic pulsante Stampa Parte Seconda (btnPrintPS)...")
                    self.wait.until(EC.element_to_be_clickable((By.ID, "btnPrintPS"))).click()
                    
                    # Verifica se è un PDL a foglio singolo o multiplo
                    self.log("⏳ Attesa dialogo opzioni stampa...")
                    time.sleep(1)
                    try:
                        btn_tutte = self.driver.find_element(By.ID, "rbStampaTutte")
                        if btn_tutte.is_displayed():
                            self.log("🔘 Seleziono 'Stampa Tutte'...")
                            btn_tutte.click()
                            time.sleep(0.5)
                            self.log("🖱️ Clic Anteprima...")
                            self.driver.find_element(By.ID, "btnAnteprima").click()
                    except Exception:
                        self.log("ℹ️ Dialogo 'Tutte' non trovato, probabilmente foglio singolo.")
                except Exception as e:
                    self.log_error(f"Click stampa Parte 2 PDL {pdl_num}", e)
                    self._safe_remove(path_temp_1)
                    continue

                self.log("⏳ Attesa download file PDF (Parte 2, timeout lungo)...")
                pdf_2 = self._attendi_e_ritorna_nuovo_pdf(ts_2, timeout=90)
                if not pdf_2:
                    self.log(f"❌ Timeout scarico Parte 2 per PdL {pdl_num}.")
                    self._safe_remove(path_temp_1)
                    continue
                self.log(f"✅ Parte 2 scaricata: {os.path.basename(pdf_2)}")

                path_temp_2 = os.path.join(self.download_path, f"temp_p2_{int(ts_2)}.pdf")
                self._safe_remove(path_temp_2)
                try:
                    os.rename(pdf_2, path_temp_2)
                except Exception as e:
                    self.log(f"⚠️ Errore rinomina Parte 2: {e}")
                    path_temp_2 = pdf_2

                # --- UNIONE PDF ---
                pdl_upper = pdl_num.upper()
                nome_finale_pdl = f"PDL_{pdl_upper.replace('/', '-')}.pdf"
                percorso_finale_pdl = os.path.join(self.download_path, nome_finale_pdl)
                self._safe_remove(percorso_finale_pdl)

                self.log(f"🔄 Avvio unione PDF [P1 + P2] -> {nome_finale_pdl}")
                from src.utils.document_processor import DocumentProcessor

                if DocumentProcessor.merge_pdfs(
                    [path_temp_1, path_temp_2], percorso_finale_pdl
                ):
                    self.log(f"✅ PdL {pdl_upper} unito con successo.")
                    self.downloaded_files.append(percorso_finale_pdl)
                    all_downloaded_pdl_paths.append(percorso_finale_pdl)
                    success_count += 1

                    # Stampa
                    if print_enabled and printer_name:
                        self.log(f"🖨️ Richiesta stampa su: {printer_name}")
                        try:
                            print_pdf(percorso_finale_pdl, printer_name)
                            self.log("✅ Comando stampa inviato.")
                        except Exception as e:
                            self.log(f"⚠️ Errore durante la stampa: {e}")
                    else:
                        self.log(f"ℹ️ Stampa non richiesta per PdL {pdl_upper}.")
                else:
                    self.log(f"❌ Fallimento unione PDF per PdL {pdl_upper}.")

                self._safe_remove(path_temp_1)
                self._safe_remove(path_temp_2)
                
            except InterruptedError:
                self.log("🛑 Stop richiesto dall'utente durante il loop.")
                raise
            except Exception as e:
                self.log_error(f"Processo PDL riga {index+1}", e)

        # --- MERGE ALL SESSION ---
        merge_all_session = any(item.get("merge_all_session", False) for item in data)
        if merge_all_session and all_downloaded_pdl_paths:
            try:
                self.log(f"🔗 Unione di TUTTI i {len(all_downloaded_pdl_paths)} PDL della sessione...")
                timestamp_str = time.strftime("%d-%m-%Y_%H-%M")
                nome_merge_totale = f"PDL_SESSIONE_{timestamp_str}.pdf"
                path_merge_totale = os.path.join(self.download_path, nome_merge_totale)

                from src.utils.document_processor import DocumentProcessor
                if DocumentProcessor.merge_pdfs(
                    all_downloaded_pdl_paths, path_merge_totale
                ):
                    self.log(f"✅ PDF Unico Sessione creato: {nome_merge_totale}")
                    self.downloaded_files.append(path_merge_totale)
                else:
                    self.log("❌ Errore creazione PDF Unico sessione.")
            except Exception as e:
                self.log_error("Unione totale sessione", e)

        self.log(f"✨ FINE ESECUZIONE: {success_count}/{total} PDL completati.")
        return success_count == total

    def _gestisci_alert_ricerca(self, timeout=10):
        if not self.driver:
            return False
        self.log("🔍 Controllo eventuali alert di errore ricerca...")
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                # Cerca il testo dell'alert per il log
                try:
                    alert_content = self.driver.find_element(By.XPATH, "//div[contains(@class, 'modal-content')]")
                    if alert_content.is_displayed():
                        testo = alert_content.text.replace("\n", " ").strip()
                        self.log(f"🚩 ALERT RILEVATO: '{testo}'")
                except:
                    pass

                btn_ok = self.driver.find_element(
                    By.XPATH, "//button[contains(@class, 'btn dialog-btn btn-ok')]"
                )
                if btn_ok.is_displayed():
                    self.log("🖱️ Clic su OK per chiudere alert.")
                    btn_ok.click()
                    time.sleep(1)
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        return False

    def _attendi_e_ritorna_nuovo_pdf(self, tempo_riferimento, timeout=60):
        scadenza = time.time() + timeout
        self.log(f"⏳ Polling cartella download (Ref Time: {int(tempo_riferimento)})...")
        while time.time() < scadenza:
            files = glob.glob(os.path.join(self.download_path, "*.pdf"))
            nuovi_files = [f for f in files if os.path.getmtime(f) > tempo_riferimento]
            if nuovi_files:
                nuovi_files.sort(key=os.path.getmtime, reverse=True)
                ultimo_file = nuovi_files[0]
                # Verifica che non ci siano download in corso (.crdownload)
                if not glob.glob(os.path.join(self.download_path, "*.crdownload")):
                    self.log(f"📄 Trovato nuovo file: {os.path.basename(ultimo_file)}")
                    return ultimo_file
            time.sleep(1)
        self.log("❌ Nessun nuovo PDF trovato entro il timeout.")
        return None
