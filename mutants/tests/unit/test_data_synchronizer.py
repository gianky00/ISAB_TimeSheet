import sqlite3

import pytest

from src.core.data_synchronizer import DataSynchronizer
from src.core.excel_importer import ExcelImporter


class TestDataSynchronizer:
    @pytest.fixture
    def temp_db(self, tmp_path):
        db_path = tmp_path / "test_sync.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Setup tables
        # Contabilita
        cols_cont = list(ExcelImporter.COLUMNS_MAPPING.values())
        schema_cont = "id INTEGER PRIMARY KEY, year INTEGER, " + ", ".join(
            [f"{c} TEXT" for c in cols_cont]
        )
        cursor.execute(f"CREATE TABLE contabilita ({schema_cont})")

        # Giornaliere
        g_cols = [
            "data",
            "personale",
            "tcl",
            "descrizione",
            "n_prev",
            "odc",
            "pdl",
            "inizio",
            "fine",
            "ore",
            "nome_file",
        ]
        schema_g = "id INTEGER PRIMARY KEY, year INTEGER, " + ", ".join(
            [f"{c} TEXT" for c in g_cols]
        )
        cursor.execute(f"CREATE TABLE giornaliere ({schema_g})")

        # Storico OdA
        s_cols = ExcelImporter.STORICO_ODA_COLS
        schema_s = "id INTEGER PRIMARY KEY, " + ", ".join(
            [f'"{c}" TEXT' for c in s_cols]
        )
        cursor.execute(f"CREATE TABLE storico_oda ({schema_s})")

        # Attivita Programmate
        # ATTIVITA_PROGRAMMATE_COLS already includes "styles"
        a_cols = ExcelImporter.ATTIVITA_PROGRAMMATE_COLS
        schema_a = "id INTEGER PRIMARY KEY, " + ", ".join(
            [f'"{c}" TEXT' for c in a_cols]
        )
        cursor.execute(f"CREATE TABLE attivita_programmate ({schema_a})")

        # Scarico Ore
        so_cols = ExcelImporter.SCARICO_ORE_COLS
        schema_so = "id INTEGER PRIMARY KEY, " + ", ".join(
            [f'"{c}" TEXT' for c in so_cols]
        )
        cursor.execute(f"CREATE TABLE scarico_ore ({schema_so})")

        conn.commit()
        conn.close()
        return db_path

    def test_sync_contabilita_dati(self, temp_db):
        # Prepare data: list of tuples matching columns excluding 'year' (which is added by sync)
        # However, sync_contabilita_dati expects imported_data to have same length as target_columns minus year?
        # No, let's check code: target_columns = ["year"] + ...
        # data = [tuple(...) for r in imported_data]
        # Wait, imported_data usually comes from ExcelImporter which returns rows.
        # The code does `cursor.executemany(..., data)` where data is processed from imported_data.
        # But `target_columns` includes 'year'. Does `imported_data` include year?
        # Looking at sync_contabilita_dati:
        # `target_columns = ["year"] + [values...]`
        # It implies imported_data MUST have year as first element.

        # Let's verify with a sample row.
        # We'll mock 2024 data.
        year = 2024
        # Create a row with 'year' + other cols.
        # Length of ExcelImporter.COLUMNS_MAPPING
        num_cols = len(ExcelImporter.COLUMNS_MAPPING)
        row1 = (year,) + tuple(f"val_{i}" for i in range(num_cols))

        added, removed = DataSynchronizer.sync_contabilita_dati(temp_db, [row1], [year])
        assert added == 1
        assert removed == 0

        # Verify DB
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contabilita WHERE year=?", (year,))
        res = cursor.fetchall()
        assert len(res) == 1
        conn.close()

        # Update: same data, no change
        added, removed = DataSynchronizer.sync_contabilita_dati(temp_db, [row1], [year])
        assert added == 0
        assert removed == 0

        # Update: new row, old removed
        row2 = (year,) + tuple(f"val_new_{i}" for i in range(num_cols))
        added, removed = DataSynchronizer.sync_contabilita_dati(temp_db, [row2], [year])
        assert added == 1
        assert removed == 1

    def test_sync_giornaliere(self, temp_db):
        # Target cols: year, data, personale, descrizione, tcl, odc, pdl, inizio, fine, ore, n_prev, nome_file
        # Total 12 cols.
        year = 2024
        row1 = (
            year,
            "2024-01-01",
            "Mario",
            "Desc",
            "TCL",
            "ODC",
            "PDL",
            "08:00",
            "17:00",
            "8",
            "P1",
            "file.xlsx",
        )

        added, removed = DataSynchronizer.sync_giornaliere(temp_db, [row1], [year])
        assert added == 1
        assert removed == 0

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM giornaliere WHERE year=?", (year,))
        assert len(cursor.fetchall()) == 1
        conn.close()

    def test_sync_storico_oda(self, temp_db):
        # Uses _sync_upsert_smart
        # Mock data for Storico ODA
        # Cols: defined in ExcelImporter.STORICO_ODA_COLS
        # We need to match the length.
        num_cols = len(ExcelImporter.STORICO_ODA_COLS)
        row1 = tuple(f"oda_{i}" for i in range(num_cols))

        added, removed = DataSynchronizer.sync_storico_oda(temp_db, [row1])
        assert added == 1  # Added
        assert removed == 0

        # Same data
        added, removed = DataSynchronizer.sync_storico_oda(temp_db, [row1])
        assert added == 0
        assert removed == 0

        # Modify row (UPSERT replaces it)
        # Note: _sync_upsert_smart uses EXCEPT logic.
        # If we change one value, it counts as 1 update.
        # Row 1 modified
        row1_mod = list(row1)
        row1_mod[0] = "oda_modified"
        row1_mod = tuple(row1_mod)

        # Insert a new one as well
        row2 = tuple(f"oda2_{i}" for i in range(num_cols))

        added, removed = DataSynchronizer.sync_storico_oda(temp_db, [row1_mod, row2])
        # Since logic is INSERT OR REPLACE, and we use a temp table + EXCEPT to count 'changes'.
        # 'row1_mod' is new compared to DB (different content).
        # 'row2' is new.
        # The old 'row1' remains in DB?
        # Wait, _sync_upsert_smart does "INSERT OR REPLACE".
        # It does NOT delete old rows that are missing in new_data unless they collide on Primary Key.
        # But our table schema created here: "id INTEGER PRIMARY KEY, ..."
        # If we don't provide ID, sqlite auto-increments.
        # So 'row1_mod' and 'row2' will be NEW insertions if we don't specify ID?
        # The code for `sync_storico_oda` defines columns. Does it include ID?
        # `ExcelImporter.STORICO_ODA_COLS` usually doesn't include ID, ID is auto-gen.
        # If no unique key is defined (other than ID), REPLACE acts like INSERT.
        # Let's check `_sync_upsert_smart` again.
        # It creates temp table, inserts data.
        # EXCEPT checks diffs.
        # Then INSERT OR REPLACE.
        # If we didn't define a UNIQUE constraint on business keys, this will just keep adding rows.
        # Let's assume the real DB has unique constraints or we should treat it as such.
        # BUT, the test creates table without unique constraints on data columns.
        # So `added` should be 2.

        assert added == 2

    def test_sync_attivita_programmate(self, temp_db):
        # Uses _sync_upsert_smart logic as well (based on reading code)
        # Plus 'styles' is added in sync_attivita_programmate DB cols,
        # but rows_to_insert must match `columns` arg in `_sync_upsert_smart`.
        # Code: `db_cols = list(ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING.values()) + ["styles"]`
        # `rows_to_insert` must match these cols.

        num_cols = (
            len(ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING.values()) + 1
        )  # + styles
        row1 = tuple(f"act_{i}" for i in range(num_cols))

        added, removed = DataSynchronizer.sync_attivita_programmate(temp_db, [row1])
        assert added == 1

    def test_sync_scarico_ore(self, temp_db):
        # Uses DELETE ALL strategy
        num_cols = len(ExcelImporter.SCARICO_ORE_COLS)
        row1 = tuple(f"so_{i}" for i in range(num_cols))

        added, removed = DataSynchronizer.sync_scarico_ore(temp_db, [row1])
        # Initially empty. Old count 0. New count 1.
        # Added = 1, Removed = 0
        assert added == 1
        assert removed == 0

        # Replace with same (DELETE ALL, INSERT)
        # Old 1, New 1. Added 0, Removed 0.
        added, removed = DataSynchronizer.sync_scarico_ore(temp_db, [row1])
        assert added == 0
        assert removed == 0

        # Replace with 2 rows
        row2 = tuple(f"so2_{i}" for i in range(num_cols))
        added, removed = DataSynchronizer.sync_scarico_ore(temp_db, [row1, row2])
        # Old 1, New 2. Added 1, Removed 0.
        assert added == 1
        assert removed == 0

        # Clear
        added, removed = DataSynchronizer.sync_scarico_ore(temp_db, [])
        # Old 2, New 0. Added 0, Removed 2.
        assert added == 0
        assert removed == 2
