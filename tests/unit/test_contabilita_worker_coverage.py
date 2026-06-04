from unittest.mock import MagicMock, patch

import pytest

from src.application.services.contabilita_worker import ContabilitaWorker


class TestContabilitaWorker:
    @pytest.fixture
    def mock_manager(self, mocker):
        return mocker.patch("src.application.services.contabilita_worker.ContabilitaManager")

    @pytest.fixture
    def worker(self, mocker):
        mocker.patch("PySide6.QtCore.QThread.__init__", return_value=None)
        # Mock signals explicitly since QThread init is mocked
        w = ContabilitaWorker("test.xlsx")
        w.finished_signal = MagicMock()
        w.progress_signal = MagicMock()
        return w

    def test_init_defaults(self):
        worker = ContabilitaWorker("test.xlsx")
        assert worker.file_path == "test.xlsx"
        assert worker.giornaliere_path == ""
        assert worker.attivita_path == ""
        assert worker.certificati_path == ""

    def test_run_success_all_phases(self, worker, mock_manager, tmp_path):
        """Test full run with all phases successful."""
        # Setup paths
        worker.giornaliere_path = str(tmp_path / "giornaliere")
        worker.attivita_path = str(tmp_path / "attivita.xlsx")
        worker.certificati_path = str(tmp_path / "certificati.xlsx")

        # Mock Path exists
        with patch("src.application.services.contabilita_worker.Path.exists", return_value=True):
            # Mock Manager methods
            mock_manager.scan_workload.return_value = (
                5,
                10,
            )  # 5 sheets, 10 daily files

            # Setup returns: success, msg, added, removed
            mock_manager.import_data_from_excel.return_value = (True, "OK", 10, 0)
            mock_manager.import_giornaliere.return_value = (True, "OK", 5, 0)
            mock_manager.import_attivita_programmate.return_value = (True, "OK", 1, 0)
            mock_manager.import_certificati_campione.return_value = (True, "OK", 1, 0)

            worker.run()

        # Verify signals
        worker.progress_signal.emit.assert_called()
        worker.finished_signal.emit.assert_called()

        # Verify arguments of finished signal
        args = worker.finished_signal.emit.call_args[0]
        assert args[0] is True  # Success
        assert "Contabilità: OK" in args[1]
        assert "Giornaliere: OK" in args[1]
        assert "Att. Prog: OK" in args[1]
        assert "Certificati: OK" in args[1]
        assert args[2] == 17  # Added (10 + 5 + 1 + 1)

    def test_run_critical_error(self, worker, mock_manager):
        """Test handling of exception during run."""
        mock_manager.init_db.side_effect = Exception("DB Error")

        worker.run()

        worker.finished_signal.emit.assert_called_with(False, "Errore critico: DB Error", 0, 0, 0.0)

    def test_progress_calculation(self, worker, mock_manager):
        """Test internal total ops calculation."""
        worker.attivita_path = "exists"
        with (
            patch("src.application.services.contabilita_worker.Path.exists", return_value=True),
        ):
            mock_manager.scan_workload.return_value = (5, 5)
            # 5 sheets + 5 files + 1 attivita + 0 certificati = 11
            res = worker._calculate_total_ops()
            assert res["total"] == 11
