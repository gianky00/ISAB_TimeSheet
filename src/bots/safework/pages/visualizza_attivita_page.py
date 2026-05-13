"""
SyncroJob - SafeWork Visualizza AttivitàPage
Gestione della pagina Visualizza Attivitàper la programmazione.
"""

import contextlib
import time
from collections.abc import Callable
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.common.locators import SafeWorkLocators


class VisualizzaAttivitaPage:
    """Gestisce le interazioni con la pagina Visualizza Attività."""

    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait[webdriver.Chrome], log_func: Callable[[str], None]
    ) -> None:
        self.driver = driver
        self.wait = wait
        self.log = log_func

    def pulisci_pdl(self) -> None:
        """Pulisce il campo PDL/Permesso se necessario."""
        with contextlib.suppress(Exception):
            fld = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.NUM_PERMESSO_FIELD))
            fld.clear()

    def imposta_date(self, data_dal: str, data_al: str) -> None:
        """Imposta il range date."""
        try:
            self.driver.execute_script(f"document.getElementById('programmazioneDal').value = '{data_dal}';")  # type: ignore[no-untyped-call]
            self.driver.execute_script(f"document.getElementById('programmazioneAl').value = '{data_al}';")  # type: ignore[no-untyped-call]
        except Exception as e:
            self.log(f"⚠️ Errore impostazione date JS: {e}")

    def seleziona_ditta(self, nome_ditta: str) -> None:
        """Seleziona la ditta dal dropdown custom."""
        self._seleziona_da_dropdown(SafeWorkLocators.DITTA_BUTTON, nome_ditta)

    def seleziona_richiedente(self, items: str | list[str]) -> bool:
        """Seleziona uno o più richiedenti nel dropdown."""
        return self._seleziona_da_dropdown(SafeWorkLocators.RICHIEDENTE_BUTTON, items)

    def esegui_ricerca(self) -> None:
        """Clicca 'Avvia Ricercà."""
        self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.SEARCH_START_BUTTON)).click()

    def esporta_excel(self) -> bool:
        """Clicca il pulsante di esportazione Excel."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.EXPORT_BUTTON))
            btn.click()
            return True  # noqa: TRY300
        except Exception as e:
            self.log(f"❌ Errore clic export: {e}")
            return False

    def get_rows(self) -> list[Any]:
        """Restituisce le righe della tabella risultati."""
        try:
            return self.driver.find_elements(*SafeWorkLocators.ROWS)
        except Exception:
            return []

    def _seleziona_da_dropdown(self, button_locator: tuple[str, str], items: str | list[str]) -> bool:
        """Helper per i dropdown ms-choice di SafeWork con supporto selezione multipla."""
        if isinstance(items, str):
            items = [items]

        try:
            # 1. Apri Dropdown
            self.wait.until(EC.element_to_be_clickable(button_locator)).click()

            # 2. Attendi apertura
            dropdown = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.DROPDOWN_OPEN))
            inp = dropdown.find_element(*SafeWorkLocators.SEARCH_INPUT_IN_DROPDOWN)

            for item in items:
                # 3. Cerca e seleziona ogni elemento
                inp.clear()
                inp.send_keys(item)
                time.sleep(0.5)  # Attesa filtro dinamico

                try:
                    opt = dropdown.find_element(
                        By.XPATH,
                        f".//li[not(contains(@class, 'ms-no-results'))]//span[contains(text(), '{item}')]",
                    )
                    opt.click()
                except Exception:
                    self.log(f"⚠️ Elemento '{item}' non trovato nel dropdown.")

            # 4. Chiudi cliccando fuori
            self.driver.find_element(By.TAG_NAME, "body").click()
            return True  # noqa: TRY300
        except Exception as e:
            self.log(f"❌ Errore selezione dropdown: {e}")
            return False
