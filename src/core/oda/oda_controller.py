"""
SyncroJob - ODA Controller
Logica di business per il caricamento, raggruppamento e processing degli Ordini di Acquisto.
Agnostico rispetto alla GUI.
"""

import logging
from collections import defaultdict
from typing import Any

from src.core.database.repositories import OdaRepository
from src.core.utils.formatters import format_date_it

logger = logging.getLogger(__name__)


class ODAController:
    """Servizio per gestire la logica di business dei dati OdA."""

    def __init__(self) -> None:
        self.repository = OdaRepository()

    def get_grouped_data(self, search_text: str = "") -> list[dict[str, Any]]:
        """Recupera i dati dal DB e li raggruppa per numero OdA."""
        records = self.repository.get_all(search_text, as_objects=True)

        # Raggruppamento per numero OdA
        grouped = defaultdict(list)
        for record in records:
            grouped[record.oda].append(record)

        # Trasformazione in lista strutturata
        structured = []
        for oda_num, positions in grouped.items():
            first = positions[0]

            # Trasformazione in dizionario compatibile con ODAAdapter
            structured.append(
                {
                    "oda": oda_num,
                    "data": format_date_it(first.data_oda),
                    "creatore": first.nome_destinatario,
                    "descrizione": first.descrizione,
                    "valore_totale": first.valore_netto_oda,
                    "stato": first.stato,
                    "rilascio": first.indicatore_rilascio,
                    # Manteniamo le posizioni come tuple per ora per compatibilità con ODAAdapter.create_child_row
                    "positions": [
                        tuple(vars(p).values())[:-1] for p in positions
                    ],  # Rimuoviamo id se presente alla fine
                    "raw_first": tuple(vars(first).values())[:-1],
                }
            )
        return structured
