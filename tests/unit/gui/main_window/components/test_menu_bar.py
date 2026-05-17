from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QObject

from src.gui.main_window.components.menu_bar import MenuBarComponent


@pytest.fixture
def mock_mainwindow():
    mw = MagicMock()
    return mw


def test_menu_bar_initialization(mock_mainwindow):
    # Dobbiamo evitare che _setup_shortcuts acceda a widget non inizializzati o fallisca
    # Mocking anche QShortcut a livello di modulo
    with pytest.MonkeyPatch.context() as m:
        m.setattr("src.gui.main_window.components.menu_bar.QShortcut", MagicMock())

        # Inizializziamo il componente senza far fallire il setup
        parent_obj = QObject()
        menu = MenuBarComponent(parent_obj)
        menu.main_window = mock_mainwindow
        assert menu.main_window == mock_mainwindow


def test_open_bug_report_dialog(mock_mainwindow):
    parent_obj = QObject()
    with pytest.MonkeyPatch.context() as m:
        m.setattr("src.gui.main_window.components.menu_bar.QShortcut", MagicMock())
        m.setattr("src.gui.main_window.components.menu_bar.BugReportDialog", MagicMock())

        menu = MenuBarComponent(parent_obj)
        menu.main_window = mock_mainwindow
        menu.open_bug_report_dialog()

        assert menu._bug_dialog is not None
        menu._bug_dialog.show.assert_called_once()
