"""Unit tests for WorkflowController."""

from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QMainWindow

from src.gui.main_window.controllers.workflow_controller import WorkflowController


@pytest.fixture
def real_main_window(qtbot):
    mw = QMainWindow()
    mw.navigation_controller = MagicMock()
    mw.status_bar_component = MagicMock()
    mw.status_bar_component.status_portale = MagicMock()
    qtbot.addWidget(mw)
    return mw


class TestWorkflowController:
    """Test suite per WorkflowController."""

    def test_run_timbrature_bot_ieri(self, real_main_window, mocker):
        ctrl = WorkflowController(real_main_window)
        mock_panel = MagicMock()
        mock_panel.status_changed = MagicMock()
        real_main_window.timbrature_bot_panel = mock_panel

        mocker.patch("src.gui.widgets.toast.ToastManager.instance")

        ctrl.run_timbrature_bot("ieri")

        yesterday = QDate.currentDate().addDays(-1).toString("dd.MM.yyyy")
        mock_panel.run_externally.assert_called_with({"data_da": yesterday, "data_a": yesterday})

    def test_handle_scarico_ts_input(self, real_main_window, qtbot):
        ctrl = WorkflowController(real_main_window)
        mock_panel = MagicMock()
        real_main_window.scarico_panel = mock_panel

        ctrl.handle_scarico_ts_input(["ODA123"])

        real_main_window.navigation_controller.navigate_to_panel.assert_called_with("scarico_ts")
        # Attesa del singleShot(200)
        qtbot.wait(300)
        assert mock_panel.run_externally.called
        args = mock_panel.run_externally.call_args[0][0]
        assert args["single_item"]["numero_oda"] == "ODA123"

    def test_run_carico_ts(self, real_main_window, qtbot):
        ctrl = WorkflowController(real_main_window)
        mock_panel = MagicMock()
        real_main_window.carico_panel = mock_panel

        ctrl.run_carico_ts()

        real_main_window.navigation_controller.navigate_to_panel.assert_called_with("carico_ts")
        qtbot.wait(300)
        assert mock_panel.run_externally.called

    def test_run_sync_dataease(self, real_main_window, qtbot):
        ctrl = WorkflowController(real_main_window)
        mock_panel = MagicMock()
        real_main_window.scarico_ore_panel = mock_panel

        ctrl.run_sync_dataease()

        from src.gui.main_window.page_index import PageIndex

        real_main_window.navigation_controller.navigate_to.assert_called_with(PageIndex.DATAEASE)
        qtbot.wait(300)
        assert mock_panel._start_update.called

    def test_run_dettagli_oda_update(self, real_main_window, qtbot, mocker):
        ctrl = WorkflowController(real_main_window)

        # Mock AutomazioniWidget e DettagliPanel
        mock_automazioni = MagicMock()
        real_main_window.navigation_controller.get_panel.return_value = mock_automazioni

        mock_panel = MagicMock()
        real_main_window.dettagli_panel = mock_panel

        # Mock lazy import
        mocker.patch("src.gui.widgets.automazioni_widget.AutomazioniWidget", return_value=mock_automazioni)
        # Poiché isinstance fallirebbe con MagicMock reale, patchiamo anche isinstance se possibile o usiamo un trucco
        # In questo caso, forziamo il codice a procedere bypassando il check di tipo se necessario

        with patch("src.gui.main_window.controllers.workflow_controller.isinstance", return_value=True):
            ctrl.run_dettagli_oda_update()

        assert mock_automazioni.set_active_tab.called
        qtbot.wait(200)
        assert mock_panel.run_externally.called
