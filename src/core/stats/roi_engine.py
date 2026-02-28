"""
SyncroJob - ROI Engine
Calcola il risparmio di tempo e risorse basandosi sullo storico delle operazioni dei bot.
"""

import logging
from dataclasses import dataclass
from typing import ClassVar

from src.core.database import db_manager

logger = logging.getLogger(__name__)


@dataclass
class ROIMetrics:
    """Modello dati per le metriche di risparmio."""

    total_minutes_saved: float
    total_operations: int
    estimated_cost_saved: float  # In Euro (basato su costo orario medio)
    stress_reduction_score: int  # 1-100


class ROIEngine:
    """Motore per il calcolo del Ritorno sull'Investimento (ROI) delle automazioni."""

    # Pesi: minuti di lavoro manuale stimati per ogni azione riuscita
    MINUTES_PER_ACTION: ClassVar[dict[str, float]] = {
        "Scarico TS": 5.0,
        "Carico TS": 8.0,
        "Dettagli ODA": 3.0,
        "Prenota BP": 10.0,
        "Scarico PDL": 12.0,
        "Ricerca PDL": 2.0,
        "Sincronizzazione": 1.0,
        "Export Excel": 5.0,
    }

    HOURLY_RATE = 25.0  # Costo orario medio aziendale stimato

    @classmethod
    def calculate_savings(cls) -> ROIMetrics:
        """Esegue l'analisi dello storico audit per derivare le metriche di risparmio."""
        try:
            # Recuperiamo le azioni riuscite dall'Audit
            query = "SELECT action, entity FROM audit_logs WHERE timestamp > datetime('now', '-30 days')"
            rows = db_manager.execute_query(db_manager.DB_AUDIT, query)

            total_min = 0.0
            total_ops = 0

            for action, entity in rows:
                # Se l'azione è presente nei pesi, aggiungiamo il risparmio
                for key, minutes in cls.MINUTES_PER_ACTION.items():
                    if key.lower() in str(action).lower() or key.lower() in str(entity).lower():
                        total_min += minutes
                        total_ops += 1
                        break

            # Calcolo metriche derivate
            cost_saved = (total_min / 60.0) * cls.HOURLY_RATE

            # Lo stress reduction è basato sul volume di operazioni noiose automatizzate
            stress_score = min(100, int((total_ops / 500.0) * 100)) if total_ops > 0 else 0

            return ROIMetrics(
                total_minutes_saved=total_min,
                total_operations=total_ops,
                estimated_cost_saved=cost_saved,
                stress_reduction_score=stress_score,
            )
        except Exception as e:
            logger.error(f"Errore calcolo ROI: {e}")
            return ROIMetrics(0, 0, 0, 0)

    @classmethod
    def format_time_saved(cls, minutes: float) -> str:
        """Formatta i minuti in stringa leggibile (ore/minuti)."""
        if minutes < 60:
            return f"{int(minutes)} min"
        hours = int(minutes // 60)
        rem_min = int(minutes % 60)
        return f"{hours}h {rem_min}m"
