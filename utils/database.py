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
    # Numero OdA, Posizione OdA, Codice Fiscale, Ingresso, Uscita,
    # Tipo Prestazione, C, M, Str D, Str N, Str F D, Str F N,
    # Sq, Nota D, Nota S, F S, G T

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        "numero_oda", "posizione_oda", "codice_fiscale", "ingresso", "uscita",
        "tipo_prestazione", "c", "m", "str_d", "str_n", "str_f_d", "str_f_n",
        "sq", "nota_d", "nota_s", "f_s", "g_t"
    ]

    placeholders = ", ".join(["?"] * len(columns))
    col_names = ", ".join(columns)

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

def clear_activities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM activities")
    conn.commit()
    conn.close()
