# mypy: disable-error-code="no-any-unimported"
"""
SyncroJob - Contabilit  Sync Engine
Engine specializzato per la sincronizzazione dei dati contabili.
"""

import sqlite3
from typing import Any

from src.core.sync.base import BaseSyncEngine, PartitionConfig


class ContabilitaSyncEngine(BaseSyncEngine):
    """Gestore sincronizzazione Contabilit  e Giornaliere."""

    @classmethod
    def sync_giornaliere(
        cls,
        db_path: Any,
        new_data: list[tuple[Any, ...]],
        years: list[int],
        columns: list[str],
    ) -> tuple[int, int]:
        """Sincronizza le giornaliere per gli anni specificati."""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            try:
                # Esegue la sincronizzazione via partizioni (Anno)
                res = cls.sync_partitioned_data(
                    cursor,
                    "giornaliere",
                    columns,
                    new_data,
                    PartitionConfig(column="anno", values=years),
                )
                conn.commit()
                return int(res[0]), int(res[1])
            except Exception:
                conn.rollback()
                raise

    @classmethod
    def sync_contabilita(
        cls,
        db_path: Any,
        new_data: list[tuple[Any, ...]],
        years: list[int],
        columns: list[str],
    ) -> tuple[int, int]:
        """Sincronizza la contabilit  per gli anni specificati."""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            try:
                # Esegue la sincronizzazione via partizioni (Anno)
                res = cls.sync_partitioned_data(
                    cursor,
                    "contabilita",
                    columns,
                    new_data,
                    PartitionConfig(column="anno", values=years),
                )
                conn.commit()
                return int(res[0]), int(res[1])
            except Exception:
                conn.rollback()
                raise
