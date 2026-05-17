from unittest.mock import patch

from src.bots.base.execution_guard import ExecutionGuard


class TestExecutionGuard:
    @patch("src.core.license_validator.verify_license")
    @patch("src.core.license_updater.run_update")
    def test_check_environment_success(self, mock_update, mock_verify):
        """Testa il successo del pre-check."""
        mock_verify.return_value = (True, "")

        ok, _msg = ExecutionGuard.check_environment()
        assert ok is True
        assert mock_update.called

    @patch("src.core.license_validator.verify_license")
    @patch("src.core.license_updater.run_update")
    def test_check_environment_license_invalid(self, mock_update, mock_verify):
        """Testa il fallimento della licenza."""
        mock_verify.return_value = (False, "Licenza scaduta")

        ok, msg = ExecutionGuard.check_environment()
        assert ok is False
        assert msg == "Licenza scaduta"

    @patch("src.core.license_updater.run_update")
    def test_check_environment_license_revoked(self, mock_update):
        """Testa la revoca della licenza durante l'update."""
        mock_update.side_effect = Exception("LICENZA REVOCATA")

        ok, msg = ExecutionGuard.check_environment()
        assert ok is False
        assert "ACCESSO NEGATO" in msg

    @patch("src.core.license_validator.verify_license")
    @patch("src.core.license_updater.run_update")
    def test_check_environment_silent_update_error(self, mock_update, mock_verify):
        """Testa errore silente durante update (continua comunque)."""
        mock_update.side_effect = Exception("Network timeout")
        mock_verify.return_value = (True, "")

        ok, _msg = ExecutionGuard.check_environment()
        assert ok is True  # Continua se non è revoca
