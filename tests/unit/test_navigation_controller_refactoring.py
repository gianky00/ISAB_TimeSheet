import pytest
from unittest.mock import MagicMock, patch
from src.gui.controllers.navigation_controller import NavigationController

@pytest.fixture
def mock_mw():
    mw = MagicMock()
    mw.page_stack = MagicMock()
    mw.sidebar = MagicMock()
    mw._current_page_index = 0
    mw.lyra_panel = MagicMock()
    mw.automazioni_widget = MagicMock()
    return mw

@pytest.fixture
def controller(mock_mw):
    return NavigationController(mock_mw)

@pytest.mark.skip(reason="Crash nativo in ambiente headless Windows V9.0 durante coordinamento grafico navigazione.")
class TestNavigationControllerRefactoring:
    def test_get_panel_already_initialized(self, controller, mock_mw):
        """Verifica il recupero di un pannello già caricato (Refactoring)."""
        setattr(mock_mw, "_panel_initialized_0", True)
        mock_widget = MagicMock()
        mock_mw.page_stack.widget.return_value = mock_widget
        controller._detached_panels = {}
        res = controller.get_panel(0)
        assert res == mock_widget

    def test_navigate_to_page_basic(self, controller, mock_mw):
        """Verifica la navigazione di base tra le pagine."""
        mock_mw._current_page_index = 0
        new_panel = MagicMock()
        with patch.object(controller, "get_panel", return_value=new_panel):
            controller.navigate_to(1)
            assert mock_mw._current_page_index == 1
            mock_mw.sidebar.set_active_button.assert_called_with(1, None, None)

    def test_navigate_to_panel_deep_linking(self, controller, mock_mw):
        """Verifica il deep linking verso un bot specifico (Refactoring)."""
        with patch.object(controller, "get_panel", return_value=mock_mw.automazioni_widget):
            controller.navigate_to_panel("timbrature")
            mock_mw.automazioni_widget.set_active_tab.assert_called_with(0, 2)

    def test_analyze_with_lyra_integration(self, controller, mock_mw):
        """Verifica l'inoltro a Lyra AI."""
        with patch.object(controller, "get_panel", return_value=mock_mw.lyra_panel):
            controller.analyze_with_lyra("data")
            mock_mw.lyra_panel.ask_lyra.assert_called()
