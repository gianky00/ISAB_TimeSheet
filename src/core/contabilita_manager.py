"""
Bot TS - Contabilita Manager
Gestione dell'importazione e archiviazione dati della Contabilità Strumentale.
"""

from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import pandas as pd

from src.core.config_manager import CONFIG_DIR
from src.core.contabilita_queries import ContabilitaQueries
from src.core.contabilita_search import ContabilitaSearch
from src.core.contabilita_stats import ContabilitaStats, YearStats
from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter


class ContabilitaManager:
    """Manager per la gestione del database e dell'importazione Excel."""

    _instance = None  # Inizializza l'attributo _instance per il pattern singleton
    DB_PATH = CONFIG_DIR / "data" / "contabilita.db"

    @classmethod
    def scan_scarico_ore_rows(cls, file_path: str) -> int:
        """Stima rapida delle righe per Scarico Ore (DataEase) per calcolo ETA."""
        return ExcelImporter.scan_scarico_ore_rows(file_path)

    @classmethod
    def scan_workload(cls, file_path: str, giornaliere_path: str) -> Tuple[int, int]:
        """Scansiona rapidamente il carico di lavoro (fogli e file) per stima ETA."""
        return ExcelImporter.scan_workload(file_path, giornaliere_path)

    @classmethod
    def init_db(cls):
        """Inizializza il database tramite DatabaseManager."""
        db_manager.init_db()

    @classmethod
    def import_data_from_excel(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, int, int]:
        """Importa i dati dal file Excel specificato (Tabella Dati)."""
        success, message, imported_rows, imported_years = (
            ExcelImporter.import_contabilita_dati(file_path, progress_callback)
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_contabilita_dati(
            cls.DB_PATH, imported_rows, imported_years
        )
        return True, message, total_added, total_removed

    @classmethod
    def import_giornaliere(
        cls,
        root_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, int, int]:
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata.", 0, 0

        current_year = datetime.now().year

        try:
            # Cleanup: ensure no data from 2026+ exists (fix for bug)
            with db_manager.get_connection(cls.DB_PATH) as conn:
                conn.execute("DELETE FROM giornaliere WHERE year >= 2026")
                conn.execute("DELETE FROM contabilita WHERE year >= 2026")
                conn.commit()

            # 1. Lookup Map Preparation
            lookup_map = {}
            try:
                with db_manager.get_connection(cls.DB_PATH, read_only=True) as conn:
                    lookup_query = "SELECT n_prev, odc FROM contabilita WHERE odc IS NOT NULL AND odc != ''"
                    cursor = conn.cursor()
                    cursor.execute(lookup_query)
                    rows = cursor.fetchall()
                    # Creazione dizionario n_prev -> odc, ignorando duplicati (usa l'ultimo trovato)
                    lookup_map = {row[0]: row[1] for row in rows if row[0]}
            except Exception:
                pass

            # 2. Import Giornaliere data
            success, message, all_new_rows, years_encountered = (
                ExcelImporter.import_giornaliere(
                    root_path, lookup_map, progress_callback
                )
            )
            if not success:
                return False, message, 0, 0

            # 3. Synchronize with database
            total_added, total_removed = DataSynchronizer.sync_giornaliere(
                cls.DB_PATH, all_new_rows, years_encountered
            )

            if not years_encountered and len(all_new_rows) == 0:
                return (
                    True,
                    "Nessuna nuova giornaliera trovata (check anno >= "
                    + str(current_year)
                    + ").",
                    0,
                    0,
                )
            return (
                True,
                f"Importate Giornaliere: {sorted(set(years_encountered))}",
                total_added,
                total_removed,
            )

        except Exception as e:
            return False, f"Errore importazione Giornaliere: {e}", 0, 0

    @classmethod
    def import_attivita_programmate(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, int, int]:
        """Importa il file Attività Programmate (veloce, senza colori)."""
        success, message, imported_rows = ExcelImporter.import_attivita_programmate(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_attivita_programmate(
            cls.DB_PATH, imported_rows
        )
        return True, message, total_added, total_removed

    @classmethod
    def import_scarico_ore(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, int, int]:
        """Importa il file Scarico Ore Cantiere (OpenPyXL per colori + Diff Logic)."""
        success, message, imported_rows = ExcelImporter.import_scarico_ore(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_scarico_ore(
            cls.DB_PATH, imported_rows
        )
        return True, message, total_added, total_removed

    @classmethod
    def import_certificati_campione(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, int, int]:
        """Importa il file Certificati Campione."""
        success, message, imported_rows = ExcelImporter.import_certificati_campione(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_certificati_campione(
            cls.DB_PATH, imported_rows
        )
        return True, message, total_added, total_removed

    @classmethod
    def get_available_years(cls) -> List[int]:
        """Restituisce la lista degli anni presenti nel DB (unione di Dati e Giornaliere)."""
        return ContabilitaQueries.get_available_years(cls.DB_PATH)

    @classmethod
    def get_data_by_year(cls, year: int) -> List[Tuple]:
        """Restituisce i dati tabella Dati per un anno specifico."""
        return ContabilitaQueries.get_data_by_year(cls.DB_PATH, year)

    @classmethod
    def get_giornaliere_by_year(cls, year: int) -> List[Tuple]:
        """Restituisce i dati Giornaliere per un anno specifico."""
        return ContabilitaQueries.get_giornaliere_by_year(cls.DB_PATH, year)

    @classmethod
    def get_attivita_programmate_data(cls) -> List[Tuple]:
        """Restituisce i dati Attività Programmate (inclusi stili)."""
        return ContabilitaQueries.get_attivita_programmate_data(cls.DB_PATH)

    @classmethod
    def get_certificati_campione_data(cls) -> List[Tuple]:
        """Restituisce i dati Certificati Campione."""
        return ContabilitaQueries.get_certificati_campione_data(cls.DB_PATH)

    @classmethod
    def get_scarico_ore_data(cls) -> List[Tuple]:
        """Restituisce tutti i dati della tabella scarico_ore inclusi gli stili."""
        return ContabilitaQueries.get_scarico_ore_data(cls.DB_PATH)

    @classmethod
    def search_oda(cls, query: str) -> List[Dict]:
        """
        Cerca OdA per codice, descrizione o ODC.
        Returns:
            List[Dict]: Lista di risultati [{'codice_oda': '...', 'descrizione': '...'}, ...]
        """
        return ContabilitaSearch.search_oda(cls.DB_PATH, query)

    @classmethod
    def search_extended(
        cls, query: str, year: int = None, limit: int = 100
    ) -> Dict[str, List[Dict]]:
        """
        Ricerca estesa in tutti i moduli (Giornaliere, Scarico Ore, Certificati).
        Returns: Dict con liste di risultati per categoria.
        """
        return ContabilitaSearch.search_extended(cls.DB_PATH, query, year, limit)

    @classmethod
    def get_year_stats(cls, year: int) -> YearStats:
        """Calcola statistiche avanzate per l'anno specificato (Tabella Dati) + KPI Diretti/Indiretti."""
        return ContabilitaStats.get_year_stats(cls.DB_PATH, year)
