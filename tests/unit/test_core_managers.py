"""Tests for src.core managers."""

import json
from datetime import UTC
from unittest.mock import patch

import pytest

from src.core import config_manager
from src.core.database import DatabaseManager


# --- CONFIG MANAGER ---
@pytest.fixture(autouse=True)
def mock_config(tmp_path):
    """Mocks the config file location and ensures clean state."""
    config_manager._config_cache = None  # Force reset BEFORE test
    fake_dir = tmp_path / "config"
    fake_dir.mkdir(parents=True, exist_ok=True)
    fake_file = fake_dir / "config.json"

    # Patch sia la DIR che la FILE sia in paths che direttamente in config_manager
    # per evitare che gli import precoci usino i valori reali.
    with (
        patch("src.core.paths.CONFIG_DIR", fake_dir),
        patch("src.core.paths.CONFIG_FILE", fake_file),
        patch("src.core.config_manager.CONFIG_DIR", fake_dir),
        patch("src.core.config_manager.CONFIG_FILE", fake_file),
    ):
        yield fake_file


def test_config_manager_defaults(mock_config):
    # Test default retrieval
    val = config_manager.get_config_value("theme", "light")
    assert val == "light"

    # Test setting value
    config_manager.set_config_value("theme", "dark")
    assert config_manager.get_config_value("theme") == "dark"

    # Verify persistence
    with open(mock_config) as f:
        data = json.load(f)
        assert data["theme"] == "dark"


def test_config_accounts(mock_config):
    # Test adding account
    config_manager.add_account("isab", {"username": "user1", "password": "pass1", "is_default": True})
    accounts = config_manager.load_config().get("accounts", [])
    assert len(accounts) == 1
    assert accounts[0]["username"] == "user1"

    # Test default
    default = config_manager.get_default_account("isab")
    assert default["username"] == "user1"

    # Test removal
    config_manager.remove_account("isab", "user1")
    assert len(config_manager.load_config().get("accounts", [])) == 0


# --- DATABASE MANAGER ---
def test_database_manager_singleton():
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    assert db1 is db2


def test_database_manager_connection(tmp_path):
    db_path = tmp_path / "test_db.sqlite"
    manager = DatabaseManager()

    # Initialize Schema (indirectly via simple query first)
    with manager.get_connection(db_path) as conn:
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, val TEXT)")
        conn.execute("INSERT INTO test (val) VALUES ('A')")
        conn.commit()

    rows = manager.execute_query(db_path, "SELECT * FROM test")
    assert len(rows) == 1
    assert rows[0][1] == "A"


# --- TIME MANAGER ---
def test_time_manager():
    # Helper to create datetime
    from datetime import datetime

    from src.core import time_manager

    # Test get_trusted_time
    # It might fail network in test, so it should return system time fallback (False trusted)
    # or True if network works.

    dt, trusted = time_manager.get_trusted_time()
    assert isinstance(dt, datetime)
    assert isinstance(trusted, bool)

    # Mock network time
    with patch("src.core.time_manager.get_network_time") as mock_net:
        mock_net.return_value = datetime(2025, 1, 1, tzinfo=UTC)
        dt, trusted = time_manager.get_trusted_time()
        assert dt == datetime(2025, 1, 1, tzinfo=UTC)
        assert trusted is True

    with patch("src.core.time_manager.get_network_time") as mock_net:
        mock_net.return_value = None
        dt, trusted = time_manager.get_trusted_time()
        assert trusted is False
