# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Prenota BP Page
Page Object Model per la gestione Prenotazioni BP usando Playwright.
"""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from playwright.sync_api import Page, TimeoutError

from ..locators import PrenotaBPLocators


class PlaywrightPrenotaBPPage:
    """Gestisce le interazioni con la pagina Prenotazioni BP usando Playwright."""

    def __init__(self, page: Page, log_callback: Callable[[str], None] | None = None) -> None:
        self.page = page
        self.log = log_callback or print

    def _get_selector(self, locator: tuple[str, str]) -> str:
        _by, value = locator
        if value.startswith(("//", "(")):
            return f"xpath={value}"
        return value

    def _wait_for_overlay(self) -> None:
        """Attende la scomparsa di maschere di caricamento."""
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask') or contains(@class, 'full-loader')][not(contains(@style,'display: none'))]"
            self.page.wait_for_selector(f"xpath={xpath}", state="hidden", timeout=5000)
        except TimeoutError:
            pass

    def navigate_to_gestione_bp(self) -> None:
        """Naviga verso la sezione Gestione Buono di Prelievo."""
        self.log("Navigazione verso Gestione Buono di Prelievo...")
        self._wait_for_overlay()

        filter_sel = self._get_selector(PrenotaBPLocators.FILTER_FORNITORE)
        if self.page.is_visible(filter_sel):
            self.log("Pagina Gestione BP già caricata.")
            return

        submenu_sel = self._get_selector(PrenotaBPLocators.SUBMENU_GESTIONE_BP)
        if self.page.is_visible(submenu_sel):
            self.log("Voce menu visibile, click diretto.")
            self.page.click(submenu_sel)
        else:
            self.log("Espansione menu 'Buono di Prelievo'...")
            self.page.click(self._get_selector(PrenotaBPLocators.MENU_BUONO_PRELIEVO))
            self.page.wait_for_selector(submenu_sel, state="visible")
            self.page.click(submenu_sel)

        self._wait_for_overlay()
        self.page.wait_for_selector(filter_sel, state="visible")
        self.log("Sezione Gestione BP caricata.")

    def filtra_buoni_prelievo(
        self,
        fornitore: str | None = None,
        numero_bp: str | None = None,
        data_da: str | None = None,
        data_a: str | None = None,
    ) -> None:
        """Imposta i filtri di ricerca."""
        self.log("Impostazione filtri di ricerca...")

        if fornitore:
            try:
                self.log(f"  Selezione fornitore: '{fornitore}'...")
                arrow_sel = self._get_selector(PrenotaBPLocators.FILTER_FORNITORE_ARROW)
                self.page.click(arrow_sel)

                option_xpath = f"xpath=//li[normalize-space(text())='{fornitore}']"
                self.page.wait_for_selector(option_xpath, state="visible", timeout=5000)
                self.page.click(option_xpath)
                self._wait_for_overlay()
            except Exception as e:
                self.log(f"  ⚠ Avviso: Selezione fornitore fallita ({e}), tento inserimento manuale.")
                self.page.fill(self._get_selector(PrenotaBPLocators.FILTER_FORNITORE), fornitore)

        if numero_bp:
            self.page.fill(self._get_selector(PrenotaBPLocators.FILTER_NUMERO_BP), numero_bp)

        if data_da:
            self.page.fill(self._get_selector(PrenotaBPLocators.FILTER_DATA_DA), data_da)

        if data_a:
            self.page.fill(self._get_selector(PrenotaBPLocators.FILTER_DATA_A), data_a)

        self.page.click(self._get_selector(PrenotaBPLocators.BT_CERCA))
        self._wait_for_overlay()
        self.log("Ricerca completata.")

    def apri_dettagli_bp(self) -> None:
        """Apre i dettagli del primo BP."""
        self.log("Apertura dettagli BP...")
        self.page.click(self._get_selector(PrenotaBPLocators.ICON_DETTAGLI))
        self._wait_for_overlay()
        self.page.wait_for_selector(self._get_selector(PrenotaBPLocators.WINDOW_DETTAGLI), state="visible")

    def chiudi_dettagli_bp(self) -> None:
        """Chiude la finestra dettagli."""
        self.log("Chiusura finestra dettagli...")
        self.page.click(self._get_selector(PrenotaBPLocators.BT_CHIUDI_POPUP))
        self._wait_for_overlay()

    def gestisci_creazione_richiesta(self, note: str) -> None:
        """Gestisce il flusso di creazione richiesta bondo."""
        self.log("Gestione creazione richiesta...")

        available_indices, total_rows = self._analizza_disponibilita()
        if total_rows == 0:
            return

        if not self._esegui_selezione(available_indices, total_rows):
            return

        self._compila_form_richiesta(note)

    def _analizza_disponibilita(self) -> tuple[list[int], int]:
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
        count_available = len(available_indices)
        if count_available == 0:
            self.log("⚠ Nessun materiale disponibile.")
            return False

        if count_available == total_rows:
            self.log("✓ Tutti i materiali disponibili. Seleziono tutto.")
            self.page.click(self._get_selector(PrenotaBPLocators.HEADER_CHECKBOX_SELECT_ALL))
            return True

        self.log(f"⚠ Disponibili {count_available} su {total_rows}. Selezione puntuale.")
        checkers_sel = self._get_selector(PrenotaBPLocators.GRID_CHECKERS)
        checkers = self.page.locator(checkers_sel).all()

        count_selected = 0
        for idx in available_indices:
            if idx < len(checkers):
                checkers[idx].click()
                count_selected += 1
        return count_selected > 0

    def _compila_form_richiesta(self, note: str) -> None:
        self.log("Click su 'Crea Richiesta'...")
        self.page.click(self._get_selector(PrenotaBPLocators.BT_CREA_RICHIESTA))
        self._wait_for_overlay()

        now = datetime.now(UTC).astimezone()
        data_oggi = now.strftime("%d/%m/%Y")
        ora_attuale = now.strftime("%H%M")
        ora_fine = (now + timedelta(minutes=30)).strftime("%H%M")

        form_sel = self._get_selector(PrenotaBPLocators.FORM_DATA_RITIRO)
        self.page.wait_for_selector(form_sel, state="visible")

        self.page.fill(form_sel, data_oggi)
        self.page.fill(self._get_selector(PrenotaBPLocators.FORM_ORA_INIZIO), ora_attuale)
        self.page.fill(self._get_selector(PrenotaBPLocators.FORM_ORA_FINE), ora_fine)
        self.page.fill(self._get_selector(PrenotaBPLocators.FORM_NOTE), note)

        self.log("Salvataggio richiesta...")
        self.page.click(self._get_selector(PrenotaBPLocators.BT_SALVA))
        self._wait_for_overlay()
        self.log("Richiesta creata e salvata con successo.")
