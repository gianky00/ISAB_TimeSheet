"""Passaggi di elaborazione per l'importazione dei Certificati Campione."""

from pathlib import Path
from typing import Any, ClassVar

import numpy as np
import pandas as pd

from src.core.logging import get_logger
from src.core.processing.base import ProcessingStep

logger = get_logger(__name__)


class ReadCertificatiExcelStep(ProcessingStep):
    """Legge il file Excel dei certificati campione, rilevando header e sheet."""

    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la lettura del file Excel."""
        file_path = context["file_path"]
        path = Path(file_path)

        xls = pd.ExcelFile(path)
        sheet_name = self._find_sheet(xls)
        if not sheet_name:
            context["success"] = False
            context["message"] = "Nessun foglio trovato."
            return

        # Scansione header più profonda (100 righe invece di 30)
        df_preview = pd.read_excel(path, sheet_name=sheet_name, header=None, nrows=100)
        header_idx = self._detect_header(df_preview)

        try:
            df = pd.read_excel(path, sheet_name=sheet_name, header=header_idx)
        except Exception:
            # Fallback su openpyxl per file complessi o xlsm
            df = pd.read_excel(path, sheet_name=sheet_name, header=header_idx, engine="openpyxl")

        if df.empty:
            context["success"] = False
            context["message"] = "Foglio vuoto."
            return

        context["df"] = df
        context["sheet_name"] = sheet_name
        context["header_idx"] = header_idx

    def _find_sheet(self, xls: pd.ExcelFile) -> str | None:
        """Individua il foglio Excel più pertinente per i certificati."""
        for name in xls.sheet_names:
            n_low = str(name).lower()
            if "strumenti campione" in n_low or "isab sud" in n_low or "registro" in n_low:
                return str(name)
        return str(xls.sheet_names[0]) if xls.sheet_names else None

    def _detect_header(self, df_preview: pd.DataFrame) -> int:
        """Rileva l'indice della riga di intestazione basandosi su parole chiave."""
        header_row_idx = -1
        max_matches = 0
        keywords = {
            "ID-COEMI",
            "ID COEMI",
            "ID-STRUMENTO",
            "ID STRUMENTO",
            "MATRICOLA",
            "CERTIFICATO",
            "SCADENZA",
        }

        for i, row in df_preview.iterrows():
            row_values = [str(val).strip().upper() for val in row.values]
            matches = sum(1 for kw in keywords if any(kw in rv for rv in row_values))

            if matches > max_matches:
                max_matches = matches
                header_row_idx = int(str(i))

        if header_row_idx == -1 or max_matches < 2:  # noqa: PLR2004
            header_row_idx = 5
        return header_row_idx


