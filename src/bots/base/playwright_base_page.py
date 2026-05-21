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

    def _check_arrow_visibility(self, arrow_selector: str) -> bool:
        """Verifica se il selettore della freccia è visibile e presente nel DOM."""
        if not arrow_selector:
            return False
        try:
            arrow = self.page.locator(arrow_selector).first
            arrow_visible = bool(arrow.is_visible(timeout=1000))
        except Exception:
            return False
        else:
            return arrow_visible

    def _trigger_combobox_arrow(self, arrow_selector: str) -> bool:
        """Tenta il trigger della freccia sia tramite eventi JS che nativamente."""
        try:
            arrow = self.page.locator(arrow_selector).first
            arrow.evaluate("el => el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}))")
            arrow.evaluate("el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
        except Exception as arrow_ex:
            self.log(
                f" [COMBO] Trigger JS fallito o timeout freccia: {str(arrow_ex)[:30]}. Provo click nativo..."
            )
            with suppress(Exception):
                arrow = self.page.locator(arrow_selector).first
                arrow.click(force=True, timeout=2000)
                return True
            return False
        else:
            return True

    def _direct_fill_combobox(self, input_selector: str, item_text: str) -> bool:
        """Gestisce l'inserimento diretto del testo nell'input con invio di Enter."""
        try:
            inp = self.page.locator(input_selector).first
            inp.wait_for(state="attached", timeout=3000)
            inp.evaluate(
                "el => { el.value = ''; el.dispatchEvent(new Event('input', {bubbles: true})); el.focus(); }"
            )
            inp.type(item_text, delay=20)
            self.page.wait_for_timeout(500)

            # Tenta di rilevare ed attendere se è apparso un suggerimento per cliccarlo
            option_xpath = f"xpath=//li[normalize-space(text())='{item_text}']"
            option = self.page.locator(option_xpath).first
            try:
                option.wait_for(state="attached", timeout=1500)
            except Exception:
                # Se nessun suggerimento appare o non è necessario, premiamo semplicemente Enter
                inp.press("Enter")
                self._wait_overlay(timeout_ms=2000)
                return True
            else:
                return False  # Trovata l'opzione da cliccare, non facciamo l'Enter
        except Exception as inp_ex:
            self.log(f" [COMBO] Errore critico durante la digitazione nell'input: {str(inp_ex)[:50]}...")
            raise

    def _select_combobox_item(
        self, input_selector: str, arrow_selector: str, item_text: str, timeout_ms: int = 15000
    ) -> bool:
        """
        Seleziona un elemento in modo ultra-robusto emulando Selenium.
        Gestisce i duplicati nelle tab prendendo sempre il primo elemento visibile.
        Previene i blocchi di 30s usando timeout brevi e pre-attese esplicite.
        Supporta anche campi senza freccia fisica (inserimento diretto).
        """
        try:
            self.log(f" [COMBO] Selezione: '{item_text}'")

            has_arrow = self._check_arrow_visibility(arrow_selector)

            if has_arrow:
                self._trigger_combobox_arrow(arrow_selector)
                option_xpath = f"xpath=//li[normalize-space(text())='{item_text}']"
                try:
                    option = self.page.locator(option_xpath).first
                    option.wait_for(state="attached", timeout=2000)
                except Exception:
                    self.log(" [COMBO] Opzione non trovata, digito nell'input...")
                    has_arrow = False

            if not has_arrow:
                is_done = self._direct_fill_combobox(input_selector, item_text)
                if is_done:
                    return True

            # Click finale forzato via JS
            option_xpath = f"xpath=//li[normalize-space(text())='{item_text}']"
            option = self.page.locator(option_xpath).first
            option.wait_for(state="attached", timeout=4000)
            option.evaluate("el => { el.scrollIntoView({block: 'nearest'}); el.click(); }")

            self._wait_overlay(timeout_ms=2000)
        except Exception as e:
            self.log(f" [COMBO] Errore selezione combobox: {str(e)[:60]}...")
            return False
        else:
            return True

