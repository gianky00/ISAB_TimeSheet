import logging
import os
import re
import warnings
import zipfile
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import pandas as pd

from src.core.schemas import validate_giornaliere
from src.core.importers.base import BaseImporter


class GiornaliereImporter(BaseImporter):
    """Importer per i dati delle Giornaliere."""

    GIORNALIERE_MAPPING = {
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
    def import_giornaliere(
        cls,
        root_path: str,
        lookup_map: Dict,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple], List[int]]:
        """Importa i dati dalle cartelle Giornaliere."""
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata.", [], []

        tasks_args = cls._collect_giornaliere_tasks(root, lookup_map)
        if not tasks_args:
            return (
                True,
                f"Nessuna nuova giornaliera trovata (check anno >= {datetime.now().year}).",
                [],
                [],
            )

        all_rows, imported_years = cls._run_parallel_import(
            tasks_args, progress_callback
        )

        if not imported_years:
            return True, "Nessuna riga valida importata dai file trovati.", [], []

        return (
            True,
            f"Importate Giornaliere: {sorted(imported_years)}",
            all_rows,
            imported_years,
        )

    @classmethod
    def _collect_giornaliere_tasks(cls, root: Path, lookup_map: Dict) -> List[Tuple]:
        tasks = []
        current_year = datetime.now().year
        for folder in root.iterdir():
            if not folder.is_dir():
                continue
            match = re.match(r"Giornaliere\s+(\d{4})", folder.name, re.IGNORECASE)
            if not match:
                continue

            year = int(match.group(1))
            if year > current_year:
                continue

            for file_path in folder.glob("*.xls*"):
                if not file_path.name.startswith("~$"):
                    tasks.append((year, file_path, lookup_map))
        return tasks

    @classmethod
    def _run_parallel_import(
        cls, tasks: List[Tuple], progress_callback: Optional[Callable]
    ) -> Tuple[List[Tuple], List[int]]:
        all_rows = []
        years_encountered = set()
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
                    logging.error(f"Errore lettura file (Year {r_year}): {r_err}")

        return all_rows, list(years_encountered)

    @classmethod
    def _process_single_giornaliera(
        cls, args: Tuple[int, Path, Dict]
    ) -> Tuple[int, List[Tuple], Optional[str]]:
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
    def _read_giornaliera_sheet(cls, file_path) -> Optional[pd.DataFrame]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pd = cls._get_pd()
            try:
                return pd.read_excel(file_path, sheet_name="RIASSUNTO")
            except ValueError:
                return None
            except zipfile.BadZipFile:
                return None
            except Exception:
                try:
                    return pd.read_excel(
                        file_path, sheet_name="RIASSUNTO", engine="openpyxl"
                    )
                except zipfile.BadZipFile:
                    return None
                except Exception as e:
                    raise e

    @classmethod
    def _normalize_giornaliera_columns(cls, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        df.columns = [str(c).strip() for c in df.columns]
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
            logging.warning(
                f"Validazione Pandera Giornaliere fallita (uso fallback): {e}"
            )

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

        if df.empty:
            return df

        for db_col in cls.GIORNALIERE_MAPPING.values():
            if db_col not in df.columns:
                df[db_col] = ""

        cols_to_clean = [
            "odc",
            "n_prev",
            "data",
            "personale",
            "descrizione",
            "tcl",
            "pdl",
            "inizio",
            "fine",
            "ore",
        ]
        # Check existence before accessing
        cols_to_clean = [c for c in cols_to_clean if c in df.columns]
        
        df[cols_to_clean] = df[cols_to_clean].astype(str).apply(lambda x: x.str.strip())
        df[cols_to_clean] = df[cols_to_clean].replace(r"(?i)^nan$", "", regex=True)
        return df

    @classmethod
    def _enrich_giornaliera_odc(cls, df: pd.DataFrame, lookup_map: Dict):
        mask_empty = df["odc"] == ""
        if mask_empty.any() and lookup_map:
            mapped = df.loc[mask_empty, "n_prev"].map(lookup_map)
            df.loc[mask_empty, "odc"] = mapped.fillna("")

        mask_empty = df["odc"] == ""
        if mask_empty.any():
            comm_pattern = r"\b(\d{2}/\d{3})\b"
            extracted = df.loc[mask_empty, "descrizione"].str.extract(
                comm_pattern, expand=False
            )
            df.loc[mask_empty, "odc"] = extracted.fillna("")

        mask_standard = ~df["odc"].str.contains("canone", case=False, na=False) & ~df[
            "odc"
        ].str.match(r"^\d{2}/\d{3}$", na=False)
        if mask_standard.any():
            extracted = df.loc[mask_standard, "odc"].str.extract(
                r"(5400\d+)", expand=False
            )
            df.loc[mask_standard, "odc"] = extracted.fillna("")
