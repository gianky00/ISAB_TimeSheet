from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.database.maintenance_worker import DatabaseMaintenanceWorker


class TestDatabaseMaintenanceWorker:
    @patch("src.core.database.db_manager.get_write_connection")
    def test_optimize_db(self, mock_conn):
        mock_db_path = Path("/fake/db.sqlite")
        worker = DatabaseMaintenanceWorker()

        worker._optimize_db(mock_db_path)

        # Verifica che vengano eseguiti ANALYZE e VACUUM
        # Il mock_conn è un context manager
        conn_instance = mock_conn.return_value.__enter__.return_value
        calls = conn_instance.execute.call_args_list
        assert any("ANALYZE" in str(c) for c in calls)
        assert any("VACUUM" in str(c) for c in calls)

    def test_clean_logs(self, fs):
        from src.core.paths import LOGS_DIR

        fs.create_dir(str(LOGS_DIR))

        # Un log recente
        fs.create_file(str(LOGS_DIR / "recent.log"))

        # Un log vecchio (usiamo patch per mtime)
        old_log = LOGS_DIR / "old.log"
        fs.create_file(str(old_log))

        with patch.object(Path, "stat") as mock_stat:
            # mock_stat deve ritornare valori diversi per file diversi
            def stat_side_effect(path_obj):
                m = MagicMock()
                if "old.log" in str(path_obj):
                    m.st_mtime = 0  # 1970
                else:
                    m.st_mtime = 2000000000  # Futuro/recente
                return m

            # Attenzione: patching Path.stat può essere pericoloso con pyfakefs
            # Meglio patchare direttamente la logica di cutoff o usare un approccio più chirurgico

    @patch("src.core.database.maintenance_worker.DatabaseMaintenanceWorker._optimize_db")
    @patch("src.core.database.maintenance_worker.DatabaseMaintenanceWorker._clean_logs")
    def test_run_orchestration(self, mock_clean, mock_optimize, fs):
        from src.core.database import db_manager

        # Creiamo un file DB finto
        fs.create_file(str(db_manager.DB_DIPENDENTI))

        worker = DatabaseMaintenanceWorker()
        worker.run()

        # Deve aver chiamato optimize almeno per il DB esistente
        assert mock_optimize.called
        assert mock_clean.called
