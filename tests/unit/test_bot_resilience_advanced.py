from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus


# Classe concreta per testare BaseBot (che è astratta)
class MockBot(BaseBot):
    @property
    def name(self):
        return "MockBot"

    @property
    def description(self):
        return "Bot di test"

    def run(self, data):
        return True

    @staticmethod
    def get_columns():
        return []

    def _handle_unsaved_changes_popup(self):
        pass


class TestBotResilienceAdvanced:
    @pytest.fixture
    def bot(self, tmp_path, mocker):
        """Setup del bot con percorsi mockati."""
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)
        bot = MockBot("user", "pass")
        return bot

    def test_save_error_state_generation(self, bot, tmp_path):
        """Test: Verifica la generazione fisica di screenshot e HTML al crash."""
        mock_driver = MagicMock()
        mock_driver.page_source = "<html>Error</html>"
        bot.driver = mock_driver

        # Simuliamo il salvataggio
        bot._save_error_state("Test Error")

        # Verifichiamo la creazione dei file nella cartella logs/errors
        error_dir = tmp_path / "logs" / "errors"
        assert error_dir.exists()

        # 1. Verifica Screenshot (chiamata mock)
        mock_driver.save_screenshot.assert_called_once()
        args, _ = mock_driver.save_screenshot.call_args
        assert "error_mockbot_" in args[0]
        assert args[0].endswith(".png")

        # 2. Verifica HTML (file reale creato da Path.write_text)
        htmls = list(error_dir.glob("*.html"))
        assert len(htmls) == 1
        assert htmls[0].read_text(encoding="utf-8") == "<html>Error</html>"

    def test_safe_login_retry_logic(self, bot):
        """Test: Verifica che il bot riprovi il login in caso di fallimento temporaneo."""
        with (
            patch.object(bot, "_init_driver"),
            patch.object(bot, "_login") as mock_login,
            patch.object(bot, "cleanup") as mock_cleanup,
        ):
            # Fallisce la prima volta, riesce la seconda
            mock_login.side_effect = [False, True]

            res = bot._safe_login_with_retry(max_retries=2)

            assert res is True
            assert mock_login.call_count == 2
            assert mock_cleanup.call_count == 1  # Chiamato dopo il primo fallimento

    def test_execute_interrupted_error(self, bot):
        """Test: Gestione corretta dell'interruzione manuale dell'utente."""
        with patch.object(bot, "_safe_login_with_retry", side_effect=InterruptedError("Stop")):
            result = bot.execute([{"data": 1}])

            assert result is False
            assert bot.status == BotStatus.STOPPED

    def test_execute_fatal_error_handling(self, bot):
        """Test: Un errore fatale deve attivare il salvataggio dello stato e impostare lo stato ERROR."""
        with (
            patch.object(bot, "_safe_login_with_retry", return_value=True),
            patch.object(bot, "run", side_effect=Exception("Crash!")),
        ):
            with patch.object(bot, "_save_error_state") as mock_save:
                result = bot.execute([{"data": 1}])

                assert result is False
                assert bot.status == BotStatus.ERROR
                mock_save.assert_called_once_with("Crash!")

    def test_validate_data_empty(self, bot):
        """Test: Validazione fallita se i dati sono vuoti."""
        valid, msg = bot.validate_data([])
        assert valid is False
        assert "Nessun dato" in msg

    def test_check_stop_raises(self, bot):
        """Test: _check_stop solleva InterruptedError se richiesto stop."""
        bot.request_stop()
        with pytest.raises(InterruptedError):
            bot._check_stop()
