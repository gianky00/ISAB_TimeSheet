"""
SyncroJob - SafeWork Common Locators
Centralizzazione dei selettori Selenium per il portale SafeWork.
"""

from selenium.webdriver.common.by import By


class SafeWorkLocators:
    """Locatori condivisi tra i bot SafeWork."""

    # Login
    SITO_BUTTON = (By.XPATH, "//button[@class='ms-choice']")
    ISAB_SUD_OPTION = (By.XPATH, "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']")
    USERNAME_FIELD = (By.ID, "inpUtente")
    PASSWORD_FIELD = (By.ID, "inpPassword")
    LOGIN_BUTTON = (By.ID, "btnLogin")
    CARICAMENTO_SPAN = (By.XPATH, "//span[contains(text(), 'Caricamento...')]")
    OVERLAY = (By.ID, "GISWaitOverlay")

    # Navigazione
    HOME_BUTTON = (By.ID, "topIcon-actHomePage")
    VISUALIZZA_ATTIVITA_BUTTON = (By.ID, "sideBar-actVisualizzaAttivita")
    RICERCA_PDL_BUTTON = (By.ID, "sideBar-actRicercaPdL")

    # Filtri Visualizza Attività
    NUM_PERMESSO_FIELD = (By.ID, "fldNumPermesso")
    # Filtri Ricerca
    ESCLUDI_CHIUSI_CHECKBOX = (By.ID, "fldEscludiChiusi")

    DITTA_BUTTON = (By.XPATH, "//select[@id='fldIdDitta']/following-sibling::div/button")
    RICHIEDENTE_BUTTON = (By.XPATH, "//select[@id='fldIdRichiedente']/following-sibling::div/button")
    DROPDOWN_OPEN = (By.XPATH, "//div[contains(@class,'ms-drop') and contains(@style,'display: block')]")
    SEARCH_INPUT_IN_DROPDOWN = (By.XPATH, ".//input[@type='text']")
    SEARCH_START_BUTTON = (By.ID, "btnAvviaRicerca")
    EXPORT_BUTTON = (By.ID, "btnEsporta")

    # Tabella Risultati
    ROWS = (By.XPATH, ".//tbody/tr")
