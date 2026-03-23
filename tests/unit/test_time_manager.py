from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from src.core.time_manager import get_network_time, get_trusted_time


class TestTimeManager:
    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_success(self, mock_head):
        mock_response = MagicMock()
        mock_response.headers = {"Date": "Sat, 01 Feb 2026 12:30:00 GMT"}
        mock_head.return_value = mock_response

        result = get_network_time()
        assert result is not None
        assert result.year == 2026
        assert result.month == 2
        assert result.day == 1
        assert result.tzinfo is not None

    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_failure(self, mock_head):
        mock_head.side_effect = Exception("Connection error")
        result = get_network_time()
        assert result is None

    @patch("src.core.time_manager.get_network_time")
    def test_get_trusted_time_trusted(self, mock_net):
        mock_net.return_value = datetime(2026, 2, 1, 12, 0, tzinfo=UTC)
        dt, is_trusted = get_trusted_time()
        assert is_trusted is True
        assert dt.year == 2026

    @patch("src.core.time_manager.get_network_time")
    def test_get_trusted_time_fallback(self, mock_net):
        mock_net.return_value = None
        dt, is_trusted = get_trusted_time()
        assert is_trusted is False
        assert dt.tzinfo is not None
