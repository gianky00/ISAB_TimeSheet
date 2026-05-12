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
    RICERCA_VELOCE_PDL = (By.ID, "fldRicercaPdLVeloce")

    # Ricerca PdL Veloce
    PRINT_PREVIEW_MENU = (By.ID, "topIcon-acticonAnteprimaStampaMenu")
    EXTEND_SEARCH_YES = (By.XPATH, "//span[@idtxt='E421C594']")
    DOWNLOAD_ITALIANO = (By.ID, "appItaliano")

    # Parte Seconda
    LABEL_PA_FOGLIO = (By.ID, "lblPAFoglio")
    TITLE_PARTE_SECONDA = (By.ID, "lblTitoloParteSeconda")
    PRINT_PS_BUTTON = (By.ID, "btnPrintPS")
    RADIO_PRINT_ALL = (By.ID, "rbStampaTutte")
    PREVIEW_BUTTON = (By.ID, "btnAnteprima")

    # Filtri Visualizza Attività
    NUM_PERMESSO_FIELD = (By.ID, "fldNumPermesso")
    DATE_FROM_PROG = (By.ID, "programmazioneDal")  # Aggiunto
    DATE_TO_PROG = (By.ID, "programmazioneAl")  # Aggiunto

    # Filtri Ricerca
    ESCLUDI_CHIUSI_CHECKBOX = (By.ID, "fldEscludiChiusi")
    DITTA_BUTTON = (By.XPATH, "//select[@id='fldIdDitta']/following-sibling::div/button")
    RICHIEDENTE_BUTTON = (By.XPATH, "//select[@id='fldIdRichiedente']/following-sibling::div/button")
    DROPDOWN_OPEN = (By.XPATH, "//div[contains(@class,'ms-drop') and contains(@style,'display: block')]")
    SEARCH_INPUT_IN_DROPDOWN = (By.XPATH, ".//input[@type='text']")

    SEARCH_START_BUTTON = (By.ID, "btnAvviaRicerca")
    SEARCH_GENERIC_BUTTON = (By.ID, "btnCerca")
    EXPORT_BUTTON = (By.ID, "btnEsporta")

    # Tabella Risultati
    ROWS = (By.XPATH, ".//tbody/tr")
