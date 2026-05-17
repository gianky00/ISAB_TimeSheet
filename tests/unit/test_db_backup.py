import os
import sqlite3
from unittest.mock import patch

import pytest

from src.core.database.backup_manager import DatabaseBackupManager


class TestBackupManager:
    @pytest.fixture(autouse=True)
    def setup_dirs(self, tmp_path):
        """Setup temporary database and backup directories."""
        self.db_dir = tmp_path / "data"
        self.db_dir.mkdir()
        self.backup_dir = self.db_dir / "backups"

        # Patching constants in the module
        with patch("src.core.database.backup_manager.DB_DIR", self.db_dir):
            DatabaseBackupManager.BACKUP_DIR = self.backup_dir
            yield

    def test_execute_backup_no_files(self):
        # Nessun file .db in db_dir
        assert DatabaseBackupManager.execute_backup() is False

    @patch("src.core.audit_manager.AuditManager.instance")
    def test_execute_backup_success(self, mock_audit, tmp_path):
        # Crea un DB fittizio
        db1 = self.db_dir / "test.db"
        with sqlite3.connect(db1) as conn:
            conn.execute("CREATE TABLE t (id INTEGER)")
            conn.commit()

        success = DatabaseBackupManager.execute_backup()
        assert success is True

        # Verifica creazione cartella sessione
        sessions = list(self.backup_dir.iterdir())
        assert len(sessions) == 1
        assert sessions[0].is_dir()

        # Verifica file backup
        backup_file = sessions[0] / "test.db"
        assert backup_file.exists()

        # Verifica log audit
        assert mock_audit.return_value.log_action.called

    def test_safe_copy_fallback(self, tmp_path):
        src = self.db_dir / "corrupt.db"
        src.write_text("not-a-db")
        dst = self.db_dir / "backup.db"

        # SQLite failerà su un file che non è un DB
        # Dovrebbe fare fallback su shutil.copy2
        res = DatabaseBackupManager._safe_copy(src, dst)
        assert res is True
        assert dst.exists()
        assert dst.read_text() == "not-a-db"

    def test_rotate_backups(self):
        # Crea 15 cartelle di backup
        for i in range(15):
            d = self.backup_dir / f"session_{i}"
            d.mkdir(parents=True)
            # Simula tempi diversi
            os.utime(d, (1000 + i, 1000 + i))

        DatabaseBackupManager._rotate_backups()

        backups = list(self.backup_dir.iterdir())
        assert len(backups) == 10
        # session_0...session_4 dovrebbero essere state eliminate (più vecchie)
        assert not (self.backup_dir / "session_0").exists()
        assert (self.backup_dir / "session_14").exists()

    def test_list_backups(self):
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        d1 = self.backup_dir / "b1"
        d1.mkdir()
        d2 = self.backup_dir / "b2"
        d2.mkdir()
        os.utime(d1, (10, 10))
        os.utime(d2, (20, 20))

        lst = DatabaseBackupManager.list_backups()
        assert len(lst) == 2
        assert lst[0] == d2  # Newest first
