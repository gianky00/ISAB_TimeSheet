from unittest.mock import MagicMock, patch

import pytest

from src.core.constants import BotStatus


class TestBaseBot:
    @pytest.fixture
    def mock_bot(self):
        with patch("src.bots.base.base_bot.config_manager"):
            with patch("src.bots.base.base_bot.get_logger"):
                from src.bots.base.base_bot import BaseBot

                # Create concrete implementation for testing
                class TestBot(BaseBot):
                    @property
                    def name(self):
                        return "TestBot"

                    @property
                    def description(self):
                        return "Test bot for unit testing"

                    def run(self, data):
                        return True

                return TestBot("user", "pass", headless=True)

    def test_init_sets_credentials(self, mock_bot):
        assert mock_bot.username == "user"
        assert mock_bot.password == "pass"
        assert mock_bot.headless is True

    def test_init_default_status(self, mock_bot):
        assert mock_bot.status == BotStatus.IDLE

    def test_status_setter(self, mock_bot):
        mock_bot.status = BotStatus.RUNNING
        assert mock_bot.status == BotStatus.RUNNING

    def test_request_stop(self, mock_bot):
        assert mock_bot._stop_requested is False

        mock_bot.request_stop()

        assert mock_bot._stop_requested is True

    def test_check_stop_raises(self, mock_bot):
        mock_bot._stop_requested = True

        with pytest.raises(InterruptedError):
            mock_bot._check_stop()

    def test_check_stop_no_raise(self, mock_bot):
        mock_bot._stop_requested = False

        # Should not raise
        mock_bot._check_stop()

    def test_set_log_callback(self, mock_bot):
        callback = MagicMock()

        mock_bot.set_log_callback(callback)

        assert mock_bot._log_callback == callback

    def test_set_telegram_service(self, mock_bot):
        telegram = MagicMock()

        mock_bot.set_telegram_service(telegram)

        assert mock_bot._telegram_service == telegram

    def test_set_input_callback(self, mock_bot):
        callback = MagicMock()

        mock_bot.set_input_callback(callback)

        assert mock_bot._input_callback == callback

    def test_log_with_callback(self, mock_bot):
        callback = MagicMock()
        mock_bot.set_log_callback(callback)

        mock_bot.log("Test message")

        callback.assert_called()

    def test_name_property(self, mock_bot):
        assert mock_bot.name == "TestBot"

    def test_description_property(self, mock_bot):
        assert mock_bot.description == "Test bot for unit testing"

    def test_validate_data_empty(self, mock_bot):
        success, msg = mock_bot.validate_data([])
        assert success is False
        assert "Nessun dato" in msg

    def test_validate_data_no_credentials(self, mock_bot):
        mock_bot.username = ""
        success, msg = mock_bot.validate_data([{"test": "data"}])
        assert success is False
        assert "Credenziali" in msg

    def test_cleanup_without_driver(self, mock_bot):
        mock_bot.driver = None

        # Should not raise
        mock_bot.cleanup()
