from unittest.mock import patch

import pytest

from src.core.lyra_client import LyraClient


class TestLyraClient:
    @pytest.fixture
    def client(self):
        with patch(
            "src.core.config_manager.load_config",
            return_value={"ai_model": "gemini-1.5-flash"},
        ):
            return LyraClient(api_key="test_api_key")

    def test_init_model_from_config(self, client):
        assert client.model == "gemini-1.5-flash"

    @patch("src.core.lyra_client.requests.get")
    def test_list_models(self, mock_get, client):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "models": [
                {
                    "name": "models/gemini-pro",
                    "supportedGenerationMethods": ["generateContent"],
                },
                {
                    "name": "models/embedding",
                    "supportedGenerationMethods": ["embedContent"],
                },
            ]
        }

        models = client.list_models()
        assert "gemini-pro" in models
        assert "embedding" not in models

    @patch("src.core.lyra_client.requests.post")
    @patch("src.core.lyra_client.LyraClient._get_system_context", return_value="CONTEXT")
    def test_ask_success(self, mock_ctx, mock_post, client):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Risposta AI"}]}}],
            "usageMetadata": {"promptTokenCount": 100, "candidatesTokenCount": 50},
        }

        response = client.ask("Qual è lo stato delle timbrature?")
        assert response == "Risposta AI"
        mock_post.assert_called_once()

    @patch("src.core.lyra_client.requests.post")
    def test_ask_api_error(self, mock_post, client):
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"

        response = client.ask("Test")
        assert "Errore API" in response
        assert "500" in response

    @patch("src.core.lyra_client.requests.post")
    def test_analyze_media(self, mock_post, client):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Analisi immagine"}]}}],
            "usageMetadata": {},
        }

        result = client.analyze_media(b"fake_image_bytes", "Descrivi l'immagine")
        assert result == "Analisi immagine"

    @patch(
        "src.core.lyra_client.ContabilitaManager.get_available_years",
        return_value=[2025, 2026],
    )
    @patch("src.core.lyra_client.ContabilitaManager.get_year_stats")
    def test_get_contabilita_context(self, mock_stats, mock_years, client):
        mock_stats.return_value = {
            "total_prev": 100000,
            "total_ore": 500,
            "count_total": 10,
            "status_counts": {"In corso": 5},
            "top_commesse": [("Commessa A", 50000)],
        }

        ctx = client._get_contabilita_context()
        assert "2026" in ctx
        assert "€ 100,000" in ctx or "100.000" in ctx
