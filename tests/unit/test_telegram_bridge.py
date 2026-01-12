import unittest
from unittest.mock import MagicMock, call, patch

from PyQt6.QtWidgets import (  # Keep QWidget for reference if needed, but remove spec from MagicMock
    QApplication,
)

from src.core.telegram_bridge import TelegramUIBridge


# Mock QApplication for tests
class MockQApplication(QApplication):
    def __init__(self, *args, **kwargs):
        pass

class TestTelegramUIBridge(unittest.TestCase):

    def setUp(self):
        # Ensure a QApplication instance exists for PyQt signals
        if QApplication.instance() is None:
            self.app = MockQApplication([])
        else:
            self.app = QApplication.instance()

        self.mock_main_window = MagicMock() # No spec for main_window

        # Mock the telegram service as a plain MagicMock, allowing dynamic attributes
        self.mock_telegram_service = MagicMock() # Removed spec=QObject

        # Explicitly mock signals and their connect method
        self.mock_telegram_service.log_signal = MagicMock()
        self.mock_telegram_service.log_signal.connect = MagicMock()

        self.mock_telegram_service.command_received = MagicMock()
        self.mock_telegram_service.command_received.connect = MagicMock()

        self.mock_telegram_service.data_received = MagicMock()
        self.mock_telegram_service.data_received.connect = MagicMock()

        self.mock_telegram_service.status_requested = MagicMock()
        self.mock_telegram_service.status_requested.connect = MagicMock()

        self.mock_telegram_service.screenshot_requested = MagicMock()
        self.mock_telegram_service.screenshot_requested.connect = MagicMock()

        self.mock_telegram_service.query_received = MagicMock()
        self.mock_telegram_service.query_received.connect = MagicMock()

        self.mock_telegram_service.photo_received = MagicMock()
        self.mock_telegram_service.photo_received.connect = MagicMock()

        self.mock_telegram_service.intent_received = MagicMock()
        self.mock_telegram_service.intent_received.connect = MagicMock()

        # Explicitly mock the methods and attributes that were failing
        self.mock_telegram_service.send_message_sync = MagicMock()
        self.mock_telegram_service.send_document_sync = MagicMock()
        self.mock_telegram_service.send_photo_sync = MagicMock()
        self.mock_telegram_service.app = MagicMock() # Mock the 'app' attribute
        self.mock_telegram_service.app.bot = MagicMock() # Mock the 'bot' attribute
        self.mock_telegram_service.loop = MagicMock() # Mock the 'loop' attribute

        # Assign the mocked telegram service to the main window and bridge
        self.mock_main_window.telegram = self.mock_telegram_service
        self.bridge = TelegramUIBridge(self.mock_main_window)

    def tearDown(self):
        if hasattr(self, 'app') and self.app is not None and not isinstance(self.app, MockQApplication):
            self.app.quit()

    def test_init(self):
        self.assertEqual(self.bridge.mw, self.mock_main_window)
        self.assertEqual(self.bridge.telegram, self.mock_main_window.telegram)

    def test_setup_connections(self):
        self.bridge.setup_connections()

        self.mock_telegram_service.log_signal.connect.assert_called_once()
        self.mock_telegram_service.command_received.connect.assert_called_once()
        self.mock_telegram_service.data_received.connect.assert_called_once()
        self.mock_telegram_service.status_requested.connect.assert_called_once()
        self.mock_telegram_service.screenshot_requested.connect.assert_called_once()
        self.mock_telegram_service.query_received.connect.assert_called_once()
        self.mock_telegram_service.photo_received.connect.assert_called_once()
        self.mock_telegram_service.intent_received.connect.assert_called_once() # Corrected: intent_received is a MagicMock, not a signal

    @patch('src.core.telegram_bridge.InputValidator')
    def test_handle_intent_add_pdl(self, MockInputValidator):
        self.mock_main_window.pdl_panel = MagicMock()
        self.mock_main_window.show_toast = MagicMock()

        # Mock InputValidator.validate_pdl
        MockInputValidator.validate_pdl.side_effect = [
            MagicMock(valid=True, sanitized_value="PDL001"),
            MagicMock(valid=True, sanitized_value="PDL002")
        ]

        chat_id = 123
        intent = {"action": "add", "object": "pdl", "items": ["pdl_item_1", "pdl_item_2"]}

        self.bridge._handle_intent(chat_id, intent)

        self.mock_main_window.pdl_panel.add_rows_simple.assert_called_once_with([
            {"numero_pdl": "PDL001"},
            {"numero_pdl": "PDL002"}
        ])
        self.mock_main_window.show_toast.assert_called_once_with("Telegram: aggiunti 2 PDL via AI")

    @patch('src.core.telegram_bridge.InputValidator')
    def test_handle_intent_add_oda(self, MockInputValidator):
        self.mock_main_window.scarico_panel = MagicMock()
        self.mock_main_window.show_toast = MagicMock()

        MockInputValidator.validate_oda.side_effect = [
            MagicMock(valid=True, sanitized_value="ODA001"),
            MagicMock(valid=True, sanitized_value="ODA002")
        ]

        chat_id = 123
        intent = {"action": "add", "object": "oda", "items": ["oda_item_1", "oda_item_2"]}

        self.bridge._handle_intent(chat_id, intent)

        self.mock_main_window.scarico_panel.add_rows_simple.assert_called_once_with([
            {"numero_oda": "ODA001"},
            {"numero_oda": "ODA002"}
        ])
        self.mock_main_window.show_toast.assert_called_once_with("Telegram: aggiunti 2 OdA via AI")

    @patch('src.core.telegram_bridge.get_installed_printers')
    @patch('src.core.telegram_bridge.InlineKeyboardButton')
    @patch('src.core.telegram_bridge.InlineKeyboardMarkup')
    @patch('asyncio.run_coroutine_threadsafe')
    def test_handle_intent_print_pdl(self, mock_run_coroutine_threadsafe, MockInlineKeyboardMarkup, MockInlineKeyboardButton, mock_get_installed_printers):
        mock_get_installed_printers.return_value = ["Printer1", "Printer2"]
        self.mock_telegram_service.pending_data = {}
        self.mock_telegram_service.app.bot.send_message = MagicMock()

        chat_id = 123
        intent = {"action": "print", "object": "pdl", "items": ["PDL001", "PDL002"]}

        self.bridge._handle_intent(chat_id, intent)

        self.assertIn(int(chat_id), self.mock_telegram_service.pending_data)
        self.assertEqual(self.mock_telegram_service.pending_data[int(chat_id)]["action"], "print")
        self.assertEqual(self.mock_telegram_service.pending_data[int(chat_id)]["items"], ["PDL001", "PDL002"])
        self.mock_telegram_service.send_message_sync.assert_called_with("✅ Ho aggiunto i PDL. **Quale stampante utilizzo?**")
        MockInlineKeyboardButton.assert_has_calls([
            call("🖨️ Printer1", callback_data=f"sel_print_run_{'Printer1'[:25]}"),
            call("🖨️ Printer2", callback_data=f"sel_print_run_{'Printer2'[:25]}")
        ], any_order=True)
        MockInlineKeyboardMarkup.assert_called_once()
        mock_run_coroutine_threadsafe.assert_called_once()

    @patch('src.core.telegram_bridge.InlineKeyboardButton')
    @patch('src.core.telegram_bridge.InlineKeyboardMarkup')
    @patch('asyncio.run_coroutine_threadsafe')
    def test_handle_intent_download_pdl(self, mock_run_coroutine_threadsafe, MockInlineKeyboardMarkup, MockInlineKeyboardButton):
        self.mock_telegram_service.app.bot.send_message = MagicMock()

        chat_id = 123
        intent = {"action": "download", "object": "pdl", "items": ["PDL001", "PDL002"]}

        self.bridge._handle_intent(chat_id, intent)

        MockInlineKeyboardButton.assert_has_calls([
            call("✅ Sì, stampa", callback_data="confirm_print_yes"),
            call("❌ No, solo download", callback_data="confirm_print_no")
        ], any_order=True)
        MockInlineKeyboardMarkup.assert_called_once()
        mock_run_coroutine_threadsafe.assert_called_once()
        self.mock_telegram_service.app.bot.send_message.assert_called_once()

    def test_handle_intent_download_oda(self):
        self.mock_main_window.navigate_to_panel = MagicMock()
        self.mock_main_window.scarico_panel = MagicMock()
        self.mock_main_window.scarico_panel.validate_ready.return_value = (True, "")
        self.mock_main_window.scarico_panel.start_btn.click = MagicMock()

        chat_id = 123
        intent = {"action": "download", "object": "oda"}

        with patch.object(self.bridge, '_handle_command') as mock_handle_command:
            self.bridge._handle_intent(chat_id, intent)
            mock_handle_command.assert_called_once_with("run_ts", {})

    def test_handle_intent_download_timbrature(self):
        chat_id = 123
        intent = {"action": "download", "object": "timbrature"}

        with patch.object(self.bridge, '_handle_command') as mock_handle_command:
            self.bridge._handle_intent(chat_id, intent)
            mock_handle_command.assert_called_once_with("run_timbrature", {"period": "today"})

    def test_handle_intent_status(self):
        chat_id = 123
        intent = {"action": "status"}

        with patch.object(self.bridge, '_handle_status') as mock_handle_status:
            self.bridge._handle_intent(chat_id, intent)
            mock_handle_status.assert_called_once_with(chat_id)

    def test_handle_intent_restart(self):
        chat_id = 123
        intent = {"action": "restart"}

        with patch.object(self.bridge, '_handle_command') as mock_handle_command:
            self.bridge._handle_intent(chat_id, intent)
            mock_handle_command.assert_called_once_with("restart_app", {})


    def test_handle_command_search_db_pdf(self):
        with patch.object(self.bridge, '_handle_search_db_pdf') as mock_handler:
            self.bridge._handle_command("search_db_pdf", {"db": "timbrature"})
            mock_handler.assert_called_once_with({"db": "timbrature"})

    def test_handle_command_run_pdl(self):
        with patch.object(self.bridge, '_handle_run_pdl') as mock_handler:
            self.bridge._handle_command("run_pdl", {"print": True})
            mock_handler.assert_called_once_with({"print": True})

    def test_handle_run_pdl(self):
        self.mock_main_window.navigate_to_panel = MagicMock()
        self.mock_main_window.pdl_panel = MagicMock()
        self.mock_main_window.pdl_panel.validate_ready.return_value = (True, "")

        params = {"print": True, "merge_and_send": True, "merge_all": False}
        self.bridge._handle_run_pdl(params)

        self.mock_main_window.navigate_to_panel.assert_called_once_with("scarico_pdl")
        self.mock_main_window.pdl_panel.print_check.setChecked.assert_called_once_with(True)
        self.assertTrue(self.mock_main_window.pdl_panel.merge_and_send_from_telegram)
        self.assertFalse(self.mock_main_window.pdl_panel.merge_all_session_from_telegram)
        self.mock_main_window.pdl_panel.start_btn.click.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_called_with("✅ Avvio Scarico PDL (Stampa=True)")

    def test_handle_list_pdl(self):
        self.mock_main_window.pdl_panel = MagicMock() # Added mock for pdl_panel
        self.mock_main_window.pdl_panel.data_table.get_data.return_value = [{"col1": "item1"}, {"col1": "item2"}]
        self.bridge._handle_list_pdl()
        self.mock_telegram_service.send_message_sync.assert_called_with("📋 **Lista PDL Corrente:**\n• `item1`\n• `item2`")

    def test_handle_clear_pdl(self):
        self.mock_main_window.pdl_panel = MagicMock() # Added mock for pdl_panel
        self.mock_main_window.pdl_panel.clear_rows_simple = MagicMock()
        self.bridge._handle_clear_pdl()
        self.mock_main_window.pdl_panel.clear_rows_simple.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_called_with("🗑️ Tabella PDL svuotata.")

    def test_handle_run_ts(self):
        self.mock_main_window.navigate_to_panel = MagicMock()
        self.mock_main_window.scarico_panel = MagicMock()
        self.mock_main_window.scarico_panel.validate_ready.return_value = (True, "")

        self.bridge._handle_run_ts()

        self.mock_main_window.navigate_to_panel.assert_called_once_with("scarico_ts")
        self.mock_main_window.scarico_panel.start_btn.click.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_called_with("✅ Avvio Scarico Timesheet.")

    def test_handle_run_carico(self):
        self.mock_main_window.navigate_to_panel = MagicMock()
        self.mock_main_window.carico_panel = MagicMock()
        self.mock_main_window.carico_panel.validate_ready.return_value = (True, "")

        self.bridge._handle_run_carico()

        self.mock_main_window.navigate_to_panel.assert_called_once_with("carico_ts")
        self.mock_main_window.carico_panel.start_btn.click.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_called_with("✅ Avvio Carico Timesheet.")

    @patch('src.core.telegram_bridge.QDate')
    def test_handle_run_timbrature(self, MockQDate):
        self.mock_main_window.navigate_to_panel = MagicMock()
        self.mock_main_window.timbrature_bot_panel = MagicMock()
        self.mock_main_window.timbrature_bot_panel.validate_ready.return_value = (True, "")

        mock_date = MagicMock()
        mock_date.addDays.return_value = "yesterday_date"
        MockQDate.currentDate.return_value = mock_date

        params = {"period": "yesterday"}
        self.bridge._handle_run_timbrature(params)

        self.mock_main_window.navigate_to_panel.assert_called_once_with("timbrature")
        self.mock_main_window.timbrature_bot_panel.date_da_edit.setDate.assert_called_once_with("yesterday_date")
        self.mock_main_window.timbrature_bot_panel.date_a_edit.setDate.assert_called_once_with("yesterday_date")
        self.mock_main_window.timbrature_bot_panel.start_btn.click.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_called_with("✅ Avvio Scarico Timbrature (yesterday).")

    @patch('src.core.telegram_bridge.subprocess.Popen')
    @patch('src.core.telegram_bridge.os.path.abspath', return_value="avvio.bat")
    @patch('src.core.telegram_bridge.QApplication.quit')
    def test_handle_restart_app(self, mock_quit, mock_abspath, mock_popen):
        self.bridge._handle_restart_app()
        mock_popen.assert_called_once()
        mock_quit.assert_called_once()

    def test_handle_stop_all(self):
        # Scenario: active panel with stop button
        mock_panel = MagicMock()
        mock_panel.stop_btn.isEnabled.return_value = True
        self.mock_main_window.bot_controller = MagicMock() # Added mock for bot_controller
        self.mock_main_window.bot_controller._get_active_bot_panel.return_value = mock_panel
        self.bridge._handle_stop_all()
        mock_panel.stop_btn.click.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_called_with("🛑 Stop inviato.")

        # Scenario: no active panel
        self.mock_main_window.bot_controller._get_active_bot_panel.return_value = None
        self.mock_telegram_service.send_message_sync.reset_mock()
        self.bridge._handle_stop_all()
        self.mock_telegram_service.send_message_sync.assert_called_with("ℹ️ Nessun processo attivo.")

    @patch('src.core.telegram_bridge.config_manager')
    @patch('src.core.telegram_bridge.generate_pdf_from_html')
    @patch('src.core.telegram_bridge.os.path.exists', return_value=True)
    @patch('src.core.telegram_bridge.datetime')
    def test_handle_search_db_pdf_timbrature(self, mock_datetime, mock_exists, mock_generate_pdf, mock_config_manager):
        mock_config_manager.CONFIG_DIR = MagicMock()
        mock_config_manager.CONFIG_DIR.__truediv__.return_value.mkdir = MagicMock()
        mock_config_manager.CONFIG_DIR.__truediv__.return_value.__truediv__.return_value = "temp/report.pdf"

        mock_datetime.now.return_value.timestamp.return_value = 12345
        self.mock_main_window.timbrature_db_panel = MagicMock() # Added mock for timbrature_db_panel
        self.mock_main_window.timbrature_db_panel.storage.get_timbrature_with_reparto.return_value = [
            ["2023-01-01", "08:00", "17:00", "Nome", "Cognome"]
        ]

        params = {"db": "timbrature", "query": "test"}
        self.bridge._handle_search_db_pdf(params)

        self.mock_telegram_service.send_message_sync.assert_any_call("🔍 Ricerca in corso in **timbrature** per: `test`...")
        mock_generate_pdf.assert_called_once()
        self.mock_telegram_service.send_document_sync.assert_called_once_with("temp/report.pdf", caption="📄 Report timbrature")

    @patch('src.core.telegram_bridge.config_manager')
    @patch('src.core.telegram_bridge.generate_pdf_from_html')
    @patch('src.core.telegram_bridge.os.path.exists', return_value=True)
    @patch('src.core.telegram_bridge.datetime')
    @patch('src.core.telegram_bridge.ContabilitaManager')
    def test_handle_search_db_pdf_strumentale(self, MockContabilitaManager, mock_datetime, mock_exists, mock_generate_pdf, mock_config_manager):
        mock_config_manager.CONFIG_DIR = MagicMock()
        mock_config_manager.CONFIG_DIR.__truediv__.return_value.mkdir = MagicMock()
        mock_config_manager.CONFIG_DIR.__truediv__.return_value.__truediv__.return_value = "temp/report.pdf"

        mock_datetime.now.return_value.timestamp.return_value = 12345
        MockContabilitaManager.search_extended.return_value = {
            "GIORNALIERE": [{"data": "2023-01-01", "personale": "P1", "descrizione": "D1"}]
        }

        params = {"db": "strumentale", "query": "test"}
        self.bridge._handle_search_db_pdf(params)

        self.mock_telegram_service.send_message_sync.assert_any_call("🔍 Ricerca in corso in **strumentale** per: `test`...")
        mock_generate_pdf.assert_called_once()
        self.mock_telegram_service.send_document_sync.assert_called_once_with("temp/report.pdf", caption="📄 Report strumentale")

    @patch('src.core.telegram_bridge.InputValidator')
    def test_handle_data_pdl(self, MockInputValidator):
        self.mock_main_window.pdl_panel = MagicMock()
        self.mock_main_window.scarico_panel = MagicMock()
        self.mock_main_window.show_toast = MagicMock()

        self.mock_main_window.pdl_panel.data_table.get_data.return_value = [{"numero_pdl": "PDL001"}]
        MockInputValidator.validate_pdl.side_effect = [
            MagicMock(valid=True, sanitized_value="PDL002"),
            MagicMock(valid=True, sanitized_value="PDL001"), # Duplicate
            MagicMock(valid=False, error="Invalid format")
        ]

        data_type = "pdl"
        items = ["PDL002", "PDL001", "INVALID_PDL"]
        self.bridge._handle_data(data_type, items)

        self.mock_main_window.pdl_panel.add_rows_simple.assert_called_once_with([{"numero_pdl": "PDL002"}])
        self.mock_main_window.navigate_to_panel.assert_called_once_with(self.mock_main_window.pdl_panel.bot_id)
        self.mock_main_window.show_toast.assert_called_once_with("Telegram: Aggiunti 1 elementi")
        self.mock_telegram_service.send_message_sync.assert_called_with("✅ Aggiunti 1\nℹ️ 1 duplicati saltati\n⚠️ Errori:\n❌ `INVALID_PDL`: Invalid format")

    def test_handle_status(self):
        # Scenario: active panel with status
        mock_panel = MagicMock()
        mock_panel.get_current_status.return_value = ("Running", "Bot is active")
        mock_panel.bot_name = "TestBot"
        self.mock_main_window._get_active_bot_panel = MagicMock(return_value=mock_panel) # Added mock for _get_active_bot_panel
        self.bridge._handle_status(123)
        self.mock_telegram_service.send_message_sync.assert_called_with("📊 **Stato Sistema**\n\nAttività: TestBot\nStato: Running\nDettaglio: Bot is active")

        # Scenario: no active panel
        self.mock_main_window._get_active_bot_panel.return_value = None
        self.mock_telegram_service.send_message_sync.reset_mock()
        self.bridge._handle_status(123)
        self.mock_telegram_service.send_message_sync.assert_called_with("📊 **Stato Sistema**\n\nIl sistema è in attesa (Idle).")

    @patch('src.core.telegram_bridge.QGuiApplication')
    @patch('src.core.telegram_bridge.QPixmap')
    @patch('src.core.telegram_bridge.QPainter')
    @patch('src.core.telegram_bridge.QBuffer')
    @patch('src.core.telegram_bridge.QIODevice')
    def test_handle_screenshot_app(self, MockQIODevice, MockQBuffer, MockQPainter, MockQPixmap, MockQGuiApplication):
        self.mock_main_window.grab.return_value = MagicMock()
        mock_buffer_instance = MagicMock()
        mock_buffer_instance.data.return_value.data.return_value = b"screenshot_bytes"
        MockQBuffer.return_value = mock_buffer_instance

        self.bridge._handle_screenshot(mode="app")

        self.mock_main_window.grab.assert_called_once()
        mock_buffer_instance.open.assert_called_once_with(MockQIODevice.OpenModeFlag.WriteOnly)
        self.mock_main_window.grab.return_value.save.assert_called_once_with(mock_buffer_instance, "PNG")
        self.mock_telegram_service.send_photo_sync.assert_called_once_with(b"screenshot_bytes", caption="📸 **Screenshot: Solo App**")

    @patch('src.core.telegram_bridge.SecretsManager')
    @patch('src.core.telegram_bridge.threading.Thread')
    @patch('src.core.telegram_bridge.LyraClient')
    def test_handle_ai_query(self, MockLyraClient, MockThread, MockSecretsManager):
        MockSecretsManager.get_gemini_api_key.return_value = "fake_api_key"
        mock_lyra_client_instance = MagicMock()
        mock_lyra_client_instance.ask.return_value = "AI response"
        MockLyraClient.return_value = mock_lyra_client_instance

        self.bridge._handle_ai_query(123, "What is the weather?")

        MockSecretsManager.get_gemini_api_key.assert_called_once()
        MockThread.assert_called_once()
        # Verify the target function of the thread
        args, kwargs = MockThread.call_args
        target_func = kwargs['target']
        # Execute the target function to check its internal calls
        target_func()
        MockLyraClient.assert_called_once_with(api_key="fake_api_key")
        mock_lyra_client_instance.ask.assert_called_once_with("What is the weather?")
        self.mock_telegram_service.send_message_sync.assert_any_call("🤖 **AI Coach**\n\nAI response")


    @patch('src.core.telegram_bridge.SecretsManager')
    @patch('src.core.telegram_bridge.threading.Thread')
    @patch('src.core.telegram_bridge.LyraClient')
    @patch('src.core.telegram_bridge.base64')
    def test_handle_photo(self, MockBase64, MockLyraClient, MockThread, MockSecretsManager):
        MockSecretsManager.get_gemini_api_key.return_value = "fake_api_key"
        mock_lyra_client_instance = MagicMock()
        mock_lyra_client_instance.ask.return_value = "Photo analysis response"
        MockLyraClient.return_value = mock_lyra_client_instance
        MockBase64.b64encode.return_value.decode.return_value = "base64_photo_string"

        photo_bytes = b"fake_photo_bytes"
        caption = "Analyze this image"
        self.bridge._handle_photo(123, photo_bytes, caption)

        MockSecretsManager.get_gemini_api_key.assert_called_once()
        self.mock_telegram_service.send_message_sync.assert_any_call("🔍 **Analisi Documento...**")
        MockThread.assert_called_once()

        # Execute the target function of the thread
        args, kwargs = MockThread.call_args
        target_func = kwargs['target']
        target_func()

        MockBase64.b64encode.assert_called_once_with(photo_bytes)
        MockLyraClient.assert_called_once_with(api_key="fake_api_key")
        mock_lyra_client_instance.ask.assert_called_once_with(
            "Estrai dati da questo rapportino. Tabella Markdown.\nNote: Analyze this image",
            images=["base64_photo_string"]
        )
        self.mock_telegram_service.send_message_sync.assert_any_call("📝 **Dati Estratti**\n\nPhoto analysis response")


if __name__ == '__main__':
    unittest.main()
