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
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from src.utils.parsing import parse_currency

# Tentativo di importare msoffcrypto
try:
    import msoffcrypto
except ImportError:
    msoffcrypto = None

class ContabilitaManager:
    """Manager per la gestione del database e dell'importazione Excel."""

    DB_PATH = Path("data/contabilita.db")

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
    # Header riga 5, Col B-L
    # Colonne target: Data, PERS1, PERS2, ODC, POS, DALLE, ALLE, TOTALE ORE, Descrizione Attività, FINITO, COMMESSA
    SCARICO_ORE_MAPPING = {
        'DATA': 'data',
        'PERS1': 'pers1',
        'PERS2': 'pers2',
        'ODC': 'odc',
        'POS': 'pos',
        'DALLE': 'dalle',
        'ALLE': 'alle',
        'TOTALE ORE': 'totale_ore',
        'DESCRIZIONE ATTIVITÀ': 'descrizione',
        'FINITO': 'finito',
        'COMMESSA': 'commessa'
    }

    @classmethod
    def init_db(cls):
        """Inizializza il database creando le tabelle se non esistono."""
        cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(cls.DB_PATH)
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

        # Tabella Scarico Ore Cantiere (Nuova)
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    @classmethod
    def import_data_from_excel(cls, file_path: str) -> Tuple[bool, str]:
        """Importa i dati dal file Excel specificato (Tabella Dati)."""
        # ... (Existing implementation unchanged) ...
        # Copied for brevity, assuming standard implementation if not modified
        # If I need to modify it, I will paste full content.
        # Since I am using overwrite_file_with_block, I MUST Provide FULL Content of the class
        # Re-using the existing logic for this method.
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
    def import_giornaliere(cls, root_path: str) -> Tuple[bool, str]:
        # ... (Existing logic for Giornaliere) ...
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata."

        current_year = datetime.now().year
        imported_years = []

        try:
            conn = sqlite3.connect(cls.DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            for folder in root.iterdir():
                if not folder.is_dir(): continue
                match = re.match(r'Giornaliere\s+(\d{4})', folder.name, re.IGNORECASE)
                if not match: continue

                year = int(match.group(1))
                if year < current_year: continue

                cursor.execute("DELETE FROM giornaliere WHERE year = ?", (year,))
                excel_files = list(folder.glob("*.xls*"))

                for file_path in excel_files:
                    if file_path.name.startswith("~$"): continue

                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            try:
                                df = pd.read_excel(file_path, sheet_name='RIASSUNTO', engine='openpyxl')
                            except ValueError:
                                continue

                            df.columns = [str(c).strip() for c in df.columns]
                            if not df.empty: df = df.iloc[:-1]

                            rename_map = {}
                            for excel_col, db_col in cls.GIORNALIERE_MAPPING.items():
                                found = False
                                for c in df.columns:
                                    if c.upper() == excel_col.upper():
                                        rename_map[c] = db_col
                                        found = True
                                        break
                            if not rename_map: continue

                            df.rename(columns=rename_map, inplace=True)
                            check_cols = [c for c in df.columns if c in cls.GIORNALIERE_MAPPING.values() and c != 'data']
                            if check_cols: df.dropna(how='all', subset=check_cols, inplace=True)
                            if df.empty: continue

                            for db_col in cls.GIORNALIERE_MAPPING.values():
                                if db_col not in df.columns: df[db_col] = ""

                            df['year'] = year
                            filename = file_path.name
                            rows_to_insert = []

                            for _, row in df.iterrows():
                                raw_odc = str(row.get('odc', '')).strip()
                                if raw_odc.lower() == 'nan': raw_odc = ""
                                match_odc = re.search(r'(5400\d+)', raw_odc)
                                final_odc = match_odc.group(1) if match_odc else ""

                                n_prev = str(row.get('n_prev', '')).strip()
                                if n_prev.lower() == 'nan': n_prev = ""

                                new_row = (
                                    year, str(row.get('data', '')), str(row.get('personale', '')),
                                    str(row.get('descrizione', '')), str(row.get('tcl', '')),
                                    final_odc, str(row.get('pdl', '')), str(row.get('inizio', '')),
                                    str(row.get('fine', '')), str(row.get('ore', '')), n_prev, filename
                                )
                                rows_to_insert.append(new_row)

                            if rows_to_insert:
                                cols = ['year', 'data', 'personale', 'descrizione', 'tcl', 'odc', 'pdl', 'inizio', 'fine', 'ore', 'n_prev', 'nome_file']
                                placeholders = ', '.join(['?'] * len(cols))
                                query = f"INSERT INTO giornaliere ({', '.join(cols)}) VALUES ({placeholders})"
                                cursor.executemany(query, rows_to_insert)

                    except Exception as e:
                        print(f"Errore lettura file {file_path}: {e}")
                        continue

                imported_years.append(year)

            conn.commit()
            conn.close()
            if not imported_years:
                return True, "Nessuna nuova giornaliera trovata (check anno >= " + str(current_year) + ")."
            return True, f"Importate Giornaliere: {sorted(imported_years)}"

        except Exception as e:
            return False, f"Errore importazione Giornaliere: {e}"

    @classmethod
    def import_scarico_ore(cls, file_path: str) -> Tuple[bool, str]:
        """Importa il file Scarico Ore Cantiere (DataEase) protetto da password."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File Scarico Ore non trovato: {file_path}"

        try:
            # 1. Decrypt file in memory
            decrypted_workbook = io.BytesIO()

            try:
                if msoffcrypto:
                    with open(path, "rb") as f:
                        office_file = msoffcrypto.OfficeFile(f)
                        office_file.load_key(password="coemi")
                        office_file.decrypt(decrypted_workbook)
                else:
                    return False, "Modulo 'msoffcrypto-tool' mancante. Impossibile aprire file protetto."
            except Exception as e:
                # Fallback: maybe it's not encrypted? Try reading directly
                print(f"Errore decrittazione (o file non criptato?): {e}")
                # Reset stream is pointless if we failed, but let's try direct read just in case
                # Actually, if it fails here, we likely can't proceed unless user provided wrong path or non-excel.
                return False, f"Errore decrittazione file: {e}"

            # 2. Read with Pandas
            # Header riga 5 (index 4)
            # Colonne B:L -> usecols="B:L"
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    df = pd.read_excel(
                        decrypted_workbook,
                        sheet_name="SCARICO ORE",
                        header=4, # Row 5 is header (0-based index 4)
                        usecols="B:L",
                        engine='openpyxl'
                    )
                except ValueError:
                    return False, "Foglio 'SCARICO ORE' non trovato o struttura errata."

            # 3. Clean and Filter
            # Colonne attese: Data, PERS1, PERS2, ODC, POS, DALLE, ALLE, TOTALE ORE, Descrizione Attività, FINITO, COMMESSA
            # Normalizza nomi colonne
            df.columns = [str(c).strip().upper() for c in df.columns]

            # Filter: Check Columns C to I (PERS2 to FINITO approx)
            # C (2) to I (8) in Excel terms relative to A?
            # Input said: "non importare nulla se da cella C a cella I sono vuote."
            # Our DF starts at Col B.
            # B=0 (DATA), C=1 (PERS1), D=2 (PERS2)...
            # Excel Cols: A B C D E F G H I J K L
            # DF Cols Idx:   0 1 2 3 4 5 6 7 8 9 10
            # DF Cols Names: DATA, PERS1, PERS2, ODC, POS, DALLE, ALLE, TOTALE ORE, DESCRIZIONE, FINITO, COMMESSA
            # Check range C:I (Excel) -> PERS1(C) to Descrizione(I)? Wait.
            # Let's map explicitly:
            # A=None
            # B=DATA
            # C=PERS1
            # D=PERS2
            # E=ODC
            # F=POS
            # G=DALLE
            # H=ALLE
            # I=TOTALE ORE
            # J=DESCRIZIONE ATTIVITA
            # K=FINITO
            # L=COMMESSA

            # User said: "non importare nulla se da cella C a cella I sono vuote."
            # C=PERS1, I=TOTALE ORE.
            # So if subset [PERS1, PERS2, ODC, POS, DALLE, ALLE, TOTALE ORE] are ALL empty? Or ANY?
            # Usually "sono vuote" implies all of them in that range.
            # Let's verify mapping against user list "Data,PERS1,PERS2,ODC,POS,DALLE,ALLE,TOTALE ORE,Descrizione Attività,FINITO,COMMESSA"
            # B=Data
            # C=PERS1
            # ...
            # I=TOTALE ORE

            # Subset to check for emptiness:
            cols_to_check = ['PERS1', 'PERS2', 'ODC', 'POS', 'DALLE', 'ALLE', 'TOTALE ORE']
            # Find actual names in DF
            df_cols_map = {}
            for col in df.columns:
                for key in cols_to_check:
                    if key in col: # Loose match
                        df_cols_map[key] = col

            check_list = list(df_cols_map.values())

            if check_list:
                df.dropna(how='all', subset=check_list, inplace=True)

            if df.empty:
                return True, "Nessun dato valido trovato nel file Scarico Ore."

            # 4. Insert into DB
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()

            # Clear old data? Or append? Usually "Database per il file" implies refresh content of that file.
            # Since it's a single file configured, likely refresh full table.
            cursor.execute("DELETE FROM scarico_ore") # Full wipe

            rows_to_insert = []

            # Map DF to DB columns
            # DB: data, pers1, pers2, odc, pos, dalle, alle, totale_ore, descrizione, finito, commessa

            for _, row in df.iterrows():
                # Helper to safely get value
                def get_val(excel_col_name_part):
                    for c in df.columns:
                        if excel_col_name_part in c:
                            val = row[c]
                            if pd.isna(val): return ""
                            return str(val).strip()
                    return ""

                new_row = (
                    get_val('DATA'),
                    get_val('PERS1'),
                    get_val('PERS2'),
                    get_val('ODC'),
                    get_val('POS'),
                    get_val('DALLE'),
                    get_val('ALLE'),
                    get_val('TOTALE ORE'),
                    get_val('DESCRIZIONE'),
                    get_val('FINITO'),
                    get_val('COMMESSA')
                )
                rows_to_insert.append(new_row)

            if rows_to_insert:
                cols = ['data', 'pers1', 'pers2', 'odc', 'pos', 'dalle', 'alle', 'totale_ore', 'descrizione', 'finito', 'commessa']
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
        """Restituisce tutti i dati della tabella scarico_ore."""
        if not cls.DB_PATH.exists(): return []
        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            cols = ['data', 'pers1', 'pers2', 'odc', 'pos', 'dalle', 'alle', 'totale_ore', 'descrizione', 'finito', 'commessa']
            # Order by Data Desc
            query = f"SELECT {', '.join(cols)} FROM scarico_ore ORDER BY id DESC"
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except: return []

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
