"""
Page Object per la gestione Prenotazioni BP sul Portale Fornitori.
"""

from datetime import datetime, timedelta
from typing import Callable, List, Optional, Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.core.constants import Timeouts

from ..locators import PrenotaBPLocators


class PrenotaBPPage:
    """
    Page Object Model per la gestione delle prenotazioni dei Buoni di Prelievo (BP).
    Gestisce la navigazione nei menu, il filtraggio e l'inserimento di nuove prenotazioni.
    """

    def __init__(self, driver: WebDriver, log_callback: Optional[Callable[[str], None]] = None):
        """Inizializza la pagina con il driver e configura i tempi di attesa."""
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.DEFAULT)
        self.short_wait = WebDriverWait(driver, 5)
        self._log = log_callback or print

    def log(self, message: str):
        """Inoltra i messaggi di log alla callback configurata."""
        self._log(message)

    def _wait_for_overlay(self):
        """Attende la scomparsa di maschere di caricamento."""
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask') or contains(@class, 'full-loader')][not(contains(@style,'display: none'))]"
            self.short_wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            pass

    def wait_and_click(self, locator, timeout=None):
        """
        Attende che un elemento sia cliccabile e vi clicca sopra, gestendo errori DOM.

        Args:
            locator: Tupla (By, value).
            timeout: Tempo massimo di attesa.
        Returns:
            WebElement: L'elemento cliccato.
        """
        self._wait_for_overlay()
        wait_time = timeout if timeout else Timeouts.DEFAULT

        # Retry loop per gestire DOM instabile (ExtJS)
        for attempt in range(3):
            try:
                # Aspetta che l'elemento sia presente e visibile
                el = WebDriverWait(self.driver, wait_time / 2).until(
                    EC.visibility_of_element_located(locator)
                )

                # Scroll al centro
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                try:
                    el.click()
                except Exception:
                    # Backup click via Javascript
                    self.driver.execute_script("arguments[0].click();", el)
                return el

            except (TimeoutException, AttributeError, Exception) as e:
                if attempt == 2:  # Ultimo tentativo fallito
                    self.log(f"⚠ Errore definitivo click su {locator}: {str(e)}")
                    raise e
                self.log(f"  (Riprovo click su {locator}...)")
                self._wait_for_overlay()

    def wait_and_fill(self, locator, text, timeout=None):
        """
        Attende un campo di input, lo pulisce e inserisce il testo.

        Args:
            locator: Tupla (By, value).
            text: Testo da inserire.
            timeout: Tempo massimo di attesa.
        """
        self._wait_for_overlay()
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        el = wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
        return el

    def login(self, username, password):
        """Metodo legacy per compatibilità, il login è ora gestito da BaseBot."""
        # Check immediato sessione
        try:
            if self.driver.find_elements(*PrenotaBPLocators.USER_INFO_PANEL):
                return
        except Exception:
            pass

        # Logica minima se chiamato esplicitamente
        self.log("Verifica sessione in corso...")

    def navigate_to_gestione_bp(self):
        """Naviga verso la sezione Gestione Buono di Prelievo gestendo l'espansione dei menu."""
        self.log("Navigazione verso Gestione Buono di Prelievo...")
        self._wait_for_overlay()

        # Verifica se i filtri sono già visibili (siamo già nella pagina corretta)
        try:
            if self.driver.find_elements(*PrenotaBPLocators.FILTER_FORNITORE):
                self.log("Pagina Gestione BP già caricata.")
                return
        except Exception:
            pass

        # Tentativo di click sul sottomenu se visibile
        try:
            submenu = self.short_wait.until(
                EC.visibility_of_element_located(PrenotaBPLocators.SUBMENU_GESTIONE_BP)
            )
            self.log("Voce menu visibile, click diretto.")
            self.driver.execute_script("arguments[0].click();", submenu)
        except Exception:
            # Espansione menu principale
            self.log("Espansione menu 'Buono di Prelievo'...")
            self.wait_and_click(PrenotaBPLocators.MENU_BUONO_PRELIEVO)
            submenu = self.wait.until(EC.element_to_be_clickable(PrenotaBPLocators.SUBMENU_GESTIONE_BP))
            self.driver.execute_script("arguments[0].click();", submenu)

        self._wait_for_overlay()

        # Attesa caricamento pagina (presenza del campo Fornitore)
        self.log("Attesa caricamento filtri...")
        self.wait.until(EC.presence_of_element_located(PrenotaBPLocators.FILTER_FORNITORE))
        self.log("Sezione Gestione BP caricata.")

    def filtra_buoni_prelievo(self, fornitore=None, numero_bp=None, data_da=None, data_a=None):
        """Imposta i filtri di ricerca e clicca su Cerca."""
        self.log("Impostazione filtri di ricerca...")

        if fornitore:
            try:
                self.log(f"  Selezione fornitore: '{fornitore}'...")
                # 1. Click sulla freccia della combo (usando ActionChains per simulare click utente)
                from selenium.webdriver.common.action_chains import ActionChains

                arrow = self.wait.until(EC.element_to_be_clickable(PrenotaBPLocators.FILTER_FORNITORE_ARROW))
                ActionChains(self.driver).move_to_element(arrow).click().perform()
                option_xpath = f"//li[normalize-space(text())='{fornitore}']"
                option = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, option_xpath))
                )

                self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)
                self.driver.execute_script("arguments[0].click();", option)
                self._wait_for_overlay()
            except Exception as e:
                self.log(f"  ⚠ Avviso: Selezione fornitore fallita ({str(e)}), tento inserimento manuale.")
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

    def apri_dettagli_bp(self):
        """Clicca sull'icona dettagli del primo BP in lista."""
        self.log("Apertura dettagli BP...")
        try:
            self.wait_and_click(PrenotaBPLocators.ICON_DETTAGLI)
            self._wait_for_overlay()
            # Attesa apertura tab dettagli
            self.wait.until(EC.visibility_of_element_located(PrenotaBPLocators.WINDOW_DETTAGLI))
        except Exception as e:
            self.log(f"Impossibile aprire i dettagli: {e}")
            raise e

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
            self.log("⚠ Nessuna riga trovata nei dettagli o timeout.")
            return False

        if not rows:
            self.log("⚠ Nessuna riga trovata nei dettagli.")
            return False

        all_ok = True
        for i, row in enumerate(rows):
            try:
                # Cerca l'icona di spunta verde nella riga corrente
                # Il locator è relativo (.//...)
                row.find_element(*PrenotaBPLocators.CELL_MATERIALE_DISPONIBILE)
            except Exception:
                self.log(f"  Riga {i + 1}: NON Disponibile ✗")
                all_ok = False

        if all_ok:
            self.log("✓ Tutti i materiali sono disponibili.")
        else:
            self.log("✗ Alcuni materiali NON sono disponibili.")

        return all_ok

    def chiudi_dettagli_bp(self):
        """Chiude la finestra dettagli."""
        self.log("Chiusura finestra dettagli...")
        try:
            # Usa il bottone chiudi della finestra dettagli specifica
            # Il locator generico potrebbe chiudere altro, ma qui ci fidiamo del contesto modale
            self.wait_and_click(PrenotaBPLocators.BT_CHIUDI_POPUP)
            self._wait_for_overlay()
        except Exception as e:
            self.log(f"Errore chiusura dettagli: {e}")

    def prenota_nuovo_bp(self, numero_bp, note):
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
            self.log(f"Errore durante la compilazione del form: {str(e)}")
            # Tenta di chiudere il popup in caso di errore per non bloccare i successivi
            try:
                self.wait_and_click(PrenotaBPLocators.BT_CHIUDI_POPUP, timeout=3)
            except Exception:
                pass
            raise e

        self._wait_for_overlay()

    def gestisci_creazione_richiesta(self, note: str):
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

    def _analizza_disponibilita(self) -> Tuple[List[int], int]:
        """Recupera le righe disponibili per la richiesta."""
        try:
            self.wait.until(EC.presence_of_element_located(PrenotaBPLocators.GRID_ROWS_DETTAGLI))
            data_rows = self.driver.find_elements(*PrenotaBPLocators.GRID_ROWS_DETTAGLI)

            indices = []
            for i, row in enumerate(data_rows):
                try:
                    row.find_element(*PrenotaBPLocators.CELL_MATERIALE_DISPONIBILE)
                    indices.append(i)
                except Exception:
                    pass
            return indices, len(data_rows)
        except Exception:
            self.log("⚠ Nessuna riga trovata per la richiesta.")
            return [], 0

    def _esegui_selezione(self, available_indices: List[int], total_rows: int) -> bool:
        """Esegue il click sui materiali disponibili."""
        count_available = len(available_indices)
        if count_available == 0:
            self.log("⚠ Nessun materiale disponibile.")
            return False

        if count_available == total_rows:
            self.log("✓ Tutti i materiali disponibili. Seleziono tutto.")
            self.wait_and_click(PrenotaBPLocators.HEADER_CHECKBOX_SELECT_ALL)
            return True

        self.log(f"⚠ Disponibili {count_available} su {total_rows}. Selezione puntuale.")
        checkers = self.driver.find_elements(*PrenotaBPLocators.GRID_CHECKERS)

        count_selected = 0
        for idx in available_indices:
            if idx < len(checkers):
                self._click_safe(checkers[idx])
                count_selected += 1
        return count_selected > 0

    def _compila_form_richiesta(self, note: str):
        """Compila e salva il form di richiesta."""
        self.log("Click su 'Crea Richiesta'...")
        try:
            self.wait_and_click(PrenotaBPLocators.BT_CREA_RICHIESTA)
            self._wait_for_overlay()

            now = datetime.now()
            data_oggi = now.strftime("%d/%m/%Y")
            ora_attuale = now.strftime("%H%M")
            ora_fine = (now + timedelta(minutes=30)).strftime("%H%M")

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
            try:
                self.wait_and_click(PrenotaBPLocators.BT_CHIUDI_POPUP, timeout=3)
            except Exception:
                pass
            raise e

    def _click_safe(self, element):
        """Esegue un click sicuro tramite scroll e JS fallback."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
