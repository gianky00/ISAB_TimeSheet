from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QObject

from src.core.telegram_bridge import TelegramUIBridge


class TestTelegramBridge:
    @pytest.fixture
    def mock_mw(self):
        m = QObject()
        m.telegram = MagicMock()
        return m

    def test_init_and_setup(self, mock_mw):
        with patch("src.core.telegram_bridge.TelegramGUIBridge"):
            with patch("src.core.telegram_bridge.TelegramUICommands"):
                with patch("src.core.telegram_bridge.TelegramDataProcessor"):
                    with patch("src.core.telegram_bridge.TelegramSystemHandler"):
                        with patch("src.core.telegram_bridge.TelegramIntentHandler"):
                            bridge = TelegramUIBridge(mock_mw)

                            bridge.setup_connections()

                            assert mock_mw.telegram.log_signal.connect.called
                            assert mock_mw.telegram.command_received.connect.called
                            assert mock_mw.telegram.data_received.connect.called
                            assert mock_mw.telegram.status_requested.connect.called
                            assert mock_mw.telegram.screenshot_requested.connect.called
                            assert mock_mw.telegram.intent_received.connect.called

    def test_dispatch_command(self, mock_mw):
        with patch("src.core.telegram_bridge.TelegramGUIBridge"):
            with patch("src.core.telegram_bridge.TelegramUICommands"):
                with patch("src.core.telegram_bridge.TelegramDataProcessor"):
                    with patch("src.core.telegram_bridge.TelegramSystemHandler"):
                        with patch("src.core.telegram_bridge.TelegramIntentHandler"):
                            bridge = TelegramUIBridge(mock_mw)
                            bridge.system_handler = MagicMock()
                            bridge.ui_commands = MagicMock()

                            # Test specific commands
                            bridge._dispatch_command("search_db_pdf", {"query": "test"})
                            assert bridge.system_handler.handle_search_db_pdf.called

                            bridge._dispatch_command("run_pdl", {"print": True})
                            assert bridge.ui_commands.run_pdl_bot.called

                            bridge._dispatch_command("list_pdl", {})
                            assert bridge.ui_commands.list_pdl.called

                            bridge._dispatch_command("restart_app", {})
                            assert bridge.system_handler.handle_restart_app.called

                            bridge._dispatch_command("unknown", {})

    def test_dispatch_data(self, mock_mw):
        with patch("src.core.telegram_bridge.TelegramGUIBridge"):
            with patch("src.core.telegram_bridge.TelegramUICommands"):
                with patch("src.core.telegram_bridge.TelegramDataProcessor"):
                    with patch("src.core.telegram_bridge.TelegramSystemHandler"):
                        with patch("src.core.telegram_bridge.TelegramIntentHandler"):
                            bridge = TelegramUIBridge(mock_mw)
                            bridge.data_processor = MagicMock()

                            bridge._dispatch_data("pdl", ["123", "456"])
                            assert bridge.data_processor.process_pdl_items.called
                            assert bridge.data_processor.process_pdl_items.call_args[0][0] == ["123", "456"]

                            bridge._dispatch_data("oda", ["ODA1"])
                            assert bridge.data_processor.process_oda_items.called

                            bridge._dispatch_data("bp", ["BP1"])
                            assert bridge.data_processor.process_bp_items.called

                            bridge._dispatch_data("unknown", ["x"])
