from typing import Any

from src.core.database import db_manager
from src.core.logging import get_logger
from src.models import PdlProgrammazioneRecord, PdlRecord

logger = get_logger(__name__)


class PdlRepository:
    """Repository per l'accesso ai dati dei Permessi di Lavoro (PDL)."""

    def __init__(self, db_manager_instance: Any = None) -> None:
        self.db = db_manager_instance or db_manager
        self.columns = [
            "id", "n_pdl", "data_creazione", "area", "unita", "ditta",
            "descrizione_lavoro", "tipologia", "stato", "apparecchiatura",
            "richiedente", "data_richiesta", "emittente", "data_emissione",
            "aprente", "data_apertura", "priorita", "contratto", "ordine",
            "sito", "importato_il"
        ]

    def get_filtered(self, filters: dict[str, Any], sort_col_name: str = "importato_il", sort_order: str = "DESC", as_objects: bool = True) -> list[PdlRecord] | list[tuple[Any, ...]]:
        """Recupera i PDL filtrati e ordinati."""
        query = f"SELECT {', '.join(self.columns)} FROM pdl WHERE 1=1"
        params = []

        search_text = filters.get("search", "")
        site_filter = filters.get("site", "Tutti i siti")
        group_filter = filters.get("group", "Tutti")
        area_filter = filters.get("area", "Tutte")
        unit_filter = filters.get("unit", "Tutte")

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
                "n_pdl", "area", "unita", "ditta", "descrizione_lavoro",
                "tipologia", "stato", "richiedente", "ordine", "sito"
            ]
            or_clause = " OR ".join([f"{col} LIKE ?" for col in search_cols])
            query += f" AND ({or_clause})"
            p = f"%{search_text}%"
            params.extend([p] * len(search_cols))

        # Sorting logic (adapted from original controller)
        if sort_col_name == "n_pdl":
            query += f" ORDER BY CAST(n_pdl AS INTEGER) {sort_order}, n_pdl {sort_order}"
        elif sort_col_name == "data_creazione":
            query += f" ORDER BY substr(data_creazione, 7, 4) || substr(data_creazione, 4, 2) || substr(data_creazione, 1, 2) || substr(data_creazione, 11) {sort_order}"
        else:
            query += f" ORDER BY {sort_col_name} {sort_order}"

        query += " LIMIT 2000"

        try:
            rows = self.db.execute_query(self.db.DB_PDL, query, tuple(params))
            if as_objects:
                # La riga deve corrispondere esattamente alle colonne del record
                return [PdlRecord(**dict(row)) for row in rows]
            return [tuple(row) for row in rows]
        except Exception:
            logger.exception("Errore repository PDL get_filtered")
            return []

    def get_unique_requesters(self) -> list[str]:
        """Restituisce i richiedenti univoci normalizzati."""
        query = "SELECT DISTINCT richiedente FROM pdl WHERE richiedente IS NOT NULL AND richiedente != ''"
        try:
            rows = self.db.execute_query(self.db.DB_PDL, query)
            clean_names = set()
            for r in rows:
                if r[0]:
                    normalized = " ".join(str(r[0]).split()).title()
                    clean_names.add(normalized)
            return sorted(clean_names)
        except Exception:
            return []

    def get_programming_by_week(self, start_date: str, end_date: str) -> list[PdlProgrammazioneRecord]:
        """Recupera la programmazione per una settimana specifica."""
        query = "SELECT * FROM pdl_programmazione WHERE settimana_start = ? AND settimana_end = ? ORDER BY id ASC"
        try:
            rows = self.db.execute_query(self.db.DB_PDL, query, (start_date, end_date))
            return [PdlProgrammazioneRecord(**dict(row)) for row in rows]
        except Exception:
            return []

    def save_programming(self, records: list[PdlProgrammazioneRecord], start_date: str, end_date: str) -> bool:
        """Salva la programmazione settimanale."""
        try:
            # 1. Pulizia settimana esistente
            query_del = "DELETE FROM pdl_programmazione WHERE settimana_start = ? AND settimana_end = ?"
            self.db.execute_query(self.db.DB_PDL, query_del, (start_date, end_date))

            if not records:
                return True

            # 2. Inserimento nuovi record
            # Raccogliamo i campi escludendo ID se None
            fields = [
                "richiedente", "n_pdl", "area", "unita", "descrizione",
                "lun_tcl", "lun_tgo", "mar_tcl", "mar_tgo", "mer_tcl", "mer_tgo",
                "gio_tcl", "gio_tgo", "ven_tcl", "ven_tgo", "sab_tcl", "sab_tgo", "dom_tcl", "dom_tgo",
                "settimana_start", "settimana_end"
            ]
            query = f"""
                INSERT INTO pdl_programmazione ({', '.join(fields)})
                VALUES ({', '.join(['?'] * len(fields))})
            """

            data_to_insert = []
            for r in records:
                data = (
                    r.richiedente, r.n_pdl, r.area, r.unita, r.descrizione,
                    r.lun_tcl, r.lun_tgo, r.mar_tcl, r.mar_tgo, r.mer_tcl, r.mer_tgo,
                    r.gio_tcl, r.gio_tgo, r.ven_tcl, r.ven_tgo, r.sab_tcl, r.sab_tgo, r.dom_tcl, r.dom_tgo,
                    r.settimana_start, r.settimana_end
                )
                data_to_insert.append(data)

            with self.db.get_connection(self.db.DB_PDL) as conn:
                conn.executemany(query, data_to_insert)
            return True
        except Exception:
            logger.exception("Errore repository PDL save_programming")
            return False
