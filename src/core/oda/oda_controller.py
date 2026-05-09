"""
SyncroJob - ODA Controller
Logica di business per il caricamento, raggruppamento e processing degli Ordini di Acquisto.
Agnostico rispetto alla GUI.
"""

import logging
from collections import defaultdict
from typing import Any

from src.core.oda_manager import OdaManager
from src.core.utils.formatters import format_date_it

logger = logging.getLogger(__name__)


class ODAController:
    """Servizio per gestire la logica di business dei dati OdA."""

    @staticmethod
    def get_grouped_data(search_text: str = "") -> list[dict[str, Any]]:
        """Recupera i dati dal DB e li raggruppa per numero OdA."""
        raw_data = OdaManager.get_all_oda(search_text)

        # Raggruppamento per numero OdA (indice 2)
        grouped = defaultdict(list)
        for r in raw_data:
            oda_num = str(r[2])
            grouped[oda_num].append(r)

        # Trasformazione in lista strutturata
        structured = []
        for oda_num, positions in grouped.items():
            first = positions[0]
            total_value = float(first[12]) if first[12] else 0.0

            structured.append(
                {
                    "oda": oda_num,
                    "data": format_date_it(first[1]),
                    "creatore": first[15],
                    "descrizione": first[6],
                    "valore_totale": total_value,
                    "stato": first[4],
                    "rilascio": first[24],
                    "positions": positions,
                    "raw_first": first,
                }
            )
        return structured
