import sqlite3

import pytest

from src.core.database.manager import DatabaseManager


@pytest.fixture
def temp_db(tmp_path):
    return tmp_path / "test.db"


def test_database_manager_singleton():
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    assert db1 is db2


def test_get_connection(temp_db):
    db = DatabaseManager()
    with db.get_connection(temp_db) as conn:
        assert isinstance(conn, sqlite3.Connection)
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        conn.commit()

    with db.get_connection(temp_db, read_only=True) as conn:
        assert isinstance(conn, sqlite3.Connection)
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test'").fetchone()
        assert res is not None


def test_execute_query(temp_db):
    db = DatabaseManager()
    with db.get_connection(temp_db) as conn:
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, val TEXT)")
        conn.execute("INSERT INTO test (val) VALUES (?)", ("test_val",))

    results = db.execute_query(temp_db, "SELECT * FROM test")
    assert len(results) == 1
    assert results[0]["val"] == "test_val"


def test_migrations_logic(tmp_path):
    db = DatabaseManager()
    db_path = tmp_path / "migration.db"

    # Mock migration
    def mig_v1(conn):
        conn.execute("CREATE TABLE users (id INTEGER)")

    migrations = {1: mig_v1}

    db._run_migrations(db_path, migrations, "TestDB")

    with db.get_connection(db_path) as conn:
        ver = db._get_db_version(conn)
        assert ver == 1
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'").fetchone()
        assert res is not None
