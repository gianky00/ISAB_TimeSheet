import contextlib
import sqlite3


def mig_contabilita_v1(conn: sqlite3.Connection) -> None:
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
            scadenza TEXT, emissione TEXT, id_strumento TEXT, stato TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_year ON contabilita(year)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_giorn_data ON giornaliere(data)")


def mig_contabilita_v2(conn: sqlite3.Connection) -> None:
    """Ottimizzazione indici Contabilità (v2)"""
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_n_prev ON contabilita(n_prev)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_odc ON contabilita(odc)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cont_tcl ON contabilita(tcl)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_giorn_odc ON giornaliere(odc)")


def mig_contabilita_v3(conn: sqlite3.Connection) -> None:
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


def mig_contabilita_v4(conn: sqlite3.Connection) -> None:
    """Risoluzione duplicati Certificati Campione e indice univoco (v4)"""
    cursor = conn.cursor()
    # 1. Pulizia duplicati esistenti (mantiene solo il primo ID trovato per coppia matricola-certificato)
    cursor.execute(
        """
        DELETE FROM certificati_campione
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM certificati_campione
            GROUP BY matricola, certificato
        )
    """
    )
    # 2. Indice univoco per prevenire futuri duplicati via INSERT OR REPLACE
    cursor.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_cert_unique ON certificati_campione(matricola, certificato)"
    )


def mig_contabilita_v5(conn: sqlite3.Connection) -> None:
    """Aggiunta colonne annotazioni e ubicazione a certificati_campione (v5)"""
    cursor = conn.cursor()
    # Ignoriamo l'errore se le colonne esistono già
    with contextlib.suppress(sqlite3.OperationalError):
        cursor.execute("ALTER TABLE certificati_campione ADD COLUMN annotazioni TEXT DEFAULT ''")
    with contextlib.suppress(sqlite3.OperationalError):
        cursor.execute("ALTER TABLE certificati_campione ADD COLUMN ubicazione TEXT DEFAULT ''")


def mig_contabilita_v6(conn: sqlite3.Connection) -> None:
    """Rimozione vincolo UNIQUE per permettere importazione 'Tale e Quale' (v6)"""
    cursor = conn.cursor()
    cursor.execute("DROP INDEX IF EXISTS idx_cert_unique")


def mig_contabilita_v7(conn: sqlite3.Connection) -> None:
    """Ridenominazione id_coemi in id_strumento (v7)"""
    cursor = conn.cursor()
    # Verifica se la colonna id_coemi esiste prima di rinominare
    cursor.execute("PRAGMA table_info(certificati_campione)")
    cols = [row[1] for row in cursor.fetchall()]
    if "id_coemi" in cols and "id_strumento" not in cols:
        with contextlib.suppress(sqlite3.OperationalError):
            cursor.execute("ALTER TABLE certificati_campione RENAME COLUMN id_coemi TO id_strumento")
