"""
Bot TS - Contabilita Queries
Gestisce tutte le query di lettura per i dati della Contabilità Strumentale.
"""

from pathlib import Path
from typing import List, Tuple

from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter  # Per accedere ai COLUMNS_MAPPING


class ContabilitaQueries:
    """Gestore per le query di lettura del database della Contabilità Strumentale."""

    @classmethod
    def get_available_years(cls, db_path: Path) -> List[int]:
        """Restituisce la lista degli anni presenti nel DB (unione di Dati e Giornaliere)."""
        if not db_path.exists():
            return []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT DISTINCT year FROM contabilita UNION SELECT DISTINCT year FROM giornaliere ORDER BY 1 DESC"
                )
                years = [row[0] for row in cursor.fetchall()]
                return years
        except Exception:
            return []

    @classmethod
    def get_data_by_year(cls, db_path: Path, year: int) -> List[Tuple]:
        """Restituisce i dati tabella Dati per un anno specifico."""
        if not db_path.exists():
            return []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                cols = list(ExcelImporter.COLUMNS_MAPPING.values())
                query = f"SELECT {', '.join(cols)} FROM contabilita WHERE year = ? ORDER BY n_prev DESC, id DESC"  # nosec B608
                cursor.execute(query, (year,))
                rows = cursor.fetchall()
                return rows
        except Exception:
            return []

    @classmethod
    def get_giornaliere_by_year(cls, db_path: Path, year: int) -> List[Tuple]:
        """Restituisce i dati Giornaliere per un anno specifico."""
        if not db_path.exists():
            return []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
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
                query = f"SELECT {', '.join(cols)} FROM giornaliere WHERE year = ? ORDER BY data DESC, id DESC"  # nosec B608
                cursor.execute(query, (year,))
                rows = cursor.fetchall()
                return rows
        except Exception:
            return []

    @classmethod
    def get_attivita_programmate_data(cls, db_path: Path) -> List[Tuple]:
        """Restituisce i dati Attività Programmate (inclusi stili)."""
        if not db_path.exists():
            return []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                cols = ExcelImporter.ATTIVITA_PROGRAMMATE_COLS
                query = f"SELECT {', '.join(cols)} FROM attivita_programmate ORDER BY id ASC"  # nosec B608
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except Exception:
            return []

    @classmethod
    def get_certificati_campione_data(cls, db_path: Path) -> List[Tuple]:
        """Restituisce i dati Certificati Campione."""
        if not db_path.exists():
            return []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                cols = ExcelImporter.CERTIFICATI_CAMPIONE_COLS
                query = f"SELECT {', '.join(cols)} FROM certificati_campione ORDER BY id ASC"  # nosec B608
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except Exception:
            return []

    @classmethod
    def get_scarico_ore_data(cls, db_path: Path) -> List[Tuple]:
        """Restituisce tutti i dati della tabella scarico_ore inclusi gli stili."""
        if not db_path.exists():
            return []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                cols = ExcelImporter.SCARICO_ORE_COLS
                query = f"SELECT {', '.join(cols)} FROM scarico_ore ORDER BY id DESC"  # nosec B608
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except Exception:
            return []
