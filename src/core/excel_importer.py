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

    # Mapping Storico OdA
    STORICO_ODA_MAPPING = {
        "Org. Acq.": "org_acq",
        "Data OdA": "data_oda",
        "OdA": "oda",
        "Pos OdA": "pos_oda",
        "Stato": "stato",
        "Cat. Contab.": "cat_contab",
        "Descrizione": "descrizione",
        "Qta": "qta",
        "UOM": "uom",
        "Data Consegna": "data_consegna",
        "Valore Netto Pos. ODA": "valore_netto_pos",
        "Valore Residuo ODA": "valore_residuo",
        "Valore Netto ODA": "valore_netto_oda",
        "Divisione": "divisione",
        "Destinatario": "destinatario",
        "Nome Destinatario": "nome_destinatario",
        "Codice Fornitore": "codice_fornitore",
        "Descrizione Fornitore": "descrizione_fornitore",
        "Emittente Fattura": "emittente_fattura",
        "Descrizione Emittente Fattura": "desc_emittente_fattura",
        "Contract Card": "contract_card",
        "Contratto": "contratto",
        "Posizione Contratto": "posizione_contratto",
        "Gruppo Acquisti": "gruppo_acquisti",
        "Indicatore Rilascio": "indicatore_rilascio",
        "Stato Rilascio": "stato_rilascio",
        "Attività": "attivita",  # Matches Attivit via robust check
        "Num riga": "num_riga",
        "Quantità": "quantita",  # Matches Quantit
        "Unità di Mis": "unita_mis",  # Matches Unit di Mis
        "Prezzo lordo": "prezzo_lordo",
        "Testo breve": "testo_breve",
    }

    STORICO_ODA_COLS = list(STORICO_ODA_MAPPING.values())

    @staticmethod
    def _decrypt_if_encrypted(file_path: Path) -> Tuple[Any, bool]:
        """Tenta di decifrare un file Excel se protetto da password."""
        if msoffcrypto:
            try:
                from src.core import config_manager

                config = config_manager.load_config()
                # Recupera password da config, default "coemi"
                pwd = config.get("excel_decryption_password", "coemi")

                with open(file_path, "rb") as f:
                    office_file = msoffcrypto.OfficeFile(f)
                    office_file.load_key(password=pwd)
                    temp_decrypted = io.BytesIO()
                    office_file.decrypt(temp_decrypted)
                    temp_decrypted.seek(0)
                    return temp_decrypted, True
            except Exception:
                # Non cifrato o errore msoffcrypto, procediamo col file originale
                pass
        return file_path, False

    @classmethod
    def _get_excel_file(cls, file_obj) -> pd.ExcelFile:
        """Tenta di aprire il file Excel con pandas o openpyxl."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                return pd.ExcelFile(file_obj)
            except Exception:
                return pd.ExcelFile(file_obj, engine="openpyxl")

    @classmethod
    def _identify_sheet_year(cls, sheet_name: str) -> Optional[int]:
        """Estrae l'anno dal nome del foglio o usa l'anno corrente per nomi specifici."""
        match = re.search(r"(\d{4})", sheet_name)
        if match:
            year = int(match.group(1))
            return year if 2000 <= year <= 2100 else None

        if sheet_name.lower() in ["dati", "preventivi", "riepilogo"]:
            return datetime.now().year
        return None

    @classmethod
    def _find_header_row(cls, xls, sheet_name) -> int:
        """Cerca l'indice della riga di intestazione basandosi su colonne chiave."""
        preview_df = pd.read_excel(xls, sheet_name=sheet_name, header=None, nrows=15)
        key_cols_norm = ["DATAPREV", "MESE", "NPREV", "TOTALEPREV", "ATTIVITA", "ODC"]

        for i_raw, row in preview_df.iterrows():
            row_norm = []
            for val in row.values:
                s = str(val).strip().upper()
                s = s.replace(" ", "").replace(".", "").replace("°", "")
                row_norm.append(s)

            matches = sum(1 for k in key_cols_norm if k in row_norm)
            if matches >= 2:
                # Debug print removed, return the index
                return int(i_raw)
        return 0  # Fallback to first row

    @classmethod
    def _normalize_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Rinomina le colonne del DataFrame usando la mappa interna."""
        normalized_map = {}
        for k, v in cls.COLUMNS_MAPPING.items():
            norm_k = k.upper().replace(" ", "").replace(".", "").replace("°", "")
            normalized_map[norm_k] = v

        rename_map = {}
        for col in df.columns:
            col_str = str(col).strip().upper()
            norm_col = col_str.replace(" ", "").replace(".", "").replace("°", "")

            if norm_col in normalized_map:
                rename_map[col] = normalized_map[norm_col]
            else:
                # Euristiche extra
                if "PREV" in norm_col and "DATA" in norm_col:
                    rename_map[col] = "data_prev"
                elif "PREV" in norm_col and ("N" in norm_col or "NUM" in norm_col):
                    rename_map[col] = "n_prev"

        df.rename(columns=rename_map, inplace=True)
        return df

    @classmethod
    def import_contabilita_dati(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, list, list]:
        """
        Importa i dati dal file Excel specificato (Tabella Dati).
        """
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", [], []

        try:
            file_obj, _ = cls._decrypt_if_encrypted(path)
            xls = cls._get_excel_file(file_obj)

            valid_sheets = [
                str(s) for s in xls.sheet_names if cls._identify_sheet_year(str(s))
            ]
            if not valid_sheets:
                return (
                    False,
                    "Nessun anno importato (Controlla nomi fogli: YYYY o 'Dati/Preventivi').",
                    [],
                    [],
                )

            all_rows, imported_years = cls._process_all_sheets(
                xls, valid_sheets, progress_callback
            )

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
            logging.error(f"Errore importazione Excel: {e}")
            return False, f"Errore critico importazione: {e}", [], []

    @classmethod
    def _process_all_sheets(
        cls, xls, sheet_names: List[str], progress_callback: Optional[Callable]
    ) -> Tuple[List[Tuple], List[int]]:
        """Cicla sui fogli e aggrega i risultati."""
        all_rows = []
        imported_years = []
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
    def _process_single_sheet(cls, xls, sheet_name: str, year: int) -> List[Tuple]:
        """Processa un singolo foglio del file Excel di contabilità."""
        try:
            header_row_idx = cls._find_header_row(xls, sheet_name)
            df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_idx)
            df.columns = [str(c).strip().upper() for c in df.columns]

            if not df.empty:
                df = df.iloc[:-1]  # Rimuovi riga dei totali solitamente presente
            df.dropna(how="all", inplace=True)

            if df.empty:
                return []

            df["year"] = year
            df = cls._normalize_columns(df)
            df = cls._ensure_required_columns(df)

            # Preparazione finale dati
            target_columns = ["year"] + list(cls.COLUMNS_MAPPING.values())
            df = df[target_columns].copy()

            # --- Gestione Tipi Intelligente ---
            for col in df.columns:
                if col == "year":
                    continue

                # 1. Tenta conversione numerica per colonne che dovrebbero essere numeri
                if col in ["totale_prev", "ore_sp", "resa"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    # Arrotonda a 2 decimali per eliminare rumore (es. .00000000001)
                    df[col] = df[col].round(2)

                # 2. Gestione Date
                elif col == "data_prev":
                    df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime(
                        "%Y-%m-%d"
                    )

                # 3. Pulizia stringhe per il resto
                else:
                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.strip()
                        .replace(r"(?i)^nan$", "", regex=True)
                    )

            # Riempie i NaN rimasti con valori sicuri per il DB
            df = df.fillna("")

            return list(df.itertuples(index=False, name=None))
        except Exception as e:
            logging.warning(f"Errore processamento foglio {sheet_name}: {e}")
            return []

    @classmethod
    def _ensure_required_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Assicura che tutte le colonne mappate esistano nel DataFrame."""
        for db_col in cls.COLUMNS_MAPPING.values():
            if db_col not in df.columns:
                df[db_col] = ""
        return df

    @classmethod
    def _process_single_giornaliera(
        cls, args: Tuple[int, Path, Dict]
    ) -> Tuple[int, List[Tuple], Optional[str]]:
        """Helper per processare un singolo file giornaliera in parallelo."""
        year, file_path, lookup_map = args
        try:
            # Decrittografia se necessaria
            file_obj, _ = cls._decrypt_if_encrypted(file_path)
            df = cls._read_giornaliera_sheet(file_obj)
            if df is None:
                return (year, [], None)

            # Normalizzazione Colonne
            df = cls._normalize_giornaliera_columns(df)
            if df is None:
                return (year, [], None)

            # Pulizia Base
            df = cls._clean_giornaliera_data(df)
            if df.empty:
                return (year, [], None)

            # Logica di Business: Arricchimento ODC
            cls._enrich_giornaliera_odc(df, lookup_map)

            # Preparazione finale
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
    def _read_giornaliera_sheet(cls, file_path: Path) -> Optional[pd.DataFrame]:
        """Legge il foglio RIASSUNTO gestendo i motori pandas."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                return pd.read_excel(file_path, sheet_name="RIASSUNTO")
            except ValueError:
                return None
            except zipfile.BadZipFile:
                # File non valido o corrotto
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
        """Applica il mapping delle colonne specifico per le giornaliere."""
        df.columns = [str(c).strip() for c in df.columns]
        rename_map = {}
        for excel_col, db_col in cls.GIORNALIERE_MAPPING.items():
            for c in df.columns:
                if c.upper() == excel_col.upper():
                    rename_map[c] = db_col
                    break

        if not rename_map:
            return None

        df.rename(columns=rename_map, inplace=True)
        return df

    @classmethod
    def _clean_giornaliera_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Esegue pulizia righe, totali e nan."""
        if df.empty:
            return df

        df = df.iloc[:-1]  # Rimuovi riga totali
        if "personale" in df.columns:
            df = df[~df["personale"].str.contains("Totale", na=False, case=False)]

        # Drop righe completamente vuote nelle colonne chiave
        check_cols = [
            c
            for c in df.columns
            if c in cls.GIORNALIERE_MAPPING.values() and c != "data"
        ]
        if check_cols:
            df.dropna(how="all", subset=check_cols, inplace=True)

        if df.empty:
            return df

        # Assicura colonne esistenti e pulisci stringhe
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
        df[cols_to_clean] = df[cols_to_clean].astype(str).apply(lambda x: x.str.strip())
        df[cols_to_clean] = df[cols_to_clean].replace(r"(?i)^nan$", "", regex=True)
        return df

    @classmethod
    def _enrich_giornaliera_odc(cls, df: pd.DataFrame, lookup_map: Dict):
        """Estrae o associa l'ODC mancante da varie fonti."""
        # 1. Da Lookup Map (n_prev -> odc)
        mask_empty = df["odc"] == ""
        if mask_empty.any() and lookup_map:
            mapped = df.loc[mask_empty, "n_prev"].map(lookup_map)
            df.loc[mask_empty, "odc"] = mapped.fillna("")

        # 2. Da Descrizione (Pattern XX/XXX)
        mask_empty = df["odc"] == ""
        if mask_empty.any():
            comm_pattern = r"\b(\d{2}/\d{3})\b"
            extracted = df.loc[mask_empty, "descrizione"].str.extract(
                comm_pattern, expand=False
            )
            df.loc[mask_empty, "odc"] = extracted.fillna("")

        # 3. Normalizzazione standard 5400...
        mask_standard = ~df["odc"].str.contains("canone", case=False, na=False) & ~df[
            "odc"
        ].str.match(r"^\d{2}/\d{3}$", na=False)
        if mask_standard.any():
            extracted = df.loc[mask_standard, "odc"].str.extract(
                r"(5400\d+)", expand=False
            )
            df.loc[mask_standard, "odc"] = extracted.fillna("")

    @classmethod
    def import_giornaliere(
        cls,
        root_path: str,
        lookup_map: Dict,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple], List[int]]:
        """
        Importa i dati dalle cartelle Giornaliere, processa i file in parallelo.
        """
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
        """Scansiona le cartelle e crea la lista dei file da processare."""
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
        """Esegue il processamento parallelo tramite ProcessPoolExecutor."""
        all_rows = []
        years_encountered = set()
        total_tasks = len(tasks)
        processed_count = 0

        # Limit max_workers to avoid memory spikes
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
    def import_attivita_programmate(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        """Importa il file Attività Programmate (veloce, senza colori)."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Attività Programmate non trovato: {file_path}", []

        try:
            df = cls._read_attivita_programmate_sheet(path)
            if df is None:
                return False, "Foglio 'Riepilogo' non trovato o file illeggibile.", []

            # Normalizzazione Colonne
            df = cls._normalize_attivita_columns(df)
            if df is None:
                return False, "Colonne non trovate. Controlla intestazione riga 3.", []

            # Pulizia e Preparazione
            rows = cls._prepare_attivita_rows(df)
            return True, f"Importate {len(rows)} righe in Attività Programmate.", rows

        except Exception as e:
            return False, f"Errore importazione Attività Programmate: {e}", []

    @classmethod
    def _read_attivita_programmate_sheet(cls, path: Path) -> Optional[pd.DataFrame]:
        """Tenta di leggere il foglio 'Riepilogo'."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                return pd.read_excel(path, sheet_name="Riepilogo", header=2)
            except (ValueError, Exception):
                try:
                    return pd.read_excel(
                        path, sheet_name="Riepilogo", header=2, engine="openpyxl"
                    )
                except Exception:
                    return None

    @classmethod
    def _normalize_attivita_columns(cls, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Applica il mapping delle colonne e l'euristica per i newline."""
        df.columns = [str(c).strip() for c in df.columns]
        rename_map = {}

        for excel_col, db_col in cls.ATTIVITA_PROGRAMMATE_MAPPING.items():
            if excel_col in df.columns:
                rename_map[excel_col] = db_col
            else:
                # Euristiche per newline (es. "STATO\nPdL" -> "STATO PdL")
                for col in df.columns:
                    if (
                        excel_col.replace("\n", " ").strip()
                        == col.replace("\n", " ").strip()
                    ):
                        rename_map[col] = db_col
                        break

        if not rename_map:
            return None

        df.rename(columns=rename_map, inplace=True)
        return df

    @classmethod
    def _prepare_attivita_rows(cls, df: pd.DataFrame) -> List[Tuple]:
        """Pulisce i dati e restituisce le tuple per il database."""
        # 1. Assicura colonne esistenti
        for db_col in cls.ATTIVITA_PROGRAMMATE_MAPPING.values():
            if db_col not in df.columns:
                df[db_col] = ""

        # 2. Drop righe vuote
        check_cols = [c for c in ["ps", "area", "descrizione"] if c in df.columns]
        if check_cols:
            df.dropna(how="all", subset=check_cols, inplace=True)

        # 3. Formattazione stringhe
        df = df.fillna("").astype(str).apply(lambda x: x.str.strip())
        df["styles"] = ""

        # 4. Selezione colonne finale
        db_cols = list(cls.ATTIVITA_PROGRAMMATE_MAPPING.values()) + ["styles"]
        df = df[db_cols]

        return list(df.itertuples(index=False, name=None))

    @classmethod
    def import_scarico_ore(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        """Importa il file Scarico Ore Cantiere (OpenPyXL per colori + Diff Logic)."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Scarico Ore non trovato: {file_path}", []

        if not openpyxl:
            return False, "Modulo 'openpyxl' mancante.", []

        try:
            wb_data = cls._load_scarico_workbook(path)
            if "SCARICO ORE" not in wb_data.sheetnames:
                return False, "Foglio 'SCARICO ORE' non trovato.", []

            ws_data = wb_data["SCARICO ORE"]
            rows = cls._process_all_scarico_rows(ws_data, progress_callback)

            return True, f"Importate {len(rows)} righe da Scarico Ore.", rows

        except Exception as e:
            return False, f"Errore importazione Scarico Ore: {e}", []

    @classmethod
    def _load_scarico_workbook(cls, path: Path) -> Any:
        """Carica il workbook gestendo l'eventuale crittografia."""
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
            warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
            return openpyxl.load_workbook(wb_file, data_only=True, read_only=False)

    @classmethod
    def _process_all_scarico_rows(
        cls, ws, progress_callback: Optional[Callable]
    ) -> List[Tuple]:
        """Cicla sulle righe del foglio scarico ore."""
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
        total_rows = ws.max_row

        for row_idx, row in enumerate(
            ws.iter_rows(min_row=start_row, min_col=2, max_col=12), start=start_row
        ):
            if progress_callback and row_idx % 200 == 0:
                progress_callback(row_idx, total_rows)

            db_row = cls._process_scarico_ore_row(row, col_keys)
            if db_row:
                rows_to_insert.append(db_row)

        return rows_to_insert

    @classmethod
    def _process_scarico_ore_row(cls, row, col_keys) -> Optional[Tuple]:
        """Processa una singola riga estraendo valori e stili."""
        # Check preliminare: riga vuota?
        if all(
            c.value is None or str(c.value).strip() == ""
            for i, c in enumerate(row)
            if i <= 7
        ):
            return None

        row_vals = {}
        row_styles = {}

        for i, key in enumerate(col_keys):
            cell = row[i]
            val = cls._format_scarico_cell_value(key, cell.value)
            row_vals[key] = val

            # Estrazione stili (colori)
            style = cls._get_cell_style(cell)
            if style:
                row_styles[key] = style

        if not cls._is_scarico_row_valid(row_vals):
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

    @staticmethod
    def _format_scarico_cell_value(key: str, val: Any) -> str:
        """Formatta il valore della cella in base al tipo di colonna."""
        if key in ["odc", "pos"]:
            if val == 0 or str(val).strip() in ["0", "0.0"]:
                return ""
        elif key == "commessa":
            if val == 0:
                return "0"

        val_str = str(val).strip() if val is not None else ""
        return val_str.replace("\n", " ")

    @staticmethod
    def _get_cell_style(cell: Any) -> Optional[Dict[str, str]]:
        """Estrae i colori (HEX) dalla cella."""
        style = {}

        # Foreground
        if fg := ExcelImporter._extract_rgb_color(
            cell.font.color if cell.font else None
        ):
            style["fg"] = fg

        # Background
        if cell.fill and cell.fill.patternType == "solid":
            if bg := ExcelImporter._extract_rgb_color(cell.fill.start_color):
                style["bg"] = bg

        return style if style else None

    @staticmethod
    def _extract_rgb_color(color_obj: Any) -> Optional[str]:
        """Estrae il codice HEX da un oggetto colore OpenPyXL."""
        if color_obj and color_obj.type == "rgb":
            rgb = str(color_obj.rgb)
            return f"#{rgb[2:]}" if len(rgb) > 6 else f"#{rgb}"
        return None

    @classmethod
    def _is_scarico_row_valid(cls, row_vals: Dict[str, str]) -> bool:
        """Verifica se la riga ha i dati minimi necessari per l'importazione."""
        # 1. Almeno uno tra i campi tecnici deve essere presente
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
            return False

        # 2. Campi obbligatori core
        if (
            not row_vals.get("odc")
            or not row_vals.get("pos")
            or not row_vals.get("totale_ore")
        ):
            return False

        # 3. Almeno un operatore
        if not row_vals.get("pers1") and not row_vals.get("pers2"):
            return False

        return True

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
    def import_storico_oda(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        """Importa il file Storico OdA."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", []

        try:
            # 1. Lettura Excel
            df = cls._read_storico_oda_excel(path)
            if df.empty:
                return False, "Foglio vuoto.", []

            # 2. Mappatura Colonne
            rename_map = cls._map_storico_oda_columns(df)
            if not rename_map:
                return False, "Nessuna colonna riconosciuta.", []

            df.rename(columns=rename_map, inplace=True)
            df = df.loc[:, ~df.columns.duplicated()]

            # 3. Normalizzazione e Pulizia
            cls._normalize_storico_oda_df(df)
            cls._clean_storico_oda_data(df)

            # 4. Conversione in tuple
            data = [tuple(x) for x in df.to_numpy()]
            return True, f"Trovate {len(data)} righe.", data

        except Exception as e:
            return False, f"Errore importazione Storico OdA: {e}", []

    @classmethod
    def _read_storico_oda_excel(cls, path: Path) -> pd.DataFrame:
        """Legge il file excel tentando diversi fogli."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                return pd.read_excel(path, sheet_name="Formato PF")
            except ValueError:
                return pd.read_excel(path, sheet_name=0)

    @classmethod
    def _map_storico_oda_columns(cls, df: pd.DataFrame) -> dict:
        """Mappa le colonne dell'Excel a quelle del DB."""
        df.columns = [str(c).strip() for c in df.columns]
        rename_map = {}
        for excel_col, db_col in cls.STORICO_ODA_MAPPING.items():
            for col in df.columns:
                if excel_col == col:
                    rename_map[col] = db_col
                    break
                # Fallback matching
                if len(excel_col) >= 4 and col.startswith(excel_col[:4]):
                    if excel_col.startswith("Unit") and col.startswith("Unit"):
                        rename_map[col] = db_col
                        break
                    if abs(len(col) - len(excel_col)) <= 2:
                        rename_map[col] = db_col
                        break
        return rename_map

    @classmethod
    def _normalize_storico_oda_df(cls, df: pd.DataFrame):
        """Assicura che tutte le colonne richieste esistano e filtra solo quelle del DB."""
        for db_col in cls.STORICO_ODA_COLS:
            if db_col not in df.columns:
                df[db_col] = ""

        # Filtra solo le colonne del DB (in-place modification via drop)
        cols_to_drop = [c for c in df.columns if c not in cls.STORICO_ODA_COLS]
        if cols_to_drop:
            df.drop(columns=cols_to_drop, inplace=True)

    @classmethod
    def _clean_storico_oda_data(cls, df: pd.DataFrame):
        """Pulisce date, numeri e ID."""
        # Date
        for date_col in ["data_oda", "data_consegna"]:
            df[date_col] = (
                pd.to_datetime(df[date_col], errors="coerce")
                .dt.strftime("%Y-%m-%d")
                .fillna("")
            )

        # Numeri
        num_cols = [
            "qta",
            "valore_netto_pos",
            "valore_residuo",
            "valore_netto_oda",
            "quantita",
            "prezzo_lordo",
        ]
        for num_col in num_cols:
            df[num_col] = df[num_col].apply(cls._clean_euro_num)

        # IDs
        id_cols = [
            "oda",
            "pos_oda",
            "num_riga",
            "divisione",
            "destinatario",
            "contratto",
            "posizione_contratto",
        ]
        for str_col in id_cols:
            df[str_col] = (
                df[str_col]
                .fillna(0)
                .astype(str)
                .str.replace(r"\\.0$", "", regex=True)
                .str.strip()
            )

        # Altre stringhe
        for col in df.columns:
            if col not in num_cols + ["data_oda", "data_consegna"] + id_cols:
                df[col] = df[col].fillna("").astype(str).str.strip()

    @staticmethod
    def _clean_euro_num(x):
        """Helper for European numbers (1.234,56 -> 1234.56)."""
        if pd.isna(x) or str(x).strip() == "":
            return 0.0
        if isinstance(x, (int, float)):
            return float(x)
        s = str(x).strip()
        if "." in s and "," in s:
            s = s.replace(".", "").replace(",", ".")
        elif "," in s:
            s = s.replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return 0.0

    @classmethod
    def _find_certificati_sheet(cls, xls: pd.ExcelFile) -> Optional[str]:
        """Trova il foglio corretto per i certificati."""
        for name in xls.sheet_names:
            n_low = str(name).lower()
            if "strumenti campione" in n_low or "isab sud" in n_low:
                return str(name)
        return str(xls.sheet_names[0]) if xls.sheet_names else None

    @classmethod
    def _read_certificati_data(
        cls, path: Path, sheet_name: str
    ) -> Tuple[pd.DataFrame, int]:
        """Legge i dati individuando l'intestazione."""
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
        """Crea la mappa di ridenominazione colonne."""
        rename_map = {}
        for excel_col, db_col in cls.CERTIFICATI_CAMPIONE_MAPPING.items():
            if excel_col in columns:
                rename_map[excel_col] = db_col
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
        sheets = cls._scan_excel_sheets(file_path)
        files = cls._scan_giornaliere_files(giornaliere_path)
        return sheets, files

    @classmethod
    def _scan_excel_sheets(cls, file_path: str) -> int:
        """Conta i fogli validi nell'Excel principale."""
        p_file = Path(file_path)
        if not file_path or not p_file.exists():
            return 0
        try:
            # Check if valid zip before opening
            if not zipfile.is_zipfile(p_file):
                # Maybe old xls format (OLE)
                return 1

            with zipfile.ZipFile(p_file, "r") as z:
                if "xl/workbook.xml" not in z.namelist():
                    return 1
                wb_xml = z.read("xl/workbook.xml").decode("utf-8")
                sheet_names = re.findall(r'name="([^"]+)"', wb_xml)
                return len([s for s in sheet_names if re.search(r"(\d{4})", s)])
        except Exception as e:
            logging.debug(f"Scan excel sheets error: {e}")
            return 1

    @classmethod
    def _scan_giornaliere_files(cls, giornaliere_path: str) -> int:
        """Conta i file validi nelle cartelle giornaliere."""
        p_giorn = Path(giornaliere_path)
        if not giornaliere_path or not p_giorn.exists():
            return 0

        count = 0
        current_year = datetime.now().year
        for folder in p_giorn.iterdir():
            if not folder.is_dir():
                continue
            match = re.match(r"Giornaliere\s+(\d{4})", folder.name, re.IGNORECASE)
            if not match:
                continue

            year = int(match.group(1))
            if year < current_year:
                continue

            for file_path in folder.glob("*.xls*"):
                if not file_path.name.startswith("~$"):
                    count += 1
        return count
