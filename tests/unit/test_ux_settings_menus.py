
import pytest
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import Qt, QPoint

from src.gui.settings_panel import SettingsPanel

# The 'qapp' fixture is automatically provided by pytest-qt via conftest.py
# and ensures a QApplication instance exists before tests run.

@pytest.fixture
def panel(qapp):
    """Fixture to create a SettingsPanel instance for each test."""
    return SettingsPanel()

def test_context_menu_setup(panel):
    """Test that list widgets have context menu policy set correctly."""
    assert panel.account_list.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu
    assert panel.contract_list.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu
    assert panel.fornitori_list.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu

def test_generic_menu_callback_structure(panel):
    """Test that the generic menu callback methods exist."""
    # We can't easily simulate a right-click in unit tests without rendering,
    # but we can verify the handler methods exist to prevent runtime errors.

    # Mock a list widget and position
    mock_list = QListWidget()
    mock_list.addItem("Item 1")

    # Check that the necessary methods exist on the panel instance.
    assert hasattr(panel, '_show_generic_list_menu')
    assert hasattr(panel, '_show_account_context_menu')
