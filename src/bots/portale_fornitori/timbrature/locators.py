"""SyncroJob - Timbrature Locators.

Specific selectors for the Timbrature bot.
"""

from selenium.webdriver.common.by import By


class TimbratureLocators:
    """Locators for the Timbrature page and elements.

    Definisce i puntatori agli elementi dell'interfaccia Report Timbrature.
    """

    # Navigation
    REPORT_MENU = (By.XPATH, "//*[normalize-space(text())='Report']")
    """Pulsante menu Report nell'header."""

    TIMBRATURE_SUBMENU = (
        By.XPATH,
        "//span[contains(@class, 'x-btn-inner-navigation-small') and normalize-space(text())='Timbrature']",
    )
    """Voce di sottomenu per accedere alle Timbrature."""

    HOME_SEARCH_INPUT = (
        By.XPATH,
        "//input[@id='home_menu_combo-inputEl' or @name='home_menu_combo-inputEl' or contains(@class, 'x-form-text-home-search-combo')]",
    )
    """Campo di ricerca globale del menu home per navigazione ultra-veloce."""

    SUPPLIER_INPUT = (
        By.XPATH,
        "//input[@name='CodiceFornitore' or @name='Fornitore' or @name='FornitoreSap']",
    )
    """Campo input del fornitore (supporta nomi multipli ExtJS)."""

    # Generic combo box arrow for ExtJS
    COMBO_ARROW_GENERIC = (By.XPATH, "//div[contains(@class, 'x-form-arrow-trigger')]")
    """Freccia generica per l'apertura delle combo box ExtJS."""

    # Specific ID pattern for Supplier combo
    COMBO_ARROW_SUPPLIER = (
        By.XPATH,
        "//input[@name='CodiceFornitore' or @name='Fornitore' or @name='FornitoreSap']/ancestor::div[contains(@class, 'x-form-trigger-wrap') or contains(@class, 'x-form-item-body')]//div[contains(@class, 'x-form-arrow-trigger')]",
    )
    """Freccia specifica per la combo box di selezione del fornitore, legata all'input e indipendente dagli ID dinamici."""

    FILTER_DATA_DA = (By.NAME, "DataDa")
    """Campo input per la data di inizio ricerca."""

    FILTER_DATA_A = (By.NAME, "DataA")
    """Campo input per la data di fine ricerca."""

    # Grid
    GRID_ROWS = (By.XPATH, "//tr[contains(@class, 'x-grid-row')]")
    """Righe della griglia dei risultati."""

    # Download Buttons (Multiple strategies)
    DOWNLOAD_BTN_TEXT = (By.XPATH, "//*[contains(text(), 'Esporta')]")
    """Pulsante di export identificato tramite testo (Esporta)."""

    DOWNLOAD_BTN_ICON = (
        By.XPATH,
        "//div[contains(@class, 'x-tool')][.//div[contains(@class, 'x-tool-tool-el') and contains(text(), '')]]",
    )
    """Pulsante di export identificato tramite l'icona unicode specifica di Excel (FontAwesome)."""

    DOWNLOAD_BTN_ARIA = (
        By.XPATH,
        "//*[(contains(@title, 'Excel') or contains(@aria-label, 'Excel') or contains(@data-qtip, 'Excel')) or (contains(@title, 'Esporta') or contains(@aria-label, 'Esporta') or contains(@data-qtip, 'Esporta'))]",
    )
    """Pulsante di export identificato tramite attributi ARIA o titoli Excel."""
