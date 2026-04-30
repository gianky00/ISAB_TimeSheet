import re
import sqlite3

db_path = r"C:\Users\Coemi\AppData\Local\SyncroJob\data\contabilita.db"


def clean_annotations() -> None:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Selezioniamo tutte le annotazioni non vuote
        cursor.execute(
            "SELECT rowid, annotazioni FROM certificati_campione WHERE annotazioni IS NOT NULL AND annotazioni != ''"
        )
        rows = cursor.fetchall()

        cleaned_count = 0
        # Pattern che identifica "6gg", "tra 6gg", "336gg fa", "340gg rim." ecc.
        # Cerchiamo la presenza di numeri seguiti da 'gg' o parole chiave come 'fa', 'rim', 'tra' vicino a 'gg'
        pattern = re.compile(r".*(\d+ ?gg|gg fa|gg rim|tra \d+).*", re.IGNORECASE)

        for rowid, ann in rows:
            if pattern.match(ann):
                # Svuotiamo la cella
                cursor.execute("UPDATE certificati_campione SET annotazioni = '' WHERE rowid = ?", (rowid,))
                cleaned_count += 1

        conn.commit()
        conn.close()
        print("Pulizia completata con successo!")
        print(f"Annotazioni rimosse: {cleaned_count}")

    except Exception as e:
        print(f"Errore durante la pulizia: {e}")


if __name__ == "__main__":
    clean_annotations()
