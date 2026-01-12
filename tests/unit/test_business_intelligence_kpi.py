
from pathlib import Path

import pytest

from src.core.contabilita_stats import ContabilitaStats


class TestBusinessIntelligenceKPI:

    @pytest.fixture
    def mock_queries(self, mocker):
        """Mock per ContabilitaQueries."""
        return mocker.patch("src.core.contabilita_stats.ContabilitaQueries")

    def test_get_year_stats_calculation(self, mock_queries):
        """Test: Calcolo corretto delle statistiche annuali con dati misti."""
        # Setup dati finti per Contabilita (Tabella Dati)
        # row[2]=n_prev, row[3]=totale_prev, row[4]=attivita, row[7]=stato_attivita, row[9]=ore_sp
        mock_data = [
            (1, 2026, "P001", "1.000,00 €", "Manutenzione A", "cat", "ent", "APERTO", "tip", "10", "100%", "note", "file"),
            (2, 2026, "P002", "2.500,50 €", "Installazione B", "cat", "ent", "CHIUSO", "tip", "20", "80%", "note", "file"),
            (3, 2026, "", "500,00 €", "Invalid", "cat", "ent", "OPEN", "tip", "5", "50%", "note", "file"), # n_prev vuoto, ignorato
            (4, 2026, "TOTALE", "999.000,00 €", "Totale", "cat", "ent", "DONE", "tip", "0", "0%", "note", "file"), # n_prev contiene 'totale', ignorato
        ]
        mock_queries.get_data_by_year.return_value = mock_data

        # Setup dati finti per Giornaliere
        # row[4]=n_prev, row[5]=odc, row[9]=ore
        mock_giornaliere = [
            ("data", "pers", "tcl", "desc", "P001", "ODC1", "pdl", "08:00", "12:00", "4", "file"), # Diretta (n_prev presente)
            ("data", "pers", "tcl", "desc", "", "ODC2", "pdl", "13:00", "17:00", "4", "file"),    # Diretta (odc presente)
            ("data", "pers", "tcl", "desc", "", "", "pdl", "08:00", "09:00", "1", "file"),        # Indiretta (niente n_prev/odc)
        ]
        mock_queries.get_giornaliere_by_year.return_value = mock_giornaliere

        stats = ContabilitaStats.get_year_stats(Path("fake.db"), 2026)

        # Verifiche Dati Contabilità
        assert stats["count_total"] == 2 # Solo P001 e P002
        assert stats["total_prev"] == 3500.50 # 1000 + 2500.50
        assert stats["total_ore"] == 30.0 # 10 + 20
        assert stats["status_counts"]["APERTO"] == 1
        assert stats["status_counts"]["CHIUSO"] == 1

        # Verifiche Top Commesse
        assert len(stats["top_commesse"]) == 2
        assert stats["top_commesse"][0][0] == "Installazione B"
        assert stats["top_commesse"][0][1] == 2500.50

        # Verifiche Ore Dirette/Indirette
        assert stats["ore_dirette"] == 8.0 # 4 + 4
        assert stats["ore_indirette"] == 1.0 # 1

    def test_get_year_stats_empty_data(self, mock_queries):
        """Test: Gestione graziosa di database vuoto o anno inesistente."""
        mock_queries.get_data_by_year.return_value = []
        mock_queries.get_giornaliere_by_year.return_value = None

        stats = ContabilitaStats.get_year_stats(Path("empty.db"), 2025)

        assert stats["total_prev"] == 0.0
        assert stats["count_total"] == 0
        assert stats["status_counts"] == {}
        assert stats["ore_dirette"] == 0.0
        assert stats["ore_indirette"] == 0.0

    def test_get_year_stats_malformed_currency(self, mock_queries):
        """Test: Resilienza a valori monetari o ore malformati."""
        mock_data = [
            (1, 2026, "P999", "NON_UN_NUMERO", "Errore Test", "cat", "ent", "DEBUG", "tip", "XYZ", "0%", "note", "file"),
        ]
        mock_queries.get_data_by_year.return_value = mock_data
        mock_queries.get_giornaliere_by_year.return_value = []

        # Non deve crashare
        stats = ContabilitaStats.get_year_stats(Path("buggy.db"), 2026)

        # Se parse_currency fallisce, dovrebbe restituire 0.0 (in base all'implementazione di parse_currency)
        assert stats["total_prev"] == 0.0
        assert stats["total_ore"] == 0.0
        assert stats["count_total"] == 1
