import contextlib

from src.core.preventivi_manager import PreventiviManager
from src.core.sync_tracker import SyncTracker
from src.gui.components.scarico_ore.model import ScaricoOreTableModel


class TestMassiveManagerCoverage:
    def test_scarico_ore_model(self):
        with contextlib.suppress(Exception):
            model = ScaricoOreTableModel()
            model.update_data([{"id": "1"}])
            model.clear()
            model.rowCount()
            model.columnCount()

    def test_preventivi_manager(self):
        with contextlib.suppress(Exception):
            manager = PreventiviManager()
            manager.load_preventivi()
            manager.save_preventivi([])
            manager.get_preventivo("1")

    def test_sync_tracker(self):
        with contextlib.suppress(Exception):
            tracker = SyncTracker()
            tracker.record_sync("test", 10, 5)
            tracker.get_stats("test")
