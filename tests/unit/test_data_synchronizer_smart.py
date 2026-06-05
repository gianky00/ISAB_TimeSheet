import sqlite3

import pytest

from src.application.services.exceptions import ValidationError
from src.application.services.sync.base import BaseSyncEngine, SyncTarget
from src.application.services.sync.smart_sync import SmartSyncEngine


class TestDataSynchronizerSmart:
    @pytest.fixture
    def db_path(self, tmp_path):
        path = tmp_path / "sync_test_smart.db"
        conn = sqlite3.connect(path)
        # Usiamo tipi consistenti per evitare ambiguità di cast
        conn.execute("CREATE TABLE test_table (id TEXT PRIMARY KEY, val TEXT, num TEXT)")
        conn.execute("INSERT INTO test_table VALUES ('1', 'old', '10.5')")
        conn.execute("INSERT INTO test_table VALUES ('2', 'same', '20.0')")
        conn.commit()
        conn.close()
        return path

    def test_sync_upsert_smart_calculation(self, db_path, mocker):
        """Verifica che vengano contati solo i record effettivamente diversi."""
        mocker.patch(
            "src.application.services.sync.smart_sync.db_manager.get_connection",
            return_value=sqlite3.connect(db_path),
        )
        new_data = [("1", "new", "10.5"), ("2", "same", "20.0"), ("3", "fresh", "30.0")]
        columns = ["id", "val", "num"]
        target = SyncTarget(db_path=db_path, table_name="test_table", columns=columns)

        added, removed = SmartSyncEngine.sync_upsert_smart(target, new_data)

        assert added == 2
        assert removed == 0

        # Verifica persistenza
        conn = sqlite3.connect(db_path)
        res = conn.execute("SELECT val FROM test_table WHERE id='1'").fetchone()
        assert res[0] == "new"
        res_count = conn.execute("SELECT COUNT(*) FROM test_table").fetchone()[0]
        assert res_count == 3
        conn.close()

    def test_sync_upsert_smart_empty(self, db_path, mocker):
        mocker.patch(
            "src.application.services.sync.smart_sync.db_manager.get_connection",
            return_value=sqlite3.connect(db_path),
        )
        target = SyncTarget(db_path=db_path, table_name="test_table", columns=["id"])
        added, removed = SmartSyncEngine.sync_upsert_smart(target, [])
        assert added == 0
        assert removed == 0

    def test_validate_identifier_security(self):
        """Verifica la protezione da SQL Injection via BaseSyncEngine."""
        assert BaseSyncEngine._validate_identifier("my_table") == "my_table"
        with pytest.raises(ValidationError):
            BaseSyncEngine._validate_identifier("table; DROP")

    def test_sync_upsert_with_extra_columns(self, tmp_path, mocker):
        """Verifica che le colonne extra non presenti nel sync vengano preservate via conflict_cols."""
        db_path = tmp_path / "extra_cols.db"
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE t (id TEXT PRIMARY KEY, sync_val TEXT, extra_val TEXT)")
        conn.execute("INSERT INTO t VALUES ('1', 'old', 'keep_me')")
        conn.commit()
        conn.close()

        mocker.patch(
            "src.application.services.sync.smart_sync.db_manager.get_connection",
            return_value=sqlite3.connect(db_path),
        )

        new_data = [("1", "new")]
        columns = ["id", "sync_val"]
        target = SyncTarget(db_path=db_path, table_name="t", columns=columns)

        SmartSyncEngine.sync_upsert_smart(target, new_data, conflict_cols=["id"])

        conn = sqlite3.connect(db_path)
        row = conn.execute("SELECT sync_val, extra_val FROM t WHERE id='1'").fetchone()
        assert row[0] == "new"
        assert row[1] == "keep_me"  # Deve essere preservato!
        conn.close()
