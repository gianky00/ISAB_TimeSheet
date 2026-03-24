"""
SyncroJob - PDL Stats Engine
Calcola le metriche e i trend per i Permessi di Lavoro (PDL).
V7.0: Aggiunta Trend Settimanale (Week-over-Week).
"""

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final

from src.core.database.manager import db_manager

logger = logging.getLogger(__name__)


@dataclass
class AreaStats:
    """Statistiche specifiche per una singola area."""

    name: str
    current_count: int
    trend_percentage: float


@dataclass
class PDLMetrics:
    """Modello dati per le metriche dei PDL."""

    total_count: int
    active_count: int
    closed_count: int
    trend_percentage: float
    weekly_trend_percentage: float  # Trend ultimi 7gg vs 7gg precedenti
    areas_stats: list[AreaStats]
    last_sync: str


class PDLStatsEngine:
    """Motore per l'analisi statistica dei PDL nel database locale."""

    DISPLAY_TO_DB: Final[dict[str, str]] = {
        "Area 1": "Process Area 1",
        "Area 2": "Process Area 2",
        "Area 3": "Process Area 3",
        "Blending Sud": "Blending Sud",
        "Pontile Sud": "Pontile Sud",
        "UTILITIES (CTE/TAS)": "UTILITIES (CTE/TAS)",
    }

    DAYS_IN_WEEK = 7
    DAYS_IN_FORTNIGHT = 14

    @classmethod
    def get_metrics(cls) -> PDLMetrics:
        """Calcola e restituisce le metriche complete per la dashboard."""
        try:
            db_path = db_manager.DB_PDL
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                total, active = cls._get_counts(cursor)

                rows = cls._fetch_raw_pdl_data(cursor)
                current_mtd, prev_mtd, last_7d, prev_7d, stats_map = cls._process_pdl_rows(rows)

                global_trend = cls._calculate_percentage_change(current_mtd, prev_mtd)
                weekly_trend = cls._calculate_percentage_change(last_7d, prev_7d)

                areas_stats_list = cls._get_area_stats(stats_map)

                from src.core.sync_tracker import SyncTracker  # noqa: PLC0415

                last_sync = SyncTracker.get_formatted_status("pdl")

                return PDLMetrics(
                    total_count=total,
                    active_count=active,
                    closed_count=total - active,
                    trend_percentage=round(global_trend, 1),
                    weekly_trend_percentage=round(weekly_trend, 1),
                    areas_stats=areas_stats_list,
                    last_sync=last_sync,
                )

        except Exception:
            logger.exception("Errore calcolo PDL Stats")
            return PDLMetrics(0, 0, 0, 0.0, 0.0, [], "--")

    @staticmethod
    def _get_counts(cursor: sqlite3.Cursor) -> tuple[int, int]:
        """Recupera i conteggi totali e attivi."""
        cursor.execute("SELECT COUNT(*) FROM pdl")
        total: int = cursor.fetchone()[0]

        active_q = """
            SELECT COUNT(*) FROM pdl
            WHERE stato LIKE 'Aperto%'
               OR stato LIKE 'Emesso%'
               OR stato LIKE 'Richiesto%'
               OR stato LIKE 'Accettato%'
        """
        cursor.execute(active_q)
        active: int = cursor.fetchone()[0]
        return total, active

    @staticmethod
    def _fetch_raw_pdl_data(cursor: sqlite3.Cursor) -> list[tuple[str, str]]:
        """Recupera le righe grezze per l'analisi dei trend."""
        now = datetime.now().astimezone()
        month_curr_str = now.strftime("/%m/%Y")
        last_day_prev = now.replace(day=1) - timedelta(days=1)
        month_prev_str = last_day_prev.strftime("/%m/%Y")

        cursor.execute(
            "SELECT area, data_creazione FROM pdl WHERE sito LIKE '%ISAB Sud%' "
            "AND (data_creazione LIKE ? OR data_creazione LIKE ?)",
            (f"%{month_curr_str}%", f"%{month_prev_str}%"),
        )
        return cursor.fetchall()

    @classmethod
    def _process_pdl_rows(
        cls, rows: list[tuple[str, str]]
    ) -> tuple[int, int, int, int, dict[str, dict[str, int]]]:
        """Processa le righe per calcolare i trend MTD e WoW."""
        now = datetime.now().astimezone()
        last_day_prev = now.replace(day=1) - timedelta(days=1)
        seven_days_ago = now - timedelta(days=cls.DAYS_IN_WEEK)
        fourteen_days_ago = now - timedelta(days=cls.DAYS_IN_FORTNIGHT)

        stats_map: dict[str, dict[str, int]] = {}
        curr_mtd, prev_mtd, last_7d, prev_7d = 0, 0, 0, 0

        for area, date_str in rows:
            try:
                dt_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S").astimezone()
                if area:
                    if area not in stats_map:
                        stats_map[area] = {"curr": 0, "prev": 0}
                    if dt_obj.month == now.month and dt_obj.year == now.year and dt_obj.day <= now.day:
                        stats_map[area]["curr"] += 1
                        curr_mtd += 1
                    elif (
                        dt_obj.month == last_day_prev.month
                        and dt_obj.year == last_day_prev.year
                        and dt_obj.day <= now.day
                    ):
                        stats_map[area]["prev"] += 1
                        prev_mtd += 1
                if dt_obj >= seven_days_ago:
                    last_7d += 1
                elif dt_obj >= fourteen_days_ago:
                    prev_7d += 1
            except (ValueError, IndexError):
                continue
        return curr_mtd, prev_mtd, last_7d, prev_7d, stats_map

    @classmethod
    def _get_area_stats(cls, stats_map: dict[str, dict[str, int]]) -> list[AreaStats]:
        """Formatta le statistiche per area."""
        areas_stats_list = []
        for display_name, db_name in cls.DISPLAY_TO_DB.items():
            curr, prev = 0, 0
            if db_name in stats_map:
                curr = stats_map[db_name]["curr"]
                prev = stats_map[db_name]["prev"]
            area_trend = cls._calculate_percentage_change(curr, prev)
            areas_stats_list.append(AreaStats(display_name, curr, round(area_trend, 1)))
        return areas_stats_list

    @staticmethod
    def _calculate_percentage_change(current: int, previous: int) -> float:
        """Calcola la variazione percentuale tra due valori."""
        if previous > 0:
            return ((current - previous) / previous) * 100.0
        return 100.0 if current > 0 else 0.0
