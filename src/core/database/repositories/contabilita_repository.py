from typing import Any, Literal, overload

from src.core.database import db_manager
from src.core.logging import get_logger
from src.models import (
    AttivitaProgrammataRecord,
    CertificatoCampioneRecord,
    ContabilitaRecord,
    GiornalieraRecord,
)

logger = get_logger(__name__)


class ContabilitaRepository:
    """Repository per l'accesso ai dati della Contabilità Strumentale."""

    def __init__(self, db_manager_instance: Any = None) -> None:
        self.db = db_manager_instance or db_manager

    def get_available_years(self) -> list[int]:
        """Restituisce la lista degli anni presenti nel DB."""
        db_path = self.db.DB_CONTABILITA
        if not db_path.exists():
            return []
        try:
            with self.db.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT DISTINCT year FROM contabilita UNION SELECT DISTINCT year FROM giornaliere ORDER BY 1 DESC"
                )
                return [row[0] for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_available_years")
            return []

    @overload
    def get_data_by_year(self, year: int, as_objects: Literal[True] = ...) -> list[ContabilitaRecord]: ...

    @overload
    def get_data_by_year(self, year: int, as_objects: Literal[False] = ...) -> list[tuple[Any, ...]]: ...

    def get_data_by_year(self, year: int, as_objects: bool = True) -> list[ContabilitaRecord] | list[tuple[Any, ...]]:
        """Restituisce i record di contabilità per un anno specifico."""
        db_path = self.db.DB_CONTABILITA
        if not db_path.exists():
            return []
        try:
            with self.db.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                if as_objects:
                    cursor.execute(
                        "SELECT * FROM contabilita WHERE year = ? ORDER BY n_prev DESC, id DESC", (year,)
                    )
                    rows = cursor.fetchall()
                    return [ContabilitaRecord(**dict(row)) for row in rows]

                # Per compatibilità legacy, selezioniamo solo le colonne mappate da Excel
                from src.core.excel_importer import ExcelImporter  # noqa: PLC0415
                cols = list(ExcelImporter.COLUMNS_MAPPING.values())
                cursor.execute(
                    f"SELECT {', '.join(cols)} FROM contabilita WHERE year = ? ORDER BY n_prev DESC, id DESC", (year,)
                )
                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_data_by_year", year=year)
            return []

    @overload
    def get_giornaliere_by_year(self, year: int, as_objects: Literal[True] = ...) -> list[GiornalieraRecord]: ...

    @overload
    def get_giornaliere_by_year(self, year: int, as_objects: Literal[False] = ...) -> list[tuple[Any, ...]]: ...

    def get_giornaliere_by_year(self, year: int, as_objects: bool = True) -> list[GiornalieraRecord] | list[tuple[Any, ...]]:
        """Restituisce i record di giornaliera per un anno specifico."""
        db_path = self.db.DB_CONTABILITA
        if not db_path.exists():
            return []
        try:
            with self.db.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                if as_objects:
                    cursor.execute(
                        "SELECT * FROM giornaliere WHERE year = ? ORDER BY data DESC, id DESC", (year,)
                    )
                    rows = cursor.fetchall()
                    return [GiornalieraRecord(**dict(row)) for row in rows]

                # Per compatibilità legacy
                cols = ["data", "personale", "tcl", "descrizione", "n_prev", "odc", "pdl", "inizio", "fine", "ore", "nome_file"]
                cursor.execute(
                    f"SELECT {', '.join(cols)} FROM giornaliere WHERE year = ? ORDER BY data DESC, id DESC", (year,)
                )
                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_giornaliere_by_year", year=year)
            return []

    @overload
    def get_attivita_programmate(self, as_objects: Literal[True] = ...) -> list[AttivitaProgrammataRecord]: ...

    @overload
    def get_attivita_programmate(self, as_objects: Literal[False] = ...) -> list[tuple[Any, ...]]: ...

    def get_attivita_programmate(self, as_objects: bool = True) -> list[AttivitaProgrammataRecord] | list[tuple[Any, ...]]:
        """Restituisce le attività programmate."""
        db_path = self.db.DB_CONTABILITA
        if not db_path.exists():
            return []
        try:
            with self.db.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                if as_objects:
                    cursor.execute("SELECT * FROM attivita_programmate ORDER BY id ASC")
                    rows = cursor.fetchall()
                    return [AttivitaProgrammataRecord(**dict(row)) for row in rows]

                # Per compatibilità legacy
                from src.core.excel_importer import ExcelImporter  # noqa: PLC0415
                cols = ExcelImporter.ATTIVITA_PROGRAMMATE_COLS
                cursor.execute(f"SELECT {', '.join(cols)} FROM attivita_programmate ORDER BY id ASC")
                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_attivita_programmate")
            return []

    @overload
    def get_certificati_campione(self, as_objects: Literal[True] = ...) -> list[CertificatoCampioneRecord]: ...

    @overload
    def get_certificati_campione(self, as_objects: Literal[False] = ...) -> list[tuple[Any, ...]]: ...

    def get_certificati_campione(self, as_objects: bool = True) -> list[CertificatoCampioneRecord] | list[tuple[Any, ...]]:
        """Restituisce i certificati campione."""
        db_path = self.db.DB_CONTABILITA
        if not db_path.exists():
            return []
        try:
            with self.db.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                if as_objects:
                    cursor.execute("SELECT * FROM certificati_campione ORDER BY id ASC")
                    rows = cursor.fetchall()
                    return [CertificatoCampioneRecord(**dict(row)) for row in rows]

                # Per compatibilità legacy
                from src.core.excel_importer import ExcelImporter  # noqa: PLC0415
                cols = ExcelImporter.CERTIFICATI_CAMPIONE_COLS
                cols_str = ", ".join(cols)
                query = f"SELECT {cols_str}, annotazioni, ubicazione, id FROM certificati_campione ORDER BY id ASC"
                cursor.execute(query)
                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_certificati_campione")
            return []
