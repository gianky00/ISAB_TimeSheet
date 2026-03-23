from unittest.mock import patch

import pytest

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaLogic:
    @pytest.fixture
    def manager(self):
        return ContabilitaManager

    def test_import_data_success(self, manager):  # noqa: ANN001
        mock_rows = [{"year": 2024}]
        with (
            patch(
                "src.core.contabilita_manager.ExcelImporter.import_contabilita_dati",
                return_value=(True, "OK", mock_rows, [2024]),
            ),
            patch("src.core.contabilita_manager.DataSynchronizer.sync_contabilita_dati", return_value=(1, 0)),
        ):
            success, _msg, added, _removed = manager.import_data_from_excel("mock.xlsx")
            assert success is True
            assert added == 1

    def test_get_year_stats(self, manager):  # noqa: ANN001
        # Mock dei dati restituiti dalle query (14 colonne per OdA, 11 per Giornaliere)
        # OdA mapping: data_prev(0), mese(1), n_prev(2), totale_prev(3), attivita(4), tcl(5), odc(6), stato_attivita(7), tipologia(8), ore_sp(9)...
        mock_oda = [
            (
                "2024-01-01",
                "GEN",
                "PREV-001",
                1000.0,
                "ATT",
                "TCL",
                "ODC",
                "CHIUSO",
                "TIP",
                10.0,
                "R",
                "N",
                "P",
                "F",
            )
        ]
        # Giornaliere mapping: data(0), personale(1), tcl(2), descrizione(3), n_prev(4), odc(5), pdl(6), inizio(7), fine(8), ore(9), nome_file(10)
        mock_giornaliere = [("2024-01-01", "P1", "T", "D", "PREV-001", "ODC", "P", "08", "17", 8.0, "F")]

        with (
            patch("src.core.contabilita_queries.ContabilitaQueries.get_data_by_year", return_value=mock_oda),
            patch(
                "src.core.contabilita_queries.ContabilitaQueries.get_giornaliere_by_year",
                return_value=mock_giornaliere,
            ),
        ):
            stats = manager.get_year_stats(2024)

            assert stats["total_prev"] == 1000.0  # noqa: PLR2004
            assert stats["total_ore"] == 10.0  # noqa: PLR2004
            assert stats["status_counts"]["CHIUSO"] == 1
            assert stats["ore_dirette"] == 8.0  # noqa: PLR2004
            assert stats["ore_indirette"] == 0.0

    def test_import_giornaliere(self, manager, tmp_path):  # noqa: ANN001
        g_dir = tmp_path / "Giornaliere 2024"
        g_dir.mkdir()
        with (
            patch(
                "src.core.contabilita_manager.ExcelImporter.import_giornaliere",
                return_value=(True, "OK", [], [2024]),
            ),
            patch("src.core.contabilita_manager.DataSynchronizer.sync_giornaliere", return_value=(1, 0)),
            patch("src.core.database.db_manager.get_connection"),
        ):
            success, _msg, added, _removed = manager.import_giornaliere(str(tmp_path))
            assert success is True
            assert added == 1

    def test_scan_workload(self, manager):  # noqa: ANN001
        with patch("src.core.contabilita_manager.ExcelImporter.scan_workload", return_value=(10, 5)):
            rows, files = manager.scan_workload("fake.xlsx", "fake_dir")
            assert rows == 10  # noqa: PLR2004
            assert files == 5  # noqa: PLR2004

    def test_scan_scarico_ore_rows(self, manager):  # noqa: ANN001
        with patch("src.core.contabilita_manager.ExcelImporter.scan_scarico_ore_rows", return_value=100):
            rows = manager.scan_scarico_ore_rows("fake.xlsx")
            assert rows == 100  # noqa: PLR2004
