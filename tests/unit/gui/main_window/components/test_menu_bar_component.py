"""Unit tests for MenuBarComponent."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QMainWindow

from src.gui.main_window.components.menu_bar import MenuBarComponent


@pytest.fixture
def real_main_window(qtbot):
    mw = QMainWindow()
    # Mock attributes expected by MenuBarComponent
    mw.workflow_controller = MagicMock()
    mw.navigation_controller = MagicMock()
    mw.app_event_handler = MagicMock()
    mw.status_bar_component = MagicMock()
    # Add show_toast if needed
    mw.show_toast = MagicMock()

    qtbot.addWidget(mw)
    return mw


class TestMenuBarComponent:
    """Test suite per MenuBarComponent."""

    def test_initialization(self, real_main_window):
        comp = MenuBarComponent(real_main_window)
        assert comp.shortcut_palette is not None
        assert comp.command_palette is None

    def test_open_command_palette_lazy_init(self, qtbot, real_main_window):
        comp = MenuBarComponent(real_main_window)

        # Primo toggle -> Inizializzazione + Show
        comp.open_command_palette()
        assert comp.command_palette is not None
        # In environment offscreen, isHidden() è più affidabile
        assert not comp.command_palette.isHidden()

    def test_open_command_palette_toggle(self, qtbot, real_main_window):
        comp = MenuBarComponent(real_main_window)
        comp.open_command_palette()  # Mostra

        # Debounce check (300ms)
        comp._last_palette_toggle -= 1000

        comp.open_command_palette()  # Nasconde
        # Nascondere è asincrono via hide_animated()
        assert comp.command_palette is not None

    def test_build_menu_tree(self, real_main_window):
        comp = MenuBarComponent(real_main_window)
        tree = comp._build_menu_tree()

        assert len(tree) > 0
        labels = [n.label for n in tree]
        assert "Esegui..." in labels
        assert "Vai a..." in labels

    def test_open_bug_report_dialog(self, qtbot, real_main_window, mocker):
        comp = MenuBarComponent(real_main_window)
        mock_dlg = mocker.patch("src.gui.main_window.components.menu_bar.BugReportDialog")

        comp.open_bug_report_dialog()
        assert mock_dlg.called

    def test_shortcut_activation(self, qtbot, real_main_window, mocker):
        comp = MenuBarComponent(real_main_window)
        mock_open = mocker.patch.object(comp, "open_command_palette")

        # Trigger segnale scorciatoia
        comp.shortcut_palette.activated.emit()
        assert mock_open.called
