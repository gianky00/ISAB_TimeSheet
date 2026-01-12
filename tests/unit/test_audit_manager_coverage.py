
import sqlite3
from datetime import datetime, timedelta

import pytest

from src.core.audit_manager import AuditManager


class TestAuditManagerCoverage:
    @pytest.fixture
    def audit_db(self, tmp_path, mocker):
        """Mock del DB di audit usando un file temporaneo."""
        db_path = tmp_path / "audit_test.db"
        # Patch del DB_PATH della classe
        mocker.patch.object(AuditManager, "DB_PATH", db_path)
        # Forza reset singleton
        AuditManager._instance = None
        manager = AuditManager()
        yield manager, db_path

    def test_log_action_hashing_chain(self, audit_db):
        """Verifica che le righe siano incatenate tramite hash."""
        manager, db_path = audit_db

        manager.log_action("Action 1")
        manager.log_action("Action 2")

        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM audit_logs ORDER BY id ASC").fetchall()

            assert len(rows) == 2
            h1 = rows[0]["row_hash"]
            h2 = rows[1]["row_hash"]

            assert h1 != h2
            assert h1 is not None
            assert len(h1) == 64

    def test_verify_integrity_success(self, audit_db):
        """Verifica che un log non manomesso passi la validazione."""
        manager, _ = audit_db
        manager.log_action("Test 1")
        manager.log_action("Test 2")

        assert manager.verify_integrity() is True

    def test_verify_integrity_tamper_detection(self, audit_db):
        """Verifica che la modifica manuale di una riga rompa l'integrità."""
        manager, db_path = audit_db
        manager.log_action("Secure Action")

        # Manomissione manuale nel DB
        with sqlite3.connect(db_path) as conn:
            conn.execute("UPDATE audit_logs SET action = 'Hacked Action' WHERE id = 1")
            conn.commit()

        assert manager.verify_integrity() is False

    def test_run_retention_policy(self, audit_db):
        """Verifica la cancellazione dei log vecchi."""
        manager, db_path = audit_db

        # Inserisci un log vecchio manualmente con formato ISO coerente
        old_date = (datetime.now() - timedelta(days=100)).isoformat()
        with sqlite3.connect(db_path) as conn:
            conn.execute("INSERT INTO audit_logs (timestamp, action, user_id) VALUES (?, ?, ?)",
                         (old_date, "Old Action", "test_user"))
            conn.commit()

        manager.run_retention_policy(days=30)

        with sqlite3.connect(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM audit_logs WHERE action = 'Old Action'").fetchone()[0]
            assert count == 0

    def test_get_current_user_fallback(self, audit_db, mocker):
        """Verifica il recupero dell'utente con vari fallback."""
        manager, _ = audit_db

        # Mock environment
        mocker.patch("os.environ.get", return_value="TestUser")
        assert manager._get_current_user() == "TestUser"

        # Mock all failed -> unknown
        mocker.patch("os.environ.get", return_value=None)
        mocker.patch("getpass.getuser", side_effect=Exception("Failed"))
        mocker.patch("os.name", "posix") # Forza posix per saltare ctypes

        assert manager._get_current_user() == "unknown"
