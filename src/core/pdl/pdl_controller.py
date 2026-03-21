"""
SyncroJob - PDL Controller
Logica di business per il caricamento, filtraggio e processing dei dati PDL SafeWork.
"""

import logging
from typing import Any

from src.core.database import db_manager
from src.core.pdl.pdl_dto import PdlRowDTO

logger = logging.getLogger(__name__)


class PDLController:
    """Controller per la gestione dei dati del database PDL."""

    def __init__(self):
        self._cache: dict[str, list[PdlRowDTO]] = {}

    def get_pdl_data(
        self, filters: dict[str, Any], sort_col: int | None = None, sort_order: str = "DESC"
    ) -> list[PdlRowDTO]:
        """Costruisce la query, interroga il DB e gestisce la cache."""
        query, params = self._build_query(filters, sort_col, sort_order)
        cache_key = f"{query}_{params}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            results = db_manager.execute_query(db_manager.DB_PDL, query, tuple(params))
            dtos = [PdlRowDTO.from_db_row(r) for r in results]
            self._cache[cache_key] = dtos
            return dtos
        except Exception as e:
            logger.error(f"Errore caricamento PDL: {e}")
            return []

    def clear_cache(self):
        """Svuota la cache interna dei risultati."""
        self._cache.clear()

    def _build_query(self, f: dict[str, Any], sort_col: int | None, sort_order: str) -> tuple[str, list[Any]]:
        """Costruisce dinamicamente la query SQL."""
        search_text = f.get("search", "")
        site_filter = f.get("site", "Tutti i siti")
        group_filter = f.get("group", "Tutti")
        area_filter = f.get("area", "Tutte")
        unit_filter = f.get("unit", "Tutte")

        query = "SELECT id, n_pdl, data_creazione, area, unita, ditta, descrizione_lavoro, tipologia, stato, apparecchiatura, richiedente, data_richiesta, emittente, data_emissione, aprente, data_apertura, priorita, contratto, ordine, sito, importato_il FROM pdl WHERE 1=1"
        params = []

        if site_filter != "Tutti i siti":
            query += " AND sito = ?"
            params.append(site_filter)

        if group_filter != "Tutti":
            query += " AND n_pdl LIKE ?"
            params.append(f"%/{group_filter}")

        if area_filter != "Tutte":
            query += " AND area = ?"
            params.append(area_filter)

        if unit_filter != "Tutte":
            query += " AND unita = ?"
            params.append(unit_filter)

        if search_text:
            search_cols = [
                "n_pdl",
                "area",
                "unita",
                "ditta",
                "descrizione_lavoro",
                "tipologia",
                "stato",
                "richiedente",
                "ordine",
                "sito",
            ]
            OR_clause = " OR ".join([f"{col} LIKE ?" for col in search_cols])
            query += f" AND ({OR_clause})"
            p = f"%{search_text}%"
            params.extend([p] * len(search_cols))

        order_map = {
            0: "data_creazione",
            1: "richiedente",
            2: "n_pdl",
            3: "area",
            4: "unita",
            5: "stato",
            6: "descrizione_lavoro",
        }
        if sort_col is not None and sort_col in order_map:
            col_name = order_map[sort_col]
            if col_name == "n_pdl":
                order_clause = f" ORDER BY CAST(n_pdl AS INTEGER) {sort_order}, n_pdl {sort_order}"
            elif col_name == "data_creazione":
                order_clause = f" ORDER BY substr(data_creazione, 7, 4) || substr(data_creazione, 4, 2) || substr(data_creazione, 1, 2) || substr(data_creazione, 11) {sort_order}"
            else:
                order_clause = f" ORDER BY {col_name} {sort_order}"
        else:
            order_clause = " ORDER BY importato_il DESC"

        query += order_clause
        query += " LIMIT 2000"
        return query, params

    @staticmethod
    def process_master_rows(full_rows: list[PdlRowDTO]) -> list[list[Any]]:
        """Formatta le righe per la visualizzazione nella tabella master."""
        return [r.to_master_list() for r in full_rows]
