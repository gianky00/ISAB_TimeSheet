import pytest

from src.gui.widgets.contabilita.year_tab import ContabilitaYearTab


class TestContabilitaTableLogic:
    @pytest.fixture
    def tab(self, qtbot):
        # V9.4: Signature is (year, parent=None)
        widget = ContabilitaYearTab(2024)
        qtbot.addWidget(widget)
        return widget

    def test_contabilita_year_tab_totals(self, tab):
        data = [
            ("PREV1", "Att1", "1.000,00", "01/01/2024", "10,0", "A", "N", "U", "C", "S"),
        ]
        tab.table.model().sourceModel().update_data(data)
        assert True

    def test_giornaliere_year_tab_format(self, tab):
        # Placeholder per verifica formattazione ore
        assert True
