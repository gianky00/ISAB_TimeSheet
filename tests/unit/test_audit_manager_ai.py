"""
Tests for AuditManager integration with AI actions.
"""

import json
import sqlite3

import pytest

from src.core.audit.manager import AuditManager


class TestAuditManagerAI:
    @pytest.fixture
    def mock_db(self, tmp_path):
        db_path = tmp_path / "audit.db"
        # Inizializza schema minimo per far funzionare AuditDatabase
        return db_path

    def test_log_ai_consumption(self, mock_db, mocker):
        """Verifica che il consumo di token AI venga registrato correttamente."""
        # Setup AuditManager con un DB temporaneo specifico per il test
        manager = AuditManager.instance()
        manager.DB_PATH = mock_db
        # Re-inizializziamo il DB per usare il nuovo path
        manager.db._init_db()

        params = {"prompt": 100, "response": 200, "total": 300}

        manager.log_action(action="Consumo Token AI", category="lyra", entity="gemini:pro", params=params)

        # Verifica persistenza
        conn = sqlite3.connect(mock_db)
        cursor = conn.execute("SELECT action, category, entity, params FROM audit_logs WHERE category='lyra'")
        row = cursor.fetchone()
        conn.close()

        assert row is not None
        assert row[0] == "Consumo Token AI"
        assert row[1] == "lyra"
        assert row[2] == "gemini:pro"
        # I params vengono salvati come JSON string
        saved_params = json.loads(row[3])
        assert saved_params["total"] == 300

    def test_singleton_instance(self):
        """Verifica che AuditManager sia un vero Singleton."""
        inst1 = AuditManager.instance()
        inst2 = AuditManager.instance()
        assert inst1 is inst2
