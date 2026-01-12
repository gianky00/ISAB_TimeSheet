from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.base_bot import BaseBot, BotStatus


class ConcreteBot(BaseBot):
    @property
    def name(self):
        return "TestBot"

    @property
    def description(self):
        return "Desc"

    def run(self, data):
        return True

    def _handle_unsaved_changes_popup(self):
        pass


class TestBaseBot:

    @pytest.fixture
    def bot(self):
        # Mock chrome driver manager e webdriver per evitare avvio reale del browser
        with patch("src.bots.base.base_bot.ChromeDriverManager"), patch("src.bots.base.base_bot.webdriver"):
            bot = ConcreteBot("user", "pass")
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot.popup_wait = MagicMock()
            bot.log = MagicMock()
            bot._stop_requested = False
            return bot

    @pytest.fixture(autouse=True)
    def mock_delays(self):
        # Patch automatico per tutti i test di questa classe
        with patch("src.bots.base.base_bot.time.sleep"), patch(
            "src.bots.base.base_bot.WebDriverWait"
        ):  # Mock WebDriverWait costruttore
            yield

    def test_init(self, bot):
        assert bot.username == "user"
        assert bot.password == "pass"
        assert bot.status == BotStatus.IDLE

    def test_login_flow_success(self, bot):
        # Mock driver attributes
        bot.driver.title = "ISAB Portal"
        bot.driver.page_source = "<html></html>"
        bot.driver.current_url = "http://portal/home"

        # Mock waits
        # WebDriverWait(driver, timeout).until(...) -> returns element
        bot.wait.until.return_value = MagicMock()

        # Mock LoginPage
        bot.login_page = MagicMock()
        bot.login_page.login.return_value = True

        # Mock internal helpers per evitare logica complessa
        with patch.object(bot, "_attendi_scomparsa_overlay", return_value=True), patch.object(
            bot, "_verify_logged_in_via_ui", return_value=False
        ), patch.object(bot, "_handle_session_popup"), patch.object(bot, "_handle_ok_popup"):

            result = bot._login()

            assert result is True
            bot.login_page.login.assert_called_with("user", "pass")

    def test_login_proxy_error(self, bot):
        bot.driver.title = "Proxy Error"
        bot.driver.page_source = "Proxy Error"

        bot.login_page = MagicMock()
        bot.login_page.login.return_value = False  # Simula fallimento login

        result = bot._login()
        assert result is False

    def test_logout(self, bot):
        bot.driver.current_url = "login.aspx"

        with patch.object(bot, "_handle_unsaved_changes_popup"):
            # Configura wait.until per ritornare un elemento cliccabile
            mock_el = MagicMock()
            bot.wait.until.return_value = mock_el

            result = bot._logout()

            assert result is True
            assert mock_el.click.called

    def test_navigate_menu(self, bot):
        bot.wait.until.return_value = MagicMock()

        with patch.object(bot, "_attendi_scomparsa_overlay"):
            result = bot.navigate_to_menu(["Menu1", "SubMenu2"])
            assert result is True
