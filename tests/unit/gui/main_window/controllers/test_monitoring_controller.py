"""Unit tests for MonitoringController."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QMainWindow

from src.gui.main_window.controllers.monitoring_controller import MonitoringController


@pytest.fixture
def real_main_window(qtbot):
    mw = QMainWindow()
    mw.sidebar = MagicMock()
    mw.sidebar.btn_dipendenti = MagicMock()
    qtbot.addWidget(mw)
    return mw


class TestMonitoringController:
    """Test suite per MonitoringController."""

    def test_initialization(self, real_main_window):
        ctrl = MonitoringController(real_main_window)
        assert ctrl.auth_check_timer is not None
        assert not ctrl.auth_check_timer.isActive()

    def test_start_monitoring(self, real_main_window, mocker):
        ctrl = MonitoringController(real_main_window)
        mock_check = mocker.patch.object(ctrl, "check_isab_authorizations")

        ctrl.start_monitoring()

        assert mock_check.called
        assert ctrl.auth_check_timer.isActive()

    def test_check_isab_authorizations_expiring(self, real_main_window, mocker):
        # Setup mock data: 1 scaduta, 1 in scadenza
        expiring = [{"stato": "SCADUTA", "nome": "Rossi"}, {"stato": "IN SCADENZA", "nome": "Verdi"}]
        mocker.patch(
            "src.gui.main_window.controllers.monitoring_controller.check_expiring_isab_authorizations",
            return_value=expiring,
        )
        mock_toast = mocker.patch("src.gui.widgets.toast.ToastManager.instance")

        ctrl = MonitoringController(real_main_window)
        ctrl.check_isab_authorizations()

        # Verifica badge sidebar
        real_main_window.sidebar.btn_dipendenti.set_badge.assert_called_with(2)

        # Verifica toast
        assert mock_toast.return_value.show.called
        toast_msg = mock_toast.return_value.show.call_args[0][0]
        assert "SCADUTE" in toast_msg
        assert "In scadenza" in toast_msg

    def test_check_isab_authorizations_empty(self, real_main_window, mocker):
        mocker.patch(
            "src.gui.main_window.controllers.monitoring_controller.check_expiring_isab_authorizations",
            return_value=[],
        )
        mock_toast = mocker.patch("src.gui.widgets.toast.ToastManager.instance")

        ctrl = MonitoringController(real_main_window)
        ctrl.check_isab_authorizations()

        # Badge resettato a 0
        real_main_window.sidebar.btn_dipendenti.set_badge.assert_called_with(0)
        # Nessun toast se vuoto
        assert not mock_toast.return_value.show.called
