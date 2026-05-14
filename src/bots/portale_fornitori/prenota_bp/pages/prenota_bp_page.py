"""
Page Object per la gestione Prenotazioni BP sul Portale Fornitori.
"""

from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import Any

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.wait import WebDriverWait

from src.core.constants import Timeouts

from ..locators import PrenotaBPLocators


class PrenotaBPPage:
    """
    Page Object Model per la gestione delle prenotazioni dei Buoni di Prelievo (BP).
    Gestisce la navigazione nei menu, il filtraggio e l'inserimento di nuove prenotazioni.
    """

    def __init__(self, driver: WebDriver, log_callback: Callable[[str], None] | None = None) -> None:
        """Inizializza la pagina con il driver e configura i tempi di attesa."""
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.short_wait = WebDriverWait(driver, Timeouts.SHORT)
        self._log = log_callback or print

    def log(self, message: str) -> None:
        """Inoltra i messaggi di log alla callback configurata."""
        self._log(message)

    def _wait_for_overlay(self) -> None:
        """Attende la scomparsa di maschere di caricamento."""
        with suppress(TimeoutException):
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask') or contains(@class, 'full-loader')][not(contains(@style,'display: none'))]"
            self.short_wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    def wait_and_click(self, locator: tuple[str, str], timeout: int | float | None = None) -> Any:
        """
        Attende che un elemento sia cliccabile e vi clicca sopra, gestendo errori DOM.

        Args:
          locator: Tupla (By, value).
          timeout: Tempo massimo di attesa.
        Returns:
          WebElement: L'elemento cliccato.
        """
        self._wait_for_overlay()
        wait_time = timeout or Timeouts.DEFAULT
        max_attempts = 3

        # Retry loop per gestire DOM instabile (ExtJS)
        for attempt in range(max_attempts):
            try:
                # Aspetta che l'elemento sia presente e visibile
                el = WebDriverWait(self.driver, wait_time / 2).until(
                    EC.visibility_of_element_located(locator)
                )

                # Scroll al centro
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)  # type: ignore[no-untyped-call]
                try:
                    el.click()
                except Exception:
                    # Backup click via Javascript
                    self.driver.execute_script("arguments[0].click();", el)  # type: ignore[no-untyped-call]
            except (TimeoutException, AttributeError, Exception) as e:
                if attempt == max_attempts - 1:  # Ultimo tentativo fallito
                    self.log(f"  Errore definitivo click su {locator}: {e}")
                    raise
                self.log(f" (Riprovo click su {locator}...)")
                self._wait_for_overlay()
            else:
                return el
        return None

    def wait_and_fill(self, locator: tuple[str, str], text: str, timeout: int | float | None = None) -> Any:
        """
        Attende un campo di input, lo pulisce e inserisce il testo.

        Args:
          locator: Tupla (By, value).
          text: Testo da inserire.
          timeout: Tempo massimo di attesa.
        """
        self._wait_for_overlay()
        el = (WebDriverWait(self.driver, timeout) if timeout else self.wait).until(
            EC.visibility_of_element_located(locator)
        )
        el.clear()
        el.send_keys(text)
        return el

    def login(self, username: str, password: str) -> None:
        """Metodo legacy per compatibilità, il login è ora gestito da BaseBot."""
        # Check immediato sessione
        with suppress(Exception):
            if self.driver.find_elements(*PrenotaBPLocators.USER_INFO_PANEL):
                return

        # Logica minima se chiamato esplicitamente
        self.log("Verifica sessione in corso...")

    def navigate_to_gestione_bp(self) -> None:
        """Naviga verso la sezione Gestione Buono di Prelievo gestendo l'espansione dei menu."""
        self.log("Navigazione verso Gestione Buono di Prelievo...")
        self._wait_for_overlay()

        # Verifica se i filtri sono già visibili (siamo già nella pagina corretta)
        with suppress(Exception):
            if self.driver.find_elements(*PrenotaBPLocators.FILTER_FORNITORE):
                self.log("Pagina Gestione BP già caricata.")
                return

        # Tentativo di click sul sottomenu se visibile
        try:
            submenu = self.short_wait.until(
                EC.visibility_of_element_located(PrenotaBPLocators.SUBMENU_GESTIONE_BP)
            )
            self.log("Voce menu visibile, click diretto.")
            self.driver.execute_script("arguments[0].click();", submenu)  # type: ignore[no-untyped-call]
        except Exception:
            # Espansione menu principale
            self.log("Espansione menu 'Buono di Prelievo'...")
            self.wait_and_click(PrenotaBPLocators.MENU_BUONO_PRELIEVO)
            submenu = self.wait.until(EC.element_to_be_clickable(PrenotaBPLocators.SUBMENU_GESTIONE_BP))
            self.driver.execute_script("arguments[0].click();", submenu)  # type: ignore[no-untyped-call]

        self._wait_for_overlay()

        # Attesa caricamento pagina (presenza del campo Fornitore)
        self.log("Attesa caricamento filtri...")
        self.wait.until(EC.presence_of_element_located(PrenotaBPLocators.FILTER_FORNITORE))
        self.log("Sezione Gestione BP caricata.")

    def filtra_buoni_prelievo(
        self,
        fornitore: str | None = None,
        numero_bp: str | None = None,
        data_da: str | None = None,
        data_a: str | None = None,
    ) -> None:
        """Imposta i filtri di ricerca e clicca su Cerca."""
        self.log("Impostazione filtri di ricerca...")

        if fornitore:
            try:
                self.log(f" Selezione fornitore: '{fornitore}'...")
                # 1. Click sulla freccia della combo (usando ActionChains per simulare click utente)
                arrow = self.wait.until(EC.element_to_be_clickable(PrenotaBPLocators.FILTER_FORNITORE_ARROW))
                ActionChains(self.driver).move_to_element(arrow).click().perform()
                option_xpath = f"//li[normalize-space(text())='{fornitore}']"
                option = WebDriverWait(self.driver, Timeouts.DEFAULT).until(
                    EC.presence_of_element_located((By.XPATH, option_xpath))
                )

                self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)  # type: ignore[no-untyped-call]
                self.driver.execute_script("arguments[0].click();", option)  # type: ignore[no-untyped-call]
                self._wait_for_overlay()
            except Exception as e:
                self.log(f"   Avviso: Selezione fornitore fallita ({e}), tento inserimento manuale.")
                self.wait_and_fill(PrenotaBPLocators.FILTER_FORNITORE, fornitore)

        if numero_bp:
            self.wait_and_fill(PrenotaBPLocators.FILTER_NUMERO_BP, numero_bp)

        if data_da:
            self.wait_and_fill(PrenotaBPLocators.FILTER_DATA_DA, data_da)

        if data_a:
            self.wait_and_fill(PrenotaBPLocators.FILTER_DATA_A, data_a)

        self.wait_and_click(PrenotaBPLocators.BT_CERCA)
        self._wait_for_overlay()
        self.log("Ricerca completata.")

    def apri_dettagli_bp(self) -> None:
        """Clicca sull'icona dettagli del primo BP in lista."""
        self.log("Apertura dettagli BP...")
        try:
            self.wait_and_click(PrenotaBPLocators.ICON_DETTAGLI)
            self._wait_for_overlay()
            # Attesa apertura tab dettagli
            self.wait.until(EC.visibility_of_element_located(PrenotaBPLocators.WINDOW_DETTAGLI))
        except Exception as e:
            self.log(f"Impossibile aprire i dettagli: {e}")
            raise

    def verifica_disponibilita_materiali(self) -> bool:
        """
        Verifica se tutti i materiali sono disponibili controllando l'icona
        nell'ultima colonna della griglia dettagli.
        Returns:
          bool: True se tutti i materiali sono disponibili, False altrimenti.
        """
        self.log("Verifica disponibilità materiali...")
        try:
            # Attende che le righe siano caricate
            self.wait.until(EC.presence_of_element_located(PrenotaBPLocators.GRID_ROWS_DETTAGLI))
            rows = self.driver.find_elements(*PrenotaBPLocators.GRID_ROWS_DETTAGLI)
        except TimeoutException:
            self.log("  Nessuna riga trovata nei dettagli o timeout.")
            return False

        if not rows:
            self.log("  Nessuna riga trovata nei dettagli.")
            return False

        all_ok = True
        for i, row in enumerate(rows):
            try:
                # Cerca l'icona di spunta verde nella riga corrente
                # Il locator è relativo (.//...)
                row.find_element(*PrenotaBPLocators.CELL_MATERIALE_DISPONIBILE)
            except Exception:
                self.log(f" Riga {i + 1}: NON Disponibile  ")
                all_ok = False

        if all_ok:
            self.log("  Tutti i materiali sono disponibili.")
        else:
            self.log("  Alcuni materiali NON sono disponibili.")

        return all_ok

    def chiudi_dettagli_bp(self) -> None:
        """Chiude la finestra dettagli."""
        self.log("Chiusura finestra dettagli...")
        try:
            # Usa il bottone chiudi della finestra dettagli specifica
            # Il locator generico potrebbe chiudere altro, ma qui ci fidiamo del contesto modale
            self.wait_and_click(PrenotaBPLocators.BT_CHIUDI_POPUP)
            self._wait_for_overlay()
        except Exception as e:
            self.log(f"Errore chiusura dettagli: {e}")

    def prenota_nuovo_bp(self, numero_bp: str, note: str) -> None:
        """Esegue una singola prenotazione BP."""
        self.log(f"Inserimento nuova prenotazione: {numero_bp}")

        self.wait_and_click(PrenotaBPLocators.BT_NUOVO)
        self._wait_for_overlay()

        # Riempimento campi nel popup
        try:
            self.wait_and_fill(PrenotaBPLocators.CAMPO_NUMERO_BP, numero_bp)
            self.wait_and_fill(PrenotaBPLocators.CAMPO_NOTE, note)

            # Salvataggio
            self.wait_and_click(PrenotaBPLocators.BT_SALVA)
            self.log(f"Prenotazione {numero_bp} salvata.")
        except Exception as e:
            self.log(f"Errore durante la compilazione del form: {e}")
            # Tenta di chiudere il popup in caso di errore per non bloccare i successivi
            with suppress(Exception):
                popup_close_timeout = 3
                self.wait_and_click(PrenotaBPLocators.BT_CHIUDI_POPUP, timeout=popup_close_timeout)
            raise

        self._wait_for_overlay()

    def gestisci_creazione_richiesta(self, note: str) -> None:
        """Gestisce la selezione dei materiali, la creazione della richiesta e la compilazione del form."""
        self.log("Gestione creazione richiesta...")

        # 1. Analisi
        available_indices, total_rows = self._analizza_disponibilita()
        if total_rows == 0:
            return

        # 2. Selezione
        if not self._esegui_selezione(available_indices, total_rows):
            return

        # 3. Form
        self._compila_form_richiesta(note)

    def _analizza_disponibilita(self) -> tuple[list[int], int]:
        """Recupera le righe disponibili per la richiesta."""
        try:
            self.wait.until(EC.presence_of_element_located(PrenotaBPLocators.GRID_ROWS_DETTAGLI))
            data_rows = self.driver.find_elements(*PrenotaBPLocators.GRID_ROWS_DETTAGLI)

            indices = []
            for i, row in enumerate(data_rows):
                with suppress(Exception):
                    row.find_element(*PrenotaBPLocators.CELL_MATERIALE_DISPONIBILE)
                    indices.append(i)
            return indices, len(data_rows)
        except Exception:
            self.log("  Nessuna riga trovata per la richiesta.")
            return [], 0

    def _esegui_selezione(self, available_indices: list[int], total_rows: int) -> bool:
        """Esegue il click sui materiali disponibili."""
        count_available = len(available_indices)
        if count_available == 0:
            self.log("  Nessun materiale disponibile.")
            return False

        if count_available == total_rows:
            self.log("  Tutti i materiali disponibili. Seleziono tutto.")
            self.wait_and_click(PrenotaBPLocators.HEADER_CHECKBOX_SELECT_ALL)
            return True

        self.log(f"  Disponibili {count_available} su {total_rows}. Selezione puntuale.")
        checkers = self.driver.find_elements(*PrenotaBPLocators.GRID_CHECKERS)

        count_selected = 0
        for idx in available_indices:
            if idx < len(checkers):
                self._click_safe(checkers[idx])
                count_selected += 1
        return count_selected > 0

    def _compila_form_richiesta(self, note: str) -> None:
        """Compila e salva il form di richiesta."""
        self.log("Click su 'Crea Richiesta'...")
        try:
            self.wait_and_click(PrenotaBPLocators.BT_CREA_RICHIESTA)
            self._wait_for_overlay()

            now = datetime.now(UTC).astimezone()
            data_oggi = now.strftime("%d/%m/%Y")
            ora_attuale = now.strftime("%H%M")
            offset_minutes = 30
            ora_fine = (now + timedelta(minutes=offset_minutes)).strftime("%H%M")

            self.wait.until(EC.visibility_of_element_located(PrenotaBPLocators.FORM_DATA_RITIRO))
            self.wait_and_fill(PrenotaBPLocators.FORM_DATA_RITIRO, data_oggi)
            self.wait_and_fill(PrenotaBPLocators.FORM_ORA_INIZIO, ora_attuale)
            self.wait_and_fill(PrenotaBPLocators.FORM_ORA_FINE, ora_fine)
            self.wait_and_fill(PrenotaBPLocators.FORM_NOTE, note)

            self.log("Salvataggio richiesta...")
            self.wait_and_click(PrenotaBPLocators.BT_SALVA)
            self._wait_for_overlay()
            self.log("Richiesta creata e salvata con successo.")
        except Exception as e:
            self.log(f"Errore nel flusso 'Crea Richiesta': {e}")
            with suppress(Exception):
                popup_close_timeout = 3
                self.wait_and_click(PrenotaBPLocators.BT_CHIUDI_POPUP, timeout=popup_close_timeout)
            raise

    def _click_safe(self, element: Any) -> None:
        """Esegue un click sicuro tramite scroll e JS fallback."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)  # type: ignore[no-untyped-call]
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)  # type: ignore[no-untyped-call]
