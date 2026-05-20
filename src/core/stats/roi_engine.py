"""
SyncroJob - ROI Engine
Calcola il risparmio di tempo e risorse basando l'analisi sui log di auditing.
"""

import logging
import operator
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from src.core.config_manager import get_config_value
from src.core.database import db_manager
from src.core.schemas import ROIMetrics

__all__ = ["ROIEngine", "ROIMetrics"]

logger = logging.getLogger(__name__)


class ROIEngine:
    """
    Motore analitico per la misurazione del Ritorno sull'Investimento (ROI).
    Analizza i log di auditing per stimare il tempo risparmiato dall'automazione.
    """

    DEFAULT_MINUTES = 5.0
    MINUTES_IN_HOUR = 60
    HOURS_IN_DAY = 8

    @staticmethod
    def get_weights() -> dict[str, float]:
        """Recupera i pesi (minuti risparmiati per operazione) dalla configurazione."""

        default_weights = {
            "Scarico TS": 15.0,
            "Carico TS": 5.0,
            "Dettagli ODA": 20.0,
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

            # Stato accumulatori
            state: dict[str, Any] = {
                "total_min_man": 0.0,
                "total_bot_min": 0.0,
                "total_ops": 0,
                "success_cnt": 0,
                "fail_count": 0,
                "critical_errs": 0,
                "curr_30d_ops": 0,
                "prev_30d_ops": 0,
                "task_counts": {},
            }

            now = datetime.now(UTC)
            dates = {"thirty": now - timedelta(days=30), "sixty": now - timedelta(days=60)}

            for row in rows:
                cls._process_audit_row(row, state, weights, task_aliases, dates)

            return cls._finalize_metrics(
                float(state["total_min_man"]),
                float(state["total_bot_min"]),
                int(state["total_ops"]),
                int(state["success_cnt"]),
                int(state["fail_count"]),
                int(state["critical_errs"]),
                int(state["curr_30d_ops"]),
                int(state["prev_30d_ops"]),
                cast("dict[str, int]", state["task_counts"]),
                rows,
            )
        except Exception:
            logger.exception("Errore critico calcolo ROI")
            return ROIMetrics(0, 0, 0, 0, 0, 0, 0.0, "Nessuno", 0.0, [])

    @classmethod
    def _process_audit_row(
        cls,
        row: Any,
        state: dict[str, Any],
        weights: dict[str, float],
        task_aliases: dict[str, list[str]],
        dates: dict[str, datetime],
    ) -> None:
        """Processa una singola riga di log aggiornando lo stato ROI."""
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
                    state["fail_count"] += 1
                    if severity == "critical":
                        state["critical_errs"] += 1
                return

            state["success_cnt"] += 1
            search_text = entity.lower() if entity and entity != "-" else action.lower()
            matched_task = cls._match_task(search_text, task_aliases)

            if matched_task:
                state["total_min_man"] += float(weights.get(matched_task, cls.DEFAULT_MINUTES))
                state["total_bot_min"] += dur_ms / 60000.0
                state["total_ops"] += 1
                state["task_counts"][matched_task] = state["task_counts"].get(matched_task, 0) + 1

                row_date = cls._parse_timestamp(ts_str)
                if row_date:
                    if row_date >= dates["thirty"]:
                        state["curr_30d_ops"] += 1
                    elif row_date >= dates["sixty"]:
                        state["prev_30d_ops"] += 1
        except (IndexError, ValueError):
            logger.exception("ROIEngine: Errore processamento riga %s", row)
        except Exception:
            logger.exception("ROIEngine: Errore imprevisto riga")

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
    ) -> ROIMetrics:
        total_days = cls._calculate_total_days(rows)
        total_attempts = success_cnt + fail_count
        success_rate = (success_cnt / total_attempts * 100) if total_attempts > 0 else 0.0
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
        if not task_counts or total_ops <= 0:
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
