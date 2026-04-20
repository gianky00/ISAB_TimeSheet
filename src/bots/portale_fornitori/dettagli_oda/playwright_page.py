# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Dettagli OdA Page
Page Object Model per Dettagli OdA usando Playwright.
"""

from collections.abc import Callable
from contextlib import suppress
from pathlib import Path

from playwright.sync_api import Page

from src.bots.base.playwright_base_page import PlaywrightBasePage
from src.bots.portale_fornitori.dettagli_oda.locators import DettagliOdALocators
from src.core.constants import Timeouts
from src.utils.helpers import sanitize_filename


class PlaywrightDettagliOdAPage(PlaywrightBasePage):
    """Gestisce le interazioni con la pagina Dettagli OdA usando Playwright."""

    def __init__(self, page: Page, log_callback: Callable[[str], None] | None = None) -> None:
        super().__init__(page, log_callback)

    def navigate_to_dettagli(self, is_first_row: bool = True) -> bool:
        """Naviga nel menu del portale fino alla pagina dei Dettagli OdA."""
        try:
            self.expand_sidebar_if_collapsed()
            self.log("Navigazione menu Report -> Oda...")

            report_sel = self._get_selector(DettagliOdALocators.REPORT_MENU)
            self.page.click(report_sel)

            if not is_first_row:
                # Se non è la prima riga, il menu potrebbe essere già aperto o richiedere un click per refresh
                self.page.click(report_sel)

            self._wait_overlay()

            oda_sel = self._get_selector(DettagliOdALocators.DETTAGLI_MENU)
            self.page.click(oda_sel)

            supplier_arrow_sel = self._get_selector(DettagliOdALocators.SUPPLIER_ARROW)
            self.page.wait_for_selector(supplier_arrow_sel, state="visible")
            self._wait_overlay()
        except Exception as e:
            self.log(f"✗ Navigazione fallita: {e}")
            return False
        else:
            return True

    def setup_supplier(self, supplier: str) -> bool:
        """
        Imposta il fornitore per il filtering dei dati in modo robusto.

        Args:
            supplier: Ragione sociale del fornitore.

        Returns:
            True se la selezione è avvenuta, False altrimenti.
        """
        try:
            self.log(f"Selezione fornitore: {supplier}")
            input_sel = self._get_selector(DettagliOdALocators.SUPPLIER_INPUT)
            arrow_sel = self._get_selector(DettagliOdALocators.SUPPLIER_ARROW)

            if not self._select_combobox_item(input_sel, arrow_sel, supplier):
                self.log("  ⚠ Avviso: Selezione fornitore fallita, tento inserimento manuale forzato.")
                self.page.fill(input_sel, supplier)
                self.page.press(input_sel, "Enter")

            self._wait_overlay()
            return True
        except Exception as e:
            self.log(f"✗ Selezione fornitore fallita: {e}")
            return False

    def expand_sidebar_if_collapsed(self) -> None:
        """Espande la sidebar se necessario in modo istantaneo."""
        with suppress(Exception):
            expand_sel = self._get_selector(DettagliOdALocators.SIDEBAR_EXPAND_BUTTON)
            btn = self.page.locator(expand_sel)
            if btn.is_visible():
                self.log("  Espansione sidebar rapida...")
                # Dispatch event bypassa l'attesa di actionability di Playwright
                btn.evaluate("el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
                self.page.wait_for_timeout(300)

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
                oda_sel = self._get_selector(DettagliOdALocators.ODA_NUMBER_FIELD)
                self.page.locator(oda_sel).evaluate(
                    "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
                    oda,
                )

            da_sel = self._get_selector(DettagliOdALocators.DATE_FROM_FIELD)
            self.page.locator(da_sel).evaluate(
                "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
                date_da,
            )

            a_sel = self._get_selector(DettagliOdALocators.DATE_A_FIELD)
            self.page.locator(a_sel).evaluate(
                "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
                date_a,
            )

            if contract:
                self.log(f"  Inserimento contratto: {contract}")
                contract_sel = self._get_selector(DettagliOdALocators.CONTRACT_FIELD)
                self.page.locator(contract_sel).evaluate(
                    "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
                    contract,
                )

            checkbox_sel = self._get_selector(DettagliOdALocators.CHECKBOX_FIELD)
            if not self.page.is_checked("input[name='GetItemServiceInfo']"):
                self.page.locator(checkbox_sel).evaluate("el => el.click()")

            self.page.locator(self._get_selector(DettagliOdALocators.SEARCH_BUTTON)).evaluate("el => el.click()")
            self.log("  Cerca cliccato...")
            self._wait_overlay()

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
                self.log(f"  [ATTENZIONE] Errore lettura conteggio: {e}")

            target_filename = ""
            if oda:
                self.log("  Apertura dettagli (OdA specifico)...")
                self.page.click(self._get_selector(DettagliOdALocators.DETAILS_ICON))
                self._wait_overlay()
                export_btn_sel = self._get_selector(DettagliOdALocators.EXPORT_EXCEL_TEXT)
                target_filename = f"dettaglio_oda_{sanitize_filename(oda)}.xlsx"
            else:
                self.log("  Esportazione lista generale...")
                export_btn_sel = self._get_selector(DettagliOdALocators.GENERAL_EXPORT_BUTTON)
                safe_date_a = date_a.replace(".", "-").replace("/", "-")
                target_filename = f"ODA_Generale_al_{safe_date_a}.xlsx"

            final_path = self._download(dest_dir, target_filename, export_btn_sel)
            self._close_all_tabs()
        except Exception as e:
            self.log(f"  ✗ Errore processamento: {e}")
            with suppress(Exception):
                self._close_all_tabs()
            return None
        else:
            return final_path

    def _close_all_tabs(self) -> None:
        """Chiude le schede aperte."""
        try:
            close_sel = self._get_selector(DettagliOdALocators.TAB_CLOSE_BTN)
            while self.page.is_visible(close_sel):
                self.page.click(close_sel)
                self._wait_overlay(timeout_ms=2000)
        except Exception as e:
            self.log(f"  [ATTENZIONE] Errore chiusura tab: {e}")

    def _download(
        self,
        dest_dir: Path,
        target_filename: str,
        selector: str,
    ) -> Path | None:
        """Esegue il download con Playwright in modo ultra-robusto."""
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            self.log(f"  Attendo download in: {dest_dir}")

            # 1. Attendi che almeno uno dei pulsanti sia nel DOM
            btn = self.page.locator(selector).first
            btn.wait_for(state="attached", timeout=5000)

            # Micro-pausa per stabilità framework (richiesta utente)
            self.page.wait_for_timeout(1000)

            # 2. Cattura il download scatenando un click JS forzato
            # Usiamo dispatchEvent per bypassare sovrapposizioni e attributi unselectable
            with self.page.expect_download(timeout=Timeouts.DOWNLOAD * 1000) as download_info:
                btn.evaluate("el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")

            download = download_info.value
            target_path = dest_dir / target_filename

            if target_path.exists():
                with suppress(Exception):
                    target_path.unlink()

            download.save_as(str(target_path))
            self.log(f"  ✓ Scaricato: {target_path.name}")
        except Exception as e:
            self.log(f"  ✗ Errore download: {e}")
            return None
        else:
            return target_path
