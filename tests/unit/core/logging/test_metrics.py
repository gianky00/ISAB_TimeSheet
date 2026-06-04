from pathlib import Path
from unittest.mock import MagicMock, patch

from src.application.services.logging.metrics import MetricsSink, PerformanceMetric, PerformanceTracker


class TestMetrics:
    def test_performance_metric_to_dict(self):
        m = PerformanceMetric("op1", 123.456, {"meta": "data"})
        d = m.to_dict()
        assert d["operation"] == "op1"
        assert d["duration_ms"] == 123.46  # arrotondato
        assert d["metadata"] == {"meta": "data"}
        # isoformat() include l'offset +00:00 o Z a seconda della versione,
        # ma non deve esserci un Z extra concatenato male.
        assert "T" in d["timestamp"]

    def test_metrics_sink_write_read(self, fs):
        mock_config = MagicMock()
        mock_config.metrics_dir = Path("/metrics_test")
        fs.create_dir("/metrics_test")

        sink = MetricsSink(config=mock_config)
        m1 = PerformanceMetric("op1", 10.0)
        m2 = PerformanceMetric("op2", 20.0)

        sink.write_metric(m1)
        sink.write_metric(m2)

        assert sink.metrics_file.exists()

        all_m = sink.read_metrics()
        assert len(all_m) == 2
        assert all_m[0].operation == "op1"

        op2_m = sink.read_metrics(operation="op2")
        assert len(op2_m) == 1
        assert op2_m[0].operation == "op2"

    def test_performance_tracker_singleton(self):
        PerformanceTracker._instance = None
        t1 = PerformanceTracker.instance()
        t2 = PerformanceTracker.instance()
        assert t1 is t2

    @patch("src.application.services.logging.metrics.MetricsSink.write_metric")
    def test_tracker_track_and_stats(self, mock_write):
        tracker = PerformanceTracker()
        tracker._in_memory_metrics.clear()

        tracker.track("op", 100)
        tracker.track("op", 200)
        tracker.track("op", 300)

        assert mock_write.called

        stats = tracker.get_statistics("op")
        assert stats["count"] == 3
        assert stats["avg"] == 200

    def test_tracker_baseline(self):
        tracker = PerformanceTracker()
        tracker.set_baseline("op", 500)
        assert tracker.get_baseline("op") == 500

    def test_metrics_sink_no_file(self, fs):
        mock_config = MagicMock()
        mock_config.metrics_dir = Path("/empty_metrics")
        fs.create_dir("/empty_metrics")
        sink = MetricsSink(config=mock_config)
        assert sink.read_metrics() == []
