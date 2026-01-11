import pytest
from PyQt6.QtWidgets import QWidget
from src.gui.accessibility import make_accessible, setup_tab_order, KeyboardShortcuts

class TestAccessibilitySimple:
    def test_make_accessible(self, qapp):
        widget = QWidget()
        make_accessible(widget, "Test Widget", "Description")
        assert widget.accessibleName() == "Test Widget"
        assert widget.accessibleDescription() == "Description"

    def test_setup_tab_order(self, qapp):
        w1, w2 = QWidget(), QWidget()
        setup_tab_order([w1, w2])
        # Success if it doesn't crash (standard Qt API)
        assert True

    def test_keyboard_shortcuts_def(self):
        assert "Ctrl+S" in KeyboardShortcuts.SHORTCUTS
        # Setup call should not crash
        KeyboardShortcuts.setup(MagicMock())

from unittest.mock import MagicMock