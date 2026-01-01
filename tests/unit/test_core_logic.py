import pytest
from unittest.mock import patch, MagicMock
from src.core.stats_manager import StatsManager
from src.core.time_manager import get_network_time, get_trusted_time

class TestCoreLogic:

    def test_stats_manager_singleton(self):
        s1 = StatsManager()
        s2 = StatsManager()
        assert s1 is s2

    @patch('src.core.config_manager.set_config_value')
    @patch('src.core.config_manager.load_config', return_value={})
    def test_stats_increment(self, mock_load, mock_set):
        mgr = StatsManager()
        mgr.stats = {} # Clean state
        
        mgr.increment_usage("test_bot")
        assert mgr.stats["test_bot"]["runs"] == 1
        
        mgr.increment_error("test_bot")
        assert mgr.stats["test_bot"]["errors"] == 1

    @patch('requests.head')
    def test_network_time(self, mock_head):
        mock_resp = MagicMock()
        mock_resp.headers = {"Date": "Wed, 21 Oct 2015 07:28:00 GMT"}
        mock_head.return_value = mock_resp
        
        dt = get_network_time()
        assert dt.year == 2015
        assert dt.month == 10
        
    @patch('src.core.time_manager.get_network_time', return_value=None)
    def test_trusted_time_fallback(self, mock_net):
        dt, trusted = get_trusted_time()
        assert trusted is False
        assert dt is not None
