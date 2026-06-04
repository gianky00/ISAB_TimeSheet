import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from telegram import CallbackQuery, Chat, Message, Update, User

from src.api.telegram.handlers import callbacks, messages
from src.api.telegram_manager import TelegramService


class TestTelegramManagerCoverage:
    def setup_method(self):
        # Patch QObject.__init__ to allow MagicMock as parent
        with patch("PySide6.QtCore.QObject.__init__", return_value=None):
            self.service = TelegramService()

        self.service.log_signal = MagicMock()
        self.service.command_received = MagicMock()
        self.service.data_received = MagicMock()
        self.service.status_requested = MagicMock()
        self.service.query_received = MagicMock()
        self.service.intent_received = MagicMock()
        self.service.photo_received = MagicMock()

    @patch("src.api.telegram.service.config_manager.load_config")
    def test_start_service_no_token(self, mock_load):
        mock_load.return_value = {"telegram_token": ""}
        self.service.start_service()
        assert self.service.log_signal.emit.called

    @patch("src.api.telegram.service.config_manager.load_config")
    @patch("threading.Thread")
    def test_start_service_success(self, mock_thread, mock_load):
        mock_load.return_value = {
            "telegram_token": "TEST_TOKEN",
            "telegram_chat_id": "123",
        }
        self.service.start_service()
        mock_thread.return_value.start.assert_called()

    def test_stop_service(self):
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True
        self.service._service_thread = mock_thread
        self.service.stop_event = MagicMock()

        self.service.stop_service()
        mock_thread.join.assert_called()

    async def async_mock_update(self, text=None, chat_id=123, user_id=123, data=None):
        update = MagicMock(spec=Update)
        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = chat_id
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = user_id

        update.message = MagicMock(spec=Message)
        update.message.text = text
        update.message.reply_text = AsyncMock()
        update.message.reply_chat_action = AsyncMock()

        if data:
            update.callback_query = MagicMock(spec=CallbackQuery)
            update.callback_query.data = data
            update.callback_query.answer = AsyncMock()
            update.callback_query.edit_message_text = AsyncMock()

        return update

    def test_handle_text_input_query(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(text="ciao", chat_id=123))
        self.service.connected_chat_id = "123"
        self.service.user_states = {}

        loop.run_until_complete(messages.handle_text_input(self.service, update, None))
        loop.close()

        self.service.query_received.emit.assert_called_with("123", "ciao")

    def test_handle_voice(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(chat_id=123))
        update.message.voice = MagicMock(file_id="fid")

        loop.run_until_complete(messages.handle_voice(self.service, update, None))
        loop.close()

        update.message.reply_text.assert_called()
        args = update.message.reply_text.call_args[0][0]
        assert "non supportati" in args

    def test_handle_photo(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(chat_id=123))
        update.message.photo = [MagicMock(file_id="fid")]
        update.message.caption = "cap"

        mock_file = AsyncMock()
        mock_file.download_as_bytearray.return_value = b"bytes"
        context = MagicMock()
        context.bot.get_file = AsyncMock(return_value=mock_file)

        self.service.connected_chat_id = "123"

        loop.run_until_complete(messages.handle_photo(self.service, update, context))
        loop.close()

        self.service.photo_received.emit.assert_called_with("123", b"bytes", "cap")

    def test_handle_button_menu_main(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(data="menu_main", chat_id=123))
        self.service.connected_chat_id = "123"

        loop.run_until_complete(callbacks.handle_button(self.service, update, None))
        loop.close()

        update.callback_query.edit_message_text.assert_called()
