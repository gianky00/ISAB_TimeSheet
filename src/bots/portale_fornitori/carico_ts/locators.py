"""
SyncroJob - Carico TS Locators
Selectors for Carico TS.
"""

from selenium.webdriver.common.by import By


class CaricoTSLocators:
    """Locatori Selenium per la pagina Carico Timesheet."""

    MANAGEMENT_MENU = (
        By.XPATH,
        "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Gestione Timesheet']]",
    )
    SUPPLIER_INPUT = (
        By.XPATH,
        "//input[@name='CodiceFornitore' or @name='Fornitore' or @name='FornitoreSap']",
    )
    """Campo input del fornitore (supporta nomi multipli ExtJS)."""

    SUPPLIER_ARROW = (
        By.XPATH,
        "//input[@name='CodiceFornitore' or @name='Fornitore' or @name='FornitoreSap']/ancestor::div[contains(@class, 'x-form-trigger-wrap') or contains(@class, 'x-form-item-body')]//div[contains(@class, 'x-form-arrow-trigger')]",
    )
    ODA_INPUT = (
        By.XPATH,
        "//label[contains(text(), 'Numero OdA')]/following::input[1]",
    )
    EXTRACT_BUTTON = (By.XPATH, "//span[contains(text(), 'Estrai OdA')]")
