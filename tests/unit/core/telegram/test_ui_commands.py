from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QDate, QObject

from src.api.telegram.bridge.ui_commands import TelegramUICommands


class TestTelegramUICommands:
    @pytest.fixture
    def mock_mw(self):
        m = QObject()
        m.navigation_controller = MagicMock()
        m.bot_controller = MagicMock()
        m.pdl_panel = MagicMock()
        m.scarico_panel = MagicMock()
        m.carico_panel = MagicMock()
        m.timbrature_bot_panel = MagicMock()
        return m

    @pytest.fixture
    def mock_tg(self):
        return MagicMock()

    def test_run_pdl_bot_success(self, mock_mw, mock_tg):
        cmds = TelegramUICommands(mock_mw, mock_tg)
        mock_mw.pdl_panel.validate_ready.return_value = (True, "")

        cmds.run_pdl_bot({"print": True, "merge_all": True})

        assert mock_mw.navigation_controller.navigate_to_panel.called
        assert mock_mw.pdl_panel.print_check.setChecked.called
        assert mock_mw.pdl_panel.start_btn.click.called
        assert "Avvio Scarico PDL" in mock_tg.send_message_sync.call_args[0][0]

    def test_run_pdl_bot_fail(self, mock_mw, mock_tg):
        cmds = TelegramUICommands(mock_mw, mock_tg)
        mock_mw.pdl_panel.validate_ready.return_value = (False, "Mancano dati")

        cmds.run_pdl_bot({})

        assert not mock_mw.pdl_panel.start_btn.click.called
        assert "Impossibile avviare" in mock_tg.send_message_sync.call_args[0][0]

    def test_list_pdl(self, mock_mw, mock_tg):
        cmds = TelegramUICommands(mock_mw, mock_tg)
        mock_mw.pdl_panel.data_table.get_data.return_value = [{"pdl": "100"}, {"pdl": "200"}]

        cmds.list_pdl()
        assert "100" in mock_tg.send_message_sync.call_args[0][0]

    def test_clear_pdl(self, mock_mw, mock_tg):
        cmds = TelegramUICommands(mock_mw, mock_tg)
        cmds.clear_pdl()
        assert mock_mw.pdl_panel.clear_rows_simple.called

    def test_run_ts_bot(self, mock_mw, mock_tg):
        cmds = TelegramUICommands(mock_mw, mock_tg)
        mock_mw.scarico_panel.validate_ready.return_value = (True, "")
        cmds.run_ts_bot()
        assert mock_mw.scarico_panel.start_btn.click.called

    def test_run_timbrature_bot_yesterday(self, mock_mw, mock_tg):
        cmds = TelegramUICommands(mock_mw, mock_tg)
        mock_mw.timbrature_bot_panel.validate_ready.return_value = (True, "")

        cmds.run_timbrature_bot({"period": "yesterday"})

        expected_date = QDate.currentDate().addDays(-1)
        mock_mw.timbrature_bot_panel.date_da_edit.setDate.assert_called_with(expected_date)
        assert mock_mw.timbrature_bot_panel.start_btn.click.called

    def test_stop_all_bots(self, mock_mw, mock_tg):
        cmds = TelegramUICommands(mock_mw, mock_tg)
        mock_panel = MagicMock()
        mock_mw.bot_controller._get_active_bot_panel.return_value = mock_panel
        mock_panel.stop_btn.isEnabled.return_value = True

        cmds.stop_all_bots()
        assert mock_panel.stop_btn.click.called
        assert "Stop inviato" in mock_tg.send_message_sync.call_args[0][0]
