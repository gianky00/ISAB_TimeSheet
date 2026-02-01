from unittest.mock import MagicMock, patch

from src.core.contabilita_stats import ContabilitaStats


class TestContabilitaStats:
    @patch("src.core.contabilita_stats.ContabilitaQueries.get_giornaliere_by_year")
    @patch("src.core.contabilita_stats.ContabilitaQueries.get_data_by_year")
    def test_get_year_stats_basic(self, mock_data, mock_giorn):
        mock_data.return_value = [
            # year, col1, n_prev, v_prev, attivita, col5, col6, status, col8, v_ore
            (
                2024,
                None,
                "ODA001",
                "1000.00",
                "Manutenzione",
                None,
                None,
                "APERTO",
                None,
                "50.0",
            ),
            (
                2024,
                None,
                "ODA002",
                "2500.50",
                "Ispezione",
                None,
                None,
                "CHIUSO",
                None,
                "100.5",
            ),
        ]
        mock_giorn.return_value = []

        stats = ContabilitaStats.get_year_stats(MagicMock(), 2024)

        assert stats["count_total"] == 2
        assert stats["total_prev"] == 3500.50
        assert stats["total_ore"] == 150.5
        assert stats["status_counts"]["APERTO"] == 1
        assert stats["status_counts"]["CHIUSO"] == 1

    @patch("src.core.contabilita_stats.ContabilitaQueries.get_giornaliere_by_year")
    @patch("src.core.contabilita_stats.ContabilitaQueries.get_data_by_year")
    def test_get_year_stats_top_commesse(self, mock_data, mock_giorn):
        mock_data.return_value = [
            (
                2024,
                None,
                "ODA001",
                "5000.00",
                "Big Project",
                None,
                None,
                "APERTO",
                None,
                "0",
            ),
            (
                2024,
                None,
                "ODA002",
                "1000.00",
                "Small Task",
                None,
                None,
                "APERTO",
                None,
                "0",
            ),
            (
                2024,
                None,
                "ODA003",
                "3000.00",
                "Medium Work",
                None,
                None,
                "APERTO",
                None,
                "0",
            ),
        ]
        mock_giorn.return_value = []

        stats = ContabilitaStats.get_year_stats(MagicMock(), 2024)

        # Top commesse should be sorted by value (descending)
        assert len(stats["top_commesse"]) == 3
        assert stats["top_commesse"][0][0] == "Big Project"
        assert stats["top_commesse"][0][1] == 5000.0

    @patch("src.core.contabilita_stats.ContabilitaQueries.get_giornaliere_by_year")
    @patch("src.core.contabilita_stats.ContabilitaQueries.get_data_by_year")
    def test_get_year_stats_giornaliere_dirette_indirette(self, mock_data, mock_giorn):
        mock_data.return_value = []
        mock_giorn.return_value = [
            # data, col1, col2, col3, n_prev, odc, col6, col7, col8, ore
            (
                "2024-01-15",
                None,
                None,
                None,
                "ODA001",
                "ODC01",
                None,
                None,
                None,
                "8.0",
            ),  # Direct
            (
                "2024-01-16",
                None,
                None,
                None,
                "",
                "",
                None,
                None,
                None,
                "4.0",
            ),  # Indirect
            (
                "2024-01-17",
                None,
                None,
                None,
                "nan",
                "nan",
                None,
                None,
                None,
                "6.0",
            ),  # Indirect
        ]

        stats = ContabilitaStats.get_year_stats(MagicMock(), 2024)

        assert stats["ore_dirette"] == 8.0
        assert stats["ore_indirette"] == 10.0

    @patch("src.core.contabilita_stats.ContabilitaQueries.get_giornaliere_by_year")
    @patch("src.core.contabilita_stats.ContabilitaQueries.get_data_by_year")
    def test_get_year_stats_empty_data(self, mock_data, mock_giorn):
        mock_data.return_value = []
        mock_giorn.return_value = []

        stats = ContabilitaStats.get_year_stats(MagicMock(), 2024)

        assert stats["count_total"] == 0
        assert stats["total_prev"] == 0.0
        assert stats["top_commesse"] == []

    @patch("src.core.contabilita_stats.ContabilitaQueries.get_giornaliere_by_year")
    @patch("src.core.contabilita_stats.ContabilitaQueries.get_data_by_year")
    def test_skips_totale_rows(self, mock_data, mock_giorn):
        mock_data.return_value = [
            (
                2024,
                None,
                "ODA001",
                "1000.00",
                "Work",
                None,
                None,
                "APERTO",
                None,
                "10.0",
            ),
            (
                2024,
                None,
                "TOTALE ANNO",
                "5000.00",
                "Totale",
                None,
                None,
                "",
                None,
                "100.0",
            ),
        ]
        mock_giorn.return_value = []

        stats = ContabilitaStats.get_year_stats(MagicMock(), 2024)

        # TOTALE row should be skipped
        assert stats["count_total"] == 1
        assert stats["total_prev"] == 1000.0
