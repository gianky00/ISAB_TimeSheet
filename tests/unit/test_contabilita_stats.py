from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.contabilita_stats import ContabilitaStats


class TestContabilitaStats:
    @pytest.fixture
    def mock_data(self):
        # Sample data matching ExcelImporter.COLUMNS_MAPPING structure
        # Index 2: n_prev, 3: v_prev, 7: status, 9: v_ore, 4: attivita
        return [
            (
                1,
                "Comm1",
                "PREV001",
                "1.000,00",
                "Attivita A",
                "Desc",
                "Cantiere",
                "APERTO",
                "Data",
                "100,00",
            ),
            (
                2,
                "Comm2",
                "PREV002",
                "2.000,00",
                "Attivita B",
                "Desc",
                "Cantiere",
                "CHIUSO",
                "Data",
                "200,00",
            ),
            (
                3,
                "Comm3",
                "TOTALE",
                "3.000,00",
                "Skip me",
                "Desc",
                "Cantiere",
                "APERTO",
                "Data",
                "0",
            ),  # Should be skipped
        ]

    @pytest.fixture
    def mock_giornaliere(self):
        # Index 4: n_prev, 5: odc, 9: ore
        return [
            (
                "Data",
                "Pers",
                "TCL",
                "Desc",
                "PREV001",
                "ODC1",
                "PDL",
                "08:00",
                "17:00",
                "8,00",
                "file",
            ),  # Direct
            (
                "Data",
                "Pers",
                "TCL",
                "Desc",
                "",
                "",
                "PDL",
                "08:00",
                "12:00",
                "4,00",
                "file",
            ),  # Indirect
            (
                "Data",
                "Pers",
                "TCL",
                "Desc",
                "nan",
                "nan",
                "PDL",
                "08:00",
                "10:00",
                "2,00",
                "file",
            ),  # Indirect
        ]

    @patch("src.core.contabilita_stats.ContabilitaQueries")
    def test_get_year_stats(self, mock_queries, mock_data, mock_giornaliere):
        mock_queries.get_data_by_year.return_value = mock_data
        mock_queries.get_giornaliere_by_year.return_value = mock_giornaliere

        stats = ContabilitaStats.get_year_stats(Path("fake.db"), 2024)

        assert stats["total_prev"] == 3000.0  # 1000 + 2000
        assert stats["total_ore"] == 300.0  # 100 + 200
        assert stats["count_total"] == 2
        assert stats["status_counts"]["APERTO"] == 1
        assert stats["status_counts"]["CHIUSO"] == 1

        assert stats["ore_dirette"] == 8.0
        assert stats["ore_indirette"] == 6.0  # 4 + 2

        assert len(stats["top_commesse"]) == 2
        assert stats["top_commesse"][0][0] == "Attivita B"
        assert stats["top_commesse"][0][1] == 2000.0

    def test_process_main_data_empty(self):
        stats = {"total_prev": 0, "total_ore": 0, "count_total": 0, "status_counts": {}}
        commesse = ContabilitaStats._process_main_data([], stats)
        assert commesse == []
        assert stats["total_prev"] == 0

    def test_process_giornaliere_stats_empty(self):
        stats = {"ore_dirette": 0, "ore_indirette": 0}
        ContabilitaStats._process_giornaliere_stats([], stats)
        assert stats["ore_dirette"] == 0
        assert stats["ore_indirette"] == 0
