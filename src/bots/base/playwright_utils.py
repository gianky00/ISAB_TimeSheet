"""
SyncroJob - Playwright Utilities
Funzioni di utilità condivise per i bot Playwright.
"""

from selenium.webdriver.common.by import By


def get_playwright_selector(locator: tuple[str, str]) -> str:
    """
    Converte un locatore Selenium (By, value) in un selettore Playwright CSS/XPath valido.

    Esempio:
      - (By.NAME, "NumeroOda") -> '[name="NumeroOda"]'
      - (By.XPATH, "//div")   -> 'xpath=//div'
      - (By.ID, "campo_id")   -> '#campo_id'
    """
    by, value = locator
    result = value

    # Se è già un selettore Playwright (con prefisso)
    if value.startswith(("xpath=", "id=", "css=", "text=")):
        return value

    if by == By.XPATH:
        result = f"xpath={value}"
    elif by == By.NAME:
        result = f'[name="{value}"]'
    elif by == By.ID:
        result = f"#{value}"
    elif by == By.CLASS_NAME:
        # Gestisce classi multiple separate da spazio
        result = f".{value.replace(' ', '.')}"
    elif by == By.CSS_SELECTOR:
        result = value
    elif value.startswith(("//", "(")):
        # Fallback: se inizia con // o ( assume XPATH
        result = f"xpath={value}"

    return result
