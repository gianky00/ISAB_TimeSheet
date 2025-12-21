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

        # Verify context injection
        with patch.object(client, '_get_system_context', return_value="SystemContext"):
            resp = client.ask("Domanda", extra_context="RowData: 123")
            assert resp == "Risposta AI"

            # Verify URL contains flash model (First choice)
            args, kwargs = mock_post.call_args
            # The first argument to post is URL
            assert "gemini-2.0-flash" in args[0]

            # Verify payload contains extra context
            payload = kwargs['json']
            text_sent = payload['contents'][0]['parts'][0]['text']
            assert "RowData: 123" in text_sent

    @patch('requests.post')
    def test_ask_fallback_logic(self, mock_post):
        """Verify Lyra falls back to secondary model on 429."""
        # Mock responses: 1st call -> 429, 2nd call -> 200
        fail_response = MagicMock()
        fail_response.status_code = 429

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {
            'candidates': [{'content': {'parts': [{'text': 'Risposta Fallback'}]}}]
        }

        mock_post.side_effect = [fail_response, success_response]

        client = LyraClient()

        with patch.object(client, '_get_system_context', return_value="Ctx"):
            resp = client.ask("Domanda")

            assert resp == "Risposta Fallback"
            assert mock_post.call_count == 2

            # Verify first call was 2.0-flash
            args1, _ = mock_post.call_args_list[0]
            assert "gemini-2.0-flash" in args1[0]

            # Verify second call was 1.5-flash
            args2, _ = mock_post.call_args_list[1]
            assert "gemini-1.5-flash" in args2[0]
