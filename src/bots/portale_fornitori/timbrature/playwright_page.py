"""SyncroJob - Playwright Timbrature Page.

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
    """Gestisce le interazioni con la pagina Timbrature usando Playwright.

    Inizializza la pagina delle timbrature.

    Args:
      page: Oggetto Page di Playwright.
      log_callback: Funzione per l'invio dei log.
      download_path: Percorso per il salvataggio dei file.
    """

    def __init__(
        self,
        page: Page,
        log_callback: Callable[[str], None] | None = None,
        download_path: str = "",
    ) -> None:
        super().__init__(page, log_callback)
        self.download_path = download_path

    def navigate_to_timbrature(self) -> bool:
        """Naviga verso Report -> Timbrature in modo diretto, veloce e robusto."""
        try:
            self.log("Navigazione verso pagina Timbrature...")

            # STRATEGIA 1 (Primaria): Ricerca globale ultra-rapida "Report Timbrature"
            search_sel = self._get_selector(TimbratureLocators.HOME_SEARCH_INPUT)
            try:
                # Controlliamo rapidamente se l'input di ricerca globale è visibile all'avvio
                inp = self.page.locator(search_sel).first
                inp.wait_for(state="visible", timeout=3000)
                self.log("[NAVIGAZIONE] Uso ricerca globale per reindirizzamento immediato...")

                # Inserimento "Report Timbrature"
                inp.click(force=True, timeout=2000)
                inp.evaluate(
                    "el => { el.value = ''; el.dispatchEvent(new Event('input', {bubbles: true})); }"
                )
                inp.type("Report Timbrature", delay=30)
                self.page.wait_for_timeout(300)
                inp.press("Enter")

                # Attesa del caricamento effettivo della pagina (comparsa dell'input del fornitore)
                supplier_input_sel = self._get_selector(TimbratureLocators.SUPPLIER_INPUT)
                self.page.wait_for_selector(supplier_input_sel, state="visible", timeout=6000)
                self._wait_overlay()
                self.log("[NAVIGAZIONE] Reindirizzamento tramite ricerca globale riuscito!")
            except Exception as e:
                self.log(
                    f"[NAVIGAZIONE] Ricerca globale non disponibile o fallita ({str(e)[:30]}). Procedo con navigazione menu..."
                )
            else:
                return True

            # STRATEGIA 2 (Fallback): Navigazione manuale robusta tramite menu Report -> sottomenu Timbrature
            report_sel = self._get_selector(TimbratureLocators.REPORT_MENU)
            self.page.click(report_sel)
            self._wait_overlay()

            # Click diretto sulla voce "Timbrature" del menu per evitare la fragilità della tastiera
            timbrature_sel = self._get_selector(TimbratureLocators.TIMBRATURE_SUBMENU)
            self.page.wait_for_selector(timbrature_sel, state="visible", timeout=5000)

            try:
                self.page.locator(timbrature_sel).evaluate("el => el.click()")
            except Exception:
                self.page.click(timbrature_sel, force=True, timeout=3000)

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

            input_sel = self._get_selector(TimbratureLocators.SUPPLIER_INPUT)
            arrow_sel = self._get_selector(TimbratureLocators.COMBO_ARROW_SUPPLIER)
            # Tenta locator specifico o generico
            if not self.page.is_visible(arrow_sel):
                arrow_sel = self._get_selector(TimbratureLocators.COMBO_ARROW_GENERIC)

            if not self._select_combobox_item(input_sel, arrow_sel, fornitore):
                self.log("   Avviso: Selezione fornitore fallita, tento inserimento manuale forzato.")
                self.page.fill(input_sel, fornitore)
                self.page.press(input_sel, "Enter")

            self._wait_overlay()
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

            # Usiamo .first per gestire eventuali ambiguità residue e logghiamo se necessario
            excel_locator = self.page.locator(excel_sel)
            count = excel_locator.count()
            if count > 1:
                self.log(f"⚠️ Attenzione: trovati {count} elementi per il pulsante Excel. Uso il primo.")

            # Playwright gestisce il download in modo nativo e sicuro
            with self.page.expect_download(timeout=Timeouts.DOWNLOAD * 1000) as download_info:
                # Clic JavaScript per evitare blocchi da overlay invisibili
                excel_locator.first.evaluate("el => el.click()")

            download = download_info.value
            self.log(f"Download avviato: {download.suggested_filename}")

            dest_dir = CONFIG_DIR / "temp"
            dest_dir.mkdir(parents=True, exist_ok=True)
            new_path = dest_dir / f"timbrature_{int(time.time())}.xlsx"

            download.save_as(str(new_path))
            self.log(f"  File scaricato e salvato: {new_path.name}")
        except Exception as e:
            self.log(f"⚠️ Errore download Excel: {e}")
            return ""
        else:
            return str(new_path)
