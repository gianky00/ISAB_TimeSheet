# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Base Page Object
Classe base condivisa per tutti i Page Objects basati su Playwright.
"""

from collections.abc import Callable

from playwright.sync_api import Page, TimeoutError

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
        try:
            # Selettore combinato per maschere generiche e testi di caricamento
            xpath_combined = f"{CommonLocators.LOADING_MASK[1]} | {CommonLocators.LOADING_TEXT[1]}"
            selector = f"xpath={xpath_combined}"

            # Attendi che non ci siano più elementi visibili che bloccano la UI
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout_ms)
        except TimeoutError:
            pass
        except Exception as e:
            self.log(f"Nota: Errore durante l'attesa overlay: {e}")
