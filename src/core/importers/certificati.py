import warnings
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import pandas as pd

from src.core.importers.base import BaseImporter


class CertificatiImporter(BaseImporter):
    """Importer per i Certificati Campione."""

    CERTIFICATI_CAMPIONE_MAPPING = {
        "Modello / Tipo": "modello",
        "Costruttore": "costruttore",
        "Matricola": "matricola",
        "Range Strumento": "range_strumento",
        "Errore max %": "errore_max",
        "Certificato Taratura": "certificato",
        "Scadenza Certificato": "scadenza",
        "Emissione Certificato": "emissione",
        "ID-COEMI": "id_coemi",
        "Stato Certificato": "stato",
    }

    CERTIFICATI_CAMPIONE_COLS = list(CERTIFICATI_CAMPIONE_MAPPING.values())

    @classmethod
    def import_certificati_campione(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        """Importa il file Certificati Campione e restituisce le righe."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", []

        try:
            pd = cls._get_pd()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                xls = pd.ExcelFile(path)
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
    def _find_certificati_sheet(cls, xls: pd.ExcelFile) -> Optional[str]:
        """Trova il foglio corretto per i certificati."""
        for name in xls.sheet_names:
            n_low = str(name).lower()
            if "strumenti campione" in n_low or "isab sud" in n_low:
                return str(name)
        return str(xls.sheet_names[0]) if xls.sheet_names else None

    @classmethod
    def _read_certificati_data(cls, path: Path, sheet_name: str) -> Tuple[pd.DataFrame, int]:
        """Legge i dati individuando l'intestazione."""
        pd = cls._get_pd()
        df_preview = pd.read_excel(path, sheet_name=sheet_name, header=None, nrows=20)
        header_idx = cls._detect_certificati_header(df_preview)
        df = pd.read_excel(path, sheet_name=sheet_name, header=header_idx)
        return df, header_idx

    @classmethod
    def _detect_certificati_header(cls, df_preview: pd.DataFrame) -> int:
        """Detects the header row index for Certificati Campione."""
        header_row_idx = -1
        max_matches = 0
        target_columns = set(cls.CERTIFICATI_CAMPIONE_MAPPING.keys())

        for i_raw, row in df_preview.iterrows():
            i = int(str(i_raw))
            row_values = [str(val).strip() for val in row.values]
            matches = sum(1 for col in target_columns if col in row_values)

            if matches > max_matches:
                max_matches = matches
                header_row_idx = i

        if header_row_idx == -1 or max_matches < 3:
            header_row_idx = 5

        return header_row_idx

    @classmethod
    def _process_certificati_df(
        cls, df: pd.DataFrame, sheet_name: str, header_row_idx: int
    ) -> Tuple[bool, str, List[Tuple]]:
        """Processes the Certificati DataFrame and returns formatted rows."""
        df.columns = [str(c).strip() for c in df.columns]

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

        # 2. Preparazione Schema
        df = cls._normalize_certificati_schema(df)

        # 3. Formattazione Dati (Date e Stati)
        df = cls._apply_certificati_formatting(df)

        # 4. Pulizia Finale
        df = df.fillna("").astype(str).apply(lambda x: x.str.strip())
        rows = list(df.itertuples(index=False, name=None))

        return True, f"Importate {len(rows)} righe in Certificati Campione.", rows

    @classmethod
    def _build_certificati_rename_map(cls, columns: List[str]) -> Dict[str, str]:
        """Costruisce la mappa di rinomina colonne basata sul mapping definito."""
        rename_map = {}
        for col in columns:
            col_clean = str(col).strip()
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
        pd = cls._get_pd()

        def format_date_it(val):
            if pd.isna(val) or val == "":
                return ""
            try:
                dt = pd.to_datetime(val)
                return dt.strftime("%d/%m/%Y")
            except Exception:
                return str(val)

        def format_stato(val):
            if pd.isna(val) or val == "":
                return ""
            try:
                num = float(val)
                days = int(round(num))
                if days > 0:
                    return f"Scade tra {days} giorni"
                elif days < 0:
                    return f"Scaduto da {abs(days)} giorni"
                return "Scade oggi"
            except (ValueError, TypeError):
                return str(val)

        df["scadenza"] = df["scadenza"].apply(format_date_it)
        df["emissione"] = df["emissione"].apply(format_date_it)
        if "stato" in df.columns:
            df["stato"] = df["stato"].apply(format_stato)
        return df
