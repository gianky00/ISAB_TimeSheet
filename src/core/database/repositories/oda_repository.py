"""Repository per l'accesso ai dati dello Storico OdA."""

import contextlib
from datetime import UTC, datetime
from typing import Any, Literal, overload

from src.core.database import db_manager
from src.core.logging import get_logger
from src.models import OdaRecord

logger = get_logger(__name__)


class OdaRepository:
    """Repository per l'accesso ai dati dello Storico OdA.

    Inizializza la classe.
    """

    def __init__(self, db_manager_instance: Any = None) -> None:
        self.db = db_manager_instance or db_manager
        self.columns = [
            "org_acq",
            "data_oda",
            "oda",
            "pos_oda",
            "stato",
            "cat_contab",
            "descrizione",
            "qta",
            "uom",
            "data_consegna",
            "valore_netto_pos",
            "valore_residuo",
            "valore_netto_oda",
            "divisione",
            "destinatario",
            "nome_destinatario",
            "codice_fornitore",
            "descrizione_fornitore",
            "emittente_fattura",
            "desc_emittente_fattura",
            "contract_card",
            "contratto",
            "posizione_contratto",
            "gruppo_acquisti",
            "indicatore_rilascio",
            "stato_rilascio",
            "attivita",
            "num_riga",
            "quantita",
            "unita_mis",
            "prezzo_lordo",
            "testo_breve",
        ]

    @overload
    def get_all(self, search_text: str | None = ..., as_objects: Literal[True] = ...) -> list[OdaRecord]: ...

    @overload
    def get_all(
        self, search_text: str | None = ..., as_objects: Literal[False] = ...
    ) -> list[tuple[Any, ...]]: ...

    def get_all(
        self, search_text: str | None = None, as_objects: bool = True
    ) -> list[OdaRecord] | list[tuple[Any, ...]]:
        """Recupera tutti gli OdA, opzionalmente filtrati per testo.

        Supporta il ritorno di oggetti Pydantic o tuple legacy.
        """
        db_path = self.db.DB_STORICO_ODA
        if not db_path.exists():
            return []

        query = f"SELECT {', '.join(self.columns)} FROM storico_oda WHERE 1=1"  # nosec B608
        # nosec B608
        params = []

        if search_text:
            search_text = search_text.lower().strip()
            search_pattern = search_text

            # Conversione data per ricerca smart (DD/MM/YYYY -> YYYY-MM-DD)
            min_date_len = 8
            if "/" in search_text and len(search_text) >= min_date_len:
                with contextlib.suppress(Exception):
                    d_obj = datetime.strptime(search_text, "%d/%m/%Y").replace(tzinfo=UTC)
                    search_pattern = d_obj.strftime("%Y-%m-%d")

            like_clause = " OR ".join([f"CAST({c} AS TEXT) LIKE ?" for c in self.columns])
            query += f" AND ({like_clause})"
            params.extend([f"%{search_pattern}%"] * len(self.columns))

        query += " ORDER BY data_oda DESC, oda DESC, CAST(pos_oda AS INTEGER) ASC, CAST(num_riga AS INTEGER) ASC LIMIT 3000"

        try:
            with self.db.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(params))
                rows = cursor.fetchall()
                if as_objects:
                    return [OdaRecord(**dict(row)) for row in rows]
                return [tuple(row) for row in rows]
        except Exception:
            logger.exception("Errore repository Oda get_all")
            return []
