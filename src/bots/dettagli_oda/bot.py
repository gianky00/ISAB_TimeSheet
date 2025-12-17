"""
Bot TS - Dettagli OdA Bot
Bot per l'accesso alla sezione Dettagli OdA del portale ISAB.
"""
import time
from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.bots.base import BaseBot, BotStatus


class DettagliOdABot(BaseBot):
    """
    Bot per l'accesso ai Dettagli OdA.
    
    Funzionalità:
    - Login al portale ISAB
    - Navigazione a Report -> OdA
    - Impostazione Filtri (Fornitore, Num OdA, Divisione, Date)
    - Browser rimane aperto per uso manuale
    """
    
    @staticmethod
    def get_name() -> str:
        return "Dettagli OdA"
    
    @staticmethod
    def get_description() -> str:
        return "Accede ai Dettagli OdA con filtri preimpostati"
    
    @staticmethod
    def get_columns() -> list:
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"}
        ]
    
    @property
    def name(self) -> str:
        return "Dettagli OdA"
    
    @property
    def description(self) -> str:
        return "Accede ai Dettagli OdA con filtri preimpostati"
    
    def __init__(self, data_da: str = "", data_a: str = "", fornitore: str = "", 
                 numero_oda: str = "", posizione_oda: str = "", **kwargs):
        """
        Inizializza il bot.
        
        Args:
            data_da: Data inizio (formato dd.mm.yyyy)
            data_a: Data fine (formato dd.mm.yyyy)
            fornitore: Nome fornitore
            numero_oda: Numero OdA (opzionale)
            posizione_oda: Posizione OdA / Divisione (opzionale)
            **kwargs: Altri parametri per BaseBot
        """
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore
        self.numero_oda = numero_oda
        self.posizione_oda = posizione_oda

    def run(self, data: Dict[str, Any]) -> bool:
        """
        Esegue la navigazione ai Dettagli OdA e imposta i filtri.
        """
        rows = []
        # Estrai i parametri se passati nel dizionario data
        if isinstance(data, dict):
            self.data_da = data.get('data_da', self.data_da)
            self.data_a = data.get('data_a', self.data_a)
            self.fornitore = data.get('fornitore', self.fornitore)
            # Se ci sono righe multiple, usale
            rows = data.get('rows', [])
            # Fallback legacy per singola riga se rows è vuoto
            if not rows:
                self.numero_oda = data.get('numero_oda', self.numero_oda)
                self.posizione_oda = data.get('posizione_oda', self.posizione_oda)

        self.log("Accesso sezione Dettagli OdA...")
        param_log = f"Fornitore='{self.fornitore}', Periodo={self.data_da}-{self.data_a}"
        if not rows and self.numero_oda:
            param_log += f", OdA={self.numero_oda}"
        if not rows and self.posizione_oda:
            param_log += f", Pos={self.posizione_oda}"
        self.log(f"Parametri Base: {param_log}")
        
        # 1. Navigazione Report -> OdA
        # Nota: Se siamo già sulla pagina (es. loop righe), la funzione gestirà l'eccezione o navigherà
        if not self._navigate_to_oda():
            self.log("⚠ Navigazione automatica fallita (o già in pagina). Proseguo con i filtri.")
        
        # 2. Impostazione Filtri
        if rows:
            self.log(f"Avvio elaborazione sequenziale di {len(rows)} righe...")
            for i, row in enumerate(rows, 1):
                self._check_stop()
                self.log(f"--- Elaborazione Riga {i}/{len(rows)} ---")

                # Aggiorna i parametri per la riga corrente
                # Nota: EditableDataTable converte le chiavi in lowercase + underscore
                self.numero_oda = row.get("numero_oda", "")
                self.posizione_oda = row.get("posizione_oda", "")

                self.log(f"  OdA: {self.numero_oda}, Pos: {self.posizione_oda}")

                # Esegui la sequenza completa (ripartendo dal Fornitore)
                if not self._setup_filters():
                    self.log(f"⚠ Errore impostazione filtri riga {i}")

                # Breve pausa tra le righe per stabilità
                time.sleep(1.0)
        else:
            # Esecuzione singola (legacy o nessuna riga specificata)
            if not self._setup_filters():
                self.log("⚠ Impostazione filtri fallita.")
        
        self.log("✓ Processo completato - Browser rimane aperto")
        self.log("⚠ Il browser rimarrà aperto")
        
        return True
    
    def _navigate_to_oda(self) -> bool:
        """Naviga a Report -> OdA usando navigazione tastiera."""
        self._check_stop()
        
        # Check rapido: se vediamo già il filtro fornitore, siamo già sulla pagina corretta
        try:
            fornitore_exists = self.driver.find_elements(By.XPATH, "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@class, 'x-form-arrow-trigger')]")
            if fornitore_exists and fornitore_exists[0].is_displayed():
                self.log("Pagina OdA già attiva. Salto navigazione menu.")
                return True
        except:
            pass

        self.log("Navigazione menu Report -> OdA...")
        
        try:
            # Click su "Report"
            self.log("Click su 'Report'...")
            report_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Report']"))
            )
            report_element.click()
            self.log("'Report' cliccato. Attesa espansione sottomenu...")
            time.sleep(1.5)  # Attendi espansione animazione ExtJS

            # Navigazione tastiera: 2 volte TAB + INVIO per selezionare Oda
            self.log("Selezione 'Oda' tramite tastiera (2x TAB + INVIO)...")
            actions = ActionChains(self.driver)
            
            # Primo TAB
            actions.send_keys(Keys.TAB)
            actions.pause(0.3)
            
            # Secondo TAB
            actions.send_keys(Keys.TAB)
            actions.pause(0.3)
            
            # Invio
            actions.send_keys(Keys.ENTER)
            actions.perform()
            
            self.log("'Oda' selezionato.")
            time.sleep(1.0)

            # Attendi caricamento pagina
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, fornitore_arrow_xpath)))
            self.log("✓ Pagina OdA caricata.")
            self._attendi_scomparsa_overlay()
            
            return True
            
        except Exception as e:
            self.log(f"✗ Errore navigazione menu (potrebbe essere già aperto): {e}")
            # Tentiamo di proseguire comunque se fallisce la navigazione menu
            return False
    
    def _setup_filters(self) -> bool:
        """Imposta Fornitore, OdA, Divisione, Date e Flag."""
        self._check_stop()
        self.log("Impostazione filtri...")
        
        try:
            # 1. Seleziona Fornitore (Click Mouse) - Punto di ripartenza per nuove righe
            if self.fornitore:
                self.log(f"  Selezione fornitore: '{self.fornitore}'...")
                fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
                fornitore_arrow_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath))
                )
                ActionChains(self.driver).move_to_element(fornitore_arrow_element).click().perform()
                time.sleep(0.5)

                # Seleziona l'opzione
                fornitore_option_xpath = f"//li[contains(text(), '{self.fornitore}')]"
                fornitore_option = self.long_wait.until(
                    EC.presence_of_element_located((By.XPATH, fornitore_option_xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", fornitore_option)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", fornitore_option)
                self.log(f"  ✓ Fornitore selezionato.")
                time.sleep(0.5)
                self._attendi_scomparsa_overlay()

            # 2. Navigazione Tastiera per OdA, Divisione, Date e Flag
            actions = ActionChains(self.driver)

            # --- STEP 1: TAB verso Numero OdA ---
            self.log("  Navigazione verso Numero OdA (TAB)...")
            actions.send_keys(Keys.TAB)
            actions.pause(0.3)
            
            # Inserimento Numero OdA
            self.log(f"  Inserimento Numero OdA: '{self.numero_oda}'")
            # Ctrl+A per pulire il campo
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
            actions.pause(0.1)
            if self.numero_oda:
                actions.send_keys(self.numero_oda)
            else:
                # Se vuoto, cancella eventuale testo precedente
                actions.send_keys(Keys.DELETE)
            actions.pause(0.3)

            # --- STEP 2: TAB verso Divisione/Posizione ---
            self.log("  Navigazione verso Divisione (TAB)...")
            actions.send_keys(Keys.TAB)
            actions.pause(0.3)
            
            # Inserimento Divisione/Posizione
            self.log(f"  Inserimento Divisione/Posizione: '{self.posizione_oda}'")
            # Ctrl+A per pulire il campo
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
            actions.pause(0.1)
            if self.posizione_oda:
                actions.send_keys(self.posizione_oda)
            else:
                actions.send_keys(Keys.DELETE)
            actions.pause(0.3)

            # --- STEP 3: TAB verso Data Da ---
            self.log("  Navigazione verso Data Da (TAB)...")
            actions.send_keys(Keys.TAB)
            actions.pause(0.3)

            # Inserimento Data Da
            if self.data_da:
                self.log(f"  Inserimento Data Da: '{self.data_da}'")
                actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
                actions.pause(0.1)
                actions.send_keys(self.data_da)
                actions.pause(0.5)

            # --- STEP 4: TAB verso Data A ---
            self.log("  Navigazione verso Data A (TAB)...")
            actions.send_keys(Keys.TAB)
            actions.pause(0.3)

            # Inserimento Data A
            if self.data_a:
                self.log(f"  Inserimento Data A: '{self.data_a}'")
                actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
                actions.pause(0.1)
                actions.send_keys(self.data_a)
                actions.pause(0.5)

            # --- STEP 5: Navigazione verso Flag (3 TAB) ---
            self.log("  Navigazione tab verso Flag Dettagli (3 TAB)...")
            for i in range(3):
                actions.send_keys(Keys.TAB)
                actions.pause(0.3)

            # --- STEP 6: Attivazione e Conferma (SPAZIO -> TAB -> INVIO) ---
            self.log("  Attivazione flag (SPAZIO)...")
            actions.send_keys(Keys.SPACE)
            actions.pause(0.3)

            self.log("  Navigazione al pulsante conferma (TAB)...")
            actions.send_keys(Keys.TAB)
            actions.pause(0.3)

            self.log("  Conferma finale (INVIO)...")
            actions.send_keys(Keys.ENTER)

            # Esegui tutta la sequenza
            actions.perform()

            self.log("✓ Filtri impostati e ricerca avviata.")
            return True

        except Exception as e:
            self.log(f"✗ Errore impostazione filtri: {e}")
            return False

    def execute(self, data: Any) -> bool:
        """
        Override: esegue login e run, ma non chiude il browser.
        """
        self._stop_requested = False
        try:
            self._init_driver()
            if not self._login():
                return False

            return self.run(data)
        except Exception as e:
            self.log(f"Errore: {e}")
            return False
