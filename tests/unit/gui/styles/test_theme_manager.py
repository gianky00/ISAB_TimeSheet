import pytest
from PySide6.QtWidgets import QApplication

from src.gui.design.colors import LIGHT
from src.gui.styles.theme_manager import ThemeManager, apply_theme


class TestThemeManager:
    @pytest.fixture
    def manager(self):
        # Reset Singleton for test isolation if needed, but it's okay for these tests
        return ThemeManager()

    def test_singleton(self):
        m1 = ThemeManager()
        m2 = ThemeManager()
        assert m1 is m2

    def test_palette_property(self, manager):
        assert manager.palette == LIGHT

    def test_process_qss(self, manager):
        qss = "div { color: {{primary}}; font-size: {{font_md}}; border-radius: {{radius_medium}}; }"
        processed = manager._process_qss(qss)

        assert LIGHT.primary in processed
        assert "14px" in processed  # font_md
        assert "8px" in processed  # radius_medium
        assert "{{" not in processed

    def test_apply_theme(self, manager, qtbot):
        # We need a dummy app, qtbot provides one or we can use the existing one
        app = QApplication.instance() or QApplication([])

        manager.apply_theme(app)

        # Verify app has a stylesheet and a palette set
        assert app.styleSheet() != ""
        # The palette is complex to check fully but we can check if it was called
        # via app.palette()
        assert (
            app.palette()
            .color(app.palette().ColorGroup.Active, app.palette().ColorRole.Window)
            .name()
            .upper()
            == LIGHT.background.upper()
        )

    def test_apply_theme_wrapper(self, qtbot):
        app = QApplication.instance() or QApplication([])
        apply_theme(app, "light")
        assert app.styleSheet() != ""
