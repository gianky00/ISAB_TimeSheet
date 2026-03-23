import pandas as pd

from src.core.stats.stats_service import StatsService


class TestStatsService:
    def test_prepare_kpi_data_empty(self):
        """Verifica che un dataframe vuoto ritorni un dict vuoto."""
        assert StatsService.prepare_kpi_data(pd.DataFrame(), 30.0) == {}

    def test_prepare_kpi_data_full(self):
        """Verifica il calcolo corretto di tutte le metriche KPI."""
        data = {
            "stato_attivita": ["CONTABILIZZATA", "DA COMPLETARE", "FORNITURA"],
            "mese": ["Gennaio", "Febbraio", "Marzo"],
            "totale_prev": [1000.0, 500.0, 2000.0],
            "ore_sp": [10.0, 5.0, 0.0],
            "tipologia": ["SQUADRA", "MISURA", "FORNITURA"],
            "resa": [100.0, 80.0, 0.0],
        }
        df = pd.DataFrame(data)

        results = StatsService.prepare_kpi_data(df, 30.0)

        # 1. Stato Attività (deve escludere FORNITURA)
        counts = results["stato_attivita"]
        assert "CONTABILIZZATA" in counts
        assert "FORNITURA" not in counts

        # 2. Prev ore mese
        prev_mese = results["prev_ore_mese"]
        assert "Gen" in prev_mese["labels"]
        assert 1000.0 in prev_mese["totale_prev"]

        # 3. Margine tipologia
        margine = results["margine_tipologia"]
        assert "SQUADRA" in margine["labels"]
        # Costo SQUADRA = 10 ore * 30.0 = 300.0
        assert 300.0 in margine["costi"]

    def test_completamento_stats_logic(self):
        """Verifica le percentuali di completamento."""
        data = {"stato_attivita": ["CONTABILIZZATA", "IN ATTESA TCL", "DA COMPLETARE", "ALTRO"]}
        df = pd.DataFrame(data)
        stats = StatsService._get_completamento_stats(df)

        assert stats["p_comp"] == 25.0
        assert stats["p_tcl"] == 25.0
        assert stats["p_todo"] == 25.0
        assert stats["p_other"] == 25.0
