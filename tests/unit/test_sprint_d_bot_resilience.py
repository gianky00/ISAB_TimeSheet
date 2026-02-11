from unittest.mock import MagicMock

import pytest

from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus


# Classe concreta minima per testare la BaseBot astratta
class DummyBot(BaseBot):
    @property
    def name(self):
        return "Dummy"

    @property
    def description(self):
        return "Test Bot"

    def run(self, data):
        return True

    @staticmethod
    def get_columns():
        return []

    def _handle_unsaved_changes_popup(self):
        pass


class TestSprintDBotResilience:
    @pytest.fixture
    def bot(self, mocker, tmp_path):
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)
        mocker.patch("src.core.config_manager.load_config", return_value={})
        return DummyBot("user", "pass")

    def test_bot_retry_logic_on_login_failure(self, bot, mocker):
        """Verifica che il bot riprovi il login in caso di fallimento iniziale."""
        # Mocking _init_driver per non aprire browser reali
        mocker.patch.object(bot, "_init_driver")
        mocker.patch.object(bot, "cleanup")

        # Primo tentativo fallisce, secondo riesce
        mock_login = mocker.patch.object(bot, "_login", side_effect=[False, True])

        result = bot._safe_login_with_retry(max_retries=2)

        assert result is True
        assert mock_login.call_count == 2
        assert bot.cleanup.call_count == 1  # Chiamato dopo il primo fallimento

    def test_bot_error_capture_screenshot(self, bot, mocker, tmp_path):
        """Verifica che il bot salvi screenshot e HTML in caso di errore fatale."""
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)

        # Mock Driver
        mock_driver = MagicMock()
        mock_driver.page_source = "<html>Error</html>"
        bot.driver = mock_driver

        # Make save_screenshot create a dummy file so glob finds it
        def dummy_save(path):
            from pathlib import Path

            Path(path).write_text("fake png")

        mock_driver.save_screenshot.side_effect = dummy_save

        bot._save_error_state("Test Error")

        error_dir = tmp_path / "logs" / "errors"
        assert error_dir.exists()

        # Verifica presenza file (usa glob per via del timestamp nel nome)
        screenshots = list(error_dir.glob("*.png"))
        html_files = list(error_dir.glob("*.html"))

        assert len(screenshots) == 1
        assert len(html_files) == 1
        assert html_files[0].read_text() == "<html>Error</html>"
        mock_driver.save_screenshot.assert_called_once()

    def test_bot_user_interruption(self, bot, mocker):
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

    def test_bot_driver_initialization_failure_handling(self, bot, mocker):
        """Verifica la gestione di errori critici durante l'init del driver (es. version mismatch)."""
        # Simula errore di versione driver
        mocker.patch(
            "selenium.webdriver.Chrome",
            side_effect=Exception("SessionNotCreatedException: version mismatch"),
        )
        mocker.patch(
            "webdriver_manager.chrome.ChromeDriverManager.install",
            return_value="fake_path",
        )

        # Dobbiamo catturare i log per verificare il suggerimento all'utente
        logs = []
        bot.set_log_callback(lambda m: logs.append(m))

        with pytest.raises(Exception, match="version mismatch"):
            bot._init_driver()

        assert any("💡 SUGGERIMENTO: Aggiorna Chrome" in m for m in logs)
        assert bot.status == BotStatus.INITIALIZING
