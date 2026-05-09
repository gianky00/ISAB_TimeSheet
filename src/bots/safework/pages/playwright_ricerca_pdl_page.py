# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - Playwright SafeWork PDL Search Page
Gestisce le interazioni con la pagina di ricerca PDL usando Playwright.
"""

from collections.abc import Callable
from contextlib import suppress

from playwright.sync_api import Page, TimeoutError

from src.bots.base.playwright_base_page import PlaywrightBasePage
from src.bots.safework.common.locators import SafeWorkLocators


class PlaywrightRicercaPDLPage(PlaywrightBasePage):
    """Page Object per la pagina di ricerca PDL usando Playwright."""

    def __init__(self, page: Page, log_func: Callable[[str], None]) -> None:
        super().__init__(page, log_func)

    def configura_filtro_chiusi(self, exclude_closed: bool) -> None:
        """Imposta il filtro 'Escludi chiusi'."""
        try:
            sel = self._get_selector(SafeWorkLocators.ESCLUDI_CHIUSI_CHECKBOX)
            is_checked = self.page.is_checked(sel)
            if is_checked != exclude_closed:
                self.log(f"[CLICK] Impostazione 'Escludi chiusi': {exclude_closed}")
                self.page.click(sel)
        except Exception as e:
            self.log(f"⚠️ Errore configurazione flag 'Escludi chiusi': {e}")

    def seleziona_sito_e_cerca(self, site_name: str) -> bool:
        """Seleziona il sito e clicca Cerca."""
        try:
            self.log(f"   Selezione sito: {site_name}")

            # 1. Clic Dropdown
            site_dropdown_sel = "xpath=//span[contains(text(), 'ISAB Sud') or contains(text(), 'ISAB Nord') or contains(text(), 'IGCC') or contains(text(), 'Sito')]"
            self.page.click(site_dropdown_sel)

            # 2. Clic Opzione
            option_sel = f"xpath=//li//span[text()='{site_name}']"
            self.page.wait_for_selector(option_sel, state="visible", timeout=5000)
            self.page.click(option_sel)

            # 3. Clic Cerca - Usa il selettore generico centralizzato
            self.log("[CLICK] Clic su Cerca...")
            search_btn_sel = self._get_selector(SafeWorkLocators.SEARCH_GENERIC_BUTTON)
            self.page.click(search_btn_sel)

            # 4. Attesa Overlay
            self._attendi_scomparsa_overlay(timeout_ms=300000)
        except Exception as e:
            self.log(f"❌ Errore selezione/ricerca: {e}")
            return False
        else:
            return True

    def _attendi_scomparsa_overlay(self, timeout_ms: int = 300000) -> None:
        """Attende la scomparsa dell'overlay GISWaitOverlay."""
        with suppress(TimeoutError):
            overlay_sel = self._get_selector(SafeWorkLocators.OVERLAY)
            # Verifica se appare e poi attendi scomparsa
            with suppress(TimeoutError):
                self.page.wait_for_selector(overlay_sel, state="visible", timeout=2000)

            self.page.wait_for_selector(overlay_sel, state="hidden", timeout=timeout_ms)

    def esporta_excel(self) -> bool:
        """Clicca sul pulsante Esporta."""
        try:
            sel = self._get_selector(SafeWorkLocators.EXPORT_BUTTON)
            self.page.click(sel)
        except Exception as e:
            self.log(f"❌ Errore click export: {e}")
            return False
        else:
            return True
