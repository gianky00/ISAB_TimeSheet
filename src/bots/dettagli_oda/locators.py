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

    # Input Fields (Based on provided HTML)
    ODA_NUMBER_FIELD = (By.NAME, "NumeroOdA")
    CONTRACT_FIELD = (By.NAME, "NumeroContratto")
    DATE_FROM_FIELD = (By.NAME, "DataCreazioneDa")
    DATE_A_FIELD = (By.NAME, "DataCreazioneA")
    CHECKBOX_FIELD = (By.NAME, "GetItemServiceInfo") # "Includi Dettaglio Prestazioni ODA"

    # Search
    SEARCH_BUTTON = (By.XPATH, "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Cerca' and contains(@class, 'x-btn-inner')]]")

    # Results
    RESULTS_COUNT_LABEL = (By.XPATH, "//label[contains(text(), 'Trovati :')]")
    DETAILS_ICON = (By.XPATH, "//div[contains(@class, 'fa-info-circle')]")

    # Export
    EXPORT_EXCEL_TEXT = (By.XPATH, "//span[contains(text(), 'Esporta in Excel')]")
    GENERAL_EXPORT_BUTTON = (By.XPATH, "//div[contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]")

    # Tabs
    TAB_CLOSE_BTN = (By.XPATH, "//*[contains(@class, 'x-tab-close-btn')]")
