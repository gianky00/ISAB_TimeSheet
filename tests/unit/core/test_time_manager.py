from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from src.core.time_manager import get_network_time, get_trusted_time


class TestTimeManager:
    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_success(self, mock_head):
        mock_response = MagicMock()
        mock_response.headers = {"Date": "Tue, 23 May 2026 10:00:00 GMT"}
        mock_head.return_value = mock_response

        net_time = get_network_time()
        assert net_time is not None
        assert net_time.year == 2026
        assert net_time.month == 5
        assert net_time.day == 23
        assert net_time.tzinfo == UTC

    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_no_date_header(self, mock_head):
        mock_response = MagicMock()
        mock_response.headers = {}
        mock_head.return_value = mock_response

        assert get_network_time() is None

    @patch("src.core.time_manager.requests.head", side_effect=Exception("Network Error"))
    def test_get_network_time_exception(self, mock_head):
        assert get_network_time() is None

    @patch("src.core.time_manager.get_network_time")
    def test_get_trusted_time_from_network(self, mock_get_net_time):
        expected_time = datetime(2026, 5, 23, 10, 0, 0, tzinfo=UTC)
        mock_get_net_time.return_value = expected_time

        time_val, is_trusted = get_trusted_time()
        assert is_trusted is True
        assert time_val == expected_time

    @patch("src.core.time_manager.get_network_time", return_value=None)
    @patch("src.core.time_manager.datetime")
    def test_get_trusted_time_fallback(self, mock_datetime, mock_get_net_time):
        expected_fallback = datetime(2026, 1, 1, tzinfo=UTC)
        mock_datetime.now.return_value = expected_fallback

        time_val, is_trusted = get_trusted_time()
        assert is_trusted is False
        assert time_val == expected_fallback
