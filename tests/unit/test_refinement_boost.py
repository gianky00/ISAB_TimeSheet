from unittest.mock import patch

import requests

from src.core.license_updater import run_update
from src.core.stats_manager import StatsManager
from src.gui.toast import ToastOverlay
from src.gui.widgets.status_indicator import StatusIndicator


class TestRefinementBoost:
    def test_stats_manager_reset(self, tmp_path):  # noqa: ANN001
        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            # Force singleton reset for test isolation
            StatsManager._instance = None
            sm = StatsManager()
            sm.increment_usage("bot1")
            stats = sm.get_all_stats()
            assert "bot1" in stats

    def test_status_indicator_all_states(self, qapp):  # noqa: ANN001
        indicator = StatusIndicator()
        states = ["idle", "running", "success", "error", "unknown"]
        for s in states:
            indicator.set_status(s, f"Msg {s}")
            assert indicator.toolTip() == f"Msg {s}"

    def test_toast_overlay_fade(self, qapp, qtbot):  # noqa: ANN001
        from PyQt6.QtWidgets import QWidget  # noqa: PLC0415

        parent = QWidget()
        toast = ToastOverlay(parent)
        toast.show_toast("Test")
        # Trigger hide logic
        toast.hide_toast()
        assert toast.anim.startValue() == 1

    @patch("src.core.license_validator.get_hardware_id", return_value="ID123")
    @patch("requests.get")
    def test_license_run_update_fail(self, mock_get, mock_hwid):  # noqa: ANN001
        # Test failure in update network call
        # Use requests.RequestException to match the try-except block in run_update
        mock_get.side_effect = requests.RequestException("Network Down")
        # Should not crash
        result = run_update()
        assert result is False
