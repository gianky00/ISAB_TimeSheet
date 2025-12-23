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
        """Inizializza il database creando le tabelle se non esistono e abilita WAL."""
        cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(cls.DB_PATH)
        # Enable WAL mode for concurrency
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
        except Exception as e:
            print(f"Warning: Could not set WAL mode: {e}")

        cursor = conn.cursor()

        # Tabella Contabilita (Dati)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contabilita (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                data_prev TEXT,
                mese TEXT,
                n_prev TEXT,
                totale_prev TEXT,
                attivita TEXT,
                tcl TEXT,
                odc TEXT,
                stato_attivita TEXT,
                tipologia TEXT,
                ore_sp TEXT,
                resa TEXT,
                annotazioni TEXT,
                indirizzo_consuntivo TEXT,
                nome_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabella Giornaliere
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS giornaliere (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                data TEXT,
                personale TEXT,
                descrizione TEXT,
                tcl TEXT,
                odc TEXT,
                pdl TEXT,
                inizio TEXT,
                fine TEXT,
                ore TEXT,
                n_prev TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Migrazione schema Giornaliere: Aggiungi colonna nome_file se non esiste
        try:
            cursor.execute("ALTER TABLE giornaliere ADD COLUMN nome_file TEXT")
        except sqlite3.OperationalError:
            pass

        # Tabella Scarico Ore Cantiere (Nuova con styles)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scarico_ore (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                pers1 TEXT,
                pers2 TEXT,
                odc TEXT,
                pos TEXT,
                dalle TEXT,
                alle TEXT,
                totale_ore TEXT,
                descrizione TEXT,
                finito TEXT,
                commessa TEXT,
                styles TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Migrazione schema scarico_ore: Aggiungi colonna styles se non esiste
        try:
            cursor.execute("ALTER TABLE scarico_ore ADD COLUMN styles TEXT")
        except sqlite3.OperationalError:
            pass

        conn.commit()
        conn.close()

    @classmethod
    def import_data_from_excel(cls, file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str]:
        """Importa i dati dal file Excel specificato (Tabella Dati)."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}"

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                xls = pd.ExcelFile(path, engine='openpyxl')
                imported_years = []
                conn = sqlite3.connect(cls.DB_PATH)
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

                        cursor.execute("DELETE FROM contabilita WHERE year = ?", (year,))
                        placeholders = ', '.join(['?'] * len(target_columns))
                        query = f"INSERT INTO contabilita ({', '.join(target_columns)}) VALUES ({placeholders})"
                        values = list(df.itertuples(index=False, name=None))
                        cursor.executemany(query, values)
                        imported_years.append(year)

                        processed_sheets += 1
                        if progress_callback:
                            progress_callback(processed_sheets, total_sheets)

                    except Exception as e:
                        print(f"Errore importazione Dati foglio {sheet_name}: {e}")
                        continue

                conn.commit()
                conn.close()
                if not imported_years: return False, "Nessun anno importato."
                return True, f"Anni importati: {sorted(imported_years)}"

        except Exception as e:
            return False, f"Errore: {e}"

    @classmethod
    def import_giornaliere(cls, root_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str]:
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata."

        current_year = datetime.now().year
        imported_years = set()

        try:
            conn = sqlite3.connect(cls.DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

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

            # Pre-clear years involved
            years_to_clear = set(t[0] for t in tasks)
            for year in years_to_clear:
                cursor.execute("DELETE FROM giornaliere WHERE year = ?", (year,))

            # 2. Process Files
            for year, file_path in tasks:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        try:
                            df = pd.read_excel(file_path, sheet_name='RIASSUNTO', engine='openpyxl')
                        except ValueError:
                            # Skip if sheet not found
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
                            # Ensure all expected DB columns exist
                            for db_col in cls.GIORNALIERE_MAPPING.values():
                                if db_col not in df.columns: df[db_col] = ""

                            # --- ⚡ Bolt Optimization: Vectorized Processing ---
                            # Clean string columns (vectorized)
                            cols_to_clean = ['odc', 'n_prev', 'data', 'personale', 'descrizione', 'tcl', 'pdl', 'inizio', 'fine', 'ore']
                            # Convert to string and strip whitespace
                            df[cols_to_clean] = df[cols_to_clean].astype(str).apply(lambda x: x.str.strip())
                            # Replace 'nan' (case insensitive) with empty string
                            df[cols_to_clean] = df[cols_to_clean].replace(r'(?i)^nan$', '', regex=True)

                            # Vectorized Regex for ODC: Extract '5400...' pattern
                            # If no match, it returns NaN, which we fill with ""
                            df['odc'] = df['odc'].str.extract(r'(5400\d+)', expand=False).fillna("")

                            # Add Metadata
                            df['year'] = year
                            df['nome_file'] = file_path.name

                            # Select and Order Columns for DB
                            target_cols = ['year', 'data', 'personale', 'descrizione', 'tcl', 'odc', 'pdl', 'inizio', 'fine', 'ore', 'n_prev', 'nome_file']
                            df_final = df[target_cols]

                            # Convert to list of tuples (High speed export)
                            rows_to_insert = list(df_final.itertuples(index=False, name=None))
                            # --------------------------------------------------

                            if rows_to_insert:
                                cols = target_cols
                                placeholders = ', '.join(['?'] * len(cols))
                                query = f"INSERT INTO giornaliere ({', '.join(cols)}) VALUES ({placeholders})"
                                cursor.executemany(query, rows_to_insert)

                        imported_years.add(year)

                except Exception as e:
                    print(f"Errore lettura file {file_path}: {e}")

                processed_count += 1
                if progress_callback: progress_callback(processed_count, total_tasks)

            conn.commit()
            conn.close()

            if not imported_years and total_tasks == 0:
                return True, "Nessuna nuova giornaliera trovata (check anno >= " + str(current_year) + ")."
            return True, f"Importate Giornaliere: {sorted(list(imported_years))}"

        except Exception as e:
            return False, f"Errore importazione Giornaliere: {e}"

    @classmethod
    def import_scarico_ore(cls, file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str]:
        """Importa il file Scarico Ore Cantiere con supporto a stili e gestione zeri."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Scarico Ore non trovato: {file_path}"

        if not openpyxl:
            return False, "Modulo 'openpyxl' mancante."

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
                 return False, "Foglio 'SCARICO ORE' non trovato."
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

            # 3. Update DB
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM scarico_ore") # Full refresh

            if rows_to_insert:
                cols = cls.SCARICO_ORE_COLS
                placeholders = ', '.join(['?'] * len(cols))
                query = f"INSERT INTO scarico_ore ({', '.join(cols)}) VALUES ({placeholders})"
                cursor.executemany(query, rows_to_insert)

            conn.commit()
            conn.close()

            return True, f"Importate {len(rows_to_insert)} righe da Scarico Ore."

        except Exception as e:
            return False, f"Errore importazione Scarico Ore: {e}"

    @classmethod
    def get_available_years(cls) -> List[int]:
        """Restituisce la lista degli anni presenti nel DB (unione di Dati e Giornaliere)."""
        if not cls.DB_PATH.exists(): return []
        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT year FROM contabilita UNION SELECT DISTINCT year FROM giornaliere ORDER BY 1 DESC")
            years = [row[0] for row in cursor.fetchall()]
            conn.close()
            return years
        except: return []

    @classmethod
    def get_data_by_year(cls, year: int) -> List[Tuple]:
        """Restituisce i dati tabella Dati per un anno specifico."""
        if not cls.DB_PATH.exists(): return []
        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            cols = [
                'data_prev', 'mese', 'n_prev', 'totale_prev', 'attivita', 'tcl', 'odc',
                'stato_attivita', 'tipologia', 'ore_sp', 'resa', 'annotazioni',
                'indirizzo_consuntivo', 'nome_file'
            ]
            # Ordinamento richiesto: N°PREV. (n_prev) dal più recente (DESC)
            query = f"SELECT {', '.join(cols)} FROM contabilita WHERE year = ? ORDER BY n_prev DESC, id DESC"
            cursor.execute(query, (year,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except: return []

    @classmethod
    def get_giornaliere_by_year(cls, year: int) -> List[Tuple]:
        """Restituisce i dati Giornaliere per un anno specifico."""
        if not cls.DB_PATH.exists(): return []
        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            # Ordine richiesto UI aggiornato:
            # data, personale, tcl, descrizione, n_prev, odc, pdl, inizio, fine, ore
            # Aggiunto nome_file in coda
            cols = ['data', 'personale', 'tcl', 'descrizione', 'n_prev', 'odc', 'pdl', 'inizio', 'fine', 'ore', 'nome_file']
            # Ordinamento richiesto: Data dal più recente (DESC)
            query = f"SELECT {', '.join(cols)} FROM giornaliere WHERE year = ? ORDER BY data DESC, id DESC"
            cursor.execute(query, (year,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except: return []

    @classmethod
    def get_scarico_ore_data(cls) -> List[Tuple]:
        """Restituisce tutti i dati della tabella scarico_ore inclusi gli stili."""
        if not cls.DB_PATH.exists(): return []
        try:
            # Use Read-Only URI if possible, but fallback to standard if not supported by sqlite ver
            # Python's sqlite3 supports URI by default in recent versions
            uri_path = f"file:{cls.DB_PATH.absolute()}?mode=ro"
            conn = sqlite3.connect(uri_path, uri=True)

            cursor = conn.cursor()
            cols = cls.SCARICO_ORE_COLS
            # Order by Data Desc
            query = f"SELECT {', '.join(cols)} FROM scarico_ore ORDER BY id DESC"
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            # Fallback to standard connection if URI fails
            try:
                conn = sqlite3.connect(cls.DB_PATH)
                cursor = conn.cursor()
                cols = cls.SCARICO_ORE_COLS
                query = f"SELECT {', '.join(cols)} FROM scarico_ore ORDER BY id DESC"
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.close()
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
