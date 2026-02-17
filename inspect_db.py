import sqlite3

db_path = r"C:/Users/gianc/Desktop/SCRIPT/report-attivita-app/report_attivita.db"
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]

    print(f"Found {len(tables)} tables.")

    print(f"Found {len(tables)} tables.")

    print("\n--- ANALYSIS ---")
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [c[1].lower() for c in cursor.fetchall()]

        has_pdl = "pdl" in columns or "n_pdl" in columns or "codice_pdl" in columns

        status = "HAS_PDL" if has_pdl else "NO_PDL"
        if status == "NO_PDL" and ("relazione" in table or "intervento" in table or "report" in table):
            status = "POTENTIAL_ORPHAN"

        print(f"TABLE: {table} -> {status}")
        if status == "POTENTIAL_ORPHAN":
            print(f"   Columns: {columns}")

    conn.close()

except Exception as e:
    print(f"Error: {e}")
