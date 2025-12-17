"""
Bot TS - Dettagli OdA Bot
Bot per l'accesso alla sezione Dettagli OdA del portale ISAB.
"""
import time
from typing import List, Dict, Any

from selenium.webdriver.common.by import By
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
    - Impostazione Filtri (Fornitore, Data Da, Data A)
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
    
    def __init__(self, data_da: str = "", data_a: str = "", fornitore: str = "", **kwargs):
        """
        Inizializza il bot.
        
        Args:
            data_da: Data inizio (formato dd.mm.yyyy)
            data_a: Data fine (formato dd.mm.yyyy)
            fornitore: Nome fornitore
            **kwargs: Altri parametri per BaseBot
        """
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore

    def run(self, data: Dict[str, Any]) -> bool:
        """
        Esegue la navigazione ai Dettagli OdA e imposta i filtri.
        """
        # Estrai i parametri se passati nel dizionario data
        if isinstance(data, dict):
            self.data_da = data.get('data_da', self.data_da)
            self.data_a = data.get('data_a', self.data_a)
            self.fornitore = data.get('fornitore', self.fornitore)

        self.log("Accesso sezione Dettagli OdA...")
        self.log(f"Parametri: Fornitore='{self.fornitore}', Periodo={self.data_da}-{self.data_a}")
        
        # 1. Navigazione Report -> OdA
        if not self._navigate_to_oda():
            self.log("⚠ Navigazione automatica fallita.")
            return False
        
        # 2. Impostazione Filtri
        if not self._setup_filters():
            self.log("⚠ Impostazione filtri fallita.")
            # Non ritorniamo False qui per lasciare il browser aperto comunque
        
        self.log("✓ Browser pronto - prosegui manualmente")
        self.log("⚠ Il browser rimarrà aperto")
        
        return True
    
    def _navigate_to_oda(self) -> bool:
        """Naviga a Report -> OdA."""
        self._check_stop()
        self.log("Navigazione menu Report -> OdA...")
        
        try:
            # Click su "Report"
            self.log("Click su 'Report'...")
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Report']"))
            ).click()
            self.log("'Report' cliccato.")
            self._attendi_scomparsa_overlay()

            # Click su "OdA"
            self.log("Click su 'OdA'...")
            # Cerca un pulsante/menu che contenga esattamente "OdA" o "Dettagli OdA"
            # Basandoci su Scarico TS, usiamo una logica simile per i menu
            oda_menu_xpath = "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='OdA']]"
            
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, oda_menu_xpath))).click()
            except TimeoutException:
                # Fallback: prova ricerca testuale generica se l'ID specifico non corrisponde
                self.log("Menu specifico non trovato, provo ricerca generica...")
                self.driver.find_element(By.XPATH, "//*[text()='OdA']").click()

            self.log("'OdA' cliccato.")
            
            # Attendi caricamento pagina (cerca dropdown fornitore)
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, fornitore_arrow_xpath)))
            self.log("✓ Pagina OdA caricata.")
            self._attendi_scomparsa_overlay()
            
            return True
            
        except Exception as e:
            self.log(f"✗ Errore navigazione menu: {e}")
            return False
    
    def _setup_filters(self) -> bool:
        """Imposta Fornitore, Data Da e Data A."""
        self._check_stop()
        self.log("Impostazione filtri...")
        
        try:
            if self.fornitore:
                # Seleziona Fornitore
                self.log(f"  Selezione fornitore: '{self.fornitore}'...")
                fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
                fornitore_arrow_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath))
                )
                ActionChains(self.driver).move_to_element(fornitore_arrow_element).click().perform()

                # Seleziona l'opzione
                fornitore_option_xpath = f"//li[contains(text(), '{self.fornitore}')]"
                fornitore_option = self.long_wait.until(
                    EC.presence_of_element_located((By.XPATH, fornitore_option_xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", fornitore_option)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", fornitore_option)
                self.log(f"  ✓ Fornitore selezionato.")
                self._attendi_scomparsa_overlay()

            # Inserisci Data Da
            if self.data_da:
                self.log(f"  Inserimento Data Da: '{self.data_da}'...")
                # Assumption: field name is DataOdaDa based on Scarico TS pattern
                campo_data_da = self.wait.until(
                    EC.visibility_of_element_located((By.NAME, "DataOdaDa"))
                )
                campo_data_da.clear()
                campo_data_da.send_keys(self.data_da)

            # Inserisci Data A
            if self.data_a:
                self.log(f"  Inserimento Data A: '{self.data_a}'...")
                # Assumption: field name is DataOdaA
                campo_data_a = self.wait.until(
                    EC.visibility_of_element_located((By.NAME, "DataOdaA"))
                )
                campo_data_a.clear()
                campo_data_a.send_keys(self.data_a)
            
            self.log("✓ Filtri impostati.")
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
