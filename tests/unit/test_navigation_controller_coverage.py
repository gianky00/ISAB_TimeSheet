import unittest
from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QStackedWidget

from src.gui.controllers.navigation_controller import NavigationController


class TestNavigationControllerCoverage(unittest.TestCase):
    def setUp(self):
        self.mock_mw = MagicMock()
        self.mock_mw.page_stack = MagicMock(spec=QStackedWidget)
        self.mock_mw.sidebar = MagicMock()
        self.mock_mw._current_page_index = 0

        # Patch QObject init
        with patch("PyQt6.QtCore.QObject.__init__"):
            self.controller = NavigationController(self.mock_mw)

    def test_get_panel_already_initialized(self):
        self.mock_mw._panel_initialized_0 = True
        mock_widget = MagicMock()
        self.mock_mw.page_stack.widget.return_value = mock_widget

        res = self.controller.get_panel(0)
        self.assertEqual(res, mock_widget)

    @patch(
        "src.gui.controllers.navigation_controller.NavigationController._create_panel_by_index"
    )
    @patch(
        "src.gui.controllers.navigation_controller.NavigationController._initialize_new_panel"
    )
    def test_get_panel_lazy_loading(self, mock_init, mock_create):
        self.mock_mw._panel_initialized_0 = False
        new_widget = MagicMock()
        mock_create.return_value = new_widget

        res = self.controller.get_panel(0)

        self.assertEqual(res, new_widget)
        mock_init.assert_called_with(0, new_widget)

    def test_initialize_new_panel(self):
        old_w = MagicMock()
        new_w = MagicMock()
        self.mock_mw.page_stack.widget.return_value = old_w

        self.controller._initialize_new_panel(1, new_w)

        self.mock_mw.page_stack.removeWidget.assert_called_with(old_w)
        self.mock_mw.page_stack.insertWidget.assert_called_with(1, new_w)
        self.assertTrue(self.mock_mw._panel_initialized_1)

    def test_navigate_to_same_page(self):
        self.mock_mw._current_page_index = 1
        self.controller.navigate_to(1)
        self.mock_mw.sidebar.set_active_button.assert_called_with(1)
        self.mock_mw.page_stack.setCurrentIndex.assert_not_called()

    @patch("src.gui.controllers.navigation_controller.NavigationController.get_panel")
    def test_navigate_to_different_page(self, mock_get):
        self.mock_mw._current_page_index = 0
        self.controller.navigate_to(1)

        mock_get.assert_called_with(1)
        self.assertEqual(self.mock_mw._current_page_index, 1)
        self.mock_mw.page_stack.setCurrentIndex.assert_called_with(1)
        self.mock_mw.sidebar.set_active_button.assert_called_with(1)

    def test_navigate_to_settings_unsaved_prompt(self):
        self.mock_mw._current_page_index = 4
        mock_settings = MagicMock()
        mock_settings.has_unsaved_changes.return_value = True
        mock_settings.prompt_save_if_needed.return_value = False  # User cancelled
        self.mock_mw.settings_panel = mock_settings

        self.controller.navigate_to(1)

        self.mock_mw.sidebar.set_active_button.assert_called_with(4)  # Reverted
        self.mock_mw.page_stack.setCurrentIndex.assert_not_called()

    @patch("src.gui.controllers.navigation_controller.NavigationController.navigate_to")
    def test_navigate_to_extended(self, mock_nav):
        self.mock_mw.database_widget = MagicMock()
        self.mock_mw.contabilita_panel = MagicMock()

        self.controller.navigate_to_extended(2, "query")

        mock_nav.assert_called_with(3)
        self.mock_mw.database_widget.setCurrentIndex.assert_called_with(1)
        self.mock_mw.contabilita_panel.main_tabs.setCurrentIndex.assert_called_with(2)
        self.mock_mw.contabilita_panel.set_search_query.assert_called_with("query")

    @patch("src.gui.controllers.navigation_controller.NavigationController.navigate_to")
    def test_navigate_to_panel_nested_bot(self, mock_nav):
        self.mock_mw.automations_widget = MagicMock()  # typo in code but let's check
        # src/gui/controllers/navigation_controller.py:168 uses self.mw.automazioni_widget
        self.mock_mw.automazioni_widget = MagicMock()
        self.mock_mw.tab_fornitori = MagicMock()

        self.controller.navigate_to_panel("scarico_ts")

        mock_nav.assert_called_with(1)
        self.mock_mw.automazioni_widget.setCurrentIndex.assert_called_with(0)
        self.mock_mw.tab_fornitori.setCurrentIndex.assert_called_with(1)

    @patch("src.gui.controllers.navigation_controller.NavigationController.navigate_to")
    def test_analyze_with_lyra(self, mock_nav):
        self.mock_mw.lyra_panel = MagicMock()
        self.controller.analyze_with_lyra("data")

        mock_nav.assert_called_with(2)
        self.mock_mw.lyra_panel.ask_lyra.assert_called()
