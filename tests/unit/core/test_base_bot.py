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
    def get_columns():  # noqa: ANN205
        return []

    from typing import ClassVar  # noqa: PLC0415

    STEPS: ClassVar[list[tuple[str, str]]] = [("step1", "Step 1"), ("step2", "Step 2")]

    def run(self, data):  # noqa: ANN001
        self.update_step("step2", StepStatus.RUNNING)
        return True


class TestBaseBot:
    @pytest.fixture
    def bot(self):
        return DummyBot("user", "pass")

    def test_initialize_steps(self, bot):  # noqa: ANN001
        bot._initialize_steps()
        assert len(bot._steps_state) == 2  # noqa: PLR2004
        assert bot._steps_state[0] == StepStatus.PENDING

    @patch("src.core.license_validator.verify_license", return_value=(True, "OK"))
    @patch("src.core.license_updater.run_update")
    def test_execute_workflow_success(self, mock_upd, mock_lic, bot):  # noqa: ANN001
        """Verifica il flusso completo di esecuzione: login -> run -> cleanup."""
        # Mocking internal methods
        bot._safe_login_with_retry = MagicMock(return_value=True)
        bot.cleanup = MagicMock()

        result = bot.execute([{"data": "test"}])

        assert result is True
        assert bot.status == BotStatus.COMPLETED
        bot._safe_login_with_retry.assert_called_once()
        bot.cleanup.assert_called_once()

    def test_validate_data_empty(self, bot):  # noqa: ANN001
        success, msg = bot.validate_data([])
        assert success is False
        assert "Nessun dato" in msg

    def test_save_error_state(self, bot, tmp_path):  # noqa: ANN001
        """Verifica il salvataggio di screenshot e HTML in caso di errore."""
        # Creiamo la struttura log dir reale
        log_dir = tmp_path / "logs" / "errors"
        log_dir.mkdir(parents=True)

        with patch("src.bots.base.base_bot.config_manager.CONFIG_DIR", tmp_path):
            bot.driver = MagicMock()
            bot.driver.page_source = "<html><script>alert(1)</script><body>Test</body></html>"

            bot._save_error_state("Test Error")

            # Verifica creazione file HTML (write_text crea il file sul disco reale se il path è reale)
            html_files = list(log_dir.glob("*.html"))
            assert len(html_files) == 1

            # Verifica chiamata screenshot
            assert bot.driver.save_screenshot.called

            # Verifica sanificazione HTML (no script)
            content = html_files[0].read_text(encoding="utf-8")
            assert "<script" not in content
            assert "SCRIPT REMOVED" in content

    def test_request_stop_logic(self, bot):  # noqa: ANN001
        """Verifica che la richiesta di stop alzi l'eccezione corretta."""
        bot.request_stop()
        assert bot._stop_requested is True

        with pytest.raises(InterruptedError):
            bot._check_stop()
