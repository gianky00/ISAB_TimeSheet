"""
SyncroJob - Stats Service
Servizio CORE per il calcolo delle statistiche KPI e manipolazione dati Pandas.
Agnostico rispetto alla GUI.
"""

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

class StatsService:
    """Servizio per l'elaborazione dei dati statistici e KPI."""

    @staticmethod
    def prepare_kpi_data(df: pd.DataFrame, hourly_cost_std: float) -> dict[str, Any]:
        """
        Prepara tutti i dati necessari per i grafici KPI partendo dal dataframe grezzo.
        
        Args:
            df: Dataframe contabilità.
            hourly_cost_std: Costo orario standard per calcoli margini.
            
        Returns:
            Dict con i dati processati pronti per il rendering.
        """
        if df.empty:
            return {}

        results = {
            "stato_attivita": StatsService._get_stato_attivita_counts(df),
            "prev_ore_mese": StatsService._get_prev_ore_mese(df),
            "margine_tipologia": StatsService._get_margine_tipologia(df, hourly_cost_std),
            "andamento_resa": StatsService._get_andamento_resa(df),
            "completamento": StatsService._get_completamento_stats(df)
        }
        return results

    @staticmethod
    def _get_stato_attivita_counts(df: pd.DataFrame) -> dict[str, int]:
        df_filtered = df[~df["stato_attivita"].str.contains("FORNITURA", case=False, na=False)]
        raw_counts = df_filtered["stato_attivita"].value_counts().to_dict()
        return {str(k): int(v) for k, v in raw_counts.items()}

    @staticmethod
    def _get_prev_ore_mese(df: pd.DataFrame) -> dict[str, Any]:
        months_order = [
            "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
            "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"
        ]
        temp_df = df.copy()
        temp_df["mese_lower"] = temp_df["mese"].str.lower().str.strip()
        temp_df["mese_cat"] = pd.Categorical(temp_df["mese_lower"], categories=months_order, ordered=True)
        grouped = temp_df.groupby("mese_cat", observed=True)[["totale_prev", "ore_sp"]].sum()

        return {
            "labels": [m.capitalize()[:3] for m in grouped.index],
            "totale_prev": grouped["totale_prev"].tolist(),
            "ore_sp": grouped["ore_sp"].tolist()
        }

    @staticmethod
    def _get_margine_tipologia(df: pd.DataFrame, hourly_cost_std: float) -> dict[str, Any]:
        target_types = ["SQUADRA", "FERMATA", "CANONE", "MISURA", "CHIAMATA"]
        temp_df = df.copy()
        temp_df["tipologia_upper"] = temp_df["tipologia"].str.upper().str.strip()
        filtered = temp_df[temp_df["tipologia_upper"].isin(target_types)]

        if filtered.empty:
            return {}

        grouped = filtered.groupby("tipologia_upper")[["totale_prev", "ore_sp"]].sum()
        grouped["Costo"] = grouped["ore_sp"] * hourly_cost_std
        grouped = grouped.sort_values(by="totale_prev", ascending=True)

        return {
            "labels": grouped.index.tolist(),
            "ricavi": grouped["totale_prev"].tolist(),
            "costi": grouped["Costo"].tolist()
        }

    @staticmethod
    def _get_andamento_resa(df: pd.DataFrame) -> dict[str, Any]:
        months_order = [
            "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
            "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"
        ]
        temp_df = df.copy()
        temp_df["mese_lower"] = temp_df["mese"].str.lower().str.strip()
        temp_df["mese_cat"] = pd.Categorical(temp_df["mese_lower"], categories=months_order, ordered=True)
        df_resa = temp_df[temp_df["resa"] > 0]
        grouped = df_resa.groupby("mese_cat", observed=True)["resa"].mean()

        return {
            "labels": [m.capitalize()[:3] for m in grouped.index],
            "values": grouped.values.tolist()
        }

    @staticmethod
    def _get_completamento_stats(df: pd.DataFrame) -> dict[str, float]:
        total = len(df)
        if total == 0:
            return {}

        completed = len(df[df["stato_attivita"].str.contains("CONTABILIZZA|CHIUSA", case=False, na=False)])
        pending_tcl = len(df[df["stato_attivita"].str.contains("IN ATTESA TCL", case=False, na=False)])
        to_complete = len(df[df["stato_attivita"].str.contains("DA COMPLETARE", case=False, na=False)])
        other = total - completed - pending_tcl - to_complete

        return {
            "p_comp": (completed / total) * 100,
            "p_tcl": (pending_tcl / total) * 100,
            "p_todo": (to_complete / total) * 100,
            "p_other": (other / total) * 100
        }
