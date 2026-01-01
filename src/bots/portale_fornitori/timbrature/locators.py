"""
Bot TS - Timbrature Locators
Specific selectors for the Timbrature bot.
"""

from selenium.webdriver.common.by import By

class TimbratureLocators:
    """Locators for the Timbrature page and elements."""

    # Navigation
    REPORT_MENU = (By.XPATH, "//*[normalize-space(text())='Report']")

    # Filters
    # Generic combo box arrow for ExtJS
    COMBO_ARROW_GENERIC = (By.XPATH, "//div[contains(@class, 'x-form-arrow-trigger')]")
    # Specific ID pattern for Supplier combo
    COMBO_ARROW_SUPPLIER = (By.XPATH, "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]")

    FILTER_DATA_DA = (By.NAME, "DataDa") # Example name, verified by logic
    FILTER_DATA_A = (By.NAME, "DataA")   # Example name, verified by logic

    # Grid
    GRID_ROWS = (By.XPATH, "//tr[contains(@class, 'x-grid-row')]")

    # Download Buttons (Multiple strategies)
    DOWNLOAD_BTN_TEXT = (By.XPATH, "//*[contains(text(), 'Esporta in Excel')]")
    DOWNLOAD_BTN_ICON = (By.XPATH, "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]")
    DOWNLOAD_BTN_ARIA = (By.XPATH, "//*[contains(@title, 'Excel') or contains(@aria-label, 'Excel') or contains(@data-qtip, 'Excel')]")
