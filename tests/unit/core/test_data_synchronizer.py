from pathlib import Path
from unittest.mock import patch

from src.core.data_synchronizer import DataSynchronizer


class TestDataSynchronizer:
    @patch("src.core.data_synchronizer.SmartSyncEngine.sync_upsert_smart")
    def test_sync_storico_oda_delegation(self, mock_smart_sync):  # noqa: ANN001
        """Verifica che la sync degli OdA deleghi correttamente allo SmartSyncEngine."""
        mock_smart_sync.return_value = (10, 2)
        db_path = Path("test.db")
        rows = [("123", "10", "1", "Desc")]

        added, removed = DataSynchronizer.sync_storico_oda(db_path, rows)

        assert added == 10  # noqa: PLR2004
        assert removed == 2  # noqa: PLR2004
        mock_smart_sync.assert_called_once()
        # Verifica parametri tramite kwargs o args
        _, kwargs = mock_smart_sync.call_args
        assert kwargs["conflict_cols"] == ["oda", "pos_oda", "num_riga"]

    @patch("src.core.data_synchronizer.OperazioniSyncEngine.sync_scarico_ore")
    def test_sync_scarico_ore_delegation(self, mock_ops_sync):  # noqa: ANN001
        mock_ops_sync.return_value = (500, 0)
        added, _removed = DataSynchronizer.sync_scarico_ore(Path("test.db"), [])
        assert added == 500  # noqa: PLR2004
        mock_ops_sync.assert_called_once()
