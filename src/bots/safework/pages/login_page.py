"""
SyncroJob - SafeWork Login Page
Encapsulamento della logica di login SafeWork.
"""

from collections.abc import Callable

from selenium import webdriver
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
        """Esegue il login completo."""
        try:
            self.log("⏳ Selezione sito 'ISAB Sud'...")
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
            return True
        except Exception as e:
            self.log(f"❌ Errore durante i passaggi di login: {e}")
            return False
