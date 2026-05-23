import sqlite3
from pathlib import Path
from unittest.mock import patch

from src.core.sync.operazioni_sync import OperazioniSyncEngine


class TestOperazioniSyncEngine:
    def _setup_db(self, db_path, table_name, columns):
        conn = sqlite3.connect(db_path)
        cols_def = ", ".join([f"{c} TEXT" for c in columns])
        conn.execute(f"CREATE TABLE {table_name} ({cols_def})")
        return conn

    @patch("src.core.sync.operazioni_sync.db_manager.get_connection")
    def test_sync_attivita_programmate(self, mock_conn):
        # We don't need a real db if we mock everything, but testing with real SQLite is better
        conn = sqlite3.connect(":memory:")
        # We need to know the columns expected. The code uses ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING
        # Let's mock ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING
        with patch("src.core.sync.operazioni_sync.ExcelImporter") as mock_importer:
            mock_importer.ATTIVITA_PROGRAMMATE_MAPPING = {"Col1": "db_col1", "Col2": "db_col2"}
            conn.execute("CREATE TABLE attivita_programmate (db_col1 TEXT, db_col2 TEXT, styles TEXT)")
            conn.execute("INSERT INTO attivita_programmate VALUES ('old1', 'old2', 's')")

            mock_conn.return_value.__enter__.return_value = conn

            rows_to_insert = [("new1", "new2", "s1"), ("new3", "new4", "s2")]

            added, removed = OperazioniSyncEngine.sync_attivita_programmate(Path("dummy.db"), rows_to_insert)

            assert added == 1  # 2 (new) - 1 (old)
            assert removed == 0  # max(0, 1 - 2)

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attivita_programmate")
            res = cursor.fetchall()
            assert len(res) == 2
            assert res[0][0] == "new1"

    @patch("src.core.sync.operazioni_sync.db_manager.get_connection")
    def test_sync_scarico_ore(self, mock_conn):
        conn = sqlite3.connect(":memory:")
        with patch("src.core.sync.operazioni_sync.ExcelImporter") as mock_importer:
            mock_importer.SCARICO_ORE_COLS = ["col1", "col2"]
            conn.execute("CREATE TABLE scarico_ore (col1 TEXT, col2 TEXT)")
            conn.execute("INSERT INTO scarico_ore VALUES ('o1', 'o2')")
            conn.execute("INSERT INTO scarico_ore VALUES ('o3', 'o4')")

            mock_conn.return_value.__enter__.return_value = conn

            rows_to_insert = [("n1", "n2")]

            added, removed = OperazioniSyncEngine.sync_scarico_ore(Path("dummy.db"), rows_to_insert)

            assert added == 0  # 1 - 2 -> 0
            assert removed == 1  # 2 - 1 -> 1

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scarico_ore")
            res = cursor.fetchall()
            assert len(res) == 1
            assert res[0][0] == "n1"
