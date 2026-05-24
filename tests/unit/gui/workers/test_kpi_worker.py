from unittest.mock import patch

from src.gui.workers.kpi_worker import KPIWorker


def test_kpi_worker_run(qtbot):
    # Mock ContabilitaManager and StatsService
    with (
        patch("src.gui.workers.kpi_worker.ContabilitaManager") as mock_mgr,
        patch("src.gui.workers.kpi_worker.StatsService") as mock_svc,
    ):
        mock_mgr.get_year_stats.return_value = {"total": 100}
        mock_svc.calculate_margins.return_value = {"margin": 10}
        # Assuming run does more things, let's keep it simple

        worker = KPIWorker(year=2024, hourly_cost_std=40.0)

        # In actual code it might emit finished_signal with a dict
        with qtbot.wait_signal(worker.finished_signal, timeout=5000) as blocker:
            worker.run()

        assert isinstance(blocker.args[0], dict)


def test_kpi_worker_error(qtbot):
    with patch("src.gui.workers.kpi_worker.ContabilitaManager") as mock_mgr:
        mock_mgr.get_year_stats.side_effect = Exception("KPI error")

        worker = KPIWorker(year=2024, hourly_cost_std=40.0)

        with qtbot.wait_signal(worker.error_signal, timeout=5000) as blocker:
            worker.run()

        assert "KPI error" in blocker.args[0]
