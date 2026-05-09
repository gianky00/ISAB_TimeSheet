"""
SyncroJob - Smart Sync Engine
Gestisce sincronizzazioni intelligenti (UPSERT) con calcolo esatto del delta via EXCEPT.
"""

from contextlib import suppress
from pathlib import Path
from typing import Any

from src.core.database import db_manager
from src.core.sync.base import BaseSyncEngine


class SmartSyncEngine(BaseSyncEngine):
    """Motore di sync intelligente per tabelle con chiavi primarie (Certificati, ODA)."""

    @classmethod
    def sync_upsert_smart(  # noqa: PLR0913
        cls,
        db_path: Path,
        table_name: str,
        columns: list[str],
        new_data: list[tuple[Any, ...]],
        conflict_cols: list[str] | None = None,
        mirror: bool = False,
    ) -> tuple[int, int]:
        """Esegue Upsert calcolando esattamente le righe modificate o aggiunte."""
        if not new_data:
            return 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            temp_table = cls._create_temp_table(cursor, table_name, columns)
            cls._populate_temp_table(cursor, temp_table, columns, new_data)

            added_or_updated = cls._calculate_diff(cursor, table_name, temp_table, columns)
            cls._execute_upsert(cursor, table_name, temp_table, columns, conflict_cols)

            deleted_count = 0
            if mirror and conflict_cols:
                deleted_count = cls._execute_mirror_cleanup(cursor, table_name, temp_table, conflict_cols)

            conn.commit()
            return added_or_updated, deleted_count

    @classmethod
    def sync_full_replace_with_metadata(  # noqa: PLR0913
        cls,
        db_path: Path,
        table_name: str,
        columns: list[str],
        new_data: list[tuple[Any, ...]],
        key_cols: list[str],
        metadata_cols: list[str],
    ) -> tuple[int, int]:
        """Sostituisce i dati preservando i metadati esistenti (es. annotazioni)."""
        if not new_data:
            return 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()

            # 1. Recupera metadati
            current_metadata = cls._fetch_current_metadata(cursor, table_name, key_cols, metadata_cols)

            # 2. Svuota tabella
            safe_table = cls._validate_identifier(table_name)
            cursor.execute(f"DELETE FROM {safe_table}")  # nosec B608

            # 3. Prepara righe finali
            final_rows = cls._merge_data_with_metadata(
                new_data, columns, key_cols, metadata_cols, current_metadata
            )

            # 4. Inserimento massivo
            cls._bulk_insert_with_metadata(cursor, table_name, columns, metadata_cols, final_rows)

            conn.commit()
            return len(final_rows), 0

    # -------------------------------------------------------------------------
    # PRIVATE HELPERS - UPSERT
    # -------------------------------------------------------------------------

    @classmethod
    def _populate_temp_table(
        cls, cursor: Any, temp_table: str, columns: list[str], data: list[tuple[Any, ...]]
    ) -> None:
        """Inserisce i dati nella tabella temporanea."""
        placeholders = ", ".join(["?"] * len(columns))
        cleaned_data = [tuple(cls._clean_value(x) for x in r) for r in data]
        cursor.executemany(f"INSERT INTO {temp_table} VALUES ({placeholders})", cleaned_data)  # nosec B608

    @classmethod
    def _calculate_diff(cls, cursor: Any, table_name: str, temp_table: str, columns: list[str]) -> int:
        """Calcola quante righe differiscono tra la tabella temporanea e quella principale."""
        safe_table = cls._validate_identifier(table_name)
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
        safe_cast_cols = ", ".join([f'CAST("{cls._validate_identifier(c)}" AS TEXT)' for c in columns])

        q_diff = f"""
      SELECT COUNT(*) FROM (
        SELECT {safe_cols} FROM {temp_table}
        EXCEPT
        SELECT {safe_cast_cols} FROM {safe_table}
      )
    """  # nosec B608
        cursor.execute(q_diff)
        return int(cursor.fetchone()[0])

    @classmethod
    def _execute_upsert(
        cls,
        cursor: Any,
        table_name: str,
        temp_table: str,
        columns: list[str],
        conflict_cols: list[str] | None,
    ) -> None:
        """Esegue l'operazione di UPSERT."""
        safe_table = cls._validate_identifier(table_name)
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])

        if not conflict_cols:
            q_upsert = (
                f"INSERT OR REPLACE INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM {temp_table}"  # nosec B608
            )
        else:
            q_upsert = cls._build_upsert_query(table_name, temp_table, columns, conflict_cols)

        cursor.execute(q_upsert)

    @classmethod
    def _build_upsert_query(
        cls, table_name: str, temp_table: str, columns: list[str], conflict_cols: list[str]
    ) -> str:
        """Costruisce la query ON CONFLICT DO UPDATE/NOTHING."""
        safe_table = cls._validate_identifier(table_name)
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
        safe_conflict = ", ".join([f'"{cls._validate_identifier(c)}"' for c in conflict_cols])

        update_assignments = ", ".join(
            [
                f'"{cls._validate_identifier(c)}" = excluded."{cls._validate_identifier(c)}"'
                for c in columns
                if c not in conflict_cols
            ]
        )

        if update_assignments:
            return f"""
        INSERT INTO {safe_table} ({safe_cols})
        SELECT {safe_cols} FROM {temp_table}
        WHERE true
        ON CONFLICT({safe_conflict}) DO UPDATE SET {update_assignments}
      """  # nosec B608

        return f"""
      INSERT INTO {safe_table} ({safe_cols})
      SELECT {safe_cols} FROM {temp_table}
      WHERE true
      ON CONFLICT({safe_conflict}) DO NOTHING
    """  # nosec B608

    @classmethod
    def _execute_mirror_cleanup(
        cls, cursor: Any, table_name: str, temp_table: str, conflict_cols: list[str]
    ) -> int:
        """Rimuove le righe non più presenti nel sorgente (mirroring)."""
        safe_table = cls._validate_identifier(table_name)
        main_id_col = cls._validate_identifier(conflict_cols[0])

        q_mirror = f"""
      DELETE FROM {safe_table}
      WHERE "{main_id_col}" NOT IN (
        SELECT "{main_id_col}" FROM {temp_table}
      )
    """  # nosec B608
        cursor.execute(q_mirror)
        return int(cursor.rowcount)

    # -------------------------------------------------------------------------
    # PRIVATE HELPERS - METADATA
    # -------------------------------------------------------------------------

    @classmethod
    def _fetch_current_metadata(
        cls, cursor: Any, table_name: str, key_cols: list[str], metadata_cols: list[str]
    ) -> dict[tuple[str, ...], dict[str, Any]]:
        """Recupera i metadati attuali dal DB."""
        metadata_map: dict[tuple[str, ...], dict[str, Any]] = {}
        if not (key_cols and metadata_cols):
            return metadata_map

        safe_table = cls._validate_identifier(table_name)
        all_cols = key_cols + metadata_cols
        safe_all_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in all_cols])

        with suppress(Exception):
            cursor.execute(f"SELECT {safe_all_cols} FROM {safe_table}")  # nosec B608
            for row in cursor.fetchall():
                keys = tuple(str(row[i]).strip() for i in range(len(key_cols)))
                meta = {metadata_cols[i]: row[len(key_cols) + i] for i in range(len(metadata_cols))}
                metadata_map[keys] = meta
        return metadata_map

    @classmethod
    def _merge_data_with_metadata(
        cls,
        new_data: list[tuple[Any, ...]],
        columns: list[str],
        key_cols: list[str],
        metadata_cols: list[str],
        metadata_map: dict[tuple[str, ...], dict[str, Any]],
    ) -> list[tuple[Any, ...]]:
        """Unisce i nuovi dati con i metadati recuperati."""
        final_rows = []
        for r in new_data:
            row_list = list(r)

            # Estrazione chiavi per il matching
            keys_val = []
            for k in key_cols:
                if k in columns:
                    idx = columns.index(k)
                    keys_val.append(str(r[idx]).strip())

            saved_meta = metadata_map.get(tuple(keys_val))

            # Aggiunta valori metadati
            meta_values = [saved_meta.get(m) if saved_meta else "" for m in metadata_cols]
            final_rows.append(tuple(row_list) + tuple(meta_values))
        return final_rows

    @classmethod
    def _bulk_insert_with_metadata(
        cls,
        cursor: Any,
        table_name: str,
        columns: list[str],
        metadata_cols: list[str],
        final_rows: list[tuple[Any, ...]],
    ) -> None:
        """Esegue l'inserimento massivo finale."""
        safe_table = cls._validate_identifier(table_name)
        all_db_cols = columns + metadata_cols
        safe_db_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in all_db_cols])
        placeholders = ", ".join(["?"] * len(all_db_cols))

        cursor.executemany(
            f"INSERT INTO {safe_table} ({safe_db_cols}) VALUES ({placeholders})",  # nosec B608
            final_rows,
        )
