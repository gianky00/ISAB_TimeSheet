# mypy: disable-error-code="no-any-unimported"
"""
SyncroJob - Data Synchronizer
Gestisce la sincronizzazione dei dati importati delegando agli engine specializzati.
"""

from pathlib import Path
from typing import Any

from src.core.sync.contabilita_sync import ContabilitaSyncEngine
from src.core.sync.smart_sync import SmartSyncEngine


class DataSynchronizer:
    """
    Orchestratore per la sincronizzazione dei dati tra file sorgente e database.
    Delega la logica atomica agli engine specializzati.
    """

    @classmethod
    def sync_contabilita(cls, db_path: Path, import_data: list[Any], years: list[int]) -> tuple[int, int]:
        """Sincronizza i dati della contabilità."""
        from src.core.importers.contabilita import ContabilitaImporter  # noqa: PLC0415

        all_new_data = []
        for r in import_data:
            if hasattr(r, "values"):
                all_new_data.append(tuple(r.values()))
            else:
                all_new_data.append(tuple(r))

        res = ContabilitaSyncEngine.sync_contabilita(
            db_path, all_new_data, years, getattr(ContabilitaImporter, "CONTABILITA_COLS", [])
        )
        return int(res[0]), int(res[1])

    @classmethod
    def sync_giornaliere(cls, db_path: Path, import_data: list[Any], years: list[int]) -> tuple[int, int]:
        """Sincronizza i dati delle giornaliere."""
        from src.core.importers.giornaliere import GiornaliereImporter  # noqa: PLC0415

        all_new_data = []
        for r in import_data:
            if hasattr(r, "values"):
                all_new_data.append(tuple(r.values()))
            else:
                all_new_data.append(tuple(r))

        res = ContabilitaSyncEngine.sync_giornaliere(
            db_path, all_new_data, years, getattr(GiornaliereImporter, "GIORNALIERE_COLS", [])
        )
        return int(res[0]), int(res[1])

    @classmethod
    def sync_storico_oda(cls, db_path: Path, rows_to_insert: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizza lo storico ODA via Upsert intelligente."""
        from src.core.importers.storico_oda import StoricoOdaImporter  # noqa: PLC0415

        res = SmartSyncEngine.sync_upsert_smart(
            db_path,
            "storico_oda",
            getattr(StoricoOdaImporter, "STORICO_ODA_COLS", []),
            rows_to_insert,
            conflict_cols=["oda", "pos_oda", "num_riga"],
        )
        return int(res[0]), int(res[1])

    @classmethod
    def sync_contabilita_dati(cls, *args: Any, **kwargs: Any) -> tuple[int, int]:
        """Alias per retrocompatibilità."""
        return cls.sync_contabilita(*args, **kwargs)

    @classmethod
    def sync_attivita_programmate(cls, db_path: Path, rows: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizza le attivitàprogrammate."""
        from src.core.importers.attivita import AttivitaImporter  # noqa: PLC0415

        res = SmartSyncEngine.sync_upsert_smart(
            db_path,
            "attivita_programmate",
            getattr(AttivitaImporter, "ATTIVITA_COLS", []),
            rows,
            conflict_cols=["oda"],
        )
        return int(res[0]), int(res[1])

    @classmethod
    def sync_scarico_ore(cls, db_path: Path, rows: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizza lo scarico ore."""
        from src.core.importers.scarico_ore import ScaricoOreImporter  # noqa: PLC0415

        res = SmartSyncEngine.sync_upsert_smart(
            db_path,
            "scarico_ore",
            getattr(ScaricoOreImporter, "SCARICO_ORE_COLS", []),
            rows,
            conflict_cols=["oda"],
        )
        return int(res[0]), int(res[1])

    @classmethod
    def sync_certificati_campione(cls, db_path: Path, rows: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizza i certificati campione."""
        from src.core.importers.certificati import CertificatiImporter  # noqa: PLC0415

        res = SmartSyncEngine.sync_upsert_smart(
            db_path,
            "certificati_campione",
            getattr(CertificatiImporter, "CERTIFICATI_COLS", []),
            rows,
            conflict_cols=["id_strumento", "certificato"],
        )
        return int(res[0]), int(res[1])
