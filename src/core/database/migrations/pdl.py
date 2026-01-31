import sqlite3


def mig_pdl_v1(conn: sqlite3.Connection):
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


def mig_pdl_v2(conn: sqlite3.Connection):
    """Aggiunge vincolo UNIQUE su n_pdl e pulisce duplicati (v2)"""
    cursor = conn.cursor()
    # 1. Rimuovi duplicati mantenendo il più recente (o ID più alto)
    cursor.execute(
        """
        DELETE FROM pdl
        WHERE id NOT IN (
            SELECT MAX(id) FROM pdl GROUP BY n_pdl
        )
    """
    )
    # 2. Per aggiungere un vincolo UNIQUE in SQLite su una tabella esistente,
    # bisogna ricreare la tabella (non supportato direttamente da ALTER TABLE).
    cursor.execute("CREATE TABLE pdl_new AS SELECT * FROM pdl WHERE 1=0")
    # Modifica lo schema della nuova tabella (non semplicissimo con CREATE TABLE AS)
    # Meglio ricreare esplicitamente
    cursor.execute("DROP TABLE pdl_new")
    cursor.execute(
        """
        CREATE TABLE pdl_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            n_pdl TEXT UNIQUE,
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
    cursor.execute("INSERT INTO pdl_new SELECT * FROM pdl")
    cursor.execute("DROP TABLE pdl")
    cursor.execute("ALTER TABLE pdl_new RENAME TO pdl")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdl_n_pdl ON pdl(n_pdl)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdl_sito ON pdl(sito)")
