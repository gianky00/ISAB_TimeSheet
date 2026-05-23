from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.sync.operazioni_sync import OperazioniSyncEngine


class TestOperazioniSyncEngine:
    @patch("src.core.database.db_manager.get_connection")
    def test_sync_attivita_programmate_success(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simula vecchio conteggio = 5
        mock_cursor.fetchone.return_value = [5]

        # 10 nuove righe
        new_data = [tuple(["val"] * 17) for _ in range(10)]

        added, removed = OperazioniSyncEngine.sync_attivita_programmate(Path("db.sqlite"), new_data)

        assert added == 5  # 10 - 5
        assert removed == 0
        assert mock_cursor.execute.called  # DELETE
        assert mock_cursor.executemany.called  # INSERT
        assert mock_conn.commit.called

    @patch("src.core.database.db_manager.get_connection")
    def test_sync_scarico_ore_success(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simula vecchio conteggio = 100
        mock_cursor.fetchone.return_value = [100]

        # 50 nuove righe (meno delle precedenti)
        new_data = [tuple(["val"] * 12) for _ in range(50)]

        added, removed = OperazioniSyncEngine.sync_scarico_ore(Path("db.sqlite"), new_data)

        assert added == 0
        assert removed == 50  # 100 - 50
        assert mock_cursor.executemany.called

    @patch("src.core.database.db_manager.get_connection")
    def test_sync_empty_data(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [10]

        added, removed = OperazioniSyncEngine.sync_scarico_ore(Path("db.sqlite"), [])

        assert added == 0
        assert removed == 10
        assert mock_cursor.executemany.called is False
