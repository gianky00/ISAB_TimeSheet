import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.application.services.logging.viewer import LogQuery, LogViewer


class TestLogViewer:
    @pytest.fixture
    def log_file(self, fs):
        path = Path("/tmp/app.json")
        fs.create_file(str(path))
        return path

    def test_log_query_filters(self, log_file, fs):
        # Scrive alcuni log JSON
        logs = [
            {
                "level": "INFO",
                "message": "Starting bot",
                "timestamp": "2023-05-23T10:00:00Z",
                "context": {"bot_type": "test"},
            },
            {
                "level": "ERROR",
                "message": "Failed to login",
                "timestamp": "2023-05-23T10:05:00Z",
                "context": {"bot_type": "test"},
            },
            {
                "level": "INFO",
                "message": "Processing",
                "timestamp": "2023-05-23T10:10:00Z",
                "context": {"bot_type": "other"},
            },
        ]
        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(log) + "\n" for log in logs)

        query = LogQuery(log_file)

        # Filtro livello
        assert query.level("ERROR").count() == 1

        # Reset filters (LogQuery non è immutabile, ricreiamo per semplicità)
        query = LogQuery(log_file)
        assert query.contains_message("bot").count() == 1

        # Filtro contesto
        query = LogQuery(log_file)
        assert query.bot_type("test").count() == 2

        # Filtro tempo
        start = datetime(2023, 5, 23, 10, 2, 0, tzinfo=UTC)
        query = LogQuery(log_file).time_range(start=start)
        assert query.count() == 2

    def test_log_query_execute_limit_offset(self, log_file, fs):
        logs = [{"id": i} for i in range(10)]
        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(log) + "\n" for log in logs)

        query = LogQuery(log_file).limit(3).offset(2)
        results = query.execute()
        assert len(results) == 3
        assert results[0]["id"] == 2

    def test_log_viewer_query_types(self):
        mock_config = MagicMock()
        mock_config.json_log_file = Path("app.json")
        mock_config.errors_log_file = Path("err.json")

        viewer = LogViewer(config=mock_config)

        assert viewer.query("application").log_file == Path("app.json")
        assert viewer.query("errors").log_file == Path("err.json")

        with pytest.raises(ValueError, match="Unknown log_type"):
            viewer.query("invalid")

    @patch("src.application.services.logging.viewer.LogViewer.query")
    def test_get_level_stats(self, mock_query, log_file):
        mock_exec = MagicMock()
        mock_exec.execute.return_value = [{"level": "INFO"}, {"level": "INFO"}, {"level": "ERROR"}]
        mock_query.return_value = mock_exec

        viewer = LogViewer()
        stats = viewer.get_level_stats()
        assert stats["INFO"] == 2
        assert stats["ERROR"] == 1

    @patch("src.application.services.logging.viewer.LogViewer.query")
    def test_generate_health_report(self, mock_query):
        # Simula esecuzione bot riuscita e una fallita
        mock_exec = MagicMock()
        mock_exec.execute.return_value = [
            {
                "level": "INFO",
                "timestamp": "2023-01-01T10:00:00Z",
                "context": {"trace_id": "T1", "bot_type": "B1"},
            },
            {
                "level": "INFO",
                "timestamp": "2023-01-01T10:05:00Z",
                "context": {"trace_id": "T1", "bot_type": "B1"},
            },
            {
                "level": "ERROR",
                "timestamp": "2023-01-01T11:00:00Z",
                "context": {"trace_id": "T2", "bot_type": "B1"},
            },
        ]
        # Per semplicità, mock_query ritorni lo stesso per tutte le chiamate interne
        mock_query.return_value.time_range.return_value = mock_exec

        viewer = LogViewer()
        with patch.object(viewer, "get_bot_runs_summary") as mock_bot:
            mock_bot.return_value = [{"success": True}, {"success": False}]

            report = viewer.generate_health_report()
            assert report["total_events"] == 3
            assert report["error_rate_percent"] == 33.33
            assert report["bot_runs"]["total"] == 2
