import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from telegram import CallbackQuery, Chat, Message, Update, User

from src.core.telegram_manager import TelegramService


class TestTelegramManagerCoverage(unittest.TestCase):
    def setUp(self):
        # Patch QObject.__init__ to allow MagicMock as parent/etc if needed
        with patch('PyQt6.QtCore.QObject.__init__'):
            self.service = TelegramService()

        self.service.log_signal = MagicMock()
        self.service.log_signal.emit = MagicMock()
        self.service.command_received = MagicMock()
        self.service.command_received.emit = MagicMock()
        self.service.data_received = MagicMock()
        self.service.data_received.emit = MagicMock()
        self.service.status_requested = MagicMock()
        self.service.status_requested.emit = MagicMock()
        self.service.query_received = MagicMock()
        self.service.query_received.emit = MagicMock()
        self.service.intent_received = MagicMock()
        self.service.intent_received.emit = MagicMock()
        self.service.photo_received = MagicMock()
        self.service.photo_received.emit = MagicMock()

        # Don't mock send_message_sync here, we need to test it.
        # Other tests will use mock as needed.

    @patch('src.core.telegram_manager.config_manager.load_config')

    def test_start_service_no_token(self, mock_load):
        mock_load.return_value = {"telegram_token": ""}
        self.service.start_service()
        self.service.log_signal.emit.assert_called_with("⚠️ Telegram Token mancante.")

    @patch('src.core.telegram_manager.config_manager.load_config')
    @patch('threading.Thread')
    def test_start_service_success(self, mock_thread, mock_load):
        mock_load.return_value = {"telegram_token": "TEST_TOKEN", "telegram_chat_id": "123"}
        self.service.start_service()
        mock_thread.return_value.start.assert_called()

    def test_stop_service(self):
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True
        self.service.thread = mock_thread

        # stop_event might be real or mocked, let's ensure it doesn't crash
        if not hasattr(self.service.stop_event, 'set'):
            self.service.stop_event = MagicMock()

        self.service.stop_service()
        mock_thread.join.assert_called()

    async def async_mock_update(self, text=None, chat_id=123, user_id=123, data=None):
        update = AsyncMock(spec=Update)
        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = chat_id
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = user_id

        update.message = AsyncMock(spec=Message)
        update.message.text = text
        update.message.reply_text = AsyncMock()
        update.message.reply_chat_action = AsyncMock()

        if data:
            update.callback_query = AsyncMock(spec=CallbackQuery)
            update.callback_query.data = data
            update.callback_query.message = AsyncMock(spec=Message)
            update.callback_query.message.chat_id = chat_id
            update.callback_query.answer = AsyncMock()
            update.callback_query.edit_message_text = AsyncMock()

        return update

    def test_check_auth_success(self):
        self.service.connected_chat_id = "123"
        update = MagicMock()
        update.effective_user.id = 123

        # Need to run async method
        loop = asyncio.new_event_loop()
        res = loop.run_until_complete(self.service._check_auth(update))
        loop.close()
        self.assertTrue(res)

    def test_check_auth_fail(self):
        self.service.connected_chat_id = "123"
        update = MagicMock()
        update.effective_user.id = 999
        update.message = AsyncMock()

        loop = asyncio.new_event_loop()
        res = loop.run_until_complete(self.service._check_auth(update))
        loop.close()
        self.assertFalse(res)

    @patch('src.core.telegram_manager.config_manager.set_config_value')
    def test_cmd_start(self, mock_set_conf):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(text="/start", chat_id=123))
        self.service.connected_chat_id = None # Simulate first connect

        loop.run_until_complete(self.service._cmd_start(update, None))
        loop.close()

        mock_set_conf.assert_called_with("telegram_chat_id", "123")
        update.message.reply_text.assert_called()

    def test_handle_text_input_nlu(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(text="stampa report", chat_id=123))
        self.service.connected_chat_id = "123"
        self.service._process_with_ai = AsyncMock()

        loop.run_until_complete(self.service._handle_text_input(update, None))
        loop.close()

        self.service._process_with_ai.assert_called_with(123, "stampa report")

    def test_handle_text_input_query(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(text="ciao", chat_id=123))
        self.service.connected_chat_id = "123"

        loop.run_until_complete(self.service._handle_text_input(update, None))
        loop.close()

        self.service.query_received.emit.assert_called_with("123", "ciao")

    def test_handle_text_input_sequential_oda(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(text="12345", chat_id=123))
        self.service.connected_chat_id = "123"
        self.service.user_states[123] = "WAITING_ODA"

        loop.run_until_complete(self.service._handle_text_input(update, None))
        loop.close()

        self.service.data_received.emit.assert_called_with("oda", ["12345"])
        self.assertIsNone(self.service.user_states[123])

    def test_handle_button_menu_main(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(data="menu_main", chat_id=123))
        self.service.connected_chat_id = "123"

        loop.run_until_complete(self.service._handle_button(update, None))
        loop.close()

        update.callback_query.edit_message_text.assert_called()

    def test_handle_button_direct_command(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(data="run_ts", chat_id=123))
        self.service.connected_chat_id = "123"

        loop.run_until_complete(self.service._handle_button(update, None))
        loop.close()

        self.service.command_received.emit.assert_called_with("run_ts", {})

    def test_handle_button_db_year(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(data="db_year_STRUMENTALE_2025", chat_id=123))
        self.service.connected_chat_id = "123"

        loop.run_until_complete(self.service._handle_button(update, None))
        loop.close()

        self.assertEqual(self.service.user_states[123], "WAITING_DB_QUERY_STRUMENTALE_2025")

    @patch('src.core.telegram_manager.SecretsManager.get_gemini_api_key')
    @patch('src.core.lyra_client.LyraClient')
    def test_process_with_ai_text(self, mock_client_cls, mock_key):
        mock_key.return_value = "API_KEY"
        mock_client = mock_client_cls.return_value
        mock_client.ask.return_value = '{"action": "test", "items": []}'

        self.service.ai_executor.submit = lambda f, *args: f(*args)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.service._process_with_ai(123, "text"))
        loop.close()

        self.service.intent_received.emit.assert_called()

    @patch('src.core.telegram_manager.SecretsManager.get_gemini_api_key')
    def test_process_with_ai_no_key(self, mock_key):
        mock_key.return_value = None
        self.service.send_message_sync = MagicMock()

        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.service._process_with_ai(123, "text"))
        loop.close()

        self.service.send_message_sync.assert_called_with("⚠️ API Key mancante per intelligenza bot.")


    def test_handle_db_query_input(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(text="query", chat_id=123))
        self.service.user_states[123] = "WAITING_DB_QUERY_DBNAME_2025"

        loop.run_until_complete(self.service._handle_db_query_input(123, "WAITING_DB_QUERY_DBNAME_2025", "query", update))
        loop.close()

        self.service.command_received.emit.assert_called_with("search_db_pdf", {
            "db": "dbname", "query": "query", "chat_id": "123", "year": "2025"
        })
        self.assertIsNone(self.service.user_states[123])

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

        loop.run_until_complete(self.service._handle_photo(update, context))
        loop.close()

        self.service.photo_received.emit.assert_called_with("123", b"bytes", "cap")

    def test_handle_voice(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(chat_id=123))
        update.message.voice = MagicMock(file_id="fid")

        mock_file = AsyncMock()
        mock_file.download_as_bytearray.return_value = b"audio"
        context = MagicMock()
        context.bot.get_file = AsyncMock(return_value=mock_file)

        self.service.connected_chat_id = "123"
        self.service._process_with_ai = AsyncMock()

        loop.run_until_complete(self.service._handle_voice(update, context))
        loop.close()

        self.service._process_with_ai.assert_called_with(123, b"audio", is_audio=True)

    def test_handle_utility_menus(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(data="menu_settings", chat_id=123))
        self.service.connected_chat_id = "123"

        with patch('src.core.telegram_manager.config_manager.load_config') as mock_conf:
             mock_conf.return_value = {"fornitori": ["A"]}
             loop.run_until_complete(self.service._handle_utility_menus("menu_settings", update.callback_query, 123))

        loop.close()
        update.callback_query.edit_message_text.assert_called()

    def test_handle_autopilot_toggle(self):
        loop = asyncio.new_event_loop()
        update = loop.run_until_complete(self.async_mock_update(data="toggle_autopilot", chat_id=123))

        with patch('src.core.telegram_manager.config_manager.load_config') as mock_conf:
             mock_conf.return_value = {"timbrature_autopilot_enabled": False}
             loop.run_until_complete(self.service._handle_setting_changes("toggle_autopilot", update.callback_query, 123))

        loop.close()
        self.service.command_received.emit.assert_called_with("set_autopilot", {"enabled": True})

    def test_send_message_sync_safe(self):
        self.service.loop = MagicMock()
        self.service.loop.is_running.return_value = True
        self.service.connected_chat_id = "123"

        with patch('src.core.telegram_manager.asyncio.run_coroutine_threadsafe') as mock_run:
            self.service.send_message_sync("msg")
            mock_run.assert_called()


    def test_send_photo_sync_safe(self):
        self.service.loop = MagicMock()
        self.service.loop.is_running.return_value = True
        self.service.connected_chat_id = "123"

        with patch('src.core.telegram_manager.asyncio.run_coroutine_threadsafe') as mock_run:
            self.service.send_photo_sync(b"data", "cap")
            mock_run.assert_called()

    def test_send_document_sync_safe(self):
        self.service.loop = MagicMock()
        self.service.loop.is_running.return_value = True
        self.service.connected_chat_id = "123"

        with patch('src.core.telegram_manager.asyncio.run_coroutine_threadsafe') as mock_run:
            self.service.send_document_sync("path/to/file.pdf", "cap")
            mock_run.assert_called()

