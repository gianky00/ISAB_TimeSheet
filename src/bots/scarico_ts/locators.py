"""
Bot TS - Scarico TS Locators
Selectors for the Scarico TS bot.
"""

from selenium.webdriver.common.by import By

class ScaricoTSLocators:
    """Locators for the Scarico TS page."""

    # Navigation
    REPORT_MENU = (By.XPATH, "//*[normalize-space(text())='Report']")
    TIMESHEET_MENU = (By.XPATH, "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]")

    # Filters
    SUPPLIER_DROPDOWN_ARROW = (By.XPATH, "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]")
    # Dynamic XPath for supplier option: f"//li[normalize-space(text())='{supplier}']"

    DATE_FROM_FIELD = (By.NAME, "DataTimesheetDa")

    # Form Fields
    ODA_NUMBER_FIELD = (By.NAME, "NumeroOda")
    ODA_POSITION_FIELD = (By.NAME, "PosizioneOda")

    # Actions
    SEARCH_BUTTON = (By.XPATH, "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Cerca' and contains(@class, 'x-btn-inner')]]")

    # Export
    # Same as Timbrature, but specific context
    EXPORT_EXCEL_BUTTON = (By.XPATH, "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]")
