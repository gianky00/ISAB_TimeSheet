from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.application.services.logging.sinks import AggregatedMetricsSink, BotLogSink, MetricsRotatingSink


class TestSinks:
    @pytest.fixture
    def mock_config(self, fs):
        m = MagicMock()
        m.metrics_dir = Path("/logs/metrics")
        fs.create_dir("/logs/metrics")
        # get_bot_log_path mock
        m.get_bot_log_path.side_effect = lambda bt, tid: Path(f"/logs/bots/{bt}_{tid}.json")
        return m

    def test_bot_log_sink_write_and_read(self, mock_config, fs):
        sink = BotLogSink(config=mock_config)

        ctx = {"trace_id": "T1", "bot_type": "B1"}
        sink.write("INFO", "logger", "msg", ctx)

        log_path = Path("/logs/bots/B1_T1.json")
        assert log_path.exists()

        logs = sink.get_bot_run_logs("B1", "T1")
        assert len(logs) == 1
        assert logs[0]["message"] == "msg"

    def test_bot_log_sink_missing_context(self, mock_config, fs):
        sink = BotLogSink(config=mock_config)
        sink.write("INFO", "l", "m", {})  # Manca trace_id
        assert not fs.exists("/logs/bots")

    def test_metrics_rotating_sink_write(self, mock_config, fs):
        # Impostiamo max_size molto piccola per testare rotazione
        sink = MetricsRotatingSink(config=mock_config, max_size_mb=0.0001)  # ~100 bytes

        metric = {"val": "X" * 200}  # > 100 bytes
        sink.write(metric)
        assert sink.metrics_file.exists()

        # Secondo write deve scatenare rotazione
        sink.write(metric)
        # Dovrebbero esserci 2 file .jsonl (uno originale ruotato, uno nuovo)
        files = list(Path("/logs/metrics").glob("*.jsonl*"))
        assert len(files) >= 2

    def test_aggregated_metrics_sink(self, mock_config, fs):
        sink = AggregatedMetricsSink(config=mock_config)
        summary = {"errors": 5}
        sink.write_daily_summary("2023-05-23", summary)

        read_back = sink.read_daily_summary("2023-05-23")
        assert read_back == summary
        assert sink.read_daily_summary("unknown") is None

    def test_bot_log_sink_error_handling(self, mock_config, fs):
        sink = BotLogSink(config=mock_config)
        # Mocking open to fail
        with patch.object(Path, "open", side_effect=PermissionError("Locked")):
            # Non deve crashare
            sink.write("INFO", "l", "m", {"trace_id": "T", "bot_type": "B"})
            assert True
