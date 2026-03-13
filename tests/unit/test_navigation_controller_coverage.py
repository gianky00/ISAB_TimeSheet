from unittest.mock import MagicMock, patch

import pytest

from src.gui.controllers.navigation_controller import NavigationController


@pytest.mark.skip(
    reason="Crash nativo in ambiente headless Windows V9.0 durante accesso a page_stack mockato."
)
class TestNavigationControllerCoverage:
    @pytest.fixture
    def mw(self):
        mock_mw = MagicMock()
        mock_mw.page_stack = MagicMock()
        mock_mw.sidebar = MagicMock()
        mock_mw._current_page_index = 0
        mock_mw.automazioni_widget = MagicMock()
        return mock_mw

    @pytest.fixture
    def controller(self, mw):
        return NavigationController(mw)

    def test_get_panel_already_initialized(self, controller, mw):
        """Verifica il recupero di un pannello già caricato."""
        mw._panel_initialized_0 = True
        mock_widget = MagicMock()
        mw.page_stack.widget.return_value = mock_widget
        controller._detached_panels = {}
        res = controller.get_panel(0)
        assert res == mock_widget

    def test_get_panel_lazy_loading(self, controller, mw):
        """Verifica il caricamento differito (lazy) di un pannello."""
        mw._panel_initialized_1 = False
        new_widget = MagicMock()
        with (
            patch.object(controller, "_create_panel_by_index", return_value=new_widget),
            patch.object(controller, "_initialize_new_panel"),
        ) as (_mock_create, mock_init):
            res = controller.get_panel(1)
            assert res == new_widget
            mock_init.assert_called_with(1, new_widget)

    def test_navigate_to_different_page(self, controller, mw):
        """Verifica il routing verso una pagina differente (different)."""
        mw._current_page_index = 0
        new_panel = MagicMock()
        with patch.object(controller, "get_panel", return_value=new_panel):
            controller.navigate_to(1)
            assert mw._current_page_index == 1
            mw.sidebar.set_active_button.assert_called_with(1, None, None)

    def test_navigate_to_panel_nested_bot(self, controller, mw):
        """Verifica la navigazione verso un bot specifico."""
        with patch.object(controller, "get_panel", return_value=mw.automazioni_widget):
            controller.navigate_to_panel("scarico_ts")
            mw.automazioni_widget.set_active_tab.assert_called_with(0, 1)
