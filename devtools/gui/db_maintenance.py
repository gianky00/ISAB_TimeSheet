"""SyncroJob - Database Maintenance Tool
Esegue operazioni di manutenzione ordinaria su TUTTI i database dell'applicazione:
1. Integrity Check
2. Vacuum (Compattazione)
3. Analyze (Ottimizzazione Query Planner)
"""

import contextlib
import io
import sqlite3
import sys
from pathlib import Path

from platformdirs import user_data_dir

# Fix encoding for Windows console to support emoji
if sys.platform == "win32":
    with contextlib.suppress(Exception):
        if hasattr(sys.stdout, "buffer"):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "buffer"):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Configurazione Percorsi
APP_NAME = "SyncroJob"
CONFIG_DIR = Path(user_data_dir(APP_NAME, appauthor=False))
DATA_DIR = CONFIG_DIR / "data"

# Lista dei database conosciuti
DATABASES = [
    "contabilita.db",
    "timbrature_Isab.db",
    "pdl.db",
    "storico_oda.db",
    "anagrafica_dipendenti.db",
    "audit_log.db",
]


def maintain_db(db_name: str) -> None:
    """Esegue operazioni di manutenzione (integrity check, vacuum, analyze) su un singolo database.

    Args:
        db_name: Nome del file database presente nella cartella dati.
    """
    db_path = DATA_DIR / db_name
    print(f"\n📦 ANALISI: {db_name}")

    if not db_path.exists():
        print("   ⚠️  Saltato: File non trovato.")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # 1. Integrity Check
            print("   🔍 Checking Integrity...", end=" ")
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            if result[0] == "ok":
                print("✅ OK")
            else:
                print(f"❌ ERRORE: {result[0]}")
                return

            # 2. Vacuum
            print("   🧹 Vacuuming...", end=" ")
            cursor.execute("VACUUM")
            print("✅ Done")

            # 3. Analyze
            print("   📊 Analyzing...", end=" ")
            cursor.execute("ANALYZE")
            print("✅ Done")

            # 4. Check Size
            size_mb = db_path.stat().st_size / (1024 * 1024)
            print(f"   📉 Size: {size_mb:.2f} MB")

    except Exception as e:
        print(f"   ❌ ERRORE CRITICO: {e}")


def main() -> None:
    """Entry point per il tool di manutenzione database."""
    print("🔧 SYNCROJOB DB MAINTENANCE TOOL")
    print(f"📂 Data Dir: {DATA_DIR}\n")

    if not DATA_DIR.exists():
        print("❌ Errore: Directory dati non trovata.")
        sys.exit(1)

    for db in DATABASES:
        maintain_db(db)

    print("\n✨ Manutenzione completata.")


if __name__ == "__main__":
    main()
