"""SyncroJob - KPI Worker.

Worker asincrono per l'elaborazione dei dati KPI e la generazione di statistiche in background.
Evita il freeze della GUI durante il calcolo massivo con Pandas.
"""

import logging

import pandas as pd
from PySide6.QtCore import QThread, Signal

from src.core.contabilita_manager import ContabilitaManager
from src.core.stats.stats_service import StatsService

logger = logging.getLogger(__name__)


class KPIWorker(QThread):
    """Worker dedicato al calcolo delle statistiche KPI.

    Esegue query SQL e analisi Pandas in un thread separato.

    Inizializza il worker.

    Args:
      year: L'anno di riferimento per l'analisi.
      hourly_cost_std: Il costo orario standard per il calcolo dei margini.

    Attributes:
        error_signal: Segnale o attributo della classe.
        finished_signal: Segnale o attributo della classe.
    """

    finished_signal = Signal(dict)  # Restituisce il dizionario con tutti i dati calcolati
    error_signal = Signal(str)

    def __init__(self, year: int, hourly_cost_std: float) -> None:
        super().__init__()
        self.year = year
        self.hourly_cost_std = hourly_cost_std

    def run(self) -> None:
        """Esegue l'elaborazione dei dati."""
        try:
            logger.info(f"[KPIWorker] Avvio elaborazione per anno {self.year}")

            # 1. Recupero statistiche base (SQL sincrono qui è sicuro perché in thread separato)
            stats = ContabilitaManager.get_year_stats(self.year)

            # 2. Recupero dati tabellari per analisi Pandas
            raw_data = ContabilitaManager.get_data_by_year(self.year)

            cols = [
                "data_prev",
                "mese",
                "n_prev",
                "totale_prev",
                "attivita",
                "tcl",
                "odc",
                "stato_attivita",
                "tipologia",
                "ore_sp",
                "resa",
                "annotazioni",
                "indirizzo_consuntivo",
                "nome_file",
            ]

            # 3. Analisi Pandas
            df = pd.DataFrame(raw_data, columns=cols)
            df["totale_prev"] = pd.to_numeric(df["totale_prev"], errors="coerce").fillna(0)
            df["ore_sp"] = pd.to_numeric(df["ore_sp"], errors="coerce").fillna(0)
            df["resa"] = pd.to_numeric(df["resa"], errors="coerce")

            avg_resa = df["resa"].mean() or 0

            # 4. Calcoli derivati
            tot_prev = stats.get("total_prev", 0.0)
            tot_ore = stats.get("total_ore", 0.0)
            costo_tot = tot_ore * self.hourly_cost_std
            margine = tot_prev - costo_tot
            marg_perc = (margine / tot_prev * 100) if tot_prev > 0 else 0
            val_ora = (tot_prev / tot_ore) if tot_ore > 0 else 0
            utile_ora = val_ora - self.hourly_cost_std

            # 5. Preparazione dati per i grafici
            kpi_chart_data = StatsService.prepare_kpi_data(df, self.hourly_cost_std)

            # 6. Assemblaggio risultato finale
            result = {
                "summary": {
                    "tot_prev": tot_prev,
                    "tot_ore": tot_ore,
                    "count": stats.get("count_total", 0),
                    "ore_dirette": stats.get("ore_dirette", 0.0),
                    "ore_indirette": stats.get("ore_indirette", 0.0),
                    "avg_resa": avg_resa,
                    "margine": margine,
                    "marg_perc": marg_perc,
                    "val_ora": val_ora,
                    "utile_ora": utile_ora,
                },
                "chart_data": kpi_chart_data,
            }

            logger.info(f"[KPIWorker] Elaborazione completata per anno {self.year}")
            self.finished_signal.emit(result)

        except Exception as e:
            logger.exception(f"[KPIWorker] Errore critico durante l'elaborazione KPI per anno {self.year}")
            self.error_signal.emit(str(e))