class NormalizeCertificatiStep(ProcessingStep):
    """Rinomina, normalizza le colonne e filtra righe vuote o invalide."""

    MIN_VALID_COLS = 3
    MIN_MATCH_LEN = 3

    CERTIFICATI_CAMPIONE_MAPPING: ClassVar[dict[str, str]] = {
        "ID-COEMI": "id_coemi",
        "ID COEMI": "id_coemi",
        "ID-STRUMENTO": "id_coemi",
        "ID STRUMENTO": "id_coemi",
        "ID": "id_coemi",
        "IDENTIFICATIVO": "id_coemi",
        "Certificato Taratura": "certificato",
        "CERTIFICATO": "certificato",
        "CERT.": "certificato",
        "N. CERT.": "certificato",
        "N. CERTIFICATO": "certificato",
        "Modello / Tipo": "modello",
        "MODELLO": "modello",
        "TIPO": "modello",
        "Costruttore": "costruttore",
        "COSTRUTTORE": "costruttore",
        "MARCA": "costruttore",
        "Matricola": "matricola",
        "MATRICOLA": "matricola",
        "S/N": "matricola",
        "SERIAL": "matricola",
        "Range Strumento": "range_strumento",
        "RANGE": "range_strumento",
        "CAMPO SCALA": "range_strumento",
        "Errore max %": "errore_max",
        "ERR %": "errore_max",
        "ERROR %": "errore_max",
        "PRECISIONE": "errore_max",
        "Emissione Certificato": "emissione",
        "EMISSIONE": "emissione",
        "DATA EMISSIONE": "emissione",
        "DATA CERT.": "emissione",
        "Scadenza Certificato": "scadenza",
        "SCADENZA": "scadenza",
        "DATA SCADENZA": "scadenza",
        "SCAD.": "scadenza",
        "Stato Certificato": "stato",
        "STATO": "stato",
    }

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

    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la normalizzazione dei dati."""
        if not context.get("df") is not None:
            return

        df = context["df"]
        df.columns = df.columns.astype(str).str.strip()

        rename_map = self._build_rename_map(df.columns.tolist())
        if len(rename_map) < self.MIN_VALID_COLS:
            context["success"] = False
            context["message"] = "Nessuna colonna valida trovata."
            return

        df.rename(columns=rename_map, inplace=True)

        for c in self.CERTIFICATI_CAMPIONE_COLS:
            if c not in df.columns:
                df[c] = ""
        df = df[self.CERTIFICATI_CAMPIONE_COLS]
        df.dropna(how="all", inplace=True)

        # Riempimento e normalizzazione testo
        df = df.fillna("").astype(str).apply(lambda x: x.str.strip())

        # Forward fill per ID e Matricola (per gestire righe raggruppate in Excel)
        for col in ("id_coemi", "matricola"):
            if col in df.columns:
                df[col] = df[col].replace("", np.nan).ffill().fillna("")

        def get_col_safe(name: str) -> Any:
            """Recupera una colonna in modo sicuro gestendo DataFrame multi-indice."""
            col = df[name]
            if hasattr(col, "iloc") and not hasattr(col, "name"):
                return col.iloc[:, 0]
            return col

        mask_empty = (get_col_safe("id_coemi") == "") & (get_col_safe("matricola") == "")
        df = df[~mask_empty]

        context["df"] = df

    def _build_rename_map(self, columns: list[str]) -> dict[str, str]:
        """Costruisce una mappa di rinomina per le colonne del DataFrame."""
        rename_map = {}
        used_db_cols = set()

        for col in columns:
            col_clean = col.strip().upper()
            for schema_col, db_col in self.CERTIFICATI_CAMPIONE_MAPPING.items():
                if db_col in used_db_cols:
                    continue
                if schema_col.upper() == col_clean:
                    rename_map[col] = db_col
                    used_db_cols.add(db_col)
                    break

        for col in columns:
            if col in rename_map:
                continue
            col_clean = col.strip().upper()
            for schema_col, db_col in self.CERTIFICATI_CAMPIONE_MAPPING.items():
                if db_col in used_db_cols:
                    continue
                s_up = schema_col.upper()
                if s_up in col_clean and len(s_up) > self.MIN_MATCH_LEN:
                    rename_map[col] = db_col
                    used_db_cols.add(db_col)
                    break
        return rename_map


class FormatCertificatiStep(ProcessingStep):
    """Applica formattazione a date, percentuali e stati, ripulendo tag debug."""

    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la formattazione dei campi."""
        if not context.get("df") is not None:
            return

        df = context["df"]

        df["scadenza"] = df["scadenza"].apply(self._format_date)
        df["emissione"] = df["emissione"].apply(self._format_date)

        if "stato" in df.columns:
            df["stato"] = df["stato"].apply(self._format_stato)
        if "errore_max" in df.columns:
            df["errore_max"] = df["errore_max"].apply(self._format_errore_max)

        for col in df.columns:
            df[col] = df[col].str.replace(r"\[ROSSO\]", "", regex=True)
            df[col] = df[col].str.replace(r"\[ERRORE\]", "", regex=True)
            df[col] = df[col].str.replace(r"\[GIALLO\]", "", regex=True)
            df[col] = df[col].str.replace(r"\[VERDE\]", "", regex=True)
            df[col] = df[col].str.strip()

        context["df"] = df
        context["rows"] = list(df.itertuples(index=False, name=None))
        context["success"] = True
        context["message"] = f"Importate {len(df)} righe in Certificati Campione."

    @staticmethod
    def _format_date(val: Any) -> str:
        """Formatta un valore in data stringa DD/MM/YYYY."""
        if pd.isna(val) or val == "" or str(val).strip() == "nan":
            return ""
        try:
            dt = pd.to_datetime(val)
            return str(dt.strftime("%d/%m/%Y"))
        except Exception:
            return str(val).split(" ")[0]

    @staticmethod
    def _format_stato(val: Any) -> str:
        if pd.isna(val) or val == "":
            return ""
        try:
            days = round(float(val))
        except (ValueError, TypeError):
            return str(val)
        else:
            if days > 0:
                return f"Scade tra {days} giorni"
            if days < 0:
                return f"Scaduto da {abs(days)} giorni"
            return "Scade oggi"

    @staticmethod
    def _format_errore_max(val: Any) -> str:
        if pd.isna(val) or val == "" or str(val).strip() == "nan":
            return ""
        try:
            if "%" in str(val):
                return str(val)
            num = float(val)
            if num < 1:
                return f"{num * 100:g}%".replace(".", ",")
            return f"{num:g}%".replace(".", ",")
        except (ValueError, TypeError):
            return str(val).replace(".", ",")


class SyncCertificatiStep(ProcessingStep):
    """Passaggio per la sincronizzazione dei certificati con il database."""

    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la sincronizzazione dei dati con il database."""
        if not context.get("success"):
            return

        rows = context.get("rows", [])
        if not rows:
            return

        from src.core.data_synchronizer import DataSynchronizer  # noqa: PLC0415
        from src.core.database import db_manager  # noqa: PLC0415

        total_added, total_removed = DataSynchronizer.sync_certificati_campione(
            db_manager.DB_CONTABILITA, rows
        )

        context["total_added"] = total_added
        context["total_removed"] = total_removed
        context["success"] = True
