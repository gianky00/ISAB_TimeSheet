import os
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtWidgets import QWidget

from src.gui.main_window.main import MainWindow
from src.gui.main_window.page_index import PageIndex

# Salta i test se siamo in modalità offscreen (causa deadlock su alcuni sistemi Windows)
SKIP_UI_TESTS = os.environ.get("QT_QPA_PLATFORM") == "offscreen"


@pytest.mark.skipif(
    SKIP_UI_TESTS, reason="I test MainWindow causano deadlock in modalità offscreen su Windows"
)
class TestMainWindow:
    @pytest.fixture(autouse=True)
    def mock_all_core(self):
        """Mock totale di tutti i servizi che potrebbero avviare thread o fare IO."""
        with (
            patch("src.gui.main_window.main.AuditManager"),
            patch("src.gui.main_window.main.TelegramService"),
            patch("src.gui.main_window.main.run_update"),
            patch("src.gui.main_window.main.perform_auto_update"),
            patch("src.gui.main_window.main.config_manager.load_config", return_value={}),
            patch("src.gui.main_window.main.apply_theme"),
            patch("src.gui.main_window.main.QTimer"),
            patch("src.gui.main_window.main.ServiceController"),
            patch("src.gui.main_window.main.WorkflowController"),
            patch("src.gui.main_window.main.MonitoringController"),
            patch("src.application.services.oda.oda_controller.ODAController"),
            patch("src.application.services.dipendenti.anagrafica_controller.AnagraficaController"),
            patch("src.application.services.pdl.pdl_controller.PDLController"),
            patch("src.application.services.contabilita.scarico_ore.controller.ScaricoOreController"),
            patch("src.application.services.contabilita.consuntivo.consuntivo_controller.ConsuntivoController"),
            patch("src.gui.main_window.main.QMainWindow.show"),  # Impedisce show() reale
        ):
            yield

    def test_init_logic(self, qapp):
        """Verifica l'inizializzazione corretta dello stato iniziale (Senza QtBot)."""
        window = MainWindow()
        assert "SyncroJob" in window.windowTitle()
        assert window.page_stack.count() >= len(PageIndex)
        window.close()

    def test_navigation_logic(self, qapp):
        """Verifica la navigazione tra le pagine (Senza QtBot)."""
        with patch(
            "src.gui.controllers.navigation_controller.NavigationController._create_panel_instance"
        ) as mock_create:
            mock_create.return_value = QWidget()
            window = MainWindow()

            # Navigazione verso Automazioni
            window.navigation_controller.navigate_to(PageIndex.AUTOMAZIONI)
            assert window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI
            window.close()

    def test_deep_link_logic(self, qapp):
        """Verifica che i deep link (navigate_to_panel) richiamino i pannelli corretti (Senza QtBot)."""
        with patch(
            "src.gui.controllers.navigation_controller.NavigationController._create_panel_instance"
        ) as mock_create:
            mock_panel = QWidget()
            mock_panel.set_current_tab = MagicMock()
            mock_create.return_value = mock_panel

            window = MainWindow()

            # 'timbrature' -> Fornitori (0), Bot Index (2)
            window.navigation_controller.navigate_to_panel("timbrature")

            assert window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI
            mock_panel.set_current_tab.assert_called_with(0, 2)
            window.close()
