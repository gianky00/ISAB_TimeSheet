"""SyncroJob - Data Synchronizer.

Gestisce la sincronizzazione dei dati importati delegando agli engine specializzati.
"""

from pathlib import Path
from typing import Any

from src.application.services.importers.attivita import AttivitaImporter
from src.application.services.importers.certificati import CertificatiImporter
from src.application.services.importers.contabilita import ContabilitaImporter
from src.application.services.importers.giornaliere import GiornaliereImporter
from src.application.services.importers.scarico_ore import ScaricoOreImporter
from src.application.services.importers.storico_oda import StoricoOdaImporter
from src.application.services.sync.base import SyncTarget
from src.application.services.sync.contabilita_sync import ContabilitaSyncEngine
from src.application.services.sync.smart_sync import SmartSyncEngine


class DataSynchronizer:
    """Orchestratore per la sincronizzazione dei dati tra file sorgente e database.

    Delega la logica atomica agli engine specializzati.
    """

    @classmethod
    def sync_contabilita(cls, db_path: Path, import_data: list[Any], years: list[int]) -> tuple[int, int]:
        """Sincronizza i dati della contabilità."""
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
        target = SyncTarget(db_path, "storico_oda", getattr(StoricoOdaImporter, "STORICO_ODA_COLS", []))
        res = SmartSyncEngine.sync_upsert_smart(
            target,
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
        """Sincronizza le attivitàprogrammate preservando gli stili."""
        target = SyncTarget(
            db_path, "attivita_programmate", getattr(AttivitaImporter, "ATTIVITA_PROGRAMMATE_COLS", [])
        )
        # Usiamo full_replace_with_metadata perché non abbiamo vincoli UNIQUE
        # e vogliamo mantenere gli stili calcolati.
        res = SmartSyncEngine.sync_full_replace_with_metadata(
            target,
            rows,
            key_cols=["ps", "area", "descrizione"],  # Chiave euristica
            metadata_cols=["styles"],
        )
        return int(res[0]), int(res[1])

    @classmethod
    def sync_scarico_ore(cls, db_path: Path, rows: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizza lo scarico ore preservando gli stili."""
        target = SyncTarget(db_path, "scarico_ore", getattr(ScaricoOreImporter, "SCARICO_ORE_COLS", []))
        # Usiamo full_replace_with_metadata per mantenere la formattazione colori.
        res = SmartSyncEngine.sync_full_replace_with_metadata(
            target,
            rows,
            key_cols=["data", "pers1", "odc", "pos"],  # Chiave euristica
            metadata_cols=["styles"],
        )
        return int(res[0]), int(res[1])

    @classmethod
    def sync_certificati_campione(cls, db_path: Path, rows: list[tuple[Any, ...]]) -> tuple[int, int]:
        """Sincronizza i certificati campione preservando annotazioni e ubicazione."""
        target = SyncTarget(
            db_path, "certificati_campione", getattr(CertificatiImporter, "CERTIFICATI_CAMPIONE_COLS", [])
        )
        # Usiamo full_replace_with_metadata perché non abbiamo vincoli UNIQUE nel DB (v6)
        # ma vogliamo mantenere le annotazioni manuali degli utenti.
        # Usiamo 'id_coemi' come chiave primaria per il matching dei metadati.
        res = SmartSyncEngine.sync_full_replace_with_metadata(
            target,
            rows,
            key_cols=["id_coemi", "certificato"],
            metadata_cols=[
                "annotazioni",
                "ubicazione",
                "guasto",
                "guasto_tipo",
                "guasto_data",
                "guasto_note",
            ],
        )
        return int(res[0]), int(res[1])
