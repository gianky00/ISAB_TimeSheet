from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QStackedWidget, QWidget

from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController


class MockMainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.sidebar = MagicMock()
        self.global_search = MagicMock()
        self.statusBar = MagicMock()

    def _show_update_banner(self, info):
        pass


class TestControllersCoverage:
    @pytest.fixture
    def mw(self, qapp):
        return MockMainWindow()

    def test_bot_controller_handle_results(self, mw, mocker):
        mock_telegram = MagicMock()
        ctrl = BotController(mw, mock_telegram)
        mocker.patch("src.gui.controllers.bot_controller.Path.exists", return_value=True)
        ctrl._handle_bot_results("scarico_pdl", ["/pdl.pdf"])
        mock_telegram.send_document_sync.assert_called_once()

    def test_navigation_controller_simple_logic(self, mw, mocker):
        # Patch PanelFactory per tornare QWidget reali per ogni chiamata
        with patch("src.gui.controllers.navigation_controller.PanelFactory") as mock_factory_class:
            mock_factory = mock_factory_class.return_value
            # side_effect con lambda che crea un nuovo QWidget ad ogni chiamata
            mock_factory.get_panel.side_effect = lambda idx: QWidget()

            ctrl = NavigationController(mw)
            ctrl.navigate_to(1)

            # Index 1
            assert mw.stacked_widget.currentIndex() == 1

    def test_search_controller_routing(self, mw, mocker):
        ctrl = SearchController(mw)
        mocker.patch.object(ctrl.search_timer, "start")
        ctrl.perform_search("test query")
        assert ctrl._last_query == "test query"

    def test_search_execution(self, mw, mocker):
        ctrl = SearchController(mw)
        ctrl._last_query = "tester"
        with patch("src.gui.controllers.search_controller.SearchWorker") as mock_worker_class:
            ctrl._execute_async_search()
            assert mock_worker_class.called
