# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Login Page Object
Gestisce le interazioni con la pagina di login del portale ISAB usando Playwright.
"""

import time
from collections.abc import Callable

from playwright.sync_api import Page, TimeoutError

from src.bots.base.playwright_base_page import PlaywrightBasePage
from src.bots.portale_fornitori.common.locators import CommonLocators, LoginLocators
from src.core.constants import Timeouts


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
        """Riempie il form di login e preme Accedi con interazioni robuste."""
        user_sel = self._get_selector(LoginLocators.USERNAME_FIELD)
        pass_sel = self._get_selector(LoginLocators.PASSWORD_FIELD)
        comp_sel = self._get_selector(LoginLocators.COMPANY_FIELD)
        btn_sel = self._get_selector(LoginLocators.LOGIN_BUTTON)

        # Attesa esplicita per visibilità e interattività
        self.page.wait_for_selector(user_sel, state="visible", timeout=10000)

        # Focus e click preventivo per attivare trigger JS di Ext JS
        self.page.click(user_sel)
        self.page.fill(user_sel, username)

        self.page.click(pass_sel)
        self.page.fill(pass_sel, password)

        # Selezione Società (ISAB/PSER)
        try:
            self.log(f"Selezione società: {company}...")
            # Attesa visibilità campo società
            self.page.wait_for_selector(comp_sel, state="visible", timeout=5000)

            # Click sull'input società per aprire il dropdown o attivare il focus
            self.page.click(comp_sel)
            # Pulizia e inserimento testo
            self.page.fill(comp_sel, "")
            self.page.fill(comp_sel, company)
            # Micro attesa per permettere al sistema di validare l'input
            time.sleep(0.5)
            # Simula pressione INVIO per confermare la selezione nel combo
            self.page.press(comp_sel, "Enter")

            # Se è un vero dropdown ExtJS, tentiamo anche il click sull'opzione se visibile
            option_xpath = f"xpath=//li[normalize-space(text())='{company}']"
            if self.page.locator(option_xpath).is_visible():
                self.page.click(option_xpath)
        except Exception as e:
            self.log(f"[ATTENZIONE] Avviso: Selezione società '{company}' non riuscita, proseguo: {e}")

        self.log("Credenziali inserite. Clicco Accedi...")
        self.page.click(btn_sel)

        # Gestione popup sessione attiva
        self._check_and_handle_session_popup()

        self.log("Accesso inviato. Monitoraggio caricamento...")
        self._wait_overlay(Timeouts.LONG * 1000)

    def _check_and_handle_session_popup(self) -> None:
        """Controlla se appare il popup 'Sessione attiva' e clicca su Si."""
        try:
            yes_sel = self._get_selector(CommonLocators.POPUP_SESSION_YES)
            # Attesa breve per il popup di sessione già aperta
            self.page.wait_for_selector(yes_sel, state="visible", timeout=5000)
            self.log("[ATTENZIONE] Rilevata sessione precedente. Clicco su 'Si' per forzare l'accesso.")
            self.page.click(yes_sel, force=True)
            time.sleep(1)
        except TimeoutError:
            pass
        except Exception as e:
            self.log(f"Nota: Popup sessione non gestito o non presente ({e})")

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
        Esegue il login al portale ISAB.
        """
        self.log(f"Navigazione a: {self.isab_url}")

        try:
            # Caricamento pagina iniziale
            response = self.page.goto(self.isab_url, wait_until="domcontentloaded")
            if response and response.status >= 400:  # noqa: PLR2004
                self.log(f"⚠ Errore HTTP {response.status}")
                return False

            self._wait_overlay(timeout_ms=15000)

            # Controllo se siamo già loggati (sessione persistente chrome_profile)
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
