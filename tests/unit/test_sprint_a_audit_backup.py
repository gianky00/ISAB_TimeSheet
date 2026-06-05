import os
import sqlite3
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from src.application.services.audit_manager import AuditManager
from src.application.services.backup.archive_rotator import ArchiveRotator
from src.application.services.backup_manager import BackupManager


class TestSprintAAuditBackup:
    @pytest.fixture(autouse=True)
    def isolate_audit_db(self, tmp_path, mocker):
        """Isolamento totale del database audit per evitare collisioni di hash."""
        db_path = tmp_path / "audit_sprint_test.db"
        mocker.patch("src.application.services.database.db_manager.DB_AUDIT", db_path)
        mocker.patch("src.application.services.audit.database.db_manager.DB_AUDIT", db_path)
        mocker.patch("src.application.services.audit.manager.AuditSignals.instance")

        AuditManager._instance = None
        yield
        AuditManager._instance = None

    def test_audit_integrity_chain(self):
        """Verifica che la catena di hash rilevi manomissioni in un DB pulito."""
        audit_mgr = AuditManager()
        audit_mgr.log_action("Action1", category="test")
        audit_mgr._log_queue.join()

        assert audit_mgr.verify_integrity() is True

        # Manomissione dell'ultimo record - Accesso tramite audit_mgr.db
        with sqlite3.connect(audit_mgr.db.db_path) as conn:
            conn.execute("UPDATE audit_logs SET action = 'MALICIOUS' WHERE id = 1")
            conn.commit()

        assert audit_mgr.verify_integrity() is False

    def test_audit_retention_policy(self):
        audit_mgr = AuditManager()
        with sqlite3.connect(audit_mgr.db.db_path) as conn:
            past_date = "2020-01-01T10:00:00"
            conn.execute(
                "INSERT INTO audit_logs (timestamp, action, category, status, severity, row_hash) VALUES (?, ?, ?, ?, ?, ?)",
                (past_date, "Old", "test", "success", "low", "fake"),
            )
            conn.commit()

        audit_mgr.log_action("New", category="test")
        audit_mgr._log_queue.join()

        audit_mgr.run_retention_policy(days=30)
        audit_mgr._log_queue.join()

        logs = audit_mgr.get_logs()
        actions = [log["action"] for log in logs]
        assert "New" in actions
        assert "Old" not in actions

    def test_backup_creation_and_filtering(self, tmp_path, mocker):
        mocker.patch("src.application.services.backup_manager.CONFIG_DIR", tmp_path)
        mocker.patch("src.application.services.backup_manager.load_config", return_value={})
        (tmp_path / "data").mkdir()
        (tmp_path / "data" / "db.db").write_text("db")
        (tmp_path / "config.json").write_text("{}")

        backup_dir = tmp_path / "Backups"
        backup_dir.mkdir()

        with patch(
            "src.application.services.backup_manager.BackupManager.get_backup_dir", return_value=backup_dir
        ):
            success, zip_path = BackupManager.create_backup()
            assert success is True
            assert Path(zip_path).exists()

    def test_backup_cleanup_limit(self, tmp_path):
        backup_dir = tmp_path / "Cleanup"
        backup_dir.mkdir()
        now = time.time()
        for i in range(7):
            f = backup_dir / f"SyncroJob_Backup_{i}.zip"
            f.write_text("data")
            os.utime(f, (now + i, now + i))

        ArchiveRotator.rotate_backups(backup_dir, keep=3)
        assert len(list(backup_dir.glob("*.zip"))) == 3

    def test_restore_error_handling(self):
        s1, _ = BackupManager.restore_backup("non_esiste.zip")
        assert s1 is False
