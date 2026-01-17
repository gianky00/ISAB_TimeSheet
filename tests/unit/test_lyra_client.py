"""
Tests for Lyra AI Client.
Mocks external API calls to Gemini and local DB interaction.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.core.lyra_client import LyraClient


@pytest.fixture
def mock_contabilita_manager():
    with patch("src.core.lyra_client.ContabilitaManager") as mock_cm:
        # Mock default return for available years
        mock_cm.get_available_years.return_value = [2025]
        # Mock default stats
        mock_cm.get_year_stats.return_value = {
            "total_prev": 100000.0,
            "total_ore": 1000.0,
            "count_total": 50,
            "status_counts": {"COMPLETED": 40, "WIP": 10},
            "top_commesse": [("Project A", 50000.0)],
        }
        yield mock_cm


@pytest.fixture
def mock_timbrature_db(tmp_path):
    with (
        patch("src.core.lyra_client.sqlite3") as mock_sqlite,
        patch("src.core.lyra_client.CONFIG_DIR", tmp_path),
    ):
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Setup cursor responses
        mock_cursor.fetchone.side_effect = [
            (100,),  # Total
            (5,),  # Anomalies (missing out)
        ]

        mock_cursor.fetchall.return_value = [("2025-01-01", "Mario", "Rossi", "08:00", "17:00")]

        yield tmp_path


def test_system_context_generation(mock_contabilita_manager, mock_timbrature_db):
    client = LyraClient(api_key="dummy_key")

    # Create the dummy file
    (mock_timbrature_db / "data").mkdir(parents=True, exist_ok=True)
    (mock_timbrature_db / "data" / "timbrature_Isab.db").touch()

    context = client._get_system_context()

    assert "REPORT CONTABILITÀ (2025)" in context
    assert "Valore Totale Preventivato: € 100,000.00" in context
    assert "REPORT TIMBRATURE" in context
    assert "Rilevate 5 timbrature con uscita mancante" in context


@patch("src.core.lyra_client.requests.post")
def test_ask_success(mock_post, mock_contabilita_manager):
    # Setup success response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"candidates": [{"content": {"parts": [{"text": "Risposta AI"}]}}]}
    mock_post.return_value = mock_response

    client = LyraClient(api_key="dummy_key")
    # Mock getting context to avoid FS ops
    with patch.object(client, "_get_system_context", return_value="[System Data]"):
        answer = client.ask("Ciao")

    assert answer == "Risposta AI"
    mock_post.assert_called_once()


@patch("src.core.lyra_client.requests.post")
def test_ask_no_retry_on_fail(mock_post, mock_contabilita_manager):
    # Setup fail sequence: 429
    r1 = MagicMock()
    r1.status_code = 429
    r1.text = "Quota Exceeded"
    mock_post.return_value = r1

    client = LyraClient(api_key="dummy_key", model_name="gemini-1.5-pro")
    with patch.object(client, "_get_system_context", return_value=""):
        answer = client.ask("Ciao")

    # Deve restituire errore e non riprovare
    assert "Errore API gemini-1.5-pro (Status 429)" in answer
    assert "Quota Exceeded" in answer
    assert mock_post.call_count == 1


@patch("src.core.lyra_client.requests.post")
def test_ask_all_fail_message(mock_post, mock_contabilita_manager):
    # All fail
    mock_fail = MagicMock()
    mock_fail.status_code = 500
    mock_fail.text = "Internal Server Error"
    mock_post.return_value = mock_fail

    client = LyraClient(api_key="dummy_key", model_name="gemini-1.5-pro")
    with patch.object(client, "_get_system_context", return_value=""):
        answer = client.ask("Ciao")

    assert "Errore API gemini-1.5-pro (Status 500)" in answer
    assert "Internal Server Error" in answer
