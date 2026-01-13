
import sqlite3
from unittest.mock import MagicMock

import pytest

from src.core.lyra_client import LyraClient


class TestLyraClientAdvanced:

    @pytest.fixture
    def client(self, mocker):
        """Fixture per LyraClient con API key mockata."""
        mocker.patch("src.core.config_manager.load_config", return_value={"ai_model": "gemini-test"})
        return LyraClient(api_key="FAKE_KEY")

    def test_get_system_context_aggregation(self, client, mocker, tmp_path):
        """Test: Aggregazione dati da Contabilità e Timbrature per il contesto AI."""
        # 1. Mock Contabilità
        mock_mgr = mocker.patch("src.core.lyra_client.ContabilitaManager")
        mock_mgr.get_available_years.return_value = [2026]
        mock_mgr.get_year_stats.return_value = {
            "total_prev": 1000.0,
            "total_ore": 10.0,
            "count_total": 1,
            "status_counts": {"APERTO": 1},
            "top_commesse": [("Attività Test", 1000.0)]
        }

        # 2. Mock Timbrature (SQLite reale in tmp_path)
        db_dir = tmp_path / "data"
        db_dir.mkdir()
        db_path = db_dir / "timbrature_Isab.db"
        mocker.patch("src.core.lyra_client.CONFIG_DIR", tmp_path)

        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE timbrature (data TEXT, nome TEXT, cognome TEXT, ingresso TEXT, uscita TEXT)")
            conn.execute("INSERT INTO timbrature VALUES ('2026-01-01', 'Mario', 'Rossi', '08:00', '17:00')")

        context = client._get_system_context()

        assert "REPORT CONTABILITÀ (2026)" in context
        assert "€ 1,000.00" in context
        assert "REPORT TIMBRATURE" in context
        assert "Mario Rossi" in context

    def test_ask_payload_and_response_parsing(self, client, mocker):
        """Test: Verifica costruzione payload e parsing risposta Gemini."""
        mock_post = mocker.patch("src.core.lyra_client.requests.post")

        # Mock risposta API
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [{
                "content": {"parts": [{"text": "Risposta AI di test"}]}
            }],
            "usageMetadata": {"totalTokenCount": 100}
        }
        mock_post.return_value = mock_resp

        # Mock context e audit
        mocker.patch.object(client, "_get_system_context", return_value="System Context")
        mock_audit = mocker.patch("src.core.lyra_client.AuditManager")

        response = client.ask("Ciao Lyra", extra_context="Contesto Utente")

        assert response == "Risposta AI di test"
        # Verifica che il payload contenga i contesti
        args, kwargs = mock_post.call_args
        payload = kwargs["json"]
        prompt = payload["contents"][0]["parts"][0]["text"]
        assert "System Context" in prompt
        assert "Contesto Utente" in prompt
        assert "Ciao Lyra" in prompt
        # Verifica audit log
        mock_audit().log_action.assert_called()

    def test_ask_api_error_handling(self, client, mocker):
        """Test: Gestione errori HTTP dall'API Gemini."""
        mock_post = mocker.patch("src.core.lyra_client.requests.post")
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        mock_resp.text = "Invalid API Key"
        mock_post.return_value = mock_resp

        mocker.patch.object(client, "_get_system_context", return_value="")

        response = client.ask("Errore?")
        assert "Errore API" in response
        assert "403" in response

    def test_list_models_success(self, client, mocker):
        """Test: Recupero lista modelli compatibili."""
        mock_get = mocker.patch("src.core.lyra_client.requests.get")
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "models": [
                {"name": "models/gemini-1.5-pro", "supportedGenerationMethods": ["generateContent"]},
                {"name": "models/embedding-001", "supportedGenerationMethods": ["embedContent"]}
            ]
        }
        mock_get.return_value = mock_resp

        models = client.list_models()
        assert "gemini-1.5-pro" in models
        assert "embedding-001" not in models # Non supporta generateContent
