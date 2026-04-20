# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Carico TS Page
Page Object Model per Carico TS usando Playwright.
"""

from collections.abc import Callable

from playwright.sync_api import Page

from src.bots.base.playwright_base_page import PlaywrightBasePage
from src.bots.portale_fornitori.carico_ts.locators import CaricoTSLocators


class PlaywrightCaricoTSPage(PlaywrightBasePage):
    """Gestisce le interazioni con la pagina Carico TS usando Playwright."""

    def __init__(self, page: Page, log_callback: Callable[[str], None] | None = None) -> None:
        """
        Inizializza la pagina di caricamento timesheet.

        Args:
            page: Oggetto Page di Playwright.
            log_callback: Funzione per l'invio dei log.
        """
        super().__init__(page, log_callback)

    def navigate(self) -> bool:
        """Naviga verso il menu Gestione Timesheet tramite click diretto."""
        try:
            self.log("Navigazione Gestione Timesheet...")
            sel = self._get_selector(CaricoTSLocators.MANAGEMENT_MENU)
            self.page.click(sel)
            self._wait_overlay()
        except Exception as e:
            self.log(f"Errore navigazione: {e}")
            return False
        else:
            return True

    def select_supplier(self, supplier: str) -> bool:
        """
        Seleziona il fornitore dal menu a discesa della pagina in modo robusto.

        Args:
            supplier: Nome del fornitore da selezionare.

        Returns:
            True se la selezione è riuscita.
        """
        try:
            self.log(f"Selezione {supplier}...")
            input_sel = self._get_selector(CaricoTSLocators.SUPPLIER_INPUT)
            arrow_sel = self._get_selector(CaricoTSLocators.SUPPLIER_ARROW)

            if not self._select_combobox_item(input_sel, arrow_sel, supplier):
                self.log("  ⚠ Avviso: Selezione fornitore fallita, tento inserimento manuale forzato.")
                self.page.fill(input_sel, supplier)
                self.page.press(input_sel, "Enter")

            self._wait_overlay()
            return True
        except Exception as e:
            self.log(f"Errore fornitore: {e}")
            return False

    def process_oda(self, oda: str) -> bool:
        """
        Inserisce il numero OdA nel campo di input e avvia l'estrazione.

        Args:
            oda: Numero dell'ordine di acquisto da processare.

        Returns:
            True se l'operazione è stata avviata.
        """
        try:
            # Inserimento OdA forzato via JS per garantire l'aggiornamento del modello ExtJS
            inp_sel = self._get_selector(CaricoTSLocators.ODA_INPUT)
            self.page.locator(inp_sel).evaluate(
                "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
                oda,
            )
            self.page.press(inp_sel, "Enter")

            # Clic sul pulsante di estrazione
            btn_sel = self._get_selector(CaricoTSLocators.EXTRACT_BUTTON)
            self.page.locator(btn_sel).evaluate("el => el.click()")
            self.log("Estrai OdA cliccato.")

        except Exception as e:
            self.log(f"Errore processo OdA: {e}")
            return False
        else:
            return True
