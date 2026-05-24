from unittest.mock import patch

from src.gui.workers.pdl_data_worker import PDLDataWorker


def test_pdl_data_worker_fetch_all(qtbot):
    with patch("src.gui.workers.pdl_data_worker.db_manager") as mock_db:
        # Mocking logic depends on what run() calls for mode "fetch_data"
        # Let's assume it calls a method that returns data
        worker = PDLDataWorker(mode="fetch_data")

        # We need to mock _fetch_pdl_data if it uses global db_manager or local controllers
        with patch.object(worker, "_fetch_pdl_data") as mock_fetch:
            mock_fetch.side_effect = lambda: worker.data_ready.emit(["pdl1"])

            with qtbot.wait_signal(worker.data_ready, timeout=5000) as blocker:
                worker.run()

            assert blocker.args[0] == ["pdl1"]


def test_pdl_data_worker_error(qtbot):
    worker = PDLDataWorker(mode="fetch_data")
    with patch.object(worker, "_fetch_pdl_data", side_effect=Exception("DB Error")):
        with qtbot.wait_signal(worker.error_signal, timeout=5000) as blocker:
            worker.run()
        assert "DB Error" in blocker.args[0]
