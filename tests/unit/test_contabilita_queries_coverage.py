import pytest

from src.core.contabilita_queries import ContabilitaQueries
from src.core.database import DatabaseManager


class TestContabilitaQueriesCoverage:
    @pytest.fixture
    def db_path(self, tmp_path, mocker):  # noqa: ANN001
        p_cont = tmp_path / "queries_cont.db"
        p_timb = tmp_path / "queries_timb.db"
        # Patch dei path globali prima di init_db
        mocker.patch.object(DatabaseManager, "DB_CONTABILITA", p_cont)
        mocker.patch.object(DatabaseManager, "DB_TIMBRATURE", p_timb)
        mocker.patch.object(DatabaseManager, "DB_PDL", tmp_path / "queries_pdl.db")
        mocker.patch.object(DatabaseManager, "DB_STORICO_ODA", tmp_path / "queries_oda.db")
        mocker.patch.object(DatabaseManager, "DB_DIPENDENTI", tmp_path / "queries_dip.db")

        DatabaseManager().init_db()
        return p_cont

    def test_get_data_by_year_columns_alignment(self, db_path):  # noqa: ANN001
        """Verifica che la query per anno restituisca tutte le colonne mappate."""
        manager = DatabaseManager()
        # Inserisci riga completa (15 colonne previste dal mapping)
        manager.execute_query(
            db_path,
            "INSERT INTO contabilita (year, n_prev, attivita, odc) VALUES (2024, 'P1', 'A1', 'O1')",
        )

        rows = ContabilitaQueries.get_data_by_year(db_path, 2024)
        assert len(rows) == 1
        # Il numero di colonne restituite deve corrispondere al mapping di ExcelImporter (14 colonne)
        from src.core.excel_importer import ExcelImporter  # noqa: PLC0415

        assert len(rows[0]) == len(ExcelImporter.COLUMNS_MAPPING)

    def test_get_available_years_empty_db(self, tmp_path):  # noqa: ANN001
        """Verifica recupero anni su DB vuoto o inesistente."""
        p = tmp_path / "non_existent.db"
        assert ContabilitaQueries.get_available_years(p) == []

    def test_get_scarico_ore_data_sorting(self, db_path):  # noqa: ANN001
        """Verifica ordinamento decrescente (id DESC) per scarico ore."""
        manager = DatabaseManager()
        manager.execute_query(db_path, "INSERT INTO scarico_ore (descrizione) VALUES ('Prima')")
        manager.execute_query(db_path, "INSERT INTO scarico_ore (descrizione) VALUES ('Ultima')")

        rows = ContabilitaQueries.get_scarico_ore_data(db_path)
        # La colonna 'descrizione' è all'indice 8 nel mapping SCARICO_ORE_COLS
        assert rows[0][8] == "Ultima"
