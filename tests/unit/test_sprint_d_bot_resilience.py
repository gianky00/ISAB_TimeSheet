from unittest.mock import patch

import pytest

from src.infrastructure.bots.base import BotStatus
from src.infrastructure.bots.base.base_bot import BaseBot


class DummyBot(BaseBot):
    @property
    def name(self) -> str:
        return "DummyBot"

    @property
    def description(self) -> str:
        return "Desc"

    @staticmethod
    def get_columns() -> list:
        return []

    def _init_driver(self):
        pass

    def cleanup(self):
        pass

    def _save_error_state(self, e):
        pass

    def _login(self):
        return True

    def run(self, data):
        return True


@pytest.fixture
def bot():
    return DummyBot("user", "pass")


class TestSprintDBotResilience:
    @patch("src.infrastructure.bots.base.execution_guard.ExecutionGuard.check_environment", return_value=(True, ""))
    def test_bot_retry_logic_on_login_failure(self, mock_env, bot, mocker):
        """Verifica che il bot tenti il login più volte in caso di errore."""
        m_init = mocker.patch.object(bot, "_init_driver")
        m_login = mocker.patch.object(bot, "_login", return_value=False)
        m_cleanup = mocker.patch.object(bot, "cleanup")

        res = bot.execute([{"data": 1}])

        assert res is False
        assert m_login.call_count == 2
        # V9.4: calls cleanup 2 times during retries + 1 time in finally block
        assert m_cleanup.call_count == 3

    @patch("src.infrastructure.bots.base.execution_guard.ExecutionGuard.check_environment", return_value=(True, ""))
    def test_bot_error_capture_screenshot(self, mock_env, bot, mocker):
        """Verifica che venga salvato lo stato in caso di eccezione."""
        mocker.patch.object(bot, "_safe_login_with_retry", return_value=True)
        mocker.patch.object(bot, "run", side_effect=Exception("Critical Fail"))
        m_save = mocker.patch.object(bot, "_save_error_state")

        bot.execute([{"data": 1}])

        assert m_save.called
        assert bot.status == BotStatus.ERROR

    @patch("src.infrastructure.bots.base.execution_guard.ExecutionGuard.check_environment", return_value=(True, ""))
    def test_bot_user_interruption(self, mock_env, bot, mocker):
        """Verifica che la richiesta di stop interrompa il flusso."""
        bot.request_stop()

        with pytest.raises(InterruptedError):
            bot._check_stop()

        # Test nel workflow execute
        mocker.patch.object(bot, "_safe_login_with_retry", return_value=True)
        mocker.patch.object(bot, "run", side_effect=InterruptedError())

        success = bot.execute([{"data": 1}])
        assert success is False
        assert bot.status == BotStatus.STOPPED

    @patch("src.infrastructure.bots.base.execution_guard.ExecutionGuard.check_environment", return_value=(True, ""))
    def test_bot_driver_initialization_failure_handling(self, mock_env, bot, mocker):
        """Verifica gestione crash totale del driver all'avvio."""
        mocker.patch.object(bot, "_init_driver", side_effect=Exception("Driver binary not found"))

        res = bot.execute([{"data": 1}])
        assert res is False
        assert bot.status == BotStatus.ERROR
