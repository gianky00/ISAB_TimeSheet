"""SyncroJob - Dettagli OdA Locators.

Selectors for the Dettagli OdA bot.
"""

from selenium.webdriver.common.by import By


class DettagliOdALocators:
    """Locators for Dettagli OdA."""

    # Navigation
    SIDEBAR_EXPAND_BUTTON = (By.CSS_SELECTOR, ".x-tool-expand-right")
    REPORT_MENU = (By.XPATH, "//*[normalize-space(text())='Report']")
    DETTAGLI_MENU = (
        By.XPATH,
        "//span[contains(@class, 'x-btn-inner')][text()='Oda']",
    )

    SUPPLIER_INPUT = (
        By.XPATH,
        "//input[@name='CodiceFornitore' or @name='FornitoreSap' or @name='Fornitore']",
    )
    """Campo input del fornitore (supporta CodiceFornitore, FornitoreSap e Fornitore)."""

    SUPPLIER_ARROW = (
        By.XPATH,
        "//input[@name='CodiceFornitore' or @name='FornitoreSap' or @name='Fornitore']/ancestor::div[contains(@class, 'x-form-trigger-wrap') or contains(@class, 'x-form-item-body')]//div[contains(@class, 'x-form-arrow-trigger')]",
    )

    # Input Fields (Specific to Portale ISAB)
    ODA_NUMBER_FIELD = (By.CSS_SELECTOR, "input[name='NumeroOdA']")
    CONTRACT_FIELD = (By.CSS_SELECTOR, "input[name='NumeroContratto']")
    DATE_FROM_FIELD = (By.CSS_SELECTOR, "input[name='DataCreazioneDa']")
    DATE_A_FIELD = (By.CSS_SELECTOR, "input[name='DataCreazioneA']")
    CHECKBOX_FIELD = (
        By.NAME,
        "GetItemServiceInfo",
    )  # "Includi Dettaglio Prestazioni ODA"

    # Search
    SEARCH_BUTTON = (
        By.XPATH,
        "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Cerca' and contains(@class, 'x-btn-inner')]]",
    )

    # Results
    RESULTS_COUNT_LABEL = (By.XPATH, "//label[contains(text(), 'Trovati :')]")
    DETAILS_ICON = (By.XPATH, "//div[contains(@class, 'fa-info-circle')]")

    # Export
    # Puntiamo al pulsante Esporta in Excel solo se contenuto nella tab attiva (visibile)
    EXPORT_EXCEL_TEXT = (
        By.XPATH,
        "//div[contains(@class, 'x-tabpanel-child') and not(contains(@class, 'x-hidden-offsets'))]//span[contains(@class, 'x-btn-inner') and contains(text(), 'Esporta in Excel')]",
    )
    """Pulsante di export identificato nella scheda attiva per evitare ambiguit ."""
    GENERAL_EXPORT_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]",
    )

    # Tabs
    TAB_CLOSE_BTN = (By.XPATH, "//*[contains(@class, 'x-tab-close-btn')]")

    # Logout Specifics
    LOGOUT_SETTINGS_BUTTON = (By.ID, "user-info-settings")
    LOGOUT_CONFIRM_YES = (
        By.XPATH,
        "//span[(text()='Sì' or text()='Si') and contains(@class, 'x-btn-inner')]",
    )
