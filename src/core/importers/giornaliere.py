import logging
import os
import re
import warnings
import zipfile
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.core.importers.base import BaseImporter
from src.core.schemas import validate_giornaliere

logger = logging.getLogger(__name__)


class GiornaliereImporter(BaseImporter):
    """Importer per i dati delle Giornaliere."""

    # Anno minimo per importazione (dal 2025 i file hanno il foglio RIASSUNTO)
    MIN_IMPORT_YEAR = 2025

    GIORNALIERE_MAPPING: ClassVar[dict[str, str]] = {
        "DATA": "data",
        "PERSONALE": "personale",
        "DESCRIZIONE ATTIVITA'": "descrizione",
        "TCL": "tcl",
        "ODC": "odc",
        "N° PDL": "pdl",
        "INIZIO": "inizio",
        "FINE": "fine",
        "ORE": "ore",
        "consuntivo": "n_prev",
    }

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
            df = cls._read_giornaliera_sheet(file_obj)
            if df is None:
                return (year, [], None)

            df = cls._normalize_giornaliera_columns(df)
            if df is None:
                return (year, [], None)

            df = cls._clean_giornaliera_data(df)
            if df.empty:
                return (year, [], None)

            cls._enrich_giornaliera_odc(df, lookup_map)

            df["year"] = year
            df["nome_file"] = file_path.name

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
            rows = list(df[target_cols].itertuples(index=False, name=None))
            return (year, rows, None)

        except Exception as e:
            return (year, [], str(e))

    @classmethod
    def _read_giornaliera_sheet(cls, file_path: Any) -> pd.DataFrame | None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pd_obj = cls._get_pd()
            try:
                return pd_obj.read_excel(file_path, sheet_name="RIASSUNTO")  # type: ignore[no-any-return]
            except ValueError:
                return None
            except zipfile.BadZipFile:
                return None
            except Exception:
                try:
                    return pd_obj.read_excel(file_path, sheet_name="RIASSUNTO", engine="openpyxl")  # type: ignore[no-any-return]
                except zipfile.BadZipFile:
                    return None
                except Exception as e:
                    raise e

    @classmethod
    def _normalize_giornaliera_columns(cls, df: pd.DataFrame) -> pd.DataFrame | None:
        df.columns = df.columns.astype(str).str.strip()
        rename_map = {}

        for excel_col, db_col in cls.GIORNALIERE_MAPPING.items():
            if excel_col in df.columns:
                rename_map[excel_col] = db_col
            else:
                for col in df.columns:
                    if col.upper() == excel_col.upper():
                        rename_map[col] = db_col
                        break

        if not rename_map:
            return None

        df.rename(columns=rename_map, inplace=True)

        try:
            df = validate_giornaliere(df)
        except Exception as e:
            logger.warning(f"Validazione Pandera Giornaliere fallita (uso fallback): {e}")

        return df

    @classmethod
    def _clean_giornaliera_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        if len(df) > 0:
            df = df.iloc[:-1]

        if df.empty:
            return df

        for col in df.columns:
            if df[col].dtype == "object":
                mask = df[col].astype(str).str.contains("Totale", na=False, case=False)
                df = df[~mask]

        if df.empty:
            return df

        critical_cols = []
        if "data" in df.columns:
            critical_cols.append("data")
        if "personale" in df.columns:
            critical_cols.append("personale")
        if "ore" in df.columns:
            critical_cols.append("ore")

        if critical_cols:
            df.dropna(subset=critical_cols, how="any", inplace=True)

        return df

    @classmethod
    def _enrich_giornaliera_odc(cls, df: pd.DataFrame, lookup_map: dict[str, str]) -> None:
        mask_empty = df["odc"] == ""
        if mask_empty.any() and lookup_map:
            mapped = df.loc[mask_empty, "n_prev"].map(lookup_map)
            df.loc[mask_empty, "odc"] = mapped.fillna("")

        mask_empty = df["odc"] == ""
        if mask_empty.any():
            comm_pattern = r"\b(\d{2}/\d{3})\b"
            extracted = df.loc[mask_empty, "descrizione"].str.extract(comm_pattern, expand=False)
            df.loc[mask_empty, "odc"] = extracted.fillna("")

        mask_standard = ~df["odc"].str.contains("canone", case=False, na=False) & ~df["odc"].str.match(
            r"^\d{2}/\d{3}$", na=False
        )
        if mask_standard.any():
            extracted = df.loc[mask_standard, "odc"].str.extract(r"(5400\d+)", expand=False)
            df.loc[mask_standard, "odc"] = extracted.fillna("")
