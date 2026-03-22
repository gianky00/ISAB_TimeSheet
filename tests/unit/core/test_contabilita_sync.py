import sqlite3

import pytest

from src.core.sync.contabilita_sync import ContabilitaSyncEngine


class TestContabilitaSyncEngine:
    @pytest.fixture
    def db_path(self, tmp_path):
        p = tmp_path / "sync_test.db"
        with sqlite3.connect(p) as conn:
            # Crea tabelle minime
            conn.execute(
                "CREATE TABLE giornaliere (year INTEGER, data TEXT, personale TEXT, descrizione TEXT, tcl TEXT, odc TEXT, pdl TEXT, inizio TEXT, fine TEXT, ore REAL, n_prev TEXT, nome_file TEXT)"
            )
            conn.execute(
                "INSERT INTO giornaliere (year, data, personale, ore) VALUES (2024, '2024-01-01', 'Rossi', 8.0)"
            )
            conn.commit()
        return p

    def test_sync_giornaliere_update_logic(self, db_path):
        """Verifica che la sync delle giornaliere rilevi correttamente i cambiamenti."""
        # Nuovi dati per il 2024 (una riga uguale, una cambiata, una nuova)
        new_rows = [
            (
                2024,
                "2024-01-01",
                "Rossi",
                "",
                "",
                "",
                "",
                "",
                "",
                8.0,
                "",
                "file1",
            ),  # Uguale (ma con nome_file)
            (2024, "2024-01-02", "Verdi", "", "", "", "", "", "", 8.0, "", "file1"),  # Nuova
        ]

        # Sincronizziamo l'anno 2024
        added, removed = ContabilitaSyncEngine.sync_giornaliere(db_path, new_rows, [2024])

        # Spiegazione: la riga 'Rossi' è considerata diversa perché nel DB originale mancavano colonne come nome_file (erano NULL)
        # Quindi: 2 aggiunte, 1 rimossa (la vecchia 'Rossi')
        assert added == 2
        assert removed == 1

        with sqlite3.connect(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM giornaliere WHERE year=2024").fetchone()[0]
            assert count == 2

    def test_sync_giornaliere_empty_input(self, db_path):
        """Verifica che input vuoti non facciano nulla."""
        added, removed = ContabilitaSyncEngine.sync_giornaliere(db_path, [], [])
        assert added == 0
        assert removed == 0

    def test_get_diff_count_logic(self, db_path):
        """Testa direttamente l'algoritmo di diff EXCEPT."""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cols = ["year", "personale", "ore"]
            # Crea temp table manuale per il test
            cursor.execute("CREATE TEMP TABLE temp_giornaliere (year INTEGER, personale TEXT, ore REAL)")
            cursor.execute("INSERT INTO temp_giornaliere VALUES (2024, 'Rossi', 8.0)")  # Uguale
            cursor.execute("INSERT INTO temp_giornaliere VALUES (2024, 'Nuovo', 4.0)")  # Nuova

            added, removed = ContabilitaSyncEngine._get_diff_count(cursor, "giornaliere", cols, 2024)

            assert added == 1
            assert removed == 0
