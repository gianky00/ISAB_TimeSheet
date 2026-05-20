from unittest.mock import MagicMock, patch

from selenium.webdriver.common.by import By

from src.bots.base.playwright_base_bot import PlaywrightBaseBot
from src.bots.base.playwright_utils import get_playwright_selector
from src.bots.base.selenium_bot_config import SeleniumBotConfig


class ConcretePlaywrightBot(PlaywrightBaseBot):
    @property
    def name(self):
        return "Test PW Bot"

    @property
    def description(self):
        return "Desc"

    @staticmethod
    def get_columns():
        return []

    def run(self, data):
        return True


def test_get_playwright_selector():
    """Verifica la conversione dei locatori Selenium in selettori Playwright."""
    assert get_playwright_selector((By.ID, "my-id")) == "#my-id"
    assert get_playwright_selector((By.NAME, "my-name")) == '[name="my-name"]'
    assert get_playwright_selector((By.XPATH, "//div")) == "xpath=//div"
    assert get_playwright_selector((By.CSS_SELECTOR, ".class")) == ".class"
    # Fallback auto-detection (priorità su By.ID se il valore è palesemente XPATH)
    assert get_playwright_selector((By.ID, "//span")) == "xpath=//span"
    assert get_playwright_selector((By.ID, "(//div)[1]")) == "xpath=(//div)[1]"


@patch("src.bots.base.playwright_base_bot.sync_playwright")
@patch("src.utils.helpers.cleanup_bot_processes")
def test_playwright_base_bot_init(mock_cleanup, mock_sync):
    """Verifica l'inizializzazione del driver Playwright."""
    config = SeleniumBotConfig(username="user", password="pass", headless=True)
    bot = ConcretePlaywrightBot(config)

    # Setup mock chain
    mock_pw_context = MagicMock()
    mock_pw_context.start.return_value = mock_pw_context
    mock_sync.return_value = mock_pw_context

    mock_browser = MagicMock()
    mock_pw_context.chromium.launch_persistent_context.return_value = mock_browser

    mock_page = MagicMock()
    mock_browser.pages = [mock_page]

    bot._init_driver()

    assert bot.playwright is not None
    assert bot.context is not None
    assert bot.page is not None
    mock_pw_context.chromium.launch_persistent_context.assert_called_once()


def test_playwright_base_bot_cleanup():
    """Verifica la chiusura corretta delle risorse."""
    config = SeleniumBotConfig(username="user", password="pass")
    bot = ConcretePlaywrightBot(config)
    mock_context = MagicMock()
    mock_pw = MagicMock()

    bot.context = mock_context
    bot.playwright = mock_pw
    bot.page = MagicMock()

    bot.cleanup()

    mock_context.close.assert_called_once()
    mock_pw.stop.assert_called_once()
    assert bot.page is None
    assert bot.context is None
    assert bot.playwright is None
