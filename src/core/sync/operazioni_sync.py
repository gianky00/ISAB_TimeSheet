"""SyncroJob - Operazioni Sync Engine.

Gestisce sincronizzazioni massive (DELETE ALL + INSERT) per AttivitàProgrammate e Scarico Ore.
"""

from pathlib import Path
from typing import Any

from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter
from src.core.sync.base import BaseSyncEngine


class OperazioniSyncEngine(BaseSyncEngine):
    """Motore di sync per operazioni massive ad alte prestazioni."""

    @classmethod
    def sync_attivita_programmate(
        cls, db_path: Path, rows_to_insert: list[tuple[Any, ...]]
    ) -> tuple[int, int]:
        """Sincronizzazione per AttivitàProgrammate."""
        db_cols = [*list(ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING.values()), "styles"]

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM attivita_programmate")
            old_count = cursor.fetchone()[0]

            cursor.execute("DELETE FROM attivita_programmate")

            if rows_to_insert:
                safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in db_cols])
                placeholders = ", ".join(["?"] * len(db_cols))
                data = [tuple(cls._clean_value(x) for x in r) for r in rows_to_insert]
                cursor.executemany(
                    f"INSERT INTO attivita_programmate ({safe_cols}) VALUES ({placeholders})",  # nosec B608
                    data,
                )

            new_count = len(rows_to_insert) if rows_to_insert else 0
            conn.commit()

            return max(0, new_count - old_count), max(0, old_count - new_count)

    @classmethod
    def sync_scarico_ore(cls, db_path: Path, rows_to_insert: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizzazione ultra-ottimizzata per Scarico Ore."""
        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM scarico_ore")
            old_count = cursor.fetchone()[0]

            cursor.execute("DELETE FROM scarico_ore")

            if rows_to_insert:
                columns = ExcelImporter.SCARICO_ORE_COLS
                safe_columns = [cls._validate_identifier(c) for c in columns]
                placeholders = ", ".join(["?"] * len(columns))
                insert_query = f"INSERT INTO scarico_ore ({', '.join(safe_columns)}) VALUES ({placeholders})"  # nosec B608

                batch_size = 10000
                all_data = [tuple(cls._clean_value(x) for x in r) for r in rows_to_insert]

                for i in range(0, len(all_data), batch_size):
                    batch = all_data[i : i + batch_size]
                    cursor.executemany(insert_query, batch)

            new_count = len(rows_to_insert)
            conn.commit()

            return max(0, new_count - old_count), max(0, old_count - new_count)
