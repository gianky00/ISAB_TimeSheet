"""Unit tests for AppStatusController."""

from unittest.mock import MagicMock

import pytest

from src.gui.controllers.app_status_controller import AppStatusController


@pytest.fixture
def mock_main_window():
    mw = MagicMock()
    mw.status_bar_component = MagicMock()
    mw.status_bar_component.footer_left = MagicMock()
    return mw


class TestAppStatusController:
    """Test suite per AppStatusController."""

    def test_rotate_account_success(self, mock_main_window, mocker):
        mocker.patch("src.application.services.config_manager.switch_default_account", return_value=True)
        mock_toast = mocker.patch("src.gui.widgets.toast.ToastManager.instance")

        ctrl = AppStatusController(mock_main_window)
        ctrl.rotate_account("isab")

        assert mock_main_window.status_bar_component.show_operational_state.called
        assert mock_main_window.status_bar_component.footer_left.refresh_accounts.called
        assert mock_toast.return_value.show.called
        assert "isab" in mock_toast.return_value.show.call_args[0][0].lower()

    def test_rotate_account_failure(self, mock_main_window, mocker):
        mocker.patch("src.application.services.config_manager.switch_default_account", return_value=False)
        mock_toast = mocker.patch("src.gui.widgets.toast.ToastManager.instance")

        ctrl = AppStatusController(mock_main_window)
        ctrl.rotate_account("isab")

        assert mock_toast.return_value.show.called
        assert mock_toast.return_value.show.call_args[0][1] == "warning"

    def test_switch_engine(self, mock_main_window, mocker):
        mocker.patch("src.application.services.config_manager.get_config_value", return_value="selenium")
        mock_set = mocker.patch("src.application.services.config_manager.set_config_value", return_value=True)
        mock_toast = mocker.patch("src.gui.widgets.toast.ToastManager.instance")

        ctrl = AppStatusController(mock_main_window)
        ctrl.switch_engine()

        mock_set.assert_called_with("automation_engine", "playwright")
        assert mock_toast.return_value.show.called

    def test_switch_headless(self, mock_main_window, mocker):
        mocker.patch(
            "src.application.services.config_manager.get_config_value", return_value=False
        )  # Visibile
        mock_set = mocker.patch("src.application.services.config_manager.set_config_value", return_value=True)
        mock_toast = mocker.patch("src.gui.widgets.toast.ToastManager.instance")

        ctrl = AppStatusController(mock_main_window)
        ctrl.switch_headless()

        mock_set.assert_called_with("browser_headless", True)  # Diventa nascosto
        assert mock_toast.return_value.show.called
        assert "NASCOSTO" in mock_toast.return_value.show.call_args[0][0]
