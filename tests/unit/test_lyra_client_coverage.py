
import sqlite3
import requests
from unittest.mock import MagicMock

import pytest

from src.core.lyra_client import LyraClient


class TestLyraClientCoverage:
    @pytest.fixture
    def client(self, mocker):
        # Mock config_manager per evitare caricamento file reali
        mocker.patch("src.core.config_manager.load_config", return_value={"ai_model": "gemini-1.5-flash"})
        return LyraClient(api_key="fake_gemini_key")

    def test_get_system_context_assembly(self, client, mocker, tmp_path):
        """Verifica l'integrazione dei dati locali nel contesto AI."""
        # Mock ContabilitaManager
        mock_stats = {
            "total_prev": 10000.0,
            "total_ore": 100.0,
            "count_total": 5,
            "status_counts": {"COMPLETATO": 2},
            "top_commesse": [("Commessa A", 5000.0)]
        }
        mocker.patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024])
        mocker.patch("src.core.contabilita_manager.ContabilitaManager.get_year_stats", return_value=mock_stats)

        # Mock SQLite per Timbrature
        db_path = tmp_path / "timbrature_test.db"
        mocker.patch("src.core.lyra_client.CONFIG_DIR", tmp_path)
        (tmp_path / "data").mkdir()
        real_db_path = tmp_path / "data" / "timbrature_Isab.db"

        conn = sqlite3.connect(real_db_path)
        conn.execute("CREATE TABLE timbrature (data TEXT, nome TEXT, cognome TEXT, ingresso TEXT, uscita TEXT)")
        conn.execute("INSERT INTO timbrature VALUES ('2024-01-01', 'G', 'A', '08:00', '17:00')")
        conn.commit()
        conn.close()

        context = client._get_system_context()

        assert "REPORT CONTABILITÀ (2024)" in context
        assert "€ 10,000.00" in context
        assert "REPORT TIMBRATURE" in context
        assert "G A (08:00 -> 17:00)" in context

    def test_ask_with_image_payload(self, client, mocker):
        """Verifica la costruzione del payload multi-modale (testo + immagine)."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Risposta AI"}]}}],
            "usageMetadata": {"totalTokenCount": 100}
        }
        mocker.patch("requests.post", return_value=mock_resp)
        m_audit = mocker.patch("src.core.audit_manager.AuditManager.log_action")

        res = client.ask("Analizza questa foto", images=["base64data"])

        assert res == "Risposta AI"
        # Verifica payload inviato a requests
        args = requests.post.call_args[1]
        payload = args["json"]
        parts = payload["contents"][0]["parts"]
        assert len(parts) == 2 # Testo + Immagine
        assert "inline_data" in parts[1]
        assert m_audit.called

    def test_list_models_success(self, client, mocker):
        """Verifica il recupero e filtraggio dei modelli Gemini."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "models": [
                {"name": "models/gemini-pro", "supportedGenerationMethods": ["generateContent"]},
                {"name": "models/embedding-001", "supportedGenerationMethods": ["embedContent"]}
            ]
        }
        mocker.patch("requests.get", return_value=mock_resp)

        models = client.list_models()
        assert "gemini-pro" in models
        assert "embedding-001" not in models

    def test_analyze_media_audio(self, client, mocker):
        """Verifica l'invio di file audio per analisi NLU."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"candidates": [{"content": {"parts": [{"text": "Voglio scaricare PDL"}]}}]}
        mocker.patch("requests.post", return_value=mock_resp)

        res = client.analyze_media(b"fake_audio_bytes", "Converti in JSON", mime_type="audio/ogg")

        assert "Voglio scaricare" in res
        payload = requests.post.call_args[1]["json"]
        assert payload["contents"][0]["parts"][1]["inline_data"]["mime_type"] == "audio/ogg"
