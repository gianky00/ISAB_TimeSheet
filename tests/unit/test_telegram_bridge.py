import unittest
from unittest.mock import MagicMock, call, patch
import asyncio

from PyQt6.QtWidgets import QApplication
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

        self.mock_main_window = MagicMock()  # No spec for main_window

        # Mock the telegram service as a plain MagicMock, allowing dynamic attributes
        self.mock_telegram_service = MagicMock()

        # Explicitly mock signals and their connect method
        for sig in ['log_signal', 'command_received', 'data_received', 'status_requested', 
                   'screenshot_requested', 'query_received', 'photo_received', 'intent_received']:
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
        if (
            hasattr(self, "app")
            and self.app is not None
            and not isinstance(self.app, MockQApplication)
        ):
            self.app.quit()

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
        # Verify navigation called with string
        self.mock_main_window.navigate_to_panel.assert_called_once_with("scarico_pdl")

    @patch("PyQt6.QtCore.QDate")
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
        self.mock_main_window.timbrature_bot_panel.start_btn.click.assert_called_once()

    @patch("src.core.telegram_bridge.subprocess.Popen")
    @patch("src.core.telegram_bridge.os.path.abspath", return_value="avvio.bat")
    @patch("src.core.telegram_bridge.QApplication.quit")
    def test_handle_restart_app(self, mock_quit, mock_abspath, mock_popen):
        self.bridge._handle_restart_app()
        mock_popen.assert_called_once()
        mock_quit.assert_called_once()

if __name__ == "__main__":
    unittest.main()