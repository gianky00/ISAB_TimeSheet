"""
SyncroJob - Contabilita Manager (Refactored)
Facade per la gestione della Contabilità Strumentale.
Orchestra i servizi di importazione, ricerca e statistiche delegando le responsabilità.
"""

from collections.abc import Callable
from typing import Any

from src.core.contabilita.importer_service import ContabilitaImporterService
from src.core.contabilita.search_service import ContabilitaSearch
from src.core.contabilita.stats_service import ContabilitaStats, YearStats
from src.core.database import db_manager
from src.core.database.repositories import ContabilitaRepository
from src.core.logging import get_logger

logger = get_logger(__name__)


class ContabilitaManager:
    """Manager Facade per la gestione del database e dell'importazione Excel."""

    _instance = None
    _repo = ContabilitaRepository()

    @classmethod
    def scan_scarico_ore_rows(cls, file_path: str) -> int:
        """Stima rapida delle righe per Scarico Ore (DataEase) per calcolo ETA."""
        from src.core.excel_importer import ExcelImporter  # noqa: PLC0415

        return ExcelImporter.scan_scarico_ore_rows(file_path)

    @classmethod
    def scan_workload(cls, file_path: str, giornaliere_path: str) -> tuple[int, int]:
        """Scansiona rapidamente il carico di lavoro (fogli e file) per stima ETA."""
        return ContabilitaImporterService.scan_workload(file_path, giornaliere_path)

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
        return ContabilitaImporterService.import_main_data(file_path, progress_callback)

    @classmethod
    def import_giornaliere(
        cls,
        root_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Scansione e importa i dati dalle cartelle annuali delle giornaliere."""
        return ContabilitaImporterService.import_giornaliere(root_path, progress_callback)

    @classmethod
    def import_attivita_programmate(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Attività Programmate."""
        return ContabilitaImporterService.import_attivita_programmate(file_path, progress_callback)

    @classmethod
    def import_scarico_ore(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Scarico Ore Cantiere."""
        return ContabilitaImporterService.import_scarico_ore(file_path, progress_callback)

    @classmethod
    def import_certificati_campione(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Certificati Campione."""
        return ContabilitaImporterService.import_certificati_campione(file_path, progress_callback)

    @classmethod
    def get_available_years(cls) -> list[int]:
        """Restituisce la lista degli anni presenti nel DB."""
        return cls._repo.get_available_years()

    @classmethod
    def get_data_by_year(cls, year: int) -> list[tuple[Any, ...]]:
        """Restituisce i dati tabella Dati per un anno specifico."""
        return cls._repo.get_data_by_year(year, as_objects=False)

    @classmethod
    def get_giornaliere_by_year(cls, year: int) -> list[tuple[Any, ...]]:
        """Restituisce i dati Giornaliere per un anno specifico."""
        return cls._repo.get_giornaliere_by_year(year, as_objects=False)

    @classmethod
    def get_attivita_programmate_data(cls) -> list[tuple[Any, ...]]:
        """Restituisce i dati Attività Programmate."""
        return cls._repo.get_attivita_programmate(as_objects=False)

    @classmethod
    def get_certificati_campione_data(cls) -> list[tuple[Any, ...]]:
        """Restituisce i dati Certificati Campione."""
        return cls._repo.get_certificati_campione(as_objects=False)

    @classmethod
    def update_certificato_field(cls, record_id: int, field: str, value: str) -> bool:
        """Aggiorna un singolo campo di un certificato campione."""
        if field not in ("annotazioni", "ubicazione"):
            return False

        try:
            query = f"UPDATE certificati_campione SET {field} = ? WHERE id = ?"  # nosec B608
            db_manager.execute_query(db_manager.DB_CONTABILITA, query, (value, record_id))
        except Exception:
            logger.exception("Errore aggiornamento certificato", field=field)
            return False
        else:
            return True

    @classmethod
    def update_certificati_ubicazione_by_id_coemi(cls, id_coemi: str, value: str) -> bool:
        """Aggiorna l'ubicazione per tutti i certificati di uno strumento (storico incluso)."""
        if not id_coemi:
            return False

        try:
            query = "UPDATE certificati_campione SET ubicazione = ? WHERE id_coemi = ?"
            db_manager.execute_query(db_manager.DB_CONTABILITA, query, (value, id_coemi))
        except Exception:
            logger.exception("Errore aggiornamento ubicazione cumulativa", id_coemi=id_coemi)
            return False
        else:
            return True

    @classmethod
    def get_scarico_ore_data(cls) -> list[tuple[Any, ...]]:
        """Restituisce tutti i dati della tabella scarico_ore."""
        return cls._repo.get_scarico_ore(as_objects=False)

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


# Istanza globale (retrocompatibilità)
contabilita_manager = ContabilitaManager()
