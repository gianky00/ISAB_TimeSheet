"""
Bot TS - Common Locators
Shared selectors for login and common UI elements.
"""

from selenium.webdriver.common.by import By

class LoginLocators:
    """Locators for the Login page."""
    USERNAME_FIELD = (By.NAME, "Username")
    PASSWORD_FIELD = (By.NAME, "Password")
    LOGIN_BUTTON = (By.XPATH, "//span[text()='Accedi' and contains(@class, 'x-btn-inner')]")
    LOGIN_BUTTON_FALLBACK = (By.XPATH, "//span[text()='Accedi' and contains(@class, 'x-btn-inner')]")

class CommonLocators:
    """Locators for common UI elements (popups, overlays, menus)."""
    # Overlays
    LOADING_MASK = (By.XPATH, "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]")
    LOADING_TEXT = (By.XPATH, "//div[text()='Caricamento...']")

    # Popups
    POPUP_SESSION_YES = (By.XPATH, "//span[text()='Si' and contains(@class, 'x-btn-inner')]/ancestor::a[contains(@class, 'x-btn')]")
    POPUP_OK = (By.XPATH, "//span[text()='OK' and contains(@class, 'x-btn-inner')]")
    POPUP_ATTENTION_HEADER = (By.XPATH, "//span[contains(@class, 'x-window-header-text') and contains(text(), 'Attenzione')]")
    POPUP_YES_BUTTON = (By.XPATH, "//div[contains(@class, 'x-window')]//span[normalize-space(text())='Si' and contains(@class, 'x-btn-inner')]")

    # Logout
    SETTINGS_BUTTON = (By.XPATH, "//span[contains(@id, 'user-info-settings-btnEl') or contains(@class, 'x-btn-icon-el-default-toolbar-small-settings')]")
    LOGOUT_OPTION = (By.XPATH, "//a[contains(@class, 'x-menu-item-link')][.//span[normalize-space(text())='Esci']]")
