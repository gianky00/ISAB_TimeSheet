import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Path hack
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))

from src.core.lyra_client import LyraClient

class TestLyra:
    @patch('requests.post')
    def test_ask_model_version(self, mock_post):
        """Verify Lyra uses the correct model version."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'candidates': [{'content': {'parts': [{'text': 'Risposta AI'}]}}]
        }
        mock_post.return_value = mock_response

        client = LyraClient()

        # Verify URL contains flash model
        assert "gemini-1.5-flash" in client._url

        # Verify context injection
        with patch.object(client, '_get_system_context', return_value="SystemContext"):
            resp = client.ask("Domanda", extra_context="RowData: 123")
            assert resp == "Risposta AI"

            # Verify payload contains extra context
            args, kwargs = mock_post.call_args
            payload = kwargs['json']
            text_sent = payload['contents'][0]['parts'][0]['text']
            assert "RowData: 123" in text_sent
