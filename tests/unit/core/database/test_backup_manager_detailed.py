import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.backup_manager import DatabaseBackupManager


class TestDatabaseBackupManagerDetailed:
    @pytest.fixture(autouse=True)
    def setup_dirs(self, fs):
        self.fake_db_dir = Path("/data")
        self.fake_backup_dir = self.fake_db_dir / "backups"
        fs.create_dir(str(self.fake_db_dir))
        fs.create_dir(str(self.fake_backup_dir))

        # Patch costanti e variabili globali
        with patch("src.core.database.backup_manager.DB_DIR", self.fake_db_dir):
            with patch.object(DatabaseBackupManager, "BACKUP_DIR", self.fake_backup_dir):
                yield

    @patch("src.core.database.backup_manager.sqlite3.connect")
    def test_safe_copy_sqlite(self, mock_connect):
        src = self.fake_db_dir / "test1.db"
        dst = self.fake_backup_dir / "test1.db"
        res = DatabaseBackupManager._safe_copy(src, dst)
        assert res is True
        mock_connect.return_value.__enter__.return_value.execute.assert_called()

    @patch("src.core.database.backup_manager.sqlite3.connect", side_effect=sqlite3.OperationalError("Fail"))
    @patch("src.core.database.backup_manager.shutil.copy2")
    def test_safe_copy_fallback(self, mock_copy, mock_connect):
        src = self.fake_db_dir / "test1.db"
        dst = self.fake_backup_dir / "test1.db"
        res = DatabaseBackupManager._safe_copy(src, dst)
        assert res is True
        assert mock_copy.called

    @patch("src.core.database.backup_manager.DatabaseBackupManager._safe_copy", return_value=True)
    @patch("src.core.database.backup_manager.AuditManager.instance")
    def test_execute_backup_success(self, mock_audit, mock_copy, fs):
        fs.create_file(str(self.fake_db_dir / "app.db"), contents=b"db")
        res = DatabaseBackupManager.execute_backup()
        assert res is True
        assert mock_audit.return_value.log_action.called

    def test_rotate_backups(self, fs):
        # Creiamo 15 cartelle di backup
        for i in range(15):
            d = self.fake_backup_dir / f"backup_{i:02d}"
            fs.create_dir(str(d))
            # Usiamo os.utime per simulare mtime diversi se necessario,
            # ma pyfakefs li ordina per creazione se non specificato.

        # Patch stat() per tornare mtime basati sul nome per determinismo
        original_stat = Path.stat

        def mock_stat(path_obj):
            m = MagicMock()
            # backup_00 -> mtime 0, backup_14 -> mtime 14
            try:
                name = Path(path_obj).name
                if "backup_" in name:
                    m.st_mtime = int(name.split("_")[1])
                else:
                    m.st_mtime = 100
            except Exception:
                m.st_mtime = 100
            return m

        with patch.object(Path, "stat", side_effect=mock_stat):
            DatabaseBackupManager._rotate_backups()

        backups = [d for d in self.fake_backup_dir.iterdir() if d.is_dir()]
        assert len(backups) == 10
