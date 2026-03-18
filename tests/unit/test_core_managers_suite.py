from datetime import UTC
from unittest.mock import MagicMock, patch

import pytest

from src.core.stats_manager import StatsManager
from src.core.time_manager import get_network_time, get_trusted_time


class TestStatsManager:
    @pytest.fixture
    def manager(self):
        # Reset singleton
        StatsManager._instance = None
        # Mock load_config to return empty dict
        with patch("src.core.config_manager.load_config", return_value={}):
            mgr = StatsManager()
            # Ensure clean state
            mgr.stats = {}
            return mgr

    @patch("src.core.config_manager.set_config_value")
    def test_increment_usage(self, mock_save, manager):
        manager.increment_usage("bot_test")
        
        # Attendi il salvataggio asincrono (necessario in V2)
        manager._save_queue.join()

        stats = manager.get_all_stats()
        assert "bot_test" in stats
        assert stats["bot_test"]["runs"] == 1
        assert stats["bot_test"]["errors"] == 0
        assert stats["bot_test"]["last_run"] is not None

        mock_save.assert_called()

    @patch("src.core.config_manager.set_config_value")
    def test_increment_error(self, mock_save, manager):
        manager.increment_error("bot_test")
        
        manager._save_queue.join()

        stats = manager.get_all_stats()
        assert "bot_test" in stats
        assert stats["bot_test"]["errors"] == 1
        # Runs should be 0 if only error incremented first
        assert stats["bot_test"]["runs"] == 0

        mock_save.assert_called()


class TestTimeManager:
    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_success(self, mock_head):
        # Mock response
        mock_resp = MagicMock()
        mock_resp.headers = {"Date": "Wed, 21 Oct 2015 07:28:00 GMT"}
        mock_head.return_value = mock_resp

        dt = get_network_time()

        assert dt is not None
        assert dt.year == 2015
        assert dt.month == 10
        assert dt.day == 21
        assert dt.tzinfo == UTC

    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_fail(self, mock_head):
        mock_head.side_effect = Exception("Timeout")

        dt = get_network_time()
        assert dt is None

    @patch("src.core.time_manager.get_network_time")
    def test_get_trusted_time_fallback(self, mock_net):
        mock_net.return_value = None

        dt, trusted = get_trusted_time()

        assert dt is not None
        assert trusted is False
        assert dt.tzinfo == UTC
