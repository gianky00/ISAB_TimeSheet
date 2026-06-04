"""SyncroJob - SafeWork Login Page.

Encapsulamento della logica di login SafeWork.
"""

from collections.abc import Callable

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.wait import WebDriverWait

from src.infrastructure.bots.safework.common.locators import SafeWorkLocators


class SafeWorkLoginPage:
    """Gestisce l'accesso al portale SafeWork.

    Inizializza la pagina di login SafeWork.

    Args:
      driver: Istanza di WebDriver Chrome.
      wait: Oggetto WebDriverWait configurato.
      log_func: Funzione di callback per il logging.
    """

    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait[webdriver.Chrome], log_func: Callable[[str], None]
    ) -> None:
        self.driver = driver
        self.wait = wait
        self.log = log_func

    def login(self, username: str, password: str, account_type: str = "Esecutore") -> bool:
        """Esegue il login con strategia differenziata in base al tipo di account."""
        try:
            # 1. Azioni Comuni (Selezione Sito, Input Credenziali, Click Login)
            self._procedura_comune_login(username, password)

            # 2. Dispatcher Logica di Attesa
            # Tipo "ISAB" -> Flusso VELOCE (TCL)
            # Tipo "Esecutore" -> Flusso ROBUSTO (STANDARD)
            if account_type == "ISAB":
                self.log(f"  Account ISAB rilevato ({username}): Avvio procedura VELOCE.")
                return self._login_flow_tcl()

            self.log(f"  Account Esecutore rilevato ({username}): Avvio procedura ROBUSTA.")
            return self._login_flow_standard()

        except Exception as e:
            self.log(f"❌ Errore critico durante il login: {e}")
            return False

    def _procedura_comune_login(self, username: str, password: str) -> None:
        """Passaggi comuni a tutti gli account prima della verifica accesso."""
        max_retries = 3
        for tentativa in range(max_retries):
            try:
                self.log(f"[ATTESA] Selezione sito 'ISAB Sud' (Tentativo {tentativa + 1}/3)...")

                # Attesa dinamica: aspetta che il loader in sovrimpressione scompaia
                WebDriverWait(self.driver, 20).until(
                    EC.invisibility_of_element_located(SafeWorkLocators.OVERLAY)
                )

                btn_sito = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(SafeWorkLocators.SITO_BUTTON)
                )
                btn_sito.click()

                opzione_isab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(SafeWorkLocators.ISAB_SUD_OPTION)
                )
                opzione_isab.click()

                self.log(f"   Inserimento credenziali per {username}...")
                u_field = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.USERNAME_FIELD))
                u_field.clear()
                u_field.send_keys(username)

                p_field = self.wait.until(EC.visibility_of_element_located(SafeWorkLocators.PASSWORD_FIELD))
                p_field.clear()
                p_field.send_keys(password)

                self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.LOGIN_BUTTON)).click()
                break  # Successo, esci dal loop

            except (TimeoutException, Exception) as e:
                if "stale" in str(e).lower() and tentativa < max_retries - 1:
                    self.log("⚠️ Rilevato elemento non più valido. Ricaricamento...")
                    self.driver.refresh()
                    continue
                self.log(f"❌ Errore fase preliminare login: {e}")
                raise

    def _login_flow_standard(self) -> bool:
        """Flusso STANDARD (Lento).

        - DEVE attendere la comparsa dello spinner 'Caricamento...'
        - DEVE attendere la sua scomparsa.
        """
        try:
            self.log("[ATTESA] In attesa dello spinner di sistema...")
            WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located(SafeWorkLocators.CARICAMENTO_SPAN)
            )
            self.log("[ATTESA] Sistema in caricamento (attesa completamento)...")

            WebDriverWait(self.driver, 300).until(
                EC.invisibility_of_element_located(SafeWorkLocators.CARICAMENTO_SPAN)
            )
            self.log("✅ Caricamento sistema completato.")

            return self._attendi_dashboard()
        except TimeoutException:
            self.log("⚠️ Timeout caricamento. Verifica diretta dashboard...")
            return self._attendi_dashboard()

    def _login_flow_tcl(self) -> bool:
        """Flusso TCL (Veloce)."""
        return self._attendi_dashboard()

    def _attendi_dashboard(self) -> bool:
        """Verifica finale comune."""
        try:
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(SafeWorkLocators.HOME_BUTTON))
            self.log("✅ Accesso alla Dashboard completato.")
        except TimeoutException:
            self.log("❌ Dashboard non raggiunta.")
            return False
        else:
            return True
