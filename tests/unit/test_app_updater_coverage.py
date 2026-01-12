
import pytest
import requests
from unittest.mock import MagicMock, patch
from src.core.app_updater import check_for_updates

class TestAppUpdaterCoverage:
    @pytest.fixture
    def mock_version(self, mocker):
        mocker.patch("src.core.version.__version__", "1.0.0")
        mocker.patch("src.core.version.UPDATE_URL", "https://api.github.com/repos/test/update.json")
        return "1.0.0"

    def test_check_for_updates_newer_version_callback(self, mock_version, mocker):
        """Verifica che la callback venga chiamata se è disponibile una nuova versione."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "version": "1.1.0",
            "url": "https://download.com/app.exe",
            "changelog": "New features"
        }
        
        mocker.patch("requests.get", return_value=mock_response)
        
        callback = MagicMock()
        check_for_updates(callback=callback)
        
        callback.assert_called_once_with("1.1.0", "https://download.com/app.exe", "New features")

    def test_check_for_updates_older_version_silent(self, mock_version, mocker):
        """Verifica che in silent mode non succeda nulla se l'app è aggiornata."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"version": "0.9.0"} # Più vecchia
        
        mocker.patch("requests.get", return_value=mock_response)
        mock_msgbox = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
        
        check_for_updates(silent=True)
        mock_msgbox.assert_not_called()

    def test_check_for_updates_newer_version_gui_yes(self, mock_version, mocker):
        """Verifica che la risposta 'Yes' al dialog apra il browser."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "version": "2.0.0",
            "url": "https://update.com"
        }
        
        mocker.patch("requests.get", return_value=mock_response)
        
        # Simula click su "Yes"
        from PyQt6.QtWidgets import QMessageBox
        mocker.patch("PyQt6.QtWidgets.QMessageBox.question", return_value=QMessageBox.StandardButton.Yes)
        mock_browser = mocker.patch("webbrowser.open")
        
        check_for_updates(silent=False)
        
        mock_browser.assert_called_once_with("https://update.com")

    def test_check_for_updates_network_error(self, mock_version, mocker):
        """Verifica gestione errore di rete durante il controllo."""
        mocker.patch("requests.get", side_effect=requests.RequestException("Offline"))
        # Non deve crashare
        check_for_updates(silent=True)

    def test_check_for_updates_invalid_url(self, mocker):
        """Verifica che non faccia nulla se l'URL è vuoto."""
        mocker.patch("src.core.version.UPDATE_URL", "")
        mock_get = mocker.patch("requests.get")
        
        check_for_updates()
        mock_get.assert_not_called()
