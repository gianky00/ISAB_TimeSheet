from unittest.mock import patch

from src.gui.contabilita_kpi_panel import ContabilitaKPIPanel


class TestContabilitaKPIPanelDeep:
    @patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024])
    @patch("src.core.contabilita_manager.ContabilitaManager.get_year_stats")
    @patch("src.core.contabilita_manager.ContabilitaManager.get_data_by_year")
    def test_load_kpi_data_and_plotting(self, mock_get_data, mock_get_stats, mock_years, qapp, qtbot):
        # Mock stats
        mock_get_stats.return_value = {
            "total_prev": 10000.0,
            "total_ore": 100.0,
            "count_total": 5,
            "ore_dirette": 80.0,
            "ore_indirette": 20.0
        }

        # Mock raw data for charts
        data = [
            ("2024-01-01", "gennaio", "P1", "1000", "A1", "T1", "O1", "CHIUSA", "SQUADRA", "10", "1.0", "", "", "")
        ]
        mock_get_data.return_value = data

        panel = ContabilitaKPIPanel()
        qtbot.addWidget(panel)

        # Trigger data load for 2024
        panel.year_combo.setCurrentText("2024")
        panel._load_kpi_data()

        # Verify cards updated
        assert "10.000,00" in panel.card_totale.lbl_value.text()
        assert "100,00" in panel.card_ore.lbl_value.text()

        # Verify charts were drawn (canvases have figures with content)
        assert len(panel.fig1.axes) > 0
        assert len(panel.fig2.axes) > 0
        assert len(panel.fig3.axes) > 0

    def test_format_currency(self, qapp):
        panel = ContabilitaKPIPanel()
        assert panel._format_currency(1234.56) == "1.234,56"
        assert panel._format_currency(1000000) == "1.000.000,00"
