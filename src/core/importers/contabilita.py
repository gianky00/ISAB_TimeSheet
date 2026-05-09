import re
import zipfile
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.core.importers.base import BaseImporter
from src.core.logging import get_logger
from src.core.schemas import validate_contabilita

logger = get_logger(__name__)


class ContabilitaImporter(BaseImporter):
    """Importer specifico per i dati di Contabilità ."""

    # Mapping colonne Excel -> DB
    COLUMNS_MAPPING: ClassVar[dict[str, str]] = {
        "DATA PREV.": "data_prev",
        "MESE": "mese",
        "N   PREV.": "n_prev",
        "TOTALE PREV.": "totale_prev",
        "ATTIVITÀ": "attivita",
        "TCL": "tcl",
        "ODC": "odc",
        "STATO ATTIVITÀ": "stato_attivita",
        "TIPOLOGIA": "tipologia",
        "ORE SP": "ore_sp",
        "RESA": "resa",
        "ANNOTAZIONI": "annotazioni",
        "INDIRIZZO CONSUNTIVO": "indirizzo_consuntivo",
        "NOME FILE": "nome_file",
    }

    @classmethod
    def scan_sheets(cls, file_path: str) -> int:
        """Conta i fogli validi nell'Excel principale (metodo veloce)."""
        p_file = Path(file_path)
        if not file_path or not p_file.exists():
            return 0
        try:
            # Check if valid zip before opening
            if not zipfile.is_zipfile(p_file):
                # Maybe old xls format (OLE) -> fallback 1 sheet
                return 1

            with zipfile.ZipFile(p_file, "r") as z:
                if "xl/workbook.xml" not in z.namelist():
                    return 1
                wb_xml = z.read("xl/workbook.xml").decode("utf-8")
                sheet_names = re.findall(r'name="([^"]+)"', wb_xml)
                return len([s for s in sheet_names if re.search(r"(\d{4})", s)])
        except Exception as e:
            logger.debug(f"Scan excel sheets error: {e}")
            return 1

    @classmethod
    def import_contabilita_dati(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]], list[int]]:
        """
        Importa i dati dal file Excel specificato (Tabella Dati).
        """
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", [], []

        try:
            file_obj, _ = cls._decrypt_if_encrypted(path)
            xls = cls._get_excel_file(file_obj)

            valid_sheets = [str(s) for s in xls.sheet_names if cls._identify_sheet_year(str(s))]
            if not valid_sheets:
                return (
                    False,
                    "Nessun anno importato (Controlla nomi fogli: YYYY o 'Dati/Preventivi').",
                    [],
                    [],
                )

            all_rows, imported_years = cls._process_all_sheets(xls, valid_sheets, progress_callback)

            if not imported_years:
                return (
                    False,
                    "Fogli validi trovati ma nessun dato importato (fogli vuoti?).",
                    [],
                    [],
                )

            return (
                True,
                f"Anni importati: {sorted(set(imported_years))}",
                all_rows,
                list(set(imported_years)),
            )

        except Exception as e:
            logger.exception("Errore importazione Excel", exc=e)
            return False, f"Errore critico importazione: {e}", [], []

    @classmethod
    def _process_all_sheets(
        cls,
        xls: Any,
        sheet_names: list[str],
        progress_callback: Callable[[int, int], None] | None,
    ) -> tuple[list[tuple[Any, ...]], list[int]]:
        """Cicla sui fogli e aggrega i risultati."""
        all_rows: list[tuple[Any, ...]] = []
        imported_years: list[int] = []
        total_sheets = len(sheet_names)

        for i, sheet_name in enumerate(sheet_names):
            year = cls._identify_sheet_year(sheet_name)
            if not year:
                continue

            rows = cls._process_single_sheet(xls, sheet_name, year)
            if rows:
                all_rows.extend(rows)
                imported_years.append(year)

            if progress_callback:
                progress_callback(i + 1, total_sheets)

        return all_rows, imported_years

    @classmethod
    def _process_single_sheet(cls, xls: Any, sheet_name: str, year: int) -> list[tuple[Any, ...]]:
        """Processa un singolo foglio del file Excel di contabilità ."""
        try:
            pd_obj = cls._get_pd()
            header_row_idx = cls._find_header_row(xls, sheet_name)

            try:
                df = pd_obj.read_excel(xls, sheet_name=sheet_name, header=header_row_idx, usecols="A:AZ")
            except Exception:
                df = pd_obj.read_excel(xls, sheet_name=sheet_name, header=header_row_idx)

            df.columns = df.columns.astype(str).str.strip().str.upper()

            if not df.empty:
                df = df.iloc[:-1]  # Rimuovi riga dei totali solitamente presente

            df.dropna(how="all", inplace=True)
            if df.empty:
                return []

            df["year"] = year
            df = cls._normalize_columns(df)
            df = cls._ensure_required_columns(df)

            # Selezione e ordinamento colonne
            target_columns = ["year", *list(cls.COLUMNS_MAPPING.values())]
            df = df[target_columns].copy()

            # Pulizia e validazione
            df = cls._clean_dataframe_types(df)

            try:
                df = validate_contabilita(df)
            except Exception as e:
                logger.warning(f"Validazione Pandera Contabilità fallita (uso fallback): {e}")

            return list(df.itertuples(index=False, name=None))
        except Exception as e:
            logger.warning(f"Errore processamento foglio {sheet_name}: {e}")
            logger.debug(f"Traceback: {e}", exc_info=True)
            return []

    @classmethod
    def _clean_dataframe_types(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Pulisce e tipizza le colonne del DataFrame di contabilità ."""
        pd_obj = cls._get_pd()

        for col in df.columns:
            if col == "year":
                continue

            if col in ("totale_prev", "ore_sp"):
                df[col] = df[col].apply(cls._clean_numeric).round(2)

            elif col == "data_prev":
                df[col] = pd_obj.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d").fillna("")

            elif col == "resa":
                df[col] = df[col].apply(cls._clean_resa_value)
            else:
                df[col] = df[col].astype(str).str.strip().replace(r"(?i)^nan$", "", regex=True).fillna("")

        return df

    @classmethod
    def _clean_numeric(cls, val: Any) -> float:
        """Converte un valore generico in float gestendo formati IT/EN."""
        if pd.isna(val) or val == "":
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)

        s = str(val).strip().replace("  ", "").replace(" ", "")
        if not s:
            return 0.0

        try:
            # Se ha sia punto che virgola, determiniamo il formato
            if "." in s and "," in s:
                s = s.replace(".", "").replace(",", ".") if s.find(".") < s.find(",") else s.replace(",", "")
            else:
                # Solo uno dei due: se  virgola,  decimale IT
                s = s.replace(",", ".")
            return float(s)
        except ValueError:
            return 0.0

    @staticmethod
    def _clean_resa_value(val: Any) -> str:
        """Pulisce il valore della colonna Resa."""
        if pd.isna(val):
            return ""
        s_val = str(val).strip()
        if not s_val:
            return ""

        # Rimuove separatori comuni per controllare se  numerico
        clean_s = s_val.replace(".", "").replace(",", "").replace("-", "")
        if clean_s.isdigit():
            # Se  un numero, lo arrotondiamo a 2 decimali e lo stringiamo
            with suppress(ValueError):
                num = float(s_val.replace(",", "."))
                return str(round(num, 2))
        return s_val

    @classmethod
    def _find_header_row(cls, xls: Any, sheet_name: str) -> int:
        """Cerca l'indice della riga di intestazione basandosi su colonne chiave."""
        preview_df = cls._get_pd().read_excel(xls, sheet_name=sheet_name, header=None, nrows=15)

        # Normalizzazione aggressiva per il confronto
        def _norm(v: Any) -> str:
            return (
                str(v)
                .strip()
                .upper()
                .replace(" ", "")
                .replace(".", "")
                .replace(" ", "")
                .replace(" ", "")
                .replace("N", "N")
            )

        key_cols_norm = ["DATAPREV", "MESE", "NPREV", "TOTALEPREV", "ATTIVITA", "ODC"]

        for i_raw, row in preview_df.iterrows():
            row_vals = [_norm(val) for val in row.values]
            if sum(1 for k in key_cols_norm if k in row_vals) >= 2:
                return int(i_raw)
        return 0

    @classmethod
    def _normalize_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Rinomina le colonne del DataFrame usando la mappa interna."""

        def _norm(v: Any) -> str:
            return str(v).strip().upper().replace(" ", "").replace(".", "").replace(" ", "").replace(" ", "")

        normalized_map = {}
        for k, v in cls.COLUMNS_MAPPING.items():
            normalized_map[_norm(k)] = v

        rename_map = {}
        for col in df.columns:
            norm_col = _norm(col)
            if norm_col in normalized_map:
                rename_map[col] = normalized_map[norm_col]
            elif "PREV" in norm_col and "DATA" in norm_col:
                rename_map[col] = "data_prev"
            elif "PREV" in norm_col and ("NUM" in norm_col or "N" in norm_col):
                rename_map[col] = "n_prev"

        df.rename(columns=rename_map, inplace=True)
        return df

    @classmethod
    def _ensure_required_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Assicura che tutte le colonne mappate esistano nel DataFrame."""
        for db_col in cls.COLUMNS_MAPPING.values():
            if db_col not in df.columns:
                df[db_col] = ""
        return df
