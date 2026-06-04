"""Modulo Timbrature."""

import sqlite3


def mig_timbrature_v1(conn: sqlite3.Connection) -> None:
    """Schema Iniziale Timbrature (v1)."""
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


def mig_timbrature_v2(conn: sqlite3.Connection) -> None:
    """Ottimizzazione indici Timbrature (v2)."""
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_nome_cognome ON timbrature(cognome, nome)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dip_nome_cognome ON dipendenti(cognome, nome)")


def mig_timbrature_v3(conn: sqlite3.Connection) -> None:
    """Aggiunge colonne codice_fiscale e ore_effettive (v3)."""
    cursor = conn.cursor()
    # Verifichiamo se le colonne esistono già per evitare errori
    cursor.execute("PRAGMA table_info(timbrature)")
    columns = [row[1] for row in cursor.fetchall()]

    if "codice_fiscale" not in columns:
        cursor.execute("ALTER TABLE timbrature ADD COLUMN codice_fiscale TEXT")
    if "ore_effettive" not in columns:
        cursor.execute("ALTER TABLE timbrature ADD COLUMN ore_effettive TEXT")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_cf ON timbrature(codice_fiscale)")


def mig_timbrature_v4(conn: sqlite3.Connection) -> None:
    """Aggiunge tutte le colonne mancanti rilevate dal file Excel reale (v4)."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(timbrature)")
    existing = [row[1] for row in cursor.fetchall()]

    new_cols = {
        "id_dipendente": "TEXT",
        "fornitore": "TEXT",
        "codice_rilpres": "TEXT",
        "numero_badge": "TEXT",
        "codice_qualifica": "TEXT",
        "specializzazione": "TEXT",
        "societa_ospitante": "TEXT",
        "data_ins": "TEXT",
    }

    for col, col_type in new_cols.items():
        if col not in existing:
            cursor.execute(f"ALTER TABLE timbrature ADD COLUMN {col} {col_type}")  # nosec B608
