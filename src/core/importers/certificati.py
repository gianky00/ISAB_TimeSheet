import warnings
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.core.importers.base import BaseImporter


class CertificatiImporter(BaseImporter):
    """Importer per i Certificati Campione."""

    CERTIFICATI_CAMPIONE_MAPPING: ClassVar[dict[str, str]] = {
        "ID-COEMI": "id_coemi",
        "Certificato Taratura": "certificato",
        "Modello / Tipo": "modello",
        "Costruttore": "costruttore",
        "Matricola": "matricola",
        "Range Strumento": "range_strumento",
        "Errore max %": "errore_max",
        "Emissione Certificato": "emissione",
        "Scadenza Certificato": "scadenza",
        "Stato Certificato": "stato",
    }

    CERTIFICATI_CAMPIONE_COLS: ClassVar[list[str]] = list(CERTIFICATI_CAMPIONE_MAPPING.values())

    @classmethod
    def import_certificati_campione(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        """Importa il file Certificati Campione e restituisce le righe."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", []

        try:
            pd_obj = cls._get_pd()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                xls = pd_obj.ExcelFile(path)
                sheet_name = cls._find_certificati_sheet(xls)
                if not sheet_name:
                    return False, "Nessun foglio trovato.", []

                df, header_idx = cls._read_certificati_data(path, sheet_name)
                if df.empty:
                    return False, "Foglio vuoto.", []

                return cls._process_certificati_df(df, sheet_name, header_idx)
        except Exception as e:
            return False, f"Errore importazione Certificati: {e}", []

    @classmethod
    def _find_certificati_sheet(cls, xls: pd.ExcelFile) -> str | None:
        """Trova il foglio corretto per i certificati."""
        for name in xls.sheet_names:
            n_low = str(name).lower()
            if "strumenti campione" in n_low or "isab sud" in n_low:
                return str(name)
        return str(xls.sheet_names[0]) if xls.sheet_names else None

    @classmethod
    def _read_certificati_data(cls, path: Path, sheet_name: str) -> tuple[pd.DataFrame, int]:
        """Legge i dati individuando l'intestazione."""
        pd_obj = cls._get_pd()
        df_preview = pd_obj.read_excel(path, sheet_name=sheet_name, header=None, nrows=20)
        header_idx = cls._detect_certificati_header(df_preview)
        df = pd_obj.read_excel(path, sheet_name=sheet_name, header=header_idx)
        return df, header_idx

    @classmethod
    def _detect_certificati_header(cls, df_preview: pd.DataFrame) -> int:
        """Detects the header row index for Certificati Campione, prioritizing ID-COEMI."""
        header_row_idx = -1
        max_matches = 0
        target_columns = set(cls.CERTIFICATI_CAMPIONE_MAPPING.keys())

        for i, row in df_preview.iterrows():
            row_values = [str(val).strip() for val in row.values]
            # Diamo peso doppio all'ID-COEMI nel rilevamento
            matches = sum(2 if col == "ID-COEMI" and col in row_values else 1
                         for col in target_columns if col in row_values)

            if matches > max_matches:
                max_matches = matches
                header_row_idx = int(str(i))

        # Se non rilevato o incerto, impostiamo riga 5 (che corrisponde alla riga 6 di Excel)
        # In questo modo i dati iniziano dalla riga 7.
        if header_row_idx == -1 or max_matches < 2:  # noqa: PLR2004
            header_row_idx = 5

        return header_row_idx

    @classmethod
    def _process_certificati_df(
        cls, df: pd.DataFrame, sheet_name: str, header_row_idx: int
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        """Processes the Certificati DataFrame and returns formatted rows."""
        df.columns = df.columns.astype(str).str.strip()

        # 1. Mapping e Validazione Colonne
        rename_map = cls._build_certificati_rename_map(df.columns.tolist())
        if not rename_map:
            found_cols = ", ".join(list(df.columns)[:5]) + "..."
            return (
                False,
                f"Nessuna colonna valida trovata. Sheet: {sheet_name}, Row: {header_row_idx}. Trovate: {found_cols}",
                [],
            )

        df.rename(columns=rename_map, inplace=True)

        # 2. Schema, 3. Formatting, 4. Cleanup
        df = (
            cls._apply_certificati_formatting(cls._normalize_certificati_schema(df))
            .fillna("")
            .astype(str)
            .apply(lambda x: x.str.strip())
        )

        return (
            True,
            f"Importate {len(df)} righe in Certificati Campione.",
            list(df.itertuples(index=False, name=None)),
        )

    @classmethod
    def _build_certificati_rename_map(cls, columns: list[str]) -> dict[str, str]:
        """Costruisce la mappa di rinomina colonne basata sul mapping definito."""
        rename_map = {}
        for col in columns:
            col_clean = col.strip()
            # Cerca match esatto o parziale nel mapping
            for schema_col, db_col in cls.CERTIFICATI_CAMPIONE_MAPPING.items():
                if schema_col.lower() == col_clean.lower():
                    rename_map[col] = db_col
                    break
                # Fallback: se la colonna contiene la stringa schema (es. "Data\nScadenza")
                if schema_col in col_clean:
                    rename_map[col] = db_col
        return rename_map

    @classmethod
    def _normalize_certificati_schema(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Assicura l'ordine e l'esistenza delle colonne richieste."""
        target_cols = list(cls.CERTIFICATI_CAMPIONE_MAPPING.values())
        for c in target_cols:
            if c not in df.columns:
                df[c] = ""
        df = df[target_cols]
        df.dropna(how="all", inplace=True)
        return df

    @classmethod
    def _apply_certificati_formatting(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Applica formattazione date e calcolo giorni scadenza."""
        pd_obj = cls._get_pd()

        def format_date_it(val: Any) -> str:
            if pd_obj.isna(val) or val == "":
                return ""
            try:
                dt = pd_obj.to_datetime(val)
                return str(dt.strftime("%d/%m/%Y"))
            except Exception:
                return str(val)

        def format_stato(val: Any) -> str:
            if pd_obj.isna(val) or val == "":
                return ""
            try:
                num = float(val)
                days = round(num)
                if days > 0:
                    return f"Scade tra {days} giorni"
                if days < 0:
                    return f"Scaduto da {abs(days)} giorni"
                return "Scade oggi"  # noqa: TRY300
            except (ValueError, TypeError):
                return str(val)

        def format_errore_max(val: Any) -> str:
            if pd_obj.isna(val) or val == "":
                return ""
            try:
                # Se è un float (es. 0.0005 da Excel per 0.05%), lo convertiamo e formattiamo
                num = float(val)
                return f"{num * 100:g}%".replace(".", ",")
            except (ValueError, TypeError):
                # Se è già una stringa formattata o altro
                return str(val).replace(".", ",")

        df["scadenza"] = df["scadenza"].apply(format_date_it)
        df["emissione"] = df["emissione"].apply(format_date_it)
        if "stato" in df.columns:
            df["stato"] = df["stato"].apply(format_stato)
        if "errore_max" in df.columns:
            df["errore_max"] = df["errore_max"].apply(format_errore_max)
        return df
