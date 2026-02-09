import sqlite3


def mig_dipendenti_v1(conn: sqlite3.Connection) -> None:
    """Schema Iniziale Dipendenti (v1)"""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dipendenti (
            id_risorsa INTEGER PRIMARY KEY,
            cognome TEXT NOT NULL,
            nome TEXT NOT NULL,
            data_nascita TEXT,
            badge TEXT,
            data_assunzione TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dip_cognome_nome ON dipendenti(cognome, nome)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dip_badge ON dipendenti(badge)")


def mig_dipendenti_v2(conn: sqlite3.Connection) -> None:
    """Aggiunge colonna codice_fiscale (v2)"""
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE dipendenti ADD COLUMN codice_fiscale TEXT")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dip_cf ON dipendenti(codice_fiscale)")


def mig_dipendenti_v3(conn: sqlite3.Connection) -> None:
    """Aggiunge colonna monitoraggio_attivo per bypass manuale (v3)"""
    cursor = conn.cursor()
    # Verifica se la colonna esiste già per evitare errori
    cursor.execute("PRAGMA table_info(dipendenti)")
    columns = [row[1] for row in cursor.fetchall()]
    if "monitoraggio_attivo" not in columns:
        cursor.execute("ALTER TABLE dipendenti ADD COLUMN monitoraggio_attivo INTEGER DEFAULT 1")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_dip_monitoraggio ON dipendenti(monitoraggio_attivo)")
