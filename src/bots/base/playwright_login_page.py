# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Login Page Object
Gestisce le interazioni con la pagina di login del portale ISAB usando Playwright.
"""

from collections.abc import Callable
from contextlib import suppress

from playwright.sync_api import Page, TimeoutError

from src.bots.base.playwright_base_page import PlaywrightBasePage
from src.bots.portale_fornitori.common.locators import CommonLocators, LoginLocators


class PlaywrightLoginPage(PlaywrightBasePage):
    """
    Page Object per la gestione della pagina di login con Playwright.
    """

    def __init__(
        self,
        page: Page,
        logger: Callable[[str], None] | None = None,
        isab_url: str = "",
    ) -> None:
        super().__init__(page, logger)
        self.isab_url = isab_url

    def _perform_login_form_action(self, username: str, password: str, company: str) -> None:
        """Riempie il form di login e preme Accedi in modo fulmineo."""
        user_sel = self._get_selector(LoginLocators.USERNAME_FIELD)
        pass_sel = self._get_selector(LoginLocators.PASSWORD_FIELD)
        comp_sel = self._get_selector(LoginLocators.COMPANY_FIELD)
        btn_sel = self._get_selector(LoginLocators.LOGIN_BUTTON)

        # Attesa visibilità campi (max 5s)
        self.page.wait_for_selector(user_sel, state="visible", timeout=5000)

        # Inserimento immediato via fill (senza click preventivi)
        self.page.fill(user_sel, username)
        self.page.fill(pass_sel, password)

        # Selezione Società (ISAB/PSER) rapida
        try:
            self.log(f"Selezione società: {company}...")
            # Inserimento diretto e pressione Invio
            self.page.locator(comp_sel).fill(company)
            self.page.keyboard.press("Enter")
        except Exception as e:
            self.log(f"[ATTENZIONE] Avviso: Selezione società '{company}' non riuscita, proseguo: {e}")

        self.log("Credenziali inserite. Clicco Accedi...")
        # Click forzato per evitare blocchi ExtJS
        self.page.locator(btn_sel).click(force=True)

        # Gestione popup sessione attiva (immediata)
        self._check_and_handle_session_popup()

        self.log("Accesso inviato. Monitoraggio caricamento...")
        self._wait_overlay(5000)

    def _check_and_handle_session_popup(self) -> None:
        """Controlla se appare il popup 'Sessione attiva' e clicca su Si."""
        with suppress(Exception):
            yes_sel = self._get_selector(CommonLocators.POPUP_SESSION_YES)
            # Attesa brevissima per il popup (max 2s)
            btn = self.page.wait_for_selector(yes_sel, state="visible", timeout=2000)
            if btn:
                self.log("[ATTENZIONE] Rilevata sessione precedente. Clicco su 'Si' per forzare l'accesso.")
                btn.click(force=True)

    def _verify_logged_in_via_ui(self) -> bool:
        """Verifica se siamo loggati tramite elementi UI post-login."""
        try:
            settings_sel = self._get_selector(CommonLocators.SETTINGS_BUTTON)
            # Se troviamo il tasto impostazioni, siamo loggati
            self.page.wait_for_selector(settings_sel, state="attached", timeout=8000)
        except TimeoutError:
            return False
        else:
            return True

    def login(self, username: str, password: str, company: str = "ISAB") -> bool:
        """
        Esegue il login al portale ISAB in modo rapido.
        """
        self.log(f"Navigazione a: {self.isab_url}")

        try:
            # Caricamento pagina (domcontentloaded è sufficiente)
            response = self.page.goto(self.isab_url, wait_until="domcontentloaded")
            if response and response.status >= 400:  # noqa: PLR2004
                self.log(f"⚠ Errore HTTP {response.status}")
                return False

            # Se il campo username è già lì, non perdiamo tempo con l'overlay
            user_sel = self._get_selector(LoginLocators.USERNAME_FIELD)
            if not self.page.locator(user_sel).is_visible():
                self._wait_overlay(timeout_ms=5000)

            # Controllo sessione persistente
            if self._verify_logged_in_via_ui():
                self.log("✓ Sessione già attiva rilevata.")
                return True

            try:
                # Primo tentativo di inserimento
                self._perform_login_form_action(username, password, company)
            except TimeoutError:
                self.log("[ATTENZIONE] Campi login non trovati or overlay bloccante. Ricarico pagina...")
                self.page.reload()
                self._wait_overlay(15000)
                # Secondo tentativo post-refresh
                self._perform_login_form_action(username, password, company)

            # Verifica finale
            if not self._verify_logged_in_via_ui():
                self.log("✗ Login fallito: pagina non caricata correttamente dopo accesso.")
                return False
        except Exception as e:
            self.log(f"✗ Errore critico durante il login: {e}")
            return False
        else:
            self.log("✓ Login completato con successo")
            return True
