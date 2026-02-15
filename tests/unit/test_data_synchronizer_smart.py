"""
Tests for DataSynchronizer smart upsert logic.
Verifies correct calculation of added/modified rows using EXCEPT.
"""

import sqlite3

import pytest

from src.core.data_synchronizer import DataSynchronizer


class TestDataSynchronizerSmart:
    @pytest.fixture
    def db_path(self, tmp_path):
        path = tmp_path / "sync_test.db"
        # Inizializza tabella con PK
        conn = sqlite3.connect(path)
        conn.execute("CREATE TABLE test_table (id TEXT PRIMARY KEY, val TEXT, num REAL)")
        conn.execute("INSERT INTO test_table VALUES ('1', 'old', 10.5)")
        conn.execute("INSERT INTO test_table VALUES ('2', 'same', 20.0)")
        conn.commit()
        conn.close()
        return path

    def test_sync_upsert_smart_calculation(self, db_path):
        """Verifica che vengano contati solo i record effettivamente diversi."""
        # Nuovi dati:
        # 1. '1', 'new', 10.5  -> MODIFICATO (contato)
        # 2. '2', 'same', 20.0 -> IDENTICO (non contato)
        # 3. '3', 'fresh', 30.0 -> AGGIUNTO (contato)
        new_data = [("1", "new", 10.5), ("2", "same", 20.0), ("3", "fresh", 30.0)]
        columns = ["id", "val", "num"]

        added, removed = DataSynchronizer._sync_upsert_smart(db_path, "test_table", columns, new_data)

        # Dovrebbe aver trovato 2 variazioni (1 mod + 1 new)
        assert added == 2
        assert removed == 0

        # Verifica persistenza nel DB
        conn = sqlite3.connect(db_path)
        res = conn.execute("SELECT val FROM test_table WHERE id='1'").fetchone()
        assert res[0] == "new"
        res_count = conn.execute("SELECT COUNT(*) FROM test_table").fetchone()[0]
        assert res_count == 3
        conn.close()

    def test_sync_upsert_smart_float_precision(self, db_path):
        """Verifica che la precisione dei float non causi falsi positivi (20.0 == 20)."""
        # SQLite CAST(... AS TEXT) di 20.0 potrebbe essere '20.0' o '20'
        # a seconda di come viene salvato.
        # DataSynchronizer usa CAST a TEXT per il confronto.
        new_data = [("2", "same", 20.0)]
        columns = ["id", "val", "num"]

        added, _ = DataSynchronizer._sync_upsert_smart(db_path, "test_table", columns, new_data)

        # Se i tipi sono gestiti correttamente (entrambi castati a TEXT),
        # e il valore è identico, added deve essere 0.
        assert added == 0

    def test_validate_identifier_security(self):
        """Verifica la protezione da SQL Injection negli identificatori."""
        # Validi
        assert DataSynchronizer._validate_identifier("my_table") == "my_table"
        assert DataSynchronizer._validate_identifier("col1") == "col1"

        # Non validi (Exception)
        with pytest.raises(ValueError):
            DataSynchronizer._validate_identifier("table; DROP TABLE users")
        with pytest.raises(ValueError):
            DataSynchronizer._validate_identifier("col-- comment")
        with pytest.raises(ValueError):
            DataSynchronizer._validate_identifier("table name")
