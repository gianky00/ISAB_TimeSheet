import warnings
import zipfile
from typing import Any, ClassVar

import pandas as pd

from src.core.logging import get_logger
from src.core.processing.base import ProcessingStep
from src.core.schemas import validate_giornaliere

logger = get_logger(__name__)


class ReadGiornalieraStep(ProcessingStep):
    """Legge il foglio 'RIASSUNTO' da un file Excel (può essere Path o BytesIO)."""

    def execute(self, context: dict[str, Any]) -> None:
        file_obj = context.get("file_obj") or context["file_path"]
        file_name = context["file_path"].name if hasattr(context["file_path"], "name") else "Sconosciuto"

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                df = pd.read_excel(file_obj, sheet_name="RIASSUNTO")
            except (ValueError, zipfile.BadZipFile):
                pass
            except Exception:
                try:
                    df = pd.read_excel(file_obj, sheet_name="RIASSUNTO", engine="openpyxl")
                except Exception as e:
                    logger.debug(f"OpenPyXL fallback fallito: {e}")
                else:
                    context["df"] = df
                    context["success"] = True
                    return
            else:
                context["df"] = df
                context["success"] = True
                return

        context["success"] = False
        context["message"] = f"Impossibile leggere il file {file_name}"
        logger.debug(f"Impossibile leggere foglio RIASSUNTO da {file_name}")


class NormalizeGiornalieraStep(ProcessingStep):
    """Normalizza e pulisce i dati della giornaliera."""

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

    def execute(self, context: dict[str, Any]) -> None:
        if not context.get("success") or "df" not in context:
            return

        df = context["df"]
        df.columns = df.columns.astype(str).str.strip()
        rename_map = {}

        for excel_col, db_col in self.GIORNALIERE_MAPPING.items():
            if excel_col in df.columns:
                rename_map[excel_col] = db_col
            else:
                for col in df.columns:
                    if col.upper() == excel_col.upper():
                        rename_map[col] = db_col
                        break

        if not rename_map:
            context["success"] = False
            return

        df.rename(columns=rename_map, inplace=True)

        try:
            df = validate_giornaliere(df)
        except Exception as e:
            logger.warning(f"Validazione Pandera Giornaliere fallita (uso fallback): {e}")

        df = self._clean_data(df)
        if df.empty:
            context["success"] = False
            return

        context["df"] = df

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
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

        critical_cols = [c for c in ["data", "personale", "ore"] if c in df.columns]
        if critical_cols:
            df.dropna(subset=critical_cols, how="any", inplace=True)

        return df


class EnrichGiornalieraStep(ProcessingStep):
    """Arricchisce i dati della giornaliera con ODC da mapping e pattern matching."""

    def execute(self, context: dict[str, Any]) -> None:
        if not context.get("success") or "df" not in context:
            return

        df = context["df"]
        lookup_map = context.get("lookup_map", {})

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

        df["year"] = context["year"]
        df["nome_file"] = context["file_path"].name if hasattr(context["file_path"], "name") else "Sconosciuto"

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

        context["rows"] = list(df[target_cols].itertuples(index=False, name=None))
