import os
import glob
import time
import fitz  # PyMuPDF
from typing import List, Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.base import SafeworkBaseBot
from src.utils.printing import print_pdf

class SafeWorkPDLBot(SafeworkBaseBot):
    """
    Bot per lo scarico e la stampa dei Permessi di Lavoro (PDL) da SafeWork.
    """

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        # Se download_path non è settato, usa quello di default
        if not self.download_path:
             from src.core.config_manager import get_download_path
             self.download_path = get_download_path()

    @property
    def name(self) -> str:
        return "scarico_pdl"

    @property
    def description(self) -> str:
        return "Scarica e stampa Permessi di Lavoro da SafeWork"

    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue la procedura per ogni riga in data.
        Data keys attese: 'pdl_number', 'print_enabled' (bool), 'printer_name' (str)
        """
        success_count = 0
        total = len(data)

        self.log(f"Avvio elaborazione di {total} PDL...")

        for index, item in enumerate(data):
            self._check_stop()
            
            # Ricerca robusta della chiave PDL
            pdl_num = item.get("numero_pdl") or item.get("pdl_number")
            
            if not pdl_num:
                # Fallback: cerca qualsiasi chiave che contenga 'pdl' o 'numero'
                for k, v in item.items():
                    k_lower = k.lower()
                    if ('pdl' in k_lower or 'numero' in k_lower) and v:
                        pdl_num = v
                        break
            
            print_enabled = item.get("print_enabled", False)
            printer_name = item.get("printer_name", "")

            if not pdl_num:
                self.log(f"⚠️ Riga {index+1}: Numero PDL mancante. Chiavi disponibili: {list(item.keys())}, Valori: {item}")
                continue

            self.log(f"--- Elaborazione PDL: {pdl_num} ({index+1}/{total}) ---")
            
            if self._process_single_pdl(pdl_num, print_enabled, printer_name):
                success_count += 1
            else:
                self.log(f"✗ Fallito scarico PDL {pdl_num}")
            
            # Piccola pausa tra uno e l'altro
            time.sleep(1)

        self.log(f"Elaborazione terminata. Successi: {success_count}/{total}")
        return success_count == total

    def _process_single_pdl(self, pdl_number: str, print_enabled: bool, printer_name: str) -> bool:
        try:
            # 1. Ricerca
            self.log(f"🔍 Ricerca PDL {pdl_number}...")
            campo_ricerca = self.wait.until(EC.visibility_of_element_located((By.ID, "fldRicercaPdLVeloce")))
            campo_ricerca.clear()
            campo_ricerca.send_keys(pdl_number)
            time.sleep(0.5)
            campo_ricerca.send_keys(Keys.ENTER)
            
            self._gestisci_alert_ricerca()
            self._attendi_scomparsa_overlay()
            self.log("✅ PDL trovato (o ricerca completata)")

            # 2. Scarico Parte 1
            self.log("📄 Scarico Parte Prima")
            path_p1 = self._download_parte_prima()
            if not path_p1: 
                self.log("❌ Errore download Parte 1")
                return False

            # 3. Passaggio a Parte 2
            self._vai_a_parte_seconda()

            # 4. Scarico Parte 2
            self.log("📄 Scarico Parte Seconda")
            path_p2 = self._download_parte_seconda()
            if not path_p2:
                self.log("❌ Errore download Parte 2")
                # Pulizia parziale
                if os.path.exists(path_p1): os.remove(path_p1)
                return False

            # 5. Unione
            nome_finale = f"PDL_{pdl_number.replace('/', '-')}.pdf"
            path_finale = os.path.join(self.download_path, nome_finale)
            
            if self._unisci_pdf(path_p1, path_p2, path_finale):
                self.log(f"✅ PDF Unito salvato in: {path_finale}")
                
                # Cleanup temp files
                try:
                    os.remove(path_p1)
                    os.remove(path_p2)
                except: pass

                # 6. Stampa (opzionale)
                if print_enabled and printer_name:
                    self.log(f"🖨️ Invio alla stampante: {printer_name}...")
                    if print_pdf(path_finale, printer_name):
                        self.log("✅ Stampa avviata.")
                    else:
                        self.log("❌ Errore avvio stampa.")
                
                return True
            else:
                return False

        except Exception as e:
            self.log(f"❌ Errore durante elaborazione PDL: {e}")
            return False

    def _gestisci_alert_ricerca(self, timeout=5):
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                btn_ok = self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn dialog-btn btn-ok')]")
                if btn_ok.is_displayed():
                    self.log("⚠️ Alert ricerca rilevato, clicco OK")
                    btn_ok.click()
                    time.sleep(1)
                    return True
            except: pass
            time.sleep(0.5)
        return False

    def _attendi_nuovo_file(self, tempo_riferimento, timeout=60) -> str:
        """Attende la creazione di un nuovo PDF nella download dir."""
        scadenza = time.time() + timeout
        while time.time() < scadenza:
            files = glob.glob(os.path.join(self.download_path, "*.pdf"))
            nuovi_files = [f for f in files if os.path.getmtime(f) > tempo_riferimento]
            if nuovi_files:
                nuovi_files.sort(key=os.path.getmtime, reverse=True)
                ultimo_file = nuovi_files[0]
                # Verifica che non sia .crdownload
                if not glob.glob(os.path.join(self.download_path, "*.crdownload")):
                    return ultimo_file
            time.sleep(1)
        return ""

    def _download_parte_prima(self) -> str:
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        ts_start = time.time()
        
        try:
            # Tenta di gestire eventuali overlay residui
            self._attendi_scomparsa_overlay(5)
            
            # Cerca il pulsante (presence, not clickable yet)
            print_btn = self.wait.until(EC.presence_of_element_located((By.ID, "topIcon-acticonAnteprimaStampaMenu")))
            
            # Prova click standard
            try:
                self.wait.until(EC.element_to_be_clickable((By.ID, "topIcon-acticonAnteprimaStampaMenu"))).click()
            except Exception:
                self.log("⚠️ Click standard P1 fallito, tento JS click...")
                self.driver.execute_script("arguments[0].click();", print_btn)
            
            time.sleep(1)
            
            # Clicca "Italiano" nel menu a tendina
            try:
                italiano_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "appItaliano")))
                italiano_btn.click()
            except Exception:
                # Se il menu non si è aperto, riprova il click sul bottone stampa
                self.log("⚠️ Menu stampa non aperto, riprovo click...")
                self.driver.execute_script("arguments[0].click();", print_btn)
                time.sleep(1)
                try:
                    self.driver.find_element(By.ID, "appItaliano").click()
                except:
                    self.driver.execute_script("document.getElementById('appItaliano').click();")

        except Exception as e:
            self.log(f"Impossibile cliccare stampa P1: {e}")
            return ""
        
        pdf_path = self._attendi_nuovo_file(ts_start)
        if not pdf_path:
             self.log("Timeout download Parte 1")
             return ""
        
        # Rinomina temporanea per evitare conflitti
        temp_path = os.path.join(self.download_path, f"temp_p1_{int(ts_start)}.pdf")
        if os.path.exists(temp_path): os.remove(temp_path)
        
        # Attendi stabilità file
        time.sleep(1) 
        os.rename(pdf_path, temp_path)
        return temp_path

    def _vai_a_parte_seconda(self):
        try:
            # Controllo se siamo già su parte seconda (label lblPAFoglio visibile)
            if not self.driver.find_elements(By.ID, "lblPAFoglio"):
                try: 
                    self.driver.find_element(By.ID, "lblTitoloParteSeconda").click()
                except: 
                    self.driver.find_element(By.XPATH, "//span[contains(text(), 'PARTE SECONDA')]").click()
                time.sleep(1)
            
            self.wait.until(EC.visibility_of_element_located((By.ID, "lblPAFoglio")))
        except Exception as e:
            self.log(f"Warning: Navigazione a Parte 2 incerta: {e}")

    def _download_parte_seconda(self) -> str:
        self._attendi_scomparsa_overlay()
        self.driver.execute_script("window.scrollTo(0, 0);")
        ts_start = time.time()

        is_single = False
        try:
            # Check se è foglio singolo (1/1)
            txt = self.driver.find_element(By.ID, "lblPAFoglio").find_element(By.XPATH, "..").text
            is_single = "1/1" in txt
        except: pass

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnPrintPS"))).click()
            
            if not is_single:
                time.sleep(1)
                self.wait.until(EC.element_to_be_clickable((By.ID, "rbStampaTutte"))).click()
                time.sleep(0.5)
                self.wait.until(EC.element_to_be_clickable((By.ID, "btnAnteprima"))).click()
        except Exception as e:
            self.log(f"Errore click stampa P2: {e}")
            return ""

        pdf_path = self._attendi_nuovo_file(ts_start, timeout=90)
        if not pdf_path:
             self.log("Timeout download Parte 2")
             return ""

        temp_path = os.path.join(self.download_path, f"temp_p2_{int(ts_start)}.pdf")
        if os.path.exists(temp_path): os.remove(temp_path)
        time.sleep(1)
        os.rename(pdf_path, temp_path)
        return temp_path

    def _unisci_pdf(self, file1, file2, output_path):
        self.log("🔄 Unione PDF...")
        try:
            doc = fitz.open()
            with fitz.open(file1) as pdf1: doc.insert_pdf(pdf1)
            with fitz.open(file2) as pdf2: doc.insert_pdf(pdf2)
            doc.save(output_path)
            doc.close()
            return True
        except Exception as e:
            self.log(f"❌ Errore unione PDF: {e}")
            return False
