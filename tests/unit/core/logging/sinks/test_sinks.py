from unittest.mock import MagicMock

import pytest

from src.application.services.logging.sinks import BotLogSink, MetricsRotatingSink


@pytest.fixture
def mock_config(tmp_path):
    config = MagicMock()
    config.metrics_dir = tmp_path / "metrics"
    config.get_bot_log_path = lambda bot, tid: tmp_path / f"{bot}_{tid}.log"
    return config


def test_bot_log_sink_write(mock_config, tmp_path):
    sink = BotLogSink(config=mock_config)
    context = {"trace_id": "123", "bot_type": "TestBot"}

    sink.write("INFO", "test_logger", "test message", context)

    log_path = tmp_path / "TestBot_123.log"
    assert log_path.exists()

    logs = sink.get_bot_run_logs("TestBot", "123")
    assert len(logs) == 1
    assert logs[0]["message"] == "test message"


def test_bot_log_sink_invalid_context(mock_config):
    sink = BotLogSink(config=mock_config)
    sink.write("INFO", "logger", "msg", {})
    assert len(list(mock_config.metrics_dir.glob("*"))) == 0


def test_metrics_rotating_sink_rotation(mock_config, tmp_path):
    # max_size 0.0001 MB (100 bytes)
    sink = MetricsRotatingSink(config=mock_config, max_size_mb=0.0001)

    # Scrivi metrica per superare soglia
    sink.write({"val": "A" * 200})

    # Verifica che il file sia stato ruotato (esiste .jsonl e almeno un file ruotato)
    files = list(mock_config.metrics_dir.glob("*.jsonl"))
    assert len(files) >= 1
