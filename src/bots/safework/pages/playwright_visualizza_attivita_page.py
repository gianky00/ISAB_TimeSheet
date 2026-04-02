# mypy: disable-error-code="no-any-unimported, unused-ignore, no-untyped-call"
"""
SyncroJob - Playwright SafeWork Visualizza Attività Page
Gestione della pagina Visualizza Attività per la programmazione usando Playwright.
"""

import time
from collections.abc import Callable
from contextlib import suppress

from playwright.sync_api import Page

from src.bots.safework.common.locators import SafeWorkLocators


class PlaywrightVisualizzaAttivitaPage:
    """Gestisce le interazioni con la pagina Visualizza Attività usando Playwright."""

    def __init__(self, page: Page, log_func: Callable[[str], None]) -> None:
        self.page = page
        self.log = log_func

    def _get_selector(self, locator: tuple[str, str]) -> str:
        _by, value = locator
        if value.startswith(("//", "(")):
            return f"xpath={value}"
        if _by == "id":
            return f"id={value}"
        return value

    def pulisci_pdl(self) -> None:
        """Pulisce il campo PDL/Permesso."""
        with suppress(Exception):
            sel = self._get_selector(SafeWorkLocators.NUM_PERMESSO_FIELD)
            self.page.fill(sel, "")

    def imposta_date(self, data_dal: str, data_al: str) -> None:
        """Imposta il range date."""
        try:
            self.page.evaluate(f"document.getElementById('programmazioneDal').value = '{data_dal}';")
            self.page.evaluate(f"document.getElementById('programmazioneAl').value = '{data_al}';")
        except Exception as e:
            self.log(f"⚠️ Errore impostazione date JS: {e}")

    def seleziona_ditta(self, nome_ditta: str) -> None:
        """Seleziona la ditta dal dropdown custom."""
        self._seleziona_da_dropdown(SafeWorkLocators.DITTA_BUTTON, nome_ditta)

    def seleziona_richiedente(self, items: str | list[str]) -> bool:
        """Seleziona uno o più richiedenti nel dropdown."""
        return self._seleziona_da_dropdown(SafeWorkLocators.RICHIEDENTE_BUTTON, items)

    def esegui_ricerca(self) -> None:
        """Clicca 'Avvia Ricerca'."""
        sel = self._get_selector(SafeWorkLocators.SEARCH_START_BUTTON)
        self.page.click(sel)

    def esporta_excel(self) -> bool:
        """Clicca il pulsante di esportazione Excel."""
        try:
            sel = self._get_selector(SafeWorkLocators.EXPORT_BUTTON)
            self.page.click(sel)
            return True
        except Exception as e:
            self.log(f"❌ Errore clic export: {e}")
            return False

    def _seleziona_da_dropdown(self, button_locator: tuple[str, str], items: str | list[str]) -> bool:
        """Helper per i dropdown ms-choice di SafeWork."""
        if isinstance(items, str):
            items = [items]

        try:
            # 1. Apri Dropdown
            self.page.click(self._get_selector(button_locator))

            # 2. Attendi apertura
            dropdown_sel = self._get_selector(SafeWorkLocators.DROPDOWN_OPEN)
            self.page.wait_for_selector(dropdown_sel, state="visible")

            inp_sel = f"{dropdown_sel} {self._get_selector(SafeWorkLocators.SEARCH_INPUT_IN_DROPDOWN)}"

            for item in items:
                # 3. Cerca e seleziona ogni elemento
                self.page.fill(inp_sel, item)
                time.sleep(0.5)

                try:
                    opt_sel = f"xpath=//div[contains(@class, 'ms-drop')]//li[not(contains(@class, 'ms-no-results'))]//span[contains(text(), '{item}')]"
                    self.page.click(opt_sel)
                except Exception:
                    self.log(f"⚠️ Elemento '{item}' non trovato nel dropdown.")

            # 4. Chiudi cliccando fuori (sulla home icon o body)
            self.page.click("body")
            return True
        except Exception as e:
            self.log(f"❌ Errore selezione dropdown: {e}")
            return False
