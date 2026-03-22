import os
import sqlite3
import time
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.audit_manager import AuditManager
from src.core.backup_manager import BackupManager


class TestSprintAAuditBackup:
    @pytest.fixture
    def audit_mgr(self, tmp_path, mocker):
        db_path = tmp_path / "audit_test.db"
        # Patch the real location in AuditDatabase
        mocker.patch("src.core.audit.database.AuditDatabase.DB_PATH", db_path)
        # Patch signals
        mocker.patch("src.core.audit.manager.AuditSignals.instance")

        # Forza reset singleton reale
        AuditManager._instance = None
        return AuditManager()

    def test_audit_integrity_chain(self, audit_mgr):
        """Verifica che la catena di hash rilevi manomissioni."""
        # Eseguiamo un log controllato
        audit_mgr.log_action("TestIntegrity", category="test")
        # Attendi il worker thread asincrono
        audit_mgr._log_queue.join()

        assert audit_mgr.verify_integrity() is True

        # Manomissione
        with sqlite3.connect(audit_mgr.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET action = 'MALICIOUS'")
            conn.commit()

        assert audit_mgr.verify_integrity() is False

    def test_audit_retention_policy(self, audit_mgr, mocker):
        """Verifica la pulizia dei log obsoleti."""
        # 1. Inserimento manuale log VECCHIO
        with sqlite3.connect(audit_mgr.DB_PATH) as conn:
            past_date = "2020-01-01T10:00:00.000000"
            conn.execute(
                "INSERT INTO audit_logs (timestamp, action, severity, status, category, user_id, params, row_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (past_date, "Old", "low", "success", "gen", "u", "{}", "fakehash"),
            )
            conn.commit()

        # 2. Inserimento log NUOVO tramite manager (Asincrono)
        audit_mgr.log_action("NewAction", category="test")
        audit_mgr._log_queue.join()

        # 3. Esegui pulizia
        audit_mgr.run_retention_policy(days=30)
        audit_mgr._log_queue.join() # Anche la pulizia logga un'azione asincrona

        # 4. Verifica
        logs = audit_mgr.get_logs()
        actions = [log["action"] for log in logs]

        assert "NewAction" in actions
        assert "Old" not in actions

    def test_backup_creation_and_filtering(self, tmp_path, mocker):
        """Verifica creazione backup e filtraggio estensioni."""
        # Mock Config Manager e Audit Manager
        mocker.patch("src.core.backup_manager.CONFIG_DIR", tmp_path)
        mocker.patch("src.core.backup_manager.load_config", return_value={})

        # Crea dati validi per il backup (.db e .json sono inclusi)
        (tmp_path / "data").mkdir()
        (tmp_path / "data" / "db1.db").write_text("dummy db")
        (tmp_path / "settings.json").write_text("{}")

        # Crea cartella da escludere
        (tmp_path / "logs").mkdir()
        (tmp_path / "logs" / "app.log").write_text("log data")

        backup_dir = tmp_path / "MyBackups"
        backup_dir.mkdir()

        with patch(
            "src.core.backup_manager.BackupManager.get_backup_dir",
            return_value=backup_dir,
        ):
            success, zip_path = BackupManager.create_backup()

            assert success is True
            assert Path(zip_path).exists()

            with zipfile.ZipFile(zip_path, "r") as z:
                files = z.namelist()
                assert any("db1.db" in f for f in files)
                assert any("settings.json" in f for f in files)
                assert not any("app.log" in f for f in files)

    def test_backup_cleanup_limit(self, tmp_path):
        """Verifica mantenimento ultimi 5 backup con timestamp differenziati."""
        backup_dir = tmp_path / "CleanupTest"
        backup_dir.mkdir()

        now = time.time()
        files = []
        for i in range(8):
            f = backup_dir / f"SyncroJob_Backup_202601{i:02d}.zip"
            f.write_text("fake")
            # Forziamo mtime crescente
            os.utime(f, (now + i, now + i))
            files.append(f)

        BackupManager._cleanup_old_backups(backup_dir, keep=5)

        remaining = sorted(backup_dir.glob("*.zip"), key=os.path.getmtime)
        assert len(remaining) == 5
        # Gli ultimi 5 devono essere quelli con i numeri più alti (6, 7, 8...)
        assert "20260107" in remaining[-1].name

    def test_restore_error_handling(self, tmp_path):
        """Verifica che il ripristino fallisca correttamente con file invalidi."""
        # Caso 1: File inesistente
        s1, _m1 = BackupManager.restore_backup("missing.zip")
        assert s1 is False

        # Caso 2: File non ZIP
        not_zip = tmp_path / "fake.zip"
        not_zip.write_text("hello")
        s2, m2 = BackupManager.restore_backup(str(not_zip))
        assert s2 is False
        assert "valido" in m2.lower()
