import os
import sqlite3

db_path = r"C:/Users/Coemi/Desktop/SCRIPT/report-attivita-app/report-attivita.db"
print(f"Verifica esistenza file: {os.path.exists(db_path)}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("\nTABELLE TROVATE:")
    for table in tables:
        t_name = table[0]
        print(f"\n--- {t_name} ---")
        cursor.execute(f"PRAGMA table_info('{t_name}')")
        cols = cursor.fetchall()
        for col in cols:
            print(f"  {col[1]} ({col[2]})")

except Exception as e:
    print(f"Errore: {e}")
finally:
    if 'conn' in locals():
        conn.close()
