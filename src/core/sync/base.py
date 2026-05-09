# mypy: disable-error-code="no-any-unimported"
"""
SyncroJob - Base Sync Engine
Logica comune per la sincronizzazione dei dati nel database SQLite.
"""

import re
import sqlite3
from dataclasses import dataclass
from typing import Any

from src.core.exceptions import ValidationError


@dataclass
class PartitionConfig:
    """Configurazione per la sincronizzazione partizionata."""

    column: str
    values: list[Any]


class BaseSyncEngine:
    """Motore base per sincronizzazioni atomiche."""

    @staticmethod
    def _validate_identifier(identifier: str) -> str:
        """Protegge da SQL Injection validando nomi di tabelle e colonne."""
        if not re.match(r"^[a-zA-Z0-9_]+$", identifier):
            raise ValidationError("Invalid identifier")  # noqa: TRY003
        return identifier

    @staticmethod
    def _clean_value(value: Any) -> Any:
        """Normalizza i valori prima dell'inserimento."""
        if value is None:
            return ""
        return str(value).strip()

    @classmethod
    def _create_temp_table(cls, cursor: sqlite3.Cursor, table_name: str, columns: list[str]) -> str:
        """Crea una tabella temporanea con la stessa struttura dell'originale."""
        safe_table = cls._validate_identifier(table_name)
        temp_table = f"temp_{safe_table}"
        cursor.execute(f"DROP TABLE IF EXISTS {temp_table}")
        cols_def = ", ".join([f'"{cls._validate_identifier(c)}" TEXT' for c in columns])
        cursor.execute(f"CREATE TEMP TABLE {temp_table} ({cols_def})")
        return temp_table

    @classmethod
    def sync_partitioned_data(
        cls,
        cursor: sqlite3.Cursor,
        table_name: str,
        columns: list[str],
        new_data: list[tuple[Any, ...]],
        partition: PartitionConfig,
    ) -> tuple[int, int]:
        """
        Esegue una sincronizzazione atomica basata su partizioni (es: Anno).
        Cancella i dati esistenti per le partizioni fornite e inserisce i nuovi.

        Returns:
          Tuple (aggiunti, rimossi).
        """
        safe_table = cls._validate_identifier(table_name)
        temp_table = cls._create_temp_table(cursor, safe_table, columns)

        if new_data:
            placeholders = ", ".join(["?"] * len(columns))
            # Pulisce i dati prima dell'inserimento
            cleaned_data = [tuple(cls._clean_value(x) for x in r) for r in new_data]
            cursor.executemany(f"INSERT INTO {temp_table} VALUES ({placeholders})", cleaned_data)  # nosec B608

        total_added, total_removed = 0, 0
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
        safe_cast_cols = ", ".join([f'CAST("{cls._validate_identifier(c)}" AS TEXT)' for c in columns])
        safe_part_col = cls._validate_identifier(partition.column)

        for val in partition.values:
            # 1. Calcolo Diff (Aggiunti)
            q_added = (
                f"SELECT COUNT(*) FROM ("  # nosec B608
                f"SELECT {safe_cast_cols} FROM {temp_table} WHERE {safe_part_col} = ? "  # nosec B608
                f"EXCEPT SELECT {safe_cast_cols} FROM {safe_table} WHERE {safe_part_col} = ?)"  # nosec B608
            )
            cursor.execute(q_added, (val, val))
            total_added += int(cursor.fetchone()[0])

            # 2. Calcolo Diff (Rimossi)
            q_removed = (
                f"SELECT COUNT(*) FROM ("  # nosec B608
                f"SELECT {safe_cast_cols} FROM {safe_table} WHERE {safe_part_col} = ? "  # nosec B608
                f"EXCEPT SELECT {safe_cast_cols} FROM {temp_table} WHERE {safe_part_col} = ?)"  # nosec B608
            )
            cursor.execute(q_removed, (val, val))
            total_removed += int(cursor.fetchone()[0])

            # 3. Sostituzione Atomica
            cursor.execute(f"DELETE FROM {safe_table} WHERE {safe_part_col} = ?", (val,))  # nosec B608
            q_ins = f"INSERT INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM {temp_table} WHERE {safe_part_col} = ?"  # nosec B608
            cursor.execute(q_ins, (val,))

        return total_added, total_removed
