import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.manager import DatabaseManager


class TestDBManager:
    @pytest.fixture
    def db_manager(self, tmp_path):  # noqa: ANN001
        manager = DatabaseManager()
        # Mocking CONFIG_DIR to use tmp_path
        manager.DB_DIPENDENTI = tmp_path / "dipendenti.db"
        return manager

    @patch("sqlite3.connect")
    def test_get_db_version_error_handling(self, mock_connect, db_manager):  # noqa: ANN001
        """Verifica che un errore nel recupero versione ritorni 0 (SOP) ma sia isolato."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        # Simula errore query
        mock_conn.execute.side_effect = Exception("Query Failed")

        version = db_manager._get_db_version(mock_conn)
        assert version == 0

    def test_init_db_creates_files(self, db_manager):  # noqa: ANN001
        """Verifica che init_db crei effettivamente i file database."""
        # Non mockiamo sqlite3 qui per vedere l'effetto reale su filesystem
        db_manager.init_db()
        assert db_manager.DB_DIPENDENTI.exists()

        # Verifica schema minimo (tabella dipendenti)
        with sqlite3.connect(db_manager.DB_DIPENDENTI) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dipendenti'")
            assert cursor.fetchone() is not None
