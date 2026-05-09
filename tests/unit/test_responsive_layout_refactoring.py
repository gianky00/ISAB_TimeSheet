"""
Baseline tests for Responsive Layouts.
"""

from PySide6.QtWidgets import QLabel

from src.gui.layouts.responsive import ResponsiveContainer


def test_responsive_mode_detection(qtbot):
    """Test that the correct mode is detected based on width."""
    container = ResponsiveContainer()
    qtbot.addWidget(container)

    assert container._get_mode(500) == "mobile"
    assert container._get_mode(750) == "tablet"
    assert container._get_mode(1200) == "desktop"


def test_layout_rebuilding(qtbot):
    """Test that widgets are correctly added back after a resize/rebuild."""
    container = ResponsiveContainer()
    qtbot.addWidget(container)

    w1 = QLabel("W1")
    w2 = QLabel("W2")
    container.addWidget(w1)
    container.addWidget(w2)

    # Force mobile (stack)
    container._current_mode = "mobile"
    container._rebuild_layout()
    assert container._main_layout.count() == 2

    # Force desktop (grid)
    container._current_mode = "desktop"
    container._rebuild_layout()
    # Desktop uses addLayout for rows
    assert container._main_layout.count() == 1  # 2 widgets in 1 row
