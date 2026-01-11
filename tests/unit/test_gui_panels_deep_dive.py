import pytest
import threading
from unittest.mock import MagicMock, patch
from src.gui.panels import BotWorker, BaseBotPanel

class TestGUIWorkerAndBase:
    def test_bot_worker_run(self, qtbot):
        mock_bot = MagicMock()
        mock_bot.execute.return_value = True
        worker = BotWorker(mock_bot, {"data": 1})
        
        # Use qtbot to wait for signal emission
        with qtbot.wait_signal(worker.finished_signal, timeout=1000) as blocker:
            worker.run()
        
        assert blocker.args[0] is True
        mock_bot.execute.assert_called_once()

    def test_bot_worker_exception(self, qtbot):
        mock_bot = MagicMock()
        mock_bot.execute.side_effect = Exception("Fatal")
        worker = BotWorker(mock_bot, {})
        
        with qtbot.wait_signal(worker.finished_signal, timeout=1000) as blocker:
            worker.run()
        
        assert blocker.args[0] is False

    def test_base_bot_panel_status_updates(self, qapp, qtbot):
        panel = BaseBotPanel("test_id", "TestBot", "Desc")
        qtbot.addWidget(panel)
        
        # Mock the signal itself, not the emit method
        mock_signal = MagicMock()
        panel.status_changed = mock_signal
        
        panel._update_status("running", "In corso...")
        mock_signal.emit.assert_called_with("running", "In corso...")
            
    def test_base_bot_panel_rows_management(self, qapp, qtbot):
        panel = BaseBotPanel("test_id", "TestBot", "Desc")
        qtbot.addWidget(panel)
        panel.data_table = MagicMock()
        panel.data_table.get_data.return_value = []
        
        panel.add_rows_simple([{"a": 1}])
        panel.data_table.set_data.assert_called()