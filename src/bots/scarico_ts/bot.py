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

from src.bots.base import BaseBot, BotStatus
from src.utils.helpers import sanitize_filename
from src.core import config_manager


class ScaricaTSBot(BaseBot):
    """
    Bot per lo scarico automatico dei timesheet.
    
    Funzionalità:
    - Login al portale ISAB
    - Navigazione a Report -> Timesheet
    - Selezione fornitore (da configurazione)
    - Impostazione data iniziale
    - Ricerca per Numero OdA / Posizione OdA
    - Download del file Excel
    - Rinomina file scaricato
    - Logout e chiusura browser
    """
    
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
    
    def __init__(self, data_da: str = "01.01.2025", fornitore: str = "", elabora_ts: bool = False, **kwargs):
        """
        Inizializza il bot.
        
        Args:
            data_da: Data inizio timesheet (formato dd.mm.yyyy)
            fornitore: Nome fornitore da selezionare (obbligatorio)
            elabora_ts: Se True, esegue la rinomina e lo spostamento post-download
            **kwargs: Altri parametri per BaseBot
        """
        super().__init__(**kwargs)
        self.data_da = data_da
        self.fornitore = fornitore
        self.elabora_ts = elabora_ts
    
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il download dei timesheet.
        
        Args:
            data: Dict con 'rows' contenente lista di dict con keys: numero_oda, posizione_oda
                  e opzionalmente 'data_da' e 'fornitore'
            
        Returns:
            True se tutti i download hanno successo
        """
        # Estrai i dati
        if isinstance(data, dict):
            rows = data.get('rows', [])
            self.data_da = data.get('data_da', self.data_da)
            if data.get('fornitore'):
                self.fornitore = data.get('fornitore')
        else:
            rows = data
        
        if not rows:
            self.log("ℹ️ Nessun dato da processare.")
            return True
        
        self.log(f"🚀 Inizio scarico TS per {len(rows)} OdA (Fornitore: {self.fornitore})...")
        
        try:
            # 1. Naviga a Report -> Timesheet
            if not self._navigate_to_timesheet():
                return False
            
            # 2. Imposta filtri (Fornitore e Data) - una sola volta
            if not self._setup_filters():
                return False
            
            # 3. Processa ogni riga
            success_count = 0

            # Usa directory download di sistema (browser default)
            source_dir = Path.home() / "Downloads"

            downloaded_files_list = [] # Per Elabora TS logic

            dest_dir = Path(self.download_path) if self.download_path else source_dir
            
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
                
                try:
                    # Inserisci Numero OdA
                    campo_numero_oda = self.wait.until(
                        EC.presence_of_element_located((By.NAME, "NumeroOda"))
                    )
                    self.driver.execute_script("arguments[0].value = arguments[1];", campo_numero_oda, numero_oda)
                    self.driver.execute_script(js_dispatch_events, campo_numero_oda)
                    
                    # Inserisci Posizione OdA
                    campo_posizione_oda = self.wait.until(
                        EC.presence_of_element_located((By.NAME, "PosizioneOda"))
                    )
                    self.driver.execute_script("arguments[0].value = '';", campo_posizione_oda)
                    self.driver.execute_script("arguments[0].value = arguments[1];", campo_posizione_oda, posizione_oda)
                    self.driver.execute_script(js_dispatch_events, campo_posizione_oda)
                    
                    # Click su Cerca
                    pulsante_cerca_xpath = "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Cerca' and contains(@class, 'x-btn-inner')]]"
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, pulsante_cerca_xpath))).click()
                    
                    # Attendi risultati
                    self._attendi_scomparsa_overlay(90)
                    
                    # Download file Excel
                    final_path = self._download_excel(source_dir, dest_dir, numero_oda, posizione_oda)
                    if final_path:
                        success_count += 1
                        downloaded_files_list.append(str(final_path))
                    
                except Exception as e:
                    self.log(f"❌ Errore OdA {numero_oda}: {e}")
                    continue
                
                time.sleep(1)
            
            self.log(f"✨ Operazione completata. {success_count}/{len(rows)} file scaricati.")
            
            # 4. Elaborazione TS (VBA Logic) se richiesto
            if self.elabora_ts and downloaded_files_list:
                self.log("🤖 Controllo duplicati e rinomina in corso...")
                self._process_downloaded_files_vba_style(downloaded_files_list, dest_dir)

            # 5. Logout
            self._logout()
            
            return success_count == len(rows)
            
        except Exception as e:
            self.log(f"❌ Errore imprevisto: {e}")
            return False
    
    def _navigate_to_timesheet(self) -> bool:
        """Naviga a Report -> Timesheet."""
        self._check_stop()
        
        try:
            # Click su "Report"
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Report']"))
            ).click()
            self._attendi_scomparsa_overlay()
            
            # Click su "Timesheet"
            timesheet_menu_xpath = "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, timesheet_menu_xpath))).click()
            
            # Attendi che il dropdown Fornitore sia visibile
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, fornitore_arrow_xpath)))
            self._attendi_scomparsa_overlay()
            
            return True
            
        except Exception as e:
            self.log(f"❌ Impossibile navigare al menu Timesheet: {e}")
            return False
    
    def _setup_filters(self) -> bool:
        """Imposta Fornitore e Data Da."""
        self._check_stop()
        
        try:
            # Seleziona Fornitore
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            fornitore_arrow_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath))
            )
            ActionChains(self.driver).move_to_element(fornitore_arrow_element).click().perform()
            
            # Seleziona l'opzione fornitore
            fornitore_option_xpath = f"//li[normalize-space(text())='{self.fornitore}']"
            fornitore_option = self.long_wait.until(
                EC.presence_of_element_located((By.XPATH, fornitore_option_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", fornitore_option)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", fornitore_option)
            
            self._attendi_scomparsa_overlay()
            
            # Inserisci Data Da
            campo_data_da = self.wait.until(
                EC.visibility_of_element_located((By.NAME, "DataTimesheetDa"))
            )
            campo_data_da.clear()
            campo_data_da.send_keys(self.data_da)
            
            return True
            
        except Exception as e:
            self.log(f"❌ Errore nell'impostazione dei filtri: {e}")
            return False
    
    def _download_excel(self, source_dir: Path, dest_dir: Path, numero_oda: str, posizione_oda: str) -> Path:
        """
        Scarica il file Excel, lo rinomina e lo sposta.
        Restituisce il path finale del file o None.
        """
        try:
            files_before = {f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}
            
            excel_button_xpath = "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, excel_button_xpath))).click()
            
            downloaded_file = None
            download_start_time = time.time()
            
            while time.time() - download_start_time < 25:
                try:
                    current_files = {f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() == '.xlsx'}
                    new_files = current_files - files_before
                    if new_files:
                        downloaded_file = max(list(new_files), key=lambda f: f.stat().st_mtime)
                        break
                except:
                    pass
                time.sleep(0.5)
            
            if downloaded_file and downloaded_file.exists():
                if not dest_dir.exists():
                    try:
                        dest_dir.mkdir(parents=True, exist_ok=True)
                    except:
                        pass

                safe_oda = sanitize_filename(numero_oda)
                safe_pos = sanitize_filename(posizione_oda)
                
                if safe_pos and safe_pos != "unnamed_file":
                    nuovo_nome_base = f"TS_{safe_oda}-{safe_pos}"
                else:
                    nuovo_nome_base = f"TS_{safe_oda}"

                nuovo_nome_file = f"{nuovo_nome_base}.xlsx"
                percorso_finale = dest_dir / nuovo_nome_file
                
                # Se "Elabora TS" è attivo, NON gestiamo qui i conflitti con timestamp o cancellazione,
                # ma spostiamo comunque qui per avere un nome base coerente (o temp).
                # Tuttavia, se Elabora TS è attivo, la logica VBA implica che dobbiamo gestire i conflitti POI.
                # Per ora, manteniamo la logica di rename standard qui.
                # Se esiste già, _download_excel standard lo sovrascrive o rinomina con timestamp.
                # Per supportare la logica VBA che CHIEDE all'utente, se Elabora TS è True,
                # dovremmo forse evitare di sovrascrivere qui se vogliamo chiedere?
                # Ma qui stiamo creando il file per la prima volta in questa sessione.

                # Se Elabora TS è True, lasciamo gestire il conflitto alla funzione _process_downloaded_files_vba_style?
                # No, perché quella funzione itera sui file già scaricati.
                # Se il file esiste già da una sessione PRECEDENTE, qui lo sovrascriviamo o rinominiamo.

                # Modifica per Elabora TS:
                # Se il file esiste già, e siamo in modalità Elabora TS, NON lo sovrascriviamo brutalmente qui?
                # Oppure lo spostiamo con un nome temporaneo e poi lo rinominiamo?

                # Approccio: Spostiamo sempre qui nel path finale con nome standard.
                # Se esiste già, aggiungiamo timestamp automatico per evitare perdita dati.
                # POI, in _process_downloaded_files_vba_style, controlliamo se ci sono conflitti "logici"?
                # No, la richiesta dice: "Esegui un codice... alla fine... Controlla se le cartelle esistono... Cicla file origine... Se destinazione esiste chiedi".

                # REVISIONE LOGICA RICHIESTA:
                # Il codice VBA sposta da Origine (C2) a Destinazione (C3).
                # Qui Origine = Downloads, Destinazione = dest_dir.
                # Se facciamo lo spostamento qui in _download_excel, non c'è più nulla da spostare "alla fine".

                # SOLUZIONE:
                # Indipendentemente dal flag, spostiamo il file nella destinazione.
                # Se elabora_ts è True: Spostiamo in una cartella temporanea per poi elaborare.
                # Se elabora_ts è False: Spostiamo direttamente nella destinazione (con rinomina standard silenziosa).

                # La richiesta utente dice:
                # "il flag Elabora TS deve solo rinominare ed elaborare all'interno il file e non spostarlo
                # visto che non inserendo il flag l'utente deve comunque avere la possibilità di spostarlo
                # se modifica il percorso di destinazione"

                # Interpretazione:
                # 1. Se Elabora TS = False: Scarica -> Sposta in dest_dir (gestione conflitti automatica/silenziosa).
                # 2. Se Elabora TS = True: Scarica -> Sposta in Temp -> Processa (rinomina + richiesta utente) -> Sposta in dest_dir.

                if self.elabora_ts:
                    # Usiamo temp dir per la fase di "Elaborazione"
                    temp_dir = config_manager.CONFIG_DIR / "temp_ts_downloads"
                    if not temp_dir.exists():
                        temp_dir.mkdir(parents=True, exist_ok=True)

                    temp_path = temp_dir / nuovo_nome_file

                    # Se esiste in temp, sovrascrivi
                    import shutil
                    if temp_path.exists():
                        try: temp_path.unlink()
                        except: pass

                    shutil.move(str(downloaded_file), str(temp_path))
                    self.log(f"  ✓ Scaricato (Temp per elaborazione): {temp_path.name}")
                    return temp_path
                else:
                    # Comportamento standard: sposta direttamente in dest_dir
                    if percorso_finale.exists():
                        try:
                            percorso_finale.unlink()
                        except:
                            # Se non riesco a cancellare (es aperto), rinomino con timestamp
                            timestamp = time.strftime("%Y%m%d-%H%M%S")
                            nuovo_nome_file = f"{nuovo_nome_base}_{timestamp}.xlsx"
                            percorso_finale = dest_dir / nuovo_nome_file

                    import shutil
                    shutil.move(str(downloaded_file), str(percorso_finale))
                    self.log(f"✅ Scaricato: {percorso_finale.name}")
                    return percorso_finale
            else:
                self.log("⚠️ File non trovato dopo il download.")
                return None
                
        except Exception as e:
            self.log(f"❌ Problema durante il download: {e}")
            return None

    def _process_downloaded_files_vba_style(self, files: List[str], dest_dir: Path):
        """
        Implementa la logica VBA: sposta file e chiede all'utente in caso di conflitto.
        """
        import shutil

        if not dest_dir.exists():
             self.log(f"  Creazione cartella destinazione: {dest_dir}")
             dest_dir.mkdir(parents=True, exist_ok=True)

        for file_path_str in files:
            self._check_stop()
            src_file = Path(file_path_str)
            if not src_file.exists():
                continue

            # Nome file base (es TS_12345.xlsx)
            filename = src_file.name
            dest_file = dest_dir / filename

            base_name = src_file.stem
            extension = src_file.suffix

            # Loop finché c'è conflitto
            while dest_file.exists():
                self.log(f"⚠ Conflitto: '{filename}' esiste già.")

                prompt = (
                    f"ATTENZIONE: Il file '{filename}' esiste già.\n\n"
                    f"Per rinominare e spostare, inserisci un testo da aggiungere al nome originale ('{base_name}').\n\n"
                    "Per SALTARE questo file, premi Annulla o lascia il campo vuoto."
                )

                # Chiedi all'utente (tramite callback GUI)
                suffix = self._ask_user(prompt)

                if not suffix or not suffix.strip():
                    self.log(f"⏭️ File '{filename}' saltato dall'utente.")
                    break # Break loop, dest_file esiste ancora, quindi if sotto fallirà

                # Nuovo tentativo
                new_filename = f"{base_name} {suffix}{extension}"
                dest_file = dest_dir / new_filename
                filename = new_filename

            # Se non esiste (conflitto risolto o non c'era), sposta
            if not dest_file.exists():
                try:
                    shutil.move(str(src_file), str(dest_file))
                    self.log(f"✓ Spostato: {src_file.name} -> {dest_file.name}")
                except Exception as e:
                    self.log(f"✗ Errore spostamento {src_file.name}: {e}")
            else:
                # Caso saltato: cancelliamo il temp?
                # Sì, per pulizia.
                try:
                    src_file.unlink()
                    self.log(f"  (Temp eliminato)")
                except:
                    pass
    
    def execute(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il workflow completo: login -> download -> logout -> chiusura.
        
        Sovrascrive execute di BaseBot per includere logout.
        """
        self._stop_requested = False
        
        try:
            if not self._safe_login_with_retry():
                self.status = BotStatus.ERROR
                return False
            
            self.status = BotStatus.RUNNING
            result = self.run(data)
            
            # Nota: logout è già chiamato in run()
            
            self.status = BotStatus.COMPLETED if result else BotStatus.ERROR
            return result
            
        except InterruptedError:
            self.log("Bot interrotto")
            self.status = BotStatus.STOPPED
            return False
        except Exception as e:
            self.log(f"✗ Errore esecuzione: {e}")
            self.status = BotStatus.ERROR
            return False
        finally:
            # Pausa prima di chiudere
            self.log("Pausa di 3 secondi prima di chiudere il browser...")
            time.sleep(3)
            self.cleanup()
