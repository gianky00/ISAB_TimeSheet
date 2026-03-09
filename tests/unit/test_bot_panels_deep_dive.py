from unittest.mock import MagicMock, patch
import pytest
from src.gui.panels.scarico_pdl import ScaricoPDLPanel

@pytest.fixture
def mock_gui_deps(mocker):
    # Mocking external services
    mocker.patch("src.core.database.db_manager", MagicMock())
    mocker.patch("src.core.lyra_sentinel.LyraSentinel", return_value=MagicMock())
    mocker.patch("src.core.telegram_manager.TelegramService", return_value=MagicMock())
    return MagicMock()

class TestScaricoPDLPanel:
    @patch("src.gui.panels.base.BotWorker")
    def test_telegram_send_after_finish(self, mock_worker_cls, qapp, qtbot, mock_gui_deps):
        panel = ScaricoPDLPanel()
        mock_win = MagicMock()
        mock_tg = MagicMock()
        mock_win.telegram = mock_tg
        
        with patch.object(panel, "window", return_value=mock_win):
            qtbot.addWidget(panel)

            # Ensure table is empty first
            panel.data_table.table.setRowCount(0)
            panel.data_table.set_data([{"N° PDL": "999"}])
            panel.merge_and_send_from_telegram = True

            with (
                patch.object(panel, "get_credentials", return_value=("u", "p")),
                patch("src.gui.panels.scarico_pdl.Path.exists", return_value=True),
            ):
                panel._on_start()
                
                # Configure the mock worker instance created by _on_start
                mock_worker = mock_worker_cls.return_value
                panel.worker = mock_worker # Ensure it's set
                
                mock_worker.bot = MagicMock()
                mock_worker.bot.downloaded_files = ["/path/to/report.pdf"]
                
                panel._on_worker_finished(True)

                mock_win.telegram.send_document_sync.assert_called()

    def test_validate_ready(self, qtbot, mock_gui_deps):
        panel = ScaricoPDLPanel()
        qtbot.addWidget(panel)
        
        # Explicitly clear table to avoid default rows interference
        panel.data_table.table.setRowCount(0)
        
        # Test empty
        ready, msg = panel.validate_ready()
        assert ready is False
        assert "OdA" in msg or "PDL" in msg

        # Test with data
        panel.data_table.set_data([{"N° PDL": "123"}])
        ready, msg = panel.validate_ready()
        assert ready is True

    def test_on_start_workflow(self, qtbot, mock_gui_deps):
        panel = ScaricoPDLPanel()
        qtbot.addWidget(panel)
        panel.data_table.set_data([{"N° PDL": "123"}])
        
        with (
            patch.object(panel, "get_bot_instance", return_value=MagicMock()),
            patch.object(panel, "get_safework_credentials", return_value=("u", "p", "E")),
        ):
            panel._on_start()
            assert panel.worker is not None
            panel.worker.stop()
            panel.worker.wait()
