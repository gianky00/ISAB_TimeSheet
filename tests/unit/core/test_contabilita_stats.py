from pathlib import Path
from unittest.mock import patch

from src.core.contabilita_stats import ContabilitaStats


class TestContabilitaStats:
    @patch("src.core.contabilita_queries.ContabilitaQueries.get_data_by_year")
    @patch("src.core.contabilita_queries.ContabilitaQueries.get_giornaliere_by_year")
    def test_get_year_stats_full_logic(self, mock_giorn, mock_data):  # noqa: ANN001
        """Verifica il calcolo aggregato di tutte le statistiche annuali."""
        # Setup Dati OdA
        # row format: [?, ?, n_prev, v_prev, attivita, ?, ?, status, ?, v_ore, ...]
        mock_data.return_value = [
            (None, None, "P1", "1.000,00", "Lavoro A", None, None, "CONTABILIZZATA", None, "10"),
            (None, None, "P2", "500", "Lavoro B", None, None, "DA COMPLETARE", None, "5"),
            (None, None, "TOTALE", "1500", "Ignora", None, None, "", None, "15"),  # Riga da saltare
        ]

        # Setup Giornaliere
        # row format: [?, ?, ?, ?, n_prev, odc, ?, ?, ?, ore, ...]
        mock_giorn.return_value = [
            (None, None, None, None, "P1", "ODC1", None, None, None, "8"),  # Diretta
            (None, None, None, None, "", "", None, None, None, "4"),  # Indiretta
        ]

        stats = ContabilitaStats.get_year_stats(Path("fake.db"), 2025)

        # Verifiche OdA
        assert stats["total_prev"] == 1500.0  # noqa: PLR2004
        assert stats["total_ore"] == 15.0  # noqa: PLR2004
        assert stats["count_total"] == 2  # noqa: PLR2004
        assert stats["status_counts"]["CONTABILIZZATA"] == 1

        # Verifiche Ore Dirette/Indirette
        assert stats["ore_dirette"] == 8.0  # noqa: PLR2004
        assert stats["ore_indirette"] == 4.0  # noqa: PLR2004

        # Verifiche Top Commesse
        assert len(stats["top_commesse"]) == 2  # noqa: PLR2004
        assert stats["top_commesse"][0] == ("Lavoro A", 1000.0)

    def test_process_main_data_empty(self):
        stats = {"total_prev": 0.0, "total_ore": 0.0, "count_total": 0, "status_counts": {}}
        commesse = ContabilitaStats._process_main_data([], stats)
        assert commesse == []
        assert stats["total_prev"] == 0.0
