from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.data_synchronizer import DataSynchronizer


class TestDataSynchronizerDetailed:
    @pytest.fixture
    def mock_db(self):
        with patch("src.core.data_synchronizer.db_manager") as mock_manager:
            conn = MagicMock()
            cursor = MagicMock()
            conn.cursor.return_value = cursor
            mock_manager.get_connection.return_value.__enter__.return_value = conn
            yield conn, cursor

    def test_sync_contabilita_dati_empty(self, mock_db):
        added, removed = DataSynchronizer.sync_contabilita_dati(Path("fake.db"), [], [])
        assert added == 0
        assert removed == 0

    def test_sync_giornaliere_logic(self, mock_db):
        _conn, cursor = mock_db
        # Mock fetchone for counts (added, removed)
        cursor.fetchone.side_effect = [(5,), (2,)]

        new_rows = [
            (
                2024,
                "2024-01-01",
                "P",
                "D",
                "T",
                "O",
                "P",
                "08",
                "17",
                8,
                "100",
                "file.xlsx",
            )
        ]
        years = [2024]

        added, removed = DataSynchronizer.sync_giornaliere(Path("fake.db"), new_rows, years)

        assert added == 5
        assert removed == 2
        assert cursor.executemany.called
        # Check if temporary table was created
        args, _ = cursor.execute.call_args_list[1]
        assert "CREATE TEMPORARY TABLE temp_giornaliere" in args[0]

    def test_sync_attivita_programmate(self, mock_db):
        _conn, cursor = mock_db
        # old_count = 10
        cursor.fetchone.return_value = (10,)

        added, removed = DataSynchronizer.sync_attivita_programmate(Path("fake.db"), [("row", "style")])

        # 1 new - 10 old = 0 added, 9 removed (net)
        assert added == 0
        assert removed == 9
        assert "attivita_programmate" in cursor.execute.call_args_list[1][0][0]

    def test_sync_scarico_ore(self, mock_db):
        _conn, cursor = mock_db
        # New logic: gets old_count (10), then calculates diff vs new_count (15)
        cursor.fetchone.return_value = (10,)

        # Create 15 dummy rows
        new_rows = [("data",)] * 15

        added, removed = DataSynchronizer.sync_scarico_ore(Path("fake.db"), new_rows)

        # 15 new - 10 old = 5 added, 0 removed
        assert added == 5
        assert removed == 0

        # Verify optimized sync calls
        # Should call SELECT COUNT
        cursor.execute.assert_any_call("SELECT COUNT(*) FROM scarico_ore")
        # Should call DELETE ALL
        cursor.execute.assert_any_call("DELETE FROM scarico_ore")
        # Should insert new rows
        assert cursor.executemany.called

    def test_sync_contabilita_full_replace(self, mock_db):
        """Test _replace_data with year=None."""
        _conn, cursor = mock_db
        DataSynchronizer._replace_data(cursor, "contabilita", ["col1"], year=None)
        cursor.execute.assert_any_call("DELETE FROM contabilita")

    def test_sync_attivita_programmate_special_values(self, mock_db):
        """Test clean_value logic with None and numeric types."""
        _conn, cursor = mock_db
        cursor.fetchone.return_value = (0,)
        rows = [(None, 123, 45.6, " string ")]
        DataSynchronizer.sync_attivita_programmate(Path("fake.db"), rows)
        # Should work without error
        assert cursor.executemany.called

    def test_sync_certificati_campione(self, mock_db):
        """Test sync_certificati_campione wrapper."""
        _conn, cursor = mock_db
        # _sync_upsert_smart returns (added, 0)
        cursor.fetchone.return_value = (3,)
        added, removed = DataSynchronizer.sync_certificati_campione(Path("fake.db"), [(1, 2)])
        assert added == 3
        assert removed == 0

    def test_sync_upsert_smart_edge_cases(self, mock_db):
        """Test _sync_upsert_smart with empty data and None."""
        _conn, cursor = mock_db

        # Empty
        added, _ = DataSynchronizer._sync_upsert_smart(Path("fake.db"), "table", ["c1"], [])
        assert added == 0

        # With None
        cursor.fetchone.return_value = (1,)
        added, _ = DataSynchronizer._sync_upsert_smart(Path("fake.db"), "table", ["c1"], [(None,)])
        assert added == 1
