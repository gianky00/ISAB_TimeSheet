from unittest.mock import MagicMock, patch

from src.application.services.contabilita.certificati_engine import CertificatiEngine
from src.gui.workers.certificati_worker import CertificatiWorker


def test_certificati_worker_run(qtbot):
    engine = MagicMock(spec=CertificatiEngine)
    engine.group_data_by_id_coemi.return_value = {"group1": []}
    # Mock prepare_groups_with_priority to return dicts with 'priority'
    engine.prepare_groups_with_priority.return_value = [{"id": "group1", "priority": 1}]

    with patch("src.gui.workers.certificati_worker.ContabilitaManager") as mock_mgr:
        mock_mgr.get_certificati_campione_data.return_value = []

        worker = CertificatiWorker(engine)

        with qtbot.wait_signal(worker.finished_signal, timeout=5000) as blocker:
            worker.run()

        assert blocker.args[0][0]["id"] == "group1"


def test_certificati_worker_error(qtbot):
    engine = MagicMock(spec=CertificatiEngine)
    with patch("src.gui.workers.certificati_worker.ContabilitaManager") as mock_mgr:
        mock_mgr.get_certificati_campione_data.side_effect = Exception("DB error")

        worker = CertificatiWorker(engine)

        with qtbot.wait_signal(worker.error_signal, timeout=5000) as blocker:
            worker.run()

        assert "DB error" in blocker.args[0]
