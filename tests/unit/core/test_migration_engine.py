from unittest.mock import MagicMock, patch

from src.core.initialization.migration_engine import DatabaseMigrationEngine


class TestDatabaseMigrationEngine:
    @patch("src.core.initialization.migration_engine.db_manager.init_db")
    @patch("src.core.initialization.migration_engine.DatabaseBackupManager.execute_backup")
    def test_initialize_database(self, mock_backup, mock_init):
        step = MagicMock()
        DatabaseMigrationEngine.initialize_database(step)
        assert mock_init.called
        assert mock_backup.called
        assert step.call_count == 2
