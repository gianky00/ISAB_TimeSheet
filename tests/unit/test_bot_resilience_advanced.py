from pathlib import Path
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
        self._check_stop()
        return True

    @staticmethod
    def get_columns():
        return []

    # Implementazione metodi astratti V9.0
    def _init_driver(self):
        pass

    def _login(self):
        return True

    def _save_error_state(self, error_msg):
        # Implementazione reale per testare test_save_error_state_generation
        from src.core.paths import get_logs_path

        error_dir = Path(get_logs_path()) / "errors"
        error_dir.mkdir(parents=True, exist_ok=True)

        if self.driver:
            self.driver.save_screenshot(str(error_dir / "error.png"))
            (error_dir / "error.html").write_text(self.driver.page_source, encoding="utf-8")

    def cleanup(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def _handle_unsaved_changes_popup(self):
        pass


class TestBotResilienceAdvanced:
    @pytest.fixture
    def bot(self, tmp_path, mocker):
        """Setup del bot con percorsi mockati."""
        mocker.patch("src.core.paths.get_logs_path", return_value=str(tmp_path / "logs"))
        # Mocking ExecutionGuard to avoid license issues
        mocker.patch("src.bots.base.base_bot.ExecutionGuard.check_environment", return_value=(True, "OK"))
        bot = MockBot("user", "pass")
        bot.signals = MagicMock()
        bot.driver = None  # FIX: Inizializza attributo driver
        return bot

    def test_save_error_state_generation(self, bot, tmp_path):
        """Test: Verifica la generazione fisica di screenshot e HTML al crash."""
        mock_driver = MagicMock()
        mock_driver.page_source = "<html>Error</html>"
        bot.driver = mock_driver

        # Simuliamo il salvataggio
        bot._save_error_state("Test Error")

        # Verifichiamo la creazione dei file
        error_dir = tmp_path / "logs" / "errors"
        assert error_dir.exists()

        # 1. Verifica Screenshot
        mock_driver.save_screenshot.assert_called_once()

        # 2. Verifica HTML
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
