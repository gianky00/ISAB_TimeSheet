from unittest.mock import MagicMock, patch

import pytest


class TestTelegramUIBridge:
    @pytest.fixture
    def mock_main_window(self):
        mw = MagicMock()
        mw.telegram = MagicMock()
        mw.telegram.pending_data = {}
        mw.pdl_panel = MagicMock()
        mw.pdl_panel.data_table.get_data.return_value = []
        mw.scarico_panel = MagicMock()
        mw.scarico_panel.data_table.get_data.return_value = []
        return mw

    @pytest.fixture
    def bridge(self, mock_main_window):
        with patch("src.core.telegram_bridge.QObject.__init__"):
            from src.core.telegram_bridge import TelegramUIBridge

            b = TelegramUIBridge(mock_main_window)
            b.mw = mock_main_window
            b.telegram = mock_main_window.telegram
            return b

    def test_setup_connections(self, bridge):
        bridge.setup_connections()
        bridge.telegram.command_received.connect.assert_called()
        bridge.telegram.status_requested.connect.assert_called()

    def test_handle_command_run_ts(self, bridge):
        bridge.mw.scarico_panel.validate_ready.return_value = (True, "OK")

        bridge._handle_command("run_ts", {})

        bridge.mw.navigate_to_panel.assert_called_with("scarico_ts")
        bridge.mw.scarico_panel.start_btn.click.assert_called()

    def test_handle_command_list_pdl(self, bridge):
        bridge.mw.pdl_panel.data_table.get_data.return_value = [
            {"numero_pdl": "12345/A"},
            {"numero_pdl": "67890/B"},
        ]

        bridge._handle_list_pdl()

        bridge.telegram.send_message_sync.assert_called()
        call_args = bridge.telegram.send_message_sync.call_args[0][0]
        assert "12345/A" in call_args

    def test_handle_command_clear_pdl(self, bridge):
        bridge._handle_clear_pdl()

        bridge.mw.pdl_panel.clear_rows_simple.assert_called()
        bridge.telegram.send_message_sync.assert_called()

    def test_handle_command_stop_all_active(self, bridge):
        mock_panel = MagicMock()
        mock_panel.stop_btn.isEnabled.return_value = True
        bridge.mw.bot_controller._get_active_bot_panel.return_value = mock_panel

        bridge._handle_stop_all()

        mock_panel.stop_btn.click.assert_called()

    def test_handle_command_stop_all_no_active(self, bridge):
        bridge.mw.bot_controller._get_active_bot_panel.return_value = None

        bridge._handle_stop_all()

        call_args = bridge.telegram.send_message_sync.call_args[0][0]
        assert "Nessun processo" in call_args

    def test_handle_status_idle(self, bridge):
        bridge.mw._get_active_bot_panel.return_value = None

        bridge._handle_status(123456)

        call_args = bridge.telegram.send_message_sync.call_args[0][0]
        assert "Idle" in call_args

    @patch("src.core.telegram_bridge.InputValidator")
    def test_process_pdl_items_valid(self, mock_validator, bridge):
        mock_result = MagicMock()
        mock_result.valid = True
        mock_result.sanitized_value = "12345/A"
        mock_validator.validate_pdl.return_value = mock_result

        bridge._process_pdl_items(["12345/A"])

        bridge.mw.pdl_panel.add_rows_simple.assert_called()

    @patch("src.core.telegram_bridge.InputValidator")
    def test_add_pdl_from_telegram(self, mock_validator, bridge):
        mock_result = MagicMock()
        mock_result.valid = True
        mock_result.sanitized_value = "12345/A"
        mock_validator.validate_pdl.return_value = mock_result

        bridge._add_pdl_from_telegram(["12345/A"])

        bridge.mw.pdl_panel.add_rows_simple.assert_called()
        bridge.mw.show_toast.assert_called()

    def test_handle_intent_status(self, bridge):
        bridge.mw._get_active_bot_panel.return_value = None

        bridge._handle_intent(123, {"action": "status", "object": None, "items": []})

        bridge.telegram.send_message_sync.assert_called()

    def test_send_data_feedback_valid(self, bridge):
        bridge._send_data_feedback(5, 2, [])

        call_args = bridge.telegram.send_message_sync.call_args[0][0]
        assert "5" in call_args
        assert "2 duplicati" in call_args
