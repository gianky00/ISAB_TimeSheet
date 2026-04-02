# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - Playwright SafeWork PDL Search Page
Gestisce le interazioni con la pagina di ricerca PDL usando Playwright.
"""

from collections.abc import Callable
from contextlib import suppress

from playwright.sync_api import Page, TimeoutError

from src.bots.safework.common.locators import SafeWorkLocators


class PlaywrightRicercaPDLPage:
    """Page Object per la pagina di ricerca PDL usando Playwright."""

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

    def configura_filtro_chiusi(self, exclude_closed: bool) -> None:
        """Imposta il filtro 'Escludi chiusi'."""
        try:
            sel = self._get_selector(SafeWorkLocators.ESCLUDI_CHIUSI_CHECKBOX)
            is_checked = self.page.is_checked(sel)
            if is_checked != exclude_closed:
                self.log(f"🖱️ Impostazione 'Escludi chiusi': {exclude_closed}")
                self.page.click(sel)
        except Exception as e:
            self.log(f"⚠️ Errore configurazione flag 'Escludi chiusi': {e}")

    def seleziona_sito_e_cerca(self, site_name: str) -> bool:
        """Seleziona il sito e clicca Cerca."""
        try:
            self.log(f"🏢 Selezione sito: {site_name}")

            # 1. Clic Dropdown
            site_dropdown_sel = "xpath=//span[contains(text(), 'ISAB Sud') or contains(text(), 'ISAB Nord') or contains(text(), 'IGCC') or contains(text(), 'Sito')]"
            self.page.click(site_dropdown_sel)

            # 2. Clic Opzione
            option_sel = f"xpath=//li//span[text()='{site_name}']"
            self.page.wait_for_selector(option_sel, state="visible", timeout=5000)
            self.page.click(option_sel)

            # 3. Clic Cerca
            self.log("🖱️ Clic su Cerca...")
            self.page.click("#btnCerca")

            # 4. Attesa Overlay
            self._attendi_scomparsa_overlay(timeout_ms=300000)

            return True
        except Exception as e:
            self.log(f"❌ Errore selezione/ricerca: {e}")
            return False

    def _attendi_scomparsa_overlay(self, timeout_ms: int = 300000) -> None:
        """Attende la scomparsa dell'overlay GISWaitOverlay."""
        try:
            # Verifica se appare e poi attendi scomparsa
            with suppress(TimeoutError):
                self.page.wait_for_selector("#GISWaitOverlay", state="visible", timeout=2000)

            self.page.wait_for_selector("#GISWaitOverlay", state="hidden", timeout=timeout_ms)
        except TimeoutError:
            pass

    def esporta_excel(self) -> bool:
        """Clicca sul pulsante Esporta."""
        try:
            sel = self._get_selector(SafeWorkLocators.EXPORT_BUTTON)
            self.page.click(sel)
            return True
        except Exception as e:
            self.log(f"❌ Errore click export: {e}")
            return False
