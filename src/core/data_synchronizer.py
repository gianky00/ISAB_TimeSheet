"""
SyncroJob - Data Synchronizer
Gestisce la sincronizzazione dei dati importati delegando ai motori specializzati.
Refactored V9.5: Modularized architecture.
"""

from pathlib import Path
from typing import Any

from src.core.excel_importer import ExcelImporter
from src.core.sync.contabilita_sync import ContabilitaSyncEngine
from src.core.sync.operazioni_sync import OperazioniSyncEngine
from src.core.sync.smart_sync import SmartSyncEngine


class DataSynchronizer:
    """
    Facade per la sincronizzazione dei dati con il database.
    Coordina i diversi motori di sync in base al dominio dei dati.
    """

    @classmethod
    def sync_contabilita_dati(
        cls, db_path: Path, imported_data: list[tuple[Any, ...]], imported_years: list[int]
    ) -> tuple[int, int]:
        """Sincronizza i dati di contabilità strumentale."""
        return ContabilitaSyncEngine.sync_contabilita_dati(db_path, imported_data, imported_years)

    @classmethod
    def sync_giornaliere(
        cls, db_path: Path, all_new_rows: list[tuple[Any, ...]], years_to_clear: list[int]
    ) -> tuple[int, int]:
        """Sincronizza i dati giornalieri."""
        return ContabilitaSyncEngine.sync_giornaliere(db_path, all_new_rows, years_to_clear)

    @classmethod
    def sync_attivita_programmate(
        cls, db_path: Path, rows_to_insert: list[tuple[Any, ...]]
    ) -> tuple[int, int]:
        """Sincronizzazione per Attività Programmate (Sostituzione completa)."""
        return OperazioniSyncEngine.sync_attivita_programmate(db_path, rows_to_insert)

    @classmethod
    def sync_scarico_ore(cls, db_path: Path, rows_to_insert: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizzazione massiva ottimizzata per Scarico Ore."""
        return OperazioniSyncEngine.sync_scarico_ore(db_path, rows_to_insert)

    @classmethod
    def sync_certificati_campione(
        cls, db_path: Path, rows_to_insert: list[tuple[Any, ...]]
    ) -> tuple[int, int]:
        """Sincronizzazione 'Tale e Quale' (Full Replace) con conservazione metadati."""
        return SmartSyncEngine.sync_full_replace_with_metadata(
            db_path,
            "certificati_campione",
            ExcelImporter.CERTIFICATI_CAMPIONE_COLS,
            rows_to_insert,
            key_cols=["id_coemi"],
            metadata_cols=["annotazioni", "ubicazione"],
        )

    @classmethod
    def sync_storico_oda(cls, db_path: Path, rows_to_insert: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizza lo storico ODA via Upsert intelligente."""
        return SmartSyncEngine.sync_upsert_smart(
            db_path,
            "storico_oda",
            ExcelImporter.STORICO_ODA_COLS,
            rows_to_insert,
            conflict_cols=["oda", "pos_oda", "num_riga"],
        )
