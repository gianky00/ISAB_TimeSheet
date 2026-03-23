from unittest.mock import ANY, AsyncMock, MagicMock, mock_open, patch

import pytest
import telegram

from src.core.telegram_manager import TelegramService


@pytest.fixture
def telegram_service():
    with patch("PyQt6.QtCore.QObject.__init__"):
        service = TelegramService()
    service.log_signal = MagicMock()
    service.command_received = MagicMock()
    service.app = AsyncMock()
    service.app.bot = AsyncMock()
    service.connected_chat_id = "123"
    service.pdl_settings = {}
    return service


@pytest.mark.asyncio
async def test_handle_error_conflict(telegram_service):
    context = MagicMock()
    context.error = telegram.error.Conflict("test")
    telegram_service.stop_event = MagicMock()

    await telegram_service._handle_error(None, context)

    telegram_service.log_signal.emit.assert_called()
    assert any("CONFLITTO" in str(args) for args in telegram_service.log_signal.emit.call_args_list)
    telegram_service.stop_event.set.assert_called()


@pytest.mark.asyncio
async def test_handle_error_network(telegram_service):
    context = MagicMock()
    context.error = telegram.error.NetworkError("test")

    await telegram_service._handle_error(None, context)

    assert any("Rete" in str(args) for args in telegram_service.log_signal.emit.call_args_list)


@pytest.mark.asyncio
async def test_handle_error_other(telegram_service):
    context = MagicMock()
    context.error = Exception("generic")

    await telegram_service._handle_error(None, context)

    assert any("Imprevisto" in str(args) for args in telegram_service.log_signal.emit.call_args_list)


@pytest.mark.asyncio
async def test_handle_run_pdl_on(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    with patch(
        "src.core.telegram.handlers.callbacks.get_installed_printers",
        return_value=["Printer 1", "Printer 2"],
    ):
        update = MagicMock()
        update.callback_query = AsyncMock()
        update.callback_query.data = "run_pdl_on"
        update.callback_query.message = AsyncMock()
        update.effective_user.id = 123
        update.effective_chat = MagicMock()
        update.effective_chat.id = 123

        await callbacks.handle_button(telegram_service, update, MagicMock())

        update.callback_query.edit_message_text.assert_called()
        _args, kwargs = update.callback_query.edit_message_text.call_args
        # The keyboard is generated via TelegramUI, we just check it was called
        assert "reply_markup" in kwargs


@pytest.mark.asyncio
async def test_handle_run_pdl_off(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    update = MagicMock()
    update.callback_query = AsyncMock()
    update.callback_query.data = "run_pdl_off"
    update.callback_query.message = AsyncMock()
    update.effective_user.id = 123
    update.effective_chat = MagicMock()
    update.effective_chat.id = 123

    await callbacks.handle_button(telegram_service, update, MagicMock())

    update.callback_query.edit_message_text.assert_called_with(
        "Vuoi ricevere il PDF unito in chat?", reply_markup=ANY
    )


@pytest.mark.asyncio
async def test_handle_printer_selection(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    with patch(
        "src.core.telegram.handlers.callbacks.get_installed_printers",
        return_value=["Printer 1", "Printer 2"],
    ):
        query = AsyncMock()
        chat_id = 123
        await callbacks._handle_printer_selection(telegram_service, "sel_print_run_Printer 1", query, chat_id)

        assert telegram_service.user_states[chat_id]["printer"] == "Printer 1"
        query.edit_message_text.assert_called()


@pytest.mark.asyncio
async def test_handle_run_pdl_confirm_print_yes(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    query = AsyncMock()
    chat_id = 123
    telegram_service.user_states[chat_id] = {"printer": "MyPrinter"}
    telegram_service.pdl_settings[chat_id] = {"merge_all": True}

    await callbacks._handle_run_pdl_confirm(telegram_service, "confirm_merge_yes_print", query, chat_id)

    telegram_service.command_received.emit.assert_any_call("set_printer", {"printer": "MyPrinter"})
    telegram_service.command_received.emit.assert_any_call(
        "run_pdl", {"merge_all": True, "print": True, "merge_and_send": True}
    )


@pytest.mark.asyncio
async def test_handle_run_pdl_confirm_noprint_no(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    query = AsyncMock()
    chat_id = 123

    await callbacks._handle_run_pdl_confirm(telegram_service, "confirm_merge_no_noprint", query, chat_id)

    telegram_service.command_received.emit.assert_called_with(
        "run_pdl", {"merge_all": False, "print": False, "merge_and_send": False}
    )


@pytest.mark.asyncio
async def test_handle_utility_actions_status(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    telegram_service.status_requested = MagicMock()
    await callbacks._handle_utility_actions(telegram_service, "status", MagicMock(), 123)
    telegram_service.status_requested.emit.assert_called_with("123")


@pytest.mark.asyncio
async def test_handle_utility_actions_screenshot(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    query = AsyncMock()
    await callbacks._handle_utility_actions(telegram_service, "screenshot", query, 123)
    query.edit_message_text.assert_called_with("📸 Screenshot:", reply_markup=ANY)


@pytest.mark.asyncio
async def test_handle_utility_actions_snap(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    telegram_service.screenshot_requested = MagicMock()
    await callbacks._handle_utility_actions(telegram_service, "snap_app", MagicMock(), 123)
    telegram_service.screenshot_requested.emit.assert_called_with("app")


@pytest.mark.asyncio
async def test_async_send_methods(telegram_service):
    await telegram_service._send_message_async("123", "text")
    telegram_service.app.bot.send_message.assert_called()

    await telegram_service._send_photo_async("123", b"photo", "caption")
    telegram_service.app.bot.send_photo.assert_called()

    with patch("builtins.open", mock_open(read_data=b"data")):
        # We need to simulate that telegram_service.app.bot is an AsyncMock
        await telegram_service._send_document_async("123", "path/to/file", "caption")
        telegram_service.app.bot.send_document.assert_called()


@pytest.mark.asyncio
async def test_shutdown_application(telegram_service):
    telegram_service.app.updater = AsyncMock()
    telegram_service.app.updater.is_running = True
    telegram_service.app.running = True

    await telegram_service._shutdown_application()

    telegram_service.app.updater.stop.assert_called()
    telegram_service.app.stop.assert_called()
    telegram_service.app.shutdown.assert_called()


def test_get_full_printer_name(telegram_service):
    from src.core.telegram.handlers import callbacks  # noqa: PLC0415

    with patch("src.core.telegram.handlers.callbacks.get_installed_printers") as mock_p:
        mock_p.return_value = ["My Specific Printer"]
        assert callbacks._get_full_printer_name("My Spec") == "My Specific Printer"
        assert callbacks._get_full_printer_name("Unknown") == "Unknown"
