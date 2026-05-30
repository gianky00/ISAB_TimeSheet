import pandas as pd
import pytest

from src.core.stats.stats_service import StatsService


class TestStatsService:
    @pytest.fixture
    def sample_df(self):
        data = {
            "stato_attivita": [
                "CONTABILIZZATA",
                "CHIUSA",
                "IN ATTESA TCL",
                "DA COMPLETARE",
                "IN CORSO",
                "FORNITURA MATERIALE",
            ],
            "mese": ["gennaio", "Febbraio ", "marzo", "aprile", "maggio", "Giugno"],
            "tipologia": ["SQUADRA", "FERMATA", "CANONE", "MISURA", "CHIAMATA", "ALTRO"],
            "totale_prev": [100.0, 200.0, 150.0, 300.0, 50.0, 0.0],
            "ore_sp": [10.0, 20.0, 15.0, 30.0, 5.0, 0.0],
            "resa": [1.5, 2.0, 0.0, 1.2, 0.8, 0.0],
        }
        return pd.DataFrame(data)

    def test_prepare_kpi_data_empty(self):
        assert StatsService.prepare_kpi_data(pd.DataFrame(), 40.0) == {}

    def test_prepare_kpi_data_success(self, sample_df):
        res = StatsService.prepare_kpi_data(sample_df, 40.0)

        assert "stato_attivita" in res
        assert "prev_ore_mese" in res
        assert "margine_tipologia" in res
        assert "andamento_resa" in res
        assert "completamento" in res

        # Check specific values
        assert res["stato_attivita"]["CONTABILIZZATA"] == 1
        assert "FORNITURA MATERIALE" not in res["stato_attivita"]

        assert res["prev_ore_mese"]["labels"][0] == "Gen"
        assert sum(res["prev_ore_mese"]["totale_prev"]) == 800.0

        assert "SQUADRA" in res["margine_tipologia"]["labels"]
        # Cost for SQUADRA: 10.0 * 40.0 = 400.0
        idx = res["margine_tipologia"]["labels"].index("SQUADRA")
        assert res["margine_tipologia"]["costi"][idx] == 400.0

    def test_get_andamento_resa(self, sample_df):
        res = StatsService._get_andamento_resa(sample_df)
        # Resa 0.0 should be excluded from mean
        assert len(res["values"]) == 4
        assert res["values"][0] == 1.5

    def test_get_completamento_stats(self, sample_df):
        res = StatsService._get_completamento_stats(sample_df)
        total = 6.0
        assert res["p_comp"] == (2 / total) * 100  # CONTABILIZZATA, CHIUSA
        assert res["p_tcl"] == (1 / total) * 100
        assert res["p_todo"] == (1 / total) * 100
        assert res["p_other"] == (2 / total) * 100  # IN CORSO, FORNITURA

    def test_get_margine_tipologia_empty_filter(self):
        df = pd.DataFrame({"tipologia": ["INVALID"], "totale_prev": [1], "ore_sp": [1]})
        assert StatsService._get_margine_tipologia(df, 40.0) == {}
