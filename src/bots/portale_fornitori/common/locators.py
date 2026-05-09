"""
Bot TS - Common Locators
Shared selectors for login and common UI elements.
"""

from selenium.webdriver.common.by import By


class LoginLocators:
    """Locators for the Login page."""

    USERNAME_FIELD = (By.NAME, "Username")
    PASSWORD_FIELD = (By.NAME, "Password")
    COMPANY_FIELD = (By.NAME, "Company")
    LOGIN_BUTTON = (
        By.XPATH,
        "//span[text()='Accedì and contains(@class, 'x-btn-inner')]",
    )
    LOGIN_BUTTON_FALLBACK = (
        By.XPATH,
        "//span[text()='Accedì and contains(@class, 'x-btn-inner')]",
    )


class CommonLocators:
    """Locators for common UI elements (popups, overlays, menus)."""

    # Overlays
    LOADING_MASK = (
        By.XPATH,
        "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]",
    )
    LOADING_TEXT = (By.XPATH, "//div[text()='Caricamento...']")

    # Popups
    POPUP_SESSION_YES = (
        By.XPATH,
        "//span[normalize-space(text())='Sì and contains(@class, 'x-btn-inner')]",
    )

    # Logout
    SETTINGS_BUTTON = (
        By.XPATH,
        "//span[contains(@id, 'user-info-settings-btnEl') or contains(@class, 'x-btn-icon-el-default-toolbar-small-settings')]",
    )
    LOGOUT_OPTION = (
        By.XPATH,
        "//a[contains(@class, 'x-menu-item-link')][.//span[normalize-space(text())='Esci']]",
    )
