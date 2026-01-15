import pytest
from datetime import datetime, timezone
from unittest.mock import patch, Mock
from src.core.time_manager import get_network_time, get_trusted_time

class TestTimeManager:
    """Test coverage for src/core/time_manager.py"""

    @patch('src.core.time_manager.requests.head')
    def test_get_network_time_success(self, mock_head):
        # Mock successful response
        mock_resp = Mock()
        mock_resp.headers = {"Date": "Wed, 21 Oct 2015 07:28:00 GMT"}
        mock_head.return_value = mock_resp
        
        dt = get_network_time()
        assert dt is not None
        assert dt.year == 2015
        assert dt.month == 10
        assert dt.day == 21
        assert dt.hour == 7
        assert dt.tzinfo == timezone.utc

    @patch('src.core.time_manager.requests.head')
    def test_get_network_time_failure_no_header(self, mock_head):
        # Mock response without Date header
        mock_resp = Mock()
        mock_resp.headers = {}
        mock_head.return_value = mock_resp
        
        dt = get_network_time()
        assert dt is None

    @patch('src.core.time_manager.requests.head')
    def test_get_network_time_exception(self, mock_head):
        # Mock connection error
        mock_head.side_effect = Exception("Connection Refused")
        
        dt = get_network_time()
        assert dt is None

    @patch('src.core.time_manager.get_network_time')
    def test_get_trusted_time_network(self, mock_get_net):
        fake_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_get_net.return_value = fake_time
        
        dt, trusted = get_trusted_time()
        assert dt == fake_time
        assert trusted is True

    @patch('src.core.time_manager.get_network_time')
    def test_get_trusted_time_fallback(self, mock_get_net):
        mock_get_net.return_value = None
        
        dt, trusted = get_trusted_time()
        assert isinstance(dt, datetime)
        assert trusted is False
        # Ensure fallback is roughly now (UTC)
        now = datetime.now(timezone.utc)
        assert abs((dt - now).total_seconds()) < 1.0