"""
SyncroJob - OdA Manager
Modulo per la gestione, l'interrogazione e l'aggiornamento del database dello Storico Ordini di Acquisto (OdA).
Gestisce la sincronizzazione tra i file Excel esportati dal portale e il database SQLite locale.
"""

import contextlib
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from src.core.config_manager import CONFIG_DIR
from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.importers.storico_oda import StoricoOdaImporter


class OdaManager:
    """
    Controller per le operazioni CRUD e di ricerca sullo Storico OdA.
    Centralizza l'accesso ai dati degli ordini, permettendo ricerche testuali complesse.
    """

    DB_PATH = CONFIG_DIR / "data" / "storico_oda.db"

    @classmethod
    def init_db(cls) -> None:
        """Inizializza lo schema del database se non esistente."""
        db_manager.init_db()

    @classmethod
    def get_all_oda(cls, search_text: str | None = None) -> list[tuple[Any, ...]]:
        """
        Recupera un elenco di ordini di acquisto dal database.
        L'ordine delle colonne nel SELECT è garantito per corrispondere agli header UI.
        """
        # Ordine colonne sincronizzato con StoricoOdaPanel.full_headers
        columns = [
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

        query = f"SELECT {', '.join(columns)} FROM storico_oda WHERE 1=1"  # nosec B608
        params = []

        if search_text:
            search_text = search_text.lower().strip()

            # Fix: Conversione data per ricerca smart (DD/MM/YYYY -> YYYY-MM-DD)
            search_pattern = search_text
            if "/" in search_text and len(search_text) >= 8:
                with contextlib.suppress(Exception):
                    d_obj = datetime.strptime(search_text, "%d/%m/%Y").replace(tzinfo=UTC)
                    search_pattern = d_obj.strftime("%Y-%m-%d")

            like_clause = " OR ".join([f"CAST({c} AS TEXT) LIKE ?" for c in columns])
            query += f" AND ({like_clause})"
            params.extend([f"%{search_pattern}%"] * len(columns))

        query += " ORDER BY data_oda DESC, oda DESC, CAST(pos_oda AS INTEGER) ASC, CAST(num_riga AS INTEGER) ASC LIMIT 3000"
        return db_manager.execute_query(cls.DB_PATH, query, tuple(params))

    @classmethod
    def import_oda_from_excel(
        cls, file_path: str, progress_callback: Callable[[int, int], None] | None = None
    ) -> tuple[bool, str, int, int]:
        """Importa dati da Excel e sincronizza il DB."""
        import time

        from src.core.sync_tracker import SyncTracker

        start_time = time.time()
        # Nota: Usiamo StoricoOdaImporter direttamente per coerenza
        success, message, imported_rows = StoricoOdaImporter.import_storico_oda(file_path, progress_callback)
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_storico_oda(cls.DB_PATH, imported_rows)
        duration = time.time() - start_time
        SyncTracker.update_status("oda", total_added, total_removed, duration)

        return True, message, total_added, total_removed
