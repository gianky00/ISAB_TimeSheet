from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController


class MockMainWindow(QObject):
    """Mock leggero che simula l'interfaccia di MainWindow senza caricare Qt reale."""

    def __init__(self):
        super().__init__()
        self.page_stack = MagicMock()
        # Aggiungiamo slide_to_index che è usato in V9.0
        self.page_stack.slide_to_index = MagicMock()

        self.automazioni_widget = MagicMock()
        self.sidebar = MagicMock()
        self._current_page_index = 0
        self.lyra_panel = MagicMock()
        self.scarico_ore_panel = MagicMock()
        self.timbrature_db_panel = MagicMock()
        self.contabilita_panel = MagicMock()


class TestControllersCoverage:
    @pytest.fixture
    def mw(self, qapp):
        return MockMainWindow()

    def test_bot_controller_handle_results(self, mw, mocker):
        """Verifica inoltro risultati bot a Telegram."""
        mock_telegram = MagicMock()
        ctrl = BotController(mw, mock_telegram)
        mocker.patch("src.gui.controllers.bot_controller.Path.exists", return_value=True)
        ctrl._handle_bot_results("scarico_pdl", ["/pdl.pdf"])
        mock_telegram.send_document_sync.assert_called_once()

    def test_navigation_controller_simple_logic(self, mw, mocker):
        """Verifica logica di navigazione senza caricare pannelli reali."""
        ctrl = NavigationController(mw)
        mocker.patch.object(ctrl, "get_panel", return_value=QWidget())

        ctrl.navigate_to(1)

        assert mw._current_page_index == 1
        # In V9.0 usa slide_to_index se presente
        mw.page_stack.slide_to_index.assert_called_with(1)
        # La sidebar ora riceve (index, sub_index, bot_index)
        mw.sidebar.set_active_button.assert_called_with(1, None, None)

    def test_navigation_controller_settings_dirty_check(self, mw, mocker):
        """Verifica blocco navigazione se impostazioni non salvate."""
        ctrl = NavigationController(mw)
        mw._current_page_index = 7
        mw.settings_panel = MagicMock()
        mw.settings_panel.has_unsaved_changes.return_value = True
        mw.settings_panel.prompt_save_if_needed.return_value = False

        ctrl.navigate_to(0)
        mw.page_stack.slide_to_index.assert_not_called()
        mw.sidebar.set_active_button.assert_called_with(7)

    def test_search_controller_routing(self, mw, mocker):
        """Verifica che la ricerca OdA inoltri i risultati correttamente."""
        ctrl = SearchController(mw)
        mock_menu = MagicMock()

        matches = [{"codice_oda": "123", "descrizione": "D"}]
        count = ctrl._add_oda_matches(matches, mock_menu)
        assert count == 1
        assert mock_menu.addAction.called
