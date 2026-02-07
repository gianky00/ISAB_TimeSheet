import sqlite3

import pytest

from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.database.migrations import contabilita, storico_oda


class TestDataSynchronizerRobust:
    @pytest.fixture
    def test_db(self, tmp_path):
        """Crea un database di test completo con schema aggiornato."""
        db_path = tmp_path / "test_sync.db"
        # Inizializza schema
        with db_manager.get_connection(db_path) as conn:
            # Eseguiamo le migrazioni necessarie per creare le tabelle
            contabilita.mig_contabilita_v1(conn)
            # Per storico_oda dobbiamo controllare la funzione esatta
            try:
                storico_oda.mig_storico_oda_v1(conn)
            except AttributeError:
                # Fallback: crea tabella manualmente se nome funzione diverso
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS storico_oda (numero_oda TEXT PRIMARY KEY, stato TEXT)"
                )

            conn.commit()
        return db_path

    def test_validate_identifier(self):
        """Test validazione identificatori SQL."""
        assert DataSynchronizer._validate_identifier("valid_table_123") == "valid_table_123"
        with pytest.raises(ValueError, match="non sicuro"):
            DataSynchronizer._validate_identifier("table; DROP TABLE users")
        with pytest.raises(ValueError, match="non sicuro"):
            DataSynchronizer._validate_identifier("col-name")

    def test_sync_contabilita_dati(self, test_db):
        """Test sincronizzazione contabilità con diffing per anno."""
        from src.core.excel_importer import ExcelImporter

        cols = ["year", *list(ExcelImporter.COLUMNS_MAPPING.values())]

        # Inseriamo un record esistente per il 2023
        with db_manager.get_connection(test_db) as conn:
            placeholders = ", ".join(["?"] * len(cols))
            row = ["2023"] + ["val"] * (len(cols) - 1)
            # Quote column names for safety
            safe_cols_str = ", ".join([f'"{c}"' for c in cols])
            conn.execute(
                f"INSERT INTO contabilita ({safe_cols_str}) VALUES ({placeholders})",
                row,
            )
            conn.commit()

        # 2. Sync: Nuovo record per 2023, mantieni lo stesso (0 add, 0 remove)
        data_same = [tuple(row)]
        added, removed = DataSynchronizer.sync_contabilita_dati(test_db, data_same, [2023])
        assert added == 0
        assert removed == 0

        # 3. Sync: Cambia record 2023 (1 add, 1 remove)
        row_new = list(row)
        row_new[2] = "changed"
        added, removed = DataSynchronizer.sync_contabilita_dati(test_db, [tuple(row_new)], [2023])
        assert added == 1
        assert removed == 1

    def test_sync_giornaliere(self, test_db):
        """Test sincronizzazione giornaliere."""
        new_rows = [
            (
                "2024",
                "01.01.2024",
                "Rossi",
                "Desc",
                "TCL1",
                "ODC1",
                "123456/S",
                "08:00",
                "17:00",
                "8",
                "1",
                "file.xlsx",
            )
        ]
        # In sync_giornaliere years_to_clear aspetta lista di int
        added, removed = DataSynchronizer.sync_giornaliere(test_db, new_rows, [2024])

        assert added == 1
        assert removed == 0

        # Verifica persistenza
        with db_manager.get_connection(test_db) as conn:
            res = conn.execute("SELECT COUNT(*) FROM giornaliere WHERE year = 2024").fetchone()
            assert res[0] == 1

    def test_sync_scarico_ore_massive(self, test_db):
        """Test sincronizzazione massiva (Scarico Ore)."""
        # 1. Popola DB con 5 righe (solo alcune colonne per semplicità)
        rows_old = [
            (
                "2024-01-01",
                "P1",
                "P2",
                "ODC1",
                "10",
                "08:00",
                "17:00",
                "8.0",
                "D",
                "S",
                "C",
                "S",
            )
            for i in range(5)
        ]
        with db_manager.get_connection(test_db) as conn:
            conn.executemany(
                "INSERT INTO scarico_ore (data, pers1, pers2, odc, pos, dalle, alle, totale_ore, descrizione, finito, commessa, styles) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                rows_old,
            )
            conn.commit()

        # 2. Sync con 10 nuove righe
        rows_new = [tuple(["val"] * 12) for _ in range(10)]

        added, removed = DataSynchronizer.sync_scarico_ore(test_db, rows_new)

        assert added == 5  # 10 - 5
        assert removed == 0

    def test_sync_upsert_smart_no_change(self, test_db):
        """Test upsert intelligente senza modifiche."""
        cols = ["id", "styles"]
        data = [(1, "bold"), (2, "italic")]

        # Primo sync (tutto nuovo)
        added, _ = DataSynchronizer._sync_upsert_smart(test_db, "attivita_programmate", cols, data)
        assert added == 2

        # Secondo sync (identico)
        added, _updated = DataSynchronizer._sync_upsert_smart(test_db, "attivita_programmate", cols, data)
        assert added == 0

    def test_sync_empty_data(self, test_db):
        """Test sincronizzazione con liste vuote."""
        assert DataSynchronizer.sync_contabilita_dati(test_db, [], []) == (0, 0)
        assert DataSynchronizer.sync_giornaliere(test_db, [], []) == (0, 0)

    def test_sync_error_handling(self, test_db):
        """Test gestione errori SQL."""
        with pytest.raises(sqlite3.OperationalError):
            DataSynchronizer._sync_upsert_smart(test_db, "non_existent_table", ["col1"], [(1,)])
