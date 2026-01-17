"""
Page Object per la gestione Prenotazioni BP sul Portale Fornitori.
"""

import time
from datetime import datetime, timedelta
from typing import Callable, Optional

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

    def __init__(
        self, driver: WebDriver, log_callback: Optional[Callable[[str], None]] = None
    ):
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
            time.sleep(0.5)
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
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", el
                )
                time.sleep(0.3)

                # Prova il click standard
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
                time.sleep(1)
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
        time.sleep(0.1)
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
            time.sleep(1.5)  # Attesa animazione ExtJS
            submenu = self.wait.until(
                EC.element_to_be_clickable(PrenotaBPLocators.SUBMENU_GESTIONE_BP)
            )
            self.driver.execute_script("arguments[0].click();", submenu)

        self._wait_for_overlay()

        # Attesa caricamento pagina (presenza del campo Fornitore)
        self.log("Attesa caricamento filtri...")
        self.wait.until(
            EC.presence_of_element_located(PrenotaBPLocators.FILTER_FORNITORE)
        )
        self.log("Sezione Gestione BP caricata.")

    def filtra_buoni_prelievo(
        self, fornitore=None, numero_bp=None, data_da=None, data_a=None
    ):
        """Imposta i filtri di ricerca e clicca su Cerca."""
        self.log("Impostazione filtri di ricerca...")

        if fornitore:
            try:
                self.log(f"  Selezione fornitore: '{fornitore}'...")
                # 1. Click sulla freccia della combo (usando ActionChains per simulare click utente)
                from selenium.webdriver.common.action_chains import ActionChains

                arrow = self.wait.until(
                    EC.element_to_be_clickable(PrenotaBPLocators.FILTER_FORNITORE_ARROW)
                )
                ActionChains(self.driver).move_to_element(arrow).click().perform()
                time.sleep(0.8)

                # 2. Click sull'opzione nella lista
                option_xpath = f"//li[normalize-space(text())='{fornitore}']"
                option = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, option_xpath))
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'nearest'});", option
                )
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", option)
                self._wait_for_overlay()
            except Exception as e:
                self.log(
                    f"  ⚠ Avviso: Selezione fornitore fallita ({str(e)}), tento inserimento manuale."
                )
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
            self.wait.until(
                EC.visibility_of_element_located(PrenotaBPLocators.WINDOW_DETTAGLI)
            )
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
            self.wait.until(
                EC.presence_of_element_located(PrenotaBPLocators.GRID_ROWS_DETTAGLI)
            )
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
                # self.log(f"  Riga {i+1}: Disponibile ✓") # Verbose
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
        time.sleep(1)

    def gestisci_creazione_richiesta(self, note: str):
        """
        Gestisce la selezione dei materiali, la creazione della richiesta e la compilazione del form.

        Flow:
        1. Seleziona materiali (Tutti o Parziali).
        2. Clicca Crea Richiesta.
        3. Compila Form (Data, Ora, Note).
        4. Salva.
        """
        self.log("Gestione creazione richiesta...")

        # 1. Analisi disponibilità
        try:
            self.wait.until(
                EC.presence_of_element_located(PrenotaBPLocators.GRID_ROWS_DETTAGLI)
            )
            # Recuperiamo le righe "Data" (quelle con l'icona disponibilità)
            data_rows = self.driver.find_elements(*PrenotaBPLocators.GRID_ROWS_DETTAGLI)
        except Exception:
            self.log("⚠ Nessuna riga trovata per la richiesta.")
            return

        available_indices = []
        for i, row in enumerate(data_rows):
            try:
                row.find_element(*PrenotaBPLocators.CELL_MATERIALE_DISPONIBILE)
                available_indices.append(i)
            except Exception:
                pass

        total_rows = len(data_rows)
        count_available = len(available_indices)

        if total_rows == 0:
            self.log("⚠ Nessuna riga da processare.")
            return

        all_available = count_available == total_rows

        # 2. Selezione
        if all_available:
            self.log(
                "✓ Tutti i materiali disponibili. Seleziono tutto (Header Checkbox)."
            )
            try:
                self.wait_and_click(PrenotaBPLocators.HEADER_CHECKBOX_SELECT_ALL)
            except Exception as e:
                self.log(f"Errore click seleziona tutto: {e}")
        else:
            self.log(
                f"⚠ Disponibili {count_available} su {total_rows}. Seleziono singolarmente."
            )

            # Recuperiamo direttamente i checkbox (presumendo ordine visuale identico)
            try:
                checkers = self.driver.find_elements(*PrenotaBPLocators.GRID_CHECKERS)
            except Exception:
                checkers = []

            # Validazione consistenza griglia
            # Nota: i checkers potrebbero essere di più se ci sono altre griglie, ma il locator è scopato al tab visibile.
            if len(checkers) < total_rows:
                self.log(
                    f"⚠ Mismatch grave: Data={total_rows}, Checkers trovati={len(checkers)}. Potrebbe fallire la selezione."
                )

            # Iterazione per selezione puntuale
            count_selected = 0
            for idx in available_indices:
                try:
                    # Usiamo l'elemento checker corrispondente
                    if idx < len(checkers):
                        checker = checkers[idx]

                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", checker
                        )
                        time.sleep(0.1)
                        # Click sicuro
                        try:
                            checker.click()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", checker)

                        count_selected += 1
                        time.sleep(0.05)
                    else:
                        self.log(
                            f"Errore: Indice riga {idx} fuori range per i checker ({len(checkers)})."
                        )
                except Exception as e:
                    self.log(f"Errore selezione riga {idx + 1}: {e}")

            if count_selected == 0:
                self.log("⚠ Nessuna riga selezionata! Interrompo il flusso.")
                return

        # 3. Crea Richiesta e Compilazione Form
        if count_available > 0:
            self.log("Click su 'Crea Richiesta'...")
            try:
                self.wait_and_click(PrenotaBPLocators.BT_CREA_RICHIESTA)
                self._wait_for_overlay()

                # Calcolo Data e Ore
                now = datetime.now()
                data_oggi = now.strftime("%d/%m/%Y")
                ora_attuale = now.strftime("%H%M")
                ora_fine = (now + timedelta(minutes=30)).strftime("%H%M")

                self.log(
                    f"Compilazione Form Richiesta: {data_oggi} {ora_attuale}-{ora_fine}"
                )

                # Verifica che il form sia effettivamente apparso prima di compilare
                try:
                    self.wait.until(
                        EC.visibility_of_element_located(
                            PrenotaBPLocators.FORM_DATA_RITIRO
                        )
                    )
                except TimeoutException as e:
                    self.log(
                        "⚠ Il form di richiesta non è apparso. Probabile errore nella selezione o pulsante disabilitato."
                    )
                    raise Exception("Form Richiesta non visibile") from e

                self.wait_and_fill(PrenotaBPLocators.FORM_DATA_RITIRO, data_oggi)
                self.wait_and_fill(PrenotaBPLocators.FORM_ORA_INIZIO, ora_attuale)
                self.wait_and_fill(PrenotaBPLocators.FORM_ORA_FINE, ora_fine)
                self.wait_and_fill(PrenotaBPLocators.FORM_NOTE, note)

                # Conferma / Salva
                self.log("Salvataggio richiesta...")
                self.wait_and_click(PrenotaBPLocators.BT_SALVA)
                self._wait_for_overlay()
                self.log("Richiesta creata e salvata con successo.")

            except Exception as e:
                self.log(f"Errore nel flusso 'Crea Richiesta': {e}")
                # Tenta chiusura form se rimasto aperto
                try:
                    self.wait_and_click(PrenotaBPLocators.BT_CHIUDI_POPUP, timeout=3)
                except Exception:
                    pass
                raise e
        else:
            self.log("Nessun materiale disponibile. Richiesta non creata.")
