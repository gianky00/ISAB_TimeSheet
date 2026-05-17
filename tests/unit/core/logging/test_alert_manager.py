import pytest
from unittest.mock import MagicMock, patch
from src.core.logging.alert_manager import AlertManager, AlertConfig
from src.core.logging.analytics import Anomaly
from datetime import datetime

class TestAlertManager:
    @pytest.fixture
    def manager(self):
        return AlertManager(config=AlertConfig(enabled=True, min_severity="medium"))

    def test_alert_manager_singleton(self):
        instance1 = AlertManager.instance()
        instance2 = AlertManager.instance()
        assert instance1 is instance2

    def test_should_alert_severity_filter(self, manager):
        low_anomaly = Anomaly(type="unusual_pattern", severity="low", message="test")
        med_anomaly = Anomaly(type="unusual_pattern", severity="medium", message="test")
        
        assert manager._should_alert(low_anomaly) is False
        assert manager._should_alert(med_anomaly) is True

    @patch("src.core.logging.alert_manager.datetime")
    def test_should_alert_cooldown(self, mock_datetime, manager):
        # Mocking time
        now = datetime(2026, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = now
        
        anomaly = Anomaly(type="error_spike", severity="high", message="test")
        
        # Primo alert: deve inviare
        assert manager._should_alert(anomaly) is True
        manager._record_alert(anomaly)
        
        # Secondo alert (subito dopo): deve bloccare (cooldown 30min)
        assert manager._should_alert(anomaly) is False
        
        # Sposta avanti il tempo di 31 min
        mock_datetime.now.return_value = datetime(2026, 1, 1, 12, 31, 0)
        assert manager._should_alert(anomaly) is True

    def test_send_alert_manual(self, manager):
        # Mock telegram service
        mock_tg = MagicMock()
        manager._telegram_service = mock_tg
        
        success = manager.send_alert("Test Title", "Test Message", level="warning")
        
        assert success is True
        mock_tg.send_message_sync.assert_called_once()
        assert "⚠️" in mock_tg.send_message_sync.call_args[0][0]
