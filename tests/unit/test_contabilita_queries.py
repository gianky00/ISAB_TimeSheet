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
        schema = "id INTEGER PRIMARY KEY, year INTEGER, " + ", ".join([f"{c} TEXT" for c in cols])
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
        g_schema = "id INTEGER PRIMARY KEY, year INTEGER, " + ", ".join([f"{c} TEXT" for c in g_cols])
        cursor.execute(f"CREATE TABLE giornaliere ({g_schema})")

        # Other tables
        # Correct schemas based on Importer definitions

        # Attivita Programmate: ps, area, pdl, imp, descrizione, lun, mar, mer, gio, ven, stato_pdl, stato_attivita, data_controllo, personale, po, avviso, styles
        ap_cols = [
            "ps",
            "area",
            "pdl",
            "imp",
            "descrizione",
            "lun",
            "mar",
            "mer",
            "gio",
            "ven",
            "stato_pdl",
            "stato_attivita",
            "data_controllo",
            "personale",
            "po",
            "avviso",
            "styles",
        ]
        schema_ap = "id INTEGER PRIMARY KEY, " + ", ".join([f"{c} TEXT" for c in ap_cols])
        cursor.execute(f"CREATE TABLE attivita_programmate ({schema_ap})")

        # Certificati Campione: modello, costruttore, matricola, range_strumento, errore_max, certificato, scadenza, emissione, id_coemi, stato
        cc_cols = [
            "modello",
            "costruttore",
            "matricola",
            "range_strumento",
            "errore_max",
            "certificato",
            "scadenza",
            "emissione",
            "id_coemi",
            "stato",
        ]
        schema_cc = "id INTEGER PRIMARY KEY, " + ", ".join([f"{c} TEXT" for c in cc_cols])
        cursor.execute(f"CREATE TABLE certificati_campione ({schema_cc})")

        # Scarico Ore: data, pers1, pers2, odc, pos, dalle, alle, totale_ore, descrizione, finito, commessa, styles
        so_cols = [
            "data",
            "pers1",
            "pers2",
            "odc",
            "pos",
            "dalle",
            "alle",
            "totale_ore",
            "descrizione",
            "finito",
            "commessa",
            "styles",
        ]
        schema_so = "id INTEGER PRIMARY KEY, " + ", ".join([f"{c} TEXT" for c in so_cols])
        cursor.execute(f"CREATE TABLE scarico_ore ({schema_so})")

        # Insert sample data
        # Index of 'n_prev' in cols is 2 (Data, Mese, N Prev)
        cursor.execute("INSERT INTO contabilita (year, n_prev) VALUES (2024, 'P1'), (2023, 'P2')")
        cursor.execute("INSERT INTO giornaliere (year, n_prev) VALUES (2024, 'P1'), (2022, 'P3')")

        # Insert sample data for other tables
        cursor.execute(
            "INSERT INTO attivita_programmate (data_controllo, styles) VALUES ('2024-01-01', 'style1')"
        )
        cursor.execute(
            "INSERT INTO certificati_campione (modello, scadenza) VALUES ('Modello1', '01/01/2024')"
        )
        cursor.execute("INSERT INTO scarico_ore (data, styles) VALUES ('2024-01-01', 'style2')")

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

    def test_get_attivita_programmate_data(self, temp_db):
        rows = ContabilitaQueries.get_attivita_programmate_data(temp_db)
        assert len(rows) == 1
        # ATTIVITA_PROGRAMMATE_COLS has data_controllo at index 12 (based on list above)
        # ps(0), area(1), pdl(2), imp(3), descrizione(4), lun(5), mar(6), mer(7), gio(8), ven(9), stato_pdl(10), stato_attivita(11), data_controllo(12)
        assert rows[0][12] == "2024-01-01"

    def test_get_certificati_campione_data(self, temp_db):
        rows = ContabilitaQueries.get_certificati_campione_data(temp_db)
        assert len(rows) == 1
        # modello(0), costruttore(1), matricola(2), range_strumento(3), errore_max(4), certificato(5), scadenza(6)
        assert rows[0][0] == "Modello1"
        assert rows[0][6] == "01/01/2024"

    def test_get_scarico_ore_data(self, temp_db):
        rows = ContabilitaQueries.get_scarico_ore_data(temp_db)
        assert len(rows) == 1
        # data(0)
        assert rows[0][0] == "2024-01-01"
        # Check styles included (last column)
        assert rows[0][-1] == "style2"

    def test_db_not_exists(self):
        assert ContabilitaQueries.get_available_years(Path("missing.db")) == []
        assert ContabilitaQueries.get_data_by_year(Path("missing.db"), 2024) == []
