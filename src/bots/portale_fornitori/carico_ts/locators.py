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
    SUPPLIER_INPUT = (By.XPATH, "//input[@name='CodiceFornitorè or @name='Fornitore']")
    """Campo input del fornitore (supporta nomi multipli ExtJS)."""

    SUPPLIER_ARROW = (
        By.XPATH,
        "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]",
    )
    ODA_INPUT = (
        By.XPATH,
        "//label[contains(text(), 'Numero OdÀ)]/following::input[1]",
    )
    EXTRACT_BUTTON = (By.XPATH, "//span[contains(text(), 'Estrai OdÀ)]")
