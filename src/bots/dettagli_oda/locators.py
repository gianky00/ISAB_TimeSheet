"""
Bot TS - Dettagli OdA Locators
Selectors for the Dettagli OdA bot.
"""

from selenium.webdriver.common.by import By

class DettagliOdALocators:
    """Locators for Dettagli OdA."""

    # Navigation
    REPORT_MENU = (By.XPATH, "//*[normalize-space(text())='Report']")
    DETTAGLI_MENU = (By.XPATH, "//span[contains(@class, 'x-btn-inner') and normalize-space(text())='Oda']")

    # Filters
    SUPPLIER_ARROW = (By.XPATH, "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]")
    SUPPLIER_INPUT = (By.XPATH, "//label[contains(text(), 'Fornitore')]/following::input[1]")
    # Contract is dynamic
    DATE_A_FIELD = (By.NAME, "DataOdAA")

    # Input
    ODA_NUMBER_FIELD = (By.XPATH, "//label[contains(text(), 'Numero OdA')]/following::input[1]")
    CONTRACT_FIELD = (By.XPATH, "//label[contains(text(), 'Numero Contratto')]/following::input[1]")

    # Search
    SEARCH_BUTTON = (By.XPATH, "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Cerca' and contains(@class, 'x-btn-inner')]]")

    # Export
    EXPORT_EXCEL_TEXT = (By.XPATH, "//*[contains(text(), 'Esporta in Excel')]")
