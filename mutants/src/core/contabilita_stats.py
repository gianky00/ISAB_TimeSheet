"""
SyncroJob - Contabilita Stats
Gestisce il calcolo delle statistiche per i dati della Contabilità Strumentale.
"""

import operator
from contextlib import suppress
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
        """Calcola statistiche avanzate per l'anno specificato."""
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

        # 1. Processo Tabella Dati (KPI OdA)
        commesse = cls._process_main_data(data, stats)
        stats["top_commesse"] = sorted(
            commesse, key=operator.itemgetter(1), reverse=True
        )[:5]

        # 2. Processo Giornaliere (KPI Diretti/Indiretti)
        cls._process_giornaliere_stats(giornaliere, stats)

        return stats

    @classmethod
    def _process_main_data(cls, data, stats) -> List[tuple]:
        """Processa i dati OdA principali per calcolare totali e status."""
        commesse: list[tuple] = []
        if not data:
            return commesse

        for row in data:
            with suppress(Exception):
                n_prev = str(row[2]).strip()
                if not n_prev or "totale" in n_prev.lower():
                    continue

                v_prev = parse_currency(row[3])
                v_ore = parse_currency(row[9])

                stats["total_prev"] += v_prev
                stats["total_ore"] += v_ore
                stats["count_total"] += 1

                status = str(row[7]).strip().upper()
                if status:
                    stats["status_counts"][status] = (
                        stats["status_counts"].get(status, 0) + 1
                    )

                if v_prev > 0:
                    attivita = str(row[4]).strip() or "N/D"
                    commesse.append((attivita, v_prev))
        return commesse

    @classmethod
    def _process_giornaliere_stats(cls, giornaliere, stats):
        """Processa le timbrature giornaliere per distinguere ore dirette/indirette."""
        if not giornaliere:
            return

        for row in giornaliere:
            with suppress(Exception):
                n_prev = str(row[4]).strip()
                odc = str(row[5]).strip()
                ore = parse_currency(row[9])

                is_direct = (n_prev and n_prev.lower() != "nan") or (
                    odc and odc.lower() != "nan"
                )

                if is_direct:
                    stats["ore_dirette"] += ore
                else:
                    stats["ore_indirette"] += ore
