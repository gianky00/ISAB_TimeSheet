# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Base Page Object
Classe base condivisa per tutti i Page Objects basati su Playwright.
"""

from collections.abc import Callable
from contextlib import suppress

from playwright.sync_api import Page

from src.bots.base.playwright_utils import get_playwright_selector
from src.bots.portale_fornitori.common.locators import CommonLocators
from src.core.constants import Timeouts


class PlaywrightBasePage:
    """
    Classe base per la gestione delle interazioni con le pagine usando Playwright.
    """

    def __init__(self, page: Page, logger: Callable[[str], None] | None = None) -> None:
        self.page = page
        self.log = logger or print

    def _get_selector(self, locator: tuple[str, str]) -> str:
        """Converte un locatore Selenium (By, value) in un selettore Playwright CSS/XPath."""
        return get_playwright_selector(locator)

    def _wait_overlay(self, timeout_ms: int = Timeouts.OVERLAY * 1000) -> None:
        """Attende la scomparsa delle maschere di caricamento del portale."""
        with suppress(Exception):
            # Selettore combinato per maschere generiche e testi di caricamento
            xpath_combined = f"{CommonLocators.LOADING_MASK[1]} | {CommonLocators.LOADING_TEXT[1]}"
            selector = f"xpath={xpath_combined}"

            # Attendi che non ci siano più elementi visibili che bloccano la UI
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout_ms)

    def _select_combobox_item(
        self, input_selector: str, arrow_selector: str, item_text: str, timeout_ms: int = 15000
    ) -> bool:
        """
        Seleziona un elemento in modo ultra-robusto emulando Selenium.
        Gestisce i duplicati nelle tab prendendo sempre il primo elemento visibile.
        """
        try:
            self.log(f"  [COMBO] Selezione: '{item_text}'")

            # 1. Trigger freccia (usiamo .first per i duplicati ExtJS)
            with suppress(Exception):
                # Puntiamo al primo elemento visibile se ce ne sono multipli (come Selenium)
                arrow = self.page.locator(arrow_selector).first
                arrow.evaluate("el => el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}))")
                arrow.evaluate("el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")

            # 2. Ricerca opzione nella lista (le liste ExtJS sono a fine body)
            option_xpath = f"xpath=//li[normalize-space(text())='{item_text}']"

            try:
                # Attesa breve per la comparsa dell'opzione (.first gestisce ambiguità)
                option = self.page.locator(option_xpath).first
                option.wait_for(state="attached", timeout=2000)
            except Exception:
                # 3. Fallback: Digitazione nell'input (sempre il primo visibile)
                self.log("  [COMBO] Opzione non trovata, digito nell'input...")
                inp = self.page.locator(input_selector).first

                inp.evaluate(
                    "el => { el.value = ''; el.dispatchEvent(new Event('input', {bubbles: true})); el.focus(); }"
                )
                inp.type(item_text, delay=20)
                self.page.wait_for_timeout(500)
                option = self.page.locator(option_xpath).first

            # 4. Click finale forzato via JS
            option.wait_for(state="attached", timeout=5000)
            option.evaluate("el => { el.scrollIntoView({block: 'nearest'}); el.click(); }")

            self._wait_overlay(timeout_ms=2000)
        except Exception as e:
            self.log(f"  [COMBO] Errore: {str(e)[:50]}...")
            return False
        else:
            return True
