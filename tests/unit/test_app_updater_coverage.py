import pytest
from unittest.mock import MagicMock, patch
from src.core.app_updater import check_for_updates, _is_newer_version, _handle_update_found
from src.core import version

class TestAppUpdater:
    @pytest.fixture
    def mock_requests(self, mocker):
        return mocker.patch("requests.get")

    @pytest.fixture
    def mock_webbrowser(self, mocker):
        return mocker.patch("webbrowser.open")

    @pytest.fixture
    def mock_qmessagebox(self, mocker):
        return mocker.patch("src.core.app_updater.QMessageBox")

    def test_check_for_updates_no_url(self, mock_requests, monkeypatch):
        monkeypatch.setattr(version, "UPDATE_URL", "")
        check_for_updates()
        mock_requests.assert_not_called()

    def test_check_for_updates_request_fail(self, mock_requests, monkeypatch):
        monkeypatch.setattr(version, "UPDATE_URL", "http://test.url")
        mock_requests.return_value.status_code = 404
        check_for_updates()
        # Should exit gracefully

    def test_check_for_updates_newer_found(self, mock_requests, mock_qmessagebox, mock_webbrowser, monkeypatch):
        monkeypatch.setattr(version, "UPDATE_URL", "http://test.url")
        monkeypatch.setattr(version, "__version__", "1.0.0")
        
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "version": "1.1.0",
            "url": "http://download.url",
            "changelog": "Fix bugs"
        }
        mock_requests.return_value = mock_resp
        
        # Simulate user clicking Yes
        mock_qmessagebox.question.return_value = mock_qmessagebox.StandardButton.Yes
        
        check_for_updates(silent=False)
        
        mock_qmessagebox.question.assert_called_once()
        mock_webbrowser.assert_called_with("http://download.url")

    def test_check_for_updates_not_newer(self, mock_requests, mock_qmessagebox, monkeypatch):
        monkeypatch.setattr(version, "UPDATE_URL", "http://test.url")
        monkeypatch.setattr(version, "__version__", "1.0.0")
        
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"version": "1.0.0"}
        mock_requests.return_value = mock_resp
        
        check_for_updates(silent=False)
        
        mock_qmessagebox.information.assert_called_once() # "Già aggiornato"

    def test_is_newer_version(self, monkeypatch):
        monkeypatch.setattr(version, "__version__", "1.0.0")
        assert _is_newer_version("1.1.0") is True
        assert _is_newer_version("0.9.0") is False
        assert _is_newer_version("1.0.0") is False
        assert _is_newer_version("invalid") is False

    def test_handle_update_found_callback(self):
        cb = MagicMock()
        _handle_update_found("1.1", "url", "log", None, cb)
        cb.assert_called_with("1.1", "url", "log")

    def test_check_updates_silent_exception(self, mock_requests, monkeypatch):
        monkeypatch.setattr(version, "UPDATE_URL", "http://test.url")
        mock_requests.side_effect = Exception("Network error")
        
        # Silent=True, should not print or show message
        check_for_updates(silent=True)
        
        # Silent=False, should print (can't easily assert print, but ensure no crash)
        check_for_updates(silent=False)