import os
import sqlite3
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from src.application.services.database.maintenance_worker import DatabaseMaintenanceWorker


class TestMaintenanceWorker:
    @pytest.fixture(autouse=True)
    def setup_env(self, tmp_path):
        """Setup temporary database and log directories."""
        self.db_dir = tmp_path / "data"
        self.db_dir.mkdir()
        self.log_dir = tmp_path / "logs"
        self.log_dir.mkdir()

        # Patching path constants
        with patch("src.application.services.database.maintenance_worker.LOGS_DIR", self.log_dir):
            yield

    def test_optimize_db(self, tmp_path):
        db_path = self.db_dir / "test.db"
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE t (id INTEGER)")
            conn.commit()

        worker = DatabaseMaintenanceWorker()
        # Mock connection manager
        with patch("src.application.services.database.db_manager.get_write_connection") as mock_conn:
            mock_c = mock_conn.return_value.__enter__.return_value
            worker._optimize_db(db_path)

            assert mock_c.execute.called
            calls = [call.args[0] for call in mock_c.execute.call_args_list]
            assert "ANALYZE" in calls
            assert "VACUUM" in calls

    def test_clean_logs(self):
        # Create 2 logs: one old, one new
        old_log = self.log_dir / "old.log"
        old_log.write_text("old")
        new_log = self.log_dir / "new.log"
        new_log.write_text("new")

        # Set old time (40 days ago)
        old_time = (datetime.now(UTC) - timedelta(days=40)).timestamp()
        os.utime(old_log, (old_time, old_time))

        worker = DatabaseMaintenanceWorker()
        worker._clean_logs(days=30)

        assert not old_log.exists()
        assert new_log.exists()

    @patch("src.application.services.database.maintenance_worker.DatabaseMaintenanceWorker._optimize_db")
    @patch("src.application.services.database.maintenance_worker.DatabaseMaintenanceWorker._clean_logs")
    def test_run_flow(self, mock_clean, mock_opt):
        db1 = self.db_dir / "db1.db"
        db1.touch()

        worker = DatabaseMaintenanceWorker()
        worker.databases = [db1]

        worker.run()

        assert mock_opt.called
        assert mock_clean.called
