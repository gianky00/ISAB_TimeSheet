"""
SyncroJob - SafeWork Ricerca PDL Page
Encapsulamento delle interazioni con la pagina di ricerca PDL.
"""

from collections.abc import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RicercaPDLPage:
    """Gestisce l'interfaccia di 'Ricerca PdL' su SafeWork."""

    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait[webdriver.Chrome], log_func: Callable[[str], None]
    ):
        self.driver = driver
        self.wait = wait
        self.log = log_func

    def configura_filtro_chiusi(self, exclude_closed: bool):
        """Imposta la checkbox per escludere i PDL chiusi."""
        try:
            checkbox = self.wait.until(EC.presence_of_element_located((By.ID, "fldEscludiChiusi")))
            if checkbox.is_selected() != exclude_closed:
                self.log(f"🖱️ Impostazione checkbox 'Escludi chiusi' a {exclude_closed}")
                self.driver.execute_script("arguments[0].click();", checkbox)
        except Exception as e:
            self.log(f"⚠️ Errore gestione checkbox chiusi: {e}")

    def seleziona_sito_e_cerca(self, site_name: str) -> bool:
        """Seleziona un sito specifico e avvia la ricerca."""
        try:
            self.log(f"🏢 Selezione sito: {site_name}")
            # Il selettore del dropdown sito varia leggermente tra le pagine
            site_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[contains(text(), 'ISAB Sud') or contains(text(), 'ISAB Nord') or contains(text(), 'IGCC') or contains(text(), 'Sito')]",
                    )
                )
            )
            site_dropdown.click()

            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{site_name}']"))
            )
            option.click()

            self.log("🖱️ Clic su Cerca...")
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnCerca"))).click()
            return True
        except Exception as e:
            self.log(f"❌ Errore ricerca per {site_name}: {e}")
            return False

    def esporta_excel(self) -> bool:
        """Clicca sul pulsante Esporta."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.ID, "btnEsporta")))
            btn.click()
            return True
        except Exception:
            return False
