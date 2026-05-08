from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.selenium_base_bot import SeleniumBaseBot
from src.core.constants import BotStatus, Timeouts


# Classe concreta per testare SeleniumBaseBot
class ConcreteBot(SeleniumBaseBot):
    @property
    def name(self) -> str:
        return "TestBot"

    @property
    def description(self) -> str:
        return "A bot for testing SeleniumBaseBot"

    @staticmethod
    def get_columns():
        return []

    def _login(self) -> bool:
        """Mock login."""
        return True

    def run(self, data):
        return True


class TestBaseBotRobust:
    @pytest.fixture
    def mock_driver_cls(self):
        with patch("src.bots.base.selenium_base_bot.webdriver.Chrome") as mock:
            yield mock

    @pytest.fixture
    def mock_service(self):
        with patch("src.bots.base.selenium_base_bot.Service") as mock:
            yield mock

    @pytest.fixture
    def mock_options(self):
        with patch("src.bots.base.selenium_base_bot.Options") as mock:
            yield mock

    @pytest.fixture
    def mock_chrome_manager(self):
        with (
            patch("webdriver_manager.chrome.ChromeDriverManager") as mock,
            patch("src.bots.base.selenium_base_bot.Path.exists", return_value=False),
        ):
            mock.return_value.install.return_value = "/path/to/chromedriver.exe"
            yield mock

    @pytest.fixture
    def bot(self):
        return ConcreteBot("user", "pass")

    # --- Init Tests ---

    def test_init_defaults(self, bot):
        """Test inizializzazione default."""
        assert bot.username == "user"
        assert bot.password == "pass"
        assert bot.headless is False
        assert bot.timeout == Timeouts.DEFAULT
        assert bot.status == BotStatus.IDLE
        assert bot._stop_requested is False

    # --- Driver Init Tests ---

    def test_init_driver_success(self, bot, mock_driver_cls, mock_service, mock_chrome_manager, mock_options):
        """Test inizializzazione driver con successo."""
        # Mock chromedriver path
        mock_chrome_manager.return_value.install.return_value = "C:/drivers/chromedriver.exe"

        # Call
        bot._init_driver()

        # Assertions
        mock_chrome_manager.return_value.install.assert_called_once()
        mock_service.assert_called_with("C:/drivers/chromedriver.exe")
        mock_driver_cls.assert_called_once()

        # Check options
        mock_opts_instance = mock_options.return_value
        assert mock_opts_instance.add_argument.call_count > 0

        # Verifica anti-detection script
        bot.driver.execute_cdp_cmd.assert_called_with(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )
        assert bot.status == BotStatus.INITIALIZING

    def test_get_chrome_options_headless(self, bot, mock_options):
        """Test _get_chrome_options logica headless."""
        bot.headless = True
        with patch("src.core.config_manager.load_config", return_value={}):
            bot._get_chrome_options()
            # Verifica che headless sia stato aggiunto
            mock_options.return_value.add_argument.assert_any_call("--headless=new")

    def test_driver_error_handling(self, bot, mock_chrome_manager):
        """Test gestione errore init driver."""
        mock_chrome_manager.return_value.install.side_effect = Exception("Download failed")

        with pytest.raises(RuntimeError, match="DriverUnavailable"):
            bot._init_driver()

    # --- Execution Flow Tests ---

    @patch("src.bots.base.execution_guard.ExecutionGuard.check_environment", return_value=(True, ""))
    @patch("src.bots.base.selenium_base_bot.LoginPage")
    def test_execute_success(self, mock_login_page_cls, mock_guard, bot):
        """Test flusso execute completo con successo."""
        # Setup mocks
        bot._init_driver = MagicMock()
        bot._login = MagicMock(return_value=True)
        bot.cleanup = MagicMock()
        bot.run = MagicMock(return_value=True)

        data = [{"id": 1}]

        # Execute
        res = bot.execute(data)

        assert res is True
        bot._init_driver.assert_called_once()
        bot._login.assert_called_once()
        bot.run.assert_called_once_with(data)
        bot.cleanup.assert_called_once()
        assert bot.status == BotStatus.COMPLETED

    # --- Cleanup Tests ---

    def test_cleanup(self, bot):
        """Test cleanup chiude driver."""
        mock_driver = MagicMock()
        bot.driver = mock_driver

        bot.cleanup()

        mock_driver.quit.assert_called_once()
        assert bot.driver is None

    def test_cleanup_safe(self, bot):
        """Test cleanup non esplode se driver è None o quit fallisce."""
        bot.driver = None
        bot.cleanup()  # No error

        mock_driver = MagicMock()
        mock_driver.quit.side_effect = Exception("Error closing")
        bot.driver = mock_driver
        bot.cleanup()  # No error propagate
        assert bot.driver is None
