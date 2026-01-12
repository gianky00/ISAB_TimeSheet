from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from src.core import time_manager


class TestTimeManagerCoverage:
    """Test suite per src/core/time_manager.py"""

    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_success(self, mock_head):
        """Test recupero orario successo."""
        mock_resp = MagicMock()
        mock_resp.headers = {"Date": "Wed, 21 Oct 2015 07:28:00 GMT"}
        mock_head.return_value = mock_resp

        dt = time_manager.get_network_time()
        assert dt is not None
        assert dt.year == 2015
        assert dt.month == 10
        # Dovrebbe essere UTC
        assert dt.tzinfo is not None

    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_error(self, mock_head):
        """Test recupero orario errore (timeout/connection)."""
        mock_head.side_effect = Exception("Timeout")
        dt = time_manager.get_network_time()
        assert dt is None

    @patch("src.core.time_manager.requests.head")
    def test_get_network_time_no_header(self, mock_head):
        """Test recupero orario header mancante."""
        mock_resp = MagicMock()
        mock_resp.headers = {} # No Date
        mock_head.return_value = mock_resp

        dt = time_manager.get_network_time()
        assert dt is None

    @patch("src.core.time_manager.requests.head")
    @patch("src.core.time_manager.parsedate_to_datetime")
    def test_get_network_time_naive_timezone(self, mock_parse, mock_head):
        """Test caso particolare datetime naive (linea 31)."""
        mock_resp = MagicMock()
        mock_resp.headers = {"Date": "Dummy"}
        mock_head.return_value = mock_resp

        # Restituisci un datetime senza tzinfo
        naive_dt = datetime(2023, 1, 1, 12, 0, 0)
        mock_parse.return_value = naive_dt

        dt = time_manager.get_network_time()

        # Verifica che sia stato convertito in timezone aware
        assert dt.tzinfo == timezone.utc
        assert dt.year == 2023

    @patch("src.core.time_manager.get_network_time")
    def test_get_trusted_time_network(self, mock_net):
        """Test get_trusted_time usa rete se disponibile."""
        fake_time = datetime(2025, 1, 1, tzinfo=timezone.utc)
        mock_net.return_value = fake_time

        dt, trusted = time_manager.get_trusted_time()
        assert dt == fake_time
        assert trusted is True

    @patch("src.core.time_manager.get_network_time")
    def test_get_trusted_time_fallback(self, mock_net):
        """Test get_trusted_time fallback su sistema."""
        mock_net.return_value = None

        dt, trusted = time_manager.get_trusted_time()
        assert isinstance(dt, datetime)
        assert trusted is False
        assert dt.tzinfo == timezone.utc
