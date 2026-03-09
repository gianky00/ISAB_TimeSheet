import sqlite3
import pytest
from src.core.sync.smart_sync import SmartSyncEngine
from src.core.sync.base import BaseSyncEngine

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

    def test_sync_upsert_smart_calculation(self, db_path):
        """Verifica che vengano contati solo i record effettivamente diversi."""
        # 1. '1', 'new', '10.5'  -> MODIFICATO (contato)
        # 2. '2', 'same', '20.0' -> IDENTICO (non contato)
        # 3. '3', 'fresh', '30.0' -> AGGIUNTO (contato)
        new_data = [("1", "new", "10.5"), ("2", "same", "20.0"), ("3", "fresh", "30.0")]
        columns = ["id", "val", "num"]

        # Chiamata diretta all'engine V9.0
        added, removed = SmartSyncEngine.sync_upsert_smart(db_path, "test_table", columns, new_data)

        assert added == 2
        assert removed == 0

        # Verifica persistenza
        conn = sqlite3.connect(db_path)
        res = conn.execute("SELECT val FROM test_table WHERE id='1'").fetchone()
        assert res[0] == "new"
        res_count = conn.execute("SELECT COUNT(*) FROM test_table").fetchone()[0]
        assert res_count == 3
        conn.close()

    def test_sync_upsert_smart_empty(self, db_path):
        added, removed = SmartSyncEngine.sync_upsert_smart(db_path, "test_table", ["id"], [])
        assert added == 0
        assert removed == 0

    def test_validate_identifier_security(self):
        """Verifica la protezione da SQL Injection via BaseSyncEngine."""
        assert BaseSyncEngine._validate_identifier("my_table") == "my_table"
        with pytest.raises(ValueError):
            BaseSyncEngine._validate_identifier("table; DROP")
