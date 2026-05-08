import os
import sqlite3

db_path = os.path.expandvars(r"%LOCALAPPDATA%\SyncroJob\data\contabilita.db")
print(f"Checking DB at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get total count
    cursor.execute("SELECT COUNT(*) FROM certificati_campione")
    count = cursor.fetchone()[0]
    print(f"Total rows in DB: {count}")

    # Check CAT01563
    cursor.execute("SELECT * FROM certificati_campione WHERE id_coemi='CAT01563'")
    row = cursor.fetchone()
    print(f"CAT01563 data: {row}")

    # Get column names
    cursor.execute("PRAGMA table_info(certificati_campione)")
    cols = [c[1] for c in cursor.fetchall()]
    print(f"Columns: {cols}")

    conn.close()
except Exception as e:
    print(f"Error: {e}")
