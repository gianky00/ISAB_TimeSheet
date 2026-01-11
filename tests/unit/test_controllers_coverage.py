import pytest
from unittest.mock import MagicMock, patch
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController

class TestControllersDeep:
    def test_navigation_deep_links(self):
        mock_stack = MagicMock()
        mock_sidebar = MagicMock()
        nav = NavigationController(mock_stack, mock_sidebar)
        
        # Test deep link to 'timbrature'
        with patch.object(nav, "switch_page") as mock_switch:
            nav.navigate_to_deep_link("timbrature")
            mock_switch.assert_called()

    def test_search_routing(self):
        mock_nav = MagicMock()
        search = SearchController(mock_nav)
        
        # Test routing an ODA search
        with patch("src.core.contabilita_manager.ContabilitaManager.search_oda", return_value=[{"codice": "123"}]):
            results = search.perform_search("123456")
            assert "oda" in results
            assert len(results["oda"]) > 0
            
    def test_search_routing_no_results(self):
        mock_nav = MagicMock()
        search = SearchController(mock_nav)
        with patch("src.core.contabilita_manager.ContabilitaManager.search_oda", return_value=[]), \
             patch("src.core.contabilita_manager.ContabilitaManager.search_extended", return_value={}):
            results = search.perform_search("nonexistent")
            assert all(len(v) == 0 for v in results.values())
