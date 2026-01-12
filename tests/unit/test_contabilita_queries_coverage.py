
import pytest

from src.core.contabilita_queries import ContabilitaQueries
from src.core.database import DatabaseManager


class TestContabilitaQueriesCoverage:
    @pytest.fixture
    def db_path(self, tmp_path):
        p = tmp_path / "queries.db"
        DatabaseManager().init_db() # Crea schema reale in path temporaneo
        # Nota: init_db usa i path globali, dobbiamo patcharli
        return p

    def test_get_data_by_year_columns_alignment(self, db_path, mocker):
        """Verifica che la query per anno restituisca tutte le colonne mappate."""
        mocker.patch("src.core.database.db_manager.get_connection", side_effect=lambda p, read_only=False: DatabaseManager().get_connection(db_path, read_only))

        manager = DatabaseManager()
        # Inserisci riga completa (15 colonne previste dal mapping)
        cols = ["year", "n_prev", "attivita", "odc"]
        manager.execute_query(db_path, "INSERT INTO contabilita (year, n_prev, attivita, odc) VALUES (2024, 'P1', 'A1', 'O1')")

        rows = ContabilitaQueries.get_data_by_year(db_path, 2024)
        assert len(rows) == 1
        # Il numero di colonne restituite deve corrispondere al mapping di ExcelImporter (14 colonne)
        from src.core.excel_importer import ExcelImporter
        assert len(rows[0]) == len(ExcelImporter.COLUMNS_MAPPING)

    def test_get_available_years_empty_db(self, tmp_path):
        """Verifica recupero anni su DB vuoto o inesistente."""
        p = tmp_path / "non_existent.db"
        assert ContabilitaQueries.get_available_years(p) == []

    def test_get_scarico_ore_data_sorting(self, db_path, mocker):
        """Verifica ordinamento decrescente (id DESC) per scarico ore."""
        mocker.patch("src.core.database.db_manager.get_connection", side_effect=lambda p, read_only=False: DatabaseManager().get_connection(db_path, read_only))

        manager = DatabaseManager()
        manager.execute_query(db_path, "INSERT INTO scarico_ore (descrizione) VALUES ('Prima')")
        manager.execute_query(db_path, "INSERT INTO scarico_ore (descrizione) VALUES ('Ultima')")

        rows = ContabilitaQueries.get_scarico_ore_data(db_path)
        # La colonna 'descrizione' è all'indice 8 nel mapping SCARICO_ORE_COLS
        assert rows[0][8] == "Ultima"
