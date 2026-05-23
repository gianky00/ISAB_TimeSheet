import json
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtNetwork import QNetworkReply

from src.core.weather_service import WeatherService


class TestWeatherService:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        WeatherService._instance = None
        self.service = WeatherService.instance()

    def test_fetch_weather_starts_request(self, qtbot):
        # Mock network manager
        mock_nm = MagicMock()
        self.service.network_manager = mock_nm

        self.service.fetch_weather()

        assert self.service._is_loading is True
        assert mock_nm.get.called
        # Verifica URL
        req = mock_nm.get.call_args[0][0]
        assert "open-meteo.com" in req.url().toString()

    def test_on_weather_received_success(self, qtbot):
        # Setup mock reply
        mock_reply = MagicMock(spec=QNetworkReply)
        mock_reply.error.return_value = QNetworkReply.NetworkError.NoError
        weather_json = json.dumps({"current": {"temp": 25}}).encode("utf-8")
        mock_reply.readAll.return_value.data.return_value = weather_json

        # Mock sender()
        with patch.object(self.service, "sender", return_value=mock_reply):
            # Mock network manager per la seconda chiamata (AQI)
            mock_nm = MagicMock()
            self.service.network_manager = mock_nm

            self.service._on_weather_received()

            assert self.service._temp_weather_data["current"]["temp"] == 25
            assert mock_nm.get.called  # Chiamata AQI avviata

    def test_on_weather_received_error(self, qtbot):
        mock_reply = MagicMock(spec=QNetworkReply)
        mock_reply.error.return_value = QNetworkReply.NetworkError.ConnectionRefusedError
        mock_reply.errorString.return_value = "Refused"

        with qtbot.wait_signal(self.service.error_occurred) as blocker:
            with patch.object(self.service, "sender", return_value=mock_reply):
                self.service._on_weather_received()

        assert blocker.args[0] == "Errore Rete Meteo"
        assert self.service._is_loading is False

    def test_on_aqi_received_final(self, qtbot):
        self.service._temp_weather_data = {"w": 1}
        self.service._is_loading = True

        mock_reply = MagicMock(spec=QNetworkReply)
        mock_reply.error.return_value = QNetworkReply.NetworkError.NoError
        aqi_json = json.dumps({"aqi": 50}).encode("utf-8")
        mock_reply.readAll.return_value.data.return_value = aqi_json

        with qtbot.wait_signal(self.service.weather_data_ready) as blocker:
            with patch.object(self.service, "sender", return_value=mock_reply):
                self.service._on_aqi_received()

        assert blocker.args[0] == {"w": 1}
        assert blocker.args[1] == {"aqi": 50}
        assert self.service._is_loading is False
