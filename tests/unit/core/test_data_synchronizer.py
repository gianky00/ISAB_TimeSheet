from pathlib import Path
from unittest.mock import patch

from src.core.data_synchronizer import DataSynchronizer


class TestDataSynchronizer:
    @patch("src.core.data_synchronizer.ContabilitaSyncEngine.sync_contabilita")
    def test_sync_contabilita(self, mock_sync):
        mock_sync.return_value = (10, 0)
        res = DataSynchronizer.sync_contabilita(Path("db"), [{"a": 1}], [2023])
        assert res == (10, 0)
        assert mock_sync.called

    @patch("src.core.data_synchronizer.ContabilitaSyncEngine.sync_giornaliere")
    def test_sync_giornaliere(self, mock_sync):
        mock_sync.return_value = (5, 5)
        res = DataSynchronizer.sync_giornaliere(Path("db"), [(2023, "R1")], [2023])
        assert res == (5, 5)

    @patch("src.core.data_synchronizer.SmartSyncEngine.sync_upsert_smart")
    def test_sync_storico_oda(self, mock_sync):
        mock_sync.return_value = (20, 2)
        res = DataSynchronizer.sync_storico_oda(Path("db"), [])
        assert res == (20, 2)

    @patch("src.core.data_synchronizer.SmartSyncEngine.sync_full_replace_with_metadata")
    def test_sync_attivita_programmate(self, mock_sync):
        mock_sync.return_value = (100, 100)
        res = DataSynchronizer.sync_attivita_programmate(Path("db"), [])
        assert res == (100, 100)

    @patch("src.core.data_synchronizer.SmartSyncEngine.sync_full_replace_with_metadata")
    def test_sync_scarico_ore(self, mock_sync):
        mock_sync.return_value = (50, 50)
        res = DataSynchronizer.sync_scarico_ore(Path("db"), [])
        assert res == (50, 50)

    @patch("src.core.data_synchronizer.SmartSyncEngine.sync_full_replace_with_metadata")
    def test_sync_certificati_campione(self, mock_sync):
        mock_sync.return_value = (30, 10)
        res = DataSynchronizer.sync_certificati_campione(Path("db"), [])
        assert res == (30, 10)
