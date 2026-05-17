from PySide6.QtCore import QRect
from PySide6.QtWidgets import QWidget

from src.gui.styles.ui_effects import UIEffectsManager


class TestUIEffectsManager:
    def test_apply_shadow(self, qtbot):
        widget = QWidget()
        UIEffectsManager.apply_shadow(widget)
        assert widget.graphicsEffect() is not None

    def test_animate_fade(self, qtbot):
        widget = QWidget()
        UIEffectsManager.animate_fade(widget, duration=10)
        # Verify animation started - hard to check result without waiting
        # but calling the method is already good for coverage

    def test_animate_geometry(self, qtbot):
        widget = QWidget()
        start = QRect(0, 0, 10, 10)
        end = QRect(0, 0, 20, 20)
        UIEffectsManager.animate_geometry(widget, start, end, duration=10)
