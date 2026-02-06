import sqlite3
from pathlib import Path
from unittest.mock import patch

from PyQt6.QtWidgets import QTreeWidget

from src.core.data_synchronizer import DataSynchronizer
from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem


class TestCoreHelpersBoost:
    def test_sortable_item_logic(self, qapp):
        tw = QTreeWidget()
        item1 = SortableTreeWidgetItem(["01/01/2024"])
        item2 = SortableTreeWidgetItem(["02/01/2024"])
        tw.addTopLevelItem(item1)
        tw.addTopLevelItem(item2)
        assert item1.__lt__(item2) is True

    def test_data_synchronizer_sync_contabilita(self, tmp_path):
        db_path = tmp_path / "test.db"
        # Init DB with table
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                "CREATE TABLE contabilita (year INTEGER, data TEXT, n_prev TEXT)"
            )

        # Test sync (empty to 1 row)
        data = [(2024, "01/01/2024", "100/24")]
        with patch(
            "src.core.excel_importer.ExcelImporter.COLUMNS_MAPPING",
            {"D": "data", "P": "n_prev"},
        ):
            added, removed = DataSynchronizer.sync_contabilita_dati(
                db_path, data, [2024]
            )
            assert added == 1
            assert removed == 0

    def test_data_synchronizer_empty(self, tmp_path):
        res = DataSynchronizer.sync_contabilita_dati(Path("nonexistent"), [], [])
        assert res == (0, 0)
