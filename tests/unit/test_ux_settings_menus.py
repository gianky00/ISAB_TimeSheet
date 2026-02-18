import pytest
from PyQt6.QtCore import Qt

from src.gui.panels.settings.main_panel import SettingsPanel

# The 'qapp' fixture is automatically provided by pytest-qt via conftest.py
# and ensures a QApplication instance exists before tests run.


@pytest.fixture
def panel(qapp, mocker):
    """Fixture to create a SettingsPanel instance for each test."""
    # Mock refresh_models to avoid background thread starting during tests
    mocker.patch("src.gui.panels.settings.pages.general_page.GeneralPage.refresh_models")
    return SettingsPanel()


def test_context_menu_setup(panel):
    """Test that list widgets have context menu policy set correctly."""
    lists_page = panel.config_tab.lists_page
    assert lists_page.account_list.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu
    assert lists_page.contract_list.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu
    assert lists_page.fornitori_list.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu


def test_generic_menu_callback_structure(panel):
    """Test that the generic menu callback methods exist."""
    lists_page = panel.config_tab.lists_page

    # Check that the necessary methods exist on the lists_page instance.
    assert hasattr(lists_page, "_show_generic_menu")
    assert hasattr(lists_page, "_show_account_menu")
