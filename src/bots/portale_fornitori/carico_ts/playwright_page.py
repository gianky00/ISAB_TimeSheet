# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Carico TS Page
Page Object Model per Carico TS usando Playwright.
"""

from collections.abc import Callable

from playwright.sync_api import Page, TimeoutError

from src.bots.portale_fornitori.carico_ts.locators import CaricoTSLocators
from src.core.constants import Timeouts


class PlaywrightCaricoTSPage:
    """Gestisce le interazioni con la pagina Carico TS usando Playwright."""

    def __init__(self, page: Page, log_callback: Callable[[str], None] | None = None) -> None:
        self.page = page
        self.log = log_callback or print

    def _get_selector(self, locator: tuple[str, str]) -> str:
        _by, value = locator
        if value.startswith(("//", "(")):
            return f"xpath={value}"
        return value

    def _wait_overlay(self) -> None:
        """Attende la scomparsa delle maschere di caricamento del portale."""
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            self.page.wait_for_selector(f"xpath={xpath}", state="hidden", timeout=Timeouts.OVERLAY * 1000)
        except TimeoutError:
            pass

    def navigate(self) -> bool:
        """Naviga verso il menu Gestione Timesheet."""
        try:
            self.log("Navigazione Gestione Timesheet...")
            sel = self._get_selector(CaricoTSLocators.MANAGEMENT_MENU)
            self.page.click(sel)
            self._wait_overlay()
            return True
        except Exception as e:
            self.log(f"Errore navigazione: {e}")
            return False

    def select_supplier(self, supplier: str) -> bool:
        """Seleziona il fornitore dal menu a discesa."""
        try:
            self.log(f"Selezione {supplier}...")
            arrow_sel = self._get_selector(CaricoTSLocators.SUPPLIER_ARROW)
            self.page.click(arrow_sel)

            opt_xpath = f"xpath=//li[contains(text(), '{supplier}')]"
            self.page.wait_for_selector(opt_xpath, state="visible", timeout=5000)
            self.page.click(opt_xpath)
            self._wait_overlay()
            return True
        except Exception as e:
            self.log(f"Errore fornitore: {e}")
            return False

    def process_oda(self, oda: str) -> bool:
        """Inserisce il numero OdA e avvia l'estrazione."""
        try:
            self.log(f"Inserimento OdA: {oda}")
            inp_sel = self._get_selector(CaricoTSLocators.ODA_INPUT)

            # Playwright fill handles input events automatically
            self.page.fill(inp_sel, oda)
            self.page.press(inp_sel, "Enter")

            btn_sel = self._get_selector(CaricoTSLocators.EXTRACT_BUTTON)
            self.page.click(btn_sel)
            self.log("Estrai OdA cliccato.")
            return True
        except Exception as e:
            self.log(f"Errore processo OdA: {e}")
            return False
