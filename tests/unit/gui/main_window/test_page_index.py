from src.gui.main_window.page_index import PageIndex


class TestPageIndex:
    def test_page_index_values(self):
        assert PageIndex.DASHBOARD == 0
        assert PageIndex.AUTOMAZIONI == 1
        assert PageIndex.CHANGELOG == 13

    def test_page_index_enum_integrity(self):
        # Verifica che non ci siano duplicati (proprietà degli Enum)
        values = [p.value for p in PageIndex]
        assert len(values) == len(set(values))
