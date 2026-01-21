"""
SyncroJob - Database Maintenance Tool
Esegue operazioni di manutenzione ordinaria sul database SQLite:
1. Integrity Check
2. Vacuum (Compattazione)
3. Analyze (Ottimizzazione Query Planner)
"""

import sqlite3
import sys
from pathlib import Path

# Cerchiamo il DB nella posizione standard
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "data" / "syncrojob.db"

def maintenance():
    print(f"🔧 AVVIO MANUTENZIONE DATABASE: {DB_PATH}")
    
    if not DB_PATH.exists():
        print(f"❌ Errore: Database non trovato in {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Integrity Check
        print("🔍 1. Esecuzione PRAGMA integrity_check...", end=" ")
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        if result[0] == "ok":
            print("✅ OK")
        else:
            print(f"❌ ERRORE: {result[0]}")
            conn.close()
            return

        # 2. Vacuum
        print("🧹 2. Esecuzione VACUUM (Compattazione)...", end=" ")
        cursor.execute("VACUUM")
        print("✅ Completato")

        # 3. Analyze
        print("📊 3. Esecuzione ANALYZE (Ottimizzazione indici)...", end=" ")
        cursor.execute("ANALYZE")
        print("✅ Completato")
        
        # 4. Check Size
        size_mb = DB_PATH.stat().st_size / (1024 * 1024)
        print(f"📉 Dimensione attuale DB: {size_mb:.2f} MB")

        conn.close()
        print("\n✨ Manutenzione completata con successo.")

    except Exception as e:
        print(f"\n❌ ERRORE CRITICO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    maintenance()
