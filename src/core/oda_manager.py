"""
SyncroJob - Oda Manager
Gestione dell'importazione e archiviazione Storico OdA.
"""

from typing import Any, Callable, List, Optional, Tuple

from src.core.config_manager import CONFIG_DIR
from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter


class OdaManager:
    """Manager per la gestione del database Storico OdA."""

    DB_PATH = CONFIG_DIR / "data" / "storico_oda.db"

    @classmethod
    def init_db(cls):
        """Inizializza il database tramite DatabaseManager."""
        db_manager.init_db()

    @classmethod
    def get_all_oda(cls, search_text: Optional[str] = None) -> List[Tuple[Any, ...]]:
        """
        Recupera tutti gli OdA dal database, opzionalmente filtrati.
        L'ordine delle colonne restituito corrisponde a quello originale del branch main.
        """
        query = """
            SELECT
                org_acq, data_oda, oda, pos_oda, stato, cat_contab, descrizione,
                qta, uom, data_consegna, valore_netto_pos, valore_residuo, valore_netto_oda,
                divisione, destinatario, nome_destinatario, codice_fornitore, descrizione_fornitore,
                emittente_fattura, desc_emittente_fattura, contract_card, contratto,
                posizione_contratto, gruppo_acquisti, indicatore_rilascio, stato_rilascio,
                attivita, num_riga, quantita, unita_mis, prezzo_lordo, testo_breve
            FROM storico_oda
            WHERE 1=1
        """
        params = []

        if search_text:
            search_text = search_text.lower().strip()
            query += """ AND (
                CAST(oda AS TEXT) LIKE ? OR
                descrizione LIKE ? OR
                descrizione_fornitore LIKE ? OR
                CAST(contratto AS TEXT) LIKE ? OR
                codice_fornitore LIKE ? OR
                CAST(pos_oda AS TEXT) LIKE ? OR
                stato LIKE ? OR
                cat_contab LIKE ? OR
                testo_breve LIKE ?
            )"""
            p = f"%{search_text}%"
            params.extend([p] * 9)

        # Ordinamento: Data decrescente, OdA decrescente, Posizione crescente
        query += (
            " ORDER BY data_oda DESC, oda DESC, "
            "CAST(pos_oda AS INTEGER) ASC, "
            "CAST(num_riga AS INTEGER) ASC LIMIT 3000"
        )

        return db_manager.execute_query(cls.DB_PATH, query, tuple(params))

    @classmethod
    def import_oda_from_excel(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, int, int]:
        """Importa i dati dal file Excel Storico OdA."""
        import time

        from src.core.sync_tracker import SyncTracker

        start_time = time.time()

        success, message, imported_rows = ExcelImporter.import_storico_oda(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_storico_oda(
            cls.DB_PATH, imported_rows
        )

        duration = time.time() - start_time
        SyncTracker.update_status("storico_oda", total_added, total_removed, duration)

        return True, message, total_added, total_removed
