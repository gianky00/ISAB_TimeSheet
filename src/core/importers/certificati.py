import logging
import warnings
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.core.importers.base import BaseImporter


class CertificatiImporter(BaseImporter):
    """Importer per i Certificati Campione."""

    # Mapping esteso per supportare sia nomi lunghi che brevi (comuni nei file Excel)
    # Rinominiamo id_strumento -> id_coemi internamente
    CERTIFICATI_CAMPIONE_MAPPING: ClassVar[dict[str, str]] = {
        "ID-COEMI": "id_coemi",
        "ID COEMI": "id_coemi",
        "ID-STRUMENTO": "id_coemi",
        "ID STRUMENTO": "id_coemi",
        "Certificato Taratura": "certificato",
        "CERTIFICATO": "certificato",
        "Modello / Tipo": "modello",
        "MODELLO": "modello",
        "TIPO": "modello",
        "Costruttore": "costruttore",
        "COSTRUTTORE": "costruttore",
        "Matricola": "matricola",
        "MATRICOLA": "matricola",
        "Range Strumento": "range_strumento",
        "RANGE": "range_strumento",
        "Errore max %": "errore_max",
        "ERR %": "errore_max",
        "ERROR %": "errore_max",
        "Emissione Certificato": "emissione",
        "EMISSIONE": "emissione",
        "Scadenza Certificato": "scadenza",
        "SCADENZA": "scadenza",
        "Stato Certificato": "stato",
        "STATO": "stato",
    }

    # Colonne effettive del DB (senza duplicati di mapping)
    CERTIFICATI_CAMPIONE_COLS: ClassVar[list[str]] = [
        "id_coemi",
        "certificato",
        "modello",
        "costruttore",
        "matricola",
        "range_strumento",
        "errore_max",
        "emissione",
        "scadenza",
        "stato",
    ]

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
            importer_logger = logging.getLogger(__name__)
            importer_logger.info(f"Avvio lettura Excel certificati: {file_path}")

            pd_obj = cls._get_pd()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                xls = pd_obj.ExcelFile(path)
                sheet_name = cls._find_certificati_sheet(xls)
                importer_logger.info(f"Foglio rilevato: {sheet_name}")

                if not sheet_name:
                    return False, "Nessun foglio trovato.", []

                df, header_idx = cls._read_certificati_data(path, sheet_name)
                importer_logger.info(f"Dati letti. Header rilevato a riga: {header_idx}, Righe trovate: {len(df)}")

                if df.empty:
                    return False, "Foglio vuoto.", []

                res_success, res_msg, rows = cls._process_certificati_df(df, sheet_name, header_idx)
                importer_logger.info(f"Processamento completato. Success: {res_success}, Messaggio: {res_msg}, Tuple generate: {len(rows)}")
                return res_success, res_msg, rows
        except Exception as e:
            return False, f"Errore importazione Certificati: {e}", []

    @classmethod
    def _find_certificati_sheet(cls, xls: pd.ExcelFile) -> str | None:
        """Trova il foglio corretto per i certificati."""
        for name in xls.sheet_names:
            n_low = str(name).lower()
            if "strumenti campione" in n_low or "isab sud" in n_low or "registro" in n_low:
                return str(name)
        return str(xls.sheet_names[0]) if xls.sheet_names else None

    @classmethod
    def _read_certificati_data(cls, path: Path, sheet_name: str) -> tuple[pd.DataFrame, int]:
        """Legge i dati individuando l'intestazione."""
        pd_obj = cls._get_pd()
        df_preview = pd_obj.read_excel(path, sheet_name=sheet_name, header=None, nrows=30)
        header_idx = cls._detect_certificati_header(df_preview)
        # Leggiamo con l'header rilevato
        df = pd_obj.read_excel(path, sheet_name=sheet_name, header=header_idx)
        return df, header_idx

    @classmethod
    def _detect_certificati_header(cls, df_preview: pd.DataFrame) -> int:
        """Rileva l'indice della riga di intestazione basandosi sulle parole chiave."""
        header_row_idx = -1
        max_matches = 0

        # Parole chiave critiche per l'intestazione
        keywords = {"ID-COEMI", "ID COEMI", "ID-STRUMENTO", "ID STRUMENTO", "MATRICOLA", "CERTIFICATO", "SCADENZA"}

        for i, row in df_preview.iterrows():
            row_values = [str(val).strip().upper() for val in row.values]
            matches = sum(1 for kw in keywords if any(kw in str(rv) for rv in row_values))

            if matches > max_matches:
                max_matches = matches
                header_row_idx = int(str(i))

        # Se non rilevato o incerto, proviamo riga 5 o 6 come fallback comune
        if header_row_idx == -1 or max_matches < 2:  # noqa: PLR2004
            header_row_idx = 5

        return header_row_idx

    @classmethod
    def _process_certificati_df(
        cls, df: pd.DataFrame, sheet_name: str, header_row_idx: int
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        """Processa il DataFrame dei Certificati e restituisce le righe formattate."""
        df.columns = df.columns.astype(str).str.strip()

        # 1. Mapping e Validazione Colonne
        rename_map = cls._build_certificati_rename_map(df.columns.tolist())
        min_required_cols = 3
        if not rename_map or len(rename_map) < min_required_cols: # Almeno ID, Matricola e Scadenza
            found_cols = ", ".join(list(df.columns)[:8]) + "..."
            return (
                False,
                f"Nessuna colonna valida trovata (Trovate: {len(rename_map)}/10). Sheet: {sheet_name}, Row: {header_row_idx}. Colonne Excel: {found_cols}",
                [],
            )

        df.rename(columns=rename_map, inplace=True)

        # 2. Schema, 3. Formatting, 4. Cleanup
        df = cls._normalize_certificati_schema(df)
        df = cls._apply_certificati_formatting(df)

        # Riempimento e normalizzazione testo
        df = df.fillna("").astype(str).apply(lambda x: x.str.strip())

        # 5. Rimuovi righe vuote in modo robusto (gestione eventuale duplicazione colonne)
        def get_col_safe(name: str) -> Any:
            col = df[name]
            # Gestione caso DataFrame se ci sono colonne duplicate nel file Excel
            if hasattr(col, "iloc") and not hasattr(col, "name"):
                return col.iloc[:, 0]  # type: ignore[call-overload]
            return col

        mask_empty = (get_col_safe('id_coemi') == "") & (get_col_safe('matricola') == "")
        df = df[~mask_empty]

        # 6. Professionalize: Remove debug tags
        for col in df.columns:
            df[col] = df[col].str.replace(r"\[ROSSO\]", "", regex=True)
            df[col] = df[col].str.replace(r"\[ERRORE\]", "", regex=True)
            df[col] = df[col].str.replace(r"\[GIALLO\]", "", regex=True)
            df[col] = df[col].str.replace(r"\[VERDE\]", "", regex=True)
            df[col] = df[col].str.strip()

        return (
            True,
            f"Importate {len(df)} righe in Certificati Campione.",
            list(df.itertuples(index=False, name=None)),
        )

    @classmethod
    def _build_certificati_rename_map(cls, columns: list[str]) -> dict[str, str]:
        """Costruisce la mappa di rinomina colonne basata sul mapping definito."""
        rename_map = {}
        used_db_cols = set()

        # Priorità al matching ID-COEMI
        for col in columns:
            col_clean = col.strip().upper()
            for schema_col, db_col in cls.CERTIFICATI_CAMPIONE_MAPPING.items():
                if db_col in used_db_cols:
                    continue
                s_up = schema_col.upper()
                if s_up == col_clean:
                    rename_map[col] = db_col
                    used_db_cols.add(db_col)
                    break

        # Secondo giro per matching parziale (fallback)
        min_label_len = 3
        for col in columns:
            if col in rename_map:
                continue
            col_clean = col.strip().upper()
            for schema_col, db_col in cls.CERTIFICATI_CAMPIONE_MAPPING.items():
                if db_col in used_db_cols:
                    continue
                s_up = schema_col.upper()
                if s_up in col_clean and len(s_up) > min_label_len:
                    rename_map[col] = db_col
                    used_db_cols.add(db_col)
                    break
        return rename_map

    @classmethod
    def _normalize_certificati_schema(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Assicura l'ordine e l'esistenza delle colonne richieste."""
        target_cols = cls.CERTIFICATI_CAMPIONE_COLS
        for c in target_cols:
            if c not in df.columns:
                df[c] = ""
        df = df[target_cols]
        df.dropna(how="all", inplace=True)
        return df

    @staticmethod
    def _format_date_it(val: Any) -> str:
        """Helper per formattare date in stile IT."""
        if pd.isna(val) or val == "" or str(val).strip() == "nan":
            return ""
        try:
            dt = pd.to_datetime(val)
            return str(dt.strftime("%d/%m/%Y"))
        except Exception:
            # Rimuoviamo eventuale timestamp 00:00:00
            s = str(val).split(" ")[0]
            return s

    @staticmethod
    def _format_stato(val: Any) -> str:
        """Helper per formattare la descrizione dello stato scadenza."""
        if pd.isna(val) or val == "":
            return ""
        try:
            num = float(val)
            days = round(num)
            if days > 0:
                return f"Scade tra {days} giorni"
            if days < 0:
                return f"Scaduto da {abs(days)} giorni"
            res = "Scade oggi"
        except (ValueError, TypeError):
            return str(val)

        return res

    @staticmethod
    def _format_errore_max(val: Any) -> str:
        """Helper per formattare l'errore massimo in percentuale."""
        if pd.isna(val) or val == "" or str(val).strip() == "nan":
            return ""
        try:
            # Se è già una stringa con %, la lasciamo così
            if "%" in str(val):
                return str(val)
            num = float(val)
            if num < 1: # Probabile decimale 0.01 -> 1%
                return f"{num * 100:g}%".replace(".", ",")
            return f"{num:g}%".replace(".", ",")
        except (ValueError, TypeError):
            return str(val).replace(".", ",")

    @classmethod
    def _apply_certificati_formatting(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Applica formattazione date e calcolo giorni scadenza."""
        df["scadenza"] = df["scadenza"].apply(cls._format_date_it)
        df["emissione"] = df["emissione"].apply(cls._format_date_it)
        if "stato" in df.columns:
            df["stato"] = df["stato"].apply(cls._format_stato)
        if "errore_max" in df.columns:
            df["errore_max"] = df["errore_max"].apply(cls._format_errore_max)
        return df
