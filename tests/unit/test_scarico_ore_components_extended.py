import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.gui.scarico_ore_components import ScaricoOreTableModel, CacheWorker

class TestScaricoOreComponentsExtended:
    def test_table_model_init(self, qapp):
        model = ScaricoOreTableModel()
        assert model.columnCount() == 11
        assert model.rowCount() == 0

    @pytest.mark.asyncio
    async def test_cache_worker_build(self, qapp, qtbot):
        # Sample data: 11 columns + style
        data = [
            ("2024-01-01", "P1", "P2", "ODC", "POS", "08:00", "17:00", "8.00", "Desc", "SI", "COMM", "{}")
        ]
        worker = CacheWorker(Path("test_cache.pkl"), data_source=data)
        
        with qtbot.wait_signal(worker.finished, timeout=2000):
            worker.start()
            
        # Verify that display cache was built
        # finished signal: display_data, search_index, float_totals, style_cache
        # We can't easily check args of signal from worker.start() without more setup,
        # but we can test the internal _build_caches
        display, search, totals, styles = worker._build_caches(data)
        assert len(display) == 1
        assert display[0][0] == "01/01/2024" # Date formatted
        assert totals[0] == 8.0

    def test_model_filtering(self, qapp):
        model = ScaricoOreTableModel()
        # Manually inject data to test filter logic without async
        model._display_data = [
            ["01/01/2024", "Mario", "Rossi", "ODC1", "1", "08", "17", "8", "Lavoro", "NO", "C1"],
            ["02/01/2024", "Luigi", "Verdi", "ODC2", "2", "09", "18", "8", "Altro", "SI", "C2"]
        ]
        model._search_index = ["01/01/2024 mario rossi odc1...", "02/01/2024 luigi verdi odc2..."]
        model._visible_indices = [0, 1]
        model._filtered_count = 2
        
        # Filter for "Mario"
        model.set_filter("mario")
        assert model.rowCount() == 1
        
        # Clear filter
        model.set_filter("")
        assert model.rowCount() == 2