from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.base_bot import BaseBot, StepStatus
from src.core.constants import BotStatus


class DummyBot(BaseBot):
    """Implementazione minima per testare la classe base."""

    @property
    def name(self):
        return "Dummy Bot"

    @property
    def description(self):
        return "Test bot"

    @staticmethod
    def get_columns():
        return []

    from typing import ClassVar

    STEPS: ClassVar[list[tuple[str, str]]] = [("step1", "Step 1"), ("step2", "Step 2")]

    def _init_driver(self):
        pass

    def cleanup(self):
        pass

    def _save_error_state(self, error_msg: str):
        pass

    def _login(self):
        return True

    def run(self, data):
        self.update_step("step2", StepStatus.RUNNING)
        return True


class TestBaseBot:
    @pytest.fixture
    def bot(self):
        return DummyBot("user", "pass")

    def test_initialize_steps(self, bot):
        bot.step_manager.reset()
        assert len(bot.step_manager.steps) == 2
        # Accediamo a _states per verifica interna del reset
        assert bot.step_manager._states[0] == StepStatus.PENDING

    @patch("src.bots.base.execution_guard.ExecutionGuard.check_environment", return_value=(True, ""))
    def test_execute_workflow_success(self, mock_guard, bot):
        """Verifica il flusso completo di esecuzione: login -> run -> cleanup."""
        # Mocking internal methods
        bot._safe_login_with_retry = MagicMock(return_value=True)
        bot.cleanup = MagicMock()

        result = bot.execute([{"data": "test"}])

        assert result is True
        assert bot.status == BotStatus.COMPLETED
        bot._safe_login_with_retry.assert_called_once()
        bot.cleanup.assert_called_once()
        mock_guard.assert_called_once()

    def test_validate_data_empty(self, bot):
        success, msg = bot.validate_data([])
        assert success is False
        assert "Nessun dato" in msg

    def test_request_stop_logic(self, bot):
        """Verifica che la richiesta di stop alzi l'eccezione corretta."""
        bot.request_stop()
        assert bot._stop_requested is True

        with pytest.raises(InterruptedError):
            bot._check_stop()
