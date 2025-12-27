"""
Utilities per accessibilità.
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

def make_accessible(widget: QWidget, name: str, description: str = "", role: str = None):
    """Rende un widget accessibile."""
    widget.setAccessibleName(name)
    if description:
        widget.setAccessibleDescription(description)

    # Assicura focus policy
    if widget.focusPolicy() == Qt.FocusPolicy.NoFocus:
        widget.setFocusPolicy(Qt.FocusPolicy.TabFocus)

def setup_tab_order(widgets: list[QWidget]):
    """Configura ordine di tabulazione."""
    for i in range(len(widgets) - 1):
        QWidget.setTabOrder(widgets[i], widgets[i + 1])

class KeyboardShortcuts:
    """Gestisce shortcut tastiera globali."""

    SHORTCUTS = {
        "Ctrl+S": "save",
        "Ctrl+R": "refresh",
        "Ctrl+Q": "quit",
        "F5": "run_bot",
        "Escape": "stop_bot",
        "Ctrl+F": "focus_search",
    }

    @classmethod
    def setup(cls, main_window):
        from PyQt6.QtGui import QShortcut, QKeySequence

        for key, action in cls.SHORTCUTS.items():
            # Check if main_window has handler (e.g., handle_save)
            # The naming convention in MainWindow is slightly different (_handle_ctrl_s)
            # This is a helper class for future standardization.
            # Currently MainWindow sets up its own shortcuts.
            pass
