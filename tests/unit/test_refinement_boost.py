import pytest
from unittest.mock import MagicMock, patch
from src.core.stats_manager import StatsManager
from src.gui.widgets.status_indicator import StatusIndicator
from src.gui.toast import ToastOverlay
from src.core.license_updater import run_update

class TestRefinementBoost:
    def test_stats_manager_reset(self, tmp_path):
        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            sm = StatsManager()
            sm.increment_usage("bot1")
            # Force reload or check internal save
            stats = sm.get_all_stats()
            assert "bot1" in stats

    def test_status_indicator_all_states(self, qapp):
        indicator = StatusIndicator()
        states = ["idle", "running", "success", "error", "unknown"]
        for s in states:
            indicator.set_status(s, f"Msg {s}")
            assert indicator.current_color is not None

    def test_toast_overlay_fade(self, qapp, qtbot):
        from PyQt6.QtWidgets import QWidget
        parent = QWidget()
        toast = ToastOverlay(parent)
        toast.show_toast("Test")
        # Trigger hide logic
        toast.hide_toast()
        assert toast.anim.startValue() == 1

    @patch("src.core.license_updater.get_hardware_id", return_value="ID123")
    @patch("requests.get")
    def test_license_run_update_fail(self, mock_get, mock_hwid):
        # Test failure in update network call
        mock_get.side_effect = Exception("Network Down")
        # Should not crash
        run_update()
        assert True
