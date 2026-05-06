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
        """Testa l'algoritmo di diff tramite l'orchestrazione base."""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cols = ["year", "personale", "ore"]
            # Dati attuali nel DB (da fixture): (2024, 'Rossi', 8.0)

            # Nuovi dati: uno uguale, uno nuovo
            new_data = [
                (2024, "Rossi", 8.0),  # Uguale
                (2024, "Nuovo", 4.0),  # Nuova
            ]

            # Eseguiamo la sync partizionata per l'anno 2024
            added, removed = ContabilitaSyncEngine._sync_partitioned_table(
                cursor, "giornaliere", cols, "year", [2024], new_data
            )

            # Rossi originale viene rimosso e riaggiunto (perché facciamo full replace della partizione)
            # ma il conteggio diff (EXCEPT) dovrebbe rilevare solo le differenze reali di contenuto.
            # In realtà _sync_partitioned_table calcola diff prima del replace.
            assert added == 1  # Solo 'Nuovo' è nuovo
            assert removed == 0 # 'Rossi' era già lì (identico)
