from unittest.mock import MagicMock

from src.gui.workers.timbrature_worker import TimbratureDataWorker


def test_timbrature_worker_run(qtbot):
    storage = MagicMock()
    # mode "fetch_data"
    worker = TimbratureDataWorker(storage, mode="fetch_data")

    storage.get_timbrature_with_reparto.return_value = [{"id": 1}]

    with qtbot.wait_signal(worker.data_ready, timeout=5000) as blocker:
        worker.run()

    assert blocker.args[0] == [{"id": 1}]


def test_timbrature_worker_error(qtbot):
    storage = MagicMock()
    worker = TimbratureDataWorker(storage, mode="fetch_data")

    storage.get_timbrature_with_reparto.side_effect = Exception("DB error")

    with qtbot.wait_signal(worker.error_signal, timeout=5000) as blocker:
        worker.run()

    assert "DB error" in blocker.args[0]
