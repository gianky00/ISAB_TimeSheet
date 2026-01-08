"""
SyncroJob - Contabilita Stats
Gestisce il calcolo delle statistiche per i dati della Contabilità Strumentale.
"""

from pathlib import Path
from typing import Dict, List, TypedDict

from src.core.contabilita_queries import ContabilitaQueries  # Per accedere ai dati
from src.utils.parsing import parse_currency


class YearStats(TypedDict):
    total_prev: float
    total_ore: float
    count_total: int
    status_counts: Dict[str, int]
    top_commesse: List[tuple]
    ore_dirette: float
    ore_indirette: float


class ContabilitaStats:
    """Gestore per il calcolo delle statistiche del database della Contabilità Strumentale."""

    @classmethod
    def get_year_stats(cls, db_path: Path, year: int) -> YearStats:
        """Calcola statistiche avanzate per l'anno specificato (Tabella Dati) + KPI Diretti/Indiretti."""
        data = ContabilitaQueries.get_data_by_year(db_path, year)
        giornaliere = ContabilitaQueries.get_giornaliere_by_year(db_path, year)

        stats: YearStats = {
            "total_prev": 0.0,
            "total_ore": 0.0,
            "count_total": 0,
            "status_counts": {},
            "top_commesse": [],
            "ore_dirette": 0.0,
            "ore_indirette": 0.0,
        }

        commesse = []
        if data:
            for row in data:
                try:
                    n_prev = str(row[2]).strip()
                    if not n_prev:
                        continue
                    if "totale" in n_prev.lower():
                        continue

                    val_prev = parse_currency(row[3])
                    val_ore = parse_currency(row[9])

                    stats["total_prev"] += val_prev
                    stats["total_ore"] += val_ore
                    stats["count_total"] += 1

                    status = str(row[7]).strip().upper()
                    if status:
                        stats["status_counts"][status] = stats["status_counts"].get(status, 0) + 1

                    if val_prev > 0:
                        attivita = str(row[4]).strip() or "N/D"
                        commesse.append((attivita, val_prev))
                except:
                    pass

        stats["top_commesse"] = sorted(commesse, key=lambda x: x[1], reverse=True)[:5]

        if giornaliere:
            for row in giornaliere:
                try:
                    n_prev = str(row[4]).strip()
                    odc = str(row[5]).strip()
                    if n_prev.lower() == "nan":
                        n_prev = ""
                    if odc.lower() == "nan":
                        odc = ""

                    ore = parse_currency(row[9])

                    if n_prev or odc:
                        stats["ore_dirette"] += ore
                    else:
                        stats["ore_indirette"] += ore
                except:
                    pass

        return stats
