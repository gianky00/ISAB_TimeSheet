import os
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.backup_manager import DatabaseBackupManager


class TestDatabaseBackupManager:
    @pytest.fixture(autouse=True)
    def setup_dirs(self, fs):
        self.db_dir = Path("/dbs")
        self.backup_dir = self.db_dir / "backups"
        fs.create_dir(str(self.db_dir))

        with patch("src.core.database.backup_manager.DB_DIR", self.db_dir):
            with patch("src.core.database.backup_manager.DatabaseBackupManager.BACKUP_DIR", self.backup_dir):
                yield

    @patch("src.core.database.backup_manager.AuditManager.instance")
    def test_execute_backup_success(self, mock_audit, fs):
        fs.create_file(str(self.db_dir / "db1.db"))
        fs.create_file(str(self.db_dir / "db2.db"))

        with patch("src.core.database.backup_manager.DatabaseBackupManager._safe_copy", return_value=True):
            success = DatabaseBackupManager.execute_backup()

        assert success is True
        assert mock_audit.return_value.log_action.called

        backups = list(self.backup_dir.iterdir())
        assert len(backups) == 1
        assert backups[0].is_dir()

    def test_execute_backup_no_files(self, fs):
        success = DatabaseBackupManager.execute_backup()
        assert success is False
        # The logic might create a session_dir before realizing there are no files.
        # But it shouldn't have created any files inside the backup dir.
        # We just assert that either it's empty, or the session_dir inside is empty.
        if self.backup_dir.exists():
            for d in self.backup_dir.iterdir():
                assert len(list(d.iterdir())) == 0

    @patch("src.core.database.backup_manager.sqlite3.connect")
    def test_safe_copy_sqlite_success(self, mock_conn):
        src = Path("/src.db")
        dst = Path("/dst.db")

        mock_cursor = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_cursor

        success = DatabaseBackupManager._safe_copy(src, dst)

        assert success is True
        mock_cursor.execute.assert_called_once()
        assert "VACUUM INTO" in mock_cursor.execute.call_args[0][0]

    @patch("src.core.database.backup_manager.sqlite3.connect")
    @patch("src.core.database.backup_manager.shutil.copy2")
    def test_safe_copy_fallback_shutil(self, mock_copy, mock_conn):
        src = Path("/src.db")
        dst = Path("/dst.db")

        mock_conn.side_effect = sqlite3.OperationalError("Locked")
        success = DatabaseBackupManager._safe_copy(src, dst)

        assert success is True
        assert mock_copy.called
        mock_copy.assert_called_with(src, dst)

    @patch("src.core.database.backup_manager.sqlite3.connect")
    @patch("src.core.database.backup_manager.shutil.copy2")
    def test_safe_copy_total_failure(self, mock_copy, mock_conn):
        src = Path("/src.db")
        dst = Path("/dst.db")

        mock_conn.side_effect = sqlite3.OperationalError("Locked")
        mock_copy.side_effect = Exception("Copy failed")

        success = DatabaseBackupManager._safe_copy(src, dst)
        assert success is False

    def test_rotate_backups(self, fs):
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        DatabaseBackupManager.MAX_BACKUPS = 3

        for i in range(5):
            d = self.backup_dir / f"backup_{i}"
            d.mkdir()
            os.utime(str(d), (1000 + i, 1000 + i))

        DatabaseBackupManager._rotate_backups()

        remaining = [d.name for d in self.backup_dir.iterdir() if d.is_dir()]
        assert len(remaining) == 3
        assert "backup_0" not in remaining
        assert "backup_1" not in remaining

    def test_list_backups(self, fs):
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        d1 = self.backup_dir / "b1"
        d2 = self.backup_dir / "b2"
        d1.mkdir()
        d2.mkdir()

        os.utime(str(d1), (1000, 1000))
        os.utime(str(d2), (2000, 2000))

        backups = DatabaseBackupManager.list_backups()

        assert len(backups) == 2
        assert backups[0].name == "b2"

    def test_list_backups_empty(self):
        assert DatabaseBackupManager.list_backups() == []
