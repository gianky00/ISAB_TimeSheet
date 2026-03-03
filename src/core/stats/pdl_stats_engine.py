"""
SyncroJob - PDL Stats Engine
Calcola le metriche e i trend per i Permessi di Lavoro (PDL).
V7.0: Aggiunta Trend Settimanale (Week-over-Week).
"""

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

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

    DB_PATH = "C:/Users/Coemi/AppData/Local/SyncroJob/data/pdl.db"

    @classmethod
    def get_metrics(cls) -> PDLMetrics:
        """Calcola e restituisce le metriche complete per la dashboard."""
        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()

            # 1. Conteggio Totale
            cursor.execute("SELECT COUNT(*) FROM pdl")
            total = cursor.fetchone()[0]

            # 2. Conteggio Attivi
            active_q = """
                SELECT COUNT(*) FROM pdl
                WHERE stato LIKE 'Aperto%'
                   OR stato LIKE 'Emesso%'
                   OR stato LIKE 'Richiesto%'
                   OR stato LIKE 'Accettato%'
            """
            cursor.execute(active_q)
            active = cursor.fetchone()[0]

            # 3. Parametri temporali
            now = datetime.now()
            today_day = now.day
            month_curr_str = now.strftime("/%m/%Y")

            first_day_curr = now.replace(day=1)
            last_day_prev = first_day_curr - timedelta(days=1)
            month_prev_str = last_day_prev.strftime("/%m/%Y")

            # Date per Trend Settimanale (Rolling)
            seven_days_ago = now - timedelta(days=7)
            fourteen_days_ago = now - timedelta(days=14)

            # 4. Recupero dati per Trend e Aree
            # Prendiamo i dati degli ultimi due mesi per coprire MTD e Weekly
            cursor.execute(
                "SELECT area, data_creazione FROM pdl WHERE sito LIKE '%ISAB Sud%' "
                "AND (data_creazione LIKE ? OR data_creazione LIKE ?)",
                (f"%{month_curr_str}%", f"%{month_prev_str}%"),
            )
            rows = cursor.fetchall()

            stats_map = {}
            current_mtd_global = 0
            prev_mtd_global = 0
            
            last_7d_count = 0
            prev_7d_count = 0

            for area, date_str in rows:
                try:
                    # Parsing data_creazione "DD/MM/YYYY HH:MM:SS"
                    dt_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                    day_part = dt_obj.day
                    
                    # --- Logica MTD (per aree e globale) ---
                    if not area: continue
                    if area not in stats_map:
                        stats_map[area] = {"curr": 0, "prev": 0}

                    if dt_obj.month == now.month and dt_obj.year == now.year:
                        if day_part <= today_day:
                            stats_map[area]["curr"] += 1
                            current_mtd_global += 1
                    elif dt_obj.month == last_day_prev.month and dt_obj.year == last_day_prev.year:
                        if day_part <= today_day:
                            stats_map[area]["prev"] += 1
                            prev_mtd_global += 1
                    
                    # --- Logica Weekly (Rolling 7d vs Prev 7d) ---
                    if dt_obj >= seven_days_ago:
                        last_7d_count += 1
                    elif dt_obj >= fourteen_days_ago:
                        prev_7d_count += 1

                except (ValueError, IndexError):
                    continue

            # 5. Elaborazione Trend
            # Trend Mensile MTD
            global_trend = (current_mtd_global - prev_mtd_global) / prev_mtd_global * 100 if prev_mtd_global > 0 else 100.0 if current_mtd_global > 0 else 0.0
            
            # Trend Settimanale WoW
            weekly_trend = (last_7d_count - prev_7d_count) / prev_7d_count * 100 if prev_7d_count > 0 else 100.0 if last_7d_count > 0 else 0.0

            # 6. Elaborazione Aree
            areas_stats_list = []
            for area_name, counts in stats_map.items():
                curr = counts["curr"]
                prev = counts["prev"]
                area_trend = (curr - prev) / prev * 100 if prev > 0 else 100.0 if curr > 0 else 0.0
                areas_stats_list.append(AreaStats(area_name, curr, round(area_trend, 1)))

            areas_stats_list.sort(key=lambda x: x.name)

            # 7. Ultimo Sync
            try:
                from src.core.sync_tracker import SyncTracker
                last_sync = SyncTracker.get_formatted_status("pdl")
            except ImportError:
                last_sync = "--"

            conn.close()

            return PDLMetrics(
                total_count=total,
                active_count=active,
                closed_count=total - active,
                trend_percentage=round(global_trend, 1),
                weekly_trend_percentage=round(weekly_trend, 1),
                areas_stats=areas_stats_list,
                last_sync=last_sync,
            )

        except Exception as e:
            logger.error(f"Errore calcolo PDL Stats WoW: {e}")
            return PDLMetrics(0, 0, 0, 0.0, 0.0, [], "--")
