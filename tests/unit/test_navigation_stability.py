"""
Tests for NavigationController stability.
Refactored for V9.0 architecture.
"""

from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QStackedWidget, QWidget

from src.gui.controllers.navigation_controller import NavigationController
from src.gui.main_window.page_index import PageIndex


class MockPanel(QWidget):
    """Sottoclasse di QWidget per distinguere i pannelli reali dai placeholder."""


class MockMainWindow(QObject):
    """Vero QObject per evitare TypeError in NavigationController."""

    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        # Inizializza lo stack con QWidget per matchare PageIndex
        for _ in range(len(PageIndex)):
            self.stacked_widget.addWidget(QWidget())

        self.sidebar = MagicMock()
        self._on_settings_saved = MagicMock()
        self._on_help_requested = MagicMock()


class TestNavigationStability:
    @pytest.fixture
    def mw(self, qtbot):
        return MockMainWindow()

    def test_lazy_loading_persistence(self, mw):
        """Verifica che il pannello venga creato una sola volta."""
        ctrl = NavigationController(mw)

        # Simula factory che ritorna un widget di tipo MockPanel
        mock_panel = MockPanel()
        with patch.object(ctrl.panel_factory, "create_panel", return_value=mock_panel):
            # Prima chiamata: inizializza (indice 1: AUTOMAZIONI)
            p1 = ctrl.get_panel(PageIndex.AUTOMAZIONI)
            assert p1 is mock_panel
            assert isinstance(p1, MockPanel)

            # Seconda chiamata: ritorna dalla cache (non chiama factory perché type(p1) is not QWidget)
            with patch.object(ctrl.panel_factory, "create_panel") as mock_factory:
                p2 = ctrl.get_panel(PageIndex.AUTOMAZIONI)
                assert p2 is p1
                assert not mock_factory.called

    def test_navigate_to_invalid_index(self, mw):
        """Verifica che la navigazione verso un indice non valido venga ignorata."""
        ctrl = NavigationController(mw)

        # Indice fuori range superiore
        ctrl.navigate_to(999)
        assert mw.stacked_widget.currentIndex() == 0

        # Indice negativo
        ctrl.navigate_to(-1)
        assert mw.stacked_widget.currentIndex() == 0

    def test_handle_panel_error_resilience(self, mw):
        """Verifica che un errore in un pannello mostri un messaggio e non crashi il controller."""
        ctrl = NavigationController(mw)

        with (
            patch.object(ctrl.panel_factory, "create_panel", side_effect=Exception("Panel Crash")),
            patch("src.gui.controllers.panel_factory.QMessageBox.critical") as mock_msg,
        ):
            # Tenta di caricare un pannello che crasha
            p = ctrl.get_panel(PageIndex.DASHBOARD)

            # Dovrebbe restituire il placeholder originale (QWidget) invece di None o crashare
            assert p is not None
            assert type(p) is QWidget
            assert not isinstance(p, MockPanel)
