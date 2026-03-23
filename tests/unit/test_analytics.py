"""
Test per il modulo analytics (AnomalyDetector e suggerimenti user-friendly).
"""

from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import pytest


@dataclass
class MockHealthReport:
    """Mock per il report di health."""

    error_rate_percent: float = 5.0
    level_distribution: dict = None
    bot_runs: dict = None
    operations: list = None

    def __post_init__(self):
        if self.level_distribution is None:
            self.level_distribution = {"ERROR": 10, "WARNING": 20, "INFO": 100}
        if self.bot_runs is None:
            self.bot_runs = {}
        if self.operations is None:
            self.operations = []

    def get(self, key, default=None):
        return getattr(self, key, default)


class TestAnomalyDetector:
    """Test per AnomalyDetector."""

    def test_detector_initialization(self):
        """Testa l'inizializzazione del detector."""
        from src.core.logging.analytics import AnomalyDetector  # noqa: PLC0415

        detector = AnomalyDetector()

        assert detector.error_rate_threshold == 5.0
        assert detector.slow_op_threshold_ms == 10000

    @patch("src.core.logging.analytics.LogViewer")
    def test_detect_error_rate_spike_user_friendly_suggestion(self, mock_viewer):
        """Testa che i suggerimenti siano user-friendly (no CLI commands)."""
        from src.core.logging.analytics import AnomalyDetector  # noqa: PLC0415

        # Mock viewer con error rate alto
        mock_instance = MagicMock()
        mock_instance.generate_health_report.return_value = {
            "error_rate_percent": 20.0,
            "level_distribution": {"ERROR": 50},
        }
        mock_viewer.return_value = mock_instance

        detector = AnomalyDetector()
        anomalies = detector.detect_error_rate_spike()

        assert len(anomalies) > 0

        # Verifica che il suggerimento NON contenga comandi CLI
        for anomaly in anomalies:
            assert "python" not in anomaly.suggestion.lower()
            assert "logs_cli" not in anomaly.suggestion.lower()
            # Verifica che sia user-friendly
            assert "Audit" in anomaly.suggestion or "sezione" in anomaly.suggestion.lower()

    @patch("src.core.logging.analytics.LogViewer")
    def test_detect_slow_operations_user_friendly_suggestion(self, mock_viewer):
        """Testa i suggerimenti per operazioni lente."""
        from src.core.logging.analytics import AnomalyDetector  # noqa: PLC0415

        mock_instance = MagicMock()
        mock_instance.generate_health_report.return_value = {
            "error_rate_percent": 0,
            "level_distribution": {},
        }
        # Mock query_slow_operations se esiste
        mock_instance.query_slow_operations.return_value = [{"operation": "login", "duration_ms": 15000}]
        mock_viewer.return_value = mock_instance

        detector = AnomalyDetector()

        # Il metodo potrebbe non esistere, skip se non presente
        if not hasattr(detector, "detect_slow_operations"):
            pytest.skip("detect_slow_operations non implementato")

        anomalies = detector.detect_slow_operations()

        # Se ci sono anomalie, verifica suggerimento
        for anomaly in anomalies:
            # Verifica suggerimento user-friendly (no CLI)
            assert "python" not in anomaly.suggestion.lower()

    @patch("src.core.logging.analytics.LogViewer")
    def test_detect_bot_failures_user_friendly_suggestion(self, mock_viewer):
        """Testa i suggerimenti per fallimenti bot."""
        from src.core.logging.analytics import AnomalyDetector  # noqa: PLC0415

        mock_instance = MagicMock()
        mock_instance.generate_health_report.return_value = {
            "error_rate_percent": 0,
            "level_distribution": {},
            "bot_runs": {
                "scarico_ts": {
                    "total_runs": 10,
                    "failed_runs": 8,
                }
            },
        }
        mock_viewer.return_value = mock_instance

        detector = AnomalyDetector()

        # Il metodo potrebbe non esistere, skip se non presente
        if not hasattr(detector, "detect_bot_failures"):
            pytest.skip("detect_bot_failures non implementato")

        anomalies = detector.detect_bot_failures()

        # Se ci sono anomalie, verifica suggerimento
        for anomaly in anomalies:
            # Verifica suggerimento user-friendly (no CLI)
            assert "python" not in anomaly.suggestion.lower()


class TestAnalyticsReport:
    """Test per la generazione del report analytics."""

    @patch("src.core.logging.analytics.LogViewer")
    @patch("src.core.logging.analytics.AnomalyDetector")
    def test_generate_analytics_report(self, mock_detector, mock_viewer):
        """Testa la generazione del report."""
        from src.core.logging.analytics import generate_analytics_report  # noqa: PLC0415

        # Mock viewer
        mock_viewer_instance = MagicMock()
        mock_viewer_instance.generate_health_report.return_value = {
            "error_rate_percent": 2.0,
            "level_distribution": {"ERROR": 5, "WARNING": 10, "INFO": 100},
            "bot_runs": {"test_bot": {"total_runs": 10, "failed_runs": 0}},
        }
        mock_viewer.return_value = mock_viewer_instance

        # Mock detector
        mock_detector_instance = MagicMock()
        mock_detector_instance.detect_all.return_value = []
        mock_detector.return_value = mock_detector_instance

        report = generate_analytics_report(hours=24)

        assert report is not None
        assert hasattr(report, "health_score")
        assert hasattr(report, "anomalies")

    def test_anomaly_dataclass(self):
        """Testa la dataclass Anomaly."""
        from src.core.logging.analytics import Anomaly  # noqa: PLC0415

        anomaly = Anomaly(
            type="test_type",
            severity="medium",
            message="Test message",
            suggestion="Test suggestion",
            details={"key": "value"},
        )

        assert anomaly.type == "test_type"
        assert anomaly.severity == "medium"
        assert anomaly.message == "Test message"
        assert anomaly.suggestion == "Test suggestion"
        assert anomaly.details == {"key": "value"}
