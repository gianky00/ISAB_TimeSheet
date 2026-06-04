from unittest.mock import patch

import pytest

from src.application.services.data_synchronizer import DataSynchronizer


class TestDataSynchronizerDeep:
    @pytest.fixture
    def db_path(self, tmp_path):
        """Prepara un database SQLite temporaneo per i test di sync con schema completo."""
        db = tmp_path / "sync_deep_v2.db"
        import sqlite3

        with sqlite3.connect(db) as conn:
            conn.execute("CREATE TABLE contabilita (id_coemi TEXT, rda TEXT, anno INTEGER)")
            conn.execute("CREATE TABLE giornaliere (nome TEXT, anno INTEGER)")
            # Schema completo per scarico_ore come definito in ScaricoOreImporter.SCARICO_ORE_COLS
            conn.execute("""
                CREATE TABLE scarico_ore (
                    data TEXT, pers1 TEXT, pers2 TEXT, odc TEXT, pos TEXT,
                    dalle TEXT, alle TEXT, totale_ore REAL, descrizione TEXT,
                    finito TEXT, commessa TEXT, styles TEXT
                )
            """)
        return db

    @patch("src.application.services.sync.contabilita_sync.ContabilitaSyncEngine.sync_contabilita")
    def test_sync_contabilita_dati_incremental(self, mock_sync, db_path):
        """Test alias e delega sync contabilità."""
        mock_sync.return_value = (10, 0)

        import_data = [{"id_coemi": "1", "rda": "A"}]
        added, _removed = DataSynchronizer.sync_contabilita_dati(db_path, import_data, [2024])

        assert added == 10
        assert mock_sync.called

    @patch("src.application.services.sync.contabilita_sync.ContabilitaSyncEngine.sync_giornaliere")
    def test_sync_giornaliere_by_year_isolation(self, mock_sync, db_path):
        """Test isolamento annuale sync giornaliere."""
        mock_sync.return_value = (5, 2)

        res = DataSynchronizer.sync_giornaliere(db_path, [], [2023, 2024])
        assert res == (5, 2)
        assert mock_sync.called

    def test_sync_generic_scarico_ore(self, db_path):
        """Test sincronizzazione full replace con metadati per scarico ore."""
        # Riga iniziale (12 colonne)
        initial_row = ("2024-01-01", "P1", "", "ODC1", "10", "08:00", "17:00", 9.0, "Desc", "S", "C1", "{}")
        DataSynchronizer.sync_scarico_ore(db_path, [initial_row])

        # Sostituzione totale con 2 nuove righe
        new_rows = [
            ("2024-01-02", "P2", "", "ODC2", "20", "09:00", "18:00", 9.0, "Desc2", "S", "C2", "{}"),
            ("2024-01-03", "P3", "", "ODC3", "30", "10:00", "19:00", 9.0, "Desc3", "S", "C3", "{}"),
        ]

        added, removed = DataSynchronizer.sync_scarico_ore(db_path, new_rows)

        # V9.4: sync_full_replace_with_metadata ritorna il totale degli inserimenti (len(new_data))
        assert added == 2
        assert removed == 0

    def test_sync_empty_data(self, db_path):
        """Verifica che il sync con dati vuoti non rompa nulla."""
        res = DataSynchronizer.sync_contabilita(db_path, [], [])
        assert res == (0, 0)

        res_oda = DataSynchronizer.sync_storico_oda(db_path, [])
        assert res_oda == (0, 0)
