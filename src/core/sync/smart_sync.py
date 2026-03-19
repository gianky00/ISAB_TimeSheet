"""
SyncroJob - Smart Sync Engine
Gestisce sincronizzazioni intelligenti (UPSERT) con calcolo esatto del delta via EXCEPT.
"""

from pathlib import Path
from typing import Any

from src.core.database import db_manager
from src.core.sync.base import BaseSyncEngine


class SmartSyncEngine(BaseSyncEngine):
    """Motore di sync intelligente per tabelle con chiavi primarie (Certificati, ODA)."""

    @classmethod
    def sync_upsert_smart(
        cls, db_path: Path, table_name: str, columns: list[str], new_data: list[tuple[Any, ...]], conflict_cols: list[str] | None = None
    ) -> tuple[int, int]:
        """Esegue Upsert calcolando esattamente le righe modificate o aggiunte."""
        if not new_data:
            return 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            temp_table = cls._create_temp_table(cursor, table_name, columns)

            safe_table = cls._validate_identifier(table_name)
            safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
            safe_cast_cols = ", ".join([f'CAST("{cls._validate_identifier(c)}" AS TEXT)' for c in columns])
            placeholders = ", ".join(["?"] * len(columns))

            data = [tuple(cls._clean_value(x) for x in r) for r in new_data]
            cursor.executemany(f"INSERT INTO {temp_table} VALUES ({placeholders})", data)  # nosec B608

            # Calcola Diff (Righe in Temp diverse da Main)
            q_diff = f"""
                SELECT COUNT(*) FROM (
                    SELECT {safe_cols} FROM {temp_table}
                    EXCEPT
                    SELECT {safe_cast_cols} FROM {safe_table}
                )
            """  # nosec B608
            cursor.execute(q_diff)
            added_or_updated = cursor.fetchone()[0]

            # Upsert
            if conflict_cols:
                safe_conflict = ", ".join([f'"{cls._validate_identifier(c)}"' for c in conflict_cols])
                update_assignments = ", ".join([f'"{cls._validate_identifier(c)}" = excluded."{cls._validate_identifier(c)}"' for c in columns if c not in conflict_cols])

                # Se non ci sono colonne da aggiornare (tutte in conflict_cols), facciamo DO NOTHING
                if update_assignments:
                    q_upsert = f"""
                        INSERT INTO {safe_table} ({safe_cols})
                        SELECT {safe_cols} FROM {temp_table}
                        WHERE true
                        ON CONFLICT({safe_conflict}) DO UPDATE SET
                        {update_assignments}
                    """  # nosec B608
                else:
                    q_upsert = f"""
                        INSERT INTO {safe_table} ({safe_cols})
                        SELECT {safe_cols} FROM {temp_table}
                        WHERE true
                        ON CONFLICT({safe_conflict}) DO NOTHING
                    """  # nosec B608
            else:
                q_upsert = (
                    f"INSERT OR REPLACE INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM {temp_table}"  # nosec B608
                )

            cursor.execute(q_upsert)
            conn.commit()

            return added_or_updated, 0
