"""
SyncroJob - Scarico TS Locators
Selectors for the Scarico TS bot.
"""

from selenium.webdriver.common.by import By


class ScaricoTSLocators:
    """Locators for the Scarico TS page."""

    # Navigation
    REPORT_MENU = (By.XPATH, "//*[normalize-space(text())='Report']")
    """Pulsante menu Report nell'header."""

    TIMESHEET_MENU = (
        By.XPATH,
        "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]",
    )
    """Voce di menu Timesheet sotto Report."""

    # Filters
    SUPPLIER_INPUT = (By.XPATH, "//input[@name='CodiceFornitorè or @name='Fornitore']")
    """Campo input del fornitore (supporta nomi multipli ExtJS)."""

    SUPPLIER_DROPDOWN_ARROW = (
        By.XPATH,
        "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]",
    )
    """Freccia per aprire il dropdown del fornitore."""

    DATE_FROM_FIELD = (By.NAME, "DataTimesheetDa")
    """Campo input data inizio timesheet."""

    # Form Fields
    ODA_NUMBER_FIELD = (By.NAME, "NumeroOda")
    """Campo input numero ordine di acquisto."""

    ODA_POSITION_FIELD = (By.NAME, "PosizioneOda")
    """Campo input posizione dell'ordine."""

    # Actions
    SEARCH_BUTTON = (
        By.XPATH,
        "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Cercà and contains(@class, 'x-btn-inner')]]",
    )
    """Pulsante Cerca per applicare i filtri."""

    # Export
    EXPORT_EXCEL_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]",
    )
    """Pulsante tecnico (icona) per l'esportazione Excel dei risultati."""
