from unittest.mock import MagicMock, patch

import pytest

from src.core.contabilita_stats import ContabilitaStats
from src.core.lyra_client import LyraClient


class TestSprintBIntelligence:
    @pytest.fixture
    def mock_db_path(self, tmp_path):
        return tmp_path / "test_data.db"

    @pytest.fixture
    def lyra(self, mocker):
        # Mock config per evitare caricamento file reali
        mocker.patch(
            "src.core.config_manager.load_config",
            return_value={"ai_model": "gemini-test"},
        )
        # Mock AuditManager per evitare scritture su DB reale
        mocker.patch("src.core.audit_manager.AuditManager.log_action")
        return LyraClient(api_key="fake_key")

    # --- CONTABILITA STATS TESTS ---

    def test_stats_kpi_logic(self, mocker, mock_db_path):
        """Verifica i calcoli dei KPI finanziari e delle ore."""
        # Dati finti (Tabella Dati)
        # Indici: 2: n_prev, 3: val_prev, 4: attivita, 7: status, 9: ore
        mock_data = [
            (
                1,
                2024,
                "P001",
                "€ 1.000,00",
                "Attivita A",
                "T1",
                "O1",
                "IN CORSO",
                "V",
                "10,0",
            ),
            (
                2,
                2024,
                "P002",
                "€ 2.000,00",
                "Attivita B",
                "T1",
                "O2",
                "CHIUSA",
                "V",
                "5,5",
            ),
            (
                3,
                2024,
                "TOTALE",
                "€ 3.000,00",
                "",
                "",
                "",
                "",
                "",
                "15,5",
            ),  # Da ignorare
        ]

        # Dati finti (Giornaliere)
        # Indici: 4: n_prev, 5: odc, 9: ore
        mock_giorn = [
            (1, 2024, "data", "p", "P001", "O1", "pdl", "i", "f", "8,0"),  # Diretta
            (2, 2024, "data", "p", "", "", "pdl", "i", "f", "2,0"),  # Indiretta
        ]

        mocker.patch(
            "src.core.contabilita_queries.ContabilitaQueries.get_data_by_year",
            return_value=mock_data,
        )
        mocker.patch(
            "src.core.contabilita_queries.ContabilitaQueries.get_giornaliere_by_year",
            return_value=mock_giorn,
        )

        stats = ContabilitaStats.get_year_stats(mock_db_path, 2024)

        assert stats["total_prev"] == 3000.0
        assert stats["total_ore"] == 15.5
        assert stats["count_total"] == 2
        assert stats["status_counts"]["IN CORSO"] == 1
        assert stats["ore_dirette"] == 8.0
        assert stats["ore_indirette"] == 2.0
        assert stats["top_commesse"][0][0] == "Attivita B"

    # --- LYRA CLIENT TESTS ---

    def test_lyra_system_context_assembly(self, lyra, mocker, tmp_path):
        """Verifica che Lyra aggreghi correttamente i dati locali per il prompt."""
        # Mock dei manager
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years",
            return_value=[2024],
        )
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_year_stats",
            return_value={
                "total_prev": 5000.0,
                "total_ore": 100.0,
                "count_total": 10,
                "status_counts": {"IN CORSO": 5},
                "top_commesse": [("Test", 1000.0)],
            },
        )
        mocker.patch("src.core.lyra_client.CONFIG_DIR", tmp_path)

        context = lyra._get_system_context()

        assert "=== REPORT CONTABILITÀ (2024) ===" in context
        assert "€ 5,000.00" in context
        assert "Ore Spese Totali: 100.0 h" in context
        # Margine stimato: 5000 - (100 * 30) = 2000
        assert "€ 2,000.00" in context

    def test_lyra_api_success_flow(self, lyra, mocker):
        """Verifica la gestione di una risposta positiva dall'API Gemini."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Risposta AI"}]}}],
            "usageMetadata": {"totalTokenCount": 100},
        }

        with patch("requests.post", return_value=mock_response):
            res = lyra.ask("Come va?")
            assert res == "Risposta AI"

    def test_lyra_api_error_handling(self, lyra, mocker):
        """Verifica che Lyra gestisca gli errori HTTP dell'API."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized API Key"

        with patch("requests.post", return_value=mock_response):
            res = lyra.ask("Test")
            assert "Errore API" in res
            assert "401" in res

    def test_lyra_media_analysis(self, lyra, mocker):
        """Verifica l'invio di dati multimediali."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"candidates": [{"content": {"parts": [{"text": "| SC | TS |"}]}}]}

        with patch("requests.post", return_value=mock_response):
            res = lyra.analyze_media(b"fake_image_bytes", prompt="Estrai tabella")
            assert "| SC | TS |" in res
