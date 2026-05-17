import sqlite3
from unittest.mock import patch

import pandas as pd
import pytest

from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage


class TestTimbratureStorage:
    @pytest.fixture
    def db_conn(self, tmp_path):
        """Fixture per creare un database di test in-memory con la tabella timbrature."""
        db_path = tmp_path / "test_timbrature.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE timbrature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                cognome TEXT,
                codice_fiscale TEXT UNIQUE,
                data TEXT,
                ingresso TEXT,
                uscita TEXT,
                fornitore TEXT,
                presenza_ts TEXT,
                sito_timbratura TEXT
            )
        """)
        conn.commit()
        conn.close()
        return db_path

    def test_ensure_columns(self, db_conn):
        """Testa che le colonne mancanti vengano aggiunte automaticamente."""
        storage = TimbratureStorage(db_path=db_conn)

        with sqlite3.connect(db_conn) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(timbrature)")
            cols = [row[1] for row in cursor.fetchall()]
            assert "id_dipendente" in cols
            assert "codice_rilpres" in cols

    def test_search_employees(self, db_conn):
        storage = TimbratureStorage(db_path=db_conn)
        with sqlite3.connect(db_conn) as conn:
            conn.execute(
                "INSERT INTO timbrature (nome, cognome, codice_fiscale) VALUES ('Mario', 'Rossi', 'RSSMRA')"
            )
            conn.commit()

        results = storage.search_employees("mari")
        assert len(results) == 1
        assert results[0]["nome"] == "Mario"

        assert storage.search_employees("x") == []  # Too short

    @patch("src.core.config_manager.load_config")
    def test_get_employees_with_mappings(self, mock_load, db_conn):
        mock_load.return_value = {"employee_mappings": {"Mario|Rossi": {"reparto": "R1", "cantiere": "C1"}}}
        storage = TimbratureStorage(db_path=db_conn)
        with sqlite3.connect(db_conn) as conn:
            conn.execute(
                "INSERT INTO timbrature (nome, cognome, codice_fiscale) VALUES ('Mario', 'Rossi', 'RSSMRA')"
            )
            conn.commit()

        emps = storage.get_employees()
        assert len(emps) == 1
        assert emps[0]["reparto"] == "R1"

    @patch("src.core.config_manager.set_config_value")
    @patch("src.core.config_manager.load_config")
    def test_update_employee_details(self, mock_load, mock_set, db_conn):
        mock_load.return_value = {"employee_mappings": {}}
        storage = TimbratureStorage(db_path=db_conn)

        storage.update_employee_details("Mario", "Rossi", reparto="R2")

        args, kwargs = mock_set.call_args
        assert args[0] == "employee_mappings"
        assert args[1]["Mario|Rossi"]["reparto"] == "R2"

    def test_normalize_search_date(self):
        storage = TimbratureStorage()
        assert storage._normalize_search_date("15/10/2023") == "2023-10-15"
        assert storage._normalize_search_date("15.10.23") == "2023-10-15"
        assert storage._normalize_search_date("15/10") == "-10-15"
        assert storage._normalize_search_date("abc") == "abc"

    @patch("src.core.config_manager.load_config")
    def test_get_timbrature_with_reparto(self, mock_load, db_conn):
        mock_load.return_value = {"employee_mappings": {"Mario|Rossi": {"reparto": "TEST"}}}
        storage = TimbratureStorage(db_path=db_conn)

        with sqlite3.connect(db_conn) as conn:
            conn.execute("""
                INSERT INTO timbrature (data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura)
                VALUES ('2023-01-01', '08:00', '17:00', 'Mario', 'Rossi', 'S', 'Sito')
            """)
            conn.commit()

        res = storage.get_timbrature_with_reparto(filter_reparto="TEST")
        assert len(res) == 1
        assert res[0][3] == "Mario"
        assert res[0][-2] == "TEST"  # Reparto enriched

    @patch("src.core.sync_tracker.SyncTracker.update_status")
    @patch("pandas.read_excel")
    def test_import_excel(self, mock_read, mock_sync, db_conn):
        storage = TimbratureStorage(db_path=db_conn)
        df = pd.DataFrame(
            {
                "Id Dipendente": ["1"],
                "Data Timbratura": ["2023-01-01"],
                "Nome Risorsa": ["Mario"],
                "Cognome Risorsa": ["Rossi"],
                "Codice Fiscale": ["RSSMRA"],
            }
        )
        mock_read.return_value = df

        success = storage.import_excel("fake.xlsx")
        assert success is True
        assert mock_sync.called

        with sqlite3.connect(db_conn) as conn:
            count = conn.execute("SELECT COUNT(*) FROM timbrature").fetchone()[0]
            assert count == 1
