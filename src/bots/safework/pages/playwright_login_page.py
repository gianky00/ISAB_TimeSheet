# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - Playwright SafeWork Login Page
Encapsulamento della logica di login SafeWork usando Playwright.
"""

from collections.abc import Callable
from contextlib import suppress

from playwright.sync_api import Page, TimeoutError

from src.bots.safework.common.locators import SafeWorkLocators


class PlaywrightSafeWorkLoginPage:
    """Gestisce l'accesso al portale SafeWork usando Playwright."""

    def __init__(self, page: Page, log_func: Callable[[str], None]) -> None:
        self.page = page
        self.log = log_func

    def _get_selector(self, locator: tuple[str, str]) -> str:
        _by, value = locator
        if value.startswith(("//", "(")):
            return f"xpath={value}"
        if _by == "id":
            return f"id={value}"
        return value

    def login(self, username: str, password: str, account_type: str = "Esecutore") -> bool:
        """
        Esegue il login con strategia differenziata in base al tipo di account.
        """
        try:
            # 1. Azioni Comuni
            self._procedura_comune_login(username, password)

            # 2. Dispatcher Logica di Attesa
            if account_type == "ISAB":
                self.log(f"⚡ Account ISAB rilevato ({username}): Avvio procedura VELOCE.")
                return self._login_flow_tcl()

            self.log(f"⚡ Account Esecutore rilevato ({username}): Avvio procedura ROBUSTA.")
            return self._login_flow_coemi()

        except Exception as e:
            self.log(f"❌ Errore critico durante il login: {e}")
            return False

    def _procedura_comune_login(self, username: str, password: str) -> None:
        """Passaggi comuni a tutti gli account prima della verifica accesso."""
        max_retries = 3
        for tentativa in range(max_retries):
            try:
                self.log(f"⏳ Selezione sito 'ISAB Sud' (Tentativo {tentativa + 1}/3)...")

                overlay_sel = self._get_selector(SafeWorkLocators.OVERLAY)
                with suppress(TimeoutError):
                    self.page.wait_for_selector(overlay_sel, state="hidden", timeout=10000)

                btn_sito_sel = self._get_selector(SafeWorkLocators.SITO_BUTTON)
                self.page.click(btn_sito_sel)

                opzione_isab_sel = self._get_selector(SafeWorkLocators.ISAB_SUD_OPTION)
                self.page.click(opzione_isab_sel)

                self.log(f"🔐 Inserimento credenziali per {username}...")
                u_field_sel = self._get_selector(SafeWorkLocators.USERNAME_FIELD)
                self.page.fill(u_field_sel, username)

                p_field_sel = self._get_selector(SafeWorkLocators.PASSWORD_FIELD)
                self.page.fill(p_field_sel, password)

                login_btn_sel = self._get_selector(SafeWorkLocators.LOGIN_BUTTON)
                self.page.click(login_btn_sel)
                break

            except Exception as e:
                if tentativa < max_retries - 1:
                    self.log(f"⚠️ Errore tentativa {tentativa + 1}: {e}. Ricarico...")
                    self.page.reload()
                    continue
                raise

    def _login_flow_coemi(self) -> bool:
        """Flusso COEMI (Lento)."""
        try:
            self.log("⏳ In attesa dello spinner di sistema...")
            caricamento_sel = self._get_selector(SafeWorkLocators.CARICAMENTO_SPAN)

            with suppress(TimeoutError):
                self.page.wait_for_selector(caricamento_sel, state="visible", timeout=30000)
                self.log("⏳ Sistema in caricamento (attesa completamento)...")
                self.page.wait_for_selector(caricamento_sel, state="hidden", timeout=300000)
                self.log("✅ Caricamento sistema completato.")

            return self._attendi_dashboard()
        except TimeoutError:
            self.log("⚠️ Timeout caricamento. Verifica diretta dashboard...")
            return self._attendi_dashboard()

    def _login_flow_tcl(self) -> bool:
        """Flusso TCL (Veloce)."""
        return self._attendi_dashboard()

    def _attendi_dashboard(self) -> bool:
        """Verifica finale comune."""
        try:
            home_btn_sel = self._get_selector(SafeWorkLocators.HOME_BUTTON)
            self.page.wait_for_selector(home_btn_sel, state="visible", timeout=30000)
            self.log("✅ Accesso alla Dashboard completato.")
            return True
        except TimeoutError:
            self.log("❌ Dashboard non raggiunta.")
            return False
