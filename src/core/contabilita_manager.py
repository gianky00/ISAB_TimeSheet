"""
Bot TS - Contabilita Manager
Gestione dell'importazione e archiviazione dati della Contabilità Strumentale.
"""
import sqlite3
import pandas as pd
from pathlib import Path
import re
import logging
import warnings
import io
import json
import zipfile
from typing import List, Dict, Tuple, Optional, Callable
from datetime import datetime
from src.utils.parsing import parse_currency
from src.core.config_manager import CONFIG_DIR
from src.core.database import db_manager

# Tentativo di importare msoffcrypto
try:
    import msoffcrypto
except ImportError:
    msoffcrypto = None

# Tentativo di importare openpyxl
try:
    import openpyxl
    from openpyxl.utils import get_column_letter
except ImportError:
    openpyxl = None

class ContabilitaManager:
    """Manager per la gestione del database e dell'importazione Excel."""

    DB_PATH = CONFIG_DIR / "data" / "contabilita.db"

    # Mapping colonne Excel -> DB (Contabilità / Dati)
    COLUMNS_MAPPING = {
        'DATA PREV.': 'data_prev',
        'MESE': 'mese',
        'N°PREV.': 'n_prev',
        'TOTALE PREV.': 'totale_prev',
        "ATTIVITA'": 'attivita',
        'TCL': 'tcl',
        'ODC': 'odc',
        "STATO ATTIVITA'": 'stato_attivita',
        'TIPOLOGIA': 'tipologia',
        'ORE SP': 'ore_sp',
        'RESA': 'resa',
        'ANNOTAZIONI': 'annotazioni',
        'INDIRIZZO CONSUNTIVO': 'indirizzo_consuntivo',
        'NOME FILE': 'nome_file'
    }

    # Mapping colonne Excel -> DB (Giornaliere)
    GIORNALIERE_MAPPING = {
        'DATA': 'data',
        'PERSONALE': 'personale',
        "DESCRIZIONE ATTIVITA'": 'descrizione',
        'TCL': 'tcl',
        'ODC': 'odc',
        'N° PDL': 'pdl',
        'INIZIO': 'inizio',
        'FINE': 'fine',
        'ORE': 'ore',
        'consuntivo': 'n_prev' # Rinominato come richiesto
    }

    # Mapping Scarico Ore Cantiere
    SCARICO_ORE_COLS = [
        'data', 'pers1', 'pers2', 'odc', 'pos', 'dalle', 'alle',
        'totale_ore', 'descrizione', 'finito', 'commessa', 'styles'
    ]

    # Mapping Attività Programmate
    # Header: PS, AREA, PdL, IMP., DESCRIZIONE ATTIVITA', LUN, MAR, MER, GIO, VEN, STATO PdL, STATO ATTIVITA', DATA CONTROLLO, PERSONALE IMPIEGATO, PO, AVVISO
    ATTIVITA_PROGRAMMATE_MAPPING = {
        'PS': 'ps',
        'AREA': 'area',
        'PdL': 'pdl',
        'IMP.': 'imp',
        "DESCRIZIONE\nATTIVITA'": 'descrizione',
        'LUN': 'lun',
        'MAR': 'mar',
        'MER': 'mer',
        'GIO': 'gio',
        'VEN': 'ven',
        "STATO\nPdL": 'stato_pdl',
        "STATO\nATTIVITA'": 'stato_attivita',
        "DATA\nCONTROLLO": 'data_controllo',
        "PERSONALE\nIMPIEGATO": 'personale',
        'PO': 'po',
        'AVVISO': 'avviso'
    }

    ATTIVITA_PROGRAMMATE_COLS = list(ATTIVITA_PROGRAMMATE_MAPPING.values()) + ['styles'] # Added styles

    # Mapping Certificati Campione
    CERTIFICATI_CAMPIONE_MAPPING = {
        'Modello / Tipo': 'modello',
        'Costruttore': 'costruttore',
        'Matricola': 'matricola',
        'Range Strumento': 'range_strumento',
        'Errore max %': 'errore_max',
        'Certificato Taratura': 'certificato',
        'Scadenza Certificato': 'scadenza',
        'Emissione Certificato': 'emissione',
        'ID-COEMI': 'id_coemi',
        'Stato Certificato': 'stato'
    }

    CERTIFICATI_CAMPIONE_COLS = list(CERTIFICATI_CAMPIONE_MAPPING.values())

    @classmethod
    def scan_scarico_ore_rows(cls, file_path: str) -> int:
        """Stima rapida delle righe per Scarico Ore (DataEase) per calcolo ETA."""
        path = Path(file_path)
        if not path.exists(): return 0

        # Use zipfile to read dimension from xml without full load
        try:
            with zipfile.ZipFile(path, 'r') as z:
                # Try to find the sheet. Usually sheet1 if it's the only one, or lookup in workbook.xml
                # For speed, assume "SCARICO ORE" is likely one of the first few sheets or search largest xml.

                # Check worksheet rels or just check dimensions in all worksheets and take the largest?
                # Faster: Parse xl/worksheets/sheetX.xml and look for <dimension ref="A1:L130000"/>

                # Let's try to find the sheet "SCARICO ORE" via workbook.xml if possible, but
                # iterating all sheet xmls is fast enough.
                max_rows = 0
                for name in z.namelist():
                    if name.startswith("xl/worksheets/sheet"):
                        with z.open(name) as f:
                            # Read first 1024 bytes which usually contain <dimension>
                            head = f.read(1024).decode('utf-8', errors='ignore')
                            match = re.search(r'<dimension ref="[A-Z]+[0-9]+:[A-Z]+(\d+)"', head)
                            if match:
                                r = int(match.group(1))
                                if r > max_rows: max_rows = r
                return max_rows
        except Exception:
            return 0

    @classmethod
    def scan_workload(cls, file_path: str, giornaliere_path: str) -> Tuple[int, int]:
        """Scansiona rapidamente il carico di lavoro (fogli e file) per stima ETA."""
        sheets = 0
        files = 0

        # 1. Scan Excel Sheets (Fast via ZipFile)
        p_file = Path(file_path)
        if file_path and p_file.exists():
            try:
                with zipfile.ZipFile(p_file, 'r') as z:
                    if 'xl/workbook.xml' in z.namelist():
                        wb_xml = z.read('xl/workbook.xml').decode('utf-8')
                        # Estrai nomi fogli e filtra per anno
                        sheet_names = re.findall(r'name="([^"]+)"', wb_xml)
                        sheets = len([s for s in sheet_names if re.search(r'(\d{4})', s)])
            except Exception:
                sheets = 1

        # 2. Scan Giornaliere (Files)
        p_giorn = Path(giornaliere_path)
        if giornaliere_path and p_giorn.exists():
             current_year = datetime.now().year
             for folder in p_giorn.iterdir():
                 if folder.is_dir():
                     match = re.match(r'Giornaliere\s+(\d{4})', folder.name, re.IGNORECASE)
                     if match:
                         year = int(match.group(1))
                         if year >= current_year:
                             files += len([f for f in folder.glob("*.xls*") if not f.name.startswith("~$")])

        return sheets, files

    @classmethod
    def init_db(cls):
        """Inizializza il database tramite DatabaseManager."""
        db_manager.init_db()

    @classmethod
    def import_data_from_excel(cls, file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str, int, int]:
        """Importa i dati dal file Excel specificato (Tabella Dati)."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", 0, 0

        total_added = 0
        total_removed = 0

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                xls = pd.ExcelFile(path, engine='openpyxl')
                imported_years = []

                # Use Manager Connection
                with db_manager.get_connection(cls.DB_PATH) as conn:
                    cursor = conn.cursor()

                    # Count valid sheets first for progress
                valid_sheets = [s for s in xls.sheet_names if re.search(r'(\d{4})', s)]
                total_sheets = len(valid_sheets)
                processed_sheets = 0

                for sheet_name in xls.sheet_names:
                    match = re.search(r'(\d{4})', sheet_name)
                    if not match: continue
                    year = int(match.group(1))
                    if not (2000 <= year <= 2100): continue

                    try:
                        df = pd.read_excel(xls, sheet_name=sheet_name, header=1)
                        if not df.empty: df = df.iloc[:-1]
                        df.columns = [str(c).strip().upper() for c in df.columns]
                        df.dropna(how='all', inplace=True)
                        if df.empty: continue

                        df['year'] = year
                        rename_map = {k: v for k, v in cls.COLUMNS_MAPPING.items() if k in df.columns}
                        df.rename(columns=rename_map, inplace=True)

                        for db_col in cls.COLUMNS_MAPPING.values():
                            if db_col not in df.columns: df[db_col] = ""

                        target_columns = ['year'] + list(cls.COLUMNS_MAPPING.values())
                        df = df[target_columns]
                        df = df.fillna("")
                        cols_to_str = [c for c in df.columns if c != 'year']
                        df[cols_to_str] = df[cols_to_str].astype(str)

                        # --- Diff Logic ---
                        # Fetch existing rows for this year (excluding ID/timestamp)
                        # We use the exact same columns as target_columns
                        cursor.execute(f"SELECT {', '.join(target_columns)} FROM contabilita WHERE year = ?", (year,))
                        # Convert to set of tuples
                        # Note: DB returns tuples. Pandas iterrows/itertuples also produces tuples.
                        # Types must match (we coerced df to str except year). DB might return int/str.
                        # We convert DB result to str where needed to match df.
                        # Actually we cast df[cols_to_str] to str. 'year' is int.

                        existing_rows = set()
                        for row in cursor.fetchall():
                            # row[0] is year (int), others are strings or None.
                            # We force strings for non-year cols to match DF preparation.
                            cleaned_row = [row[0]] + [str(x) if x is not None else "" for x in row[1:]]
                            existing_rows.add(tuple(cleaned_row))

                        # New rows from DF
                        new_rows_list = list(df.itertuples(index=False, name=None))
                        new_rows_set = set(new_rows_list)

                        added = len(new_rows_set - existing_rows)
                        removed = len(existing_rows - new_rows_set)

                        total_added += added
                        total_removed += removed
                        # ------------------

                        cursor.execute("DELETE FROM contabilita WHERE year = ?", (year,))
                        placeholders = ', '.join(['?'] * len(target_columns))
                        query = f"INSERT INTO contabilita ({', '.join(target_columns)}) VALUES ({placeholders})"
                        cursor.executemany(query, new_rows_list)
                        imported_years.append(year)

                        processed_sheets += 1
                        if progress_callback:
                            progress_callback(processed_sheets, total_sheets)

                    except Exception as e:
                        print(f"Errore importazione Dati foglio {sheet_name}: {e}")
                        continue

                    conn.commit()

                if not imported_years: return False, "Nessun anno importato.", 0, 0
                return True, f"Anni importati: {sorted(imported_years)}", total_added, total_removed

        except Exception as e:
            return False, f"Errore: {e}", 0, 0

    @classmethod
    def import_giornaliere(cls, root_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str, int, int]:
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata.", 0, 0

        current_year = datetime.now().year
        imported_years = set()

        total_added = 0
        total_removed = 0

        try:
            # 1. Scan and collect files (Flattened loop for progress)
            tasks = []
            for folder in root.iterdir():
                if not folder.is_dir(): continue
                match = re.match(r'Giornaliere\s+(\d{4})', folder.name, re.IGNORECASE)
                if not match: continue

                year = int(match.group(1))
                if year < current_year: continue

                # Collect files
                for file_path in folder.glob("*.xls*"):
                    if not file_path.name.startswith("~$"):
                        tasks.append((year, file_path))

            total_tasks = len(tasks)
            processed_count = 0

            # 1.1 Diff Logic Preparation
            # Collect all new rows in memory first to compare against DB
            all_new_rows = [] # List of tuples matching DB schema

            # Columns definition for consistent ordering
            target_cols = ['year', 'data', 'personale', 'descrizione', 'tcl', 'odc', 'pdl', 'inizio', 'fine', 'ore', 'n_prev', 'nome_file']

            # Lookup map cache
            lookup_map = {}
            try:
                with db_manager.get_connection(cls.DB_PATH, read_only=True) as conn:
                    lookup_query = "SELECT n_prev, odc FROM contabilita WHERE odc IS NOT NULL AND odc != ''"
                    lookup_df = pd.read_sql_query(lookup_query, conn)
                    lookup_df = lookup_df.drop_duplicates(subset=['n_prev'])
                    lookup_map = dict(zip(lookup_df['n_prev'], lookup_df['odc']))
            except: pass

            # 2. Process Files (Read and Accumulate)
            # We process files first to build the "New State", then we diff, then write.
            # This differs slightly from original loop but is safer for diffing.

            years_encountered = set()

            for year, file_path in tasks:
                years_encountered.add(year)
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        try:
                            df = pd.read_excel(file_path, sheet_name='RIASSUNTO', engine='openpyxl')
                        except ValueError:
                            processed_count += 1
                            if progress_callback: progress_callback(processed_count, total_tasks)
                            continue

                        df.columns = [str(c).strip() for c in df.columns]
                        if not df.empty: df = df.iloc[:-1]

                        rename_map = {}
                        for excel_col, db_col in cls.GIORNALIERE_MAPPING.items():
                            for c in df.columns:
                                if c.upper() == excel_col.upper():
                                    rename_map[c] = db_col
                                    break

                        if not rename_map:
                            processed_count += 1
                            if progress_callback: progress_callback(processed_count, total_tasks)
                            continue

                        df.rename(columns=rename_map, inplace=True)
                        check_cols = [c for c in df.columns if c in cls.GIORNALIERE_MAPPING.values() and c != 'data']
                        if check_cols: df.dropna(how='all', subset=check_cols, inplace=True)

                        if not df.empty:
                            for db_col in cls.GIORNALIERE_MAPPING.values():
                                if db_col not in df.columns: df[db_col] = ""

                            cols_to_clean = ['odc', 'n_prev', 'data', 'personale', 'descrizione', 'tcl', 'pdl', 'inizio', 'fine', 'ore']
                            df[cols_to_clean] = df[cols_to_clean].astype(str).apply(lambda x: x.str.strip())
                            df[cols_to_clean] = df[cols_to_clean].replace(r'(?i)^nan$', '', regex=True)

                            # Apply Lookup
                            mask_empty_odc = df['odc'] == ""
                            if mask_empty_odc.any() and lookup_map:
                                mapped_values = df.loc[mask_empty_odc, 'n_prev'].map(lookup_map)
                                df.loc[mask_empty_odc, 'odc'] = mapped_values.fillna("")

                            # Regex
                            mask_canone = df['odc'].str.contains('canone', case=False, na=False)
                            mask_standard = ~mask_canone
                            extracted = df.loc[mask_standard, 'odc'].str.extract(r'(5400\d+)', expand=False)
                            df.loc[mask_standard, 'odc'] = extracted.fillna("")

                            df['year'] = year
                            df['nome_file'] = file_path.name

                            df_final = df[target_cols]
                            rows = list(df_final.itertuples(index=False, name=None))
                            all_new_rows.extend(rows)

                        imported_years.add(year)

                except Exception as e:
                    print(f"Errore lettura file {file_path}: {e}")

                processed_count += 1
                if progress_callback: progress_callback(processed_count, total_tasks)

            # 3. Diff and Commit
            with db_manager.get_connection(cls.DB_PATH) as conn:
                conn.row_factory = sqlite3.Row # Temp setting
                cursor = conn.cursor()

                years_to_clear = years_encountered # Only clear years we touched

                # Fetch Existing
                existing_rows_set = set()
                for year in years_to_clear:
                    cursor.execute(f"SELECT {', '.join(target_cols)} FROM giornaliere WHERE year = ?", (year,))
                    for row in cursor.fetchall():
                        # Ensure types match (year is int, others strings)
                        row_list = [row[0]] + [str(x) if x is not None else "" for x in row[1:]]
                        existing_rows_set.add(tuple(row_list))

                new_rows_set = set(all_new_rows)

                total_added = len(new_rows_set - existing_rows_set)
                total_removed = len(existing_rows_set - new_rows_set)

                # Delete old
                for year in years_to_clear:
                    cursor.execute("DELETE FROM giornaliere WHERE year = ?", (year,))

                # Insert new
                if all_new_rows:
                    placeholders = ', '.join(['?'] * len(target_cols))
                    query = f"INSERT INTO giornaliere ({', '.join(target_cols)}) VALUES ({placeholders})"
                    # Batch insert is efficient
                    cursor.executemany(query, all_new_rows)

                conn.commit()

            if not imported_years and total_tasks == 0:
                return True, "Nessuna nuova giornaliera trovata (check anno >= " + str(current_year) + ").", 0, 0
            return True, f"Importate Giornaliere: {sorted(list(imported_years))}", total_added, total_removed

        except Exception as e:
            return False, f"Errore importazione Giornaliere: {e}", 0, 0

    @classmethod
    def import_attivita_programmate(cls, file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str, int, int]:
        """Importa il file Attività Programmate con stili (colori)."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Attività Programmate non trovato: {file_path}", 0, 0

        if not openpyxl:
            return False, "Modulo 'openpyxl' mancante.", 0, 0

        total_added = 0
        total_removed = 0

        try:
            # Load Workbook with styles
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
                # read_only=False required for style extraction
                wb = openpyxl.load_workbook(path, data_only=True, read_only=False)

            if "Riepilogo" not in wb.sheetnames:
                return False, "Foglio 'Riepilogo' non trovato.", 0, 0

            ws = wb["Riepilogo"]

            # Header is at row 3 (1-based)
            header_row_idx = 3
            data_start_row = 4

            # Map columns
            # We iterate headers to find indices
            col_map = {} # db_col -> 1-based index

            for cell in ws[header_row_idx]:
                if not cell.value: continue
                val_str = str(cell.value)

                mapped_col = None
                for k, v in cls.ATTIVITA_PROGRAMMATE_MAPPING.items():
                    if str(k) == val_str or str(k).strip() == val_str.strip():
                        mapped_col = v
                        break

                if mapped_col:
                    col_map[mapped_col] = cell.column # 1-based index

            if not col_map:
                 return False, "Colonne non trovate. Controlla intestazione riga 3.", 0, 0

            # Cols to insert (including styles)
            db_cols = list(cls.ATTIVITA_PROGRAMMATE_MAPPING.values()) + ['styles']

            rows_to_insert = []

            # Iterate rows
            for row in ws.iter_rows(min_row=data_start_row):
                # Basic check if empty (check first few mapped cols)
                is_empty = True
                for db_key in ['ps', 'area', 'descrizione']:
                    if db_key in col_map:
                        idx = col_map[db_key] - 1 # tuple index
                        if idx < len(row) and row[idx].value:
                            is_empty = False
                            break
                if is_empty: continue

                row_data = {}
                row_styles = {}

                for db_col, col_idx in col_map.items():
                    # col_idx is 1-based, tuple is 0-based relative to row?
                    # iter_rows returns tuple of cells.
                    # If min_col not specified, it returns from col 1.
                    # So tuple index = col_idx - 1
                    cell_idx = col_idx - 1
                    if cell_idx < len(row):
                        cell = row[cell_idx]
                        val = cell.value
                        val_str = str(val).strip() if val is not None else ""
                        if val_str.lower() == 'nan': val_str = ""
                        row_data[db_col] = val_str

                        # Extract Styles
                        fg_color = None
                        bg_color = None

                        if cell.font and cell.font.color:
                            if cell.font.color.type == 'rgb':
                                 c = str(cell.font.color.rgb)
                                 if len(c) > 6: c = "#" + c[2:]
                                 else: c = "#" + c
                                 fg_color = c

                        if cell.fill and cell.fill.patternType == 'solid':
                             if cell.fill.start_color:
                                 if cell.fill.start_color.type == 'rgb':
                                     c = str(cell.fill.start_color.rgb)
                                     if len(c) > 6: c = "#" + c[2:]
                                     else: c = "#" + c
                                     bg_color = c

                        if fg_color or bg_color:
                            style_entry = {}
                            if fg_color: style_entry['fg'] = fg_color
                            if bg_color: style_entry['bg'] = bg_color
                            row_styles[db_col] = style_entry

                # Fill missing cols with empty string
                final_row = []
                for col in cls.ATTIVITA_PROGRAMMATE_MAPPING.values():
                    final_row.append(row_data.get(col, ""))

                final_row.append(json.dumps(row_styles) if row_styles else "")
                rows_to_insert.append(tuple(final_row))

            # DB Update
            with db_manager.get_connection(cls.DB_PATH) as conn:
                cursor = conn.cursor()

                # Diff Logic (Simple count)
                cursor.execute(f"SELECT COUNT(*) FROM attivita_programmate")
                prev_count = cursor.fetchone()[0]

                cursor.execute("DELETE FROM attivita_programmate")

                if rows_to_insert:
                    placeholders = ', '.join(['?'] * len(db_cols))
                    query = f"INSERT INTO attivita_programmate ({', '.join(db_cols)}) VALUES ({placeholders})"
                    cursor.executemany(query, rows_to_insert)

                conn.commit()

            new_count = len(rows_to_insert)
            total_added = max(0, new_count - prev_count)
            total_removed = max(0, prev_count - new_count)

            return True, f"Importate {len(rows_to_insert)} righe in Attività Programmate.", total_added, total_removed

        except Exception as e:
            return False, f"Errore importazione Attività Programmate: {e}", 0, 0

    @classmethod
    def import_scarico_ore(cls, file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str, int, int]:
        """Importa il file Scarico Ore Cantiere con supporto a stili e gestione zeri."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Scarico Ore non trovato: {file_path}", 0, 0

        if not openpyxl:
            return False, "Modulo 'openpyxl' mancante.", 0, 0

        total_added = 0
        total_removed = 0

        try:
            # 1. Decrypt/Load Workbook
            wb_file = io.BytesIO()
            is_encrypted = False

            # Try to check if encrypted using msoffcrypto
            if msoffcrypto:
                try:
                    with open(path, "rb") as f:
                        office_file = msoffcrypto.OfficeFile(f)
                        office_file.load_key(password="coemi")
                        office_file.decrypt(wb_file)
                        is_encrypted = True
                except Exception:
                    # Likely not encrypted or msoffcrypto failed on non-OLE file
                    pass

            if not is_encrypted:
                with open(path, "rb") as f:
                    wb_file.write(f.read())

            wb_file.seek(0)

            # Load with data_only=True first to get values.
            # Performance Note: read_only=False is required for style extraction.
            # This will consume more memory/time for 130k rows but is necessary for the requirement.
            # ⚡ Fix: Suppress UserWarning about Data Validation
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
                wb_data = openpyxl.load_workbook(wb_file, data_only=True, read_only=False)

            if "SCARICO ORE" not in wb_data.sheetnames:
                 return False, "Foglio 'SCARICO ORE' non trovato.", 0, 0
            ws_data = wb_data["SCARICO ORE"]

            # 2. Iterate and Extract
            rows_to_insert = []

            # Header is at row 5 (1-based), data starts at row 6
            start_row = 6

            # Column Mapping (0-based relative to row array or explicit indices)
            # Excel Cols: B=Data, C=Pers1, D=Pers2, E=ODC, F=POS, G=Dalle, H=Alle, I=TotOre, J=Desc, K=Finito, L=Commessa
            # openpyxl cols (1-based): B=2, C=3, ..., L=12
            col_indices = {
                'data': 2, 'pers1': 3, 'pers2': 4, 'odc': 5, 'pos': 6,
                'dalle': 7, 'alle': 8, 'totale_ore': 9, 'descrizione': 10,
                'finito': 11, 'commessa': 12
            }

            # Pre-calc column keys for JSON styles
            col_keys = list(col_indices.keys())
            total_rows = ws_data.max_row

            for row_idx, row in enumerate(ws_data.iter_rows(min_row=start_row, min_col=2, max_col=12), start=start_row):
                if progress_callback and row_idx % 200 == 0:
                    progress_callback(row_idx, total_rows)

                # row is a tuple of Cells
                # Index in tuple: 0=B, 1=C, ... 10=L

                # Check empty row (logic: if Pers1...TotOre are empty)
                # Tuple indices: 1(Pers1) to 7(TotOre)
                # Check if all None/Empty
                subset_vals = [c.value for i, c in enumerate(row) if 1 <= i <= 7]
                if all(v is None or str(v).strip() == "" for v in subset_vals):
                    continue

                row_vals = {}
                row_styles = {}

                for i, key in enumerate(col_keys):
                    cell = row[i]
                    val = cell.value

                    # --- Zero Logic ---
                    # ODC (idx 3 in tuple, col 5), POS (idx 4 in tuple, col 6)
                    # COMMESSA (idx 10 in tuple, col 12)

                    if key in ['odc', 'pos']:
                        if val == 0 or str(val).strip() == "0":
                            val = ""
                    elif key == 'commessa':
                        if val == 0: # Numerical 0
                            val = "0" # Force string "0"
                        # If None/Empty, remains None

                    # Convert to string safely
                    val_str = str(val).strip() if val is not None else ""
                    row_vals[key] = val_str

                    # --- Style Logic ---
                    # Extract FG/BG color
                    fg_color = None
                    bg_color = None

                    # Font Color
                    if cell.font and cell.font.color:
                        # rgb can be ARGB hex string or Theme index
                        if cell.font.color.type == 'rgb':
                             # '00000000' or 'FFFFFFFF'
                             # Often 'FF000000' (ARGB). We need RGB.
                             c = str(cell.font.color.rgb)
                             if len(c) > 6: c = "#" + c[2:] # Strip alpha
                             else: c = "#" + c
                             fg_color = c

                    # Fill Color
                    if cell.fill and cell.fill.patternType == 'solid':
                         if cell.fill.start_color:
                             if cell.fill.start_color.type == 'rgb':
                                 c = str(cell.fill.start_color.rgb)
                                 if len(c) > 6: c = "#" + c[2:]
                                 else: c = "#" + c
                                 bg_color = c

                    if fg_color or bg_color:
                        style_entry = {}
                        if fg_color: style_entry['fg'] = fg_color
                        if bg_color: style_entry['bg'] = bg_color
                        # Key index matches column index (0-based in output tuple)
                        row_styles[key] = style_entry

                # Prepare DB Row
                db_row = (
                    row_vals['data'],
                    row_vals['pers1'],
                    row_vals['pers2'],
                    row_vals['odc'],
                    row_vals['pos'],
                    row_vals['dalle'],
                    row_vals['alle'],
                    row_vals['totale_ore'],
                    row_vals['descrizione'],
                    row_vals['finito'],
                    row_vals['commessa'],
                    json.dumps(row_styles) if row_styles else ""
                )
                rows_to_insert.append(db_row)

            # 3. Diff and Update DB
            with db_manager.get_connection(cls.DB_PATH) as conn:
                cursor = conn.cursor()

                # Diff Logic
                cols = cls.SCARICO_ORE_COLS
                cursor.execute(f"SELECT {', '.join(cols)} FROM scarico_ore")
                existing_rows_set = set(cursor.fetchall())

                new_rows_set = set(rows_to_insert)

                total_added = len(new_rows_set - existing_rows_set)
                total_removed = len(existing_rows_set - new_rows_set)

                cursor.execute("DELETE FROM scarico_ore") # Full refresh

                if rows_to_insert:
                    placeholders = ', '.join(['?'] * len(cols))
                    query = f"INSERT INTO scarico_ore ({', '.join(cols)}) VALUES ({placeholders})"
                    cursor.executemany(query, rows_to_insert)

                conn.commit()

            return True, f"Importate {len(rows_to_insert)} righe da Scarico Ore.", total_added, total_removed

        except Exception as e:
            return False, f"Errore importazione Scarico Ore: {e}", 0, 0

    @classmethod
    def get_available_years(cls) -> List[int]:
        """Restituisce la lista degli anni presenti nel DB (unione di Dati e Giornaliere)."""
        if not cls.DB_PATH.exists(): return []
        try:
            with db_manager.get_connection(cls.DB_PATH, read_only=True) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT year FROM contabilita UNION SELECT DISTINCT year FROM giornaliere ORDER BY 1 DESC")
                years = [row[0] for row in cursor.fetchall()]
                return years
        except: return []

    @classmethod
    def get_data_by_year(cls, year: int) -> List[Tuple]:
        """Restituisce i dati tabella Dati per un anno specifico."""
        if not cls.DB_PATH.exists(): return []
        try:
            with db_manager.get_connection(cls.DB_PATH, read_only=True) as conn:
                cursor = conn.cursor()
                cols = [
                    'data_prev', 'mese', 'n_prev', 'totale_prev', 'attivita', 'tcl', 'odc',
                    'stato_attivita', 'tipologia', 'ore_sp', 'resa', 'annotazioni',
                    'indirizzo_consuntivo', 'nome_file'
                ]
                query = f"SELECT {', '.join(cols)} FROM contabilita WHERE year = ? ORDER BY n_prev DESC, id DESC"
                cursor.execute(query, (year,))
                rows = cursor.fetchall()
                return rows
        except: return []

    @classmethod
    def get_giornaliere_by_year(cls, year: int) -> List[Tuple]:
        """Restituisce i dati Giornaliere per un anno specifico."""
        if not cls.DB_PATH.exists(): return []
        try:
            with db_manager.get_connection(cls.DB_PATH, read_only=True) as conn:
                cursor = conn.cursor()
                cols = ['data', 'personale', 'tcl', 'descrizione', 'n_prev', 'odc', 'pdl', 'inizio', 'fine', 'ore', 'nome_file']
                query = f"SELECT {', '.join(cols)} FROM giornaliere WHERE year = ? ORDER BY data DESC, id DESC"
                cursor.execute(query, (year,))
                rows = cursor.fetchall()
                return rows
        except: return []

    @classmethod
    def get_attivita_programmate_data(cls) -> List[Tuple]:
        """Restituisce i dati Attività Programmate (inclusi stili)."""
        if not cls.DB_PATH.exists(): return []
        try:
            with db_manager.get_connection(cls.DB_PATH, read_only=True) as conn:
                cursor = conn.cursor()
                cols = cls.ATTIVITA_PROGRAMMATE_COLS
                query = f"SELECT {', '.join(cols)} FROM attivita_programmate ORDER BY id ASC"
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except: return []

    @classmethod
    def import_certificati_campione(cls, file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str, int, int]:
        """Importa il file Certificati Campione."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Certificati Campione non trovato: {file_path}", 0, 0

        total_added = 0
        total_removed = 0

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Sheet: strumenti campione ISAB SUD
                # Header row: 6 (index 5)
                try:
                    df = pd.read_excel(path, sheet_name="strumenti campione ISAB SUD", header=5, engine='openpyxl')
                except Exception as e:
                     return False, f"Errore lettura file Certificati: {e}", 0, 0

                if df.empty: return False, "Foglio vuoto.", 0, 0

                # Rename columns
                df.columns = [str(c).strip() for c in df.columns]

                # Check mapping
                rename_map = {}
                for excel_col, db_col in cls.CERTIFICATI_CAMPIONE_MAPPING.items():
                    if excel_col in df.columns:
                        rename_map[excel_col] = db_col

                if not rename_map:
                     return False, "Nessuna colonna valida trovata per Certificati Campione.", 0, 0

                df.rename(columns=rename_map, inplace=True)

                # Filter cols
                target_cols = list(cls.CERTIFICATI_CAMPIONE_MAPPING.values())
                # Add missing
                for c in target_cols:
                    if c not in df.columns: df[c] = ""

                df = df[target_cols]

                # Filter empty rows (mandatory check on matricola or id_coemi?)
                df.dropna(how='all', inplace=True)

                # Format Dates: scadenza, emissione -> DD/MM/YYYY
                def format_date_it(val):
                    if pd.isna(val) or val == "": return ""
                    try:
                        dt = pd.to_datetime(val)
                        return dt.strftime("%d/%m/%Y")
                    except:
                        return str(val)

                df['scadenza'] = df['scadenza'].apply(format_date_it)
                df['emissione'] = df['emissione'].apply(format_date_it)

                # Format Stato: Transform numeric values (days diff) to user-friendly string
                # If Excel formula returns a number like 133 or -985, we format it.
                def format_stato(val):
                    if pd.isna(val) or val == "": return ""
                    try:
                        # Try parsing as float first
                        num = float(val)
                        days = int(round(num))
                        if days > 0:
                            return f"Scade tra {days} giorni"
                        elif days < 0:
                            return f"Scaduto da {abs(days)} giorni"
                        else:
                            return "Scade oggi"
                    except ValueError:
                        # Not a number, maybe already text or invalid
                        return str(val)

                if 'stato' in df.columns:
                    df['stato'] = df['stato'].apply(format_stato)

                # Fill N/A and convert to str
                df = df.fillna("")
                df = df.astype(str)

                rows = list(df.itertuples(index=False, name=None))

                # DB Ops
                with db_manager.get_connection(cls.DB_PATH) as conn:
                    cursor = conn.cursor()

                    cursor.execute("DELETE FROM certificati_campione")

                    if rows:
                        placeholders = ', '.join(['?'] * len(target_cols))
                        query = f"INSERT INTO certificati_campione ({', '.join(target_cols)}) VALUES ({placeholders})"
                        cursor.executemany(query, rows)

                    conn.commit()

                return True, f"Importate {len(rows)} righe in Certificati Campione.", len(rows), 0

        except Exception as e:
            return False, f"Errore importazione Certificati Campione: {e}", 0, 0

    @classmethod
    def get_certificati_campione_data(cls) -> List[Tuple]:
        """Restituisce i dati Certificati Campione."""
        if not cls.DB_PATH.exists(): return []
        try:
            with db_manager.get_connection(cls.DB_PATH, read_only=True) as conn:
                cursor = conn.cursor()
                cols = cls.CERTIFICATI_CAMPIONE_COLS
                query = f"SELECT {', '.join(cols)} FROM certificati_campione ORDER BY id ASC"
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except: return []

    @classmethod
    def get_scarico_ore_data(cls) -> List[Tuple]:
        """Restituisce tutti i dati della tabella scarico_ore inclusi gli stili."""
        if not cls.DB_PATH.exists(): return []
        try:
            with db_manager.get_connection(cls.DB_PATH, read_only=True) as conn:
                cursor = conn.cursor()
                cols = cls.SCARICO_ORE_COLS
                query = f"SELECT {', '.join(cols)} FROM scarico_ore ORDER BY id DESC"
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except:
            return []

    @classmethod
    def get_year_stats(cls, year: int) -> Dict:
        """Calcola statistiche avanzate per l'anno specificato (Tabella Dati) + KPI Diretti/Indiretti."""
        data = cls.get_data_by_year(year)

        # Recupera anche Giornaliere per calcolo Dirette/Indirette (basato su richiesta utente)
        # "Se in giornaliera, una riga è associata ad un n°prev oppure ODC, allora è una spesa ore diretta altrimenti è una spesa ore indiretta."
        giornaliere = cls.get_giornaliere_by_year(year)

        stats = {
            "total_prev": 0.0,
            "total_ore": 0.0,
            "count_total": 0,
            "status_counts": {},
            "top_commesse": [],
            # New Metrics
            "ore_dirette": 0.0,
            "ore_indirette": 0.0
        }

        # 1. Stats from Dati (Contabilita)
        commesse = []
        if data:
            for row in data:
                try:
                    # row indices: 2=n_prev, 3=totale_prev, 4=attivita, 7=stato, 9=ore_sp, 10=resa
                    n_prev = str(row[2]).strip()
                    if not n_prev: continue
                    if "totale" in n_prev.lower(): continue

                    val_prev = parse_currency(row[3])
                    val_ore = parse_currency(row[9]) # Ore from 'Dati' table

                    stats["total_prev"] += val_prev
                    stats["total_ore"] += val_ore
                    stats["count_total"] += 1

                    status = str(row[7]).strip().upper()
                    if status:
                        stats["status_counts"][status] = stats["status_counts"].get(status, 0) + 1

                    if val_prev > 0:
                        attivita = str(row[4]).strip() or "N/D"
                        commesse.append((attivita, val_prev))
                except:
                    pass

        stats["top_commesse"] = sorted(commesse, key=lambda x: x[1], reverse=True)[:5]

        # 2. Stats from Giornaliere (Direct vs Indirect)
        # Giornaliere Cols: data, personale, tcl, descrizione, n_prev, odc, pdl, inizio, fine, ore, nome_file
        # Index: 4=n_prev, 5=odc, 9=ore
        if giornaliere:
            for row in giornaliere:
                try:
                    n_prev = str(row[4]).strip()
                    odc = str(row[5]).strip()
                    # Clean placeholders
                    if n_prev.lower() == 'nan': n_prev = ""
                    if odc.lower() == 'nan': odc = ""

                    ore = parse_currency(row[9])

                    # Logic: Associated with N_PREV OR ODC -> Direct
                    if n_prev or odc:
                        stats["ore_dirette"] += ore
                    else:
                        stats["ore_indirette"] += ore
                except:
                    pass

        return stats
