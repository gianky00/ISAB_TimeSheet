from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.data_synchronizer import DataSynchronizer


@pytest.fixture
def mock_db_path():
    return Path("mock_db.sqlite")

def test_sync_contabilita(mock_db_path):
    with patch("src.core.data_synchronizer.ContabilitaSyncEngine") as mock_engine:
        mock_engine.sync_contabilita.return_value = (10, 0)

        # Test input list format
        data = [{"col1": "val1"}, {"col1": "val2"}]
        inserted, _updated = DataSynchronizer.sync_contabilita(mock_db_path, data, [2026])

        assert inserted == 10
        mock_engine.sync_contabilita.assert_called_once()
        # Verifica trasformazione dati
        args = mock_engine.sync_contabilita.call_args[0]
        assert args[1] == [("val1",), ("val2",)]

def test_sync_giornaliere(mock_db_path):
    with patch("src.core.data_synchronizer.ContabilitaSyncEngine") as mock_engine:
        mock_engine.sync_giornaliere.return_value = (5, 0)

        data = [("val1",), ("val2",)]
        inserted, _updated = DataSynchronizer.sync_giornaliere(mock_db_path, data, [2026])

        assert inserted == 5
        mock_engine.sync_giornaliere.assert_called_once()
        assert mock_engine.sync_giornaliere.call_args[0][1] == data
