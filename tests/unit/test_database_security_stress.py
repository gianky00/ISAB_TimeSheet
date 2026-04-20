import sqlite3
import threading
import time
from unittest.mock import patch

import pytest

from src.core.database import DatabaseManager
from src.utils.security import PasswordManager


class TestDatabaseSecurityStress:
    @pytest.fixture
    def db_mgr(self, tmp_path, mocker):
        # Patch DB_DIR per usare tmp_path
        mocker.patch("src.core.database.manager.DB_DIR", tmp_path)
        return DatabaseManager()

    def test_database_wal_mode_concurrency(self, db_mgr, tmp_path):
        """Verifica la resilienza della scrittura concorrente in WAL mode."""
        db_path = tmp_path / "stress_test.db"

        with db_mgr.get_connection(db_path) as conn:
            conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, val TEXT)")
            conn.execute("INSERT INTO test (val) VALUES ('initial')")

        errors = []

        def writer_task():
            try:
                for i in range(20):
                    db_mgr.execute_query(db_path, "INSERT INTO test (val) VALUES (?)", (f"val_{i}",))
            except Exception as e:
                errors.append(f"Writer error: {e}")

        def reader_task():
            try:
                for _ in range(50):
                    db_mgr.execute_query(db_path, "SELECT COUNT(*) FROM test")
            except Exception as e:
                errors.append(f"Reader error: {e}")

        t1 = threading.Thread(target=writer_task)
        t2 = threading.Thread(target=reader_task)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert len(errors) == 0, f"Rilevati errori di concorrenza: {errors}"
        res = db_mgr.execute_query(db_path, "SELECT COUNT(*) FROM test")
        assert res[0][0] == 21

    def test_database_retry_on_locked(self, db_mgr, tmp_path):
        """Verifica che il manager gestisca il database occupato senza crashare."""
        db_path = tmp_path / "locked_real.db"
        db_mgr.execute_query(db_path, "CREATE TABLE t (id int)")

        conn_lock = sqlite3.connect(db_path)
        conn_lock.execute("BEGIN EXCLUSIVE")

        errors = []

        def attempt_write():
            try:
                db_mgr.execute_query(db_path, "INSERT INTO t VALUES (1)", retry_count=5)
            except Exception as e:
                errors.append(str(e))

        t = threading.Thread(target=attempt_write)
        t.start()

        time.sleep(1.0)
        conn_lock.rollback()
        conn_lock.close()
        t.join()

        assert len(errors) == 0, f"Query fallita nonostante lo sblocco: {errors}"

    def test_password_manager_encryption_flow(self, tmp_path, mocker):
        """Verifica il ciclo completo di sicurezza delle password."""
        # Patch SECURITY_DIR nel modulo security
        mocker.patch("src.utils.security.SECURITY_DIR", tmp_path / "security")

        # Re-inizializzazione per il test
        with patch("src.utils.security.PasswordManager._instance", None):
            pm = PasswordManager()
            plaintext = "SuperSecret123!"
            encrypted = pm.encrypt(plaintext)
            assert encrypted.startswith("ENC:v2:")
            decrypted = pm.decrypt(encrypted)
            assert decrypted == plaintext

    def test_security_key_stability(self, tmp_path, mocker):
        """Verifica che la chiave sia persistente e non cambi tra i riavvii."""
        sec_dir = tmp_path / "security"
        sec_dir.mkdir(parents=True, exist_ok=True)

        # Patching SECURITY_DIR
        mocker.patch("src.utils.security.SECURITY_DIR", sec_dir)

        # 1. Primo avvio
        with patch("src.utils.security.PasswordManager._instance", None):
            pm1 = PasswordManager()
            key1 = pm1._key

        assert (sec_dir / "secret.key").exists()

        # 2. Secondo avvio (caricamento da file)
        with patch("src.utils.security.PasswordManager._instance", None):
            pm2 = PasswordManager()
            key2 = pm2._key

        assert key1 == key2, "La chiave crittografica è cambiata tra i riavvii!"
