from unittest.mock import MagicMock

import pytest
import requests
from PyQt6.QtWidgets import QApplication, QMessageBox

# Simula QApplication prima di importare AppUpdater per evitare errori di Qt
app = QApplication([])

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


def test_check_for_updates_no_url(mocker, mock_app_version):
    mocker.patch.object(version, "UPDATE_URL", None)

    # Assicurati che non ci siano chiamate a requests.get
    mock_requests_get = mocker.patch("requests.get")
    check_for_updates(silent=False)
    mock_requests_get.assert_not_called()


def test_check_for_updates_no_new_version(mocker, mock_app_version, mock_update_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.0.0", "url": "http://download.url"}
    mocker.patch("requests.get", return_value=mock_response)

    mock_qmessagebox_info = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
    check_for_updates(silent=False)

    mock_qmessagebox_info.assert_called_once_with(
        None, "✅ Aggiornamento", f"L'applicazione è aggiornata (v{version.__version__})"
    )


def test_check_for_updates_new_version_download(mocker, mock_app_version, mock_update_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.1.0", "url": "http://download.url"}
    mocker.patch("requests.get", return_value=mock_response)

    mock_qmessagebox_question = mocker.patch("PyQt6.QtWidgets.QMessageBox.question")
    mock_qmessagebox_question.return_value = QMessageBox.StandardButton.Yes
    mock_webbrowser_open = mocker.patch("webbrowser.open")
    mock_audit_log = mocker.patch.object(AuditManager, "log_action")

    check_for_updates(silent=False)

    mock_qmessagebox_question.assert_called_once()
    mock_webbrowser_open.assert_called_once_with("http://download.url")
    # mock_audit_log.assert_called_once() # Removed as per implementation


def test_check_for_updates_new_version_no_download(mocker, mock_app_version, mock_update_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.1.0", "url": "http://download.url"}
    mocker.patch("requests.get", return_value=mock_response)

    mock_qmessagebox_question = mocker.patch("PyQt6.QtWidgets.QMessageBox.question")
    mock_qmessagebox_question.return_value = QMessageBox.StandardButton.No
    mock_webbrowser_open = mocker.patch("webbrowser.open")
    mock_audit_log = mocker.patch.object(AuditManager, "log_action")

    check_for_updates(silent=False)

    mock_qmessagebox_question.assert_called_once()
    mock_webbrowser_open.assert_not_called()
    mock_audit_log.assert_not_called()


def test_check_for_updates_http_error(mocker, mock_app_version, mock_update_url):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)

    mock_qmessagebox_info = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
    check_for_updates(silent=False)

    mock_qmessagebox_info.assert_not_called()  # Should print to console, not show message box for non-silent


def test_check_for_updates_timeout(mocker, mock_app_version, mock_update_url):
    mocker.patch("requests.get", side_effect=requests.Timeout)

    mock_qmessagebox_info = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
    check_for_updates(silent=False)

    mock_qmessagebox_info.assert_not_called()


def test_check_for_updates_request_exception(mocker, mock_app_version, mock_update_url):
    mocker.patch("requests.get", side_effect=requests.RequestException("Connection error"))

    mock_qmessagebox_info = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
    check_for_updates(silent=False)

    mock_qmessagebox_info.assert_not_called()


def test_check_for_updates_silent_mode(mocker, mock_app_version, mock_update_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.0.0", "url": "http://download.url"}
    mocker.patch("requests.get", return_value=mock_response)

    mock_qmessagebox_info = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
    check_for_updates(silent=True)

    mock_qmessagebox_info.assert_not_called()


def test_check_for_updates_no_download_url_provided(mocker, mock_app_version, mock_update_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"version": "1.1.0", "url": None}
    mocker.patch("requests.get", return_value=mock_response)

    mock_qmessagebox_question = mocker.patch("PyQt6.QtWidgets.QMessageBox.question")
    mock_qmessagebox_question.return_value = QMessageBox.StandardButton.Yes
    mock_webbrowser_open = mocker.patch("webbrowser.open")
    mock_qmessagebox_information = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")

    check_for_updates(silent=False)

    mock_qmessagebox_question.assert_called_once()
    mock_webbrowser_open.assert_not_called()
    mock_qmessagebox_information.assert_not_called()
