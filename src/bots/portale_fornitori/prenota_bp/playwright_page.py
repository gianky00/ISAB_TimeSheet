"""SyncroJob - Playwright Prenota BP Page.

Page Object Model per la gestione Prenotazioni BP usando Playwright.
"""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from playwright.sync_api import Page

from src.bots.base.playwright_base_page import PlaywrightBasePage

from .locators import PrenotaBPLocators


class PlaywrightPrenotaBPPage(PlaywrightBasePage):
    """Gestisce le interazioni con la pagina Prenotazioni BP usando Playwright."""

    def __init__(self, page: Page, log_callback: Callable[[str], None] | None = None) -> None:
        """Inizializza la pagina di prenotazione BP.

        Args:
          page: Oggetto Page di Playwright.
          log_callback: Funzione per l'invio dei log.
        """
        super().__init__(page, log_callback)

    def navigate_to_gestione_bp(self) -> None:
        """Naviga verso la sezione Gestione Buono di Prelievo espandendo il menu se necessario."""
        self.log("Navigazione verso Gestione Buono di Prelievo...")
        self._wait_overlay()

        filter_sel = self._get_selector(PrenotaBPLocators.FILTER_FORNITORE)
        if self.page.is_visible(filter_sel):
            self.log("Pagina Gestione BP già caricata.")
            return

        submenu_sel = self._get_selector(PrenotaBPLocators.SUBMENU_GESTIONE_BP)
        if self.page.is_visible(submenu_sel):
            self.log("Voce menu visibile, click diretto.")
            self.page.click(submenu_sel)
        else:
            self.log("Espansione menu 'Buono di Prelievò...")
            self.page.click(self._get_selector(PrenotaBPLocators.MENU_BUONO_PRELIEVO))
            self.page.wait_for_selector(submenu_sel, state="visible")
            self.page.click(submenu_sel)

        self._wait_overlay()
        self.page.wait_for_selector(filter_sel, state="visible")
        self.log("Sezione Gestione BP caricata.")

    def filtra_buoni_prelievo(
        self,
        fornitore: str | None = None,
        numero_bp: str | None = None,
        data_da: str | None = None,
        data_a: str | None = None,
    ) -> None:
        """Imposta i filtri di ricerca per individuare il buono di prelievo.

        Args:
          fornitore: Nome del fornitore da selezionare.
          numero_bp: Numero del BP da cercare.
          data_da: Data inizio intervallo.
          data_a: Data fine intervallo.
        """
        self.log("Impostazione filtri di ricerca...")

        if fornitore:
            input_sel = self._get_selector(PrenotaBPLocators.FILTER_FORNITORE)
            arrow_sel = self._get_selector(PrenotaBPLocators.FILTER_FORNITORE_ARROW)

            if not self._select_combobox_item(input_sel, arrow_sel, fornitore):
                self.log("   Avviso: Selezione fornitore fallita, tento inserimento manuale forzato.")
                self.page.fill(input_sel, fornitore)
                self.page.press(input_sel, "Enter")

        if numero_bp:
            num_sel = self._get_selector(PrenotaBPLocators.FILTER_NUMERO_BP)
            self.page.locator(num_sel).evaluate(
                "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
                numero_bp,
            )

        if data_da:
            da_sel = self._get_selector(PrenotaBPLocators.FILTER_DATA_DA)
            self.page.locator(da_sel).evaluate(
                "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
                data_da,
            )

        if data_a:
            a_sel = self._get_selector(PrenotaBPLocators.FILTER_DATA_A)
            self.page.locator(a_sel).evaluate(
                "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
                data_a,
            )

        self.page.locator(self._get_selector(PrenotaBPLocators.BT_CERCA)).evaluate("el => el.click()")
        self._wait_overlay()
        self.log("Ricerca completata.")

    def apri_dettagli_bp(self) -> None:
        """Apre la finestra di dettaglio del primo buono di prelievo trovato."""
        self.log("Apertura dettagli BP...")
        self.page.click(self._get_selector(PrenotaBPLocators.ICON_DETTAGLI))
        self._wait_overlay()
        self.page.wait_for_selector(self._get_selector(PrenotaBPLocators.WINDOW_DETTAGLI), state="visible")

    def chiudi_dettagli_bp(self) -> None:
        """Chiude la finestra dei dettagli attualmente aperta."""
        self.log("Chiusura finestra dettagli...")
        self.page.click(self._get_selector(PrenotaBPLocators.BT_CHIUDI_POPUP))
        self._wait_overlay()

    def gestisci_creazione_richiesta(self, note: str) -> None:
        """Orchestra il flusso di analisi disponibilita', selezione materiali e creazione richiesta.

        Args:
          note: Testo da inserire nel campo note della richiesta.
        """
        self.log("Gestione creazione richiesta...")

        available_indices, total_rows = self._analizza_disponibilita()
        if total_rows == 0:
            return

        if not self._esegui_selezione(available_indices, total_rows):
            return

        self._compila_form_richiesta(note)

    def _analizza_disponibilita(self) -> tuple[list[int], int]:
        """Scansiona le righe dei dettagli per identificare i materiali disponibili."""
        rows_sel = self._get_selector(PrenotaBPLocators.GRID_ROWS_DETTAGLI)
        self.page.wait_for_selector(rows_sel, state="visible")
        rows = self.page.locator(rows_sel).all()

        indices = []
        check_xpath = self._get_selector(PrenotaBPLocators.CELL_MATERIALE_DISPONIBILE).replace("xpath=", "")

        for i, row in enumerate(rows):
            # Cerca l'icona di disponibilità all'interno della riga
            if row.locator(f"xpath={check_xpath}").count() > 0:
                indices.append(i)

        return indices, len(rows)

    def _esegui_selezione(self, available_indices: list[int], total_rows: int) -> bool:
        """Seleziona i materiali disponibili nella griglia."""
        count_available = len(available_indices)
        if count_available == 0:
            self.log("  Nessun materiale disponibile.")
            return False

        if count_available == total_rows:
            self.log("  Tutti i materiali disponibili. Seleziono tutto.")
            self.page.click(self._get_selector(PrenotaBPLocators.HEADER_CHECKBOX_SELECT_ALL))
            return True

        self.log(f"  Disponibili {count_available} su {total_rows}. Selezione puntuale.")
        checkers_sel = self._get_selector(PrenotaBPLocators.GRID_CHECKERS)
        checkers = self.page.locator(checkers_sel).all()

        count_selected = 0
        for idx in available_indices:
            if idx < len(checkers):
                checkers[idx].click()
                count_selected += 1
        return count_selected > 0

    def _compila_form_richiesta(self, note: str) -> None:
        """Compila e salva il modulo di richiesta ritiro materiale."""
        self.log("Click su 'Crea Richiestà...")
        self.page.click(self._get_selector(PrenotaBPLocators.BT_CREA_RICHIESTA))
        self._wait_overlay()

        now = datetime.now(UTC).astimezone()
        data_oggi = now.strftime("%d/%m/%Y")
        ora_attuale = now.strftime("%H%M")
        ora_fine = (now + timedelta(minutes=30)).strftime("%H%M")

        form_sel = self._get_selector(PrenotaBPLocators.FORM_DATA_RITIRO)
        self.page.wait_for_selector(form_sel, state="visible")

        self.page.locator(form_sel).evaluate(
            "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
            data_oggi,
        )
        self.page.locator(self._get_selector(PrenotaBPLocators.FORM_ORA_INIZIO)).evaluate(
            "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
            ora_attuale,
        )
        self.page.locator(self._get_selector(PrenotaBPLocators.FORM_ORA_FINE)).evaluate(
            "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
            ora_fine,
        )
        self.page.locator(self._get_selector(PrenotaBPLocators.FORM_NOTE)).evaluate(
            "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }",
            note,
        )

        self.log("Salvataggio richiesta...")
        self.page.locator(self._get_selector(PrenotaBPLocators.BT_SALVA)).evaluate("el => el.click()")
        self._wait_overlay()
        self.log("Richiesta creata e salvata con successo.")
