from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels.scarico_pdl import ScaricoPDLPanel


@pytest.fixture
def mock_gui_deps(mocker):
    # Mocking external services
    mocker.patch("src.application.services.database.db_manager", MagicMock())
    # Note: LyraSentinel might not exist or be needed here, keeping it generic
    mocker.patch("src.application.services.notification_manager.NotificationManager.instance")
    mocker.patch("src.application.services.config_manager.load_config", return_value={})
    return mocker


class TestScaricoPDLPanel:
    @patch("src.gui.panels.scarico_pdl.BotWorker")
    def test_telegram_send_after_finish(self, mock_worker_cls, qapp, qtbot, mock_gui_deps):
        panel = ScaricoPDLPanel()
        mock_win = MagicMock()
        mock_tg = MagicMock()
        mock_win.telegram = mock_tg

        # Mock window() method of QWidget
        panel.window = MagicMock(return_value=mock_win)

        qtbot.addWidget(panel)

        # Ensure table uses technical names
        panel.data_table.table.setRowCount(0)
        panel.data_table.set_data([{"numero_pdl": "999"}])
        panel.merge_and_send_from_telegram = True

        with (
            patch.object(panel, "get_safework_credentials", return_value=("u", "p", "E")),
            patch("src.gui.panels.scarico_pdl.Path.exists", return_value=True),
        ):
            # Simula avvio
            panel._on_start()

            # Configure the mock worker instance
            mock_worker = mock_worker_cls.return_value
            panel.worker = mock_worker
            mock_worker.bot = MagicMock()
            mock_worker.bot.downloaded_files = ["/path/to/report.pdf"]

            # Chiama il completamento
            panel._on_worker_finished(True)

            # Verifica invio Telegram
            mock_tg.send_document_sync.assert_called_once()
            args = mock_tg.send_document_sync.call_args[0]
            assert args[0] == "/path/to/report.pdf"

    def test_validate_ready(self, qtbot, mock_gui_deps):
        panel = ScaricoPDLPanel()
        qtbot.addWidget(panel)

        # Clear default rows
        panel.data_table.table.setRowCount(0)

        # Test empty
        ready, msg = panel.validate_ready()
        assert ready is False
        assert "numero PDL" in msg

        # Test with data (usando nome tecnico)
        panel.data_table.set_data([{"numero_pdl": "123"}])
        ready, msg = panel.validate_ready()
        assert ready is True

    @patch("src.gui.panels.scarico_pdl.BotWorker")
    def test_on_start_workflow(self, mock_worker_cls, qtbot, mock_gui_deps):
        panel = ScaricoPDLPanel()
        qtbot.addWidget(panel)
        panel.data_table.set_data([{"numero_pdl": "123"}])

        with patch.object(panel, "get_safework_credentials", return_value=("u", "p", "E")):
            panel._on_start()
            assert panel.worker is not None
            mock_worker_cls.assert_called_once()
