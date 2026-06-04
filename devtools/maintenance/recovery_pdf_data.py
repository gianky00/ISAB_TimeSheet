import sqlite3

from src.application.services.paths import DB_DIR

# Mappa estratta via OCR dal PDF del 29-04-2026
# Formato: "ID_COEMI": ("UBICAZIONE", "ANNOTAZIONI")
recovery_data = {
    "CAT01367": ("UFFICIO STRU", ""),
    "CAT01527": ("UFFICIO STRU", ""),
    "CAT01563": ("SEDE", ""),
    "CAT01647": ("UFFICIO STRU", ""),
    "CAT01674": ("SEDE", ""),
    "CAT01902": ("UFFICIO STRU", ""),
    "CAT01905": ("UFFICIO STRU", ""),
    "CAT01906": ("OFFICINA STRU", "TEST PENUM. 3-15 PSI"),
    "CAT01944": ("SEDE", ""),
    "CAT03500": ("UFFICIO STRU", ""),
    "CAT03501": ("UFFICIO STRU", ""),
    "CAT03502": ("UFFICIO STRU", ""),
    "CAT03503": ("OFFICINA STRU", "INST. SU POMPETTA H2O"),
    "CAT03950": ("UFFICIO STRU", ""),
    "CAT03951": ("UFFICIO STRU", ""),
    "CAT04119": ("UFFICIO STRU", ""),
    "CAT04120": ("UFFICIO STRU", ""),
    "CAT04123": ("UFFICIO STRU", ""),
    "CAT04129": ("UFFICIO STRU", ""),
    "CAT04130": ("UFFICIO STRU", ""),
    "CAT04131": ("UFFICIO STRU", ""),
    "CAT09190": ("ASSEGNATO AL TECNICO", "GUARINO RICCARDO"),
    "CAT09191": ("ASSEGNATO AL TECNICO", "TARASCIO BENITO"),
    "CAT09194": ("ASSEGNATO AL TECNICO", "MILLO FRANCESCO"),
    "CAT09195": ("UFFICIO STRU", ""),
    "CAT09250": ("UFFICIO STRU", ""),
    "CAT09251": ("UFFICIO STRU", ""),
    "CAT09252": ("UFFICIO STRU", ""),
    "CAT09380": ("UFFICIO STRU", ""),
    "CAT09381": ("UFFICIO STRU", ""),
    "CAT09382": ("UFFICIO STRU", ""),
}

def restore_metadata() -> None:
    db_path = DB_DIR / "contabilita.db"
    if not db_path.exists():
        print(f"Errore: Database non trovato in {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    updated_count = 0
    try:
        for id_coemi, (ubicazione, annotazioni) in recovery_data.items():
            # Cerchiamo lo strumento per ID COEMI
            # Nota: usiamo LIKE o stringa esatta a seconda di come è salvato nel DB
            cursor.execute(
                "UPDATE certificati_campione SET ubicazione = ?, annotazioni = ? WHERE id_coemi = ?",
                (ubicazione, annotazioni, id_coemi)
            )
            if cursor.rowcount > 0:
                updated_count += cursor.rowcount
                print(f"[OK] Ripristinato {id_coemi}: {ubicazione} | {annotazioni}")
            else:
                print(f"[!] ID {id_coemi} non trovato nel database attuale.")

        conn.commit()
        print("\n--- RECOVERY COMPLETATO ---")
        print(f"Strumenti aggiornati: {updated_count}")
    except Exception as e:
        print(f"Errore durante il ripristino: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    restore_metadata()
