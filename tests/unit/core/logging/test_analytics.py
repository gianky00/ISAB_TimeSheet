from unittest.mock import MagicMock, patch

import pytest

from src.core.logging.analytics import (
    Anomaly,
    AnomalyDetector,
    HealthScorer,
    PatternDetector,
    generate_analytics_report,
)


class TestAnalytics:
    @pytest.fixture
    def mock_viewer(self):
        viewer = MagicMock()
        viewer.generate_health_report.return_value = {
            "error_rate_percent": 2.0,
            "level_distribution": {"ERROR": 5},
            "bot_runs": {"success_rate_percent": 95},
        }
        viewer.get_slow_operations.return_value = []
        viewer.get_bot_runs_summary.return_value = []
        viewer.get_error_summary.return_value = []
        return viewer

    def test_anomaly_detector_no_anomalies(self, mock_viewer):
        detector = AnomalyDetector(mock_viewer)
        anomalies = detector.detect_all()
        assert len(anomalies) == 0

    def test_anomaly_detector_error_spike(self, mock_viewer):
        mock_viewer.generate_health_report.return_value["error_rate_percent"] = 20.0
        detector = AnomalyDetector(mock_viewer)
        anomalies = detector.detect_error_rate_spike()
        assert len(anomalies) == 1
        assert anomalies[0].type == "error_spike"
        assert anomalies[0].severity == "high"

    def test_anomaly_detector_slow_ops(self, mock_viewer):
        mock_viewer.get_slow_operations.return_value = [{"operation": "long_task", "duration_ms": 40000}]
        detector = AnomalyDetector(mock_viewer)
        anomalies = detector.detect_slow_operations()
        assert len(anomalies) == 1
        assert anomalies[0].type == "slow_operation"
        assert anomalies[0].severity == "high"

    def test_pattern_detector(self, mock_viewer):
        mock_viewer.get_error_summary.return_value = [{"message": "Repeat me", "count": 5}]
        detector = PatternDetector(mock_viewer)
        patterns = detector.detect_all()
        assert len(patterns) == 1
        assert patterns[0].count == 5
        assert "Repeat me" in patterns[0].message

    def test_health_scorer(self):
        scorer = HealthScorer()

        # Perfetto
        assert scorer.calculate(anomalies=[], error_rate=0, bot_success_rate=100) == 100

        # Una anomalia critica
        a = Anomaly(type="unusual_pattern", severity="critical", message="Crash")
        assert scorer.calculate(anomalies=[a], error_rate=0, bot_success_rate=100) == 75

        # Error rate elevato
        assert scorer.calculate(anomalies=[], error_rate=10, bot_success_rate=100) == 90

        # Bot failure: (100 - 80) / 2 = 10 -> 100 - 10 = 90
        assert scorer.calculate(anomalies=[], error_rate=0, bot_success_rate=80) == 90

    @patch("src.core.logging.analytics.LogViewer")
    def test_generate_analytics_report_integration(self, mock_viewer_class):
        mock_v = MagicMock()
        mock_viewer_class.return_value = mock_v
        mock_v.generate_health_report.return_value = {
            "error_rate_percent": 0,
            "bot_runs": {"success_rate_percent": 100},
        }
        mock_v.get_slow_operations.return_value = []
        mock_v.get_bot_runs_summary.return_value = []
        mock_v.get_error_summary.return_value = []

        report = generate_analytics_report()
        assert report.health_score == 100
        assert report.anomaly_count == 0
