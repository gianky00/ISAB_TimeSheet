"""
Tests for AppUpdater.
Verifies version check and update notification.
"""

from unittest.mock import MagicMock

import requests

from src.core.app_updater import check_for_updates


class TestAppUpdaterSimulation:
    def test_check_for_updates_found(self, mocker):
        """Verifica la logica quando viene trovata una nuova versione."""
        # 1. Mock della versione locale (es. v1.0.0)
        mocker.patch("src.core.app_updater.version.__version__", "1.0.0")
        mocker.patch("src.core.app_updater.version.UPDATE_URL", "http://update.api")

        # 2. Mock della risposta API (es. v1.1.0)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "version": "1.1.0",
            "url": "http://download.exe",
            "changelog": "Novità incredibili",
        }
        mocker.patch("requests.get", return_value=mock_resp)

        # 3. Mock della UI (QMessageBox)
        mock_msg = mocker.patch("PyQt6.QtWidgets.QMessageBox.question")
        mock_msg.return_value = MagicMock()  # Non importa cosa preme qui

        check_for_updates(silent=False)

        # Deve aver mostrato la domanda di aggiornamento
        assert mock_msg.called
        args = mock_msg.call_args[0]
        assert "1.1.0" in args[2]  # Messaggio contiene nuova versione

    def test_check_for_updates_already_updated(self, mocker):
        """Verifica che non faccia nulla se la versione locale è uguale o maggiore."""
        mocker.patch("src.core.app_updater.version.__version__", "2.0.0")
        mocker.patch("src.core.app_updater.version.UPDATE_URL", "http://update.api")

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"version": "1.5.0"}
        mocker.patch("requests.get", return_value=mock_resp)

        mock_msg = mocker.patch("PyQt6.QtWidgets.QMessageBox.question")

        check_for_updates(silent=True)

        # Non deve aver mostrato nulla
        assert not mock_msg.called

    def test_check_for_updates_http_error(self, mocker):
        """Verifica che gli errori di rete non causino crash (silent=True)."""
        mocker.patch("src.core.app_updater.version.UPDATE_URL", "http://bad.url")
        mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Offline"))

        # Non deve sollevare eccezioni
        check_for_updates(silent=True)
