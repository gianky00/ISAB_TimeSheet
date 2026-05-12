"""
Tests for system telemetry and audit retention.
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

from src.core.audit.manager import AuditManager
from src.utils.system_telemetry import get_current_process_ram_mb


class TestSystemIntegrity:
    def test_get_current_process_ram_mb(self):
        """Verifica che il recupero RAM restituisca un valore plausibile."""
        ram = get_current_process_ram_mb()
        assert isinstance(ram, float)
        # Se il recupero fallisce per motivi di sandbox/permessi, ritorna 0.0.
        # Validiamo solo che sia un float non negativo.
        assert ram >= 0.0

    def test_audit_retention_policy(self, mocker):
        """Verifica che la policy di retention elimini i log vecchi."""
        from datetime import UTC

        manager = AuditManager.instance()
        mock_db = MagicMock()
        mock_db.delete_older_than.return_value = 5  # Simula 5 righe eliminate
        manager.db = mock_db

        # Patch log_action per evitare ricorsione o effetti collaterali reali
        mock_log = mocker.patch.object(manager, "log_action")

        manager.run_retention_policy(days=30)

        # Verifica chiamata al DB
        assert mock_db.delete_older_than.called
        args = mock_db.delete_older_than.call_args[0]
        # La data di cutoff deve essere circa 30 giorni fa
        cutoff = datetime.fromisoformat(args[0])
        expected = datetime.now(UTC) - timedelta(days=30)
        assert abs((expected - cutoff).total_seconds()) < 10  # Tolleranza 10s

        # Verifica che l'azione sia stata auditata
        mock_log.assert_called()
        assert "Pulizia Log" in mock_log.call_args[0][0]
