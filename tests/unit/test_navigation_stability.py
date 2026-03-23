"""
Tests for NavigationController stability.
"""

from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QStackedWidget, QWidget

from src.gui.controllers.navigation_controller import NavigationController


class MockMainWindow(QObject):
    """Vero QObject per evitare TypeError in NavigationController."""

    def __init__(self):  # noqa: ANN204
        super().__init__()
        self.page_stack = QStackedWidget()
        for _i in range(12):
            self.page_stack.addWidget(QWidget())
        self._current_page_index = 0
        self.sidebar = MagicMock()
        self._on_settings_saved = MagicMock()
        self._on_help_requested = MagicMock()


class TestNavigationStability:
    @pytest.fixture
    def mw(self, qtbot):  # noqa: ANN001
        return MockMainWindow()

    def test_lazy_loading_persistence(self, mw):  # noqa: ANN001
        """Verifica che il pannello venga creato una sola volta."""
        ctrl = NavigationController(mw)

        # Simula factory che ritorna un widget
        mock_panel = QWidget()
        with patch.object(ctrl, "_create_panel_by_index", return_value=mock_panel):
            # Prima chiamata: inizializza
            p1 = ctrl.get_panel(2)  # LYRA
            assert p1 is mock_panel
            assert mw._panel_initialized_2 is True

            # Seconda chiamata: ritorna dalla cache (non chiama factory)
            with patch.object(ctrl, "_create_panel_by_index") as mock_factory:
                p2 = ctrl.get_panel(2)
                assert p2 is p1
                assert not mock_factory.called

    def test_navigate_to_with_settings_unsaved(self, mw):  # noqa: ANN001
        """Verifica che la navigazione venga bloccata se ci sono modifiche non salvate in settings."""
        ctrl = NavigationController(mw)
        mw._current_page_index = 7  # SETTINGS

        mock_settings = MagicMock()
        mock_settings.has_unsaved_changes.return_value = True
        mock_settings.prompt_save_if_needed.return_value = False  # Utente annulla o nega salvataggio
        mw.settings_panel = mock_settings

        ctrl.navigate_to(0)  # Prova ad andare alla dashboard

        # Deve essere rimasto a 7
        assert mw._current_page_index == 7  # noqa: PLR2004
        mw.sidebar.set_active_button.assert_called_with(7)

    def test_handle_panel_error_resilience(self, mw):  # noqa: ANN001
        """Verifica che un errore in un pannello mostri un messaggio e non crashi il controller."""
        ctrl = NavigationController(mw)

        with (
            patch.object(ctrl, "_create_panel_by_index", side_effect=Exception("Panel Crash")),
            patch("PyQt6.QtWidgets.QMessageBox.critical") as mock_msg,
        ):
            p = ctrl.get_panel(1)
            assert mock_msg.called
            assert "Panel Crash" in str(mock_msg.call_args[0][2])
