from pathlib import Path
from unittest.mock import patch

from src.core.contabilita.stats_service import ContabilitaStats


class TestContabilitaStats:
    @patch("src.core.contabilita.stats_service.ContabilitaQueries")
    def test_get_year_stats_empty(self, mock_queries):
        mock_queries.get_data_by_year.return_value = []
        mock_queries.get_giornaliere_by_year.return_value = []

        stats = ContabilitaStats.get_year_stats(Path("fake.db"), 2024)

        assert stats["total_prev"] == 0.0
        assert stats["count_total"] == 0
        assert stats["top_commesse"] == []

    @patch("src.core.contabilita.stats_service.ContabilitaQueries")
    def test_get_year_stats_full_flow(self, mock_queries):
        # target columns for data: ..., n_prev (idx 2), v_prev (idx 3), attivita (idx 4), status (idx 7), v_ore (idx 9)
        mock_data = [
            (None, None, "P1", "1.000,00", "Lavoro A", None, None, "APERTO", None, "5,0"),
            (None, None, "P2", "2.000,00", "Lavoro B", None, None, "COMPLETATO", None, "10,0"),
        ]
        # target columns for giornaliere: ..., n_prev (idx 4), odc (idx 5), ore (idx 9)
        mock_giornaliere = [
            (None, None, None, None, "P1", "", None, None, None, "8,0"),  # Diretta
            (None, None, None, None, "", "", None, None, None, "2,0"),  # Indiretta
        ]

        mock_queries.get_data_by_year.return_value = mock_data
        mock_queries.get_giornaliere_by_year.return_value = mock_giornaliere

        stats = ContabilitaStats.get_year_stats(Path("fake.db"), 2024)

        assert stats["total_prev"] == 3000.0
        assert stats["total_ore"] == 15.0
        assert stats["count_total"] == 2
        assert stats["status_counts"]["APERTO"] == 1
        assert stats["ore_dirette"] == 8.0
        assert stats["ore_indirette"] == 2.0
        assert len(stats["top_commesse"]) == 2
        assert stats["top_commesse"][0][0] == "Lavoro B"

    def test_process_main_data_noise_filter(self):
        data = [
            (None, None, "Totale", "100", "X", None, None, "S", None, "0"),
            (None, None, "", "100", "X", None, None, "S", None, "0"),
        ]
        stats = {"total_prev": 0.0, "total_ore": 0.0, "count_total": 0, "status_counts": {}}
        res = ContabilitaStats._process_main_data(data, stats)
        assert len(res) == 0
        assert stats["count_total"] == 0
