import unittest
from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QApplication

from src.core.telegram_bridge import TelegramUIBridge


class TestTelegramUIBridge(unittest.TestCase):
    def setUp(self):
        # Ensure a QApplication instance exists (provided by pytest-qt in full suite)
        self.app = QApplication.instance()

        self.mock_main_window = MagicMock()

        # Mock the telegram service as a plain MagicMock
        self.mock_telegram_service = MagicMock()

        # Explicitly mock signals and their connect method
        for sig in [
            "log_signal",
            "command_received",
            "data_received",
            "status_requested",
            "screenshot_requested",
            "query_received",
            "photo_received",
            "intent_received",
        ]:
            setattr(self.mock_telegram_service, sig, MagicMock())
            getattr(self.mock_telegram_service, sig).connect = MagicMock()

        # Explicitly mock the methods and attributes
        self.mock_telegram_service.send_message_sync = MagicMock()
        self.mock_telegram_service.send_document_sync = MagicMock()
        self.mock_telegram_service.send_photo_sync = MagicMock()
        self.mock_telegram_service.pending_data = {}
        self.mock_telegram_service.app = MagicMock()
        self.mock_telegram_service.app.bot = MagicMock()
        self.mock_telegram_service.loop = MagicMock()

        # Assign the mocked telegram service to the main window and bridge
        self.mock_main_window.telegram = self.mock_telegram_service
        self.bridge = TelegramUIBridge(self.mock_main_window)

    def tearDown(self):
        # Cleanup mocked app if needed
        pass

    def test_init(self):
        self.assertEqual(self.bridge.mw, self.mock_main_window)
        self.assertEqual(self.bridge.telegram, self.mock_main_window.telegram)

    def test_setup_connections(self):
        self.bridge.setup_connections()
        self.mock_telegram_service.log_signal.connect.assert_called_once()
        self.mock_telegram_service.command_received.connect.assert_called_once()

    @patch("src.core.telegram_bridge.InputValidator")
    def test_handle_intent_add_pdl(self, MockInputValidator):
        self.mock_main_window.pdl_panel = MagicMock()
        self.mock_main_window.show_toast = MagicMock()

        MockInputValidator.validate_pdl.side_effect = [
            MagicMock(valid=True, sanitized_value="PDL001"),
            MagicMock(valid=True, sanitized_value="PDL002"),
            MagicMock(valid=True, sanitized_value="PDL001"),
            MagicMock(valid=True, sanitized_value="PDL002"),
        ]

        chat_id = 123
        intent = {
            "action": "add",
            "object": "pdl",
            "items": ["pdl_item_1", "pdl_item_2"],
        }

        self.bridge._handle_intent(chat_id, intent)

        self.mock_main_window.pdl_panel.add_rows_simple.assert_called_once_with(
            [{"numero_pdl": "PDL001"}, {"numero_pdl": "PDL002"}]
        )

    @patch("src.core.telegram_bridge.get_installed_printers")
    @patch("src.core.telegram_bridge.InlineKeyboardButton")
    @patch("src.core.telegram_bridge.InlineKeyboardMarkup")
    @patch("asyncio.run_coroutine_threadsafe")
    def test_handle_intent_print_pdl(
        self,
        mock_run_coroutine_threadsafe,
        MockInlineKeyboardMarkup,
        MockInlineKeyboardButton,
        mock_get_installed_printers,
    ):
        mock_get_installed_printers.return_value = ["Printer1"]
        self.mock_telegram_service.pending_data = {}
        self.mock_telegram_service.app.bot.send_message = MagicMock()

        chat_id = 123
        intent = {"action": "print", "object": "pdl", "items": ["PDL001"]}

        self.bridge._handle_intent(chat_id, intent)

        self.assertIn(int(chat_id), self.mock_telegram_service.pending_data)
        self.assertEqual(
            self.mock_telegram_service.pending_data[int(chat_id)]["action"], "print"
        )

    @patch("src.core.telegram_bridge.InputValidator")
    def test_handle_data_pdl(self, MockInputValidator):
        self.mock_main_window.pdl_panel = MagicMock()
        self.mock_main_window.scarico_panel = MagicMock()
        self.mock_main_window.show_toast = MagicMock()
        self.mock_main_window.navigate_to_panel = MagicMock()

        # Setup specific mock attribute
        self.mock_main_window.pdl_panel.bot_id = "scarico_pdl"

        self.mock_main_window.pdl_panel.data_table.get_data.return_value = [
            {"numero_pdl": "PDL001"}
        ]
        MockInputValidator.validate_pdl.side_effect = [
            MagicMock(valid=True, sanitized_value="PDL002"),
            MagicMock(valid=True, sanitized_value="PDL001"),  # Duplicate
            MagicMock(valid=False, error="Invalid format"),
        ]

        data_type = "pdl"
        items = ["PDL002", "PDL001", "INVALID_PDL"]
        self.bridge._handle_data(data_type, items)

        self.mock_main_window.pdl_panel.add_rows_simple.assert_called_once_with(
            [{"numero_pdl": "PDL002"}]
        )
        self.mock_main_window.navigate_to_panel.assert_called_once_with("scarico_pdl")
        self.mock_telegram_service.send_message_sync.assert_called_with(
            "✅ Aggiunti/Impostati 1\nℹ️ 1 duplicati ignorati\n⚠️ Errori:\n❌ `INVALID_PDL`: Invalid format"
        )

    def test_handle_status(self):
        mock_panel = MagicMock()
        mock_panel.get_current_status.return_value = ("Running", "Bot is active")
        mock_panel.bot_name = "TestBot"
        self.mock_main_window._get_active_bot_panel = MagicMock(return_value=mock_panel)
        self.bridge._handle_status(123)
        self.mock_telegram_service.send_message_sync.assert_called_with(
            "📊 **Stato Sistema**\n\nAttività: TestBot\nStato: Running\nDettaglio: Bot is active"
        )

        self.mock_main_window._get_active_bot_panel.return_value = None
        self.mock_telegram_service.send_message_sync.reset_mock()
        self.bridge._handle_status(123)
        self.mock_telegram_service.send_message_sync.assert_called_with(
            "📊 **Stato Sistema**\n\nIl sistema è in attesa (Idle)."
        )

    @patch("src.core.telegram_bridge.QGuiApplication")
    @patch("src.core.telegram_bridge.QPixmap")
    @patch("src.core.telegram_bridge.QPainter")
    @patch("src.core.telegram_bridge.QBuffer")
    @patch("src.core.telegram_bridge.QIODevice")
    def test_handle_screenshot_app(
        self, MockQIODevice, MockQBuffer, MockQPainter, MockQPixmap, MockQGuiApplication
    ):
        self.mock_main_window.grab.return_value = MagicMock()
        mock_buffer_instance = MagicMock()
        mock_buffer_instance.data.return_value.data.return_value = b"screenshot_bytes"
        MockQBuffer.return_value = mock_buffer_instance

        self.bridge._handle_screenshot(mode="app")

        self.mock_main_window.grab.assert_called_once()
        mock_buffer_instance.open.assert_called_once_with(
            MockQIODevice.OpenModeFlag.WriteOnly
        )
        self.mock_main_window.grab.return_value.save.assert_called_once_with(
            mock_buffer_instance, "PNG"
        )
        self.mock_telegram_service.send_photo_sync.assert_called_once_with(
            b"screenshot_bytes", caption="📸 **Screenshot: Solo App**"
        )

    @patch("src.core.telegram_bridge.SecretsManager")
    @patch("src.core.telegram_bridge.threading.Thread")
    @patch("src.core.telegram_bridge.LyraClient")
    def test_handle_ai_query(self, MockLyraClient, MockThread, MockSecretsManager):
        MockSecretsManager.get_gemini_api_key.return_value = "fake_api_key"
        mock_lyra_client_instance = MagicMock()
        mock_lyra_client_instance.ask.return_value = "AI response"
        MockLyraClient.return_value = mock_lyra_client_instance

        self.bridge._handle_ai_query(123, "What is the weather?")

        MockSecretsManager.get_gemini_api_key.assert_called_once()
        MockThread.assert_called_once()
        args, kwargs = MockThread.call_args
        target_func = kwargs["target"]
        target_func()
        MockLyraClient.assert_called_once_with(api_key="fake_api_key")
        mock_lyra_client_instance.ask.assert_called_once_with("What is the weather?")
        self.mock_telegram_service.send_message_sync.assert_any_call(
            "🤖 **AI Coach**\n\nAI response"
        )

    @patch("src.core.telegram_bridge.SecretsManager")
    @patch("src.core.telegram_bridge.threading.Thread")
    @patch("src.core.telegram_bridge.LyraClient")
    @patch("src.core.telegram_bridge.base64")
    def test_handle_photo(
        self,
        MockBase64,
        MockLyraClient,
        MockThread,
        MockSecretsManager,
    ):
        MockSecretsManager.get_gemini_api_key.return_value = "fake_api_key"
        mock_lyra_client_instance = MagicMock()
        mock_lyra_client_instance.ask.return_value = "Photo analysis response"
        MockLyraClient.return_value = mock_lyra_client_instance
        MockBase64.b64encode.return_value.decode.return_value = "base64_photo_string"

        photo_bytes = b"fake_photo_bytes"
        caption = "Analyze this image"
        self.bridge._handle_photo(123, photo_bytes, caption)

        MockSecretsManager.get_gemini_api_key.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_any_call(
            "🔍 **Analisi Documento...**"
        )
        MockThread.assert_called_once()

        args, kwargs = MockThread.call_args
        target_func = kwargs["target"]
        target_func()

        MockLyraClient.assert_called_once_with(api_key="fake_api_key")
        mock_lyra_client_instance.ask.assert_called_once_with(
            "Estrai dati da questo rapportino. Tabella Markdown.\nNote: Analyze this image",
            images=["base64_photo_string"],
        )
        self.mock_telegram_service.send_message_sync.assert_any_call(
            "📝 **Dati Estratti**\n\nPhoto analysis response"
        )

    @patch("src.core.telegram_bridge.subprocess")
    @patch("src.core.telegram_bridge.os.path.abspath", return_value="avvio.bat")
    @patch("src.core.telegram_bridge.QApplication.quit")
    def test_handle_restart_app(self, mock_quit, mock_abspath, mock_subprocess):
        self.bridge._handle_restart_app()
        mock_subprocess.Popen.assert_called_once()
        mock_quit.assert_called_once()

    @patch("src.core.telegram_bridge.QDate")
    def test_handle_run_timbrature(self, MockQDate):
        self.mock_main_window.navigate_to_panel = MagicMock()
        self.mock_main_window.timbrature_bot_panel = MagicMock()
        self.mock_main_window.timbrature_bot_panel.validate_ready.return_value = (
            True,
            "",
        )

        mock_date = MagicMock()
        mock_date.addDays.return_value = "yesterday_date"
        MockQDate.currentDate.return_value = mock_date

        params = {"period": "yesterday"}
        self.bridge._handle_run_timbrature(params)

        self.mock_main_window.navigate_to_panel.assert_called_once_with("timbrature")
        self.mock_main_window.timbrature_bot_panel.date_da_edit.setDate.assert_called_once_with(
            "yesterday_date"
        )
        self.mock_main_window.timbrature_bot_panel.date_a_edit.setDate.assert_called_once_with(
            "yesterday_date"
        )
        self.mock_main_window.timbrature_bot_panel.start_btn.click.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_called_with(
            "✅ Avvio Scarico Timbrature (ieri)."
        )


if __name__ == "__main__":
    unittest.main()
