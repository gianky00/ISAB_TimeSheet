from unittest.mock import MagicMock

import pytest
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
    mock = mocker.patch("src.gui.dialogs.updater_dialog.QMessageBox")
    # Preserve StandardButton Enum for comparisons
    mock.StandardButton = QMessageBox.StandardButton
    return mock


def test_check_for_updates_no_url(mocker, mock_app_version, mock_msgbox):
    mocker.patch.object(version, "UPDATE_URL", None)

    # Patch functions in the GUI module
    mocker.patch("src.gui.dialogs.updater_dialog.get_web_update_info", return_value=None)
    mocker.patch("src.gui.dialogs.updater_dialog.get_network_update_info", return_value=None)

    check_for_updates(silent=False)

    # Should call information if no sources found
    mock_msgbox.information.assert_called_once()


def test_check_for_updates_no_new_version(mocker, mock_app_version, mock_update_url, mock_msgbox):
    # Simula versione uguale alla corrente
    mocker.patch(
        "src.gui.dialogs.updater_dialog.get_web_update_info",
        return_value={"version": "1.0.0", "url": "http://download.url"},
    )
    mocker.patch("src.gui.dialogs.updater_dialog.get_network_update_info", return_value=None)

    check_for_updates(silent=False)

    mock_msgbox.information.assert_called_once_with(
        None,
        "[OK] Aggiornamento",
        f"L'applicazione è aggiornata (v{version.__version__})",
    )


def test_check_for_updates_new_version_download(mocker, mock_app_version, mock_update_url, mock_msgbox):
    # Simula versione nuova
    mocker.patch(
        "src.gui.dialogs.updater_dialog.get_web_update_info",
        return_value={"version": "1.1.0", "url": "http://download.url"},
    )
    mocker.patch("src.gui.dialogs.updater_dialog.get_network_update_info", return_value=None)

    # Mock delle dipendenze GUI/Sistema
    mock_msgbox.question.return_value = QMessageBox.StandardButton.Yes
    mocker.patch.object(AuditManager, "log_action")
    mock_auto_update = mocker.patch("src.gui.dialogs.updater_dialog.perform_auto_update")

    # Mock HEAD request per la dimensione remota
    mock_resp = MagicMock()
    mock_resp.headers = {"content-length": "1000000"}
    mocker.patch("src.gui.dialogs.updater_dialog.requests.head", return_value=mock_resp)

    check_for_updates(silent=False)

    mock_msgbox.question.assert_called_once()
    mock_auto_update.assert_called_once_with("http://download.url", None)


def test_check_for_updates_new_version_no_download(mocker, mock_app_version, mock_update_url, mock_msgbox):
    mocker.patch(
        "src.gui.dialogs.updater_dialog.get_web_update_info",
        return_value={"version": "1.1.0", "url": "http://download.url"},
    )
    mocker.patch("src.gui.dialogs.updater_dialog.get_network_update_info", return_value=None)

    mock_msgbox.question.return_value = QMessageBox.StandardButton.No

    # Mock HEAD request
    mock_resp = MagicMock()
    mock_resp.headers = {"content-length": "1000000"}
    mocker.patch("src.gui.dialogs.updater_dialog.requests.head", return_value=mock_resp)

    check_for_updates(silent=False)

    mock_msgbox.question.assert_called_once()


def test_check_for_updates_http_error(mocker, mock_app_version, mock_update_url, mock_msgbox):
    mocker.patch("src.gui.dialogs.updater_dialog.get_web_update_info", return_value=None)
    mocker.patch("src.gui.dialogs.updater_dialog.get_network_update_info", return_value=None)

    check_for_updates(silent=False)

    mock_msgbox.information.assert_called_once()


def test_check_for_updates_silent_mode(mocker, mock_app_version, mock_update_url, mock_msgbox):
    mocker.patch(
        "src.gui.dialogs.updater_dialog.get_web_update_info",
        return_value={"version": "1.0.0", "url": "http://download.url"},
    )
    mocker.patch("src.gui.dialogs.updater_dialog.get_network_update_info", return_value=None)

    check_for_updates(silent=True)

    mock_msgbox.information.assert_not_called()


def test_check_for_updates_no_download_url_provided(mocker, mock_app_version, mock_update_url, mock_msgbox):
    mocker.patch(
        "src.gui.dialogs.updater_dialog.get_web_update_info",
        return_value={"version": "1.1.0", "url": None},
    )
    mocker.patch("src.gui.dialogs.updater_dialog.get_network_update_info", return_value=None)

    check_for_updates(silent=False)

    # Se l'URL è None, non dovrebbe nemmeno considerarlo una sorgente valida (info.get('url') check in code?)
    # Vediamo il codice: if info and info.get("version"): update_sources.append(info)
    # Quindi entra, ma poi download_url è None.
    # Se silent=False, dovrebbe mostrare "aggiornata" o nulla se ha fallito i check successivi.

    mock_msgbox.information.assert_called_once()
