r"""
Script per rimuovere i duplicati dalla tabella attivita_programmate.
Esegui con: .venv\Scripts\python.exe scripts\cleanup_duplicates.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.config_manager import CONFIG_DIR
from src.core.database import db_manager


def cleanup_attivita_duplicates():  # noqa: ANN201
    db_path = CONFIG_DIR / "data" / "contabilita.db"

    if not db_path.exists():
        print("Database non trovato!")
        return

    print("=" * 60)
    print("PULIZIA DUPLICATI - Attivita Programmate")
    print("=" * 60)

    with db_manager.get_connection(db_path) as conn:
        cursor = conn.cursor()

        # Conta righe totali
        cursor.execute("SELECT COUNT(*) FROM attivita_programmate")
        total_before = cursor.fetchone()[0]
        print(f"\nRighe totali PRIMA: {total_before}")

        # Trova duplicati
        cursor.execute(
            """
            SELECT ps, area, pdl, descrizione, COUNT(*) as cnt
            FROM attivita_programmate
            GROUP BY ps, area, pdl, descrizione
            HAVING cnt > 1
        """
        )
        duplicates = cursor.fetchall()
        print(f"Gruppi di duplicati trovati: {len(duplicates)}")

        if duplicates:
            print("\nEsempi di duplicati:")
            for dup in duplicates[:5]:
                print(f"  - PS={dup[0]}, PDL={dup[2]}, count={dup[4]}")

        # Rimuovi duplicati mantenendo solo la prima occorrenza (id minore)
        cursor.execute(
            """
            DELETE FROM attivita_programmate
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM attivita_programmate
                GROUP BY ps, area, pdl, descrizione
            )
        """
        )

        deleted = cursor.rowcount
        conn.commit()

        # Conta righe dopo
        cursor.execute("SELECT COUNT(*) FROM attivita_programmate")
        total_after = cursor.fetchone()[0]

        print(f"\nRighe eliminate: {deleted}")
        print(f"Righe totali DOPO: {total_after}")

    print("\n" + "=" * 60)
    print("PULIZIA COMPLETATA")
    print("=" * 60)


if __name__ == "__main__":
    cleanup_attivita_duplicates()
