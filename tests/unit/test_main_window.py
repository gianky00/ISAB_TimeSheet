from unittest.mock import patch

import pytest

from src.gui.main_window.main import MainWindow
from src.gui.main_window.page_index import PageIndex


class TestMainWindow:
    @pytest.fixture
    def app(self, qapp):
        return qapp

    @patch("src.gui.main_window.main.ServiceController")
    @patch("src.gui.main_window.main.LyraSentinel")
    @patch("src.gui.main_window.main.config_manager.load_config")
    @patch("src.gui.main_window.main.apply_theme")
    def test_init(self, mock_theme, mock_conf, mock_sentinel, mock_service, app, qtbot):
        mock_conf.return_value = {}

        window = MainWindow()
        qtbot.addWidget(window)

        assert "SyncroJob" in window.windowTitle()
        assert window.page_stack.count() >= 6
        assert window.sidebar.btn_home.isChecked()

    def test_navigation(self, app, qtbot):
        # Mock internal components to avoid side effects
        with (
            patch("src.gui.main_window.main.ServiceController"),
            patch("src.gui.main_window.main.LyraSentinel"),
            patch(
                "src.gui.panels.contabilita_panel.ContabilitaManager"
            ) as mock_manager,
            patch(
                "src.gui.main_window.main.config_manager.load_config", return_value={}
            ),
        ):
            mock_manager.get_available_years.return_value = []
            mock_manager.get_year_stats.return_value = {
                "total_prev": 0.0,
                "total_ore": 0.0,
                "count_total": 0,
                "status_counts": {},
                "top_commesse": [],
                "ore_dirette": 0.0,
                "ore_indirette": 0.0,
            }

            window = MainWindow()
            qtbot.addWidget(window)

            # Click Automazioni
            window.sidebar.btn_automazioni.click()
            assert window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI
            assert window.sidebar.btn_automazioni.isChecked()

            # Click Database (Dipendenti in refactored version)
            window.sidebar.btn_database.click()
            assert window.page_stack.currentIndex() == PageIndex.TIMBRATURE
            assert window.sidebar.btn_database.isChecked()

    def test_navigate_to_panel(self, app, qtbot):
        with (
            patch("src.gui.main_window.main.ServiceController"),
            patch("src.gui.main_window.main.LyraSentinel"),
            patch(
                "src.gui.panels.contabilita_panel.ContabilitaManager"
            ) as mock_manager,
            patch(
                "src.gui.main_window.main.config_manager.load_config", return_value={}
            ),
        ):
            mock_manager.get_available_years.return_value = []
            mock_manager.get_year_stats.return_value = {
                "total_prev": 0.0,
                "total_ore": 0.0,
                "count_total": 0,
                "status_counts": {},
                "top_commesse": [],
                "ore_dirette": 0.0,
                "ore_indirette": 0.0,
            }

            window = MainWindow()
            qtbot.addWidget(window)

            window.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)

            # Test deep link navigation
            window.navigation_controller.navigate_to_panel(
                "timbrature"
            )  # Should go to Automazioni -> Timbrature (Tab 2)
            assert window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI

            # Automazioni panel is at index 1
            automazioni_panel = window.navigation_controller.get_panel(
                PageIndex.AUTOMAZIONI
            )
            # Timbrature is at index 2 in Portale Fornitori (tab 0 of Automazioni)
            portale_fornitori_tab = automazioni_panel.widget(0)
            assert portale_fornitori_tab.currentIndex() == 2
