from unittest.mock import MagicMock, patch

from src.gui.workers.health_worker import HealthWorker


def test_health_worker_run(qtbot):
    # Mock generate_analytics_report and LogViewer
    with (
        patch("src.gui.workers.health_worker.generate_analytics_report") as mock_gen,
        patch("src.gui.workers.health_worker.LogViewer") as mock_viewer_cls,
    ):
        # Must return an object with health_score and anomalies attributes
        report = MagicMock()
        report.health_score = 90
        report.anomalies = []
        mock_gen.return_value = report

        mock_viewer = MagicMock()
        mock_viewer.generate_health_report.return_value = {
            "bot_runs": {"successful": 5, "failed": 1},
            "error_rate_percent": 2.0,
        }
        mock_viewer_cls.return_value = mock_viewer

        worker = HealthWorker()

        with qtbot.wait_signal(worker.finished_signal, timeout=5000) as blocker:
            worker.run()

        results = blocker.args[0]
        assert results["health_score"] == 90
        assert results["bot_runs_ok"] == 5
        assert results["bot_runs_fail"] == 1
        assert results["error_rate"] == 2.0


def test_health_worker_error(qtbot):
    with patch("src.gui.workers.health_worker.generate_analytics_report") as mock_gen:
        mock_gen.side_effect = Exception("Health fail")

        worker = HealthWorker()

        with qtbot.wait_signal(worker.error_signal, timeout=5000) as blocker:
            worker.run()

        assert "Health fail" in blocker.args[0]
