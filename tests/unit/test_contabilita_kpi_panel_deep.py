from unittest.mock import patch

from PySide6.QtWidgets import QWidget


class TestContabilitaKPIPanelDeep:
    def test_format_currency(self, qapp):
        import src.gui.panels.contabilita_kpi.kpi_panel as kpi_mod

        with (
            patch.object(kpi_mod, "KPIChartsManager"),
            patch.object(kpi_mod, "ChartContainer", return_value=QWidget()),
        ):
            panel = kpi_mod.ContabilitaKPIPanel()
            assert panel._format_currency(1234.56) == "1.234,56"
            assert panel._format_currency(1000000) == "1.000.000,00"
