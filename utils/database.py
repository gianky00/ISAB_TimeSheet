import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DB_FILE = DATA_DIR / "database.db"

def get_connection():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Columns requested:
    # Stato (nuova), Numero OdA, Posizione OdA, Codice Fiscale, Ingresso, Uscita,
    # Tipo Prestazione, C, M, Str D, Str N, Str F D, Str F N,
    # Sq, Nota D, Nota S, F S, G T

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stato TEXT DEFAULT 'da_processare',
            data_ts TEXT,
            numero_oda TEXT,
            posizione_oda TEXT,
            codice_fiscale TEXT,
            ingresso TEXT,
            uscita TEXT,
            tipo_prestazione TEXT,
            c TEXT,
            m TEXT,
            str_d TEXT,
            str_n TEXT,
            str_f_d TEXT,
            str_f_n TEXT,
            sq TEXT,
            nota_d TEXT,
            nota_s TEXT,
            f_s TEXT,
            g_t TEXT
        )
    """)
    
    # Verifica se le colonne esistono già (per DB esistenti)
    cursor.execute("PRAGMA table_info(activities)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'stato' not in columns:
        cursor.execute("ALTER TABLE activities ADD COLUMN stato TEXT DEFAULT 'da_processare'")
    if 'data_ts' not in columns:
        cursor.execute("ALTER TABLE activities ADD COLUMN data_ts TEXT")
    
    conn.commit()
    conn.close()

def insert_activity(data):
    """
    Inserts a single record.
    data: dict matching column names (excluding id)
    """
    conn = get_connection()
    cursor = conn.cursor()

    columns = [
        "stato", "data_ts", "numero_oda", "posizione_oda", "codice_fiscale", "ingresso", "uscita",
        "tipo_prestazione", "c", "m", "str_d", "str_n", "str_f_d", "str_f_n",
        "sq", "nota_d", "nota_s", "f_s", "g_t"
    ]

    placeholders = ", ".join(["?"] * len(columns))
    col_names = ", ".join(columns)

    # Default stato a 'da_processare' se non specificato
    if "stato" not in data:
        data["stato"] = "da_processare"

    values = [data.get(col, "") for col in columns]

    cursor.execute(f"INSERT INTO activities ({col_names}) VALUES ({placeholders})", values)
    conn.commit()
    conn.close()

def get_all_activities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_activity_status(activity_id, new_status):
    """
    Aggiorna lo stato di una singola attività.
    new_status: 'da_processare', 'completato', 'errore: <descrizione>'
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE activities SET stato = ? WHERE id = ?", (new_status, activity_id))
    conn.commit()
    conn.close()

def clear_activities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM activities")
    conn.commit()
    conn.close()

def reset_all_status():
    """Resetta tutti gli stati a 'da_processare'"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE activities SET stato = 'da_processare'")
    conn.commit()
    conn.close()
