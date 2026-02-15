"""
SyncroJob - SafeWork Login Page
Encapsulamento della logica di login SafeWork.
"""

from collections.abc import Callable

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.common.locators import SafeWorkLocators


class SafeWorkLoginPage:
    """Gestisce l'accesso al portale SafeWork."""

    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait[webdriver.Chrome], log_func: Callable[[str], None]
    ):
        self.driver = driver
        self.wait = wait
        self.log = log_func

    def login(self, username, password) -> bool:
        """
        Esegue il login con strategia differenziata in base all'account.
        """
        try:
            # 1. Azioni Comuni (Selezione Sito, Input Credenziali, Click Login)
            self._procedura_comune_login(username, password)

            # 2. Dispatcher Logica di Attesa
            if "gallegretti" in username.lower():
                self.log(f"🔄 Account COEMI ({username}): Avvio procedura di attesa COMPLETA.")
                return self._login_flow_coemi()
            self.log(f"⚡ Account TCL/Standard ({username}): Avvio procedura VELOCE.")
            return self._login_flow_tcl()

        except Exception as e:
            self.log(f"❌ Errore critico durante il login: {e}")
            return False

    def _procedura_comune_login(self, username, password):
        """Passaggi comuni a tutti gli account prima della verifica accesso."""
        MAX_RETRIES = 3
        for tentativa in range(MAX_RETRIES):
            try:
                self.log(f"⏳ Tentativo {tentativa + 1}/{MAX_RETRIES}: Selezione sito 'ISAB Sud'...")
                btn_sito = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(SafeWorkLocators.SITO_BUTTON)
                )
                btn_sito.click()

                opzione_isab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(SafeWorkLocators.ISAB_SUD_OPTION)
                )
                opzione_isab.click()

                self.log(f"🔐 Inserimento credenziali per: {username}")
                u_field = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.USERNAME_FIELD))
                u_field.clear()
                u_field.send_keys(username)

                p_field = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.PASSWORD_FIELD))
                p_field.clear()
                p_field.send_keys(password)

                self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.LOGIN_BUTTON)).click()
                break  # Successo, esci dal loop

            except (TimeoutException, Exception) as e:
                if "stale" in str(e).lower() and tentativa < MAX_RETRIES - 1:
                    self.log(f"⚠️ Rilevato elemento stale. Riprovo la procedura di login... ({e})")
                    self.driver.refresh()  # Resettiamo lo stato per sicurezza
                    continue
                self.log(f"❌ Errore irreversibile fase preliminare login: {e}")
                raise

    def _login_flow_coemi(self) -> bool:
        """
        Flusso COEMI (Lento):
        - DEVE attendere la comparsa dello spinner 'Caricamento...'
        - DEVE attendere la sua scomparsa.
        - Infine attende la Dashboard.
        """
        try:
            self.log("⏳ [COEMI] Attesa obbligatoria spinner 'Caricamento...'")
            # Timeout allineati alla logica "main" (SafeworkBaseBot._attendi_caricamento_sistema)
            # 1. Attesa comparsa (molto generosa perché il sistema può essere lento a reagire)
            WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located(SafeWorkLocators.CARICAMENTO_SPAN)
            )
            self.log("🔄 [COEMI] Spinner apparso. Attesa completamento...")

            # 2. Attesa scomparsa (fino a 5 minuti come da storico log)
            WebDriverWait(self.driver, 300).until(
                EC.invisibility_of_element_located(SafeWorkLocators.CARICAMENTO_SPAN)
            )
            self.log("✅ [COEMI] Spinner scomparso.")

            self._attendi_dashboard()
            return True
        except TimeoutException:
            self.log("⚠️ [COEMI] Timeout attesa spinner. Provo comunque a verificare la dashboard...")
            return self._attendi_dashboard()

    def _login_flow_tcl(self) -> bool:
        """
        Flusso TCL (Veloce):
        - NON attende spinner (spesso non appare nemmeno).
        - Va dritto al controllo Dashboard.
        """
        self.log("⚡ [TCL] Salto controlli caricamento. Attesa diretta dashboard.")
        return self._attendi_dashboard()

    def _attendi_dashboard(self) -> bool:
        """Verifica finale comune."""
        self.log("⏳ Verifica finale accesso Dashboard...")
        try:
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(SafeWorkLocators.HOME_BUTTON))
            self.log("✅ Dashboard raggiunta correttamente.")
            return True
        except TimeoutException:
            self.log("❌ Dashboard non raggiunta nei tempi previsti.")
            return False
