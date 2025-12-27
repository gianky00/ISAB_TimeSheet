"""
Bot TS - Database Manager
Centralized SQLite database management.
Provides connection handling, context managers, and common utilities for all application databases.
"""
import sqlite3
import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Generator, Optional, Any, List, Dict

from src.core.config_manager import CONFIG_DIR

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Singleton class to manage SQLite connections.
    """
    _instance = None

    # Predefined Paths
    DB_CONTABILITA = CONFIG_DIR / "data" / "contabilita.db"
    DB_TIMBRATURE = CONFIG_DIR / "data" / "timbrature_Isab.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._ensure_dirs()
        return cls._instance

    def _ensure_dirs(self):
        """Ensures the data directory exists."""
        (CONFIG_DIR / "data").mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self, db_path: Path, read_only: bool = False) -> Generator[sqlite3.Connection, None, None]:
        """
        Yields a SQLite connection to the specified database.
        Enables WAL mode and handles closing.
        """
        uri = f"file:{db_path.absolute()}"
        if read_only:
            uri += "?mode=ro"

        try:
            conn = sqlite3.connect(uri, uri=True)
        except sqlite3.OperationalError:
            # Fallback for read-only if file doesn't exist or other error
            conn = sqlite3.connect(str(db_path))

        try:
            # Optimize Performance
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")

            # Row Factory for dict-like access if desired, but many legacy queries expect tuples.
            # We keep default (tuples) here, but consumers can change it.

            yield conn
        except Exception as e:
            logger.error(f"Database Error ({db_path.name}): {e}")
            raise
        finally:
            conn.close()

    def execute_query(self, db_path: Path, query: str, params: tuple = ()) -> List[Any]:
        """Executes a query and returns results (SELECT) or None (INSERT/UPDATE)."""
        with self.get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                conn.commit()
                return []

    def init_db(self):
        """
        Initializes schema and indexes for all databases.
        This unifies initialization logic previously scattered.
        """
        self._init_contabilita()
        self._init_timbrature()

    def _init_contabilita(self):
        with self.get_connection(self.DB_CONTABILITA) as conn:
            cursor = conn.cursor()

            # --- Tables ---

            # Contabilita (Dati)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contabilita (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    data_prev TEXT,
                    mese TEXT,
                    n_prev TEXT,
                    totale_prev TEXT,
                    attivita TEXT,
                    tcl TEXT,
                    odc TEXT,
                    stato_attivita TEXT,
                    tipologia TEXT,
                    ore_sp TEXT,
                    resa TEXT,
                    annotazioni TEXT,
                    indirizzo_consuntivo TEXT,
                    nome_file TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Giornaliere
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS giornaliere (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    data TEXT,
                    personale TEXT,
                    descrizione TEXT,
                    tcl TEXT,
                    odc TEXT,
                    pdl TEXT,
                    inizio TEXT,
                    fine TEXT,
                    ore TEXT,
                    n_prev TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Migration
            try: cursor.execute("ALTER TABLE giornaliere ADD COLUMN nome_file TEXT")
            except: pass

            # Scarico Ore
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scarico_ore (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT,
                    pers1 TEXT,
                    pers2 TEXT,
                    odc TEXT,
                    pos TEXT,
                    dalle TEXT,
                    alle TEXT,
                    totale_ore TEXT,
                    descrizione TEXT,
                    finito TEXT,
                    commessa TEXT,
                    styles TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            try: cursor.execute("ALTER TABLE scarico_ore ADD COLUMN styles TEXT")
            except: pass

            # Attivita Programmate
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attivita_programmate (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ps TEXT,
                    area TEXT,
                    pdl TEXT,
                    imp TEXT,
                    descrizione TEXT,
                    lun TEXT,
                    mar TEXT,
                    mer TEXT,
                    gio TEXT,
                    ven TEXT,
                    stato_pdl TEXT,
                    stato_attivita TEXT,
                    data_controllo TEXT,
                    personale TEXT,
                    po TEXT,
                    avviso TEXT,
                    styles TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            try: cursor.execute("ALTER TABLE attivita_programmate ADD COLUMN styles TEXT")
            except: pass

            # Certificati Campione
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS certificati_campione (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modello TEXT,
                    costruttore TEXT,
                    matricola TEXT,
                    range_strumento TEXT,
                    errore_max TEXT,
                    certificato TEXT,
                    scadenza TEXT,
                    emissione TEXT,
                    id_coemi TEXT,
                    stato TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # --- Indexes (Performance) ---
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_year ON contabilita(year)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_nprev ON contabilita(n_prev)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_giorn_year ON giornaliere(year)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_giorn_data ON giornaliere(data)")

            conn.commit()

    def _init_timbrature(self):
        with self.get_connection(self.DB_TIMBRATURE) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timbrature (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT,
                    ingresso TEXT,
                    uscita TEXT,
                    nome TEXT,
                    cognome TEXT,
                    presenza_ts TEXT,
                    sito_timbratura TEXT,
                    UNIQUE(data, ingresso, uscita, nome, cognome)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dipendenti (
                    nome TEXT,
                    cognome TEXT,
                    reparto TEXT,
                    PRIMARY KEY (nome, cognome)
                )
            ''')

            # --- Indexes ---
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_data ON timbrature(data)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_nome_cogn ON timbrature(nome, cognome)")

            conn.commit()

# Global Accessor
db_manager = DatabaseManager()
