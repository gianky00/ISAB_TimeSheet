import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService


class TestTelegramCoverage:
    @pytest.fixture
    def service(self, mocker):
        mocker.patch(
            "src.core.config_manager.load_config",
            return_value={"telegram_token": "TOKEN"},
        )
        return TelegramService()

    @pytest.mark.asyncio
    async def test_async_loop_lifecycle(self, service, mocker):
        # Mock Application builder
        mock_app = MagicMock()
        mock_app.initialize = AsyncMock()
        mock_app.start = AsyncMock()
        mock_app.stop = AsyncMock()
        mock_app.shutdown = AsyncMock()
        mock_app.updater = MagicMock()
        mock_app.updater.start_polling = AsyncMock()
        mock_app.updater.stop = AsyncMock()
        mock_app.running = True

        mocker.patch.object(service, "_build_application", return_value=mock_app)

        # Ensure the loop exits immediately
        service.stop_event.set()

        # Test the core async logic directly
        await service._main_loop_logic("TOKEN")

        # Verification
        mock_app.initialize.assert_awaited()
        mock_app.shutdown.assert_awaited()

    def test_send_message_sync(self, service, mocker):
        service.loop = MagicMock()
        service.loop.is_running.return_value = True
        service.connected_chat_id = "123"

        with patch("asyncio.run_coroutine_threadsafe") as mock_run:
            service.send_message_sync("Hello")
            mock_run.assert_called()
            # Ensure called with a coroutine
            args = mock_run.call_args[0]
            assert asyncio.iscoroutine(args[0])
            # Close the coroutine to avoid warning
            args[0].close()


class TestTelegramBridge:
    @pytest.fixture
    def bridge(self, mocker):
        mw = MagicMock()
        mw.telegram = MagicMock()
        # Mock loop for threadsafe calls
        mw.telegram.loop = MagicMock()
        return TelegramUIBridge(mw)

    def test_intent_processing_pdl(self, bridge):
        intent = {"action": "print", "object": "pdl", "items": ["123456/C", "invalid"]}

        # Mock validators
        with patch("src.utils.validators.InputValidator.validate_pdl") as mock_val:
            mock_val.side_effect = lambda x: MagicMock(valid=(x == "123456/C"), sanitized_value=x)

            with patch("asyncio.run_coroutine_threadsafe") as mock_run:
                bridge._handle_intent("123", intent)

                # Check rows added
                bridge.mw.pdl_panel.add_rows_simple.assert_called()
                # Check messages sent
                bridge.telegram.send_message_sync.assert_called()
                # Check async message sent
                mock_run.assert_called()
                args = mock_run.call_args[0]
                assert asyncio.iscoroutine(args[0])
                args[0].close()

    def test_handle_command_run_ts(self, bridge):
        bridge.mw.scarico_panel.validate_ready.return_value = (True, "OK")
        bridge._handle_command("run_ts", {})

        bridge.mw.navigate_to_panel.assert_called_with("scarico_ts")
        bridge.mw.scarico_panel.start_btn.click.assert_called()
