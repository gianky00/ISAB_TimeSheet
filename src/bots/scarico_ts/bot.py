"""
Bot TS - Scarico TS Bot
Bot per il download automatico dei timesheet dal portale ISAB.
"""
import os
import time
import glob
from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..base import BaseBot


class ScaricaTSBot(BaseBot):
    """
    Bot per lo scarico automatico dei timesheet.
    
    Funzionalità:
    - Login al portale ISAB
    - Navigazione alla sezione Timesheet
    - Ricerca per Commessa/Mese/Anno
    - Download del file
    """
    
    @property
    def name(self) -> str:
        return "Scarico TS"
    
    @property
    def description(self) -> str:
        return "Scarica i timesheet dal portale ISAB"
    
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il download dei timesheet.
        
        Args:
            data: Lista di dict con keys: commessa, mese, anno
            
        Returns:
            True se tutti i download hanno successo
        """
        if not data:
            self.log("Nessun dato da processare")
            return True
        
        self.log(f"Processamento {len(data)} righe...")
        success_count = 0
        
        # Navigate to Timesheet section
        if not self._navigate_to_timesheet():
            return False
        
        for i, row in enumerate(data, 1):
            self._check_stop()
            
            commessa = row.get('commessa', '').strip()
            mese = row.get('mese', '').strip()
            anno = row.get('anno', '').strip()
            
            if not commessa or not mese or not anno:
                self.log(f"Riga {i}: dati incompleti, saltata")
                continue
            
            self.log(f"Riga {i}/{len(data)}: {commessa} - {mese}/{anno}")
            
            if self._download_timesheet(commessa, mese, anno):
                success_count += 1
                self.log(f"✓ Download completato")
            else:
                self.log(f"✗ Download fallito")
        
        self.log(f"Completato: {success_count}/{len(data)} download riusciti")
        return success_count == len(data)
    
    def _navigate_to_timesheet(self) -> bool:
        """Naviga alla sezione Timesheet."""
        self._check_stop()
        self.log("Navigazione alla sezione Timesheet...")
        
        try:
            # Wait for page to load
            time.sleep(2)
            
            # Navigate using TAB sequence (more reliable than XPath for ExtJS)
            # This may need adjustment based on actual portal structure
            menu_path = ["Timesheet", "Scarico Timesheet"]
            
            for item in menu_path:
                self._check_stop()
                try:
                    element = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            f"//*[contains(text(), '{item}')]"
                        ))
                    )
                    element.click()
                    time.sleep(1.5)
                except TimeoutException:
                    self.log(f"⚠ Menu '{item}' non trovato, provo navigazione alternativa")
                    # Try alternative navigation
                    pass
            
            time.sleep(2)
            return True
            
        except Exception as e:
            self.log(f"✗ Errore navigazione Timesheet: {e}")
            return False
    
    def _download_timesheet(self, commessa: str, mese: str, anno: str) -> bool:
        """
        Scarica un singolo timesheet.
        
        Args:
            commessa: Codice commessa
            mese: Mese (1-12)
            anno: Anno (YYYY)
            
        Returns:
            True se il download ha successo
        """
        self._check_stop()
        
        try:
            # Fill search fields
            # Commessa field
            commessa_field = self._find_field("Commessa")
            if commessa_field:
                commessa_field.clear()
                commessa_field.send_keys(commessa)
            
            # Mese field
            mese_field = self._find_field("Mese")
            if mese_field:
                mese_field.clear()
                mese_field.send_keys(mese)
            
            # Anno field
            anno_field = self._find_field("Anno")
            if anno_field:
                anno_field.clear()
                anno_field.send_keys(anno)
            
            time.sleep(1)
            self._check_stop()
            
            # Click search button
            search_btn = self._find_button(["Cerca", "Search", "Ricerca"])
            if search_btn:
                search_btn.click()
                time.sleep(2)
            
            self._check_stop()
            
            # Wait for results and click download
            download_btn = self._find_button(["Scarica", "Download", "Esporta"])
            if download_btn:
                # Get download directory for monitoring
                download_dir = self.download_path or os.path.expanduser("~/Downloads")
                
                # Get existing files before download
                existing_files = set(glob.glob(os.path.join(download_dir, "*")))
                
                download_btn.click()
                
                # Wait for download to complete
                return self._wait_for_download(download_dir, existing_files)
            else:
                self.log("⚠ Pulsante download non trovato")
                return False
                
        except Exception as e:
            self.log(f"✗ Errore download: {e}")
            return False
    
    def _find_field(self, label: str):
        """Trova un campo input per label."""
        selectors = [
            f"//input[contains(@name, '{label.lower()}')]",
            f"//label[contains(text(), '{label}')]/following::input[1]",
            f"//input[contains(@placeholder, '{label}')]",
            f"//*[contains(@class, 'x-form-field')][contains(@name, '{label.lower()}')]"
        ]
        
        for selector in selectors:
            try:
                element = self.driver.find_element(By.XPATH, selector)
                if element.is_displayed():
                    return element
            except:
                continue
        
        return None
    
    def _find_button(self, labels: List[str]):
        """Trova un pulsante per possibili label."""
        for label in labels:
            selectors = [
                f"//button[contains(text(), '{label}')]",
                f"//span[contains(text(), '{label}')]/ancestor::button",
                f"//*[contains(@class, 'x-btn')][contains(., '{label}')]",
                f"//a[contains(text(), '{label}')]"
            ]
            
            for selector in selectors:
                try:
                    element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if element.is_displayed():
                        return element
                except:
                    continue
        
        return None
    
    def _wait_for_download(self, download_dir: str, existing_files: set, timeout: int = 60) -> bool:
        """
        Attende il completamento del download.
        
        Args:
            download_dir: Directory di download
            existing_files: Set di file esistenti prima del download
            timeout: Timeout in secondi
            
        Returns:
            True se il download è completato
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            self._check_stop()
            
            # Check for .crdownload files (Chrome downloading)
            crdownload_files = glob.glob(os.path.join(download_dir, "*.crdownload"))
            
            if not crdownload_files:
                # Check for new files
                current_files = set(glob.glob(os.path.join(download_dir, "*")))
                new_files = current_files - existing_files
                
                if new_files:
                    # Download completed
                    for f in new_files:
                        self.log(f"📁 File: {os.path.basename(f)}")
                    return True
            
            time.sleep(1)
        
        self.log("⚠ Timeout download")
        return False
