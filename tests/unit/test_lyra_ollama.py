"""
Unit tests for LyraClient with Ollama provider.
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.core.lyra_client import LyraClient


class TestLyraOllama:
    @pytest.fixture
    def client(self):
        return LyraClient(provider="ollama", model_name="llama3", ollama_url="http://localhost:11434")

    def test_list_models_ollama(self, client):
        """Verifica il recupero della lista modelli da Ollama."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": [{"name": "llama3:latest"}, {"name": "mistral:latest"}]}

        with patch("requests.get", return_value=mock_response):
            models = client.list_models()
            assert "llama3:latest" in models
            assert "mistral:latest" in models

    def test_ask_ollama_success(self, client):
        """Verifica una richiesta di chat andata a buon fine su Ollama."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": "Risposta da Ollama"}}

        with (
            patch("requests.post", return_value=mock_response) as mock_post,
            patch.object(client, "_get_system_context", return_value="Sistema OK"),
        ):
            answer = client.ask("Ciao")
            assert answer == "Risposta da Ollama"

            # Verifica payload inviato
            _args, kwargs = mock_post.call_args
            payload = kwargs["json"]
            assert payload["model"] == "llama3"
            assert any(m["role"] == "user" and m["content"] == "Ciao" for m in payload["messages"])

    def test_ask_ollama_connection_error(self, client):
        """Verifica la gestione di errore di connessione a Ollama."""
        with (
            patch("requests.post", side_effect=requests.exceptions.ConnectionError),
            patch.object(client, "_get_system_context", return_value="Ctx"),
        ):
            answer = client.ask("Test")
            assert "Impossibile connettersi a Ollama" in answer

    def test_ask_ollama_http_error(self, client):
        """Verifica la gestione di un errore HTTP restituito da Ollama."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.json.return_value = {"error": "Modello non caricato"}

        with (
            patch("requests.post", return_value=mock_response),
            patch.object(client, "_get_system_context", return_value="Ctx"),
        ):
            answer = client.ask("Test")
            assert "Errore Ollama (Status 500)" in answer
            assert "Modello non caricato" in answer

    def test_analyze_media_ollama(self, client):
        """Verifica l'invio di immagini a Ollama."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": "Vedo un gatto"}}

        with (
            patch("requests.post", return_value=mock_response) as mock_post,
            patch.object(client, "_get_system_context", return_value="Ctx"),
        ):
            answer = client.analyze_media(b"fakebytes", "Cosa vedi?")
            assert answer == "Vedo gatto" or "Vedo un gatto" in answer

            # Verifica che le immagini siano state incluse nel payload
            _args, kwargs = mock_post.call_args
            payload = kwargs["json"]
            assert "images" in payload["messages"][-1]
            assert len(payload["messages"][-1]["images"]) == 1
