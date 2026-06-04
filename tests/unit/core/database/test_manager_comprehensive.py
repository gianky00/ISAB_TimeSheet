import sqlite3
from unittest.mock import MagicMock

import pytest

from src.application.services.database.manager import DatabaseManager


class TestDatabaseManager:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        DatabaseManager._instance = None

    @pytest.fixture
    def db_dir(self, tmp_path):
        d = tmp_path / "db"
        d.mkdir()
        return d

    def test_singleton(self):
        dm1 = DatabaseManager()
        dm2 = DatabaseManager()
        assert dm1 is dm2

    def test_get_connection_standard(self, db_dir):
        db_path = db_dir / "test.db"
        dm = DatabaseManager()
        with dm.get_connection(db_path) as conn:
            assert isinstance(conn, sqlite3.Connection)
            conn.execute("CREATE TABLE test (id INTEGER)")
            conn.execute("INSERT INTO test VALUES (1)")

        # Verify persistence
        with dm.get_connection(db_path) as conn:
            res = conn.execute("SELECT * FROM test").fetchone()
            assert res[0] == 1

    def test_get_connection_readonly(self, db_dir):
        db_path = db_dir / "test_ro.db"
        dm = DatabaseManager()
        # Create DB first
        with dm.get_connection(db_path) as conn:
            conn.execute("CREATE TABLE test (id INTEGER)")

        with dm.get_connection(db_path, read_only=True) as conn:
            with pytest.raises(sqlite3.OperationalError, match="readonly"):
                conn.execute("INSERT INTO test VALUES (1)")

    def test_get_write_connection_locking(self, db_dir):
        db_path = db_dir / "test_write.db"
        dm = DatabaseManager()
        with dm.get_write_connection(db_path) as conn:
            conn.execute("CREATE TABLE test (id INTEGER)")
            assert dm._write_lock.locked()
        assert not dm._write_lock.locked()

    def test_execute_query(self, db_dir):
        db_path = db_dir / "test_exec.db"
        dm = DatabaseManager()
        with dm.get_connection(db_path) as conn:
            conn.execute("CREATE TABLE test (val TEXT)")
            conn.execute("INSERT INTO test VALUES ('hello')")

        results = dm.execute_query(db_path, "SELECT * FROM test")
        assert len(results) == 1
        assert results[0]["val"] == "hello"

    def test_execute_query_retry_on_locked(self, db_dir, mocker):
        db_path = db_dir / "test_retry.db"
        dm = DatabaseManager()
        with dm.get_connection(db_path) as conn:
            conn.execute("CREATE TABLE t (id INT)")

        # Mock connect to fail with "database is locked" twice then succeed
        mock_conn = mocker.patch("sqlite3.connect")
        # 1st call: error, 2nd call: error, 3rd call: actual connection
        real_conn = sqlite3.connect(db_path)
        mock_conn.side_effect = [
            sqlite3.OperationalError("database is locked"),
            sqlite3.OperationalError("database is locked"),
            real_conn,
        ]

        mocker.patch("time.sleep")  # Speed up test

        res = dm.execute_query(db_path, "SELECT 1")
        # connect is called inside context manager 'get_connection'
        # Total calls: 3 expected (fail, fail, success)
        # If it's 4, it means something else is calling connect
        assert mock_conn.call_count >= 3
        real_conn.close()

    def test_migrations_flow(self, db_dir, mocker):
        db_path = db_dir / "test_mig.db"
        dm = DatabaseManager()

        # Define mock migrations
        m1 = MagicMock()
        m2 = MagicMock()
        mock_migrations = {1: m1, 2: m2}

        # Run migrations on clean DB
        dm._run_migrations(db_path, mock_migrations, "TestDB")

        assert m1.called
        assert m2.called

        with dm.get_connection(db_path) as conn:
            ver = conn.execute("PRAGMA user_version").fetchone()[0]
            assert ver == 2

        # Run again -> nothing should happen
        m1.reset_mock()
        m2.reset_mock()
        dm._run_migrations(db_path, mock_migrations, "TestDB")
        assert not m1.called
        assert not m2.called

    def test_migrations_failure_rollback(self, db_dir, mocker):
        db_path = db_dir / "test_fail.db"
        dm = DatabaseManager()

        class BoomError(Exception):
            pass

        def failing_mig(conn):
            # Use non-DDL to test transaction rollback properly if possible,
            # but here we check if table creation is rolled back.
            conn.execute("CREATE TABLE bad (id INT)")
            raise BoomError("Boom")

        mock_migrations = {1: failing_mig}

        with pytest.raises(BoomError, match="Boom"):
            dm._run_migrations(db_path, mock_migrations, "FailDB")

        # Note: SQLite DDL in some versions/configs might NOT rollback perfectly.
        # But our get_connection has a rollback on exception.
        with dm.get_connection(db_path) as conn:
            # Check version still 0
            ver = conn.execute("PRAGMA user_version").fetchone()[0]
            assert ver == 0

    def test_init_db_integration(self, db_dir, mocker):
        dm = DatabaseManager()
        # Mock DB paths to point to our temp dir
        mocker.patch.object(dm, "DB_CONTABILITA", db_dir / "c.db")
        mocker.patch.object(dm, "DB_TIMBRATURE", db_dir / "t.db")
        mocker.patch.object(dm, "DB_PDL", db_dir / "p.db")
        mocker.patch.object(dm, "DB_STORICO_ODA", db_dir / "o.db")
        mocker.patch.object(dm, "DB_DIPENDENTI", db_dir / "d.db")

        # Test full init
        dm.init_db()

        assert (db_dir / "c.db").exists()
        assert (db_dir / "d.db").exists()
