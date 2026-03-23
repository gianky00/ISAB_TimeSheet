import sqlite3

import pytest

from src.core.sync.smart_sync import SmartSyncEngine


class TestSmartSyncEngine:
    @pytest.fixture
    def mock_db(self, tmp_path):
        """Crea un DB reale in un path temporaneo per testare l'algoritmo SQL."""
        db_path = tmp_path / "test_sync.db"
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, val TEXT, num REAL)")
            conn.execute("INSERT INTO test_table VALUES (1, 'A', 10.5)")
            conn.commit()
        return db_path

    def test_sync_upsert_smart_no_change(self, mock_db):
        """Verifica che dati identici non generino delta (+0)."""
        cols = ["id", "val", "num"]
        # Dati identici a quelli già nel DB
        new_data = [(1, "A", 10.5)]

        added, _removed = SmartSyncEngine.sync_upsert_smart(
            mock_db, "test_table", cols, new_data, conflict_cols=["id"]
        )

        assert added == 0, "Non dovrebbero esserci aggiunte se i dati sono identici"

    def test_sync_upsert_smart_update(self, mock_db):
        """Verifica il rilevamento di una modifica su riga esistente."""
        cols = ["id", "val", "num"]
        # Cambiamo 'A' in 'B'
        new_data = [(1, "B", 10.5)]

        added, _removed = SmartSyncEngine.sync_upsert_smart(
            mock_db, "test_table", cols, new_data, conflict_cols=["id"]
        )

        assert added == 1
        with sqlite3.connect(mock_db) as conn:
            row = conn.execute("SELECT val FROM test_table WHERE id=1").fetchone()
            assert row[0] == "B"

    def test_sync_upsert_smart_new_row(self, mock_db):
        """Verifica l'inserimento di una nuova riga."""
        cols = ["id", "val", "num"]
        new_data = [(1, "A", 10.5), (2, "New", 20.0)]

        added, _removed = SmartSyncEngine.sync_upsert_smart(
            mock_db, "test_table", cols, new_data, conflict_cols=["id"]
        )

        assert added == 1  # Solo la riga 2 è nuova
        with sqlite3.connect(mock_db) as conn:
            count = conn.execute("SELECT COUNT(*) FROM test_table").fetchone()[0]
            assert count == 2
