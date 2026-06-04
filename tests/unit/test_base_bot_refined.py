from unittest.mock import MagicMock

import pytest

from src.infrastructure.bots.base.base_bot import BaseBot


class ConcreteDummyBot(BaseBot):
    @property
    def name(self):
        return "Dummy"

    @property
    def description(self):
        return "Desc"

    def run(self, data):
        return True

    @staticmethod
    def get_columns():
        return []

    def _init_driver(self):
        pass

    def cleanup(self):
        pass

    def _save_error_state(self, error_msg: str):
        pass

    def _login(self) -> bool:
        return True

    def _handle_unsaved_changes_popup(self):
        pass


class TestBaseBotRefined:
    def test_request_stop_logic(self):
        bot = ConcreteDummyBot("u", "p")
        bot.request_stop()
        assert bot._stop_requested is True
        with pytest.raises(InterruptedError):
            bot._check_stop()

    def test_execute_validation_failure(self):
        bot = ConcreteDummyBot("u", "p")
        # Fail validation by passing empty data
        result = bot.execute([])
        assert result is False
        assert bot.status.name == "ERROR"

    def test_log_and_telegram_integration(self):
        bot = ConcreteDummyBot("u", "p")
        mock_tg = MagicMock()
        bot.set_telegram_service(mock_tg)

        bot.log("Test Log")
        mock_tg.send_message_sync.assert_called()
