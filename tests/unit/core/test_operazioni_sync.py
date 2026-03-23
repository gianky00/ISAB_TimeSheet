import sqlite3

import pytest

from src.core.sync.operazioni_sync import OperazioniSyncEngine


class TestOperazioniSyncEngine:
    @pytest.fixture
    def db_path(self, tmp_path):  # noqa: ANN001
        p = tmp_path / "ops_test.db"
        with sqlite3.connect(p) as conn:
            # Crea tabella con tutte le colonne previste da SCARICO_ORE_COLS
            conn.execute("""
                CREATE TABLE scarico_ore (
                    data TEXT, pers1 TEXT, pers2 TEXT, odc TEXT, pos TEXT,
                    dalle TEXT, alle TEXT, totale_ore REAL, descrizione TEXT,
                    finito TEXT, commessa TEXT, styles TEXT
                )
            """)
            conn.execute("""
                INSERT INTO scarico_ore (data, pers1, totale_ore, commessa, styles)
                VALUES ('2024-01-01', 'Rossi', 8.0, 'C1', '')
            """)
            conn.commit()
        return p

    def test_sync_scarico_ore_full_replace(self, db_path):  # noqa: ANN001
        """Verifica la sostituzione completa dei dati scarico ore."""
        # Creiamo righe con 11 colonne come previsto dallo schema
        new_data = [
            ("2024-01-02", "Verdi", "", "123", "10", "08:00", "17:00", 8.0, "D2", "NO", "C2", ""),
            ("2024-01-03", "Bianchi", "", "124", "20", "08:00", "12:00", 4.0, "D3", "NO", "C3", ""),
        ]

        added, removed = OperazioniSyncEngine.sync_scarico_ore(db_path, new_data)

        # New Count (2) - Old Count (1) = 1 aggiunta netta
        # Old Count (1) - New Count (2) = 0 rimosse nette (limite della logica attuale)
        assert added == 1
        assert removed == 0

        with sqlite3.connect(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM scarico_ore").fetchone()[0]
            assert count == 2  # noqa: PLR2004
            # Verifica che la vecchia riga 'Rossi' sia sparita
            rossi = conn.execute("SELECT * FROM scarico_ore WHERE pers1='Rossi'").fetchone()
            assert rossi is None

    def test_sync_scarico_ore_batching(self, db_path):  # noqa: ANN001
        """Verifica che il batching funzioni con molte righe (simulato con 100)."""
        # Creiamo 100 righe con 12 colonne
        large_data = [("2024-01-01", "P", "", "ODC", "10", "08", "17", 1.0, "D", "NO", "C", "")] * 100

        added, _removed = OperazioniSyncEngine.sync_scarico_ore(db_path, large_data)

        assert added == 99  # 100 new - 1 old  # noqa: PLR2004
        with sqlite3.connect(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM scarico_ore").fetchone()[0]
            assert count == 100  # noqa: PLR2004
