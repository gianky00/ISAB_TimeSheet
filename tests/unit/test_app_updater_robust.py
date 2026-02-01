from unittest.mock import MagicMock, patch

from src.core.app_updater import (
    _handle_update_found,
    _is_newer_version,
    check_for_updates,
)


class TestAppUpdaterRobust:
    @patch("src.core.version.__version__", "1.10.0")
    def test_is_newer_version(self):
        assert _is_newer_version("1.11.0") is True
        assert _is_newer_version("1.10.1") is True
        assert _is_newer_version("1.10.0") is False
        assert _is_newer_version("1.9.0") is False
        assert _is_newer_version("invalid") is False

    @patch("src.core.app_updater.requests.get")
    @patch("src.core.version.UPDATE_URL", "http://fake.url")
    def test_check_for_updates_success(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "version": "2.0.0",
            "url": "http://download.url",
            "changelog": "Big update",
        }
        mock_get.return_value = mock_response

        with patch("src.core.app_updater._is_newer_version", return_value=True):
            with patch("src.core.app_updater._handle_update_found") as mock_handle:
                check_for_updates()
                mock_handle.assert_called_once_with(
                    "2.0.0", "http://download.url", "Big update", None, None
                )

    @patch("src.core.app_updater.requests.get")
    @patch("src.core.version.UPDATE_URL", "http://fake.url")
    def test_check_for_updates_failure(self, mock_get):
        # 1. 404 Error
        mock_get.return_value.status_code = 404
        check_for_updates()  # Should not raise

        # 2. Timeout/Network Error
        mock_get.side_effect = Exception("Connection Timeout")
        check_for_updates(silent=False)  # Should print but not crash

    @patch("src.core.app_updater.QMessageBox.question")
    @patch("src.core.app_updater.webbrowser.open")
    def test_handle_update_found_gui(self, mock_browser, mock_msgbox):
        from PyQt6.QtWidgets import QMessageBox

        # Simuliamo click su "Yes"
        mock_msgbox.return_value = QMessageBox.StandardButton.Yes

        _handle_update_found("2.0.0", "http://download.url", "Changelog", None, None)

        mock_browser.assert_called_once_with("http://download.url")

    def test_handle_update_found_callback(self):
        mock_callback = MagicMock()

        _handle_update_found("2.0.0", "http://url", "Changes", None, mock_callback)

        mock_callback.assert_called_once_with("2.0.0", "http://url", "Changes")
