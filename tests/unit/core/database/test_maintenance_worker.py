import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.maintenance_worker import DatabaseMaintenanceWorker


@pytest.fixture
def mock_db_manager():
    with patch("src.core.database.maintenance_worker.db_manager") as db:
        yield db


@pytest.fixture
def worker(mock_db_manager):
    return DatabaseMaintenanceWorker()


def test_run_success(worker):
    with patch.object(worker, "_optimize_db") as mock_opt:
        with patch.object(worker, "_clean_logs") as mock_clean:
            # Setup db paths to exist
            for db in worker.databases:
                db.exists = MagicMock(return_value=True)

            worker.run()

            assert mock_opt.call_count == len(worker.databases)
            mock_clean.assert_called_once_with(days=30)


def test_run_optimize_error(worker):
    with patch.object(worker, "_optimize_db", side_effect=Exception("Opt Error")):
        with patch.object(worker, "_clean_logs"):
            for db in worker.databases:
                db.exists = MagicMock(return_value=True)

            # Should not raise exception
            worker.run()


def test_run_db_not_exists(worker):
    with patch.object(worker, "_optimize_db") as mock_opt:
        with patch.object(worker, "_clean_logs"):
            for db in worker.databases:
                db.exists = MagicMock(return_value=False)

            worker.run()
            assert mock_opt.call_count == 0


def test_optimize_db(worker, mock_db_manager):
    mock_conn = MagicMock()
    mock_db_manager.get_write_connection.return_value.__enter__.return_value = mock_conn

    db_path = MagicMock(spec=Path)
    db_path.name = "test.db"

    worker._optimize_db(db_path)

    assert mock_conn.execute.call_count == 2
    mock_conn.execute.assert_any_call("ANALYZE")
    mock_conn.execute.assert_any_call("VACUUM")


def test_clean_logs(worker, tmp_path):
    with patch("src.core.database.maintenance_worker.LOGS_DIR", tmp_path):
        # Create old and new logs
        old_log = tmp_path / "old.log"
        old_log.write_text("old")

        new_log = tmp_path / "new.log"
        new_log.write_text("new")

        # We need to set actual mtime
        cutoff = datetime.now(UTC) - timedelta(days=30)

        old_time = (cutoff - timedelta(days=5)).timestamp()
        new_time = (cutoff + timedelta(days=5)).timestamp()

        os.utime(old_log, (old_time, old_time))
        os.utime(new_log, (new_time, new_time))

        worker._clean_logs(days=30)

        # check old_log was unlinked
        assert not old_log.exists()
        assert new_log.exists()


def test_clean_logs_dir_not_exists(worker):
    with patch("src.core.database.maintenance_worker.LOGS_DIR") as mock_logs_dir:
        mock_logs_dir.exists.return_value = False
        worker._clean_logs(days=30)
        mock_logs_dir.glob.assert_not_called()


def test_clean_logs_error_unlinking(worker, tmp_path):
    with patch("src.core.database.maintenance_worker.LOGS_DIR", tmp_path):
        old_log = tmp_path / "old.log"
        old_log.write_text("old")

        cutoff = datetime.now(UTC) - timedelta(days=30)
        old_time = (cutoff - timedelta(days=5)).timestamp()

        os.utime(old_log, (old_time, old_time))

        with patch.object(Path, "unlink", side_effect=Exception("Unlink Error")):
            # Should not raise
            worker._clean_logs(days=30)
