"""
SyncroJob - SafeWork Visualizza Attività Page
Gestione della pagina Visualizza Attività per la programmazione.
"""

from collections.abc import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.common.locators import SafeWorkLocators


class VisualizzaAttivitaPage:
    """Gestisce le interazioni con la pagina Visualizza Attività."""

    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait[webdriver.Chrome], log_func: Callable[[str], None]
    ):
        self.driver = driver
        self.wait = wait
        self.log = log_func

    def pulisci_pdl(self):
        """Pulisce il campo PDL/Permesso se necessario."""
        try:
            fld = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.NUM_PERMESSO_FIELD))
            fld.clear()
        except Exception:
            pass

    def imposta_date(self, data_dal: str, data_al: str):
        """Imposta il range date."""
        try:
            self.driver.execute_script(f"document.getElementById('programmazioneDal').value = '{data_dal}';")
            self.driver.execute_script(f"document.getElementById('programmazioneAl').value = '{data_al}';")
        except Exception as e:
            self.log(f"⚠️ Errore impostazione date JS: {e}")

    def seleziona_ditta(self, nome_ditta: str):
        """Seleziona la ditta dal dropdown custom."""
        self._seleziona_da_dropdown(SafeWorkLocators.DITTA_BUTTON, nome_ditta)

    def seleziona_richiedente(self, nome_richiedente: str) -> bool:
        """Seleziona il richiedente."""
        return self._seleziona_da_dropdown(SafeWorkLocators.RICHIEDENTE_BUTTON, nome_richiedente)

    def esegui_ricerca(self):
        """Clicca 'Avvia Ricerca'."""
        self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.SEARCH_START_BUTTON)).click()

    def get_rows(self):
        """Restituisce le righe della tabella risultati."""
        try:
            return self.driver.find_elements(*SafeWorkLocators.ROWS)
        except Exception:
            return []

    def _seleziona_da_dropdown(self, button_locator, search_text: str) -> bool:
        """Helper per i dropdown ms-choice di SafeWork."""
        try:
            # 1. Apri Dropdown
            self.wait.until(EC.element_to_be_clickable(button_locator)).click()
            
            # 2. Attendi apertura
            dropdown = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.DROPDOWN_OPEN))
            
            # 3. Cerca
            inp = dropdown.find_element(*SafeWorkLocators.SEARCH_INPUT_IN_DROPDOWN)
            inp.clear()
            inp.send_keys(search_text)
            
            # 4. Seleziona Opzione (Select All o specifica)
            # Qui semplifichiamo selezionando la prima opzione visibile che non sia "Select all" se specifica
            # Oppure premiamo invio. SafeWork spesso filtra e basta premere invio o cliccare l'opzione.
            # Assumiamo click su checkbox visibile
            opt = dropdown.find_element(By.XPATH, f".//span[contains(text(), '{search_text}')]")
            opt.click()
            
            # 5. Chiudi (spesso cliccando fuori o sul bottone)
            self.driver.find_element(By.TAG_NAME, "body").click()
            return True
        except Exception as e:
            self.log(f"❌ Errore selezione '{search_text}': {e}")
            return False
