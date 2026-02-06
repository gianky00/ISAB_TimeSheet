from unittest.mock import MagicMock

import pytest
import requests
from PyQt6.QtWidgets import QMessageBox

from src.core import version
from src.core.app_updater import check_for_updates
from src.core.audit_manager import AuditManager


@pytest.fixture
def mock_app_version():
    # Salva la versione originale e ripristina alla fine del test
    original_version = version.__version__
    version.__version__ = "1.0.0"
    yield
    version.__version__ = original_version


@pytest.fixture
def mock_update_url():
    original_url = version.UPDATE_URL
    version.UPDATE_URL = "http://fake.update.url"
    yield
    version.UPDATE_URL = original_url


@pytest.fixture
def mock_msgbox(mocker):
    """Mock the whole QMessageBox class in the target module while preserving Enums."""
    mock = mocker.patch("src.core.app_updater.QMessageBox")
    # Preserve StandardButton Enum for comparisons
    mock.StandardButton = QMessageBox.StandardButton
    return mock


def test_check_for_updates_no_url(mocker, mock_app_version, mock_msgbox):
    mocker.patch.object(version, "UPDATE_URL", None)

    # Assicurati che non ci siano chiamate a requests.get
    mock_requests_get = mocker.patch("requests.get")
    check_for_updates(silent=False)
    mock_requests_get.assert_not_called()


def test_check_for_updates_no_new_version(
    mocker, mock_app_version, mock_update_url, mock_msgbox
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.0.0", "url": "http://download.url"}
    mocker.patch("requests.get", return_value=mock_response)

    check_for_updates(silent=False)

    mock_msgbox.information.assert_called_once_with(
        None,
        "✅ Aggiornamento",
        f"L'applicazione è aggiornata (v{version.__version__})",
    )


def test_check_for_updates_new_version_download(
    mocker, mock_app_version, mock_update_url, mock_msgbox
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.1.0", "url": "http://download.url"}
    mocker.patch("requests.get", return_value=mock_response)

    mock_msgbox.question.return_value = QMessageBox.StandardButton.Yes
    mock_webbrowser_open = mocker.patch("webbrowser.open")
    mocker.patch.object(AuditManager, "log_action")

    check_for_updates(silent=False)

    mock_msgbox.question.assert_called_once()
    mock_webbrowser_open.assert_called_once_with("http://download.url")


def test_check_for_updates_new_version_no_download(
    mocker, mock_app_version, mock_update_url, mock_msgbox
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.1.0", "url": "http://download.url"}
    mocker.patch("requests.get", return_value=mock_response)

    mock_msgbox.question.return_value = QMessageBox.StandardButton.No
    mock_webbrowser_open = mocker.patch("webbrowser.open")
    mocker.patch.object(AuditManager, "log_action")

    check_for_updates(silent=False)

    mock_msgbox.question.assert_called_once()
    mock_webbrowser_open.assert_not_called()


def test_check_for_updates_http_error(
    mocker, mock_app_version, mock_update_url, mock_msgbox
):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)

    check_for_updates(silent=False)

    mock_msgbox.information.assert_not_called()


def test_check_for_updates_timeout(
    mocker, mock_app_version, mock_update_url, mock_msgbox
):
    mocker.patch("requests.get", side_effect=requests.Timeout)

    check_for_updates(silent=False)

    mock_msgbox.information.assert_not_called()


def test_check_for_updates_request_exception(
    mocker, mock_app_version, mock_update_url, mock_msgbox
):
    mocker.patch(
        "requests.get", side_effect=requests.RequestException("Connection error")
    )

    check_for_updates(silent=False)

    mock_msgbox.information.assert_not_called()


def test_check_for_updates_silent_mode(
    mocker, mock_app_version, mock_update_url, mock_msgbox
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.0.0", "url": "http://download.url"}
    mocker.patch("requests.get", return_value=mock_response)

    check_for_updates(silent=True)

    mock_msgbox.information.assert_not_called()


def test_check_for_updates_no_download_url_provided(
    mocker, mock_app_version, mock_update_url, mock_msgbox
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.1.0", "url": None}
    mocker.patch("requests.get", return_value=mock_response)

    mock_msgbox.question.return_value = QMessageBox.StandardButton.Yes
    mock_webbrowser_open = mocker.patch("webbrowser.open")

    check_for_updates(silent=False)

    mock_msgbox.question.assert_called_once()
    mock_webbrowser_open.assert_not_called()
    mock_msgbox.information.assert_not_called()
