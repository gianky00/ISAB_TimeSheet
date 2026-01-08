import glob
import os
import time
from typing import Any, Dict, List

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

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        if not self.download_path:
            from src.core.config_manager import get_download_path

            self.download_path = get_download_path()

        # Setup File Logging
        try:
            log_dir = config_manager.CONFIG_DIR / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            self.log_file = log_dir / "pdl_bot_debug.txt"
            # Inizializza file con header sessione
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n--- NUOVA SESSIONE: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        except Exception as e:
            print(f"Errore setup log file: {e}")
            self.log_file = None
        self.downloaded_files = []
        self.merged_pdf_path = None # Inizializza qui

    def log(self, message: str):
        """Override log per salvare su file."""
        super().log(message)
        if hasattr(self, "log_file") and self.log_file:
            try:
                timestamp = time.strftime("%H:%M:%S")
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] {message}\n")
            except:
                pass

    @property
    def name(self) -> str:
        return "scarico_pdl"

    @property
    def description(self) -> str:
        return "Scarica e stampa Permessi di Lavoro da SafeWork"

    def _login(self) -> bool:
        """Login SafeWork ricalcato dall'originale."""
        if not self.driver or not self.wait:
            return False
        self.log("🌐 Accesso a Safework...")
        self.driver.get(self.SAFEWORK_URL)

        try:
            self.log("⏳ Tentativo selezione sito ISAB Sud...")
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='ms-choice']"))
            ).click()
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']")
                )
            ).click()
            self.log("✅ Sito ISAB Sud selezionato.")
        except Exception as e:
            self.log(f"⚠️ Selezione sito non necessaria o fallita: {e}")

        self.log("🔐 Eseguo il login...")
        self.wait.until(EC.visibility_of_element_located((By.ID, "inpUtente"))).send_keys(self.username)
        self.wait.until(EC.visibility_of_element_located((By.ID, "inpPassword"))).send_keys(self.password)
        self.wait.until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()

        self.log("⏳ Attendo caricamento sistema...")
        self._attendi_caricamento_sistema()
        self.log("✅ Login a Safework completato.")
        return True

    def _safe_remove(self, path):
        """Rimuove un file ignorando errori se in uso."""
        try:
            if os.path.exists(path):
                os.remove(path)
                self.log(f"🗑️ Rimosso file temporaneo: {os.path.basename(path)}")
        except Exception as e:
            self.log(f"⚠️ Impossibile rimuovere file temp (in uso?): {path} - {e}")

    def run(self, data: List[Dict[str, Any]]) -> bool:
        if not self.driver or not self.wait:
            self.log("❌ Driver non inizializzato.")
            return False
        
        success_count = 0
        total = len(data)
        self.downloaded_files = []
        all_downloaded_pdl_paths = [] # Tutti i PDL scaricati per l'unione finale
        self.merged_pdf_path = None

        for index, item in enumerate(data):
            self._check_stop()
            pdl_num = item.get("pdl_number") or item.get("numero_pdl")
            print_enabled = item.get("print_enabled", False)
            printer_name = item.get("printer_name", "")
            merge_and_send = item.get("merge_and_send", False)

            if not pdl_num:
                self.log(f"⚠️ PDL non valido o mancante nella riga {index + 1}. Salto.")
                continue

            self.log(f"🔄 Processo PdL {pdl_num} ({index + 1}/{total})")
            campo_ricerca = self.wait.until(EC.visibility_of_element_located((By.ID, "fldRicercaPdLVeloce")))
            campo_ricerca.clear()
            campo_ricerca.send_keys(pdl_num)
            time.sleep(0.5)
            campo_ricerca.send_keys(Keys.ENTER)

            if self._gestisci_alert_ricerca():
                self.log(f"❌ Alert di ricerca per PdL {pdl_num}. Probabilmente non trovato o errore.")
                continue # Salta questo PDL e vai al successivo

            self._attendi_scomparsa_overlay()
            self.log(f"✅ PdL {pdl_num} trovato.")

            # --- PARTE PRIMA ---
            self.log(f"⬇️ Scarico Parte Prima per PdL {pdl_num}...")
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            ts_1 = time.time()
            self.wait.until(EC.element_to_be_clickable((By.ID, "topIcon-acticonAnteprimaStampaMenu"))).click()
            time.sleep(0.5)
            self.wait.until(EC.element_to_be_clickable((By.ID, "appItaliano"))).click()

            pdf_1 = self._attendi_e_ritorna_nuovo_pdf(ts_1)
            if not pdf_1:
                self.log(f"❌ Timeout scarico Parte 1 per PdL {pdl_num}.")
                continue
            self.log(f"✅ Parte 1 scaricata: {os.path.basename(pdf_1)}")

            path_temp_1 = os.path.join(self.download_path, f"temp_p1_{int(ts_1)}.pdf")
            self._safe_remove(path_temp_1)
            try:
                os.rename(pdf_1, path_temp_1)
            except OSError:
                time.sleep(2)  # Retry once
                os.rename(pdf_1, path_temp_1)

            # --- PARTE SECONDA ---
            try:
                self.log(f"⏳ Apertura Parte Seconda per PdL {pdl_num}...")
                if not self.driver.find_element(By.ID, "lblPAFoglio").is_displayed():
                    try:
                        self.driver.find_element(By.ID, "lblTitoloParteSeconda").click()
                    except:
                        self.driver.find_element(
                            By.XPATH, "//span[contains(text(), 'PARTE SECONDA')]"
                        ).click()
                    time.sleep(1)
                self.wait.until(EC.visibility_of_element_located((By.ID, "lblPAFoglio")))
                self.log(f"✅ Parte Seconda aperta.")
            except Exception as e:
                self.log(f"⚠️ Errore apertura Parte Seconda per PdL {pdl_num}: {e}")

            self.log(f"⬇️ Scarico Parte Seconda per PdL {pdl_num}...")
            self._attendi_scomparsa_overlay()
            self.driver.execute_script("window.scrollTo(0, 0);")
            ts_2 = time.time()

            is_single = False
            try:
                txt = self.driver.find_element(By.ID, "lblPAFoglio").find_element(By.XPATH, "..").text
                is_single = "1/1" in txt
            except:
                pass

            self.wait.until(EC.element_to_be_clickable((By.ID, "btnPrintPS"))).click()

            if not is_single:
                time.sleep(1)
                self.wait.until(EC.element_to_be_clickable((By.ID, "rbStampaTutte"))).click()
                time.sleep(0.5)
                self.wait.until(EC.element_to_be_clickable((By.ID, "btnAnteprima"))).click()

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
            except OSError:
                time.sleep(2)
                os.rename(pdf_2, path_temp_2)

            # --- UNIONE PDF --- 
            nome_finale_pdl = f"PDL_{pdl_num.replace('/', '-')}.pdf"
            percorso_finale_pdl = os.path.join(self.download_path, nome_finale_pdl)
            self._safe_remove(percorso_finale_pdl)
            
            self.log(f"🔄 Unione PDF per PdL {pdl_num}...")
            from src.utils.document_processor import DocumentProcessor # Import qui per evitare circular import

            # Unisci solo la prima pagina del primo PDF con tutte le pagine del secondo
            if DocumentProcessor.merge_pdfs([path_temp_1, path_temp_2], percorso_finale_pdl):
                self.log(f"✅ PDF {pdl_num} unito correttamente: {nome_finale_pdl}")
                self.downloaded_files.append(percorso_finale_pdl)
                all_downloaded_pdl_paths.append(percorso_finale_pdl) # Aggiungi alla lista per l'unione finale
                success_count += 1

                # Stampa
                if print_enabled and printer_name:
                    self.log(f"🖨️ Stampa PdL {pdl_num} su: {printer_name}")
                    print_pdf(percorso_finale_pdl, printer_name)
                else:
                    self.log(f"ℹ️ Stampa disabilitata per PdL {pdl_num}.")

            else:
                self.log(f"❌ Errore durante l'unione dei PDF per PdL {pdl_num}.")
            
            self._safe_remove(path_temp_1)
            self._safe_remove(path_temp_2)

        self.log(f"✨ Completato: {success_count}/{total} PDL elaborati.")
        # self.downloaded_files è già popolato con i percorsi finali dei singoli PDL
        return success_count == total

    def _gestisci_alert_ricerca(self, timeout=10):
        if not self.driver:
            return False
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                btn_ok = self.driver.find_element(
                    By.XPATH, "//button[contains(@class, 'btn dialog-btn btn-ok')]"
                )
                if btn_ok.is_displayed():
                    btn_ok.click()
                    time.sleep(1)
                    return True
            except:
                pass
            time.sleep(0.5)
        return False

    def _attendi_e_ritorna_nuovo_pdf(self, tempo_riferimento, timeout=60):
        scadenza = time.time() + timeout
        while time.time() < scadenza:
            files = glob.glob(os.path.join(self.download_path, "*.pdf"))
            nuovi_files = [f for f in files if os.path.getmtime(f) > tempo_riferimento]
            if nuovi_files:
                nuovi_files.sort(key=os.path.getmtime, reverse=True)
                ultimo_file = nuovi_files[0]
                if not glob.glob(os.path.join(self.download_path, "*.crdownload")):
                    return ultimo_file
            time.sleep(1)
        return None


