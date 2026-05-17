from unittest.mock import MagicMock

import pytest

from src.core.logging.analytics import AnomalyDetector


class TestAnomalyDetector:
    @pytest.fixture
    def mock_viewer(self):
        return MagicMock()

    def test_detect_error_rate_spike_low(self, mock_viewer):
        detector = AnomalyDetector(viewer=mock_viewer)
        mock_viewer.generate_health_report.return_value = {"error_rate_percent": 2.0}

        anomalies = detector.detect_error_rate_spike()
        assert len(anomalies) == 0

    def test_detect_error_rate_spike_medium(self, mock_viewer):
        detector = AnomalyDetector(viewer=mock_viewer)
        mock_viewer.generate_health_report.return_value = {"error_rate_percent": 6.0}

        anomalies = detector.detect_error_rate_spike()
        assert len(anomalies) == 1
        assert anomalies[0].severity == "medium"
        assert anomalies[0].type == "error_spike"

    def test_detect_error_rate_spike_critical(self, mock_viewer):
        detector = AnomalyDetector(viewer=mock_viewer)
        mock_viewer.generate_health_report.return_value = {"error_rate_percent": 30.0}

        anomalies = detector.detect_error_rate_spike()
        assert len(anomalies) == 1
        assert anomalies[0].severity == "critical"

    def test_detect_slow_operations_high(self, mock_viewer):
        detector = AnomalyDetector(viewer=mock_viewer)
        mock_viewer.get_slow_operations.return_value = [
            {"duration_ms": 35000, "operation": "test_op"}
        ]

        anomalies = detector.detect_slow_operations()
        assert len(anomalies) == 1
        assert anomalies[0].severity == "high"
        assert anomalies[0].type == "slow_operation"
