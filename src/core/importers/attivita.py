import warnings
from collections.abc import Callable
from pathlib import Path
from typing import ClassVar

import pandas as pd

from src.core.importers.base import BaseImporter


class AttivitaImporter(BaseImporter):
    """Importer per le Attività Programmate."""

    ATTIVITA_PROGRAMMATE_MAPPING: ClassVar[dict[str, str]] = {
        "PS": "ps",
        "AREA": "area",
        "PdL": "pdl",
        "IMP.": "imp",
        "DESCRIZIONE\nATTIVITA'": "descrizione",
        "LUN": "lun",
        "MAR": "mar",
        "MER": "mer",
        "GIO": "gio",
        "VEN": "ven",
        "STATO\nPdL": "stato_pdl",
        "STATO\nATTIVITA'": "stato_attivita",
        "DATA\nCONTROLLO": "data_controllo",
        "PERSONALE\nIMPIEGATO": "personale",
        "PO": "po",
        "AVVISO": "avviso",
    }

    ATTIVITA_PROGRAMMATE_COLS: ClassVar[list[str]] = [*list(ATTIVITA_PROGRAMMATE_MAPPING.values()), "styles"]

    @classmethod
    def import_attivita_programmate(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple]]:
        """Importa il file Attività Programmate (veloce, senza colori)."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Attività Programmate non trovato: {file_path}", []

        try:
            df = cls._read_attivita_programmate_sheet(path)
            if df is None:
                return False, "Foglio 'Riepilogo' non trovato o file illeggibile.", []

            df = cls._normalize_attivita_columns(df)
            if df is None:
                return False, "Colonne non trovate. Controlla intestazione riga 3.", []

            rows = cls._prepare_attivita_rows(df)
            return True, f"Importate {len(rows)} righe in Attività Programmate.", rows

        except Exception as e:
            return False, f"Errore importazione Attività Programmate: {e}", []

    @classmethod
    def _read_attivita_programmate_sheet(cls, path: Path) -> pd.DataFrame | None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pd_obj = cls._get_pd()
            try:
                return pd_obj.read_excel(path, sheet_name="Riepilogo", header=2)
            except (ValueError, Exception):
                try:
                    return pd_obj.read_excel(
                        path,
                        sheet_name="Riepilogo",
                        header=2,
                        engine="openpyxl",
                    )
                except Exception:
                    return None

    @classmethod
    def _normalize_attivita_columns(cls, df: pd.DataFrame) -> pd.DataFrame | None:
        df.columns = df.columns.astype(str).str.strip()
        rename_map = {}

        for excel_col, db_col in cls.ATTIVITA_PROGRAMMATE_MAPPING.items():
            if excel_col in df.columns:
                rename_map[excel_col] = db_col
            else:
                for col in df.columns:
                    if excel_col.replace("\n", " ").strip() == col.replace("\n", " ").strip():
                        rename_map[col] = db_col
                        break

        if not rename_map:
            return None

        df.rename(columns=rename_map, inplace=True)
        return df

    @classmethod
    def _prepare_attivita_rows(cls, df: pd.DataFrame) -> list[tuple]:
        for db_col in cls.ATTIVITA_PROGRAMMATE_MAPPING.values():
            if db_col not in df.columns:
                df[db_col] = ""

        check_cols = [c for c in ("ps", "area", "descrizione") if c in df.columns]
        if check_cols:
            df.dropna(how="all", subset=check_cols, inplace=True)

        df = df.fillna("").astype(str).apply(lambda x: x.str.strip())
        df["styles"] = ""

        db_cols = [*list(cls.ATTIVITA_PROGRAMMATE_MAPPING.values()), "styles"]
        df = df[db_cols]

        return list(df.itertuples(index=False, name=None))
