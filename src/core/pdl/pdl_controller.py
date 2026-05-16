"""
SyncroJob - PDL Controller
Logica di business per il caricamento, filtraggio e processing dei dati PDL SafeWork.
"""

import logging
from typing import Any

from src.core.database.repositories import PdlRepository
from src.core.pdl.pdl_dto import PdlRowDTO

logger = logging.getLogger(__name__)


class PDLController:
    """Controller per la gestione dei dati del database PDL."""

    def __init__(self) -> None:
        self.repository = PdlRepository()
        self._cache: dict[str, list[PdlRowDTO]] = {}

    def get_pdl_data(
        self, filters: dict[str, Any], sort_col: int | None = None, sort_order: str = "DESC"
    ) -> list[PdlRowDTO]:
        """Recupera i dati tramite repository e gestisce la cache."""
        # Mappatura indici colonne GUI -> Nomi colonne DB
        order_map: dict[int, str] = {
            0: "data_creazione",
            1: "richiedente",
            2: "n_pdl",
            3: "area",
            4: "unita",
            5: "stato",
            6: "descrizione_lavoro",
        }

        sort_col_name = "importato_il"
        if sort_col is not None and sort_col in order_map:
            sort_col_name = order_map[sort_col]

        cache_key = f"{filters}_{sort_col_name}_{sort_order}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            records = self.repository.get_filtered(filters, sort_col_name, sort_order, as_objects=True)
            # Convertiamo i modelli in DTO
            dtos = [PdlRowDTO.from_model(r) for r in records]
            self._cache[cache_key] = dtos
        except Exception:
            logger.exception("Errore caricamento PDL tramite repository")
            return []
        else:
            return dtos

    def clear_cache(self) -> None:
        """Svuota la cache interna dei risultati."""
        self._cache.clear()

    @staticmethod
    def process_master_rows(full_rows: list[PdlRowDTO]) -> list[list[Any]]:
        """Formatta le righe per la visualizzazione nella tabella master."""
        return [r.to_master_list() for r in full_rows]
