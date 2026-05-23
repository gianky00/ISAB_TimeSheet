from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QObject


class MockMainWindow(QObject):
    """Sottoclasse reale di QObject per WorkflowController."""

    def __init__(self):
        super().__init__()
        self.timbrature_bot_panel = MagicMock()
        self.navigation_controller = MagicMock()
        self.scarico_ore_panel = MagicMock()
        # Mock minimal per evitare AttributeError senza spec rigido
        self.status_bar_component = MagicMock()

    def _show_update_banner(self, info):
        pass


class TestWorkflowController:
    @pytest.fixture
    def mw(self, qapp):
        return MockMainWindow()

    def test_workflow_controller_init(self, mw):
        from src.gui.main_window.controllers.workflow_controller import WorkflowController

        ctrl = WorkflowController(mw)
        assert ctrl.mw == mw

    def test_run_timbrature_bot(self, mw, mocker):
        from src.gui.main_window.controllers.workflow_controller import WorkflowController

        ctrl = WorkflowController(mw)

        with patch("src.gui.widgets.toast.ToastManager.instance") as mock_toast:
            ctrl.run_timbrature_bot("ieri")
            assert mw.timbrature_bot_panel.run_externally.called
            assert mock_toast().show.called

    def test_run_sync_dataease(self, mw):
        from src.gui.main_window.controllers.workflow_controller import WorkflowController

        ctrl = WorkflowController(mw)

        with patch("PySide6.QtCore.QTimer.singleShot", side_effect=lambda ms, fn: fn()):
            ctrl.run_sync_dataease()
            assert mw.navigation_controller.navigate_to.called
            assert mw.scarico_ore_panel._start_update.called
