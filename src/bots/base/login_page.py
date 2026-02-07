"""
Bot TS - Login Page Object
Gestisce le interazioni con la pagina di login del portale ISAB.
"""

import time
from collections.abc import Callable
from contextlib import suppress

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.portale_fornitori.common.locators import CommonLocators, LoginLocators
from src.core.constants import Timeouts


class LoginPage:
    """
    Page Object per la gestione della pagina di login.
    """

    def __init__(
        self,
        driver: WebDriver,
        wait: WebDriverWait,
        logger: Callable[[str], None] | None = None,
        isab_url: str = "",
    ):
        self.driver = driver
        self.wait = wait
        self.log = logger or print
        self.isab_url = isab_url

    def _attendi_scomparsa_overlay(self, timeout_secondi: int = Timeouts.OVERLAY) -> bool:
        """
        Waits for Ext JS loading overlays to disappear.
        """
        try:
            overlay_wait = WebDriverWait(self.driver, timeout_secondi)
            xpath_combined = f"{CommonLocators.LOADING_MASK[1]} | {CommonLocators.LOADING_TEXT[1]}"

            overlay_wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_combined)))
            self.log(" -> Overlay di caricamento scomparso.")
            time.sleep(0.3)
            return True
        except TimeoutException:
            self.log(f"⚠ Timeout ({timeout_secondi}s) attesa overlay. Proseguo con cautela.")
            return False

    def _perform_login_form_action(self, username: str, password: str):
        """Fills login form and clicks Enter."""
        username_field = self.wait.until(EC.element_to_be_clickable(LoginLocators.USERNAME_FIELD))
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.wait.until(EC.element_to_be_clickable(LoginLocators.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)

        try:
            accedi_btn = self.wait.until(EC.element_to_be_clickable(LoginLocators.LOGIN_BUTTON))
            accedi_btn.click()
        except (TimeoutException, ElementClickInterceptedException):
            self.log("⚠️ Click standard intercettato o timeout. Tento click JavaScript...")
            accedi_element = self.driver.find_element(*LoginLocators.LOGIN_BUTTON_FALLBACK)
            self.driver.execute_script("arguments[0].click();", accedi_element)

        # Gestione popup sessione attiva (immediatamente dopo click)
        self._check_and_handle_session_popup()

        self.log("Login effettuato. Attendo scomparsa overlay...")
        self._attendi_scomparsa_overlay(Timeouts.LONG)

    def _check_and_handle_session_popup(self):
        """Controlla se appare il popup 'Sessione attiva' e clicca su Si."""
        try:
            # Breve attesa per il popup (non bloccante per il flusso normale)
            wait_popup = WebDriverWait(self.driver, 3)
            # Cerchiamo il bottone "Si" se appare un popup di attenzione
            yes_btn = wait_popup.until(EC.element_to_be_clickable(CommonLocators.POPUP_SESSION_YES))
            self.log("⚠️ Rilevata sessione precedente. Clicco su 'Si' per forzare l'accesso.")
            yes_btn.click()
            time.sleep(1)
        except TimeoutException:
            # Nessun popup, procedi
            pass
        except Exception as e:
            self.log(f"Nota: Controllo popup sessione ignorato ({e})")

    def _verify_logged_in_via_ui(self) -> bool:
        """Checks for post-login UI elements."""
        with suppress(Exception):
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(CommonLocators.SETTINGS_BUTTON)
            )
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        """
        Performs login to ISAB portal.
        Returns False if Proxy Error is detected.
        """
        self.log(f"Navigazione a: {self.isab_url}")

        try:
            self.driver.get(self.isab_url)

            if "Proxy Error" in self.driver.title or "Proxy Error" in self.driver.page_source:
                self.log("⚠ Rilevato 'Proxy Error' durante l'accesso iniziale.")
                return False

            self.log("Tentativo di login...")
            self._attendi_scomparsa_overlay(timeout_secondi=10)

            try:
                # 1. Cerca il form di login (comportamento standard)
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(LoginLocators.USERNAME_FIELD)
                )
                self._perform_login_form_action(username, password)
            except TimeoutException:
                # 2. Se il form non c'è, controlla se siamo già loggati (fast-skip)
                if self._verify_logged_in_via_ui():
                    self.log("✓ Rilevata sessione attiva (skip login).")
                    return True

                self.log("⚠️ Username assente e sessione invalida/scaduta.")
                self.log("🔄 Ricarico la pagina per forzare il form di login...")
                self.driver.refresh()
                self._attendi_scomparsa_overlay(10)

                try:
                    self._perform_login_form_action(username, password)
                    return True
                except Exception as e:
                    self.log(f"✗ Fallito recupero sessione: {e}")
                    return False

            self.log("✓ Login completato con successo")
            return True

        except TimeoutException:
            self.log("✗ Timeout durante il login")
            return False
        except Exception as e:
            self.log(f"✗ Errore login: {e}")
            return False
