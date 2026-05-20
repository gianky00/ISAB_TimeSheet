import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.audit_manager import AuditManager
from src.core.database.backup_manager import DatabaseBackupManager


@pytest.fixture
def mock_db_dir(tmp_path):
    with patch("src.core.database.backup_manager.DB_DIR", tmp_path):
        DatabaseBackupManager.BACKUP_DIR = tmp_path / "backups"
        yield tmp_path


def test_execute_backup_success(mock_db_dir):
    # Create dummy db file
    (mock_db_dir / "test.db").write_text("dummy")

    with patch("src.core.database.backup_manager.DatabaseBackupManager._safe_copy", return_value=True):
        with patch.object(AuditManager, "instance") as mock_audit:
            assert DatabaseBackupManager.execute_backup() is True
            mock_audit.return_value.log_action.assert_called_once()

    assert len(list(DatabaseBackupManager.BACKUP_DIR.iterdir())) == 1


def test_execute_backup_no_files(mock_db_dir):
    assert DatabaseBackupManager.execute_backup() is False


def test_execute_backup_copy_fails(mock_db_dir):
    (mock_db_dir / "test.db").write_text("dummy")

    with patch("src.core.database.backup_manager.DatabaseBackupManager._safe_copy", return_value=False):
        assert DatabaseBackupManager.execute_backup() is False


def test_safe_copy_success(mock_db_dir):
    src = mock_db_dir / "test.db"
    dst = mock_db_dir / "backup.db"
    src.write_text("dummy")

    with patch("sqlite3.connect") as mock_conn:
        mock_conn.return_value.__enter__.return_value.execute = MagicMock()
        assert DatabaseBackupManager._safe_copy(src, dst) is True


def test_safe_copy_fallback_success(mock_db_dir):
    src = mock_db_dir / "test.db"
    dst = mock_db_dir / "backup.db"
    src.write_text("dummy")

    with patch("sqlite3.connect", side_effect=sqlite3.OperationalError):
        with patch("shutil.copy2") as mock_copy:
            assert DatabaseBackupManager._safe_copy(src, dst) is True
            mock_copy.assert_called_once()


def test_safe_copy_fallback_fail(mock_db_dir):
    src = mock_db_dir / "test.db"
    dst = mock_db_dir / "backup.db"
    src.write_text("dummy")

    with patch("sqlite3.connect", side_effect=sqlite3.OperationalError):
        with patch("shutil.copy2", side_effect=Exception):
            assert DatabaseBackupManager._safe_copy(src, dst) is False


def test_safe_copy_general_error(mock_db_dir):
    src = mock_db_dir / "test.db"
    dst = mock_db_dir / "backup.db"

    with patch("sqlite3.connect", side_effect=Exception):
        assert DatabaseBackupManager._safe_copy(src, dst) is False


def test_rotate_backups(mock_db_dir):
    DatabaseBackupManager.BACKUP_DIR.mkdir(parents=True)
    DatabaseBackupManager.MAX_BACKUPS = 2

    # Create 3 backup dirs
    for i in range(3):
        d = DatabaseBackupManager.BACKUP_DIR / f"dir_{i}"
        d.mkdir()

    DatabaseBackupManager._rotate_backups()
    assert len(list(DatabaseBackupManager.BACKUP_DIR.iterdir())) == 2


def test_rotate_backups_error(mock_db_dir):
    with patch.object(Path, "iterdir", side_effect=Exception):
        # Should not raise
        DatabaseBackupManager._rotate_backups()


def test_list_backups(mock_db_dir):
    DatabaseBackupManager.BACKUP_DIR.mkdir(parents=True)
    (DatabaseBackupManager.BACKUP_DIR / "b1").mkdir()
    (DatabaseBackupManager.BACKUP_DIR / "b2").mkdir()

    backups = DatabaseBackupManager.list_backups()
    assert len(backups) == 2


def test_list_backups_not_exists(mock_db_dir):
    assert DatabaseBackupManager.list_backups() == []
