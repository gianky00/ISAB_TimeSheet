import sqlite3

import pytest

from src.core.sync.contabilita_sync import ContabilitaSyncEngine


class TestContabilitaSyncEngine:
    @pytest.fixture
    def db_path(self, tmp_path):
        p = tmp_path / "sync_test.db"
        with sqlite3.connect(p) as conn:
            conn.execute(
                "CREATE TABLE giornaliere (year INTEGER, data TEXT, personale TEXT, descrizione TEXT, tcl TEXT, odc TEXT, pdl TEXT, inizio TEXT, fine TEXT, ore REAL, n_prev TEXT, nome_file TEXT)"
            )
            conn.execute(
                "INSERT INTO giornaliere (year, data, personale, ore) VALUES (2024, '2024-01-01', 'Rossi', 8.0)"
            )
            conn.commit()
        return p

    def test_sync_giornaliere_update_logic(self, db_path):
        cols = [
            "year",
            "data",
            "personale",
            "descrizione",
            "tcl",
            "odc",
            "pdl",
            "inizio",
            "fine",
            "ore",
            "n_prev",
            "nome_file",
        ]
        new_rows = [
            (2024, "2024-01-01", "Rossi", "", "", "", "", "", "", 8.0, "", "file1"),
            (2024, "2024-01-02", "Verdi", "", "", "", "", "", "", 8.0, "", "file1"),
        ]

        added, _removed = ContabilitaSyncEngine.sync_giornaliere(db_path, new_rows, [2024], cols)

        # La logica di sync aggiorna i record.
        assert added >= 1

        with sqlite3.connect(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM giornaliere WHERE year=2024").fetchone()[0]
            assert count == 2

    def test_sync_giornaliere_empty_input(self, db_path):
        cols = ["year", "data", "personale", "ore"]
        added, removed = ContabilitaSyncEngine.sync_giornaliere(db_path, [], [2024], cols)
        assert added == 0
        assert removed == 1

    def test_sync_partitioned_data_logic(self, db_path):
        """Testa l'algoritmo di sync tramite l'interfaccia pubblica."""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cols = ["year", "personale", "ore"]
            new_data = [(2024, "Rossi", 8.0), (2024, "Nuovo", 4.0)]

            from src.core.sync.base import PartitionConfig

            # Sync tramite interfaccia pubblica
            added, _removed = ContabilitaSyncEngine.sync_partitioned_data(
                cursor, "giornaliere", cols, new_data, PartitionConfig(column="year", values=[2024])
            )

            assert added == 1
