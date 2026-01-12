
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
        self.automazioni_widget = MagicMock()
        self.tab_fornitori = MagicMock()
        self.tab_safework = MagicMock()
        self.global_status_card = MagicMock()
        self.sidebar = MagicMock()
        self._current_page_index = 0
        self.lyra_panel = MagicMock()
        self.database_widget = MagicMock()
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

        mocker.patch("src.gui.controllers.bot_controller.os.path.exists", return_value=True)

        ctrl._handle_bot_results("scarico_pdl", ["/pdl.pdf"])
        mock_telegram.send_document_sync.assert_called_once()

    def test_navigation_controller_simple_logic(self, mw, mocker):
        """Verifica logica di navigazione senza caricare pannelli reali."""
        ctrl = NavigationController(mw)

        # Mock get_panel per evitare import reali
        mocker.patch.object(ctrl, "get_panel", return_value=QWidget())

        ctrl.navigate_to(1)

        assert mw._current_page_index == 1
        mw.page_stack.setCurrentIndex.assert_called_with(1)
        mw.sidebar.set_active_button.assert_called_with(1)

    def test_navigation_controller_settings_dirty_check(self, mw, mocker):
        """Verifica blocco navigazione se impostazioni non salvate."""
        ctrl = NavigationController(mw)
        mw._current_page_index = 4

        mw.settings_panel = MagicMock()
        mw.settings_panel.has_unsaved_changes.return_value = True
        mw.settings_panel.prompt_save_if_needed.return_value = False

        ctrl.navigate_to(0)

        # Deve essere rimasto sulla pagina 4
        mw.page_stack.setCurrentIndex.assert_not_called()
        mw.sidebar.set_active_button.assert_called_with(4)

    def test_bot_controller_panel_status_sync(self, mw, mocker):
        """Verifica sincronizzazione stato globale."""
        ctrl = BotController(mw, MagicMock())
        mock_panel = MagicMock()

        mocker.patch.object(ctrl, "_get_active_bot_panel", return_value=mock_panel)
        mocker.patch.object(ctrl, "sender", return_value=mock_panel)

        ctrl._on_panel_status_changed("RUNNING", "Test")
        mw.global_status_card.setStatus.assert_called_with("RUNNING", "Test")

    def test_search_controller_routing(self, mw, mocker):
        """Verifica che la ricerca OdA inoltri i risultati correttamente."""
        ctrl = SearchController(mw)
        mock_menu = MagicMock()

        mocker.patch("src.core.contabilita_manager.ContabilitaManager.search_oda",
                     return_value=[{"codice_oda": "123", "descrizione": "D"}])

        count = ctrl._search_oda("123", mock_menu)
        assert count == 1
        assert mock_menu.addAction.called
