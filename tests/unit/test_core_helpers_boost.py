import sqlite3
from unittest.mock import patch

import pytest

from src.application.services.data_synchronizer import DataSynchronizer


class TestCoreHelpersBoost:
    @pytest.fixture
    def db(self, tmp_path):
        db_path = tmp_path / "helpers_boost.db"
        with sqlite3.connect(db_path) as conn:
            # Schema allineato a ContabilitaSyncEngine (usa 'year')
            conn.execute("CREATE TABLE contabilita (year INTEGER, data_prev TEXT, n_prev TEXT)")
            conn.commit()
        return db_path

    def test_data_synchronizer_sync_contabilita(self, db):
        new_data = [(2024, "01/01/2024", "100/24")]
        years = [2024]

        with patch("src.application.services.sync.contabilita_sync.ContabilitaSyncEngine.sync_partitioned_data") as mock_sync:
            mock_sync.return_value = (1, 0)
            added, _removed = DataSynchronizer.sync_contabilita(db, new_data, years)
            assert added == 1
            assert mock_sync.called

    def test_data_synchronizer_empty(self, db):
        res = DataSynchronizer.sync_storico_oda(db, [])
        assert res == (0, 0)

    def test_sortable_item_logic(self):
        from src.gui.widgets.core_widgets import SortableTableWidgetItem

        it1 = SortableTableWidgetItem("10")
        it2 = SortableTableWidgetItem("2")
        # Ordinamento numerico: 2 < 10
        assert it2 < it1
