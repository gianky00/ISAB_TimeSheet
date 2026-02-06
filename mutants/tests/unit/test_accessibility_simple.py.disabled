from unittest.mock import MagicMock, patch

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from src.gui.accessibility import KeyboardShortcuts, make_accessible, setup_tab_order


class TestAccessibilitySimple:
    def test_make_accessible(self):
        widget = MagicMock(spec=QWidget)
        # Mock focusPolicy to return NoFocus by default
        widget.focusPolicy.return_value = Qt.FocusPolicy.NoFocus

        make_accessible(widget, "Test Widget", "Description")

        widget.setAccessibleName.assert_called_with("Test Widget")
        widget.setAccessibleDescription.assert_called_with("Description")
        widget.setFocusPolicy.assert_called_with(Qt.FocusPolicy.TabFocus)

    def test_setup_tab_order(self):
        w1, w2 = MagicMock(spec=QWidget), MagicMock(spec=QWidget)
        with patch("src.gui.accessibility.QWidget.setTabOrder") as mock_set_tab:
            setup_tab_order([w1, w2])
            mock_set_tab.assert_called_once_with(w1, w2)

    def test_keyboard_shortcuts_def(self):
        assert "Ctrl+S" in KeyboardShortcuts.SHORTCUTS
        # Setup call should not crash
        KeyboardShortcuts.setup(MagicMock())
