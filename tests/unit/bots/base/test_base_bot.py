from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus


class MockBot(BaseBot):
    @property
    def name(self) -> str:
        return "MockBot"

    @property
    def description(self) -> str:
        return "Bot di test"

    @staticmethod
    def get_columns() -> list:
        return []

    def _init_driver(self):
        pass

    def cleanup(self):
        pass

    def _save_error_state(self, error_msg):
        pass

    def _login(self) -> bool:
        return True

    def run(self, data) -> bool:
        return True


class TestBaseBot:
    def test_bot_initialization(self):
        """Testa l'inizializzazione del bot."""
        bot = MockBot("user", "pass")
        assert bot.username == "user"
        assert bot.password == "pass"
        assert bot.status == BotStatus.IDLE
        assert bot.headless is False  # Default

    def test_status_setter_signals(self):
        """Testa l'invio di segnali al cambio di stato."""
        bot = MockBot("u", "p")
        mock_signal = MagicMock()
        bot.signals.status_changed.connect(mock_signal.emit)

        bot.status = BotStatus.RUNNING
        assert mock_signal.emit.called
        assert bot.status == BotStatus.RUNNING

    def test_validate_data(self):
        """Testa la validazione dei dati."""
        bot = MockBot("u", "p")
        assert bot.validate_data([{"k": "v"}])[0] is True
        assert bot.validate_data([])[0] is False

        bot_no_creds = MockBot("", "")
        assert bot_no_creds.validate_data([{"k": "v"}])[0] is False

    @patch("src.bots.base.execution_guard.ExecutionGuard.check_environment")
    def test_execute_environment_denied(self, mock_guard):
        """Testa execute quando l'ambiente non è pronto (es. licenza)."""
        mock_guard.return_value = (False, "ACCESSO NEGATO: Licenza scaduta")
        bot = MockBot("u", "p")

        res = bot.execute([{"k": "v"}])
        assert res is False
        assert bot.status == BotStatus.ERROR

    @patch("src.bots.base.execution_guard.ExecutionGuard.check_environment")
    def test_execute_success_flow(self, mock_guard):
        """Testa il flusso di esecuzione positivo."""
        mock_guard.return_value = (True, "OK")
        bot = MockBot("u", "p")

        res = bot.execute([{"k": "v"}])
        assert res is True
        assert bot.status == BotStatus.COMPLETED

    def test_request_stop(self):
        """Testa la richiesta di stop."""
        bot = MockBot("u", "p")
        bot.request_stop()
        assert bot._stop_requested is True

        with pytest.raises(InterruptedError):
            bot._check_stop()

    @patch("src.bots.base.execution_guard.ExecutionGuard.check_environment")
    def test_execute_fatal_error(self, mock_guard):
        """Testa la gestione di errori fatali durante run."""
        mock_guard.return_value = (True, "OK")
        bot = MockBot("u", "p")

        with patch.object(MockBot, "run", side_effect=ValueError("Boom")):
            res = bot.execute([{"k": "v"}])
            assert res is False
            assert bot.status == BotStatus.ERROR
