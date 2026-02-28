"""
SyncroJob - Contabilita Sync Engine
Gestisce la sincronizzazione di Contabilità e Giornaliere con logica di partizionamento per anno.
"""

from pathlib import Path
from typing import Any

from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter
from src.core.sync.base import BaseSyncEngine


class ContabilitaSyncEngine(BaseSyncEngine):
    """Motore di sync per i dati di contabilità strumentale e giornaliere personale."""

    @classmethod
    def sync_contabilita_dati(
        cls, db_path: Path, imported_data: list[tuple[Any, ...]], imported_years: list[int]
    ) -> tuple[int, int]:
        """Sincronizza i dati di contabilità strumentale."""
        if not imported_data:
            return 0, 0

        target_columns = [
            "year",
            *[cls._validate_identifier(c) for c in ExcelImporter.COLUMNS_MAPPING.values()],
        ]
        total_added, total_removed = 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            temp_table = cls._create_temp_table(cursor, "contabilita", target_columns)

            placeholders = ", ".join(["?"] * len(target_columns))
            data = [tuple(cls._clean_value(x) for x in r) for r in imported_data]
            cursor.executemany(f"INSERT INTO {temp_table} VALUES ({placeholders})", data)

            for year in imported_years:
                added, removed = cls._get_diff_count(cursor, "contabilita", target_columns, year)
                total_added += added
                total_removed += removed
                cls._replace_data(cursor, "contabilita", target_columns, year)
            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_giornaliere(
        cls, db_path: Path, all_new_rows: list[tuple[Any, ...]], years_to_clear: list[int]
    ) -> tuple[int, int]:
        """Sincronizza i dati giornalieri."""
        if not all_new_rows and not years_to_clear:
            return 0, 0

        target_cols = [
            "year",
            "data",
            "personale",
            "descrizione",
            "tcl",
            "odc",
            "pdl",
            "inizio",
            "fine",
            "ore",
            "n_prev",
            "nome_file",
        ]
        total_added, total_removed = 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            temp_table = cls._create_temp_table(cursor, "giornaliere", target_cols)

            if all_new_rows:
                placeholders = ", ".join(["?"] * len(target_cols))
                data = [tuple(cls._clean_value(x) for x in r) for r in all_new_rows]
                cursor.executemany(f"INSERT INTO {temp_table} VALUES ({placeholders})", data)

            for year in years_to_clear:
                added, removed = cls._get_diff_count(cursor, "giornaliere", target_cols, year)
                total_added += added
                total_removed += removed
                cls._replace_data(cursor, "giornaliere", target_cols, year)
            conn.commit()

        return total_added, total_removed

    @classmethod
    def _get_diff_count(
        cls, cursor: Any, table_name: str, columns: list[str], year: int | None = None
    ) -> tuple[int, int]:
        """Calcola aggiunti e rimossi usando EXCEPT."""
        safe_table = cls._validate_identifier(table_name)
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
        safe_cast_cols = ", ".join([f'CAST("{cls._validate_identifier(c)}" AS TEXT)' for c in columns])

        where_clause = "WHERE year = ?" if year is not None else ""
        params = (year,) if year is not None else ()

        # Aggiunti
        q_added = f"SELECT COUNT(*) FROM (SELECT {safe_cols} FROM temp_{safe_table} {where_clause} EXCEPT SELECT {safe_cast_cols} FROM {safe_table} {where_clause})"
        cursor.execute(q_added, params + params)
        added = cursor.fetchone()[0]

        # Rimossi
        q_removed = f"SELECT COUNT(*) FROM (SELECT {safe_cast_cols} FROM {safe_table} {where_clause} EXCEPT SELECT {safe_cols} FROM temp_{safe_table} {where_clause})"
        cursor.execute(q_removed, params + params)
        removed = cursor.fetchone()[0]

        return added, removed

    @classmethod
    def _replace_data(cls, cursor: Any, table_name: str, columns: list[str], year: int | None = None) -> None:
        """Sostituisce i dati per anno."""
        safe_table = cls._validate_identifier(table_name)
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])

        if year is not None:
            cursor.execute(f"DELETE FROM {safe_table} WHERE year = ?", (year,))
            q_ins = f"INSERT INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM temp_{safe_table} WHERE year = ?"
            cursor.execute(q_ins, (year,))
        else:
            cursor.execute(f"DELETE FROM {safe_table}")
            q_ins = f"INSERT INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM temp_{safe_table}"
            cursor.execute(q_ins)
