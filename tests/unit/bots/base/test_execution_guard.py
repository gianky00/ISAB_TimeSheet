from unittest.mock import patch

from src.bots.base.execution_guard import ExecutionGuard


class TestExecutionGuard:
    @patch("src.core.license_validator.verify_license")
    def test_check_environment_success(self, mock_verify):
        """Testa il successo del pre-check."""
        mock_verify.return_value = (True, "")

        ok, _msg = ExecutionGuard.check_environment()
        assert ok is True

    @patch("src.core.license_validator.verify_license")
    def test_check_environment_license_invalid(self, mock_verify):
        """Testa il fallimento della licenza."""
        mock_verify.return_value = (False, "Licenza scaduta")

        ok, msg = ExecutionGuard.check_environment()
        assert ok is False
        assert msg == "Licenza scaduta"

    @patch("src.core.license_validator.verify_license")
    def test_check_environment_exception_handling(self, mock_verify):
        """Testa la gestione di eccezioni impreviste durante la verifica."""
        mock_verify.side_effect = Exception("Crash")

        # In questo caso l'eccezione non è catturata da ExecutionGuard volutamente per lasciarla al bot
        import pytest

        with pytest.raises(Exception, match="Crash"):
            ExecutionGuard.check_environment()
