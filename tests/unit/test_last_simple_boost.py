import pytest
from unittest.mock import MagicMock, patch
from src.utils.printing import get_installed_printers
from src.gui.styles import apply_theme
from src.core.stats_manager import StatsManager
from src.gui.toast import ToastOverlay
from PyQt6.QtWidgets import QWidget

class TestLastSimpleBoost:
    def test_get_printers_logic(self):
        with patch("src.utils.printing.win32print") as mock_win:
            mock_win.EnumPrinters.return_value = [{"pPrinterName": "P1"}]
            printers = get_installed_printers()
            assert "P1" in printers

    def test_apply_theme_logic(self, qapp):
        widget = QWidget()
        with patch("src.gui.styles.ResourceManager.get_style", return_value="QWidget { color: red; }"):
            apply_theme(widget, "light")
            assert "color: red" in widget.styleSheet()

    def test_stats_manager_increment(self, tmp_path):
        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            sm = StatsManager()
            sm.increment_usage("test_bot")
            stats = sm.get_all_stats()
            assert stats["test_bot"]["runs"] == 1

    def test_toast_overlay_basic(self, qapp):
        parent = QWidget()
        toast = ToastOverlay(parent)
        assert toast is not None
        toast.show_toast("Messaggio", 1000)
        assert toast.isVisible()
        assert toast.label.text() == "Messaggio"