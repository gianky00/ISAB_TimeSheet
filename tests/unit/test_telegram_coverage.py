from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.api.telegram_manager import TelegramService
from src.application.services.telegram_bridge import TelegramUIBridge


class TestTelegramCoverage:
    @pytest.fixture
    def service(self, mocker):
        mocker.patch(
            "src.application.services.config_manager.load_config", return_value={"telegram_token": "TOKEN"}
        )
        return TelegramService()

    @pytest.mark.asyncio
    async def test_async_loop_lifecycle(self, service, mocker):
        mock_app = MagicMock()
        mock_app.initialize = AsyncMock()
        mock_app.start = AsyncMock()
        mock_app.shutdown = AsyncMock()
        mock_app.updater = MagicMock()
        mocker.patch.object(service, "_build_application", return_value=mock_app)
        service.stop_event.set()
        await service._main_loop_logic("TOKEN")
        mock_app.initialize.assert_awaited()

    def test_send_message_sync(self, service, mocker):
        service.loop = MagicMock()
        service.loop.is_running.return_value = True
        service.connected_chat_id = "123"
        with patch("asyncio.run_coroutine_threadsafe") as mock_run:
            service.send_message_sync("Hello")
            assert mock_run.called


class TestTelegramBridge:
    @pytest.fixture
    def bridge(self, mocker):
        mw = MagicMock()
        mw.telegram = MagicMock()
        mw.telegram.loop = MagicMock()
        mw.pdl_panel = MagicMock()
        mw.scarico_panel = MagicMock()
        # Patch QObject.__init__ per evitare inizializzazione Qt reale
        with patch("src.application.services.telegram_bridge.QObject.__init__"):
            return TelegramUIBridge(mw)

    def test_handle_command_run_ts(self, bridge):
        """Verifica il dispatch del comando run_ts isolando ui_commands."""
        with patch.object(bridge.ui_commands, "run_ts_bot") as mock_run:
            bridge._dispatch_command("run_ts", {})
            mock_run.assert_called_once()
