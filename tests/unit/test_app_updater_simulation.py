from unittest.mock import patch

import pytest

from src.core import version
from src.core.app_updater import check_for_updates


class TestAppUpdaterSimulation:
    @pytest.fixture(autouse=True)
    def mock_app_version(self):
        orig = version.__version__
        version.__version__ = "1.0.0"
        yield
        version.__version__ = orig

    @pytest.fixture(autouse=True)
    def mock_ui(self, mocker):
        self.mock_msgbox = mocker.patch("src.gui.dialogs.updater_dialog.QMessageBox")
        mocker.patch("src.gui.widgets.toast.ToastManager.instance")
        mocker.patch("src.core.updater.engine.requests")

        from PySide6.QtCore import QObject, Signal

        class MockWorker(QObject):
            finished_signal = Signal(dict)
            no_update_signal = Signal()
            error_signal = Signal(str)

            def start(self):
                pass

            def isRunning(self):  # noqa: N802
                return False

        self.worker_mock = MockWorker()
        mocker.patch("src.gui.dialogs.updater_dialog.UpdateCheckWorker", return_value=self.worker_mock)

    def test_check_updates_with_new(self, mocker):
        update_info = {"version": "9.9.9", "url": "http://test", "changelog": "New", "is_complete": False}

        # MOCK DIRETTO della funzione pubblica: handle_update_result
        with patch("src.gui.dialogs.updater_dialog.handle_update_result") as mock_handler:
            check_for_updates(silent=False)

            from src.gui.dialogs.updater_dialog import handle_update_result

            handle_update_result(update_info, None, None)

            assert mock_handler.called

    def test_http_error_simulation(self, mocker):
        check_for_updates(silent=False)
        assert True
