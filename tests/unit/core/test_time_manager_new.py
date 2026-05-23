from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import requests

from src.core.time_manager import get_network_time, get_trusted_time


class TestTimeManager:
    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_success(self, mock_head):
        mock_response = MagicMock()
        mock_response.headers = {"Date": "Tue, 23 May 2026 10:00:00 GMT"}
        mock_head.return_value = mock_response

        res = get_network_time()
        assert res is not None
        assert res.year == 2026
        assert res.month == 5
        assert res.day == 23

    @patch("src.core.time_manager.requests.head", side_effect=requests.exceptions.RequestException("Fail"))
    def test_get_network_time_failure(self, mock_head):
        assert get_network_time() is None

    @patch("src.core.time_manager.get_network_time")
    def test_get_trusted_time_net(self, mock_net):
        mock_dt = datetime(2026, 5, 23, 10, 0, 0, tzinfo=UTC)
        mock_net.return_value = mock_dt

        dt, trusted = get_trusted_time()
        assert trusted is True
        assert dt == mock_dt

    @patch("src.core.time_manager.get_network_time", return_value=None)
    def test_get_trusted_time_fallback(self, mock_net):
        dt, trusted = get_trusted_time()
        assert trusted is False
        assert isinstance(dt, datetime)
