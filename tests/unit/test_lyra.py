import os
import sys
from unittest.mock import MagicMock, patch

# Path hack
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from src.core.lyra_client import LyraClient


class TestLyra:
    @patch("requests.post")
    def test_ask_model_version(self, mock_post):
        """Verify Lyra uses the correct model version."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"candidates": [{"content": {"parts": [{"text": "Risposta AI"}]}}]}
        mock_post.return_value = mock_response

        # Specifichiamo un modello esplicito
        client = LyraClient(api_key="dummy_key", model_name="test-model-123")

        # Verify context injection
        with patch.object(client, "_get_system_context", return_value="SystemContext"):
            resp = client.ask("Domanda", extra_context="RowData: 123")
            assert resp == "Risposta AI"

            # Verify URL contains the requested model
            args, kwargs = mock_post.call_args
            assert "test-model-123" in args[0]

            # Verify payload contains extra context
            payload = kwargs["json"]
            text_sent = payload["contents"][0]["parts"][0]["text"]
            assert "RowData: 123" in text_sent

    @patch("requests.post")
    def test_no_fallback_logic(self, mock_post):
        """Verify Lyra does NOT fall back anymore and reports error directly."""
        fail_response = MagicMock()
        fail_response.status_code = 429
        fail_response.text = "Quota Exceeded"
        mock_post.return_value = fail_response

        client = LyraClient(api_key="dummy_key", model_name="gemini-1.5-pro")

        with patch.object(client, "_get_system_context", return_value="Ctx"):
            resp = client.ask("Domanda")

            # Deve fallire subito e riportare l'errore completo
            assert "Errore API gemini-1.5-pro (Status 429)" in resp
            assert "Quota Exceeded" in resp
            assert mock_post.call_count == 1
