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
from typing import List, Dict, Tuple, Optional
from datetime import datetime

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

        conn.commit()
        conn.close()

    @classmethod
    def import_data_from_excel(cls, file_path: str) -> Tuple[bool, str]:
        """
        Importa i dati dal file Excel specificato (Tabella Dati).
        """
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
        """Importa le Giornaliere dalla root directory specificata."""
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata."

        current_year = datetime.now().year
        imported_years = []

        try:
            conn = sqlite3.connect(cls.DB_PATH)
            # Row factory per accesso facile ai risultati query lookup
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Cerca cartelle "Giornaliere YYYY"
            for folder in root.iterdir():
                if not folder.is_dir(): continue
                match = re.match(r'Giornaliere\s+(\d{4})', folder.name, re.IGNORECASE)
                if not match: continue

                year = int(match.group(1))
                # Regola: importare solo dal 2025 (anno corrente) in poi
                if year < current_year: continue

                # Cancella dati precedenti per l'anno
                cursor.execute("DELETE FROM giornaliere WHERE year = ?", (year,))

                # Cerca file Excel nella cartella
                excel_files = list(folder.glob("*.xls*"))

                for file_path in excel_files:
                    if file_path.name.startswith("~$"): continue # Ignora temp files

                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            # Leggi solo foglio RIASSUNTO
                            try:
                                df = pd.read_excel(file_path, sheet_name='RIASSUNTO', engine='openpyxl')
                            except ValueError:
                                # Foglio RIASSUNTO non trovato
                                continue

                            # Normalizza colonne
                            df.columns = [str(c).strip() for c in df.columns]

                            # Filtra colonne interessanti
                            rename_map = {}
                            available_cols = []
                            for excel_col, db_col in cls.GIORNALIERE_MAPPING.items():
                                # Cerca case-insensitive
                                found = False
                                for c in df.columns:
                                    if c.upper() == excel_col.upper():
                                        rename_map[c] = db_col
                                        available_cols.append(db_col)
                                        found = True
                                        break
                                if not found:
                                    # Se manca colonna obbligatoria? Creiamo vuota
                                    pass

                            if not rename_map: continue

                            df.rename(columns=rename_map, inplace=True)

                            # Rimuovi righe vuote
                            df.dropna(how='all', inplace=True)

                            # Aggiungi colonne mancanti
                            for db_col in cls.GIORNALIERE_MAPPING.values():
                                if db_col not in df.columns: df[db_col] = ""

                            df['year'] = year

                            # Processamento Righe
                            rows_to_insert = []

                            # Cache per lookup ODC da Dati per velocizzare
                            # Carichiamo mappa n_prev -> odc dalla tabella contabilita per l'anno corrente
                            cursor.execute("SELECT n_prev, odc FROM contabilita WHERE year = ?", (year,))
                            dati_odc_map = {row['n_prev'].strip(): row['odc'].strip() for row in cursor.fetchall() if row['n_prev'] and row['odc']}

                            for _, row in df.iterrows():
                                # 1. Pulisci ODC (Estrai 5400...)
                                raw_odc = str(row.get('odc', '')).strip()
                                match_odc = re.search(r'(5400\d+)', raw_odc)
                                final_odc = match_odc.group(1) if match_odc else ""

                                n_prev = str(row.get('n_prev', '')).strip()

                                # 2. Se ODC vuoto, cerca in Dati tramite n_prev (consuntivo)
                                if not final_odc and n_prev:
                                    # Lookup nella cache
                                    lookup_odc = dati_odc_map.get(n_prev)
                                    if lookup_odc:
                                        # Pulisci anche questo ODC se necessario o prendi raw
                                        match_lookup = re.search(r'(5400\d+)', lookup_odc)
                                        if match_lookup:
                                            final_odc = match_lookup.group(1)
                                        else:
                                            # Se in dati c'è ma non è 5400..., prendiamo comunque?
                                            # La richiesta dice: "estrapolare solo... 5400".
                                            # Se manca, "verificare in Dati... se lo contiene puoi copiarlo".
                                            # Assumiamo di copiare solo se conforme o se non specificato diversamente.
                                            # Copiamo raw se non troviamo pattern, oppure lasciamo vuoto?
                                            # Meglio copiare quello che c'è se trovato.
                                            final_odc = lookup_odc

                                # Prepara riga
                                new_row = (
                                    year,
                                    str(row.get('data', '')),
                                    str(row.get('personale', '')),
                                    str(row.get('descrizione', '')),
                                    str(row.get('tcl', '')),
                                    final_odc,
                                    str(row.get('pdl', '')),
                                    str(row.get('inizio', '')),
                                    str(row.get('fine', '')),
                                    str(row.get('ore', '')),
                                    n_prev
                                )
                                rows_to_insert.append(new_row)

                            # Inserimento bulk per il file
                            if rows_to_insert:
                                cols = ['year', 'data', 'personale', 'descrizione', 'tcl', 'odc', 'pdl', 'inizio', 'fine', 'ore', 'n_prev']
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
            query = f"SELECT {', '.join(cols)} FROM contabilita WHERE year = ? ORDER BY id"
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
            # Ordine richiesto UI: data, personale, descrizione, n_prev, odc, pdl, inizio, fine, ore
            # Ma qui ritorniamo tutto, l'ordine lo decide la UI.
            # Ritorno DB order o struct:
            cols = ['data', 'personale', 'descrizione', 'n_prev', 'odc', 'pdl', 'inizio', 'fine', 'ore', 'tcl']
            query = f"SELECT {', '.join(cols)} FROM giornaliere WHERE year = ? ORDER BY id"
            cursor.execute(query, (year,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except: return []

    @classmethod
    def get_year_stats(cls, year: int) -> Dict:
        """Calcola statistiche avanzate per l'anno specificato (Tabella Dati)."""
        data = cls.get_data_by_year(year)
        if not data: return {}

        stats = {
            "total_prev": 0.0,
            "total_ore": 0.0,
            "count_total": len(data),
            "status_counts": {},
            "top_commesse": []
        }
        commesse = []
        for row in data:
            try:
                t_str = str(row[3]).replace('.','').replace(',','.').replace('€','').strip()
                val_prev = float(t_str) if t_str else 0.0
            except: val_prev = 0.0
            try:
                o_str = str(row[9]).replace(',','.').strip()
                val_ore = float(o_str) if o_str else 0.0
            except: val_ore = 0.0

            stats["total_prev"] += val_prev
            stats["total_ore"] += val_ore

            status = str(row[7]).strip().upper()
            if status:
                stats["status_counts"][status] = stats["status_counts"].get(status, 0) + 1

            if val_prev > 0:
                attivita = str(row[4]).strip() or "N/D"
                commesse.append((attivita, val_prev))

        commesse.sort(key=lambda x: x[1], reverse=True)
        stats["top_commesse"] = commesse[:5]
        return stats
