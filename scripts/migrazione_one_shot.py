import sys
from pathlib import Path

# Aggiungiamo la root del progetto al path python per importare i moduli src
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.database import db_manager  # noqa: E402
from src.core.employees import employee_manager  # noqa: E402


def run_migration():
    print("--- Inizio Migrazione Anagrafica ---")

    # 1. Assicuriamoci che il DB sia inizializzato con lo schema corretto
    print("Inizializzazione Schema DB...")
    db_manager.init_db()

    # 2. Percorso del CSV
    csv_path = project_root / "anagrafica_dipendenti.csv"

    if not csv_path.exists():
        print(f"ERRORE: File {csv_path} non trovato!")
        return

    print(f"Lettura da: {csv_path}")

    # 3. Esegui import
    try:
        count = employee_manager.import_from_csv(str(csv_path))
        print(f"--- SUCCESSO: {count} dipendenti importati/aggiornati nel Database ---")

        # 4. Verifica
        rows = employee_manager.get_all_employees()
        print(f"Verifica DB: Trovati {len(rows)} record nella tabella 'dipendenti'.")
        if rows:
            print(f"Esempio primo record: {dict(rows[0])}")

    except Exception as e:
        print(f"ERRORE CRITICO: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    run_migration()
