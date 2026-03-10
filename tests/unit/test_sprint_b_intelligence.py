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
        # Patch preventivo per evitare migrazioni o caricamenti reali
        mocker.patch("src.core.config_manager.load_config", return_value={"ai_model": "gemini-test"})
        mocker.patch("src.core.audit_manager.AuditManager.instance")
        return LyraClient(api_key="fake_key")

    def test_stats_kpi_logic(self, mocker, mock_db_path):
        """Verifica i calcoli dei KPI finanziari V9.0."""
        # 14 colonne mappate
        mock_oda = [
            ("2024-01-01", "GEN", "P001", 1000.0, "Att A", "T1", "O1", "IN CORSO", "T", 10.0, "R", "N", "P", "F"),
            ("2024-01-01", "GEN", "P002", 2000.0, "Att B", "T1", "O2", "CHIUSA", "T", 5.5, "R", "N", "P", "F"),
            # Riga totale da ignorare (status vuoto o nan)
            ("2024-01-01", "GEN", "TOTALE", 3000.0, "", "", "", "", "", 15.5, "", "", "", "")
        ]
        # 11 colonne giornaliere
        mock_giorn = [
            ("2024-01-01", "P1", "T", "D", "P001", "O1", "pdl", "08", "17", 8.0, "F"),
            ("2024-01-01", "P1", "T", "D", "", "", "pdl", "08", "17", 2.0, "F")
        ]

        mocker.patch("src.core.contabilita_queries.ContabilitaQueries.get_data_by_year", return_value=mock_oda)
        mocker.patch("src.core.contabilita_queries.ContabilitaQueries.get_giornaliere_by_year", return_value=mock_giorn)

        stats = ContabilitaStats.get_year_stats(mock_db_path, 2024)

        assert stats["total_prev"] == 3000.0
        assert stats["total_ore"] == 15.5
        assert stats["count_total"] == 2
        assert stats["status_counts"]["IN CORSO"] == 1
        assert stats["ore_dirette"] == 8.0
        assert stats["ore_indirette"] == 2.0

    def test_lyra_system_context_assembly(self, lyra, mocker, tmp_path):
        """Verifica che Lyra aggreghi correttamente i dati locali per il prompt."""
        mocker.patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024])
        mocker.patch("src.core.contabilita_manager.ContabilitaManager.get_year_stats", return_value={
            "total_prev": 5000.0,
            "total_ore": 100.0,
            "count_total": 10,
            "status_counts": {"IN CORSO": 5},
            "top_commesse": [("Test", 1000.0)],
        })
        mocker.patch("src.core.lyra_client.CONFIG_DIR", tmp_path)

        context = lyra._get_system_context()

        assert "=== REPORT CONTABILITÀ (2024) ===" in context
        # Flessibilità su formattazione migliaia
        assert "5,000" in context or "5.000" in context
        assert "Ore Spese Totali: 100.0 h" in context

    def test_lyra_api_success_flow(self, lyra, mocker):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Risposta AI"}]}}],
            "usageMetadata": {"totalTokenCount": 100},
        }
        with patch("requests.post", return_value=mock_response):
            res = lyra.ask("Come va?")
            assert res == "Risposta AI"

    def test_lyra_media_analysis(self, lyra, mocker):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"candidates": [{"content": {"parts": [{"text": "Tabella"}]}}]}
        with patch("requests.post", return_value=mock_response):
            res = lyra.analyze_media(b"fake", prompt="Estrai")
            assert "Tabella" in res
