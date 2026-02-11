from unittest.mock import MagicMock, patch

from src.bots.base.base_bot import BaseBot
from src.bots.base.login_page import LoginPage
from src.bots.portale_fornitori.common.locators import LoginLocators


class ConcreteBot(BaseBot):
    """Sottoclasse concreta per testare BaseBot."""

    def __init__(self, username="user", password=None, **kwargs):
        super().__init__(username=username, password=password or "*", **kwargs)

    @property
    def name(self):
        return "TestBot"

    @property
    def description(self):
        return "Desc"

    def run(self, data):
        return True

    @staticmethod
    def get_columns():
        return []

    def _handle_unsaved_changes_popup(self):
        pass


class TestBotBasePages:
    def test_login_page_logic(self):
        mock_driver = MagicMock()
        mock_wait = MagicMock()
        page = LoginPage(mock_driver, wait=mock_wait)

        # Test locators from LoginLocators
        assert LoginLocators.USERNAME_FIELD is not None

        # Test login method (logic only)
        with patch.object(page, "_perform_login_form_action") as mock_form:
            # Mock driver.get and overlays
            with patch.object(page, "_attendi_scomparsa_overlay", return_value=True):
                page.login("user", "pass")
                mock_form.assert_called_with("user", "pass")

    @patch("src.bots.base.base_bot.webdriver.Chrome")
    @patch("src.bots.base.base_bot.ChromeDriverManager")
    def test_base_bot_lifecycle(self, mock_dm, mock_chrome):
        bot = ConcreteBot(username="test_user", password="test_password")

        # BaseBot doesn't have start(), it has execute()
        with (
            patch.object(bot, "_safe_login_with_retry", return_value=True),
            patch.object(bot, "cleanup"),
        ):
            result = bot.execute([{"data": 1}])
            assert result is True
            assert bot.status.name == "COMPLETED"

        bot.cleanup()
        assert bot.driver is None
