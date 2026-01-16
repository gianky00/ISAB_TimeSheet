"""
Selettori per il bot Prenota BP (Portale Fornitori ISAB).
Estratti tramite Universal Inspector.
"""

from selenium.webdriver.common.by import By


class PrenotaBPLocators:
    """Locatori Selenium per la gestione delle prenotazioni Buono di Prelievo."""

    # Login
    USERNAME_FIELD = (By.NAME, "Username")
    PASSWORD_FIELD = (By.NAME, "Password")
    LOGIN_BUTTON = (By.XPATH, "//a[.//span[text()='Accedi']] | //span[text()='Accedi']")
    BT_SI_SESSIONE_ATTIVA = (
        By.XPATH,
        "//span[normalize-space(text())='Si' or normalize-space(text())='Sì']/ancestor::a",
    )
    USER_INFO_PANEL = (By.ID, "user-info-panel")

    # Menu Principale (Buono di Prelievo)
    MENU_BUONO_PRELIEVO = (
        By.XPATH,
        "//div[contains(@class, 'x-title-text')][text()='Buono di Prelievo']",
    )

    # Sotto Menu (Gestione Buono di Prelievo)
    SUBMENU_GESTIONE_BP = (
        By.XPATH,
        "//span[contains(@class, 'x-btn-inner')][text()='Gestione Buono di Prelievo']",
    )

    # Pannello Gestione BP (Griglia e Filtri)
    FILTER_FORNITORE = (By.NAME, "Fornitore")
    FILTER_FORNITORE_ARROW = (
        By.XPATH,
        "//div[contains(@id, 'generic_refresh_combo_box') and contains(@id, 'trigger-picker')]",
    )
    FILTER_NUMERO_BP = (By.NAME, "IdBuonoDiPrelievo")

    FILTER_DATA_DA = (By.NAME, "DataBPDa")
    FILTER_DATA_A = (By.NAME, "DataBPA")
    BT_CERCA = (By.XPATH, "//a[contains(@class, 'x-btn')][.//span[text()='Cerca']]")
    BT_NUOVO = (
        By.XPATH,
        "//a[contains(@class, 'x-btn')][.//span[contains(normalize-space(text()), 'Nuovo')]]",
    )

    # Form Nuova Prenotazione
    # Cerchiamo varianti comuni per i nomi dei campi nel DOM ExtJS
    CAMPO_NUMERO_BP = (
        By.XPATH,
        "//input[@name='NumeroBP' or @name='Numero' or @name='BPNumber' or contains(@name, 'Numero')]",
    )
    CAMPO_NOTE = (
        By.XPATH,
        "//textarea[@name='NoteRitiro' or @name='Note' or @name='Notes' or contains(@name, 'Note')] | //input[@name='Note']",
    )
    BT_SALVA = (By.XPATH, "//span[text()='Salva' or text()='Conferma']/ancestor::a")
    BT_CHIUDI_POPUP = (By.XPATH, "//div[contains(@class, 'x-tool-close')]")

    # Dettagli BP
    ICON_DETTAGLI = (
        By.XPATH,
        "//div[contains(@class, 'x-action-col-icon') and contains(@class, 'fa-info-circle')]",
    )
    # Finestra Dettagli
    WINDOW_DETTAGLI = (
        By.XPATH,
        "//div[contains(@class, 'x-window') and .//div[contains(text(), 'Buono Di Prelievo')]]",
    )
    GRID_ROWS_DETTAGLI = (
        By.XPATH,
        "//div[contains(@class, 'x-window') and .//div[contains(text(), 'Buono Di Prelievo')]]//tr[contains(@class, 'x-grid-row')]",
    )
    # Cella "Materiale Disponibile" (Ultima colonna)
    CELL_MATERIALE_DISPONIBILE = (
        By.XPATH,
        ".//td[contains(@class, 'x-grid-cell-last')]//span[contains(@class, 'fa-check') and contains(@style, 'LightGreen')]",
    )
