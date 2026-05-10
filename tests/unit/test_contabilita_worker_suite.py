from unittest.mock import MagicMock, patch

from src.core.contabilita_worker import ContabilitaWorker


class TestContabilitaWorkerLogic:
    @patch("src.core.contabilita_worker.ContabilitaManager")
    @patch("src.core.contabilita_worker.Path.exists", return_value=True)
    def test_worker_run_sequence(self, mock_exists, mock_manager, qtbot):
        worker = ContabilitaWorker("f.xlsx", "g_path", "a.xlsx", "c.xlsx")

        # Mock manager methods
        mock_manager.scan_workload.return_value = (2, 5)  # 2 sheets, 5 files
        mock_manager.import_data_from_excel.return_value = (True, "OK", 10, 0)
        mock_manager.import_giornaliere.return_value = (True, "OK", 20, 0)
        mock_manager.import_attivita_programmate.return_value = (True, "OK", 5, 0)
        mock_manager.import_certificati_campione.return_value = (True, "OK", 2, 0)

        finished_mock = MagicMock()
        worker.finished_signal.connect(finished_mock)

        worker.run()

        assert finished_mock.called
        # Risultati attesi: (successo, messaggio, aggiunti, rimossi, durata)
        args = finished_mock.call_args[0]
        assert args[0] is True
        assert "Contabilità: OK" in args[1]
        assert "Giornaliere: OK" in args[1]
        assert args[2] == 37  # 10+20+5+2

    @patch("src.core.contabilita_worker.ContabilitaManager")
    @patch("src.core.contabilita_worker.Path.exists", return_value=True)
    def test_worker_error_handling(self, mock_exists, mock_manager):
        worker = ContabilitaWorker("f.xlsx")
        mock_manager.scan_workload.side_effect = Exception("Crash")

        finished_mock = MagicMock()
        worker.finished_signal.connect(finished_mock)

        worker.run()

        assert finished_mock.called
        assert finished_mock.call_args[0][0] is False
        assert "Errore critico" in finished_mock.call_args[0][1]
