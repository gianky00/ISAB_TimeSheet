import pytest

from src.gui.panels.contabilita_kpi.kpi_panel import ContabilitaKPIPanel


class TestContabilitaKPIPanelDeep:
    @pytest.fixture
    def panel(self, qtbot, mocker):
        # Mocking complex dependencies to avoid Qt crashes in headless
        mocker.patch("src.core.sync_tracker.SyncTracker.get_formatted_status", return_value="OK")
        mocker.patch(
            "src.gui.panels.contabilita_kpi.main_panel.ContabilitaStats.get_year_stats",
            return_value={
                "total_prev": 1000.0,
                "total_ore": 100.0,
                "count_total": 10,
                "status_counts": {},
                "top_commesse": [],
                "ore_dirette": 80.0,
                "ore_indirette": 20.0,
            },
        )
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024]
        )

        p = ContabilitaKPIPanel()
        qtbot.addWidget(p)
        return p

    def test_format_currency(self, panel):
        # Verifica logica di formattazione interna (non visuale)
        from src.gui.formatters import format_currency_smart

        res = format_currency_smart(1200.5)
        # Italian locale: '1.200,50' or similar
        assert "1.200" in res

    def test_refresh_data_logic(self, panel):
        panel.refresh_data()
        assert panel.total_prev_card.val_lbl.text() != "-"
