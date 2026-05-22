"""Modulo Giornaliere."""

import os
import re
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.core.importers.base import BaseImporter
from src.core.logging import get_logger
from src.core.processing.base import Pipeline
from src.core.processing.giornaliere.steps import (
    EnrichGiornalieraStep,
    NormalizeGiornalieraStep,
    ReadGiornalieraStep,
    SyncGiornaliereStep,
)

logger = get_logger(__name__)


class GiornaliereImporter(BaseImporter):
    """Importer per i dati delle Giornaliere."""

    # Anno minimo per importazione (dal 2025 i file hanno il foglio RIASSUNTO)
    MIN_IMPORT_YEAR = 2025

    GIORNALIERE_MAPPING: ClassVar[dict[str, str]] = {
        "DATA": "data",
        "PERSONALE": "personale",
        "DESCRIZIONE ATTIVITÀ": "descrizione",
        "TCL": "tcl",
        "ODC": "odc",
        "N  PDL": "pdl",
        "INIZIO": "inizio",
        "FINE": "fine",
        "ORE": "ore",
        "consuntivo": "n_prev",
    }

    GIORNALIERE_COLS: ClassVar[list[str]] = [
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

    @classmethod
    def scan_files(cls, giornaliere_path: str) -> int:
        """Conta i file validi nelle cartelle giornaliere (solo anni >= MIN_IMPORT_YEAR)."""
        p_giorn = Path(giornaliere_path)
        if not giornaliere_path or not p_giorn.exists():
            return 0

        count = 0
        current_year = datetime.now(UTC).year
        for folder in p_giorn.iterdir():
            if not folder.is_dir():
                continue
            match = re.match(r"Giornaliere\s+(\d{4})", folder.name, re.IGNORECASE)
            if not match:
                continue

            year = int(match.group(1))
            # Salta anni futuri e anni prima di MIN_IMPORT_YEAR (senza foglio RIASSUNTO)
            if year > current_year or year < cls.MIN_IMPORT_YEAR:
                continue

            for file_path in folder.glob("*.xls*"):
                if not file_path.name.startswith("~$"):
                    count += 1
        return count

    @classmethod
    def import_giornaliere(
        cls,
        root_path: str,
        lookup_map: dict[str, str],
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]], list[int]]:
        """Importa i dati dalle cartelle Giornaliere."""
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata.", [], []

        tasks_args = cls._collect_giornaliere_tasks(root, lookup_map)
        if not tasks_args:
            return (
                True,
                f"Nessuna nuova giornaliera trovata (check anno >= {datetime.now(UTC).year}).",
                [],
                [],
            )

        all_rows, imported_years = cls._run_parallel_import(tasks_args, progress_callback)

        if not imported_years:
            return True, "Nessuna riga valida importata dai file trovati.", [], []

        return (
            True,
            f"Importate Giornaliere: {sorted(imported_years)}",
            all_rows,
            imported_years,
        )

    @classmethod
    def _collect_giornaliere_tasks(
        cls, root: Path, lookup_map: dict[str, str]
    ) -> list[tuple[int, Path, dict[str, str]]]:
        """Raccoglie i task di importazione (solo anni >= MIN_IMPORT_YEAR con foglio RIASSUNTO)."""
        tasks: list[tuple[int, Path, dict[str, str]]] = []
        current_year = datetime.now(UTC).year
        for folder in root.iterdir():
            if not folder.is_dir():
                continue
            match = re.match(r"Giornaliere\s+(\d{4})", folder.name, re.IGNORECASE)
            if not match:
                continue

            year = int(match.group(1))
            # Salta anni futuri e anni prima di MIN_IMPORT_YEAR (senza foglio RIASSUNTO)
            if year > current_year or year < cls.MIN_IMPORT_YEAR:
                continue

            tasks.extend(
                (year, file_path, lookup_map)
                for file_path in folder.glob("*.xls*")
                if not file_path.name.startswith("~$")
            )
        return tasks

    @classmethod
    def _run_parallel_import(
        cls,
        tasks: list[tuple[int, Path, dict[str, str]]],
        progress_callback: Callable[[int, int], None] | None,
    ) -> tuple[list[tuple[Any, ...]], list[int]]:
        all_rows: list[tuple[Any, ...]] = []
        years_encountered: set[int] = set()
        total_tasks = len(tasks)
        processed_count = 0

        max_workers = min(4, (os.cpu_count() or 1))
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(cls._process_single_giornaliera, tasks):
                processed_count += 1
                if progress_callback:
                    progress_callback(processed_count, total_tasks)

                r_year, r_rows, r_err = result
                if r_rows:
                    all_rows.extend(r_rows)
                    years_encountered.add(r_year)
                if r_err:
                    logger.error(f"Errore lettura file (Year {r_year}): {r_err}")

        return all_rows, list(years_encountered)

    @classmethod
    def _process_single_giornaliera(
        cls, args: tuple[int, Path, dict[str, str]]
    ) -> tuple[int, list[tuple[Any, ...]], str | None]:
        year, file_path, lookup_map = args
        try:
            file_obj, _ = cls._decrypt_if_encrypted(file_path)

            pipeline = Pipeline()
            pipeline.add_step(ReadGiornalieraStep())
            pipeline.add_step(NormalizeGiornalieraStep())
            pipeline.add_step(EnrichGiornalieraStep())
            pipeline.add_step(SyncGiornaliereStep())

            context = {
                "file_path": file_path,
                "file_obj": file_obj,
                "year": year,
                "lookup_map": lookup_map,
            }

            result = pipeline.run(context)

            if not result.get("success"):
                return (year, [], result.get("message"))

            rows = result.get("rows", [])

        except Exception as e:
            return (year, [], str(e))
        else:
            return (year, rows, None)

    @classmethod
    def _normalize_giornaliera_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Alias per retrocompatibilità con i test."""
        from typing import cast  # noqa: PLC0415

        from src.core.processing.giornaliere.steps import NormalizeGiornalieraStep  # noqa: PLC0415

        context = {"df": df, "success": True}
        NormalizeGiornalieraStep().execute(context)
        return cast("pd.DataFrame", context["df"])

    @classmethod
    def _clean_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Alias per retrocompatibilità con i test."""
        from src.core.processing.giornaliere.steps import NormalizeGiornalieraStep  # noqa: PLC0415

        return NormalizeGiornalieraStep()._clean_data(df)
