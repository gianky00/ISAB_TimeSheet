from unittest.mock import MagicMock

import pytest

from src.core.app_updater import check_for_updates


class TestAppUpdaterCoverage:

    @pytest.fixture
    def mock_deps(self, mocker):
        """Mock per requests, webbrowser e QMessageBox nel namespace di app_updater."""
        mock_req = mocker.patch("src.core.app_updater.requests")
        mock_web = mocker.patch("src.core.app_updater.webbrowser")
        mock_msg = mocker.patch("src.core.app_updater.QMessageBox")

        # Patch modulo version
        mock_ver = mocker.patch("src.core.app_updater.version")
        mock_ver.__version__ = "1.0.0"
        mock_ver.UPDATE_URL = "http://fake.url"

        return {
            "requests": mock_req,
            "webbrowser": mock_web,
            "msgbox": mock_msg,
            "version": mock_ver
        }

    def test_update_available_and_user_confirms(self, mock_deps):
        """Test: Nuova versione disponibile, l'utente accetta di scaricarla."""
        mock_deps["version"].__version__ = "1.0.0"

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "version": "1.1.0",
            "url": "http://download.url",
            "changelog": "Fixes"
        }
        mock_deps["requests"].get.return_value = mock_resp

        # QMessageBox.question deve restituire YES
        from PyQt6.QtWidgets import QMessageBox
        mock_deps["msgbox"].StandardButton = QMessageBox.StandardButton # Mantieni accesso a Enum
        mock_deps["msgbox"].question.return_value = QMessageBox.StandardButton.Yes

        check_for_updates(silent=False)

        mock_deps["webbrowser"].open.assert_called_with("http://download.url")

    def test_app_is_up_to_date(self, mock_deps):
        """Test: L'app è già aggiornata (o versione locale > remota)."""
        mock_deps["version"].__version__ = "1.2.0"

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"version": "1.1.0"}
        mock_deps["requests"].get.return_value = mock_resp

        check_for_updates(silent=False)

        mock_deps["msgbox"].information.assert_called_once()
        mock_deps["webbrowser"].open.assert_not_called()

    def test_update_callback_mechanism(self, mock_deps):
        """Test: Utilizzo del meccanismo di callback invece del dialog standard."""
        mock_deps["version"].__version__ = "1.0.0"

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "version": "2.0.0",
            "url": "http://new.url",
            "changelog": "Mega update"
        }
        mock_deps["requests"].get.return_value = mock_resp

        callback = MagicMock()
        check_for_updates(callback=callback)

        callback.assert_called_with("2.0.0", "http://new.url", "Mega update")
        mock_deps["msgbox"].question.assert_not_called()

    def test_requests_timeout_handling(self, mock_deps):
        """Test: Gestione timeout o errori di rete (silent=False)."""
        mock_deps["requests"].get.side_effect = Exception("Timeout")

        check_for_updates(silent=False)
        mock_deps["msgbox"].information.assert_not_called()
