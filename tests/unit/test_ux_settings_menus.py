
import sys
import unittest
from PyQt6.QtWidgets import QApplication, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QPoint

# Use a dummy QApplication
app = QApplication(sys.argv)

from src.gui.settings_panel import SettingsPanel

class TestSettingsContextMenus(unittest.TestCase):
    def test_context_menu_setup(self):
        """Test that list widgets have context menu policy set correctly."""
        panel = SettingsPanel()
        
        # Check Account List
        self.assertEqual(panel.account_list.contextMenuPolicy(), Qt.ContextMenuPolicy.CustomContextMenu)
        
        # Check Contract List
        self.assertEqual(panel.contract_list.contextMenuPolicy(), Qt.ContextMenuPolicy.CustomContextMenu)
        
        # Check Fornitori List
        self.assertEqual(panel.fornitori_list.contextMenuPolicy(), Qt.ContextMenuPolicy.CustomContextMenu)

    def test_generic_menu_callback(self):
        """Test that the generic menu callback structure is valid."""
        panel = SettingsPanel()
        
        # We can't simulate a right click easily in unit tests without rendering,
        # but we can call the method directly to ensure no runtime errors.
        
        # Mock a list widget and position
        mock_list = QListWidget()
        mock_list.addItem("Item 1")
        mock_pos = QPoint(10, 10)
        
        # Define dummy callbacks
        def add(): pass
        def edit(): pass
        def remove(): pass
        
        # Call the method (it will try to exec menu, which might block or fail in headless without correct QPoint mapping)
        # However, checking existence is a good first step.
        self.assertTrue(hasattr(panel, '_show_generic_list_menu'))
        self.assertTrue(hasattr(panel, '_show_account_context_menu'))

if __name__ == '__main__':
    unittest.main()
