"""
SyncroJob - Contabilita Sync Engine
Gestisce la sincronizzazione di Contabilità e Giornaliere con logica di partizionamento per anno.
Refactored V9.5: Simplified via BaseSyncEngine orchestration.
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
        """Sincronizza i dati di contabilità strumentale delegando all'orchestrazione base."""
        if not imported_data:
            return 0, 0

        target_columns = [
            "year",
            *[cls._validate_identifier(c) for c in ExcelImporter.COLUMNS_MAPPING.values()],
        ]

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            res = cls._sync_partitioned_table(
                cursor=cursor,
                table_name="contabilita",
                columns=target_columns,
                partition_col="year",
                partition_values=imported_years,
                new_data=imported_data,
            )
            conn.commit()
            return res

    @classmethod
    def sync_giornaliere(
        cls, db_path: Path, all_new_rows: list[tuple[Any, ...]], years_to_clear: list[int]
    ) -> tuple[int, int]:
        """Sincronizza i dati giornalieri delegando all'orchestrazione base."""
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

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            res = cls._sync_partitioned_table(
                cursor=cursor,
                table_name="giornaliere",
                columns=target_cols,
                partition_col="year",
                partition_values=years_to_clear,
                new_data=all_new_rows,
            )
            conn.commit()
            return res
