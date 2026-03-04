"""
SyncroJob - PDL Stats Engine
Calcola le metriche e i trend per i Permessi di Lavoro (PDL).
V7.0: Aggiunta Trend Settimanale (Week-over-Week).
"""

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

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

    @classmethod
    def get_metrics(cls) -> PDLMetrics:
        """Calcola e restituisce le metriche complete per la dashboard."""
        try:
            # Usiamo DatabaseManager per ottenere il percorso corretto
            db_path = db_manager.DB_PDL
            conn = sqlite3.connect(db_path)
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
            now = datetime.now().astimezone()
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
                    dt_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S").astimezone()
                    day_part = dt_obj.day

                    # --- Logica MTD (per aree e globale) ---
                    if not area:
                        continue
                    if area not in stats_map:
                        stats_map[area] = {"curr": 0, "prev": 0}

                    if dt_obj.month == now.month and dt_obj.year == now.year and day_part <= today_day:
                        stats_map[area]["curr"] += 1
                        current_mtd_global += 1
                    elif dt_obj.month == last_day_prev.month and dt_obj.year == last_day_prev.year and day_part <= today_day:
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

            # 6. Elaborazione Aree (Filtrate e Ordinate come da specifica)
            # Mapping tra Nome Visualizzato e Nome nel Database
            DISPLAY_TO_DB = {
                "Area 1": "Process Area 1",
                "Area 2": "Process Area 2",
                "Area 3": "Process Area 3",
                "Blending Sud": "Blending Sud",
                "Pontile Sud": "Pontile Sud",
                "UTILITIES (CTE/TAS)": "UTILITIES (CTE/TAS)"
            }

            areas_stats_list = []
            for display_name, db_name in DISPLAY_TO_DB.items():
                if db_name in stats_map:
                    counts = stats_map[db_name]
                    curr = counts["curr"]
                    prev = counts["prev"]
                    area_trend = (curr - prev) / prev * 100 if prev > 0 else 100.0 if curr > 0 else 0.0
                    areas_stats_list.append(AreaStats(display_name, curr, round(area_trend, 1)))
                else:
                    # Se un'area non ha dati nel periodo, la aggiungiamo comunque a 0 per mantenere l'ordine
                    areas_stats_list.append(AreaStats(display_name, 0, 0.0))

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
