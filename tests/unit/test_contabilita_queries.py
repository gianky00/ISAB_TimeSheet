import sqlite3
from pathlib import Path

import pytest

from src.core.contabilita_queries import ContabilitaQueries
from src.core.excel_importer import ExcelImporter


class TestContabilitaQueries:
    @pytest.fixture
    def temp_db(self, tmp_path):
        db_path = tmp_path / "test_contabilita.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table 'contabilita' using actual mapping values
        cols = list(ExcelImporter.COLUMNS_MAPPING.values())
        # Add 'id' and 'year' which are always present in DB
        schema = "id INTEGER PRIMARY KEY, year INTEGER, " + ", ".join(
            [f"{c} TEXT" for c in cols]
        )
        cursor.execute(f"CREATE TABLE contabilita ({schema})")

        # Create table 'giornaliere'
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
        g_schema = "id INTEGER PRIMARY KEY, year INTEGER, " + ", ".join(
            [f"{c} TEXT" for c in g_cols]
        )
        cursor.execute(f"CREATE TABLE giornaliere ({g_schema})")

        # Other tables
        cursor.execute(
            "CREATE TABLE attivita_programmate (id INTEGER PRIMARY KEY, data TEXT, commessa TEXT, n_prev TEXT, attivita TEXT, desc TEXT, cantiere TEXT, status TEXT, styles TEXT)"
        )
        cursor.execute(
            "CREATE TABLE certificati_campione (id INTEGER PRIMARY KEY, data TEXT, commessa TEXT, n_prev TEXT, attivita TEXT, desc TEXT, cantiere TEXT, status TEXT)"
        )
        cursor.execute(
            "CREATE TABLE scarico_ore (id INTEGER PRIMARY KEY, data TEXT, commessa TEXT, n_prev TEXT, attivita TEXT, desc TEXT, cantiere TEXT, status TEXT, styles TEXT)"
        )

        # Insert sample data
        # Index of 'n_prev' in cols is 2 (Data, Mese, N Prev)
        cursor.execute(
            "INSERT INTO contabilita (year, n_prev) VALUES (2024, 'P1'), (2023, 'P2')"
        )
        cursor.execute(
            "INSERT INTO giornaliere (year, n_prev) VALUES (2024, 'P1'), (2022, 'P3')"
        )

        conn.commit()
        conn.close()
        return db_path

    def test_get_available_years(self, temp_db):
        years = ContabilitaQueries.get_available_years(temp_db)
        # 2024, 2023 from contabilita; 2024, 2022 from giornaliere
        assert sorted(years, reverse=True) == [2024, 2023, 2022]

    def test_get_data_by_year(self, temp_db):
        rows = ContabilitaQueries.get_data_by_year(temp_db, 2024)
        assert len(rows) == 1
        # In the query 'SELECT data_prev, mese, n_prev...', n_prev is at index 2
        assert rows[0][2] == "P1"

    def test_get_giornaliere_by_year(self, temp_db):
        rows = ContabilitaQueries.get_giornaliere_by_year(temp_db, 2024)
        assert len(rows) == 1
        # 'SELECT data, personale, tcl, descrizione, n_prev...', n_prev is at index 4
        assert rows[0][4] == "P1"

    def test_db_not_exists(self):
        assert ContabilitaQueries.get_available_years(Path("missing.db")) == []
        assert ContabilitaQueries.get_data_by_year(Path("missing.db"), 2024) == []
