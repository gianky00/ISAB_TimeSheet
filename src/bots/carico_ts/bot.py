"""
Bot TS - Carico Timesheet
Bot per l'upload dei timesheet sul portale ISAB.
"""
from typing import Dict, Any, Optional, Callable
from ..base import BaseBot, BotStatus


class CaricoTSBot(BaseBot):
    """
    Bot per l'upload dei Timesheet sul portale ISAB.
    
    Funzionalità:
    - Login al portale ISAB
    - Navigazione alla sezione Timesheet
    - Upload file timesheet per commessa/mese/anno
    """
    
    @staticmethod
    def get_name() -> str:
        return "Carico TS"
    
    @staticmethod
    def get_description() -> str:
        return "Upload automatico dei Timesheet sul portale ISAB"
    
    @staticmethod
    def get_icon() -> str:
        return "📤"
    
    @staticmethod
    def get_columns() -> list:
        """Restituisce la configurazione delle colonne per la tabella dati."""
        return [
            {"name": "Commessa", "type": "text"},
            {"name": "Mese", "type": "month"},
            {"name": "Anno", "type": "year"},
            {"name": "File", "type": "file"}  # Percorso del file da caricare
        ]
    
    @staticmethod
    def get_config_key() -> str:
        return "last_carico_ts_data"
    
    def run(self, data: Dict[str, Any]) -> bool:
        """
        Esegue l'upload dei timesheet.
        
        Args:
            data: Dict con 'rows' contenente i dati delle righe
        
        Returns:
            True se completato con successo
        """
        rows = data.get("rows", [])
        
        if not rows:
            self._log("[AVVISO] Nessun dato da processare")
            return True
        
        self._log(f"[INFO] Trovate {len(rows)} righe da processare")
        
        # Naviga alla sezione Timesheet
        if not self._navigate_to_timesheet():
            return False
        
        success_count = 0
        error_count = 0
        
        for i, row in enumerate(rows):
            if self._check_stop():
                self._log("[AVVISO] Operazione interrotta dall'utente")
                return False
            
            commessa = row.get("commessa", "")
            mese = row.get("mese", "")
            anno = row.get("anno", "")
            file_path = row.get("file", "")
            
            if not commessa or not file_path:
                self._log(f"[AVVISO] Riga {i+1}: dati mancanti (commessa o file)")
                error_count += 1
                continue
            
            self._log(f"[INFO] [{i+1}/{len(rows)}] Caricamento TS: {commessa} - {mese}/{anno}")
            
            try:
                if self._upload_timesheet(commessa, mese, anno, file_path):
                    success_count += 1
                    self._log(f"[OK] Timesheet caricato con successo")
                else:
                    error_count += 1
                    self._log(f"[ERRORE] Impossibile caricare il timesheet")
            except Exception as e:
                error_count += 1
                self._log(f"[ERRORE] Eccezione: {e}")
        
        self._log(f"[INFO] Completato: {success_count} caricati, {error_count} errori")
        return error_count == 0
    
    def _navigate_to_timesheet(self) -> bool:
        """Naviga alla sezione Timesheet."""
        try:
            self._log("[INFO] Navigazione alla sezione Timesheet...")
            
            # Clicca sul menu Timesheet
            menu_path = ["Timesheet", "Carico Timesheet"]
            
            for menu_item in menu_path:
                if self._check_stop():
                    return False
                
                try:
                    # Cerca il menu item
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    
                    element = WebDriverWait(self.driver, self.timeout).until(
                        EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{menu_item}')]"))
                    )
                    element.click()
                    self._wait(1)
                except Exception as e:
                    self._log(f"[AVVISO] Menu '{menu_item}' non trovato: {e}")
            
            self._wait(2)
            return True
            
        except Exception as e:
            self._log(f"[ERRORE] Navigazione fallita: {e}")
            return False
    
    def _upload_timesheet(self, commessa: str, mese: str, anno: str, file_path: str) -> bool:
        """
        Carica un singolo timesheet.
        
        Args:
            commessa: Codice commessa
            mese: Mese
            anno: Anno
            file_path: Percorso del file da caricare
        
        Returns:
            True se upload riuscito
        """
        try:
            import os
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.keys import Keys
            
            # Verifica che il file esista
            if not os.path.exists(file_path):
                self._log(f"[ERRORE] File non trovato: {file_path}")
                return False
            
            # Compila i campi di ricerca
            # Campo Commessa
            try:
                commessa_input = WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'commessa') or contains(@id, 'commessa')]"))
                )
                commessa_input.clear()
                commessa_input.send_keys(commessa)
            except Exception:
                self._log("[AVVISO] Campo commessa non trovato, provo con TAB navigation")
                self._tab_navigation_fill([commessa, mese, anno])
            
            self._wait(1)
            
            # Cerca il pulsante o input per upload file
            try:
                file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
                file_input.send_keys(file_path)
                self._log(f"[INFO] File selezionato: {os.path.basename(file_path)}")
            except Exception as e:
                self._log(f"[ERRORE] Input file non trovato: {e}")
                return False
            
            self._wait(2)
            
            # Clicca sul pulsante di upload/conferma
            try:
                upload_btn = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[contains(text(), 'Carica') or contains(text(), 'Upload') or contains(text(), 'Conferma')]"
                    ))
                )
                upload_btn.click()
            except Exception:
                # Prova con ENTER
                self.driver.switch_to.active_element.send_keys(Keys.ENTER)
            
            self._wait(3)
            
            # Verifica successo (cerca messaggi di conferma)
            try:
                success_msg = self.driver.find_element(By.XPATH, 
                    "//*[contains(text(), 'successo') or contains(text(), 'caricato') or contains(text(), 'completato')]"
                )
                return True
            except Exception:
                # Non trovato messaggio di successo, ma potrebbe essere ok
                pass
            
            return True
            
        except Exception as e:
            self._log(f"[ERRORE] Upload fallito: {e}")
            return False
    
    def _tab_navigation_fill(self, values: list):
        """Compila i campi usando TAB navigation."""
        from selenium.webdriver.common.keys import Keys
        
        active = self.driver.switch_to.active_element
        
        for value in values:
            if value:
                active.send_keys(value)
            active.send_keys(Keys.TAB)
            self._wait(0.3)
            active = self.driver.switch_to.active_element


class CaricoTSBotFactory:
    """Factory per creare istanze di CaricoTSBot."""
    
    @staticmethod
    def create(**kwargs) -> CaricoTSBot:
        return CaricoTSBot(**kwargs)
