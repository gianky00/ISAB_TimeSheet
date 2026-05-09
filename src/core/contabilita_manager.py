"""
Bot TS - Contabilita Manager
Gestione dell'importazione e archiviazione dati della Contabilità Strumentale.
"""

import logging
from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.core.contabilita_queries import ContabilitaQueries
from src.core.contabilita_search import ContabilitaSearch
from src.core.contabilita_stats import ContabilitaStats, YearStats
from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter

logger = logging.getLogger(__name__)


class ContabilitaManager:
    """Manager per la gestione del database e dell'importazione Excel."""

    _instance = None  # Inizializza l'attributo _instance per il pattern singleton

    @classmethod
    def scan_scarico_ore_rows(cls, file_path: str) -> int:
        """Stima rapida delle righe per Scarico Ore (DataEase) per calcolo ETA."""
        return ExcelImporter.scan_scarico_ore_rows(file_path)

    @classmethod
    def scan_workload(cls, file_path: str, giornaliere_path: str) -> tuple[int, int]:
        """Scansiona rapidamente il carico di lavoro (fogli e file) per stima ETA."""
        return ExcelImporter.scan_workload(file_path, giornaliere_path)

    @classmethod
    def init_db(cls) -> None:
        """Inizializza il database tramite DatabaseManager."""
        db_manager.init_db()

    @classmethod
    def import_data_from_excel(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa i dati dal file Excel specificato (Tabella Dati)."""
        (
            success,
            message,
            imported_rows,
            imported_years,
        ) = ExcelImporter.import_contabilita_dati(file_path, progress_callback)
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_contabilita_dati(
            db_manager.DB_CONTABILITA, imported_rows, imported_years
        )
        return True, message, total_added, total_removed

    @classmethod
    def import_giornaliere(
        cls,
        root_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """
        Scansione e importa i dati dalle cartelle annuali delle giornaliere.
        """
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata.", 0, 0

        current_year = datetime.now(UTC).year

        try:
            # 1. Lookup Map Preparation
            lookup_map = {}
            with (
                suppress(Exception),
                db_manager.get_connection(db_manager.DB_CONTABILITA, read_only=True) as conn,
            ):
                lookup_query = "SELECT n_prev, odc FROM contabilita WHERE odc IS NOT NULL AND odc != ''"
                cursor = conn.cursor()
                cursor.execute(lookup_query)
                rows = cursor.fetchall()
                lookup_map = {row[0]: row[1] for row in rows if row[0]}

            # 2. Import Giornaliere data
            (
                success,
                message,
                all_new_rows,
                years_encountered,
            ) = ExcelImporter.import_giornaliere(root_path, lookup_map, progress_callback)
            if not success:
                return False, message, 0, 0

            # 3. Synchronize with database
            total_added, total_removed = DataSynchronizer.sync_giornaliere(
                db_manager.DB_CONTABILITA, all_new_rows, years_encountered
            )

            if not years_encountered and not all_new_rows:
                return (
                    True,
                    "Nessuna nuova giornaliera trovata (check anno >= " + str(current_year) + ").",
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
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Attivita'Programmate (veloce, senza colori)."""
        success, message, imported_rows = ExcelImporter.import_attivita_programmate(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_attivita_programmate(
            db_manager.DB_CONTABILITA, imported_rows
        )
        return True, message, total_added, total_removed

    @classmethod
    def import_scarico_ore(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Scarico Ore Cantiere."""
        success, message, imported_rows = ExcelImporter.import_scarico_ore(file_path, progress_callback)
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_scarico_ore(
            db_manager.DB_CONTABILITA, imported_rows
        )
        return True, message, total_added, total_removed

    @classmethod
    def import_certificati_campione(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Certificati Campione."""
        success, message, imported_rows = ExcelImporter.import_certificati_campione(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_certificati_campione(
            db_manager.DB_CONTABILITA, imported_rows
        )
        return True, message, total_added, total_removed

    @classmethod
    def get_available_years(cls) -> list[int]:
        """Restituisce la lista degli anni presenti nel DB."""
        return ContabilitaQueries.get_available_years(db_manager.DB_CONTABILITA)

    @classmethod
    def get_data_by_year(cls, year: int) -> list[tuple[Any, ...]]:
        """Restituisce i dati tabella Dati per un anno specifico."""
        return ContabilitaQueries.get_data_by_year(db_manager.DB_CONTABILITA, year)

    @classmethod
    def get_giornaliere_by_year(cls, year: int) -> list[tuple[Any, ...]]:
        """Restituisce i dati Giornaliere per un anno specifico."""
        return ContabilitaQueries.get_giornaliere_by_year(db_manager.DB_CONTABILITA, year)

    @classmethod
    def get_attivita_programmate_data(cls) -> list[tuple[Any, ...]]:
        """Restituisce i dati Attivita'Programmate."""
        return ContabilitaQueries.get_attivita_programmate_data(db_manager.DB_CONTABILITA)

    @classmethod
    def get_certificati_campione_data(cls) -> list[tuple[Any, ...]]:
        """Restituisce i dati Certificati Campione."""
        return ContabilitaQueries.get_certificati_campione_data(db_manager.DB_CONTABILITA)

    @classmethod
    def update_certificato_field(cls, record_id: int, field: str, value: str) -> bool:
        """Aggiorna un singolo campo di un certificato campione."""
        if field not in ("annotazioni", "ubicazione"):
            return False

        try:
            query = f"UPDATE certificati_campione SET {field} = ? WHERE id = ?"  # nosec B608
            db_manager.execute_query(db_manager.DB_CONTABILITA, query, (value, record_id))
            return True  # noqa: TRY300
        except Exception as e:
            logger.error(f"Errore aggiornamento certificato ({field}): {e}")  # noqa: TRY400
            return False

    @classmethod
    def get_scarico_ore_data(cls) -> list[tuple[Any, ...]]:
        """Restituisce tutti i dati della tabella scarico_ore."""
        return ContabilitaQueries.get_scarico_ore_data(db_manager.DB_CONTABILITA)

    @classmethod
    def search_oda(cls, query: str) -> list[dict[str, Any]]:
        """Cerca OdA per codice, descrizione o ODC."""
        return ContabilitaSearch.search_oda(db_manager.DB_CONTABILITA, query)

    @classmethod
    def search_extended(
        cls, query: str, year: int | None = None, limit: int = 100
    ) -> dict[str, list[dict[str, Any]]]:
        """Ricerca estesa in tutti i moduli."""
        return ContabilitaSearch.search_extended(db_manager.DB_CONTABILITA, query, year, limit)

    @classmethod
    def get_year_stats(cls, year: int) -> YearStats:
        """Calcola statistiche avanzate per l'anno specificato."""
        return ContabilitaStats.get_year_stats(db_manager.DB_CONTABILITA, year)
