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
    DATA_DAL = (By.ID, "programmazioneDal")
    DATA_AL = (By.ID, "programmazioneAl")
    NUM_PERMESSO_FIELD = (By.ID, "fldNumPermesso")
    # Selettore robusto per il filtro Sito/Impianto basato sulla label adiacente
    # Cerca una label che contiene "Sito" o "Impianto" o "Reparto" e prende il bottone dropdown successivo
    # Filtri Ricerca
    ESCLUDI_CHIUSI_CHECKBOX = (By.ID, "fldEscludiChiusi")
    
    # Selettore "Main Style" per il dropdown sito (più semplice e diretto)
    SITO_DROPDOWN_SPAN = (By.XPATH, "//span[contains(text(), 'ISAB Sud') or contains(text(), 'ISAB Nord') or contains(text(), 'IGCC') or contains(text(), 'Sito')]")
    
    # Vecchio selettore mantenuto per compatibilità/fallback ma deprecato
    SITO_FILTER_BUTTON = (By.XPATH, "//label[contains(text(), 'Sito') or contains(text(), 'Impianto') or contains(text(), 'Reparto')]/following::div[contains(@class, 'ms-parent')][1]//button")
    DITTA_BUTTON = (By.XPATH, "//select[@id='fldIdDitta']/following-sibling::div/button")
    RICHIEDENTE_BUTTON = (By.XPATH, "//select[@id='fldIdRichiedente']/following-sibling::div/button")
    DROPDOWN_OPEN = (By.XPATH, "//div[contains(@class,'ms-drop') and contains(@style,'display: block')]")
    SEARCH_INPUT_IN_DROPDOWN = (By.XPATH, ".//input[@type='text']")
    SEARCH_START_BUTTON = (By.ID, "btnAvviaRicerca")
    EXPORT_BUTTON = (By.ID, "btnEsporta")

    # Tabella Risultati
    RESULTS_TABLE = (By.XPATH, "//table[contains(@class, 'table')]")
    ROWS = (By.XPATH, ".//tbody/tr")
    CELLS = (By.TAG_NAME, "td")
    NO_DATA_MSG = (By.XPATH, "//td[contains(text(), 'Nessun dato')]")

    # Popup
    MODAL_DIALOG = (By.XPATH, "//div[contains(@class, 'modal') and contains(@style, 'display: block')]")
    MODAL_OK_BUTTON = (By.XPATH, ".//button[contains(text(), 'OK') or @data-dismiss='modal']")
