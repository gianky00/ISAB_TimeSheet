"""
Bot TS - Dettagli OdA Bot
Bot per l'accesso alla sezione Dettagli OdA del portale ISAB.
"""
import time
from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..base import BaseBot


class DettagliOdABot(BaseBot):
    """
    Bot per l'accesso ai Dettagli OdA.
    
    Funzionalità:
    - Login al portale ISAB
    - Navigazione alla sezione OdA (opzionale)
    - Browser rimane aperto per uso manuale
    
    Note:
    - Questo bot NON chiude il browser dopo l'esecuzione
    - L'utente può continuare manualmente
    """
    
    @property
    def name(self) -> str:
        return "Dettagli OdA"
    
    @property
    def description(self) -> str:
        return "Accede ai Dettagli OdA - browser rimane aperto"
    
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue la navigazione ai Dettagli OdA.
        
        Args:
            data: Lista di dict con keys: numero_oda, posizione_oda
                  (usati solo per riferimento, navigazione manuale)
            
        Returns:
            True se il login e navigazione hanno successo
        """
        self.log("Accesso sezione Dettagli OdA...")
        
        # Optionally navigate to OdA section
        if not self._navigate_to_oda():
            self.log("⚠ Navigazione automatica fallita - prosegui manualmente")
        
        # Log data reference if provided
        if data:
            self.log(f"Riferimento: {len(data)} OdA da consultare")
            for row in data[:5]:  # Show first 5
                num = row.get('numero_oda', '')
                pos = row.get('posizione_oda', '')
                if num:
                    self.log(f"  • OdA {num}" + (f" - Pos. {pos}" if pos else ""))
            
            if len(data) > 5:
                self.log(f"  ... e altri {len(data) - 5}")
        
        self.log("✓ Browser pronto - prosegui manualmente")
        self.log("⚠ Il browser rimarrà aperto")
        
        return True
    
    def _navigate_to_oda(self) -> bool:
        """Tenta la navigazione alla sezione OdA."""
        self._check_stop()
        self.log("Tentativo navigazione sezione OdA...")
        
        try:
            time.sleep(2)
            
            # Try common menu paths for OdA section
            menu_items = [
                "Ordini", "OdA", "Dettagli OdA", 
                "Ordini di Acquisto", "Gestione Ordini"
            ]
            
            for item in menu_items:
                self._check_stop()
                try:
                    element = self.driver.find_element(
                        By.XPATH, 
                        f"//*[contains(text(), '{item}')]"
                    )
                    if element.is_displayed():
                        element.click()
                        time.sleep(1.5)
                        self.log(f"✓ Menu '{item}' selezionato")
                except:
                    continue
            
            return True
            
        except Exception as e:
            self.log(f"⚠ Navigazione OdA: {e}")
            return False
    
    def execute(self, data: List[Dict[str, Any]]) -> bool:
        """
        Override: esegue senza cleanup (browser rimane aperto).
        
        Args:
            data: Dati da processare
            
        Returns:
            True se l'esecuzione ha successo
        """
        return self.execute_login_only()
