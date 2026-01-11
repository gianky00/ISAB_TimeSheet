"""
SyncroJob - Excel Importer
Gestisce l'importazione di dati da vari formati Excel.
"""

import io
import json
import logging
import os
import re
import warnings
import zipfile
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import pandas as pd

# Tentativo di importare msoffcrypto
try:
    import msoffcrypto  # type: ignore
except ImportError:
    msoffcrypto = None

# Tentativo di importare openpyxl
try:
    import openpyxl  # type: ignore

    HAS_OPENPYXL = True
except ImportError:
    openpyxl = None  # type: ignore
    HAS_OPENPYXL = False


class ExcelImporter:
    """Gestore per l'importazione di dati da file Excel."""

    # Mapping colonne Excel -> DB (Contabilità / Dati)
    COLUMNS_MAPPING = {
        "DATA PREV.": "data_prev",
        "MESE": "mese",
        "N° PREV.": "n_prev",
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

    # Mapping colonne Excel -> DB (Giornaliere)
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
        "consuntivo": "n_prev",  # Rinominato come richiesto
    }

    # Mapping Scarico Ore Cantiere
    SCARICO_ORE_COLS = [
        "data",
        "pers1",
        "pers2",
        "odc",
        "pos",
        "dalle",
        "alle",
        "totale_ore",
        "descrizione",
        "finito",
        "commessa",
        "styles",
    ]

    # Mapping Attività Programmate
    ATTIVITA_PROGRAMMATE_MAPPING = {
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

    ATTIVITA_PROGRAMMATE_COLS = list(ATTIVITA_PROGRAMMATE_MAPPING.values()) + [
        "styles"
    ]  # Added styles

    # Mapping Certificati Campione
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

    @staticmethod
    def _decrypt_if_encrypted(file_path: Path) -> Tuple[Any, bool]:
        """Tenta di decifrare un file Excel se protetto da password."""
        if msoffcrypto:
            try:
                with open(file_path, "rb") as f:
                    office_file = msoffcrypto.OfficeFile(f)
                    office_file.load_key(password="coemi")
                    temp_decrypted = io.BytesIO()
                    office_file.decrypt(temp_decrypted)
                    temp_decrypted.seek(0)
                    return temp_decrypted, True
            except Exception:
                # Non cifrato o errore msoffcrypto, procediamo col file originale
                pass
        return file_path, False

    @classmethod
    def import_contabilita_dati(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, list, list]:
        """
        Importa i dati dal file Excel specificato (Tabella Dati), gestisce la decrittazione,
        normalizza i dati e restituisce i dataframe per l'anno e le nuove/vecchie righe.
        Non esegue operazioni sul database.
        """
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", [], []

        all_new_rows = []
        imported_years = []

        try:
            file_obj, _ = cls._decrypt_if_encrypted(path)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    xls = pd.ExcelFile(file_obj)
                except Exception:
                    xls = pd.ExcelFile(file_obj, engine="openpyxl")

                valid_sheets = [
                    s for s in xls.sheet_names if re.search(r"(\d{4})", str(s))
                ]
                total_sheets = len(valid_sheets)
                if total_sheets == 0:
                    fallback_sheets = [
                        s
                        for s in xls.sheet_names
                        if str(s).lower() in ["dati", "preventivi", "riepilogo"]
                    ]
                    if fallback_sheets:
                        total_sheets = len(fallback_sheets)

                processed_sheets = 0

                for sheet_name_raw in xls.sheet_names:
                    sheet_name = str(sheet_name_raw)
                    year = None
                    match = re.search(r"(\d{4})", sheet_name)

                    if match:
                        year = int(match.group(1))
                        if not (2000 <= year <= 2100):
                            continue
                    elif sheet_name.lower() in ["dati", "preventivi", "riepilogo"]:
                        year = datetime.now().year
                    else:
                        continue

                    try:
                        preview_df = pd.read_excel(
                            xls, sheet_name=sheet_name, header=None, nrows=10
                        )
                        header_row_idx = 1
                        key_cols_norm = [
                            "DATAPREV",
                            "MESE",
                            "NPREV",
                            "TOTALEPREV",
                            "ATTIVITA",
                            "ODC",
                        ]

                        for i_raw, row in preview_df.iterrows():
                            i = int(str(i_raw))
                            row_norm = []
                            for val in row.values:
                                s = str(val).strip().upper()
                                s = s.replace(" ", "").replace(".", "").replace("°", "")
                                row_norm.append(s)

                            matches = sum(1 for k in key_cols_norm if k in row_norm)
                            if matches >= 2:
                                header_row_idx = i
                                break

                        df = pd.read_excel(
                            xls, sheet_name=sheet_name, header=header_row_idx
                        )
                        df.columns = [str(c).strip().upper() for c in df.columns]

                        if not df.empty:
                            df = df.iloc[:-1]
                        df.dropna(how="all", inplace=True)

                        if df.empty:
                            continue

                        df["year"] = year

                        normalized_map = {}
                        for k, v in cls.COLUMNS_MAPPING.items():
                            norm_k = (
                                k.upper()
                                .replace(" ", "")
                                .replace(".", "")
                                .replace("°", "")
                            )
                            normalized_map[norm_k] = v

                        rename_map = {}
                        for col in df.columns:
                            col_str = str(col).strip().upper()
                            norm_col = (
                                col_str.replace(" ", "")
                                .replace(".", "")
                                .replace("°", "")
                            )

                            if norm_col in normalized_map:
                                rename_map[col] = normalized_map[norm_col]
                            else:
                                if "PREV" in norm_col and "DATA" in norm_col:
                                    rename_map[col] = "data_prev"
                                elif "PREV" in norm_col and (
                                    "N" in norm_col or "NUM" in norm_col
                                ):
                                    rename_map[col] = "n_prev"

                        df.rename(columns=rename_map, inplace=True)

                    except Exception as e:
                        logging.warning(
                            f"Errore durante l'elaborazione del foglio {sheet_name}: {e}"
                        )
                        continue

                    for db_col in cls.COLUMNS_MAPPING.values():
                        if db_col not in df.columns:
                            df[db_col] = ""

                    target_columns = ["year"] + list(cls.COLUMNS_MAPPING.values())
                    df = df[target_columns]
                    df = df.fillna("")
                    cols_to_str = [c for c in df.columns if c != "year"]
                    df[cols_to_str] = df[cols_to_str].astype(str)
                    df[cols_to_str] = df[cols_to_str].apply(lambda x: x.str.strip())

                    rows = list(df.itertuples(index=False, name=None))
                    all_new_rows.extend(rows)
                    imported_years.append(year)

                    processed_sheets += 1
                    if progress_callback:
                        progress_callback(processed_sheets, total_sheets)

                if not imported_years:
                    return (
                        False,
                        "Nessun anno importato (Controlla nomi fogli: YYYY o 'Dati/Preventivi').",
                        [],
                        [],
                    )

                return (
                    True,
                    f"Anni importati: {sorted(set(imported_years))}",
                    all_new_rows,
                    list(set(imported_years)),
                )

        except Exception as e:
            return False, f"Errore: {e}", [], []

    @classmethod
    def _process_single_giornaliera(
        cls, args: Tuple[int, Path, Dict]
    ) -> Tuple[int, List[Tuple], Optional[str]]:
        """Helper per processare un singolo file giornaliera in parallelo."""
        year, file_path, lookup_map = args
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    df = pd.read_excel(file_path, sheet_name="RIASSUNTO")
                except ValueError:
                    return (year, [], None)
                except Exception:
                    try:
                        df = pd.read_excel(
                            file_path, sheet_name="RIASSUNTO", engine="openpyxl"
                        )
                    except Exception as e:
                        return (year, [], str(e))

                df.columns = [str(c).strip() for c in df.columns]

                rename_map = {}
                for excel_col, db_col in cls.GIORNALIERE_MAPPING.items():
                    for c in df.columns:
                        if c.upper() == excel_col.upper():
                            rename_map[c] = db_col
                            break

                if not rename_map:
                    return (year, [], None)

                df.rename(columns=rename_map, inplace=True)

                if not df.empty:
                    df = df.iloc[:-1]

                if "personale" in df.columns and not df.empty:
                    df = df[
                        ~df["personale"].str.contains("Totale", na=False, case=False)
                    ]

                check_cols = [
                    c
                    for c in df.columns
                    if c in cls.GIORNALIERE_MAPPING.values() and c != "data"
                ]
                if check_cols:
                    df.dropna(how="all", subset=check_cols, inplace=True)

                if not df.empty:
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
                    df[cols_to_clean] = (
                        df[cols_to_clean].astype(str).apply(lambda x: x.str.strip())
                    )
                    df[cols_to_clean] = df[cols_to_clean].replace(
                        r"(?i)^nan$", "", regex=True
                    )

                    mask_empty_odc = df["odc"] == ""
                    if mask_empty_odc.any() and lookup_map:
                        mapped_values = df.loc[mask_empty_odc, "n_prev"].map(lookup_map)
                        df.loc[mask_empty_odc, "odc"] = mapped_values.fillna("")

                    mask_still_empty_odc = df["odc"] == ""
                    if mask_still_empty_odc.any():
                        commessa_pattern = r"\b(\d{2}/\d{3})\b"
                        extracted_commessa = df.loc[
                            mask_still_empty_odc, "descrizione"
                        ].str.extract(commessa_pattern, expand=False)
                        df.loc[mask_still_empty_odc, "odc"] = extracted_commessa.fillna(
                            ""
                        )

                    mask_canone = df["odc"].str.contains("canone", case=False, na=False)
                    mask_commessa = df["odc"].str.match(r"^\d{2}/\d{3}$", na=False)
                    mask_standard = ~mask_canone & ~mask_commessa
                    extracted = df.loc[mask_standard, "odc"].str.extract(
                        r"(5400\d+)", expand=False
                    )
                    df.loc[mask_standard, "odc"] = extracted.fillna("")

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
                    df_final = df[target_cols]
                    rows = list(df_final.itertuples(index=False, name=None))
                    return (year, rows, None)

                return (year, [], None)
        except Exception as e:
            return (year, [], str(e))

    @classmethod
    def import_giornaliere(
        cls,
        root_path: str,
        lookup_map: Dict,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple], List[int]]:
        """
        Importa i dati dalle cartelle Giornaliere, processa i file in parallelo,
        e restituisce le righe importate per la sincronizzazione. Non esegue operazioni sul database.
        """
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata.", [], []

        current_year = datetime.now().year

        tasks_args = []
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
                    tasks_args.append((year, file_path, lookup_map))

        total_tasks = len(tasks_args)
        processed_count = 0

        all_new_rows = []
        years_encountered = set()

        if total_tasks > 0:
            # Use ProcessPoolExecutor for CPU-bound Excel parsing
            # Limit max_workers to 4 or cpu_count/2 to avoid memory spikes
            max_workers = min(4, (os.cpu_count() or 1))
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                for result in executor.map(cls._process_single_giornaliera, tasks_args):
                    processed_count += 1
                    if progress_callback:
                        progress_callback(processed_count, total_tasks)

                    r_year, r_rows, r_err = result
                    if r_rows:
                        all_new_rows.extend(r_rows)
                        years_encountered.add(r_year)
                    if r_err:
                        logging.error(f"Errore lettura file (Year {r_year}): {r_err}")

        imported_years = list(years_encountered)
        if not imported_years and total_tasks == 0:
            return (
                True,
                "Nessuna nuova giornaliera trovata (check anno >= "
                + str(current_year)
                + ").",
                [],
                [],
            )

        return (
            True,
            f"Importate Giornaliere: {sorted(imported_years)}",
            all_new_rows,
            imported_years,
        )

    @classmethod
    def import_attivita_programmate(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        """Importa il file Attività Programmate (veloce, senza colori) e restituisce le righe."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Attività Programmate non trovato: {file_path}", []

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    df = pd.read_excel(path, sheet_name="Riepilogo", header=2)
                except ValueError:
                    return False, "Foglio 'Riepilogo' non trovato.", []
                except Exception:
                    try:
                        df = pd.read_excel(
                            path, sheet_name="Riepilogo", header=2, engine="openpyxl"
                        )
                    except Exception as e2:
                        return False, f"Errore lettura file: {e2}", []

            df.columns = [str(c).strip() for c in df.columns]

            rename_map = {}
            for excel_col, db_col in cls.ATTIVITA_PROGRAMMATE_MAPPING.items():
                if excel_col in df.columns:
                    rename_map[excel_col] = db_col
                else:
                    for col in df.columns:
                        if (
                            excel_col.replace("\n", " ").strip()
                            == col.replace("\n", " ").strip()
                        ):
                            rename_map[col] = db_col
                            break

            if not rename_map:
                return False, "Colonne non trovate. Controlla intestazione riga 3.", []

            df.rename(columns=rename_map, inplace=True)

            for db_col in cls.ATTIVITA_PROGRAMMATE_MAPPING.values():
                if db_col not in df.columns:
                    df[db_col] = ""

            check_cols = [c for c in ["ps", "area", "descrizione"] if c in df.columns]
            if check_cols:
                df.dropna(how="all", subset=check_cols, inplace=True)

            df = df.fillna("")
            df = df.astype(str)
            df = df.apply(lambda x: x.str.strip())

            df["styles"] = ""

            db_cols = list(cls.ATTIVITA_PROGRAMMATE_MAPPING.values()) + ["styles"]

            for c in db_cols:
                if c not in df.columns:
                    df[c] = ""

            df = df[db_cols]

            rows_to_insert = list(df.itertuples(index=False, name=None))

            return (
                True,
                f"Importate {len(rows_to_insert)} righe in Attività Programmate.",
                rows_to_insert,
            )

        except Exception as e:
            return False, f"Errore importazione Attività Programmate: {e}", []

    @classmethod
    def import_scarico_ore(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        """Importa il file Scarico Ore Cantiere (OpenPyXL per colori + Diff Logic) e restituisce le righe."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Scarico Ore non trovato: {file_path}", []

        if not openpyxl:
            return False, "Modulo 'openpyxl' mancante.", []

        try:
            wb_file = io.BytesIO()
            is_encrypted = False

            if msoffcrypto:
                try:
                    with open(path, "rb") as f:
                        office_file = msoffcrypto.OfficeFile(f)
                        office_file.load_key(password="coemi")
                        office_file.decrypt(wb_file)
                        is_encrypted = True
                except Exception:
                    pass

            if not is_encrypted:
                with open(path, "rb") as f:
                    wb_file.write(f.read())

            wb_file.seek(0)

            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore", category=UserWarning, module="openpyxl"
                )
                wb_data = openpyxl.load_workbook(
                    wb_file, data_only=True, read_only=False
                )

            if "SCARICO ORE" not in wb_data.sheetnames:
                return False, "Foglio 'SCARICO ORE' non trovato.", []
            ws_data = wb_data["SCARICO ORE"]

            rows_to_insert = []
            start_row = 6
            col_keys = [
                "data",
                "pers1",
                "pers2",
                "odc",
                "pos",
                "dalle",
                "alle",
                "totale_ore",
                "descrizione",
                "finito",
                "commessa",
            ]

            total_rows = ws_data.max_row

            for row_idx, row in enumerate(
                ws_data.iter_rows(min_row=start_row, min_col=2, max_col=12),
                start=start_row,
            ):
                if progress_callback and row_idx % 200 == 0:
                    progress_callback(row_idx, total_rows)

                db_row = cls._process_scarico_ore_row(row, col_keys)
                if db_row:
                    rows_to_insert.append(db_row)

            return (
                True,
                f"Importate {len(rows_to_insert)} righe da Scarico Ore.",
                rows_to_insert,
            )

        except Exception as e:
            return False, f"Errore importazione Scarico Ore: {e}", []

    @classmethod
    def _process_scarico_ore_row(cls, row, col_keys) -> Optional[Tuple]:
        """Helper to process a single row from Scarico Ore."""
        subset_vals = [c.value for i, c in enumerate(row) if i <= 7]
        if all(v is None or str(v).strip() == "" for v in subset_vals):
            return None

        row_vals = {}
        row_styles = {}

        for i, key in enumerate(col_keys):
            cell = row[i]
            val = cell.value

            if key in ["odc", "pos"]:
                if val == 0 or str(val).strip() in ["0", "0.0"]:
                    val = ""
            elif key == "commessa":
                if val == 0:
                    val = "0"

            val_str = str(val).strip() if val is not None else ""
            val_str = val_str.replace("\n", " ")
            row_vals[key] = val_str

            fg_color = None
            bg_color = None

            if cell.font and cell.font.color:
                if cell.font.color.type == "rgb":
                    c = str(cell.font.color.rgb)
                    if len(c) > 6:
                        c = "#" + c[2:]
                    else:
                        c = "#" + c
                    fg_color = c

            if cell.fill and cell.fill.patternType == "solid":
                if cell.fill.start_color:
                    if cell.fill.start_color.type == "rgb":
                        c = str(cell.fill.start_color.rgb)
                        if len(c) > 6:
                            c = "#" + c[2:]
                        else:
                            c = "#" + c
                        bg_color = c

            if fg_color or bg_color:
                style_entry = {}
                if fg_color:
                    style_entry["fg"] = fg_color
                if bg_color:
                    style_entry["bg"] = bg_color
                row_styles[key] = style_entry

        check_all_empty = [
            "pers1",
            "pers2",
            "odc",
            "pos",
            "dalle",
            "alle",
            "totale_ore",
        ]
        if all(row_vals.get(k, "") == "" for k in check_all_empty):
            return None

        if (
            not row_vals.get("odc")
            or not row_vals.get("pos")
            or not row_vals.get("totale_ore")
        ):
            return None

        if not row_vals.get("pers1") and not row_vals.get("pers2"):
            return None

        return (
            row_vals["data"],
            row_vals["pers1"],
            row_vals["pers2"],
            row_vals["odc"],
            row_vals["pos"],
            row_vals["dalle"],
            row_vals["alle"],
            row_vals["totale_ore"],
            row_vals["descrizione"],
            row_vals["finito"],
            row_vals["commessa"],
            json.dumps(row_styles) if row_styles else "",
        )

    @classmethod
    def import_certificati_campione(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        """Importa il file Certificati Campione e restituisce le righe."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Certificati Campione non trovato: {file_path}", []

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                try:
                    xls = pd.ExcelFile(path)
                    sheet_name = None

                    for name_raw in xls.sheet_names:
                        name = str(name_raw)
                        name_lower = name.lower()
                        if (
                            "strumenti campione" in name_lower
                            or "isab sud" in name_lower
                        ):
                            sheet_name = name
                            break

                    if not sheet_name and xls.sheet_names:
                        sheet_name = str(xls.sheet_names[0])

                    if not sheet_name:
                        return False, "Nessun foglio trovato nel file Excel.", []

                except Exception as e:
                    return False, f"Errore apertura file Excel: {e}", []

                try:
                    df_preview = pd.read_excel(
                        path, sheet_name=sheet_name, header=None, nrows=20
                    )
                    header_row_idx = cls._detect_certificati_header(df_preview)

                    df = pd.read_excel(
                        path, sheet_name=sheet_name, header=header_row_idx
                    )

                except Exception as e:
                    return (
                        False,
                        f"Errore lettura file Certificati (sheet: {sheet_name}): {e}",
                        [],
                    )

                if df.empty:
                    return False, "Foglio vuoto.", []

                return cls._process_certificati_df(df, sheet_name, header_row_idx)

        except Exception as e:
            return False, f"Errore importazione Certificati Campione: {e}", []

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

        rename_map = {}
        for excel_col, db_col in cls.CERTIFICATI_CAMPIONE_MAPPING.items():
            if excel_col in df.columns:
                rename_map[excel_col] = db_col

        if not rename_map:
            found_cols = ", ".join(list(df.columns)[:5]) + "..."
            return (
                False,
                f"Nessuna colonna valida trovata. Sheet: {sheet_name}, Row: {header_row_idx}. Trovate: {found_cols}",
                [],
            )

        df.rename(columns=rename_map, inplace=True)

        target_cols = list(cls.CERTIFICATI_CAMPIONE_MAPPING.values())
        for c in target_cols:
            if c not in df.columns:
                df[c] = ""

        df = df[target_cols]
        df.dropna(how="all", inplace=True)

        def format_date_it(val):
            if pd.isna(val) or val == "":
                return ""
            try:
                dt = pd.to_datetime(val)
                return dt.strftime("%d/%m/%Y")
            except Exception:
                return str(val)

        df["scadenza"] = df["scadenza"].apply(format_date_it)
        df["emissione"] = df["emissione"].apply(format_date_it)

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
                else:
                    return "Scade oggi"
            except ValueError:
                return str(val)

        if "stato" in df.columns:
            df["stato"] = df["stato"].apply(format_stato)

        df = df.fillna("")
        df = df.astype(str)
        df = df.apply(lambda x: x.str.strip())

        rows = list(df.itertuples(index=False, name=None))

        return (
            True,
            f"Importate {len(rows)} righe in Certificati Campione.",
            rows,
        )

    @classmethod
    def scan_scarico_ore_rows(cls, file_path: str) -> int:
        """Stima rapida delle righe per Scarico Ore (DataEase) per calcolo ETA."""
        path = Path(file_path)
        if not path.exists():
            return 0

        try:
            with zipfile.ZipFile(path, "r") as z:
                max_rows = 0
                for name in z.namelist():
                    if name.startswith("xl/worksheets/sheet"):
                        with z.open(name) as f:
                            head = f.read(1024).decode("utf-8", errors="ignore")
                            match = re.search(
                                r'<dimension ref="[A-Z]+[0-9]+:[A-Z]+(\d+)"', head
                            )
                            if match:
                                r = int(match.group(1))
                                if r > max_rows:
                                    max_rows = r
                return max_rows
        except Exception:
            return 0

    @classmethod
    def scan_workload(cls, file_path: str, giornaliere_path: str) -> Tuple[int, int]:
        """Scansiona rapidamente il carico di lavoro (fogli e file) per stima ETA."""
        sheets = 0
        files = 0

        p_file = Path(file_path)
        if file_path and p_file.exists():
            try:
                with zipfile.ZipFile(p_file, "r") as z:
                    if "xl/workbook.xml" in z.namelist():
                        wb_xml = z.read("xl/workbook.xml").decode("utf-8")
                        sheet_names = re.findall(r'name="([^"]+)"', wb_xml)
                        sheets = len(
                            [s for s in sheet_names if re.search(r"(\d{4})", s)]
                        )
            except Exception:
                sheets = 1

        p_giorn = Path(giornaliere_path)
        if giornaliere_path and p_giorn.exists():
            current_year = datetime.now().year
            for folder in p_giorn.iterdir():
                if folder.is_dir():
                    match = re.match(
                        r"Giornaliere\s+(\d{4})", folder.name, re.IGNORECASE
                    )
                    if match:
                        year = int(match.group(1))
                        if year >= current_year:
                            files += len(
                                [
                                    f
                                    for f in folder.glob("*.xls*")
                                    if not f.name.startswith("~$")
                                ]
                            )

        return sheets, files
