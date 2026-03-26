import logging
import re
import zipfile
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.core.importers.base import BaseImporter
from src.core.schemas import validate_contabilita

logger = logging.getLogger(__name__)


class ContabilitaImporter(BaseImporter):
    """Importer specifico per i dati di ContabilitÃ ."""

    # Mapping colonne Excel -> DB
    COLUMNS_MAPPING: ClassVar[dict[str, str]] = {
        "DATA PREV.": "data_prev",
        "MESE": "mese",
        "NÂ° PREV.": "n_prev",
        "TOTALE PREV.": "totale_prev",
        "ATTIVITA'": "attivita",
        "TCL": "tcl",
        "ODC": "odc",
        "STATO ATTIVITA'": "stato_attivita",
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
            logger.error(f"Errore importazione Excel: {e}")  # noqa: TRY400
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
    def _process_single_sheet(cls, xls: Any, sheet_name: str, year: int) -> list[tuple[Any, ...]]:  # noqa: PLR0915
        """Processa un singolo foglio del file Excel di contabilitÃ ."""
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

            # Pulizia preliminare righe vuote
            df.dropna(how="all", inplace=True)

            if df.empty:
                return []

            df["year"] = year
            df = cls._normalize_columns(df)
            df = cls._ensure_required_columns(df)

            # Preparazione finale dati
            target_columns = ["year", *list(cls.COLUMNS_MAPPING.values())]
            df = df[target_columns].copy()

            # --- Gestione Tipi Intelligente ---
            def _clean_numeric(val: Any) -> float:
                if pd_obj.isna(val) or val == "":
                    return 0.0
                if isinstance(val, (int, float)):
                    return float(val)
                # Gestione stringhe con formati IT/EN (1.234,56 o 1,234.56)
                s = str(val).strip().replace("€", "").replace(" ", "")
                if not s:
                    return 0.0
                try:
                    # Se ha sia punto che virgola, determiniamo il formato
                    if "." in s and "," in s:
                        if s.find(".") < s.find(","):  # IT: 1.234,56
                            s = s.replace(".", "").replace(",", ".")
                        else:  # EN: 1,234.56
                            s = s.replace(",", "")
                    else:
                        # Solo uno dei due: se è virgola, è decimale IT
                        s = s.replace(",", ".")
                    return float(s)
                except ValueError:
                    return 0.0

            for col in df.columns:
                if col == "year":
                    continue

                if col in ("totale_prev", "ore_sp"):
                    df[col] = df[col].apply(_clean_numeric)
                    df[col] = df[col].round(2)

                elif col == "data_prev":
                    df[col] = pd_obj.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d").fillna("")

                elif col == "resa":
                    df[col] = df[col].apply(
                        lambda x: (
                            str(round(float(x), 2))
                            if pd_obj.notna(x)
                            and str(x).replace(".", "").replace(",", "").replace("-", "").isdigit()
                            else str(x).strip()
                            if pd_obj.notna(x)
                            else ""
                        )
                    )
                else:
                    df[col] = df[col].astype(str).str.strip().replace(r"(?i)^nan$", "", regex=True).fillna("")

            # Validazione Pandera finale su dati puliti
            try:
                df = validate_contabilita(df)
            except Exception as e:
                logger.warning(f"Validazione Pandera ContabilitÃ  fallita (uso fallback): {e}")

            return list(df.itertuples(index=False, name=None))
        except Exception as e:
            logger.warning(f"Errore processamento foglio {sheet_name}: {e}")
            import traceback  # noqa: PLC0415

            logger.debug(traceback.format_exc())
            return []

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
                .replace("°", "")
                .replace("Â", "")
                .replace("N", "N")
            )

        key_cols_norm = ["DATAPREV", "MESE", "NPREV", "TOTALEPREV", "ATTIVITA", "ODC"]

        for i_raw, row in preview_df.iterrows():
            row_vals = [_norm(val) for val in row.values]
            if sum(1 for k in key_cols_norm if k in row_vals) >= 2:  # noqa: PLR2004
                return int(i_raw)
        return 0

    @classmethod
    def _normalize_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Rinomina le colonne del DataFrame usando la mappa interna."""

        def _norm(v: Any) -> str:
            return str(v).strip().upper().replace(" ", "").replace(".", "").replace("°", "").replace("Â", "")

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
