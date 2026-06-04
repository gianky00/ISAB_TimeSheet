"""Repository per l'accesso ai dati della Contabilità Strumentale."""

from typing import Any, Literal, overload

from src.application.services.database import db_manager
from src.application.services.logging import get_logger
from src.domain import (
    AttivitaProgrammataRecord,
    CertificatoCampioneRecord,
    ContabilitaRecord,
    GiornalieraRecord,
)

logger = get_logger(__name__)


class ContabilitaRepository:
    """Repository per l'accesso ai dati della Contabilità Strumentale.

    Inizializza la classe.
    """

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

    def get_data_by_year(
        self, year: int, as_objects: bool = True
    ) -> list[ContabilitaRecord] | list[tuple[Any, ...]]:
        """Restituisce i record di contabilità per un anno specifico.

        Supporta il ritorno di oggetti Pydantic o tuple legacy.
        """
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
                from src.application.services.excel_importer import ExcelImporter  # noqa: PLC0415

                cols = list(ExcelImporter.COLUMNS_MAPPING.values())
                cursor.execute(
                    f"SELECT {', '.join(cols)} FROM contabilita WHERE year = ? ORDER BY n_prev DESC, id DESC",  # nosec B608
                    (year,),
                )
                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_data_by_year", year=year)
            return []

    @overload
    def get_giornaliere_by_year(
        self, year: int, as_objects: Literal[True] = ...
    ) -> list[GiornalieraRecord]: ...

    @overload
    def get_giornaliere_by_year(
        self, year: int, as_objects: Literal[False] = ...
    ) -> list[tuple[Any, ...]]: ...

    def get_giornaliere_by_year(
        self, year: int, as_objects: bool = True
    ) -> list[GiornalieraRecord] | list[tuple[Any, ...]]:
        """Restituisce i record di giornaliera per un anno specifico.

        Supporta il ritorno di oggetti Pydantic o tuple legacy.
        """
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
                cols = [
                    "data",
                    "personale",
                    "tcl",
                    "descrizione",
                    "n_prev",
                    "odc",
                    "pdl",
                    "inizio",
                    "fine",
                    "ore",
                    "nome_file",
                ]
                query = (
                    f"SELECT {', '.join(cols)} FROM giornaliere WHERE year = ? ORDER BY data DESC, id DESC"  # nosec B608
                )
                cursor.execute(
                    query,
                    (year,),
                )

                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_giornaliere_by_year", year=year)
            return []

    @overload
    def get_attivita_programmate(
        self, as_objects: Literal[True] = ...
    ) -> list[AttivitaProgrammataRecord]: ...

    @overload
    def get_attivita_programmate(self, as_objects: Literal[False] = ...) -> list[tuple[Any, ...]]: ...

    def get_attivita_programmate(
        self, as_objects: bool = True
    ) -> list[AttivitaProgrammataRecord] | list[tuple[Any, ...]]:
        """Restituisce le attività programmate.

        Supporta il ritorno di oggetti Pydantic o tuple legacy.
        """
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
                from src.application.services.excel_importer import ExcelImporter  # noqa: PLC0415

                cols = ExcelImporter.ATTIVITA_PROGRAMMATE_COLS
                cursor.execute(f"SELECT {', '.join(cols)} FROM attivita_programmate ORDER BY id ASC")  # nosec B608
                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_attivita_programmate")
            return []

    @overload
    def get_certificati_campione(
        self, as_objects: Literal[True] = ...
    ) -> list[CertificatoCampioneRecord]: ...

    @overload
    def get_certificati_campione(self, as_objects: Literal[False] = ...) -> list[tuple[Any, ...]]: ...

    def get_certificati_campione(
        self, as_objects: bool = True
    ) -> list[CertificatoCampioneRecord] | list[tuple[Any, ...]]:
        """Restituisce i certificati campione.

        Supporta il ritorno di oggetti Pydantic o tuple legacy.
        """
        db_path = self.db.DB_CONTABILITA
        if not db_path.exists():
            return []
        try:
            with self.db.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()

                # Rilevamento colonne per gestire transizione id_strumento -> id_coemi
                cursor.execute("PRAGMA table_info(certificati_campione)")
                db_cols = [row[1] for row in cursor.fetchall()]
                id_col = "id_coemi" if "id_coemi" in db_cols else "id_strumento"

                if as_objects:
                    cursor.execute("SELECT * FROM certificati_campione ORDER BY id ASC")
                    rows = cursor.fetchall()
                    results = []
                    for row in rows:
                        d = dict(row)
                        # Allineamento dinamico al modello
                        if "id_strumento" in d and "id_coemi" not in d:
                            d["id_coemi"] = d.pop("id_strumento")

                        # Rimuovi campi non presenti nel modello (es. created_at)
                        filtered_d = {
                            k: v for k, v in d.items() if k in CertificatoCampioneRecord.__dataclass_fields__
                        }
                        results.append(CertificatoCampioneRecord(**filtered_d))
                    return results

                from src.application.services.excel_importer import ExcelImporter  # noqa: PLC0415

                cols = ExcelImporter.CERTIFICATI_CAMPIONE_COLS.copy()

                # Sostituiamo id_coemi con quello reale del DB se necessario
                if id_col == "id_strumento" and "id_coemi" in cols:
                    cols[cols.index("id_coemi")] = "id_strumento"

                cols = [
                    "id_coemi",
                    "certificato",
                    "modello",
                    "costruttore",
                    "matricola",
                    "range_strumento",
                    "errore_max",
                    "emissione",
                    "scadenza",
                    "stato",
                ]
                cols_str = ", ".join(cols)
                query = f"SELECT {cols_str}, annotazioni, ubicazione, guasto, guasto_tipo, guasto_data, guasto_note, id FROM certificati_campione ORDER BY id ASC"  # nosec B608
                cursor.execute(query)
                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_certificati_campione")
            return []

    def get_scarico_ore(self, as_objects: bool = False) -> list[tuple[Any, ...]] | list[Any]:
        """Restituisce i record dello scarico ore (cantiere)."""
        db_path = self.db.DB_CONTABILITA
        if not db_path.exists():
            return []
        try:
            with self.db.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                if as_objects:
                    # In futuro possiamo implementare un modello per ScaricoOre
                    cursor.execute("SELECT * FROM scarico_ore ORDER BY id DESC")
                    return cursor.fetchall()

                # Per compatibilità legacy
                from src.application.services.excel_importer import ExcelImporter  # noqa: PLC0415

                cols = ExcelImporter.SCARICO_ORE_COLS
                query = f"SELECT {', '.join(cols)} FROM scarico_ore ORDER BY id DESC"  # nosec B608
                cursor.execute(query)
                return [tuple(row) for row in cursor.fetchall()]
        except Exception:
            logger.exception("Errore repository get_scarico_ore")
            return []
