# mypy: disable-error-code="no-any-unimported, name-defined, no-untyped-call"
"""
SyncroJob - Playwright Timbrature Page
Page Object Model per la sezione Timbrature usando Playwright.
"""

import time
from collections.abc import Callable

from playwright.sync_api import Page

from src.bots.base.playwright_base_page import PlaywrightBasePage
from src.bots.portale_fornitori.timbrature.locators import TimbratureLocators
from src.core.constants import Timeouts
from src.core.paths import CONFIG_DIR


class PlaywrightTimbraturePage(PlaywrightBasePage):
    """Gestisce le interazioni con la pagina Timbrature usando Playwright."""

    def __init__(
        self,
        page: Page,
        log_callback: Callable[[str], None] | None = None,
        download_path: str = "",
    ) -> None:
        """
        Inizializza la pagina delle timbrature.

        Args:
            page: Oggetto Page di Playwright.
            log_callback: Funzione per l'invio dei log.
            download_path: Percorso per il salvataggio dei file.
        """
        super().__init__(page, log_callback)
        self.download_path = download_path

    def navigate_to_timbrature(self) -> bool:
        """Naviga verso Report -> Timbrature."""
        try:
            self.log("Navigazione verso pagina Timbrature...")
            report_sel = self._get_selector(TimbratureLocators.REPORT_MENU)

            self.page.click(report_sel)

            # Navigazione da tastiera (come nell'originale)
            self.page.keyboard.press("Tab")
            self.page.wait_for_timeout(300)
            self.page.keyboard.press("Tab")
            self.page.wait_for_timeout(300)
            self.page.keyboard.press("Tab")
            self.page.wait_for_timeout(300)
            self.page.keyboard.press("Enter")

            self._wait_overlay()
        except Exception as e:
            self.log(f"Errore navigazione: {e}")
            return False
        else:
            return True

    def set_filters(self, fornitore: str, data_da: str, data_a: str) -> bool:
        """Imposta i filtri di ricerca (fornitore e date)."""
        try:
            if fornitore:
                self._select_supplier(fornitore)

            self.log("Imposto filtri data e flag...")

            # Sequenza Tab per raggiungere i campi data (come originale)
            self.page.keyboard.press("Tab")
            self.page.wait_for_timeout(500)
            if data_da:
                self.page.keyboard.type(data_da, delay=50)

            self.page.keyboard.press("Tab")
            self.page.wait_for_timeout(500)
            if data_a:
                self.page.keyboard.type(data_a, delay=50)

            # Checkbox "Verifica Presenza Timesheet" (5 Tab)
            for _ in range(5):
                self.page.keyboard.press("Tab")
                self.page.wait_for_timeout(100)

            # Toggle check (Space)
            self.page.keyboard.press("Space")
            self.page.wait_for_timeout(500)

            # Bottone Cerca (1 Tab + Enter)
            self.page.keyboard.press("Tab")
            self.page.wait_for_timeout(500)
            self.page.keyboard.press("Enter")

            self.log("Eseguita sequenza tasti. Attendo caricamento...")
            self._wait_overlay()
        except Exception as e:
            self.log(f"Errore impostazione filtri: {e}")
            return False
        else:
            return True

    def _select_supplier(self, fornitore: str) -> None:
        """Seleziona il fornitore dal menu a tendina con pattern stabilità."""
        self.log(f"Seleziono fornitore: {fornitore}")
        try:
            self._wait_overlay()

            arrow_sel = self._get_selector(TimbratureLocators.COMBO_ARROW_SUPPLIER)
            # Tenta locator specifico o generico
            if not self.page.is_visible(arrow_sel):
                arrow_sel = self._get_selector(TimbratureLocators.COMBO_ARROW_GENERIC)

            self.page.click(arrow_sel)
            self.page.wait_for_timeout(1000)  # Delay rendering lista ExtJS

            # Pattern robusto: attendi che sia presente nel DOM, scrolla e clicca via JS
            option_xpath = f"xpath=//li[normalize-space(text())='{fornitore}']"
            self.page.wait_for_selector(option_xpath, state="attached", timeout=15000)

            # Scroll into view e clic forzato
            self.page.locator(option_xpath).evaluate("el => { el.scrollIntoView({block: 'nearest'}); el.click(); }")

            self._wait_overlay()
        except Exception as e:
            self.log(f"[ATTENZIONE] Erreore selezione fornitore: {e}")

    def download_excel(self) -> str:
        """Individua e clicca il pulsante Excel, gestendo il download."""
        try:
            self.log("Cerco pulsante Excel...")
            # Tenta diverse strategie come nell'originale
            strategies = [
                TimbratureLocators.DOWNLOAD_BTN_TEXT,
                TimbratureLocators.DOWNLOAD_BTN_ICON,
                TimbratureLocators.DOWNLOAD_BTN_ARIA,
            ]

            excel_sel = None
            for loc in strategies:
                sel = self._get_selector(loc)
                if self.page.is_visible(sel):
                    excel_sel = sel
                    break

            if not excel_sel:
                self.log("[ATTENZIONE] Pulsante Excel non trovato.")
                return ""

            self.log("Clicco su Excel...")

            # Playwright gestisce il download in modo nativo e sicuro
            with self.page.expect_download(timeout=Timeouts.DOWNLOAD * 1000) as download_info:
                # Clic JavaScript per evitare blocchi da overlay invisibili
                self.page.locator(excel_sel).evaluate("el => el.click()")

            download = download_info.value
            self.log(f"Download avviato: {download.suggested_filename}")

            dest_dir = CONFIG_DIR / "temp"
            dest_dir.mkdir(parents=True, exist_ok=True)
            new_path = dest_dir / f"timbrature_{int(time.time())}.xlsx"

            download.save_as(str(new_path))
            self.log(f"✓ File scaricato e salvato: {new_path.name}")
        except Exception as e:
            self.log(f"[ATTENZIONE] Errore download Excel: {e}")
            return ""
        else:
            return str(new_path)
