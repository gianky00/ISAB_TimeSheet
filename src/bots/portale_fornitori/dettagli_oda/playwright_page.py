# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Dettagli OdA Page
Page Object Model per Dettagli OdA usando Playwright.
"""

from collections.abc import Callable
from contextlib import suppress
from pathlib import Path

from playwright.sync_api import Page, TimeoutError

from src.bots.portale_fornitori.dettagli_oda.locators import DettagliOdALocators
from src.core.constants import Timeouts
from src.utils.helpers import sanitize_filename


class PlaywrightDettagliOdAPage:
    """Gestisce le interazioni con la pagina Dettagli OdA usando Playwright."""

    def __init__(self, page: Page, log_callback: Callable[[str], None] | None = None) -> None:
        self.page = page
        self._log = log_callback or print

    def log(self, msg: str) -> None:
        self._log(msg)

    def _get_selector(self, locator: tuple[str, str]) -> str:
        """Converte un locatore Selenium (By, value) in un selettore Playwright."""
        from src.bots.base.playwright_utils import get_playwright_selector  # noqa: PLC0415

        return get_playwright_selector(locator)

    def _wait_for_overlay(self, timeout_ms: int | None = None) -> None:
        t = timeout_ms or (Timeouts.OVERLAY * 1000)
        xpath = (
            "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')]"
            "[not(contains(@style,'display: none'))]"
        )
        try:
            self.page.wait_for_selector(f"xpath={xpath}", state="hidden", timeout=t)
        except TimeoutError:
            self.log("⚠️ Timeout attesa overlay.")

    def navigate_to_dettagli(self, is_first_row: bool = True) -> bool:
        """Naviga nel menu del portale fino alla pagina dei Dettagli OdA."""
        try:
            self.expand_sidebar_if_collapsed()
            self.log("Navigazione menu Report -> Oda...")

            report_sel = self._get_selector(DettagliOdALocators.REPORT_MENU)
            self.page.click(report_sel)

            if not is_first_row:
                # Se non è la prima riga, il menu potrebbe essere già aperto o richiedere un click per refresh
                # Mantengo logica originale
                self.page.click(report_sel)

            self._wait_for_overlay()

            oda_sel = self._get_selector(DettagliOdALocators.DETTAGLI_MENU)
            self.page.click(oda_sel)

            supplier_arrow_sel = self._get_selector(DettagliOdALocators.SUPPLIER_ARROW)
            self.page.wait_for_selector(supplier_arrow_sel, state="visible")
            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"✗ Navigazione fallita: {e}")
            return False

    def setup_supplier(self, supplier: str) -> bool:
        """Seleziona il fornitore dal menu a discesa."""
        try:
            self.log(f"Selezione fornitore: {supplier}")
            arrow_sel = self._get_selector(DettagliOdALocators.SUPPLIER_ARROW)
            self.page.click(arrow_sel)

            option_xpath = f"xpath=//li[contains(text(), '{supplier}')]"
            self.page.wait_for_selector(option_xpath, state="visible", timeout=15000)
            self.page.click(option_xpath)
            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"✗ Selezione fornitore fallita: {e}")
            return False

    def expand_sidebar_if_collapsed(self) -> None:
        """Espande la sidebar se necessario."""
        with suppress(Exception):
            expand_sel = self._get_selector(DettagliOdALocators.SIDEBAR_EXPAND_BUTTON)
            if self.page.is_visible(expand_sel):
                self.log("  Menu laterale collassato, espansione in corso...")
                self.page.click(expand_sel)

    def process_oda(
        self,
        oda: str,
        contract: str,
        date_da: str,
        date_a: str,
        dest_dir: Path,
    ) -> Path | None:
        """Compila il form e avvia l'esportazione."""
        try:
            if oda:
                self.page.fill(self._get_selector(DettagliOdALocators.ODA_NUMBER_FIELD), oda)

            self.page.fill(self._get_selector(DettagliOdALocators.DATE_FROM_FIELD), date_da)
            self.page.fill(self._get_selector(DettagliOdALocators.DATE_A_FIELD), date_a)

            if contract:
                self.log(f"  Inserimento contratto: {contract}")
                self.page.fill(self._get_selector(DettagliOdALocators.CONTRACT_FIELD), contract)

            checkbox_sel = self._get_selector(DettagliOdALocators.CHECKBOX_FIELD)
            # ExtJS checkboxes possono essere ostiche, usiamo click se non selezionato
            if not self.page.is_checked("input[name='GetItemServiceInfo']"):
                self.page.click(checkbox_sel)

            self.page.click(self._get_selector(DettagliOdALocators.SEARCH_BUTTON))
            self.log("  Cerca cliccato...")
            self._wait_for_overlay()

            try:
                count_sel = self._get_selector(DettagliOdALocators.RESULTS_COUNT_LABEL)
                count_text = self.page.inner_text(count_sel).strip()
                if ":" in count_text:
                    count = int(count_text.split(":")[-1].strip())
                    self.log(f"  Risultati trovati: {count}")
                    if count == 0:
                        self.log("  Nessun risultato. Salto esportazione.")
                        self._close_all_tabs()
                        return None
            except Exception as e:
                self.log(f"  ⚠️ Errore lettura conteggio: {e}")

            target_filename = ""
            if oda:
                self.log("  Apertura dettagli (OdA specifico)...")
                self.page.click(self._get_selector(DettagliOdALocators.DETAILS_ICON))
                self._wait_for_overlay()
                export_btn_sel = self._get_selector(DettagliOdALocators.EXPORT_EXCEL_TEXT)
                target_filename = f"dettaglio_oda_{sanitize_filename(oda)}.xlsx"
            else:
                self.log("  Esportazione lista generale...")
                export_btn_sel = self._get_selector(DettagliOdALocators.GENERAL_EXPORT_BUTTON)
                safe_date_a = date_a.replace(".", "-").replace("/", "-")
                target_filename = f"ODA_Generale_al_{safe_date_a}.xlsx"

            final_path = self._download(dest_dir, target_filename, export_btn_sel)
            self._close_all_tabs()
            return final_path

        except Exception as e:
            self.log(f"  ✗ Errore processamento: {e}")
            with suppress(Exception):
                self._close_all_tabs()
            return None

    def _close_all_tabs(self) -> None:
        """Chiude le schede aperte."""
        try:
            close_sel = self._get_selector(DettagliOdALocators.TAB_CLOSE_BTN)
            while self.page.is_visible(close_sel):
                self.page.click(close_sel)
                self._wait_for_overlay(timeout_ms=2000)
        except Exception as e:
            self.log(f"  ⚠️ Errore chiusura tab: {e}")

    def _download(
        self,
        dest_dir: Path,
        target_filename: str,
        selector: str,
    ) -> Path | None:
        """Esegue il download con Playwright."""
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            self.log(f"  Attendo download in: {dest_dir}")

            with self.page.expect_download(timeout=Timeouts.DOWNLOAD * 1000) as download_info:
                self.page.click(selector)

            download = download_info.value
            target_path = dest_dir / target_filename

            if target_path.exists():
                with suppress(Exception):
                    target_path.unlink()

            download.save_as(str(target_path))
            self.log(f"  ✓ Scaricato: {target_path.name}")
            return target_path
        except Exception as e:
            self.log(f"  ✗ Errore download: {e}")
            return None
