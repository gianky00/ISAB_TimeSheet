import sqlite3

db_path = r'C:\Users\Coemi\AppData\Local\SyncroJob\data\contabilita.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Conteggio strumenti
    cursor.execute("SELECT COUNT(DISTINCT matricola) FROM certificati_campione")
    count = cursor.fetchone()[0]
    print(f"Strumenti unici nel DB: {count}")

    # Elenco strumenti
    cursor.execute("SELECT matricola, certificato, modello FROM certificati_campione GROUP BY matricola")
    rows = cursor.fetchall()
    print("\nElenco strumenti presenti:")
    for r in rows:
        print(f"Matricola: {r[0]} | Cert: {r[1]} | Modello: {r[2]}")

    # Conteggio totale righe
    cursor.execute("SELECT COUNT(*) FROM certificati_campione")
    total = cursor.fetchone()[0]
    print(f"\nTotale certificati (righe): {total}")

    conn.close()
except Exception as e:
    print(f"Errore: {e}")
