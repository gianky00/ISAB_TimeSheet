import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.maintenance_worker import DatabaseMaintenanceWorker


class TestDatabaseMaintenanceWorker:
    @pytest.fixture
    def worker(self):
        # Impediamo l'esecuzione reale del thread
        return DatabaseMaintenanceWorker()

    def test_init(self, worker):
        assert worker.name == "DatabaseMaintenanceWorker"
        assert worker.daemon is True
        assert len(worker.databases) > 0

    @patch("src.core.database.maintenance_worker.db_manager.get_write_connection")
    def test_optimize_db_success(self, mock_conn, worker):
        mock_cursor = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_cursor

        worker._optimize_db(Path("test.db"))

        # Analisi e Vacuum devono essere chiamati
        mock_cursor.execute.assert_any_call("ANALYZE")
        mock_cursor.execute.assert_any_call("VACUUM")

    @patch("src.core.database.maintenance_worker.DatabaseMaintenanceWorker._optimize_db")
    @patch("src.core.database.maintenance_worker.DatabaseMaintenanceWorker._clean_logs")
    def test_run_success(self, mock_clean, mock_opt, worker, fs):
        # Simula presenza db
        test_db = Path("test1.db")
        fs.create_file(str(test_db))
        worker.databases = [test_db]

        worker.run()

        assert mock_opt.called
        mock_opt.assert_called_with(test_db)
        assert mock_clean.called

    @patch("src.core.database.maintenance_worker.DatabaseMaintenanceWorker._optimize_db")
    @patch("src.core.database.maintenance_worker.DatabaseMaintenanceWorker._clean_logs")
    def test_run_db_not_exists(self, mock_clean, mock_opt, worker):
        # Non crea il db
        test_db = Path("missing.db")
        worker.databases = [test_db]

        worker.run()

        assert not mock_opt.called
        assert mock_clean.called

    @patch("src.core.database.maintenance_worker.DatabaseMaintenanceWorker._optimize_db")
    @patch("src.core.database.maintenance_worker.DatabaseMaintenanceWorker._clean_logs")
    def test_run_db_exception(self, mock_clean, mock_opt, worker, fs):
        test_db = Path("error.db")
        fs.create_file(str(test_db))
        worker.databases = [test_db]

        mock_opt.side_effect = Exception("DB Fail")

        # Non deve crashare
        worker.run()

        assert mock_opt.called
        assert mock_clean.called

    def test_clean_logs(self, worker, fs):
        with patch("src.core.database.maintenance_worker.LOGS_DIR", Path("/logs")):
            fs.create_dir("/logs")

            # File vecchi di 40 e 20 giorni
            old_file = Path("/logs/old.log")
            recent_file = Path("/logs/new.log")

            fs.create_file(str(old_file))
            fs.create_file(str(recent_file))

            old_time = (datetime.now(UTC) - timedelta(days=40)).timestamp()
            recent_time = (datetime.now(UTC) - timedelta(days=20)).timestamp()

            os.utime(str(old_file), (old_time, old_time))
            os.utime(str(recent_file), (recent_time, recent_time))

            worker._clean_logs(30)

            assert not old_file.exists()
            assert recent_file.exists()

    def test_clean_logs_no_dir(self, worker, fs):
        with patch("src.core.database.maintenance_worker.LOGS_DIR", Path("/missing_logs")):
            # Se la dir non c'è, torna subito senza crash
            worker._clean_logs(30)
