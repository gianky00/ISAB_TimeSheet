from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus


class ConcreteBot(BaseBot):
    @property
    def name(self):
        return "TestBot"

    @property
    def description(self):
        return "Test Description"

    def run(self, data):
        self._check_stop()
        return True

    @staticmethod
    def get_columns():
        return []

    def _handle_unsaved_changes_popup(self):
        pass


@pytest.fixture
def mock_bot_deps():
    with (
        patch("src.bots.base.base_bot.webdriver") as mock_webdriver,
        patch("src.bots.base.base_bot.ChromeDriverManager") as mock_cdm,
        patch("src.bots.base.base_bot.config_manager") as mock_config,
        patch("src.bots.base.base_bot.LoginPage") as mock_login_page,
    ):
        mock_config.load_config.return_value = {}
        yield {
            "webdriver": mock_webdriver,
            "cdm": mock_cdm,
            "config": mock_config,
            "login_page": mock_login_page,
        }


class TestBaseBot:
    def test_initialization(self):
        bot = ConcreteBot("user", "pass")
        assert bot.username == "user"
        assert bot.password == "pass"
        assert bot.status == BotStatus.IDLE

    def test_status_logging(self):
        bot = ConcreteBot("u", "p")
        log_mock = MagicMock()
        bot.set_log_callback(log_mock)

        # RUNNING should NOT log anymore to reduce noise
        bot.status = BotStatus.RUNNING
        assert bot.status == BotStatus.RUNNING
        log_mock.assert_not_called()

        # Final states SHOULD log
        bot.status = BotStatus.COMPLETED
        log_mock.assert_called_with("🏁 Stato finale: COMPLETED")

    def test_log_telegram(self):
        bot = ConcreteBot("u", "p")
        tg_mock = MagicMock()
        bot.set_telegram_service(tg_mock)

        bot.log("Hello Telegram")
        tg_mock.send_message_sync.assert_called()
        # Verify cleaning logic (re.sub)
        args, _ = tg_mock.send_message_sync.call_args
        assert "Hello Telegram" in args[0]

    def test_request_stop(self):
        bot = ConcreteBot("u", "p")
        bot.request_stop()
        assert bot._stop_requested is True

        with pytest.raises(InterruptedError):
            bot._check_stop()

    def test_validate_data_base(self):
        bot = ConcreteBot("u", "p")
        valid, msg = bot.validate_data([])
        assert valid is False
        assert "Nessun dato" in msg

        bot.username = ""
        valid, msg = bot.validate_data([{"d": 1}])
        assert valid is False
        assert "Credenziali" in msg

    @patch.object(ConcreteBot, "_safe_login_with_retry", return_value=True)
    def test_execute_workflow_success(self, mock_login):
        bot = ConcreteBot("u", "p")
        result = bot.execute([{"data": 1}])

        assert result is True
        assert bot.status == BotStatus.COMPLETED
        mock_login.assert_called_once()

    @patch.object(ConcreteBot, "_safe_login_with_retry", return_value=False)
    def test_execute_workflow_login_fail(self, mock_login):
        bot = ConcreteBot("u", "p")
        result = bot.execute([{"data": 1}])

        assert result is False
        assert bot.status == BotStatus.ERROR

    @patch.object(ConcreteBot, "_safe_login_with_retry", return_value=True)
    def test_execute_workflow_run_fail(self, mock_login):
        bot = ConcreteBot("u", "p")
        with patch.object(bot, "run", return_value=False):
            result = bot.execute([{"data": 1}])
            assert result is False
            assert bot.status == BotStatus.ERROR

    def test_safe_login_retry_logic(self, mock_bot_deps):
        bot = ConcreteBot("u", "p")

        # Mock _init_driver and _login
        with (
            patch.object(bot, "_init_driver") as mock_init,
            patch.object(bot, "_login") as mock_login,
        ):
            # Fail first, succeed second
            mock_login.side_effect = [False, True]

            result = bot._safe_login_with_retry(max_retries=2)

            assert result is True
            assert mock_init.call_count == 2
            assert mock_login.call_count == 2

    def test_save_error_state(self, mock_bot_deps):
        bot = ConcreteBot("u", "p")
        mock_driver = MagicMock()
        mock_driver.page_source = "<html></html>"
        bot.driver = mock_driver

        with (
            patch("pathlib.Path.mkdir"),
            patch("pathlib.Path.write_text"),
            patch("datetime.datetime") as mock_dt,
        ):
            mock_dt.now.return_value.strftime.return_value = "timestamp"
            bot._save_error_state("some error")

            mock_driver.save_screenshot.assert_called()
