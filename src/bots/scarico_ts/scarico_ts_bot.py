"""
Bot TS - Scarico TS Bot
Bot per il download automatico dei timesheet dal portale ISAB.
Basato sullo script standalone funzionante.
"""
import os
import time
from pathlib import Path
from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from ..base import BaseBot


class ScaricaTSBot(BaseBot):
    """
    Bot per lo scarico automatico dei timesheet.
    
    Funzionalità:
    - Login al portale ISAB
    - Navigazione a Report -> Timesheet
    - Selezione fornitore COEMI S.R.L.
    - Impostazione data iniziale
    - Ricerca per Numero OdA / Posizione OdA
    - Download del file Excel
    - Rinomina file scaricato
    - Logout e chiusura browser
    """
    
    # Fornitore predefinito
    FORNITORE = "KK10608 - COEMI S.R.L."
    
    @staticmethod
    def get_name() -> str:
        return "Scarico TS"
    
    @staticmethod
    def get_description() -> str:
        return "Scarica i timesheet dal portale ISAB"
    
    @staticmethod
    def get_columns() -> list:
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"}
        ]
    
    @property
    def name(self) -> str:
        return "Scarico TS"
    
    @property
    def description(self) -> str:
        return "Scarica i timesheet dal portale ISAB"
    
    def __init__(self, data_da: str = "01.01.2025", **kwargs):
        """
        Inizializza il bot.
        
        Args:
            data_da: Data inizio timesheet (formato dd.mm.yyyy)
            **kwargs: Altri parametri per BaseBot
        """
        super().__init__(**kwargs)
        self.data_da = data_da
    
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il download dei timesheet.
        
        Args:
            data: Dict con 'rows' contenente lista di dict con keys: numero_oda, posizione_oda
                  e opzionalmente 'data_da' per la data
            
        Returns:
            True se tutti i download hanno successo
        """
        # Estrai i dati
        if isinstance(data, dict):
            rows = data.get('rows', [])
            self.data_da = data.get('data_da', self.data_da)
        else:
            rows = data
        
        if not rows:
            self.log("Nessun dato da processare")
            return True
        
        self.log(f"Processamento {len(rows)} righe...")
        self.log(f"Data inizio: {self.data_da}")
        
        try:
            # 1. Naviga a Report -> Timesheet
            if not self._navigate_to_timesheet():
                return False
            
            # 2. Imposta filtri (Fornitore e Data) - una sola volta
            if not self._setup_filters():
                return False
            
            # 3. Processa ogni riga
            success_count = 0
            download_dir = Path(self.download_path) if self.download_path else Path.home() / "Downloads"
            
            # JS per dispatch eventi su input ExtJS
            js_dispatch_events = """
                var el = arguments[0]; 
                var ev_in = new Event('input', {bubbles:true}); el.dispatchEvent(ev_in);
                var ev_ch = new Event('change', {bubbles:true}); el.dispatchEvent(ev_ch);
            """
            
            for i, row in enumerate(rows, 1):
                self._check_stop()
                
                numero_oda = str(row.get('numero_oda', '')).strip()
                posizione_oda = str(row.get('posizione_oda', '')).strip()
                
                if not numero_oda:
                    self.log(f"Riga {i}: Numero OdA mancante, saltata")
                    continue
                
                self.log("-" * 40)
                self.log(f"Riga {i}/{len(rows)}: OdA='{numero_oda}', Pos='{posizione_oda}'")
                
                try:
                    # Inserisci Numero OdA
                    campo_numero_oda = self.wait.until(
                        EC.presence_of_element_located((By.NAME, "NumeroOda"))
                    )
                    self.driver.execute_script("arguments[0].value = arguments[1];", campo_numero_oda, numero_oda)
                    self.driver.execute_script(js_dispatch_events, campo_numero_oda)
                    self.log(f"  Valore '{numero_oda}' impostato in 'NumeroOda'.")
                    
                    # Inserisci Posizione OdA
                    campo_posizione_oda = self.wait.until(
                        EC.presence_of_element_located((By.NAME, "PosizioneOda"))
                    )
                    self.driver.execute_script("arguments[0].value = '';", campo_posizione_oda)
                    self.driver.execute_script("arguments[0].value = arguments[1];", campo_posizione_oda, posizione_oda)
                    self.driver.execute_script(js_dispatch_events, campo_posizione_oda)
                    self.log(f"  Valore '{posizione_oda}' impostato in 'PosizioneOda'.")
                    
                    # Click su Cerca
                    pulsante_cerca_xpath = "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Cerca' and contains(@class, 'x-btn-inner')]]"
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, pulsante_cerca_xpath))).click()
                    self.log("  Pulsante 'Cerca' cliccato. Attesa risultati...")
                    
                    # Attendi risultati
                    self._attendi_scomparsa_overlay(90)
                    
                    # Download file Excel
                    if self._download_excel(download_dir, numero_oda, posizione_oda):
                        success_count += 1
                    
                except Exception as e:
                    self.log(f"  ✗ Errore elaborazione riga {i}: {e}")
                    continue
                
                time.sleep(1)
            
            self.log("-" * 40)
            self.log(f"Completato: {success_count}/{len(rows)} download riusciti")
            
            # 4. Logout
            self._logout()
            
            return success_count == len(rows)
            
        except Exception as e:
            self.log(f"✗ Errore durante l'esecuzione: {e}")
            return False
    
    def _navigate_to_timesheet(self) -> bool:
        """Naviga a Report -> Timesheet."""
        self._check_stop()
        self.log("Navigazione menu Report -> Timesheet...")
        
        try:
            # Click su "Report"
            self.log("Click su 'Report'...")
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Report']"))
            ).click()
            self.log("'Report' cliccato.")
            self._attendi_scomparsa_overlay()
            
            # Click su "Timesheet"
            self.log("Click su 'Timesheet'...")
            timesheet_menu_xpath = "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, timesheet_menu_xpath))).click()
            self.log("'Timesheet' cliccato.")
            
            # Attendi che il dropdown Fornitore sia visibile
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, fornitore_arrow_xpath)))
            self.log("✓ Pagina Timesheet caricata.")
            self._attendi_scomparsa_overlay()
            
            return True
            
        except Exception as e:
            self.log(f"✗ Errore navigazione menu: {e}")
            return False
    
    def _setup_filters(self) -> bool:
        """Imposta Fornitore e Data Da."""
        self._check_stop()
        self.log("Impostazione filtri (Fornitore, Data)...")
        
        try:
            # Seleziona Fornitore
            self.log(f"  Selezione fornitore: '{self.FORNITORE}'...")
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            fornitore_arrow_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath))
            )
            ActionChains(self.driver).move_to_element(fornitore_arrow_element).click().perform()
            self.log("  Click sulla freccia del dropdown Fornitore eseguito.")
            
            # Seleziona l'opzione COEMI
            coemi_option_xpath = f"//li[normalize-space(text())='{self.FORNITORE}']"
            coemi_option = self.long_wait.until(
                EC.presence_of_element_located((By.XPATH, coemi_option_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", coemi_option)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", coemi_option)
            self.log(f"  ✓ Fornitore '{self.FORNITORE}' selezionato.")
            
            self._attendi_scomparsa_overlay()
            
            # Inserisci Data Da
            self.log(f"  Inserimento data '{self.data_da}'...")
            campo_data_da = self.wait.until(
                EC.visibility_of_element_located((By.NAME, "DataTimesheetDa"))
            )
            campo_data_da.clear()
            campo_data_da.send_keys(self.data_da)
            self.log(f"  ✓ Data '{self.data_da}' inserita.")
            
            self.log("✓ Filtri impostati.")
            return True
            
        except Exception as e:
            self.log(f"✗ Errore impostazione filtri: {e}")
            return False
    
    def _download_excel(self, download_dir: Path, numero_oda: str, posizione_oda: str) -> bool:
        """
        Scarica il file Excel e lo rinomina.
        
        Args:
            download_dir: Directory di download
            numero_oda: Numero OdA per il nome file
            posizione_oda: Posizione OdA per il nome file
            
        Returns:
            True se download e rinomina riusciti
        """
        self.log("  Tentativo di download del file Excel...")
        
        try:
            # File esistenti prima del download
            files_before = {f for f in download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}
            
            # Click sul pulsante Excel
            excel_button_xpath = "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, excel_button_xpath))).click()
            self.log("  Icona Excel per download cliccata. Attesa download (max 25s)...")
            
            # Attendi il download
            downloaded_file = None
            download_start_time = time.time()
            
            while time.time() - download_start_time < 25:
                current_files = {f for f in download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}
                new_files = current_files - files_before
                if new_files:
                    downloaded_file = max(list(new_files), key=lambda f: f.stat().st_mtime)
                    self.log(f"  File scaricato rilevato: {downloaded_file.name}")
                    break
                time.sleep(0.5)
            
            # Fallback: controllo finale
            if not downloaded_file:
                self.log("  File non rilevato rapidamente, controllo finale dopo breve attesa...")
                time.sleep(5)
                current_files = {f for f in download_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}
                new_files = current_files - files_before
                if new_files:
                    downloaded_file = max(list(new_files), key=lambda f: f.stat().st_mtime)
            
            if downloaded_file and downloaded_file.exists():
                # Costruisci il nuovo nome
                nome_base_pos = f"-{posizione_oda}" if posizione_oda else ""
                nuovo_nome_base = f"{numero_oda}{nome_base_pos}"
                nuovo_nome_file = f"{nuovo_nome_base}.xlsx"
                percorso_rinominato = download_dir / nuovo_nome_file
                
                # Gestisci duplicati
                counter = 1
                while percorso_rinominato.exists() and percorso_rinominato.resolve() != downloaded_file.resolve():
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    nuovo_nome_file = f"{nuovo_nome_base}-{timestamp}_{counter}.xlsx"
                    percorso_rinominato = download_dir / nuovo_nome_file
                    counter += 1
                
                downloaded_file.rename(percorso_rinominato)
                self.log(f"  ✓ File rinominato: {percorso_rinominato.name}")
                return True
            else:
                self.log("  ✗ Download fallito o file non trovato.")
                return False
                
        except Exception as e:
            self.log(f"  ✗ Errore download: {e}")
            return False
    
    def execute(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il workflow completo: login -> download -> logout -> chiusura.
        
        Sovrascrive execute di BaseBot per includere logout.
        """
        self._stop_requested = False
        
        try:
            self._init_driver()
            
            if not self._login():
                self.status.ERROR
                return False
            
            self.status.RUNNING
            result = self.run(data)
            
            # Nota: logout è già chiamato in run()
            
            self.status = self.status.COMPLETED if result else self.status.ERROR
            return result
            
        except InterruptedError:
            self.log("Bot interrotto")
            self.status = self.status.STOPPED
            return False
        except Exception as e:
            self.log(f"✗ Errore esecuzione: {e}")
            self.status = self.status.ERROR
            return False
        finally:
            # Pausa prima di chiudere
            self.log("Pausa di 3 secondi prima di chiudere il browser...")
            time.sleep(3)
            self.cleanup()
