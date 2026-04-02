# mypy: disable-error-code="no-any-unimported, name-defined, no-untyped-call"
"""
SyncroJob - Playwright Timbrature Page
Page Object Model per la sezione Timbrature usando Playwright.
"""

import time
from collections.abc import Callable

from playwright.sync_api import Page, TimeoutError

from src.bots.portale_fornitori.timbrature.locators import TimbratureLocators
from src.core.constants import Timeouts
from src.core.paths import CONFIG_DIR


class PlaywrightTimbraturePage:
    """Gestisce le interazioni con la pagina Timbrature usando Playwright."""

    def __init__(
        self,
        page: Page,
        log_callback: Callable[[str], None] | None = None,
        download_path: str = "",
    ) -> None:
        self.page = page
        self._log = log_callback or print
        self.download_path = download_path

    def log(self, msg: str) -> None:
        self._log(msg)

    def _get_selector(self, locator: tuple[str, str]) -> str:
        _by, value = locator
        if value.startswith(("//", "(")):
            return f"xpath={value}"
        return value

    def _wait_for_overlay(self) -> None:
        """Attende che l'overlay di caricamento scompaia."""
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            self.page.wait_for_selector(f"xpath={xpath}", state="hidden", timeout=Timeouts.OVERLAY * 1000)
        except TimeoutError:
            self.log("⚠️ Timeout attesa overlay.")

    def navigate_to_timbrature(self) -> bool:
        """Naviga verso Report -> Timbrature."""
        try:
            self.log("Navigazione verso pagina Timbrature...")
            report_sel = self._get_selector(TimbratureLocators.REPORT_MENU)

            self.page.click(report_sel)

            # Navigazione da tastiera (come nell'originale)
            self.page.keyboard.press("Tab")
            time.sleep(0.3)
            self.page.keyboard.press("Tab")
            time.sleep(0.3)
            self.page.keyboard.press("Tab")
            time.sleep(0.3)
            self.page.keyboard.press("Enter")

            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"Errore navigazione: {e}")
            return False

    def set_filters(self, fornitore: str, data_da: str, data_a: str) -> bool:
        """Imposta i filtri di ricerca."""
        try:
            if fornitore:
                self._select_supplier(fornitore)

            self.log("Imposto filtri data e flag...")

            # Sequenza Tab per raggiungere i campi data (come originale)
            self.page.keyboard.press("Tab")
            time.sleep(0.5)
            if data_da:
                self.page.keyboard.type(data_da, delay=50)

            self.page.keyboard.press("Tab")
            time.sleep(0.5)
            if data_a:
                self.page.keyboard.type(data_a, delay=50)

            # Checkbox "Verifica Presenza Timesheet" (5 Tab)
            for _ in range(5):
                self.page.keyboard.press("Tab")
                time.sleep(0.1)

            # Toggle check (Space)
            self.page.keyboard.press("Space")
            time.sleep(0.5)

            # Bottone Cerca (1 Tab + Enter)
            self.page.keyboard.press("Tab")
            time.sleep(0.5)
            self.page.keyboard.press("Enter")

            self.log("Eseguita sequenza tasti. Attendo caricamento...")
            self._wait_for_overlay()
            return True

        except Exception as e:
            self.log(f"Errore impostazione filtri: {e}")
            return False

    def _select_supplier(self, fornitore: str) -> None:
        """Seleziona il fornitore dal menu a tendina."""
        self.log(f"Seleziono fornitore: {fornitore}")
        try:
            self._wait_for_overlay()

            arrow_sel = self._get_selector(TimbratureLocators.COMBO_ARROW_SUPPLIER)
            # Tenta locator specifico o generico
            if not self.page.is_visible(arrow_sel):
                arrow_sel = self._get_selector(TimbratureLocators.COMBO_ARROW_GENERIC)

            self.page.click(arrow_sel)

            option_xpath = f"xpath=//li[contains(text(), '{fornitore}')]"
            self.page.wait_for_selector(option_xpath, state="visible", timeout=15000)
            self.page.click(option_xpath)

            self._wait_for_overlay()
        except Exception as e:
            self.log(f"⚠️ Errore selezione fornitore: {e}")

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
                self.log("⚠️ Pulsante Excel non trovato.")
                return ""

            self.log("Clicco su Excel...")

            # Playwright gestisce il download in modo nativo e sicuro
            with self.page.expect_download(timeout=Timeouts.DOWNLOAD * 1000) as download_info:
                self.page.click(excel_sel)

            download = download_info.value
            self.log(f"Download avviato: {download.suggested_filename}")

            dest_dir = CONFIG_DIR / "temp"
            dest_dir.mkdir(parents=True, exist_ok=True)
            new_path = dest_dir / f"timbrature_{int(time.time())}.xlsx"

            download.save_as(str(new_path))
            self.log(f"✓ File scaricato e salvato: {new_path.name}")
            return str(new_path)

        except Exception as e:
            self.log(f"⚠️ Errore download Excel: {e}")
            return ""
