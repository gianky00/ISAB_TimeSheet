"""
SyncroJob - OdA Manager
Modulo per la gestione, l'interrogazione e l'aggiornamento del database dello Storico Ordini di Acquisto (OdA).
Gestisce la sincronizzazione tra i file Excel esportati dal portale e il database SQLite locale.
"""

from collections.abc import Callable
from typing import Any

from src.core.config_manager import CONFIG_DIR
from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter


class OdaManager:
    """
    Controller per le operazioni CRUD e di ricerca sullo Storico OdA.
    Centralizza l'accesso ai dati degli ordini, permettendo ricerche testuali complesse
    e procedure di importazione batch da sorgenti Excel.
    """

    DB_PATH = CONFIG_DIR / "data" / "storico_oda.db"
    """Percorso del database SQLite dedicato allo storico OdA."""

    @classmethod
    def init_db(cls) -> None:
        """Inizializza lo schema del database se non esistente tramite il Database Manager."""
        db_manager.init_db()

    @classmethod
    def get_all_oda(cls, search_text: str | None = None) -> list[tuple[Any, ...]]:
        """
        Recupera un elenco di ordini di acquisto dal database, con supporto alla ricerca full-text.
        Il risultato è limitato alle prime 3000 occorrenze per ottimizzare la velocità della UI.

        Args:
            search_text: Stringa di ricerca da applicare a tutte le colonne testuali e numeriche.

        Returns:
            list: Lista di tuple rappresentanti le righe del database (32 colonne).
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
                CAST(oda AS TEXT) LIKE ? OR descrizione LIKE ? OR descrizione_fornitore LIKE ? OR 
                CAST(contratto AS TEXT) LIKE ? OR codice_fornitore LIKE ? OR CAST(pos_oda AS TEXT) LIKE ? OR 
                stato LIKE ? OR cat_contab LIKE ? OR testo_breve LIKE ? OR org_acq LIKE ? OR 
                CAST(data_oda AS TEXT) LIKE ? OR CAST(qta AS TEXT) LIKE ? OR uom LIKE ? OR 
                CAST(data_consegna AS TEXT) LIKE ? OR CAST(valore_netto_pos AS TEXT) LIKE ? OR 
                CAST(valore_residuo AS TEXT) LIKE ? OR CAST(valore_netto_oda AS TEXT) LIKE ? OR 
                divisione LIKE ? OR destinatario LIKE ? OR nome_destinatario LIKE ? OR 
                emittente_fattura LIKE ? OR desc_emittente_fattura LIKE ? OR contract_card LIKE ? OR 
                CAST(posizione_contratto AS TEXT) LIKE ? OR gruppo_acquisti LIKE ? OR 
                indicatore_rilascio LIKE ? OR stato_rilascio LIKE ? OR attivita LIKE ? OR 
                CAST(num_riga AS TEXT) LIKE ? OR CAST(quantita AS TEXT) LIKE ? OR 
                unita_mis LIKE ? OR CAST(prezzo_lordo AS TEXT) LIKE ?
            )"""
            params.extend([f"%{search_text}%"] * 32)

        query += " ORDER BY data_oda DESC, oda DESC, CAST(pos_oda AS INTEGER) ASC, CAST(num_riga AS INTEGER) ASC LIMIT 3000"
        return db_manager.execute_query(cls.DB_PATH, query, tuple(params))

    @classmethod
    def import_oda_from_excel(
        cls, file_path: str, progress_callback: Callable[[int, int], None] | None = None
    ) -> tuple[bool, str, int, int]:
        """
        Importa dati da un file Excel (.xlsx) e sincronizza il database locale.
        La sincronizzazione avviene tramite un'operazione di merge che inserisce i nuovi record 
        e rimuove quelli obsoleti.

        Args:
            file_path: Percorso del file Excel sorgente.
            progress_callback: Funzione opzionale per monitorare l'avanzamento (riga_attuale, righe_totali).

        Returns:
            tuple: (success: bool, messaggio: str, aggiunti: int, rimossi: int).
        """
        import time
        from src.core.sync_tracker import SyncTracker

        start_time = time.time()
        success, message, imported_rows = ExcelImporter.import_storico_oda(file_path, progress_callback)
        if not success: return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_storico_oda(cls.DB_PATH, imported_rows)
        duration = time.time() - start_time
        SyncTracker.update_status("storico_oda", total_added, total_removed, duration)

        return True, message, total_added, total_removed
