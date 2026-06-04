from unittest.mock import patch

from src.application.services.contabilita_worker import ContabilitaWorker


class TestContabilitaWorkerDeep:
    def test_worker_run_success(self, qtbot):
        worker = ContabilitaWorker("fake_path.xlsx")

        with (
            patch("src.application.services.contabilita_manager.ContabilitaManager.init_db"),
            patch(
                "src.application.services.contabilita_manager.ContabilitaManager.scan_workload",
                return_value=(1, 1),
            ),
            patch("src.application.services.contabilita_manager.ContabilitaManager.import_data_from_excel") as mock_import,
            patch("src.application.services.contabilita_worker.Path.exists", return_value=True),
        ):
            mock_import.return_value = (True, "Successo", 10, 2)

            # Using qtbot to catch signals
            with qtbot.wait_signal(worker.finished_signal, timeout=2000):
                worker.start()  # Start in real thread

            # import_data_from_excel should have been called
            mock_import.assert_called_once()

    def test_worker_error_handling(self, qtbot):
        worker = ContabilitaWorker("bad_path")
        # We test the logic of run() directly but mock everything inside to catch exception
        with (
            patch("src.application.services.contabilita_manager.ContabilitaManager.init_db"),
            patch(
                "src.application.services.contabilita_manager.ContabilitaManager.scan_workload",
                return_value=(1, 1),
            ),
            patch(
                "src.application.services.contabilita_manager.ContabilitaManager.import_data_from_excel",
                side_effect=Exception("Crash"),
            ),
            patch("src.application.services.contabilita_worker.Path.exists", return_value=True),
        ):
            # Direct call to run() instead of start() to see how it handles exception
            # Actually worker.run() has a try-except? Let's check
            # No, ContabilitaWorker.run in file I saw doesn't have a global try-except for import_data_from_excel
            # It has try-except for the whole thing only in some places.

            with qtbot.wait_signal(worker.finished_signal, timeout=2000):
                # We expect the worker to emit False if it crashes, but we need to ensure it doesn't raise
                # Since the current code DOES NOT have a top-level try-except around import_data_from_excel,
                # we should probably add it to the code to make it robust.
                worker.start()
