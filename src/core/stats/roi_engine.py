"""
SyncroJob - ROI Engine
Calcola il risparmio di tempo e risorse basandosi sullo storico delle operazioni dei bot.
"""

import logging
import operator
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime, timedelta

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
        from typing import cast  # noqa: PLC0415

        return cast("dict[str, float]", get_config_value("roi_weights", default_weights))

    @classmethod
    def calculate_savings(cls) -> ROIMetrics:  # noqa: PLR0912, PLR0915
        """Esegue l'analisi dello storico audit per derivare le metriche di risparmio."""
        try:
            # Carichiamo i pesi dinamici
            weights = cls.get_weights()

            # Alias per il mapping flessibile delle azioni audit ai pesi ROI
            task_aliases = {
                "Scarico TS": [
                    "scarico ts",
                    "scarico timesheet",
                    "download ts",
                    "download timesheet",
                    "scarico ore",
                ],
                "Carico TS": ["carico ts", "carico timesheet", "upload ts", "upload timesheet", "carico ore"],
                "Dettagli ODA": [
                    "dettagli oda",
                    "scarico oda",
                    "analisi oda",
                    "importazione oda",
                    "dettagli oda",
                ],
                "Prenota BP": ["prenota bp", "prenotazione bp", "creazione bp"],
                "Scarico PDL": ["scarico pdl", "download pdl", "esportazione pdl"],
                "Ricerca PDL": ["ricerca pdl", "search pdl", "query pdl"],
                "Sincronizzazione": ["sincronizzazione", "sync", "allineamento database"],
                "Export Excel": ["export excel", "esportazione excel", "generazione report"],
            }

            # Recuperiamo TUTTE le azioni dall'Audit includendo la durata reale
            # Ordine esplicito delle colonne per evitare errori di unpacking
            query = "SELECT action, entity, status, severity, timestamp, duration_ms, category FROM audit_logs ORDER BY timestamp ASC"
            rows = db_manager.execute_query(db_manager.DB_AUDIT, query)

            if not rows:
                logger.warning("ROIEngine: Nessun log di audit trovato.")
                return ROIMetrics(0, 0, 0, 0, 0, 0, 0.0, "Nessuno", 0.0, [])

            total_min_manual = 0.0
            total_bot_min = 0.0
            total_ops = 0
            success_count = 0
            fail_count = 0
            critical_errors = 0

            # Variabili per Trend e Top Task
            current_30d_ops = 0
            prev_30d_ops = 0
            task_counts: dict[str, int] = {}

            # Calcolo giorni totali e reference date per il trend
            now = datetime.now().astimezone()
            thirty_days_ago = now - timedelta(days=30)
            sixty_days_ago = now - timedelta(days=60)

            for row in rows:
                try:
                    # Estrazione sicura per indice (action, entity, status, severity, timestamp, duration_ms, category)
                    action = str(row[0])
                    entity = str(row[1])
                    status = str(row[2]).lower()
                    severity = str(row[3]).lower()
                    ts_str = str(row[4])
                    dur_ms = row[5] or 0

                    is_success = status == "success"

                    # Consideriamo solo il completamento per non duplicare i minuti (avvio + fine)
                    # Supportiamo sia il nome esatto che varianti
                    if not is_success or "Completamento" not in action:
                        if not is_success:
                            fail_count += 1
                            if severity == "critical":
                                critical_errors += 1
                        continue

                    success_count += 1
                    # Testo di ricerca: preferiamo l'entità, poi l'azione
                    search_text = entity.lower() if entity and entity != "-" else action.lower()

                    # Logica di mapping flessibile
                    matched_task = None
                    for weight_key, aliases in task_aliases.items():
                        if any(alias in search_text for alias in aliases):
                            matched_task = weight_key
                            break

                    # Caso speciale: "Timbrature" nel log deve mappare a un peso ROI (es. Scarico TS)
                    if not matched_task and "timbrature" in search_text:
                        matched_task = "Scarico TS"

                    if matched_task:
                        minutes = float(weights.get(matched_task, 5.0))
                        total_min_manual += minutes

                        # Aggiungiamo la durata reale del bot (ms -> min)
                        bot_dur_min = (dur_ms) / 60000.0
                        total_bot_min += bot_dur_min

                        total_ops += 1
                        task_counts[matched_task] = task_counts.get(matched_task, 0) + 1

                        # Calcolo del trend a 30 e 60 giorni
                        row_date = None
                        with suppress(Exception):
                            row_date = datetime.fromisoformat(
                                ts_str.split(".")[0].replace(" ", "T")
                            ).astimezone()

                        if row_date:
                            if row_date >= thirty_days_ago:
                                current_30d_ops += 1
                            elif row_date >= sixty_days_ago:
                                prev_30d_ops += 1
                except (IndexError, ValueError) as row_err:
                    logger.error(f"ROIEngine: Errore processamento riga {row}: {row_err}")  # noqa: TRY400
                    continue

            # Calcolo giorni totali dallo storico reale
            total_days = 1
            if rows:
                try:
                    first_ts = str(rows[0][4])
                    last_ts = str(rows[-1][4])
                    d1 = datetime.fromisoformat(first_ts.split(".")[0].replace(" ", "T"))
                    d2 = datetime.fromisoformat(last_ts.split(".")[0].replace(" ", "T"))
                    total_days = max(1, (d2 - d1).days)
                except Exception:
                    total_days = 1

            # Calcolo metriche derivate
            total_actions = success_count + fail_count
            success_rate = (success_count / total_actions * 100) if total_actions > 0 else 0

            # Affidabilità: 100% meno penalità per errori critici
            reliability = 100 - (critical_errors * 5)
            reliability = max(0, min(100, reliability))

            # Trend calculation
            if prev_30d_ops > 0:
                trend_percentage = ((current_30d_ops - prev_30d_ops) / prev_30d_ops) * 100.0
            else:
                trend_percentage = 100.0 if current_30d_ops > 0 else 0.0

            # Risparmio Netto
            net_min = max(0.0, total_min_manual - total_bot_min)

            # Top Tasks calculation (Top 3)
            top_tasks_list = []
            top_task_name = "Nessuno"
            top_task_pct = 0.0

            if task_counts:
                # Ordina per numero di esecuzioni decrescente
                sorted_tasks = sorted(task_counts.items(), key=operator.itemgetter(1), reverse=True)

                for name, count in sorted_tasks[:3]:
                    pct = (count / total_ops) * 100 if total_ops > 0 else 0.0
                    top_tasks_list.append((name, round(pct, 1)))

                if top_tasks_list:
                    top_task_name = top_tasks_list[0][0]
                    top_task_pct = top_tasks_list[0][1]

            return ROIMetrics(
                total_minutes_saved=total_min_manual,
                net_minutes_saved=net_min,
                total_operations=total_ops,
                success_rate=round(success_rate, 1),
                reliability_score=reliability,
                total_days=total_days,
                trend_percentage=round(trend_percentage, 1),
                top_task_name=top_task_name,
                top_task_pct=top_task_pct,
                top_tasks=top_tasks_list,
            )
        except Exception as e:
            logger.error(f"Errore critico calcolo ROI: {e}", exc_info=True)
            return ROIMetrics(0, 0, 0, 0, 0, 0, 0.0, "Nessuno", 0.0, [])

    @classmethod
    def format_time_saved(cls, minutes: float) -> str:
        """Formatta i minuti in stringa leggibile (ore/minuti)."""
        if minutes < 60:  # noqa: PLR2004
            return f"{int(minutes)} min"
        hours = int(minutes // 60)
        rem_min = int(minutes % 60)

        if hours > 24:  # noqa: PLR2004
            days = hours // 24
            rem_hours = hours % 24
            return f"{days}g {rem_hours}h"

        return f"{hours}h {rem_min}m"
