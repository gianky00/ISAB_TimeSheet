from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QWidget

from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController


class TestControllersDeep:
    def test_navigation_panel_routing(self, qapp):
        # NavigationController expects a QObject (main_window)
        mock_mw = QWidget()
        mock_mw.page_stack = MagicMock()
        mock_mw.sidebar = MagicMock()
        mock_mw.automazioni_widget = MagicMock()
        mock_mw.tab_fornitori = MagicMock()
        mock_mw.tab_safework = MagicMock()
        mock_mw._current_page_index = -1

        nav = NavigationController(mock_mw)

        with patch.object(nav, "navigate_to") as mock_nav:
            nav.navigate_to_panel("timbrature")
            mock_nav.assert_called_with(1)
            mock_mw.automazioni_widget.setCurrentIndex.assert_called_with(0)
            mock_mw.tab_fornitori.setCurrentIndex.assert_called_with(2)

    def test_search_routing_logic(self, qapp):
        mock_mw = QWidget()
        mock_mw.global_search = MagicMock()

        # SearchController(main_window)
        search = SearchController(mock_mw)

        with patch("src.gui.controllers.search_controller.QMenu") as mock_menu:
            with patch("src.core.contabilita_manager.ContabilitaManager.search_oda", return_value=[{"codice_oda": "123", "descrizione": "test"}]):
                search.perform_search("123456")
                assert mock_menu.called

    def test_search_routing_no_results(self, qapp):
        mock_mw = QWidget()
        search = SearchController(mock_mw)

        with patch("src.core.contabilita_manager.ContabilitaManager.search_oda", return_value=[]):
            search.perform_search("x")
            # Too short, should return early
