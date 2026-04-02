# mypy: disable-error-code="no-any-unimported, no-untyped-call"
"""
SyncroJob - Playwright Login Page Object
Gestisce le interazioni con la pagina di login del portale ISAB usando Playwright.
"""

import time
from collections.abc import Callable

from playwright.sync_api import Page, TimeoutError

from src.bots.portale_fornitori.common.locators import CommonLocators, LoginLocators
from src.core.constants import Timeouts


class PlaywrightLoginPage:
    """
    Page Object per la gestione della pagina di login con Playwright.
    """

    def __init__(
        self,
        page: Page,
        logger: Callable[[str], None] | None = None,
        isab_url: str = "",
    ) -> None:
        self.page = page
        self.log = logger or print
        self.isab_url = isab_url

    def _get_selector(self, locator: tuple[str, str]) -> str:
        """Converte un locatore Selenium (By, value) in un selettore Playwright."""
        _by, value = locator
        # Selenium (By.XPATH, "//...") -> Playwright "xpath=//..."
        # Selenium (By.NAME, "name") -> Playwright "name=name"
        if value.startswith(("//", "(")):
            return f"xpath={value}"
        return value

    def _attendi_scomparsa_overlay(self, timeout_ms: int = Timeouts.OVERLAY * 1000) -> bool:
        """
        Attende che gli overlay di caricamento Ext JS scompaiano.
        """
        try:
            xpath_combined = f"{CommonLocators.LOADING_MASK[1]} | {CommonLocators.LOADING_TEXT[1]}"
            selector = f"xpath={xpath_combined}"

            self.page.wait_for_selector(selector, state="hidden", timeout=timeout_ms)
            self.log(" -> Overlay di caricamento scomparso.")
        except TimeoutError:
            self.log(f"⚠ Timeout ({timeout_ms / 1000}s) attesa overlay. Proseguo con cautela.")
            return False
        else:
            return True

    def _perform_login_form_action(self, username: str, password: str) -> None:
        """Riempie il form di login e preme Accedi."""
        user_sel = self._get_selector(LoginLocators.USERNAME_FIELD)
        pass_sel = self._get_selector(LoginLocators.PASSWORD_FIELD)
        btn_sel = self._get_selector(LoginLocators.LOGIN_BUTTON)

        self.page.fill(user_sel, username)
        self.page.fill(pass_sel, password)

        # Clicca Accedi e gestisci eventuale popup sessione
        self.page.click(btn_sel)

        # Gestione popup sessione attiva
        self._check_and_handle_session_popup()

        self.log("Login effettuato. Attendo scomparsa overlay...")
        self._attendi_scomparsa_overlay(Timeouts.LONG * 1000)

    def _check_and_handle_session_popup(self) -> None:
        """Controlla se appare il popup 'Sessione attiva' e clicca su Si."""
        try:
            yes_sel = self._get_selector(CommonLocators.POPUP_SESSION_YES)
            # Attesa breve per il popup
            self.page.wait_for_selector(yes_sel, state="visible", timeout=3000)
            self.log("⚠️ Rilevata sessione precedente. Clicco su 'Si' per forzare l'accesso.")
            self.page.click(yes_sel)
            time.sleep(1)
        except TimeoutError:
            pass
        except Exception as e:
            self.log(f"Nota: Controllo popup sessione ignorato ({e})")

    def _verify_logged_in_via_ui(self) -> bool:
        """Verifica se siamo loggati tramite elementi UI post-login."""
        try:
            settings_sel = self._get_selector(CommonLocators.SETTINGS_BUTTON)
            self.page.wait_for_selector(settings_sel, state="attached", timeout=5000)
        except TimeoutError:
            return False
        else:
            return True

    def login(self, username: str, password: str) -> bool:
        """
        Esegue il login al portale ISAB.
        """
        self.log(f"Navigazione a: {self.isab_url}")

        try:
            response = self.page.goto(self.isab_url)
            if response and response.status >= 400:  # noqa: PLR2004
                self.log(f"⚠ Errore HTTP {response.status} durante l'accesso.")
                return False

            if "Proxy Error" in self.page.title() or "Proxy Error" in self.page.content():
                self.log("⚠ Rilevato 'Proxy Error' durante l'accesso iniziale.")
                return False

            self.log("Tentativo di login...")
            self._attendi_scomparsa_overlay(timeout_ms=10000)

            try:
                user_sel = self._get_selector(LoginLocators.USERNAME_FIELD)
                self.page.wait_for_selector(user_sel, state="visible", timeout=5000)
                self._perform_login_form_action(username, password)
            except TimeoutError:
                if self._verify_logged_in_via_ui():
                    self.log("✓ Rilevata sessione attiva (skip login).")
                    return True

                self.log("⚠️ Username assente e sessione invalida/scaduta. Ricarico...")
                self.page.reload()
                self._attendi_scomparsa_overlay(10000)

                try:
                    self._perform_login_form_action(username, password)
                    return True
                except Exception as e:
                    self.log(f"✗ Fallito recupero sessione: {e}")
                    return False

            self.log("✓ Login completato con successo")
            return True

        except TimeoutError:
            self.log("✗ Timeout durante il login")
            return False
        except Exception as e:
            self.log(f"✗ Errore login: {e}")
            return False
