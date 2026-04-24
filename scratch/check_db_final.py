import sqlite3

db_path = r'C:\Users\Coemi\AppData\Local\SyncroJob\data\contabilita.db'

def check_db_final() -> None:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Conteggio totale
        cursor.execute("SELECT COUNT(*) FROM certificati_campione")
        count = cursor.fetchone()[0]
        print(f"TOTALE RIGHE NEL DATABASE: {count}")

        # Vediamo i primi ID-COEMI per capire se sono duplicati o diversi
        cursor.execute("SELECT id_coemi, matricola, certificato FROM certificati_campione LIMIT 20")
        rows = cursor.fetchall()
        print("\nEsempio primi 20 record:")
        for r in rows:
            print(f"ID: {r[0]} | MATR: {r[1]} | CERT: {r[2]}")

        conn.close()
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    check_db_final()
