"""
SyncroJob - ROI Engine
Calcola il risparmio di tempo e risorse basandosi sullo storico delle operazioni dei bot.
"""

import logging
import operator
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Final, cast

from src.core.config_manager import get_config_value
from src.core.database import db_manager

logger = logging.getLogger(__name__)


@dataclass
class ROIMetrics:
    """Modello dati per le metriche di risparmio."""

    total_minutes_saved: float  # Tempo manuale stimato
    net_minutes_saved: float  # Risparmio reale (Manuale - Bot)
    total_operations: int
    success_rate: float  # Percentuale di successo (0-100)
    reliability_score: int  # Affidabilità del sistema (0-100)
    total_days: int  # Giorni totali di storico
    trend_percentage: float  # Variazione % rispetto al mese precedente
    top_task_name: str  # Nome del task più eseguito (mantenuto per compatibilità)
    top_task_pct: float  # Percentuale del top task sul totale (mantenuto per compatibilità)
    top_tasks: list[tuple[str, float]]  # Top 3 task: [(nome, percentuale), ...]


class ROIEngine:
    """Motore per il calcolo del Ritorno sull'Investimento (ROI) delle automazioni."""

    DEFAULT_MINUTES: Final[float] = 5.0
    MINUTES_IN_HOUR: Final[int] = 60
    MINUTES_IN_DAY: Final[int] = 1440
    HOURS_IN_DAY: Final[int] = 24

    @classmethod
    def get_weights(cls) -> dict[str, float]:
        """Recupera i pesi (minuti manuali) dalla configurazione."""
        default_weights = {
            "Scarico TS": 5.0,
            "Carico TS": 8.0,
            "Dettagli ODA": 3.0,
            "Prenota BP": 10.0,
            "Scarico PDL": 12.0,
            "Ricerca PDL": 2.0,
            "Sincronizzazione": 1.0,
            "Export Excel": 5.0,
        }

        return cast("dict[str, float]", get_config_value("roi_weights", default_weights))

    @classmethod
    def calculate_savings(cls) -> ROIMetrics:
        """Esegue l'analisi dello storico audit per derivare le metriche di risparmio."""
        try:
            weights = cls.get_weights()
            task_aliases = cls._get_task_aliases()

            query = "SELECT action, entity, status, severity, timestamp, duration_ms, category FROM audit_logs ORDER BY timestamp ASC"
            rows = db_manager.execute_query(db_manager.DB_AUDIT, query)

            if not rows:
                logger.warning("ROIEngine: Nessun log di audit trovato.")
                return ROIMetrics(0, 0, 0, 0, 0, 0, 0.0, "Nessuno", 0.0, [])

            total_min_man, total_bot_min, total_ops, success_cnt, fail_count, critical_errs = (
                0.0,
                0.0,
                0,
                0,
                0,
                0,
            )
            curr_30d_ops, prev_30d_ops = 0, 0
            task_counts: dict[str, int] = {}

            now = datetime.now().astimezone()
            thirty_days_ago = now - timedelta(days=30)
            sixty_days_ago = now - timedelta(days=60)

            for row in rows:
                try:
                    action, entity, status, severity, ts_str, dur_ms = (
                        str(row[0]),
                        str(row[1]),
                        str(row[2]).lower(),
                        str(row[3]).lower(),
                        str(row[4]),
                        row[5] or 0,
                    )
                    is_success = status == "success"

                    if not is_success or "Completamento" not in action:
                        if not is_success:
                            fail_count += 1
                            if severity == "critical":
                                critical_errs += 1
                        continue

                    success_cnt += 1
                    search_text = entity.lower() if entity and entity != "-" else action.lower()
                    matched_task = cls._match_task(search_text, task_aliases)

                    if matched_task:
                        total_min_man += float(weights.get(matched_task, cls.DEFAULT_MINUTES))
                        total_bot_min += dur_ms / 60000.0
                        total_ops += 1
                        task_counts[matched_task] = task_counts.get(matched_task, 0) + 1
                        row_date = cls._parse_timestamp(ts_str)
                        if row_date:
                            if row_date >= thirty_days_ago:
                                curr_30d_ops += 1
                            elif row_date >= sixty_days_ago:
                                prev_30d_ops += 1
                except (IndexError, ValueError):
                    logger.exception("ROIEngine: Errore processamento riga %s", row)
                    continue

            return cls._finalize_metrics(
                total_min_man,
                total_bot_min,
                total_ops,
                success_cnt,
                fail_count,
                critical_errs,
                curr_30d_ops,
                prev_30d_ops,
                task_counts,
                rows,
            )
        except Exception:
            logger.exception("Errore critico calcolo ROI")
            return ROIMetrics(0, 0, 0, 0, 0, 0, 0.0, "Nessuno", 0.0, [])

    @staticmethod
    def _get_task_aliases() -> dict[str, list[str]]:
        return {
            "Scarico TS": [
                "scarico ts",
                "scarico timesheet",
                "download ts",
                "download timesheet",
                "scarico ore",
            ],
            "Carico TS": ["carico ts", "carico timesheet", "upload ts", "upload timesheet", "carico ore"],
            "Dettagli ODA": ["dettagli oda", "scarico oda", "analisi oda", "importazione oda"],
            "Prenota BP": ["prenota bp", "prenotazione bp", "creazione bp"],
            "Scarico PDL": ["scarico pdl", "download pdl", "esportazione pdl"],
            "Ricerca PDL": ["ricerca pdl", "search pdl", "query pdl"],
            "Sincronizzazione": ["sincronizzazione", "sync", "allineamento database"],
            "Export Excel": ["export excel", "esportazione excel", "generazione report"],
        }

    @classmethod
    def _finalize_metrics(  # noqa: PLR0913
        cls,
        total_min_man: float,
        total_bot_min: float,
        total_ops: int,
        success_cnt: int,
        fail_count: int,
        critical_errs: int,
        curr_30d_ops: int,
        prev_30d_ops: int,
        task_counts: dict[str, int],
        rows: list[Any],
    ) -> ROIMetrics:  # noqa: PLR0913, RUF100
        total_days = cls._calculate_total_days(rows)
        success_rate = (
            (success_cnt / (success_cnt + fail_count) * 100) if (success_cnt + fail_count) > 0 else 0
        )
        reliability = max(0, min(100, 100 - (critical_errs * 5)))
        trend_percentage = cls._calculate_trend(curr_30d_ops, prev_30d_ops)
        top_tasks_list = cls._get_top_tasks(task_counts, total_ops)

        return ROIMetrics(
            total_minutes_saved=total_min_man,
            net_minutes_saved=max(0.0, total_min_man - total_bot_min),
            total_operations=total_ops,
            success_rate=round(success_rate, 1),
            reliability_score=reliability,
            total_days=total_days,
            trend_percentage=round(trend_percentage, 1),
            top_task_name=top_tasks_list[0][0] if top_tasks_list else "Nessuno",
            top_task_pct=top_tasks_list[0][1] if top_tasks_list else 0.0,
            top_tasks=top_tasks_list,
        )

    @staticmethod
    def _match_task(search_text: str, task_aliases: dict[str, list[str]]) -> str | None:
        """Mappa il testo della ricerca a un task ROI."""
        for weight_key, aliases in task_aliases.items():
            if any(alias in search_text for alias in aliases):
                return weight_key
        if "timbrature" in search_text:
            return "Scarico TS"
        return None

    @staticmethod
    def _parse_timestamp(ts_str: str) -> datetime | None:
        """Parsa una stringa timestamp in datetime aware."""
        with suppress(Exception):
            return datetime.fromisoformat(ts_str.split(".")[0].replace(" ", "T")).astimezone()
        return None

    @staticmethod
    def _calculate_total_days(rows: list[Any]) -> int:
        """Calcola i giorni totali coperti dai log."""
        try:
            first_ts = str(rows[0][4])
            last_ts = str(rows[-1][4])
            d1 = datetime.fromisoformat(first_ts.split(".")[0].replace(" ", "T"))
            d2 = datetime.fromisoformat(last_ts.split(".")[0].replace(" ", "T"))
            return max(1, (d2 - d1).days)
        except Exception:
            return 1

    @staticmethod
    def _calculate_trend(current: int, previous: int) -> float:
        """Calcola la variazione percentuale."""
        if previous > 0:
            return ((current - previous) / previous) * 100.0
        return 100.0 if current > 0 else 0.0

    @staticmethod
    def _get_top_tasks(task_counts: dict[str, int], total_ops: int) -> list[tuple[str, float]]:
        """Restituisce i top 3 task per frequenza."""
        if not task_counts:
            return []
        sorted_tasks = sorted(task_counts.items(), key=operator.itemgetter(1), reverse=True)
        return [(name, round((count / total_ops) * 100, 1)) for name, count in sorted_tasks[:3]]

    @classmethod
    def format_time_saved(cls, minutes: float) -> str:
        """Formatta i minuti in stringa leggibile (ore/minuti)."""
        if minutes < cls.MINUTES_IN_HOUR:
            return f"{int(minutes)} min"
        hours = int(minutes // cls.MINUTES_IN_HOUR)
        rem_min = int(minutes % cls.MINUTES_IN_HOUR)

        if hours > cls.HOURS_IN_DAY:
            days = hours // cls.HOURS_IN_DAY
            rem_hours = hours % cls.HOURS_IN_DAY
            return f"{days}g {rem_hours}h"

        return f"{hours}h {rem_min}m"
