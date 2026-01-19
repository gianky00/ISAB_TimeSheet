"""
SyncroJob - Database Manager
Centralized SQLite database management with Thread Safety.
"""

import logging
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, List

from src.core.config_manager import CONFIG_DIR

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Singleton class to manage SQLite connections with thread safety and WAL mode.
    Implements a write lock to prevent contention.
    """

    _instance = None
    _write_lock = threading.Lock()

    # Predefined Paths
    DB_CONTABILITA = CONFIG_DIR / "data" / "contabilita.db"
    DB_TIMBRATURE = CONFIG_DIR / "data" / "timbrature_Isab.db"
    DB_PDL = CONFIG_DIR / "data" / "pdl.db"
    DB_STORICO_ODA = CONFIG_DIR / "data" / "storico_oda.db"

    def __new__(cls):
        """Pattern Singleton per il gestore database."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._ensure_dirs()
        return cls._instance

    def _ensure_dirs(self):
        """Ensures the data directory exists."""
        (CONFIG_DIR / "data").mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(
        self, db_path: Path, read_only: bool = False, timeout: float = 30.0
    ) -> Generator[sqlite3.Connection, None, None]:
        """
        Yields a SQLite connection with Thread Safety features.
        - WAL Mode enabled for concurrent read/write.
        - Increased timeout for locked databases.
        - Auto-commit handling via context manager.
        """
        uri = f"file:{db_path.absolute()}"
        if read_only:
            uri += "?mode=ro"

        conn = None
        try:
            # check_same_thread=False is safe when using one connection per context/thread
            conn = sqlite3.connect(
                uri, uri=True, timeout=timeout, check_same_thread=False
            )

            # Performance & Concurrency Optimizations
            if not read_only:
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("PRAGMA synchronous=NORMAL;")
                conn.execute(f"PRAGMA busy_timeout={int(timeout * 1000)};")

            # Enable Foreign Keys for both read and write
            conn.execute("PRAGMA foreign_keys = ON;")

            yield conn

            if not read_only and conn.in_transaction:
                conn.commit()

        except sqlite3.OperationalError as e:
            logger.error(f"Database Operational Error ({db_path.name}): {e}")
            if conn:
                conn.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected Database Error ({db_path.name}): {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(
        self, db_path: Path, query: str, params: tuple = (), retry_count: int = 3
    ) -> List[Any]:
        """Executes a query with automatic retries and write synchronization."""
        is_write = not query.strip().upper().startswith("SELECT")

        last_error = None
        for attempt in range(retry_count):
            try:
                # Se è una scrittura, acquisiamo il lock globale per questo processo
                if is_write:
                    self._write_lock.acquire()

                try:
                    with self.get_connection(db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute(query, params)
                        if not is_write:
                            return cursor.fetchall()
                        return []
                finally:
                    if is_write:
                        self._write_lock.release()

            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() or "busy" in str(e).lower():
                    last_error = e
                    time.sleep(0.1 * (attempt + 1))
                    continue
                raise

        logger.error(
            f"Failed to execute query after {retry_count} retries: {last_error}"
        )
        if last_error:
            raise last_error
        raise sqlite3.OperationalError(
            f"Failed to execute query after {retry_count} retries"
        )

    def init_db(self):
        """Initializes schema for all databases using the migration system."""
        self._run_migrations(
            self.DB_CONTABILITA, self.MIGRATIONS_CONTABILITA, "Contabilita"
        )
        self._run_migrations(
            self.DB_TIMBRATURE, self.MIGRATIONS_TIMBRATURE, "Timbrature"
        )
        self._run_migrations(self.DB_PDL, self.MIGRATIONS_PDL, "PDL")
        self._run_migrations(
            self.DB_STORICO_ODA, self.MIGRATIONS_STORICO_ODA, "Storico OdA"
        )

    def _get_db_version(self, conn: sqlite3.Connection) -> int:
        try:
            return conn.execute("PRAGMA user_version").fetchone()[0]
        except Exception:
            return 0

    def _set_db_version(self, conn: sqlite3.Connection, version: int):
        conn.execute(f"PRAGMA user_version = {version}")

    def _run_migrations(self, db_path: Path, migrations: dict, db_name: str):
        """
        Executes pending migrations for a specific database.
        """
        with self.get_connection(db_path) as conn:
            current_ver = self._get_db_version(conn)
            target_ver = max(migrations.keys()) if migrations else 0

            if current_ver < target_ver:
                logger.info(
                    f"[{db_name}] Database outdated (v{current_ver}). Migrating to v{target_ver}..."
                )

                try:
                    # Apply migrations sequentially
                    for ver in range(current_ver + 1, target_ver + 1):
                        if ver in migrations:
                            logger.info(f"[{db_name}] Applying migration v{ver}...")
                            migrations[ver](conn)
                            self._set_db_version(conn, ver)
                            logger.info(f"[{db_name}] Migration v{ver} completed.")

                    logger.info(f"[{db_name}] All migrations completed successfully.")
                except Exception as e:
                    logger.critical(f"[{db_name}] Migration failed at step v{ver}: {e}")
                    raise

    # ==========================================
    # DEFINIZIONE MIGRAZIONI CONTABILITÀ
    # ==========================================
    @staticmethod
    def _mig_contabilita_v1(conn: sqlite3.Connection):
        """Schema Iniziale Contabilità (v1)"""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contabilita (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                data_prev TEXT, mese TEXT, n_prev TEXT, totale_prev TEXT,
                attivita TEXT, tcl TEXT, odc TEXT, stato_attivita TEXT,
                tipologia TEXT, ore_sp TEXT, resa TEXT, annotazioni TEXT,
                indirizzo_consuntivo TEXT, nome_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS giornaliere (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                data TEXT, personale TEXT, descrizione TEXT,
                tcl TEXT, odc TEXT, pdl TEXT, inizio TEXT, fine TEXT,
                ore TEXT, n_prev TEXT, nome_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scarico_ore (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT, pers1 TEXT, pers2 TEXT, odc TEXT, pos TEXT,
                dalle TEXT, alle TEXT, totale_ore TEXT, descrizione TEXT,
                finito TEXT, commessa TEXT, styles TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS attivita_programmate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ps TEXT, area TEXT, pdl TEXT, imp TEXT, descrizione TEXT,
                lun TEXT, mar TEXT, mer TEXT, gio TEXT, ven TEXT,
                stato_pdl TEXT, stato_attivita TEXT, data_controllo TEXT,
                personale TEXT, po TEXT, avviso TEXT, styles TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS certificati_campione (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                modello TEXT, costruttore TEXT, matricola TEXT,
                range_strumento TEXT, errore_max TEXT, certificato TEXT,
                scadenza TEXT, emissione TEXT, id_coemi TEXT, stato TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_year ON contabilita(year)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_giorn_data ON giornaliere(data)")

    @staticmethod
    def _mig_contabilita_v2(conn: sqlite3.Connection):
        """Ottimizzazione indici Contabilità (v2)"""
        cursor = conn.cursor()
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_cont_n_prev ON contabilita(n_prev)"
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_odc ON contabilita(odc)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_tcl ON contabilita(tcl)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_giorn_odc ON giornaliere(odc)")

    # ==========================================
    # DEFINIZIONE MIGRAZIONI TIMBRATURE
    # ==========================================
    @staticmethod
    def _mig_timbrature_v1(conn: sqlite3.Connection):
        """Schema Iniziale Timbrature (v1)"""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS timbrature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT, ingresso TEXT, uscita TEXT,
                nome TEXT, cognome TEXT, presenza_ts TEXT, sito_timbratura TEXT,
                UNIQUE(data, ingresso, uscita, nome, cognome)
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dipendenti (
                nome TEXT, cognome TEXT, reparto TEXT, cantiere TEXT,
                PRIMARY KEY (nome, cognome)
            )
        """
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_data ON timbrature(data)")

    @staticmethod
    def _mig_timbrature_v2(conn: sqlite3.Connection):
        """Ottimizzazione indici Timbrature (v2)"""
        cursor = conn.cursor()
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_timb_nome_cognome ON timbrature(cognome, nome)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_dip_nome_cognome ON dipendenti(cognome, nome)"
        )

    # ==========================================
    # DEFINIZIONE MIGRAZIONI PDL
    # ==========================================
    @staticmethod
    def _mig_pdl_v1(conn: sqlite3.Connection):
        """Schema Iniziale PDL (v1) basato su Ricerca.xlsx"""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pdl (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                n_pdl TEXT,
                data_creazione TEXT,
                area TEXT,
                unita TEXT,
                ditta TEXT,
                descrizione_lavoro TEXT,
                tipologia TEXT,
                stato TEXT,
                apparecchiatura TEXT,
                richiedente TEXT,
                data_richiesta TEXT,
                emittente TEXT,
                data_emissione TEXT,
                aprente TEXT,
                data_apertura TEXT,
                priorita TEXT,
                contratto TEXT,
                ordine TEXT,
                sito TEXT,
                importato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdl_n_pdl ON pdl(n_pdl)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdl_sito ON pdl(sito)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdl_area ON pdl(area)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdl_stato ON pdl(stato)")

    # ==========================================
    # DEFINIZIONE MIGRAZIONI STORICO ODA
    # ==========================================
    @staticmethod
    def _mig_storico_oda_v1(conn: sqlite3.Connection):
        """Schema Iniziale Storico OdA (v1)"""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS storico_oda (
                oda TEXT,
                pos_oda TEXT,
                num_riga TEXT,
                org_acq TEXT,
                data_oda TEXT,
                stato TEXT,
                cat_contab TEXT,
                descrizione TEXT,
                qta REAL,
                uom TEXT,
                data_consegna TEXT,
                valore_netto_pos REAL,
                valore_residuo REAL,
                valore_netto_oda REAL,
                divisione TEXT,
                destinatario TEXT,
                nome_destinatario TEXT,
                codice_fornitore TEXT,
                descrizione_fornitore TEXT,
                emittente_fattura TEXT,
                desc_emittente_fattura TEXT,
                contract_card TEXT,
                contratto TEXT,
                posizione_contratto TEXT,
                gruppo_acquisti TEXT,
                indicatore_rilascio TEXT,
                stato_rilascio TEXT,
                attivita TEXT,
                quantita REAL,
                unita_mis TEXT,
                prezzo_lordo REAL,
                testo_breve TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (oda, pos_oda, num_riga)
            )
        """
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_oda_data_oda ON storico_oda(data_oda)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_oda_fornitore ON storico_oda(codice_fornitore)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_oda_contratto ON storico_oda(contratto)"
        )

    @staticmethod
    def _mig_storico_oda_v2(conn: sqlite3.Connection):
        """Fix tipi colonne per evitare overflow (v2)"""
        # Poiché SQLite non supporta ALTER COLUMN facilmente, e i dati sono corrotti/cache,
        # ricreiamo la tabella.
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS storico_oda")
        DatabaseManager._mig_storico_oda_v1(conn)

    @staticmethod
    def _mig_contabilita_v3(conn: sqlite3.Connection):
        """Implementazione FTS5 per ricerche veloci (v3)"""
        cursor = conn.cursor()
        # Tabella virtuale per Contabilità
        cursor.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS contabilita_fts USING fts5(
                n_prev, attivita, odc, annotazioni,
                content='contabilita',
                content_rowid='id'
            )
        """
        )
        # Trigger per mantenere sincronizzato l'indice FTS
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS contabilita_ai AFTER INSERT ON contabilita BEGIN
                INSERT INTO contabilita_fts(rowid, n_prev, attivita, odc, annotazioni)
                VALUES (new.id, new.n_prev, new.attivita, new.odc, new.annotazioni);
            END;
        """
        )
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS contabilita_ad AFTER DELETE ON contabilita BEGIN
                INSERT INTO contabilita_fts(contabilita_fts, rowid, n_prev, attivita, odc, annotazioni)
                VALUES('delete', old.id, old.n_prev, old.attivita, old.odc, old.annotazioni);
            END;
        """
        )
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS contabilita_au AFTER UPDATE ON contabilita BEGIN
                INSERT INTO contabilita_fts(contabilita_fts, rowid, n_prev, attivita, odc, annotazioni)
                VALUES('delete', old.id, old.n_prev, old.attivita, old.odc, old.annotazioni);
                INSERT INTO contabilita_fts(rowid, n_prev, attivita, odc, annotazioni)
                VALUES (new.id, new.n_prev, new.attivita, new.odc, new.annotazioni);
            END;
        """
        )

        # Popolamento iniziale se la tabella non è vuota
        cursor.execute(
            "INSERT INTO contabilita_fts(rowid, n_prev, attivita, odc, annotazioni) SELECT id, n_prev, attivita, odc, annotazioni FROM contabilita"
        )

    # Dizionari di Migrazione
    MIGRATIONS_CONTABILITA = {
        1: _mig_contabilita_v1,
        2: _mig_contabilita_v2,
        3: _mig_contabilita_v3,
    }

    MIGRATIONS_TIMBRATURE = {1: _mig_timbrature_v1, 2: _mig_timbrature_v2}

    MIGRATIONS_PDL = {1: _mig_pdl_v1}

    MIGRATIONS_STORICO_ODA = {1: _mig_storico_oda_v1, 2: _mig_storico_oda_v2}


db_manager = DatabaseManager()
