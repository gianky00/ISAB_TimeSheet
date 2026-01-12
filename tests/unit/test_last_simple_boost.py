from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QWidget

from src.core.stats_manager import StatsManager
from src.gui.styles import apply_theme
from src.gui.toast import ToastOverlay
from src.utils.printing import get_installed_printers


class TestLastSimpleBoost:
    def test_get_printers_logic(self):
        # win32print.EnumPrinters level 2 returns tuples where index 2 is the name
        with patch("src.utils.printing.win32print") as mock_win:
            mock_win.EnumPrinters.return_value = ( (None, None, "P1", None), )
            printers = get_installed_printers()
            assert "P1" in printers

    def test_apply_theme_logic(self, qapp):
        # Mock Path.exists and open to return a custom stylesheet
        with patch("src.gui.styles.get_asset_path", return_value="fake.qss"), \
             patch("src.gui.styles.Path.exists", return_value=True), \
             patch("builtins.open", MagicMock()):

            # Setup open mock to return specific content
            with patch("src.gui.styles.open", create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = "QWidget { color: red; }"
                apply_theme(qapp, "light")
                assert "color: red" in qapp.styleSheet()

    def test_stats_manager_increment(self, tmp_path):
        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            StatsManager._instance = None
            sm = StatsManager()
            sm.increment_usage("test_bot")
            stats = sm.get_all_stats()
            assert stats["test_bot"]["runs"] == 1

    def test_toast_overlay_basic(self, qapp):
        parent = QWidget()
        toast = ToastOverlay(parent)
        assert toast is not None
        with patch.object(toast, "show"):
            toast.show_toast("Messaggio", 1000)
            assert toast.label.text() == "Messaggio"
