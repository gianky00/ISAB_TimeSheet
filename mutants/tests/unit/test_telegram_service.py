import threading
from unittest.mock import MagicMock, patch

import pytest


class TestTelegramService:
    @pytest.fixture
    def service(self):
        with patch("src.core.telegram.service.QObject.__init__"):
            from src.core.telegram.service import TelegramService

            svc = TelegramService()
            svc.log_signal = MagicMock()
            svc.command_received = MagicMock()
            return svc

    def test_init(self, service):
        assert service.app is None
        assert service.loop is None
        assert service.connected_chat_id is None
        assert service.user_states == {}

    @patch("src.core.telegram.service.config_manager.load_config")
    def test_start_service_no_token(self, mock_config, service):
        mock_config.return_value = {"telegram_token": ""}

        service.start_service()

        service.log_signal.emit.assert_called()
        call_args = service.log_signal.emit.call_args[0][0]
        assert "Token mancante" in call_args

    @patch("src.core.telegram.service.config_manager.load_config")
    @patch("threading.Thread")
    def test_start_service_with_token(self, mock_thread, mock_config, service):
        mock_config.return_value = {
            "telegram_token": "123456:ABC",
            "telegram_chat_id": "999",
        }

        service.start_service()

        mock_thread.assert_called_once()
        assert service.connected_chat_id == "999"

    def test_stop_service_no_thread(self, service):
        service.thread = None

        # Should not raise
        service.stop_service()

    def test_stop_service_with_thread(self, service):
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True
        service.thread = mock_thread

        service.stop_service()

        assert service.stop_event.is_set()
        mock_thread.join.assert_called()

    def test_build_application(self, service):
        with patch("src.core.telegram.service.Application") as mock_app:
            mock_builder = MagicMock()
            mock_app.builder.return_value = mock_builder
            mock_builder.token.return_value = mock_builder
            mock_builder.read_timeout.return_value = mock_builder
            mock_builder.connect_timeout.return_value = mock_builder
            mock_builder.build.return_value = MagicMock()

            service._build_application("test_token")

            mock_builder.token.assert_called_with("test_token")

    def test_start_lock_prevents_concurrent_starts(self, service):
        # Verify _start_lock exists and is a Lock
        assert hasattr(service, "_start_lock")
        assert isinstance(service._start_lock, type(threading.Lock()))

    def test_user_states_isolation(self, service):
        service.user_states[123] = {"mode": "pdl"}
        service.user_states[456] = {"mode": "oda"}

        assert service.user_states[123]["mode"] == "pdl"
        assert service.user_states[456]["mode"] == "oda"

    def test_pending_data_storage(self, service):
        service.pending_data[123] = {"action": "print", "items": ["12345/C"]}

        assert service.pending_data[123]["action"] == "print"
        assert "12345/C" in service.pending_data[123]["items"]
